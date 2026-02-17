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
        topic="Advanced Metering Infrastructure (AMI): Two-way Communication",
        keywords=["AMI", "two-way communication", "smart meters", "data exchange", "metering", "customer interface"],
        conclusion_template="AMI systems must provide secure, reliable two-way communication between meters and utility control centers to enable real-time data exchange and demand-side management.",
        reasoning_framework="""
The implementation of AMI requires robust two-way communication channels to facilitate real-time data acquisition and remote control. This enables utilities to monitor consumption, detect outages, and implement demand response programs. The framework must address network reliability, data integrity, and security, considering the scale of deployment and heterogeneity of devices. Regulatory compliance (e.g., NERC CIP) and interoperability standards (e.g., IEEE 1701/1702) are critical. Utilities must balance cost, scalability, and privacy concerns, ensuring customer data is protected while enabling operational efficiencies.
        """,
        key_factors=[
            "Network reliability",
            "Data integrity",
            "Cybersecurity",
            "Interoperability standards",
            "Regulatory compliance",
            "Customer privacy",
            "Scalability"
        ],
        primary_authority=[
            "NERC CIP",
            "IEEE 1701/1702",
            "FERC",
            "NIST Smart Grid Framework"
        ],
        burden_holder="Utility operator",
        adversary_position="AMI introduces new attack surfaces and privacy risks that outweigh operational benefits.",
        counter_arguments=[
            "Advanced encryption and authentication mitigate security risks.",
            "Regulatory frameworks enforce privacy protections.",
            "Operational benefits (outage detection, DR) justify investment."
        ],
        resolution_strategy="Adopt layered security, comply with standards, and conduct regular risk assessments.",
        entity_scope="Utility, Meter Vendor, Customer",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FERC Order 2222; NISTIR 7628"
    ),
    DoctrineBlock(
        topic="SCADA: Supervisory Control and Data Acquisition",
        keywords=["SCADA", "supervisory control", "data acquisition", "remote terminal unit", "RTU", "PLC", "HMI"],
        conclusion_template="SCADA systems must ensure real-time, secure, and reliable monitoring and control of grid assets, with redundancy and failover mechanisms.",
        reasoning_framework="""
SCADA systems are foundational for grid operations, providing centralized monitoring and control. The reasoning framework emphasizes the need for real-time data, low-latency communication, and robust failover. Security is paramount due to the critical nature of SCADA, requiring segmentation, encryption, and strict access controls. Integration with legacy devices and modern protocols (e.g., DNP3, IEC 61850) must be managed. Regulatory mandates (NERC CIP) dictate minimum security and reliability standards. Human factors, such as operator training and interface usability, also influence system effectiveness.
        """,
        key_factors=[
            "Real-time data acquisition",
            "Low-latency communication",
            "Redundancy",
            "Cybersecurity",
            "Protocol interoperability",
            "Operator training"
        ],
        primary_authority=[
            "NERC CIP",
            "IEC 61850",
            "DNP3",
            "ISA/IEC 62443"
        ],
        burden_holder="Grid operator",
        adversary_position="SCADA centralization increases risk of catastrophic failure and targeted cyberattacks.",
        counter_arguments=[
            "Redundant architectures reduce single points of failure.",
            "Network segmentation and monitoring detect and isolate threats.",
            "Operator training and drills improve incident response."
        ],
        resolution_strategy="Implement defense-in-depth, redundancy, and continuous monitoring.",
        entity_scope="Utility, Control Center, Field Devices",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NERC CIP-007; ISA/IEC 62443-3-3"
    ),
    DoctrineBlock(
        topic="DER Integration: Distributed Energy Resources",
        keywords=["DER", "distributed energy resources", "inverter", "solar", "wind", "distributed generation", "interconnection"],
        conclusion_template="DER integration must ensure grid stability, interoperability, and compliance with interconnection standards, while enabling bidirectional power flows.",
        reasoning_framework="""
The proliferation of DERs introduces variability and complexity to grid operations. Integration requires adherence to interconnection standards (IEEE 1547), advanced inverter functions (e.g., Volt-VAR, frequency ride-through), and real-time monitoring. Utilities must address voltage regulation, protection coordination, and reverse power flow. Communication protocols must support interoperability, and cybersecurity must be enforced at all endpoints. Regulatory frameworks incentivize DER adoption but require utilities to maintain reliability and power quality.
        """,
        key_factors=[
            "Interconnection standards",
            "Grid stability",
            "Advanced inverter functions",
            "Voltage regulation",
            "Protection coordination",
            "Cybersecurity"
        ],
        primary_authority=[
            "IEEE 1547",
            "FERC Order 2222",
            "NERC Reliability Standards"
        ],
        burden_holder="DER operator",
        adversary_position="DERs destabilize the grid and complicate protection schemes.",
        counter_arguments=[
            "Advanced inverters support grid services.",
            "Real-time monitoring and adaptive protection mitigate risks.",
            "Regulatory oversight ensures compliance."
        ],
        resolution_strategy="Mandate advanced inverter capabilities and real-time telemetry.",
        entity_scope="Utility, DER Operator, Aggregator",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 1547-2018; FERC Order 2222"
    ),
    DoctrineBlock(
        topic="Demand Response (DR): Incentive and Price-Based Programs",
        keywords=["demand response", "DR", "incentive programs", "price-based", "load management", "customer participation"],
        conclusion_template="DR programs should leverage both incentive and price-based mechanisms to optimize grid load and engage customers in energy management.",
        reasoning_framework="""
Demand response programs are essential for balancing supply and demand, especially with increasing DER penetration. The framework distinguishes between incentive-based (direct payments for load reduction) and price-based (dynamic pricing, time-of-use rates) DR. Effective DR requires real-time communication, customer engagement, and measurement & verification (M&V) systems. Regulatory support and market integration are key. Privacy and equity considerations must be addressed to ensure broad participation and avoid disproportionate impacts.
        """,
        key_factors=[
            "Program design (incentive vs. price-based)",
            "Customer engagement",
            "Measurement & verification",
            "Communication infrastructure",
            "Regulatory compliance",
            "Equity and privacy"
        ],
        primary_authority=[
            "FERC Order 745",
            "DOE Demand Response Roadmap",
            "NARUC"
        ],
        burden_holder="Program administrator",
        adversary_position="DR programs are unreliable and unfairly burden certain customer classes.",
        counter_arguments=[
            "Automated DR increases reliability.",
            "Equitable program design mitigates disproportionate impacts.",
            "M&V ensures accurate compensation."
        ],
        resolution_strategy="Implement automated DR, transparent M&V, and inclusive program design.",
        entity_scope="Utility, Aggregator, Customer",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FERC Order 745"
    ),
    DoctrineBlock(
        topic="Microgrid: Islanding, Reconnection, and Black Start",
        keywords=["microgrid", "islanding", "reconnection", "black start", "resilience", "local generation", "autonomy"],
        conclusion_template="Microgrids must safely transition between grid-connected and islanded modes, with robust reconnection and black start procedures.",
        reasoning_framework="""
Microgrids enhance resilience by enabling localized operation during grid disturbances. The framework covers intentional islanding, seamless transition, and safe reconnection. Black start capability allows microgrids to restore power autonomously. Key considerations include protection coordination, synchronization, DER management, and communication with the main grid. Standards (IEEE 1547.4, IEEE 2030.7) guide design and operation. Regulatory approval and coordination with the utility are essential for safe operation.
        """,
        key_factors=[
            "Islanding detection",
            "Seamless transition",
            "Black start capability",
            "Protection coordination",
            "Synchronization",
            "Regulatory approval"
        ],
        primary_authority=[
            "IEEE 1547.4",
            "IEEE 2030.7",
            "DOE Microgrid Initiative"
        ],
        burden_holder="Microgrid operator",
        adversary_position="Microgrid transitions risk damaging equipment and endangering personnel.",
        counter_arguments=[
            "Automated protection and synchronization reduce risks.",
            "Operator training and standards compliance ensure safety.",
            "Coordination protocols with utility mitigate hazards."
        ],
        resolution_strategy="Adopt automated protection, comply with standards, and coordinate with utility.",
        entity_scope="Microgrid Operator, Utility, DER Owner",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 1547.4-2011; IEEE 2030.7-2017"
    ),
    DoctrineBlock(
        topic="Energy Storage: Battery, Flywheel, and Compressed Air",
        keywords=["energy storage", "battery", "flywheel", "compressed air", "frequency regulation", "peak shaving", "grid services"],
        conclusion_template="Energy storage systems must be integrated to provide grid services such as frequency regulation, peak shaving, and backup, with appropriate safety and control measures.",
        reasoning_framework="""
Energy storage enhances grid flexibility and reliability. The framework evaluates technology selection (battery, flywheel, CAES), use cases (frequency regulation, peak shaving, backup), and integration with grid management systems. Safety standards (NFPA 855, UL 9540) and operational protocols must be followed. Control systems should enable real-time dispatch and monitoring. Economic viability, lifecycle management, and environmental impact are also considered. Regulatory incentives and market participation rules influence deployment.
        """,
        key_factors=[
            "Technology selection",
            "Grid integration",
            "Safety standards",
            "Control systems",
            "Economic viability",
            "Regulatory incentives"
        ],
        primary_authority=[
            "NFPA 855",
            "UL 9540",
            "FERC Order 841"
        ],
        burden_holder="Storage system owner",
        adversary_position="Storage systems are costly, complex, and pose safety risks.",
        counter_arguments=[
            "Advanced controls and safety standards mitigate risks.",
            "Market participation improves economic returns.",
            "Lifecycle management reduces long-term costs."
        ],
        resolution_strategy="Adopt certified technologies, comply with safety standards, and optimize control strategies.",
        entity_scope="Utility, Storage Owner, Market Operator",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FERC Order 841; NFPA 855"
    ),
    DoctrineBlock(
        topic="Power Quality: Voltage Sag, Swell, Harmonics, THD",
        keywords=["power quality", "voltage sag", "voltage swell", "harmonics", "THD", "PQ monitoring", "disturbance"],
        conclusion_template="Utilities must monitor and mitigate power quality disturbances, maintaining voltage and harmonic levels within prescribed standards.",
        reasoning_framework="""
Power quality is critical for reliable grid operation and customer satisfaction. The framework addresses sources of sags, swells, and harmonics, and the impact of non-linear loads and DERs. Utilities must deploy PQ monitoring, analyze event data, and implement mitigation (e.g., filters, voltage regulators). Standards (IEEE 1159, IEEE 519) define acceptable limits. Customer complaints and sensitive loads require prioritized response. Coordination with DER operators is increasingly important due to inverter-based resources.
        """,
        key_factors=[
            "Monitoring infrastructure",
            "Event analysis",
            "Mitigation strategies",
            "Standards compliance",
            "Customer impact",
            "DER coordination"
        ],
        primary_authority=[
            "IEEE 1159",
            "IEEE 519",
            "ANSI C84.1"
        ],
        burden_holder="Utility",
        adversary_position="PQ mitigation is expensive and benefits only a subset of customers.",
        counter_arguments=[
            "PQ issues can damage equipment and increase costs for all.",
            "Targeted mitigation reduces overall system risk.",
            "Standards compliance is mandatory."
        ],
        resolution_strategy="Deploy PQ monitoring, prioritize mitigation, and enforce standards.",
        entity_scope="Utility, Customer, DER Operator",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 1159-2019; IEEE 519-2014"
    ),
    DoctrineBlock(
        topic="Wide Area Monitoring (WAMS): Synchrophasor, PMU",
        keywords=["WAMS", "synchrophasor", "PMU", "wide area monitoring", "phasor measurement", "grid visibility"],
        conclusion_template="WAMS deployment with PMUs enables real-time, high-resolution grid monitoring, enhancing situational awareness and stability.",
        reasoning_framework="""
WAMS leverages PMUs to provide time-synchronized, high-speed measurements of grid parameters. This improves situational awareness, enables early detection of instability, and supports advanced analytics. The framework includes PMU placement, data communication (IEEE C37.118), and integration with control centers. Data management, cybersecurity, and interoperability are critical. Regulatory support and funding influence deployment. Operator training is required to interpret and act on WAMS data.
        """,
        key_factors=[
            "PMU placement",
            "Data communication",
            "Cybersecurity",
            "Data management",
            "Operator training",
            "Regulatory support"
        ],
        primary_authority=[
            "IEEE C37.118",
            "NERC PRC-002",
            "DOE Synchrophasor Initiative"
        ],
        burden_holder="Transmission operator",
        adversary_position="WAMS is costly and generates excessive data with limited actionable value.",
        counter_arguments=[
            "WAMS enables early detection of grid instability.",
            "Data analytics extract actionable insights.",
            "Regulatory mandates support deployment."
        ],
        resolution_strategy="Optimize PMU placement, invest in analytics, and comply with standards.",
        entity_scope="Transmission Operator, ISO/RTO, Utility",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE C37.118-2014; NERC PRC-002-2"
    ),
    DoctrineBlock(
        topic="Distribution Automation: Recloser, Sectionalizer",
        keywords=["distribution automation", "recloser", "sectionalizer", "fault isolation", "self-healing", "DA"],
        conclusion_template="Distribution automation systems must enable rapid fault detection, isolation, and service restoration using reclosers and sectionalizers.",
        reasoning_framework="""
Distribution automation enhances reliability by automating fault detection and isolation. The framework covers deployment of reclosers and sectionalizers, integration with SCADA/OMS, and communication requirements. Self-healing networks reduce outage duration and improve SAIDI/SAIFI metrics. Standards (IEEE 1613, IEC 61850) guide device interoperability. Cybersecurity and maintenance are ongoing concerns. Utilities must balance automation costs with reliability improvements.
        """,
        key_factors=[
            "Device interoperability",
            "Communication infrastructure",
            "Integration with SCADA/OMS",
            "Cybersecurity",
            "Reliability metrics",
            "Maintenance"
        ],
        primary_authority=[
            "IEEE 1613",
            "IEC 61850",
            "NERC Reliability Standards"
        ],
        burden_holder="Utility",
        adversary_position="Automation increases complexity and introduces new failure modes.",
        counter_arguments=[
            "Self-healing reduces outage duration.",
            "Redundant systems mitigate failure risks.",
            "Interoperability standards simplify integration."
        ],
        resolution_strategy="Adopt interoperable devices, redundant architectures, and continuous monitoring.",
        entity_scope="Utility, Distribution Operator, Field Crew",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 1613-2009; IEC 61850"
    ),
    DoctrineBlock(
        topic="Volt-VAR Optimization: Capacitor Bank, Regulator",
        keywords=["volt-var optimization", "VVO", "capacitor bank", "voltage regulator", "reactive power", "distribution grid"],
        conclusion_template="Volt-VAR optimization should leverage automated capacitor banks and voltage regulators to maintain optimal voltage profiles and reduce losses.",
        reasoning_framework="""
VVO improves efficiency and power quality by managing voltage and reactive power. The framework involves deploying automated capacitor banks and regulators, integrating with DA/SCADA, and using advanced algorithms for real-time control. Standards (IEEE 1547, ANSI C84.1) define voltage limits. Communication and interoperability are essential for coordinated control. Utilities must consider cost, maintenance, and impact on DER integration.
        """,
        key_factors=[
            "Automated control",
            "Integration with DA/SCADA",
            "Voltage limits",
            "Interoperability",
            "Cost-benefit analysis",
            "DER impact"
        ],
        primary_authority=[
            "IEEE 1547",
            "ANSI C84.1",
            "DOE VVO Initiative"
        ],
        burden_holder="Utility",
        adversary_position="Automated VVO is expensive and may conflict with DER operations.",
        counter_arguments=[
            "VVO reduces losses and improves PQ.",
            "Coordination protocols mitigate DER conflicts.",
            "Cost savings justify investment."
        ],
        resolution_strategy="Integrate VVO with DER management and prioritize interoperability.",
        entity_scope="Utility, Distribution Operator, DER Owner",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 1547-2018; ANSI C84.1-2020"
    ),
    DoctrineBlock(
        topic="Outage Management (OMS): Fault Location, FLISR",
        keywords=["outage management", "OMS", "fault location", "FLISR", "restoration", "SAIDI", "SAIFI"],
        conclusion_template="OMS must incorporate automated fault location and FLISR to minimize outage duration and improve reliability indices.",
        reasoning_framework="""
OMS systems enhance reliability by automating outage detection, fault location, and service restoration (FLISR). The framework covers integration with AMI, DA, and SCADA, real-time data analytics, and customer notification. Accurate fault location reduces restoration time and improves SAIDI/SAIFI. Regulatory mandates require utilities to report and minimize outages. Cybersecurity and data privacy must be addressed, especially with customer-facing interfaces.
        """,
        key_factors=[
            "Integration with AMI/DA/SCADA",
            "Automated fault location",
            "FLISR algorithms",
            "Customer communication",
            "Reliability indices",
            "Cybersecurity"
        ],
        primary_authority=[
            "IEEE 1366",
            "NERC Reliability Standards",
            "DOE Grid Modernization Lab Consortium"
        ],
        burden_holder="Utility",
        adversary_position="OMS automation is costly and may not significantly improve reliability.",
        counter_arguments=[
            "FLISR reduces outage duration and improves metrics.",
            "Customer satisfaction increases with timely communication.",
            "Regulatory compliance requires outage reporting."
        ],
        resolution_strategy="Integrate OMS with field automation and prioritize customer communication.",
        entity_scope="Utility, Distribution Operator, Customer",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 1366-2012"
    ),
    DoctrineBlock(
        topic="Cybersecurity: NERC CIP Standards Compliance",
        keywords=["cybersecurity", "NERC CIP", "compliance", "critical infrastructure", "risk management", "incident response"],
        conclusion_template="Utilities must comply with NERC CIP standards to protect critical infrastructure from cyber threats, with comprehensive risk management and incident response plans.",
        reasoning_framework="""
Cybersecurity is a top priority for grid operators. The framework mandates compliance with NERC CIP standards, covering asset identification, risk assessment, access control, incident response, and recovery. Utilities must conduct regular audits, employee training, and vulnerability assessments. Supply chain risks and third-party access must be managed. Regulatory penalties for non-compliance are significant. Continuous improvement and adaptation to evolving threats are essential.
        """,
        key_factors=[
            "Asset identification",
            "Risk assessment",
            "Access control",
            "Incident response",
            "Employee training",
            "Supply chain management"
        ],
        primary_authority=[
            "NERC CIP",
            "FERC",
            "DOE Cybersecurity Capability Maturity Model"
        ],
        burden_holder="Utility",
        adversary_position="CIP compliance is burdensome and diverts resources from operational priorities.",
        counter_arguments=[
            "Non-compliance risks regulatory penalties and outages.",
            "Cyber incidents can cause catastrophic damage.",
            "Continuous improvement reduces long-term costs."
        ],
        resolution_strategy="Implement comprehensive risk management, regular audits, and employee training.",
        entity_scope="Utility, Vendor, Regulator",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NERC CIP-005-7; NERC CIP-007-6"
    ),
    # 28+ more DoctrineBlock instances with real, authoritative content follow...
    DoctrineBlock(
        topic="AMI: Data Privacy and Customer Consent",
        keywords=["AMI", "data privacy", "customer consent", "personal data", "regulatory compliance", "GDPR"],
        conclusion_template="AMI deployments must ensure customer data privacy and obtain informed consent for data collection and sharing.",
        reasoning_framework="""
AMI systems collect granular consumption data, raising privacy concerns. The framework requires utilities to implement data minimization, encryption, and access controls. Customer consent must be explicit, with clear communication of data usage and sharing practices. Compliance with privacy regulations (GDPR, CCPA) is mandatory. Utilities should provide opt-out mechanisms and respond promptly to data access or deletion requests.
        """,
        key_factors=[
            "Data minimization",
            "Encryption",
            "Access control",
            "Customer communication",
            "Regulatory compliance",
            "Opt-out mechanisms"
        ],
        primary_authority=[
            "GDPR",
            "CCPA",
            "NISTIR 7628"
        ],
        burden_holder="Utility",
        adversary_position="Granular AMI data enables surveillance and misuse of personal information.",
        counter_arguments=[
            "Encryption and access controls limit misuse.",
            "Transparency builds customer trust.",
            "Regulatory oversight enforces compliance."
        ],
        resolution_strategy="Implement privacy by design, clear consent processes, and regular audits.",
        entity_scope="Utility, Customer, Regulator",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GDPR Article 6; CCPA Section 1798"
    ),
    DoctrineBlock(
        topic="SCADA: Legacy System Modernization",
        keywords=["SCADA", "legacy systems", "modernization", "protocol conversion", "interoperability", "migration"],
        conclusion_template="Legacy SCADA systems should be modernized through phased migration, protocol conversion, and enhanced security.",
        reasoning_framework="""
Many utilities operate legacy SCADA systems with outdated protocols and limited security. The framework advocates phased modernization, starting with protocol converters and network segmentation. Migration to modern protocols (IEC 61850, secure DNP3) should be planned to minimize disruption. Security enhancements (firewalls, intrusion detection) are critical. Operator retraining and documentation updates are required. Regulatory reporting may be necessary for critical infrastructure changes.
        """,
        key_factors=[
            "Protocol conversion",
            "Network segmentation",
            "Security enhancements",
            "Operator training",
            "Migration planning",
            "Regulatory reporting"
        ],
        primary_authority=[
            "ISA/IEC 62443",
            "NERC CIP",
            "DOE Grid Modernization Initiative"
        ],
        burden_holder="Utility",
        adversary_position="Modernization is costly and risks operational disruption.",
        counter_arguments=[
            "Phased migration reduces risk.",
            "Security improvements protect critical assets.",
            "Regulatory incentives may offset costs."
        ],
        resolution_strategy="Adopt phased approach, prioritize security, and engage stakeholders.",
        entity_scope="Utility, Vendor, Regulator",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISA/IEC 62443-3-2"
    ),
    DoctrineBlock(
        topic="DER Integration: Aggregator Participation",
        keywords=["DER", "aggregator", "market participation", "FERC Order 2222", "distributed resources"],
        conclusion_template="Aggregators should be enabled to participate in wholesale markets, subject to interoperability and telemetry requirements.",
        reasoning_framework="""
Aggregators pool DERs to provide grid services and participate in wholesale markets. The framework requires real-time telemetry, interoperability with market operators, and compliance with FERC Order 2222. Aggregators must ensure accurate measurement, dispatchability, and cybersecurity. Market rules should facilitate entry while maintaining reliability and transparency. Coordination with utilities is essential to avoid operational conflicts.
        """,
        key_factors=[
            "Telemetry requirements",
            "Interoperability",
            "Market rules",
            "Cybersecurity",
            "Coordination with utilities",
            "Measurement accuracy"
        ],
        primary_authority=[
            "FERC Order 2222",
            "ISO/RTO Tariffs",
            "NERC Reliability Standards"
        ],
        burden_holder="Aggregator",
        adversary_position="Aggregator participation complicates market operations and grid reliability.",
        counter_arguments=[
            "Aggregators increase flexibility and competition.",
            "Telemetry and coordination mitigate reliability risks.",
            "Market rules ensure transparency."
        ],
        resolution_strategy="Mandate telemetry, interoperability, and coordination protocols.",
        entity_scope="Aggregator, Utility, ISO/RTO",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FERC Order 2222"
    ),
    DoctrineBlock(
        topic="Demand Response: Measurement and Verification (M&V)",
        keywords=["demand response", "M&V", "measurement", "verification", "baseline", "settlement"],
        conclusion_template="DR programs must implement robust M&V protocols to ensure accurate baseline calculation and fair settlement.",
        reasoning_framework="""
M&V is essential for DR credibility and market settlement. The framework includes baseline methodology selection, data quality assurance, and third-party verification. Automated metering and analytics improve accuracy. Regulatory standards (e.g., NAESB) guide M&V practices. Dispute resolution mechanisms are necessary for settlement disagreements. Transparency and auditability are key for stakeholder trust.
        """,
        key_factors=[
            "Baseline methodology",
            "Data quality",
            "Third-party verification",
            "Automation",
            "Regulatory standards",
            "Dispute resolution"
        ],
        primary_authority=[
            "NAESB",
            "FERC",
            "DOE"
        ],
        burden_holder="Program administrator",
        adversary_position="M&V protocols are complex and may disadvantage certain participants.",
        counter_arguments=[
            "Automation reduces complexity and bias.",
            "Third-party verification ensures fairness.",
            "Regulatory standards provide consistency."
        ],
        resolution_strategy="Adopt automated, transparent, and auditable M&V protocols.",
        entity_scope="Utility, Aggregator, Market Operator",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NAESB DR M&V Standards"
    ),
    DoctrineBlock(
        topic="Microgrid: Regulatory Approval and Interconnection",
        keywords=["microgrid", "regulatory approval", "interconnection", "utility coordination", "safety", "IEEE 1547"],
        conclusion_template="Microgrid projects must secure regulatory approval and comply with interconnection standards for safe operation.",
        reasoning_framework="""
Microgrid deployment requires navigating regulatory processes and interconnection requirements. The framework covers application procedures, safety studies, and utility coordination. Compliance with IEEE 1547 ensures safe operation and grid protection. Utilities may require additional studies for protection and operational impacts. Stakeholder engagement and public hearings may be necessary. Timely approval depends on thorough documentation and adherence to standards.
        """,
        key_factors=[
            "Application procedures",
            "Safety studies",
            "Interconnection standards",
            "Utility coordination",
            "Stakeholder engagement",
            "Documentation"
        ],
        primary_authority=[
            "IEEE 1547",
            "State PUC",
            "FERC"
        ],
        burden_holder="Microgrid developer",
        adversary_position="Regulatory processes are slow and discourage innovation.",
        counter_arguments=[
            "Standardized procedures streamline approval.",
            "Safety studies protect grid and public.",
            "Stakeholder engagement builds support."
        ],
        resolution_strategy="Follow standardized procedures, engage stakeholders, and ensure documentation.",
        entity_scope="Microgrid Developer, Utility, Regulator",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 1547-2018"
    ),
    DoctrineBlock(
        topic="Energy Storage: Fire Safety and Emergency Response",
        keywords=["energy storage", "fire safety", "emergency response", "NFPA 855", "first responder training"],
        conclusion_template="Energy storage installations must comply with fire safety standards and provide emergency response plans and training.",
        reasoning_framework="""
Energy storage systems, especially batteries, pose fire and explosion risks. The framework mandates compliance with NFPA 855 and local fire codes. Emergency response plans must be developed in coordination with first responders. Training and access to safety data sheets (SDS) are required. Systems should include fire suppression, ventilation, and monitoring. Incident reporting and post-event analysis support continuous improvement.
        """,
        key_factors=[
            "Fire safety standards",
            "Emergency response plans",
            "First responder training",
            "Fire suppression systems",
            "Incident reporting",
            "Continuous improvement"
        ],
        primary_authority=[
            "NFPA 855",
            "UL 9540A",
            "Local Fire Code"
        ],
        burden_holder="Storage system owner",
        adversary_position="Fire safety requirements increase project costs and complexity.",
        counter_arguments=[
            "Safety standards prevent catastrophic incidents.",
            "Training reduces response time and risk.",
            "Insurance and regulatory compliance depend on adherence."
        ],
        resolution_strategy="Comply with standards, coordinate with responders, and document procedures.",
        entity_scope="Storage Owner, Utility, First Responders",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 855-2020"
    ),
    DoctrineBlock(
        topic="Power Quality: DER-Induced Harmonics",
        keywords=["power quality", "harmonics", "DER", "inverter", "THD", "IEEE 519"],
        conclusion_template="DER interconnections must be evaluated for harmonic emissions and comply with IEEE 519 limits.",
        reasoning_framework="""
Inverter-based DERs can introduce harmonics, affecting power quality. The framework requires harmonic studies during interconnection, compliance with IEEE 519, and deployment of filters if necessary. Continuous monitoring and event logging support enforcement. Utilities should coordinate with DER operators to address violations. Customer complaints should trigger investigations and mitigation.
        """,
        key_factors=[
            "Harmonic studies",
            "Compliance with IEEE 519",
            "Filter deployment",
            "Continuous monitoring",
            "Coordination with DER operators",
            "Customer complaint response"
        ],
        primary_authority=[
            "IEEE 519",
            "IEEE 1547",
            "ANSI C84.1"
        ],
        burden_holder="DER operator",
        adversary_position="Harmonic limits restrict DER deployment and increase costs.",
        counter_arguments=[
            "Harmonics can damage equipment and degrade PQ.",
            "Filter technology is mature and cost-effective.",
            "Standards ensure fair grid access."
        ],
        resolution_strategy="Mandate harmonic studies and enforce compliance.",
        entity_scope="Utility, DER Operator, Customer",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 519-2014"
    ),
    DoctrineBlock(
        topic="WAMS: Data Management and Analytics",
        keywords=["WAMS", "data management", "analytics", "big data", "PMU", "data retention"],
        conclusion_template="WAMS deployments must implement scalable data management and analytics platforms to extract actionable insights from PMU data.",
        reasoning_framework="""
WAMS generates large volumes of time-synchronized data. The framework requires scalable storage, efficient retrieval, and advanced analytics. Data retention policies must comply with regulatory requirements. Cybersecurity and data integrity are critical. Visualization tools aid operator decision-making. Collaboration with research institutions can enhance analytics capabilities. Data sharing agreements may be necessary for multi-utility coordination.
        """,
        key_factors=[
            "Scalable storage",
            "Efficient retrieval",
            "Advanced analytics",
            "Data retention policies",
            "Cybersecurity",
            "Visualization tools"
        ],
        primary_authority=[
            "NERC PRC-002",
            "DOE Synchrophasor Initiative",
            "IEEE C37.118"
        ],
        burden_holder="Transmission operator",
        adversary_position="Data management costs outweigh operational benefits.",
        counter_arguments=[
            "Analytics improve grid reliability and efficiency.",
            "Regulatory mandates require data retention.",
            "Visualization enhances situational awareness."
        ],
        resolution_strategy="Invest in scalable platforms and analytics, and comply with retention policies.",
        entity_scope="Transmission Operator, Utility, Research Partner",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NERC PRC-002-2"
    ),
    DoctrineBlock(
        topic="Distribution Automation: Cybersecurity for Field Devices",
        keywords=["distribution automation", "cybersecurity", "field devices", "recloser", "sectionalizer", "encryption"],
        conclusion_template="Distribution automation deployments must secure field devices with encryption, authentication, and continuous monitoring.",
        reasoning_framework="""
Field devices are increasingly networked, exposing new attack surfaces. The framework mandates device-level encryption, mutual authentication, and secure firmware updates. Continuous monitoring and anomaly detection are required. Physical security and tamper detection should be implemented. Incident response plans must include field device compromise scenarios. Compliance with NERC CIP and ISA/IEC 62443 is essential.
        """,
        key_factors=[
            "Device-level encryption",
            "Authentication",
            "Firmware security",
            "Continuous monitoring",
            "Physical security",
            "Incident response"
        ],
        primary_authority=[
            "NERC CIP",
            "ISA/IEC 62443",
            "DOE"
        ],
        burden_holder="Utility",
        adversary_position="Cybersecurity increases device cost and complexity.",
        counter_arguments=[
            "Security breaches can disrupt grid operations.",
            "Standards-based approaches reduce integration risk.",
            "Continuous monitoring detects threats early."
        ],
        resolution_strategy="Adopt standards-based security and monitor field devices continuously.",
        entity_scope="Utility, Vendor, Field Crew",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NERC CIP-007-6; ISA/IEC 62443-4-2"
    ),
    DoctrineBlock(
        topic="Volt-VAR Optimization: DER Coordination",
        keywords=["volt-var optimization", "DER", "inverter", "coordination", "reactive power", "VVO"],
        conclusion_template="VVO algorithms must coordinate with DER inverters to optimize voltage and reactive power across the distribution grid.",
        reasoning_framework="""
DER inverters can provide Volt-VAR support, but require coordination with utility VVO schemes. The framework includes real-time communication, interoperability standards (IEEE 1547-2018), and adaptive algorithms. Utilities must monitor DER participation and adjust setpoints as needed. Cybersecurity and data privacy must be maintained. Regulatory incentives may encourage DER participation in VVO.
        """,
        key_factors=[
            "Real-time communication",
            "Interoperability",
            "Adaptive algorithms",
            "Monitoring",
            "Cybersecurity",
            "Regulatory incentives"
        ],
        primary_authority=[
            "IEEE 1547-2018",
            "ANSI C84.1",
            "DOE"
        ],
        burden_holder="Utility",
        adversary_position="DER coordination complicates VVO and may reduce reliability.",
        counter_arguments=[
            "DERs increase VVO flexibility.",
            "Adaptive algorithms manage complexity.",
            "Interoperability standards ensure reliability."
        ],
        resolution_strategy="Implement interoperable, adaptive VVO with DER coordination.",
        entity_scope="Utility, DER Operator, Aggregator",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 1547-2018"
    ),
    DoctrineBlock(
        topic="Outage Management: Customer Notification and Engagement",
        keywords=["outage management", "customer notification", "engagement", "OMS", "communication", "mobile app"],
        conclusion_template="OMS should provide timely, multi-channel customer notifications and enable two-way engagement during outages.",
        reasoning_framework="""
Customer engagement improves satisfaction and reduces call volume during outages. The framework includes automated notifications (SMS, email, app), estimated restoration times, and two-way communication for status updates. Integration with OMS and CRM systems is required. Accessibility and language support should be considered. Feedback mechanisms support continuous improvement. Regulatory requirements may mandate notification timelines.
        """,
        key_factors=[
            "Automated notifications",
            "Multi-channel communication",
            "Integration with OMS/CRM",
            "Accessibility",
            "Feedback mechanisms",
            "Regulatory compliance"
        ],
        primary_authority=[
            "State PUC",
            "DOE Grid Modernization Lab Consortium",
            "IEEE 1366"
        ],
        burden_holder="Utility",
        adversary_position="Automated notifications are costly and may overwhelm customers.",
        counter_arguments=[
            "Timely communication reduces frustration.",
            "Multi-channel approach increases reach.",
            "Feedback improves future response."
        ],
        resolution_strategy="Implement multi-channel, accessible notification systems and gather feedback.",
        entity_scope="Utility, Customer, Regulator",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 1366-2012"
    ),
    DoctrineBlock(
        topic="Cybersecurity: Supply Chain Risk Management",
        keywords=["cybersecurity", "supply chain", "risk management", "vendor", "third-party", "NERC CIP-013"],
        conclusion_template="Utilities must implement supply chain risk management for all vendors and third parties, as required by NERC CIP-013.",
        reasoning_framework="""
Supply chain attacks can compromise critical infrastructure. The framework mandates vendor risk assessments, contract requirements for cybersecurity, and continuous monitoring. Utilities must maintain an approved vendor list, conduct audits, and require incident reporting. Compliance with NERC CIP-013 is mandatory. Training and awareness programs for procurement staff are recommended. Incident response plans should include supply chain scenarios.
        """,
        key_factors=[
            "Vendor risk assessment",
            "Contractual cybersecurity requirements",
            "Continuous monitoring",
            "Approved vendor list",
            "Audits",
            "Incident response"
        ],
        primary_authority=[
            "NERC CIP-013",
            "FERC",
            "DOE"
        ],
        burden_holder="Utility",
        adversary_position="Supply chain requirements slow procurement and increase costs.",
        counter_arguments=[
            "Supply chain attacks can have catastrophic impacts.",
            "Contractual controls reduce risk.",
            "Audits ensure compliance."
        ],
        resolution_strategy="Enforce NERC CIP-013, conduct regular audits, and train procurement staff.",
        entity_scope="Utility, Vendor, Regulator",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NERC CIP-013-1"
    ),
    DoctrineBlock(
        topic="AMI: Remote Disconnect/Reconnect",
        keywords=["AMI", "remote disconnect", "remote reconnect", "service control", "customer safety"],
        conclusion_template="AMI systems with remote disconnect/reconnect must include safety interlocks and customer notification protocols.",
        reasoning_framework="""
Remote disconnect/reconnect features improve operational efficiency but introduce safety risks. The framework requires safety interlocks to prevent disconnection during critical medical device use or extreme weather. Customer notification protocols must be followed, including advance warning and restoration timelines. Regulatory oversight may dictate permissible use cases. System logs should record all remote operations for auditability.
        """,
        key_factors=[
            "Safety interlocks",
            "Customer notification",
            "Regulatory oversight",
            "Auditability",
            "Operational efficiency",
            "Vulnerable customer protection"
        ],
        primary_authority=[
            "State PUC",
            "NISTIR 7628",
            "DOE"
        ],
        burden_holder="Utility",
        adversary_position="Remote disconnects risk customer safety and can be abused.",
        counter_arguments=[
            "Safety protocols and oversight reduce risk.",
            "Audit logs ensure accountability.",
            "Operational benefits justify deployment."
        ],
        resolution_strategy="Implement safety interlocks, notification protocols, and audit logging.",
        entity_scope="Utility, Customer, Regulator",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NISTIR 7628; State PUC Orders"
    ),
    DoctrineBlock(
        topic="SCADA: Network Segmentation and Defense-in-Depth",
        keywords=["SCADA", "network segmentation", "defense-in-depth", "firewall", "DMZ", "intrusion detection"],
        conclusion_template="SCADA networks must be segmented and protected with defense-in-depth strategies, including firewalls and intrusion detection.",
        reasoning_framework="""
Critical SCADA assets must be isolated from enterprise networks. The framework prescribes network segmentation (DMZs), firewalls, and intrusion detection/prevention systems. Defense-in-depth includes layered security controls, regular vulnerability assessments, and incident response planning. Compliance with NERC CIP and ISA/IEC 62443 is mandatory. Operator training and continuous monitoring are required to maintain security posture.
        """,
        key_factors=[
            "Network segmentation",
            "Firewalls",
            "Intrusion detection",
            "Layered controls",
            "Vulnerability assessment",
            "Operator training"
        ],
        primary_authority=[
            "NERC CIP",
            "ISA/IEC 62443",
            "DOE"
        ],
        burden_holder="Utility",
        adversary_position="Segmentation increases complexity and may hinder legitimate operations.",
        counter_arguments=[
            "Segmentation limits attack propagation.",
            "Layered controls improve resilience.",
            "Training ensures operational continuity."
        ],
        resolution_strategy="Implement layered security, monitor continuously, and train operators.",
        entity_scope="Utility, Vendor, Regulator",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NERC CIP-005-7; ISA/IEC 62443-3-3"
    ),
    DoctrineBlock(
        topic="DER Integration: Ride-Through and Anti-Islanding",
        keywords=["DER", "ride-through", "anti-islanding", "IEEE 1547", "inverter", "grid support"],
        conclusion_template="DERs must comply with ride-through and anti-islanding requirements to support grid stability.",
        reasoning_framework="""
Ride-through and anti-islanding functions prevent DERs from disconnecting during minor disturbances and avoid unintentional islanding. The framework mandates compliance with IEEE 1547-2018, including voltage/frequency ride-through profiles and anti-islanding detection. Utilities must verify settings during commissioning and monitor ongoing compliance. Coordination with protection schemes is essential to avoid nuisance tripping.
        """,
        key_factors=[
            "Ride-through profiles",
            "Anti-islanding detection",
            "Commissioning verification",
            "Ongoing monitoring",
            "Protection coordination",
            "Standards compliance"
        ],
        primary_authority=[
            "IEEE 1547-2018",
            "FERC",
            "NERC"
        ],
        burden_holder="DER operator",
        adversary_position="Ride-through requirements increase DER cost and complexity.",
        counter_arguments=[
            "Grid stability depends on DER support.",
            "Standardized settings simplify integration.",
            "Monitoring ensures compliance."
        ],
        resolution_strategy="Mandate compliance, verify settings, and monitor performance.",
        entity_scope="Utility, DER Operator, Aggregator",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 1547-2018"
    ),
    DoctrineBlock(
        topic="Demand Response: Customer Data Security",
        keywords=["demand response", "customer data", "security", "privacy", "encryption"],
        conclusion_template="DR programs must secure customer data with encryption and access controls, complying with privacy regulations.",
        reasoning_framework="""
DR programs collect sensitive customer data for M&V and settlement. The framework requires encryption in transit and at rest, role-based access controls, and regular audits. Compliance with privacy regulations (GDPR, CCPA) is mandatory. Customer consent and transparency are essential. Incident response plans must address data breaches. Utilities should provide data access and deletion mechanisms.
        """,
        key_factors=[
            "Encryption",
            "Access control",
            "Privacy compliance",
            "Customer consent",
            "Incident response",
            "Auditability"
        ],
        primary_authority=[
            "GDPR",
            "CCPA",
            "NISTIR 7628"
        ],
        burden_holder="Program administrator",
        adversary_position="Security requirements increase program cost and complexity.",
        counter_arguments=[
            "Data breaches erode trust and incur penalties.",
            "Encryption and controls are industry best practice.",
            "Transparency builds customer confidence."
        ],
        resolution_strategy="Implement encryption, access controls, and transparent consent processes.",
        entity_scope="Utility, Aggregator, Customer",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GDPR Article 32; CCPA Section 1798"
    ),
    DoctrineBlock(
        topic="Microgrid: Black Start Coordination",
        keywords=["microgrid", "black start", "coordination", "utility", "resilience"],
        conclusion_template="Microgrid black start procedures must be coordinated with the utility to ensure safe and reliable restoration.",
        reasoning_framework="""
Black start capability allows microgrids to restore power autonomously after an outage. The framework requires coordination with utility restoration plans, communication protocols, and synchronization procedures. Safety studies and operator training are essential. Regulatory approval may be required. Post-event analysis supports continuous improvement.
        """,
        key_factors=[
            "Coordination with utility",
            "Communication protocols",
            "Synchronization",
            "Safety studies",
            "Operator training",
            "Post-event analysis"
        ],
        primary_authority=[
            "IEEE 1547.4",
            "DOE Microgrid Initiative",
            "State PUC"
        ],
        burden_holder="Microgrid operator",
        adversary_position="Black start coordination is complex and may delay restoration.",
        counter_arguments=[
            "Coordination ensures safety and reliability.",
            "Training reduces errors.",
            "Continuous improvement streamlines future events."
        ],
        resolution_strategy="Coordinate with utility, train operators, and conduct post-event reviews.",
        entity_scope="Microgrid Operator, Utility, Regulator",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 1547.4-2011"
    ),
    DoctrineBlock(
        topic="Energy Storage: Market Participation and Revenue Stacking",
        keywords=["energy storage", "market participation", "revenue stacking", "FERC Order 841", "ancillary services"],
        conclusion_template="Storage systems should be enabled to participate in multiple markets, maximizing value through revenue stacking.",
        reasoning_framework="""
Revenue stacking allows storage to provide multiple grid services (e.g., frequency regulation, peak shaving, capacity). The framework requires market rules that enable participation in energy, capacity, and ancillary services markets. Accurate metering and telemetry are necessary. Compliance with FERC Order 841 is required. Coordination with utilities and ISOs ensures reliability. Economic analysis should guide participation strategies.
        """,
        key_factors=[
            "Market rules",
            "Accurate metering",
            "Telemetry",
            "Coordination with ISO/utility",
            "Economic analysis",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FERC Order 841",
            "ISO/RTO Tariffs",
            "DOE"
        ],
        burden_holder="Storage owner",
        adversary_position="Revenue stacking complicates market operations and may reduce reliability.",
        counter_arguments=[
            "Stacking increases storage value and grid flexibility.",
            "Market rules manage operational risks.",
            "Telemetry ensures transparency."
        ],
        resolution_strategy="Enable multi-market participation with accurate telemetry and compliance.",
        entity_scope="Storage Owner, Utility, ISO/RTO",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FERC Order 841"
    ),
    DoctrineBlock(
        topic="Power Quality: Event Logging and Root Cause Analysis",
        keywords=["power quality", "event logging", "root cause analysis", "PQ monitoring", "disturbance"],
        conclusion_template="Utilities must implement event logging and root cause analysis for PQ disturbances to prevent recurrence.",
        reasoning_framework="""
Event logging supports identification and mitigation of PQ disturbances. The framework requires deployment of PQ monitors, automated event logging, and root cause analysis. Utilities should maintain a disturbance database and share findings with stakeholders. Corrective actions may include equipment upgrades, filter installation, or operational changes. Regulatory reporting may be required for significant events.
        """,
        key_factors=[
            "PQ monitoring",
            "Automated event logging",
            "Root cause analysis",
            "Disturbance database",
            "Corrective actions",
            "Regulatory reporting"
        ],
        primary_authority=[
            "IEEE 1159",
            "IEEE 519",
            "ANSI C84.1"
        ],
        burden_holder="Utility",
        adversary_position="Event logging is resource-intensive and rarely yields actionable insights.",
        counter_arguments=[
            "Logging enables proactive mitigation.",
            "Root cause analysis prevents recurrence.",
            "Regulatory compliance may require reporting."
        ],
        resolution_strategy="Automate event logging and conduct regular root cause analysis.",
        entity_scope="Utility, Customer, DER Operator",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 1159-2019"
    ),
    DoctrineBlock(
        topic="WAMS: Inter-Utility Data Sharing",
        keywords=["WAMS", "data sharing", "inter-utility", "synchrophasor", "PMU", "regional coordination"],
        conclusion_template="WAMS operators should establish secure data sharing agreements to support regional grid coordination.",
        reasoning_framework="""
Regional grid stability benefits from inter-utility data sharing. The framework includes secure data exchange protocols, data anonymization, and legal agreements. Compliance with privacy and cybersecurity standards is required. Operators should define data ownership, access rights, and dispute resolution mechanisms. Collaboration with ISOs/RTOs enhances situational awareness and response.
        """,
        key_factors=[
            "Secure data exchange",
            "Legal agreements",
            "Data ownership",
            "Access rights",
            "Privacy compliance",
            "Regional coordination"
        ],
        primary_authority=[
            "NERC PRC-002",
            "DOE Synchrophasor Initiative",
            "ISO/RTO"
        ],
        burden_holder="WAMS operator",
        adversary_position="Data sharing risks privacy breaches and competitive disadvantage.",
        counter_arguments=[
            "Regional coordination improves reliability.",
            "Legal agreements manage risk.",
            "Anonymization protects sensitive data."
        ],
        resolution_strategy="Establish agreements, anonymize data, and comply with standards.",
        entity_scope="Transmission Operator, Utility, ISO/RTO",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NERC PRC-002-2"
    ),
    DoctrineBlock(
        topic="Distribution Automation: Predictive Maintenance",
        keywords=["distribution automation", "predictive maintenance", "condition monitoring", "asset management", "DA"],
        conclusion_template="DA systems should incorporate predictive maintenance to optimize asset life and reduce unplanned outages.",
        reasoning_framework="""
Predictive maintenance uses sensor data and analytics to forecast equipment failures. The framework includes condition monitoring, data analytics, and integration with asset management systems. Utilities should prioritize high-value assets and schedule maintenance proactively. Cost-benefit analysis guides investment. Regulatory incentives may support adoption. Training and change management are necessary for successful implementation.
        """,
        key_factors=[
            "Condition monitoring",
            "Data analytics",
            "Asset management integration",
            "Cost-benefit analysis",
            "Regulatory incentives",
            "Training"
        ],
        primary_authority=[
            "DOE Grid Modernization Lab Consortium",
            "NERC Reliability Standards",
            "IEEE 1451"
        ],
        burden_holder="Utility",
        adversary_position="Predictive maintenance requires costly sensors and analytics platforms.",
        counter_arguments=[
            "Reduces unplanned outages and maintenance costs.",
            "Extends asset life.",
            "Regulatory incentives may offset costs."
        ],
        resolution_strategy="Implement condition monitoring and analytics, and seek regulatory support.",
        entity_scope="Utility, Vendor, Field Crew",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="DOE GMLC Predictive Maintenance Initiative"
    ),
    DoctrineBlock(
        topic="Volt-VAR Optimization: Conservation Voltage Reduction (CVR)",
        keywords=["volt-var optimization", "CVR", "conservation voltage reduction", "energy efficiency", "distribution grid"],
        conclusion_template="VVO should enable CVR to improve energy efficiency and reduce peak demand.",
        reasoning_framework="""
CVR reduces system voltage within allowable limits to decrease energy consumption and peak demand. The framework includes voltage monitoring, automated control, and customer impact analysis. Utilities must comply with ANSI C84.1 voltage limits. Customer communication and opt-out options may be necessary. Cost-benefit analysis should guide implementation.
        """,
        key_factors=[
            "Voltage monitoring",
            "Automated control",
            "Customer impact analysis",
            "Compliance with voltage limits",
            "Customer communication",
            "Cost-benefit analysis"
        ],
        primary_authority=[
            "ANSI C84.1",
            "DOE",
            "IEEE 1547"
        ],
        burden_holder="Utility",
        adversary_position="CVR may negatively impact sensitive customer equipment.",
        counter_arguments=[
            "Voltage limits protect customer equipment.",
            "Customer communication mitigates concerns.",
            "Energy savings justify implementation."
        ],
        resolution_strategy="Monitor voltage, communicate with customers, and analyze impacts.",
        entity_scope="Utility, Customer, Regulator",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ANSI C84.1-2020"
    ),
    DoctrineBlock(
        topic="Outage Management: Integration with Distributed Energy Resources",
        keywords=["outage management", "DER", "OMS", "restoration", "islanding", "microgrid"],
        conclusion_template="OMS must integrate with DER management systems to coordinate restoration and islanding during outages.",
        reasoning_framework="""
DERs and microgrids can support outage restoration and islanding. The framework requires OMS integration with DERMS and microgrid controllers, real-time communication, and restoration protocols. Utilities must coordinate with DER operators and communicate with customers. Regulatory approval may be required for intentional islanding. Data analytics support optimal restoration sequencing.
        """,
        key_factors=[
            "OMS-DERMS integration",
            "Restoration protocols",
            "Real-time communication",
            "Coordination with DER operators",
            "Regulatory approval",
            "Data analytics"
        ],
        primary_authority=[
            "DOE Grid Modernization Lab Consortium",
            "IEEE 1547",
            "State PUC"
        ],
        burden_holder="Utility",
        adversary_position="DER integration complicates outage management and restoration.",
        counter_arguments=[
            "DERs enhance restoration flexibility.",
            "Protocols manage complexity.",
            "Analytics optimize sequencing."
        ],
        resolution_strategy="Integrate OMS with DERMS, coordinate protocols, and use analytics.",
        entity_scope="Utility, DER Operator, Microgrid Operator",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="DOE GMLC DER Integration Initiative"
    ),
    DoctrineBlock(
        topic="Cybersecurity: Incident Response and Recovery",
        keywords=["cybersecurity", "incident response", "recovery", "NERC CIP", "playbook"],
        conclusion_template="Utilities must maintain and regularly test incident response and recovery plans for cyber events.",
        reasoning_framework="""
Incident response is critical for minimizing cyber event impacts. The framework requires documented response plans, regular tabletop exercises, and post-incident reviews. Plans should cover detection, containment, eradication, and recovery. Communication protocols with regulators and law enforcement must be established. Lessons learned should inform plan updates. Compliance with NERC CIP and DOE C2M2 is required.
        """,
        key_factors=[
            "Documented response plans",
            "Regular exercises",
            "Post-incident review",
            "Communication protocols",
            "Plan updates",
            "Regulatory compliance"
        ],
        primary_authority=[
            "NERC CIP",
            "DOE C2M2",
            "FERC"
        ],
        burden_holder="Utility",
        adversary_position="Incident response planning is resource-intensive and rarely used.",
        counter_arguments=[
            "Preparedness reduces incident impact.",
            "Regulatory compliance is mandatory.",
            "Lessons learned improve future response."
        ],
        resolution_strategy="Maintain, test, and update response plans regularly.",
        entity_scope="Utility, Vendor, Regulator",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NERC CIP-008-6"
    ),
    DoctrineBlock(
        topic="AMI: Interoperability and Open Standards",
        keywords=["AMI", "interoperability", "open standards", "IEEE 1701", "multi-vendor", "integration"],
        conclusion_template="AMI systems must support interoperability and open standards to enable multi-vendor integration and future scalability.",
        reasoning_framework="""
Interoperability ensures AMI systems can integrate devices from multiple vendors. The framework requires adherence to open standards (IEEE 1701/1702, DLMS/COSEM), standardized data models, and protocol converters where necessary. Utilities should avoid vendor lock-in and plan for future scalability. Testing and certification support interoperability. Regulatory mandates may require open standards adoption.
        """,
        key_factors=[
            "Open standards compliance",
            "Standardized data models",
            "Protocol converters",
            "Testing and certification",
            "Vendor lock-in avoidance",
            "Scalability"
        ],
        primary_authority=[
            "IEEE 1701/1702",
            "DLMS/COSEM",
            "NIST Smart Grid Framework"
        ],
        burden_holder="Utility",
        adversary_position="Open standards increase integration complexity and cost.",
        counter_arguments=[
            "Interoperability reduces long-term costs.",
            "Certification ensures compatibility.",
            "Scalability supports future needs."
        ],
        resolution_strategy="Adopt open standards, certify devices, and plan for scalability.",
        entity_scope="Utility, Vendor, Regulator",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 1701-2014; NISTIR 7628"
    ),
    DoctrineBlock(
        topic="SCADA: Human-Machine Interface (HMI) Usability",
        keywords=["SCADA", "HMI", "usability", "operator training", "alarm management", "situational awareness"],
        conclusion_template="SCADA HMIs must be designed for usability, supporting operator situational awareness and effective alarm management.",
        reasoning_framework="""
HMI design impacts operator performance and grid reliability. The framework includes ergonomic layout, intuitive navigation, and effective alarm management. Training and simulation support operator proficiency. Standards (ISA-101) guide HMI design. Usability testing and operator feedback inform continuous improvement. Integration with SCADA and DA systems is required for comprehensive situational awareness.
        """,
        key_factors=[
            "Ergonomic layout",
            "Intuitive navigation",
            "Alarm management",
            "Operator training",
            "Usability testing",
            "Continuous improvement"
        ],
        primary_authority=[
            "ISA-101",
            "NERC Reliability Standards",
            "DOE"
        ],
        burden_holder="Utility",
        adversary_position="Usability improvements are subjective and hard to justify.",
        counter_arguments=[
            "Improved usability reduces operator error.",
            "Alarm management prevents overload.",
            "Training and feedback support continuous improvement."
        ],
        resolution_strategy="Follow HMI standards, test usability, and gather operator feedback.",
        entity_scope="Utility, Control Center, Vendor",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISA-101-2015"
    ),
    DoctrineBlock(
        topic="DER Integration: Cybersecurity for Inverter-Based Resources",
        keywords=["DER", "cybersecurity", "inverter", "IEC 62443", "encryption", "authentication"],
        conclusion_template="Inverter-based DERs must implement cybersecurity controls, including encryption and authentication, in compliance with IEC 62443.",
        reasoning_framework="""
Inverter-based DERs are increasingly networked and vulnerable to cyber threats. The framework requires device-level encryption, mutual authentication, and secure firmware updates. Compliance with IEC 62443 and NERC CIP is recommended. Utilities should verify cybersecurity controls during commissioning and monitor for vulnerabilities. Incident response plans must include DER compromise scenarios.
        """,
        key_factors=[
            "Device-level encryption",
            "Authentication",
            "Firmware security",
            "Commissioning verification",
            "Ongoing monitoring",
            "Incident response"
        ],
        primary_authority=[
            "IEC 62443",
            "NERC CIP",
            "DOE"
        ],
        burden_holder="DER operator",
        adversary_position="Cybersecurity increases DER cost and integration complexity.",
        counter_arguments=[
            "Cyber incidents can disrupt grid operations.",
            "Standards-based controls reduce risk.",
            "Monitoring ensures ongoing compliance."
        ],
        resolution_strategy="Mandate cybersecurity controls and monitor DERs continuously.",
        entity_scope="DER Operator, Utility, Vendor",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEC 62443-4-2; NERC CIP-007-6"
    ),
    DoctrineBlock(
        topic="Demand Response: Integration with Distributed Energy Resources",
        keywords=["demand response", "DER", "integration", "load management", "market participation"],
        conclusion_template="DR programs should integrate with DERs to enhance flexibility and enable aggregated market participation.",
        reasoning_framework="""
DERs can participate in DR programs, increasing grid flexibility. The framework includes real-time communication, aggregation platforms, and market integration. Measurement and verification protocols must account for DER contributions. Regulatory support and interoperability standards are essential. Customer engagement and transparency build trust and encourage participation.
        """,
        key_factors=[
            "Real-time communication",
            "Aggregation platforms",
            "Market integration",
            "M&V protocols",
            "Regulatory support",
            "Customer engagement"
        ],
        primary_authority=[
            "FERC Order 2222",
            "NAESB",
            "DOE"
        ],
        burden_holder="Program administrator",
        adversary_position="DER integration complicates DR settlement and increases risk.",
        counter_arguments=[
            "Aggregation increases flexibility and value.",
            "M&V protocols ensure fairness.",
            "Regulatory support facilitates integration."
        ],
        resolution_strategy="Integrate DR with DERs, adopt M&V protocols, and engage customers.",
        entity_scope="Utility, Aggregator, DER Operator",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FERC Order 2222"
    ),
    DoctrineBlock(
        topic="Microgrid: Resilience Metrics and Reporting",
        keywords=["microgrid", "resilience", "metrics", "reporting", "SAIDI", "SAIFI"],
        conclusion_template="Microgrid operators should track and report resilience metrics to demonstrate value and support regulatory compliance.",
        reasoning_framework="""
Resilience metrics quantify microgrid performance during grid disturbances. The framework includes tracking SAIDI, SAIFI, and outage duration. Operators should report metrics to regulators and stakeholders. Data analytics support performance improvement. Regulatory incentives may depend on demonstrated resilience. Transparent reporting builds stakeholder trust.
        """,
        key_factors=[
            "SAIDI/SAIFI tracking",
            "Outage duration",
            "Data analytics",
            "Regulatory reporting",
            "Performance improvement",
            "Stakeholder communication"
        ],
        primary_authority=[
            "IEEE 1366",
            "DOE Microgrid Initiative",
            "State PUC"
        ],
        burden_holder="Microgrid operator",
        adversary_position="Reporting requirements increase administrative burden.",
        counter_arguments=[
            "Metrics demonstrate value and support incentives.",
            "Analytics guide improvement.",
            "Transparency builds trust."
        ],
        resolution_strategy="Track metrics, analyze performance, and report transparently.",
        entity_scope="Microgrid Operator, Utility, Regulator",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 1366-2012"
    ),
    DoctrineBlock(
        topic="Energy Storage: End-of-Life Management",
        keywords=["energy storage", "end-of-life", "recycling", "disposal", "environmental compliance"],
        conclusion_template="Storage system owners must implement end-of-life management plans, including recycling and compliant disposal.",
        reasoning_framework="""
End-of-life management reduces environmental impact and regulatory risk. The framework requires recycling programs, compliant disposal, and documentation. Coordination with certified recyclers and waste handlers is necessary. Regulatory compliance (EPA, state laws) is mandatory. Utilities should educate customers and stakeholders on proper disposal. Lifecycle analysis supports sustainability goals.
        """,
        key_factors=[
            "Recycling programs",
            "Compliant disposal",
            "Documentation",
            "Certified recyclers",
            "Regulatory compliance",
            "Stakeholder education"
        ],
        primary_authority=[
            "EPA",
            "State Environmental Agencies",
            "DOE"
        ],
        burden_holder="Storage owner",
        adversary_position="End-of-life management increases costs and administrative burden.",
        counter_arguments=[
            "Reduces environmental liability.",
            "Supports sustainability goals.",
            "Regulatory compliance is mandatory."
        ],
        resolution_strategy="Partner with certified recyclers and document disposal processes.",
        entity_scope="Storage Owner, Utility, Regulator",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Battery Recycling Guidelines"
    ),
    DoctrineBlock(
        topic="Power Quality: Customer Complaint Resolution",
        keywords=["power quality", "customer complaint", "resolution", "PQ monitoring", "investigation"],
        conclusion_template="Utilities must investigate and resolve customer PQ complaints promptly, using monitoring and corrective actions.",
        reasoning_framework="""
Customer complaints often indicate underlying PQ issues. The framework includes deploying PQ monitors, investigating root causes, and implementing corrective actions. Utilities should communicate findings and resolutions to customers. Regulatory timelines may apply. Data from complaints can inform broader PQ improvement initiatives.
        """,
        key_factors=[
            "PQ monitoring",
            "Root cause investigation",
            "Corrective actions",
            "Customer communication",
            "Regulatory timelines",
            "Continuous improvement"
        ],
        primary_authority=[
            "IEEE 1159",
            "State PUC",
            "DOE"
        ],
        burden_holder="Utility",
        adversary_position="Complaint investigations are costly and rarely yield actionable results.",
        counter_arguments=[
            "Prompt resolution improves customer satisfaction.",
            "Data informs system improvements.",
            "Regulatory compliance may require investigation."
        ],
        resolution_strategy="Deploy monitors, investigate promptly, and communicate with customers.",
        entity_scope="Utility, Customer, Regulator",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 1159-2019"
    ),
    DoctrineBlock(
        topic="WAMS: PMU Placement Optimization",
        keywords=["WAMS", "PMU placement", "optimization", "synchrophasor", "grid visibility"],
        conclusion_template="PMU placement should be optimized to maximize grid observability and minimize deployment costs.",
        reasoning_framework="""
Optimal PMU placement enhances grid visibility and supports advanced analytics. The framework includes observability analysis, cost-benefit assessment, and redundancy planning. Collaboration with ISOs/RTOs and neighboring utilities may improve regional coverage. Regulatory mandates may dictate minimum placement. Simulation and modeling tools support decision-making.
        """,
        key_factors=[
            "Observability analysis",
            "Cost-benefit assessment",
            "Redundancy planning",
            "Regional collaboration",
            "Regulatory mandates",
            "Simulation tools"
        ],
        primary_authority=[
            "IEEE C37.118",
            "NERC PRC-002",
            "DOE"
        ],
        burden_holder="Transmission operator",
        adversary_position="Optimized placement increases planning complexity and delays deployment.",
        counter_arguments=[
            "Improves grid reliability and analytics.",
            "Redundancy reduces risk.",
            "Collaboration enhances regional visibility."
        ],
        resolution_strategy="Use simulation tools and collaborate regionally for optimal placement.",
        entity_scope="Transmission Operator, Utility, ISO/RTO",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE C37.118-2014"
    ),
    DoctrineBlock(
        topic="Distribution Automation: Integration with GIS and Asset Management",
        keywords=["distribution automation", "GIS", "asset management", "integration", "DA"],
        conclusion_template="DA systems should integrate with GIS and asset management platforms for improved situational awareness and maintenance planning.",
        reasoning_framework="""
Integration with GIS and asset management enhances DA effectiveness. The framework includes data synchronization, standardized interfaces, and real-time updates. Utilities should ensure data quality and consistency. Integration supports outage management, predictive maintenance, and capital planning. Regulatory reporting may require asset data. Training and change management are necessary for successful adoption.
        """,
        key_factors=[
            "Data synchronization",
            "Standardized interfaces",
            "Data quality",
            "Real-time updates",
            "Regulatory reporting",
            "Training"
        ],
        primary_authority=[
            "DOE Grid Modernization Lab Consortium",
            "NERC Reliability Standards",
            "IEEE 1451"
        ],
        burden_holder="Utility",
        adversary_position="Integration increases IT complexity and cost.",
        counter_arguments=[
            "Improves situational awareness and planning.",
            "Supports regulatory compliance.",
            "Training ensures successful adoption."
        ],
        resolution_strategy="Standardize interfaces, ensure data quality, and provide training.",
        entity_scope="Utility, Vendor, Field Crew",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="DOE GMLC DA-GIS Integration Initiative"
    ),
    DoctrineBlock(
        topic="Volt-VAR Optimization: Customer Impact Assessment",
        keywords=["volt-var optimization", "customer impact", "assessment", "VVO", "PQ"],
        conclusion_template="VVO deployments must assess and mitigate potential impacts on sensitive customer equipment.",
        reasoning_framework="""
VVO can affect voltage at customer premises, impacting sensitive equipment. The framework requires pre- and post-deployment assessments, customer surveys, and monitoring. Utilities should provide mitigation options (e.g., voltage regulators, filters) and communicate with affected customers. Regulatory reporting may be required for adverse impacts. Continuous improvement processes should incorporate customer feedback.
        """,
        key_factors=[
            "Pre- and post-deployment assessment",
            "Customer surveys",
            "Monitoring",
            "Mitigation options",
            "Customer communication",
            "Regulatory reporting"
        ],
        primary_authority=[
            "ANSI C84.1",
            "DOE",
            "State PUC"
        ],
        burden_holder="Utility",
        adversary_position="VVO increases PQ complaints and customer dissatisfaction.",
        counter_arguments=[
            "Assessment and mitigation reduce complaints.",
            "Communication builds trust.",
            "Regulatory compliance requires impact analysis."
        ],
        resolution_strategy="Assess impacts, provide mitigation, and communicate transparently.",
        entity_scope="Utility, Customer, Regulator",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ANSI C84.1-2020"
    ),
    DoctrineBlock(
        topic="Outage Management: FLISR Algorithm Transparency",
        keywords=["outage management", "FLISR", "algorithm", "transparency", "customer communication"],
        conclusion_template="Utilities should provide transparency into FLISR algorithms and communicate restoration logic to stakeholders.",
        reasoning_framework="""
Transparency in FLISR algorithms builds trust and supports regulatory oversight. The framework includes documentation, stakeholder briefings, and customer communication. Utilities should explain restoration priorities and logic. Feedback mechanisms support continuous improvement. Regulatory reporting may require algorithm disclosure. Training ensures staff can explain and defend restoration decisions.
        """,
        key_factors=[
            "Documentation",
            "Stakeholder briefings",
            "Customer communication",
            "Feedback mechanisms",
            "Regulatory reporting",
            "Staff training"
        ],
        primary_authority=[
            "IEEE 1366",
            "State PUC",
            "DOE"
        ],
        burden_holder="Utility",
        adversary_position="Algorithm transparency exposes proprietary information and increases risk.",
        counter_arguments=[
            "Transparency builds trust and supports oversight.",
            "Feedback improves algorithms.",
            "Training ensures consistent communication."
        ],
        resolution_strategy="Document algorithms, communicate with stakeholders, and gather feedback.",
        entity_scope="Utility, Customer, Regulator",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 1366-2012"
    ),
    DoctrineBlock(
        topic="Cybersecurity: Employee Training and Awareness",
        keywords=["cybersecurity", "employee training", "awareness", "phishing", "social engineering"],
        conclusion_template="Utilities must provide regular cybersecurity training and awareness programs for all employees.",
        reasoning_framework="""
Human error is a leading cause of cyber incidents. The framework requires regular training on phishing, social engineering, and secure practices. Simulated attacks and assessments measure effectiveness. Compliance with NERC CIP and DOE C2M2 is recommended. Training should be updated regularly to address evolving threats. Incident reporting and feedback loops support continuous improvement.
        """,
        key_factors=[
            "Regular training",
            "Simulated attacks",
            "Assessment",
            "Curriculum updates",
            "Incident reporting",
            "Continuous improvement"
        ],
        primary_authority=[
            "NERC CIP",
            "DOE C2M2",
            "FERC"
        ],
        burden_holder="Utility",
        adversary_position="Training is costly and has limited impact.",
        counter_arguments=[
            "Reduces human error and incident rates.",
            "Simulated attacks improve preparedness.",
            "Continuous improvement adapts to new threats."
        ],
        resolution_strategy="Implement regular, updated training and measure effectiveness.",
        entity_scope="Utility, Vendor, Regulator",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NERC CIP-004-6"
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