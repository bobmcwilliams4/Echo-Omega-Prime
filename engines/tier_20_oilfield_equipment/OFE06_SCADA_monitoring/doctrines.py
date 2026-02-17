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
        topic="RTU Polling Interval Optimization",
        keywords=["RTU", "polling", "interval", "optimization", "latency", "bandwidth", "SCADA", "OFE06"],
        conclusion_template="The optimal RTU polling interval for OFE06 SCADA deployments should balance data freshness with network bandwidth constraints, typically ranging from 5 to 30 seconds depending on field device criticality and communication medium.",
        reasoning_framework=(
            "1. Assess the criticality of each RTU data point and the operational requirements for real-time monitoring.\n"
            "2. Analyze the communication medium (radio, cellular, fiber) and its bandwidth/latency characteristics.\n"
            "3. Evaluate the impact of polling frequency on network congestion and device CPU utilization.\n"
            "4. Reference AGA, API, and ISA guidelines for minimum recommended polling intervals.\n"
            "5. Consider the effect of polling interval on alarm/event latency and operator situational awareness.\n"
            "6. Model typical and worst-case network loads under various polling intervals.\n"
            "7. Select an interval that ensures timely data delivery without saturating the network or overloading RTUs.\n"
            "8. Validate the interval in a pilot deployment and adjust based on empirical performance data.\n"
            "9. Document the rationale and obtain stakeholder approval.\n"
            "10. Periodically review polling intervals as field conditions or network infrastructure evolve."
        ),
        key_factors=[
            "Data criticality",
            "Network bandwidth",
            "Communication latency",
            "RTU processing capacity",
            "Alarm/event response requirements"
        ],
        primary_authority=[
            "ISA-101.01",
            "API RP 1165",
            "AGA Report No. 12",
            "OFE06 SCADA Design Manual"
        ],
        burden_holder="SCADA System Integrator",
        adversary_position="Shorter polling intervals are always better for operational awareness.",
        counter_arguments=[
            "Excessively short intervals can cause network congestion and data collisions.",
            "Some field devices cannot support high-frequency polling.",
            "Longer intervals may be acceptable for non-critical data."
        ],
        resolution_strategy="Conduct a technical review with IT/OT stakeholders and validate with field trials.",
        entity_scope="OFE06 RTU and SCADA deployments",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 1165 Section 7.2"
    ),
    DoctrineBlock(
        topic="Modbus Register Mapping Best Practices",
        keywords=["Modbus", "register", "mapping", "best practices", "addressing", "OFE06"],
        conclusion_template="Modbus register mapping for OFE06 SCADA systems should use contiguous blocks, avoid overlapping addresses, and document all mappings in a central repository.",
        reasoning_framework=(
            "1. Review the Modbus register allocation for each RTU and field device.\n"
            "2. Ensure that registers are grouped by function (e.g., analog inputs, digital outputs) and assigned in contiguous blocks to minimize read/write operations.\n"
            "3. Avoid overlapping register addresses across devices to prevent data corruption.\n"
            "4. Use a standardized register map template and maintain a central mapping repository.\n"
            "5. Reference Modbus Application Protocol Specification for address conventions.\n"
            "6. Validate register assignments during FAT/SAT and update documentation as changes occur.\n"
            "7. Train SCADA and field personnel on register mapping conventions."
        ),
        key_factors=[
            "Register address uniqueness",
            "Contiguous mapping",
            "Documentation quality",
            "Ease of troubleshooting"
        ],
        primary_authority=[
            "Modbus Application Protocol Specification v1.1b3",
            "OFE06 SCADA Integration Guide"
        ],
        burden_holder="SCADA System Designer",
        adversary_position="Ad hoc register mapping is sufficient if the system works.",
        counter_arguments=[
            "Ad hoc mapping increases troubleshooting time and risk of address conflicts.",
            "Poor documentation leads to operational errors during maintenance."
        ],
        resolution_strategy="Enforce mapping reviews during design and commissioning phases.",
        entity_scope="OFE06 Modbus RTUs and SCADA systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Modbus.org Best Practice Guide"
    ),
    DoctrineBlock(
        topic="DNP3 Configuration for Oilfield SCADA",
        keywords=["DNP3", "configuration", "oilfield", "SCADA", "security", "OFE06"],
        conclusion_template="DNP3 configuration for OFE06 SCADA should enable Secure Authentication, time synchronization, and unsolicited messaging where supported.",
        reasoning_framework=(
            "1. Review DNP3 device capabilities for Secure Authentication (SA) and enable where possible.\n"
            "2. Configure time synchronization to ensure accurate event logging and sequence-of-events reporting.\n"
            "3. Enable unsolicited messaging for critical alarms to reduce polling latency.\n"
            "4. Use event buffers to minimize data loss during communication outages.\n"
            "5. Apply DNP3 Secure Authentication per IEEE 1815-2012 recommendations.\n"
            "6. Document all DNP3 settings and maintain configuration backups."
        ),
        key_factors=[
            "Security (authentication)",
            "Time accuracy",
            "Alarm/event latency",
            "Data reliability"
        ],
        primary_authority=[
            "IEEE 1815-2012 (DNP3)",
            "OFE06 SCADA Security Policy"
        ],
        burden_holder="SCADA Security Architect",
        adversary_position="DNP3 security features are unnecessary for closed OT networks.",
        counter_arguments=[
            "Insider threats and lateral movement are possible even in closed networks.",
            "Regulatory frameworks increasingly require secure protocols."
        ],
        resolution_strategy="Mandate DNP3 SA and audit compliance annually.",
        entity_scope="OFE06 DNP3-enabled devices and SCADA network",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IEEE 1815-2012 Section 5"
    ),
    DoctrineBlock(
        topic="ROC800 Flow Computer Setup for Custody Transfer",
        keywords=["ROC800", "flow computer", "custody transfer", "setup", "OFE06"],
        conclusion_template="ROC800 flow computers must be configured per API 21.1 for custody transfer, including audit trails, secure time stamps, and redundant memory.",
        reasoning_framework=(
            "1. Review API 21.1 requirements for custody transfer measurement and auditability.\n"
            "2. Configure ROC800 with secure, tamper-evident audit trails and time-stamped logs.\n"
            "3. Enable redundant memory and periodic backups to prevent data loss.\n"
            "4. Validate meter factors, calibration records, and event logs during commissioning.\n"
            "5. Document all configuration settings and store in a secure repository.\n"
            "6. Schedule periodic audits and recalibration as per regulatory requirements."
        ),
        key_factors=[
            "Auditability",
            "Data integrity",
            "Regulatory compliance",
            "Redundancy"
        ],
        primary_authority=[
            "API MPMS Chapter 21.1",
            "OFE06 Custody Transfer SOP"
        ],
        burden_holder="Measurement Engineer",
        adversary_position="Standard ROC800 configuration is sufficient for custody transfer.",
        counter_arguments=[
            "Custody transfer requires enhanced audit trails and regulatory compliance.",
            "Default configurations may not meet API 21.1 standards."
        ],
        resolution_strategy="Review by third-party measurement auditor prior to go-live.",
        entity_scope="OFE06 custody transfer points",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="API MPMS Chapter 21.1 Section 6"
    ),
    DoctrineBlock(
        topic="Flow Computer vs PLC for Custody Transfer",
        keywords=["flow computer", "PLC", "custody transfer", "comparison", "OFE06"],
        conclusion_template="Flow computers are preferred over PLCs for custody transfer in OFE06 due to specialized audit trails, regulatory compliance, and measurement accuracy.",
        reasoning_framework=(
            "1. Compare the measurement accuracy, audit trail capabilities, and regulatory compliance of flow computers and PLCs.\n"
            "2. Review API and AGA requirements for custody transfer measurement.\n"
            "3. Evaluate the ability to generate tamper-evident logs and secure data storage.\n"
            "4. Consider long-term support and firmware update policies.\n"
            "5. Assess integration complexity with SCADA and enterprise systems."
        ),
        key_factors=[
            "Measurement accuracy",
            "Audit trail robustness",
            "Regulatory compliance",
            "Integration complexity"
        ],
        primary_authority=[
            "API MPMS Chapter 21.1",
            "AGA Report No. 3",
            "OFE06 Measurement Policy"
        ],
        burden_holder="Measurement Solution Architect",
        adversary_position="PLCs can be configured to match flow computer functionality.",
        counter_arguments=[
            "PLCs lack native custody transfer features and audit trails.",
            "Regulators may not accept PLC-based custody transfer."
        ],
        resolution_strategy="Mandate flow computers for all custody transfer points.",
        entity_scope="OFE06 custody transfer sites",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="API MPMS Chapter 21.1 Section 4"
    ),
    DoctrineBlock(
        topic="Radio Telemetry Frequency Selection for Oilfield SCADA",
        keywords=["radio", "telemetry", "frequency", "selection", "SCADA", "OFE06"],
        conclusion_template="Radio telemetry frequencies for OFE06 SCADA should be selected based on FCC/IC licensing, interference studies, and terrain analysis.",
        reasoning_framework=(
            "1. Identify available frequency bands (licensed and unlicensed) for the deployment region.\n"
            "2. Conduct an interference study to assess congestion and co-channel users.\n"
            "3. Analyze terrain and path profiles to determine optimal frequency for propagation.\n"
            "4. Reference FCC and Industry Canada regulations for licensing and power limits.\n"
            "5. Select frequency that balances range, data rate, and regulatory compliance.\n"
            "6. Document frequency assignments and maintain a frequency management plan."
        ),
        key_factors=[
            "Regulatory licensing",
            "Interference environment",
            "Terrain and path loss",
            "Data rate requirements"
        ],
        primary_authority=[
            "FCC Part 90",
            "Industry Canada RSS-119",
            "OFE06 Radio Telemetry Policy"
        ],
        burden_holder="SCADA Communications Engineer",
        adversary_position="Unlicensed frequencies are always preferable for cost savings.",
        counter_arguments=[
            "Unlicensed bands are more susceptible to interference and congestion.",
            "Licensed frequencies offer greater reliability for critical SCADA data."
        ],
        resolution_strategy="Require engineering study and regulatory approval before frequency selection.",
        entity_scope="OFE06 SCADA radio networks",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FCC Part 90 Subpart T"
    ),
    DoctrineBlock(
        topic="Cellular SCADA vs Radio Telemetry",
        keywords=["cellular", "SCADA", "radio telemetry", "comparison", "OFE06"],
        conclusion_template="Cellular SCADA is suitable for non-critical, widely distributed sites, while radio telemetry is preferred for critical, latency-sensitive OFE06 operations.",
        reasoning_framework=(
            "1. Evaluate site distribution, data criticality, and latency requirements.\n"
            "2. Assess cellular coverage and reliability in the deployment area.\n"
            "3. Compare ongoing operational costs (data plans vs. radio maintenance).\n"
            "4. Consider security implications and private network options.\n"
            "5. Reference NIST and AGA guidelines for critical infrastructure communications."
        ),
        key_factors=[
            "Site criticality",
            "Network reliability",
            "Latency tolerance",
            "Operational cost"
        ],
        primary_authority=[
            "NIST SP 800-82",
            "AGA Report No. 12",
            "OFE06 Communications Policy"
        ],
        burden_holder="SCADA Network Architect",
        adversary_position="Cellular is always cheaper and easier to deploy.",
        counter_arguments=[
            "Cellular networks may not meet reliability or latency requirements for critical sites.",
            "Radio telemetry offers dedicated bandwidth and lower operational risk."
        ],
        resolution_strategy="Hybrid approach with site-by-site analysis and risk assessment.",
        entity_scope="OFE06 SCADA communication networks",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AGA Report No. 12 Section 3"
    ),
    DoctrineBlock(
        topic="Tank Level Measurement Technology Selection",
        keywords=["tank level", "measurement", "technology", "selection", "OFE06"],
        conclusion_template="Radar level transmitters are preferred for OFE06 tank level measurement due to accuracy, reliability, and minimal maintenance.",
        reasoning_framework=(
            "1. Compare radar, ultrasonic, and hydrostatic level measurement technologies.\n"
            "2. Assess environmental conditions (temperature, vapor, foam, dust) at OFE06 sites.\n"
            "3. Evaluate accuracy, maintenance requirements, and total cost of ownership.\n"
            "4. Reference API and ISA standards for custody transfer and inventory measurement.\n"
            "5. Consider integration with SCADA and legacy systems."
        ),
        key_factors=[
            "Measurement accuracy",
            "Environmental suitability",
            "Maintenance requirements",
            "Integration complexity"
        ],
        primary_authority=[
            "API MPMS Chapter 3.1B",
            "ISA-18.2",
            "OFE06 Measurement Technology Guide"
        ],
        burden_holder="Measurement Solution Designer",
        adversary_position="Ultrasonic or hydrostatic transmitters are more cost-effective.",
        counter_arguments=[
            "Radar offers better reliability in harsh oilfield environments.",
            "Long-term maintenance costs are lower for radar technology."
        ],
        resolution_strategy="Standardize on radar for new deployments; legacy sites reviewed case-by-case.",
        entity_scope="OFE06 tank level measurement systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API MPMS Chapter 3.1B Section 4"
    ),
    DoctrineBlock(
        topic="OT Network Segmentation for SCADA Cybersecurity",
        keywords=["OT", "network segmentation", "cybersecurity", "SCADA", "OFE06"],
        conclusion_template="OFE06 SCADA networks must implement OT network segmentation using firewalls, DMZs, and VLANs to isolate critical assets.",
        reasoning_framework=(
            "1. Identify critical SCADA assets and data flows within the OFE06 network.\n"
            "2. Design network architecture with segmented zones (e.g., field, control, enterprise) using firewalls and VLANs.\n"
            "3. Implement DMZs for external access (e.g., remote support, vendor connections).\n"
            "4. Apply least privilege and zero trust principles for inter-zone communications.\n"
            "5. Reference NIST and IEC standards for OT network segmentation.\n"
            "6. Periodically test segmentation effectiveness through penetration testing and audits."
        ),
        key_factors=[
            "Asset criticality",
            "Network architecture",
            "Access control",
            "Regulatory compliance"
        ],
        primary_authority=[
            "NIST SP 800-82",
            "IEC 62443-3-2",
            "OFE06 Cybersecurity Policy"
        ],
        burden_holder="OT Security Architect",
        adversary_position="Flat networks are easier to manage and troubleshoot.",
        counter_arguments=[
            "Flat networks increase risk of lateral movement and widespread compromise.",
            "Segmentation is required by most cybersecurity frameworks."
        ],
        resolution_strategy="Mandate segmentation in all new and upgraded SCADA networks.",
        entity_scope="OFE06 SCADA and OT networks",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="NIST SP 800-82 Section 5"
    ),
    DoctrineBlock(
        topic="SCADA Alarm Management - ISA-18.2 Principles",
        keywords=["SCADA", "alarm management", "ISA-18.2", "best practices", "OFE06"],
        conclusion_template="OFE06 SCADA alarm management must follow ISA-18.2 principles: rationalization, prioritization, and periodic review.",
        reasoning_framework=(
            "1. Inventory all SCADA alarms and classify by priority and consequence.\n"
            "2. Rationalize alarms to eliminate nuisance and redundant events.\n"
            "3. Implement alarm shelving, suppression, and escalation per ISA-18.2.\n"
            "4. Train operators on alarm response procedures and document alarm philosophy.\n"
            "5. Review alarm performance metrics and conduct periodic audits."
        ),
        key_factors=[
            "Alarm rationalization",
            "Operator workload",
            "Alarm prioritization",
            "Performance metrics"
        ],
        primary_authority=[
            "ISA-18.2",
            "OFE06 Alarm Management Policy"
        ],
        burden_holder="SCADA Operations Manager",
        adversary_position="All alarms should be enabled by default for maximum awareness.",
        counter_arguments=[
            "Excessive alarms lead to operator overload and missed critical events.",
            "ISA-18.2 requires rationalization and prioritization."
        ],
        resolution_strategy="Annual alarm review and rationalization workshops.",
        entity_scope="OFE06 SCADA alarm systems",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="ISA-18.2 Section 7"
    ),
    # Additional doctrine blocks (31+) for full coverage
    DoctrineBlock(
        topic="SCADA Data Historian Retention Policy",
        keywords=["SCADA", "data historian", "retention", "policy", "OFE06"],
        conclusion_template="OFE06 SCADA historian data must be retained for a minimum of 7 years for regulatory and operational analysis.",
        reasoning_framework=(
            "1. Review regulatory requirements for data retention (e.g., API, PHMSA).\n"
            "2. Assess storage capacity and data growth rates.\n"
            "3. Implement tiered storage (hot, warm, cold) for efficient access and cost management.\n"
            "4. Document retention policy and communicate to stakeholders.\n"
            "5. Periodically review and adjust retention periods as regulations or business needs change."
        ),
        key_factors=[
            "Regulatory requirements",
            "Storage capacity",
            "Data access needs",
            "Cost management"
        ],
        primary_authority=[
            "API RP 1165",
            "PHMSA 49 CFR 195",
            "OFE06 Data Management Policy"
        ],
        burden_holder="SCADA Data Steward",
        adversary_position="Shorter retention periods reduce storage costs.",
        counter_arguments=[
            "Regulatory fines for insufficient retention can exceed storage savings.",
            "Long-term data is valuable for trend analysis and incident investigation."
        ],
        resolution_strategy="Automated data archiving and periodic audits.",
        entity_scope="OFE06 SCADA historian systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 1165 Section 8"
    ),
    DoctrineBlock(
        topic="SCADA User Access Management",
        keywords=["SCADA", "user access", "management", "authentication", "authorization", "OFE06"],
        conclusion_template="OFE06 SCADA user access must be managed using role-based access control (RBAC) and multi-factor authentication (MFA) for all remote access.",
        reasoning_framework=(
            "1. Define user roles and associated privileges for SCADA operations.\n"
            "2. Implement RBAC in SCADA applications and enforce least privilege.\n"
            "3. Require MFA for all remote access to SCADA systems.\n"
            "4. Periodically review user access and remove unnecessary accounts.\n"
            "5. Document access management procedures and train personnel."
        ),
        key_factors=[
            "Role definition",
            "Authentication strength",
            "Access review frequency",
            "Regulatory compliance"
        ],
        primary_authority=[
            "NIST SP 800-53",
            "IEC 62443-2-1",
            "OFE06 Access Control Policy"
        ],
        burden_holder="OT Security Administrator",
        adversary_position="Single-factor authentication is sufficient for internal users.",
        counter_arguments=[
            "Credential theft is a leading cause of OT breaches.",
            "MFA is required by most modern cybersecurity frameworks."
        ],
        resolution_strategy="Quarterly access reviews and mandatory MFA for all users.",
        entity_scope="OFE06 SCADA user accounts",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="NIST SP 800-53 AC-2"
    ),
    DoctrineBlock(
        topic="SCADA Patch Management Policy",
        keywords=["SCADA", "patch management", "policy", "OFE06"],
        conclusion_template="OFE06 SCADA systems must follow a quarterly patch cycle, with expedited patching for critical vulnerabilities.",
        reasoning_framework=(
            "1. Maintain an inventory of all SCADA assets and software versions.\n"
            "2. Monitor vendor advisories for new vulnerabilities and patches.\n"
            "3. Schedule quarterly patch windows and test patches in a staging environment.\n"
            "4. Expedite patching for critical vulnerabilities per CVSS score.\n"
            "5. Document all patching activities and maintain rollback plans."
        ),
        key_factors=[
            "Asset inventory",
            "Vulnerability severity",
            "Patch testing",
            "Downtime scheduling"
        ],
        primary_authority=[
            "NIST SP 800-40",
            "IEC 62443-2-3",
            "OFE06 Patch Management Policy"
        ],
        burden_holder="OT Systems Administrator",
        adversary_position="Annual patching is sufficient for air-gapped SCADA systems.",
        counter_arguments=[
            "Threat actors target unpatched OT systems.",
            "Quarterly patching balances risk and operational impact."
        ],
        resolution_strategy="Patch management audits and incident-driven reviews.",
        entity_scope="OFE06 SCADA servers and workstations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-40 Section 4"
    ),
    DoctrineBlock(
        topic="SCADA Remote Access Security",
        keywords=["SCADA", "remote access", "security", "VPN", "OFE06"],
        conclusion_template="All remote access to OFE06 SCADA must use VPN with strong encryption and session logging.",
        reasoning_framework=(
            "1. Require VPN with AES-256 encryption for all remote SCADA access.\n"
            "2. Enable session logging and periodic review of remote access logs.\n"
            "3. Restrict remote access to authorized personnel and devices.\n"
            "4. Implement session timeouts and automatic disconnects for inactivity.\n"
            "5. Reference NIST and IEC guidelines for remote OT access."
        ),
        key_factors=[
            "Encryption strength",
            "Access logging",
            "Device authentication",
            "Session management"
        ],
        primary_authority=[
            "NIST SP 800-113",
            "IEC 62443-3-3",
            "OFE06 Remote Access Policy"
        ],
        burden_holder="OT Security Engineer",
        adversary_position="Remote desktop without VPN is sufficient for trusted users.",
        counter_arguments=[
            "Unencrypted remote access exposes SCADA to interception and compromise.",
            "VPNs provide layered security and auditability."
        ],
        resolution_strategy="Quarterly remote access reviews and technical controls.",
        entity_scope="OFE06 SCADA remote access endpoints",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-113 Section 5"
    ),
    DoctrineBlock(
        topic="SCADA Backup and Disaster Recovery",
        keywords=["SCADA", "backup", "disaster recovery", "OFE06"],
        conclusion_template="OFE06 SCADA systems must have daily backups and a tested disaster recovery plan with RTO < 24 hours.",
        reasoning_framework=(
            "1. Identify critical SCADA data and configuration files for backup.\n"
            "2. Schedule automated daily backups to secure, offsite storage.\n"
            "3. Develop and document a disaster recovery plan with defined RTO and RPO.\n"
            "4. Test disaster recovery procedures at least annually.\n"
            "5. Maintain backup logs and verify backup integrity."
        ),
        key_factors=[
            "Backup frequency",
            "Offsite storage",
            "Recovery time objective (RTO)",
            "Testing frequency"
        ],
        primary_authority=[
            "NIST SP 800-34",
            "OFE06 DR Policy"
        ],
        burden_holder="OT Systems Administrator",
        adversary_position="Weekly backups are sufficient for SCADA systems.",
        counter_arguments=[
            "Daily backups minimize data loss in the event of failure.",
            "Regulatory frameworks often require daily or more frequent backups."
        ],
        resolution_strategy="Annual DR drills and backup verification.",
        entity_scope="OFE06 SCADA servers and historian systems",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="NIST SP 800-34 Section 3"
    ),
    DoctrineBlock(
        topic="SCADA Change Management",
        keywords=["SCADA", "change management", "OFE06"],
        conclusion_template="All changes to OFE06 SCADA systems must follow formal change management with documented risk assessment and rollback plans.",
        reasoning_framework=(
            "1. Submit all SCADA changes through a formal change request process.\n"
            "2. Assess risks, impacts, and required downtime for each change.\n"
            "3. Develop rollback plans for critical changes.\n"
            "4. Obtain approval from change advisory board (CAB) before implementation.\n"
            "5. Document all changes and lessons learned."
        ),
        key_factors=[
            "Change documentation",
            "Risk assessment",
            "CAB approval",
            "Rollback planning"
        ],
        primary_authority=[
            "ITIL Change Management",
            "OFE06 Change Management Policy"
        ],
        burden_holder="SCADA Project Manager",
        adversary_position="Informal changes are faster and reduce project delays.",
        counter_arguments=[
            "Uncontrolled changes increase risk of outages and security incidents.",
            "Formal change management is required for regulatory compliance."
        ],
        resolution_strategy="Monthly change management audits.",
        entity_scope="OFE06 SCADA infrastructure",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="ITIL Change Management 4.2"
    ),
    DoctrineBlock(
        topic="SCADA Incident Response",
        keywords=["SCADA", "incident response", "OFE06"],
        conclusion_template="OFE06 SCADA must have a documented incident response plan with defined roles, escalation paths, and post-incident reviews.",
        reasoning_framework=(
            "1. Develop an incident response plan specific to SCADA threats and scenarios.\n"
            "2. Define roles, responsibilities, and escalation procedures.\n"
            "3. Train personnel on incident response procedures.\n"
            "4. Conduct post-incident reviews to identify root causes and corrective actions.\n"
            "5. Update the plan annually or after major incidents."
        ),
        key_factors=[
            "Plan documentation",
            "Role definition",
            "Training frequency",
            "Post-incident review"
        ],
        primary_authority=[
            "NIST SP 800-61",
            "OFE06 IR Policy"
        ],
        burden_holder="OT Security Manager",
        adversary_position="Ad hoc response is sufficient for rare SCADA incidents.",
        counter_arguments=[
            "Documented plans improve response time and reduce impact.",
            "Regulators require formal incident response procedures."
        ],
        resolution_strategy="Annual IR drills and plan updates.",
        entity_scope="OFE06 SCADA operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-61 Section 2"
    ),
    DoctrineBlock(
        topic="SCADA Vendor Management",
        keywords=["SCADA", "vendor management", "third-party", "OFE06"],
        conclusion_template="All OFE06 SCADA vendors must sign security agreements and undergo annual risk assessments.",
        reasoning_framework=(
            "1. Require all SCADA vendors to sign security and confidentiality agreements.\n"
            "2. Conduct annual risk assessments of vendor access and services.\n"
            "3. Limit vendor access to least privilege and monitor all activity.\n"
            "4. Review vendor compliance with OFE06 security policies."
        ),
        key_factors=[
            "Vendor agreements",
            "Risk assessment",
            "Access monitoring",
            "Compliance reviews"
        ],
        primary_authority=[
            "NIST SP 800-161",
            "OFE06 Vendor Management Policy"
        ],
        burden_holder="SCADA Procurement Manager",
        adversary_position="Vendor management adds unnecessary overhead.",
        counter_arguments=[
            "Vendors are a major source of OT security incidents.",
            "Formal management reduces risk and ensures accountability."
        ],
        resolution_strategy="Annual vendor reviews and access audits.",
        entity_scope="OFE06 SCADA vendor relationships",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-161 Section 5"
    ),
    DoctrineBlock(
        topic="SCADA Time Synchronization",
        keywords=["SCADA", "time synchronization", "NTP", "OFE06"],
        conclusion_template="All OFE06 SCADA systems must use NTP with GPS reference for time synchronization.",
        reasoning_framework=(
            "1. Deploy NTP servers with GPS reference at central SCADA locations.\n"
            "2. Configure all SCADA servers, RTUs, and flow computers to synchronize with NTP.\n"
            "3. Monitor time drift and synchronize at least daily.\n"
            "4. Document time synchronization architecture and procedures."
        ),
        key_factors=[
            "NTP server reliability",
            "GPS reference",
            "Time drift monitoring",
            "Documentation"
        ],
        primary_authority=[
            "NIST SP 800-53 AU-8",
            "OFE06 Time Sync Policy"
        ],
        burden_holder="SCADA Systems Engineer",
        adversary_position="Manual time setting is sufficient for SCADA devices.",
        counter_arguments=[
            "Manual time setting leads to drift and inaccurate logs.",
            "NTP with GPS ensures consistent time across all devices."
        ],
        resolution_strategy="Quarterly time sync audits.",
        entity_scope="OFE06 SCADA and field devices",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="NIST SP 800-53 AU-8"
    ),
    DoctrineBlock(
        topic="SCADA Encryption of Data in Transit",
        keywords=["SCADA", "encryption", "data in transit", "OFE06"],
        conclusion_template="All OFE06 SCADA data in transit must be encrypted using TLS 1.2 or higher.",
        reasoning_framework=(
            "1. Identify all SCADA data flows over untrusted networks.\n"
            "2. Enable TLS 1.2+ for all SCADA communications, including HMI, historian, and remote access.\n"
            "3. Disable legacy protocols and ciphers.\n"
            "4. Monitor for unencrypted traffic and remediate promptly."
        ),
        key_factors=[
            "Protocol version",
            "Cipher strength",
            "Legacy protocol usage",
            "Traffic monitoring"
        ],
        primary_authority=[
            "NIST SP 800-52",
            "OFE06 Encryption Policy"
        ],
        burden_holder="OT Security Engineer",
        adversary_position="Encryption adds unnecessary latency to SCADA traffic.",
        counter_arguments=[
            "Modern CPUs handle TLS with minimal performance impact.",
            "Encryption is required for regulatory compliance and risk reduction."
        ],
        resolution_strategy="Annual encryption audits and technical controls.",
        entity_scope="OFE06 SCADA data flows",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-52 Section 3"
    ),
    DoctrineBlock(
        topic="SCADA Device Hardening",
        keywords=["SCADA", "device hardening", "OFE06"],
        conclusion_template="All OFE06 SCADA field devices must be hardened by disabling unused services and changing default credentials.",
        reasoning_framework=(
            "1. Inventory all field devices and their enabled services.\n"
            "2. Disable all unused services and ports.\n"
            "3. Change default credentials and enforce strong password policies.\n"
            "4. Document hardening steps and verify during commissioning."
        ),
        key_factors=[
            "Service minimization",
            "Credential management",
            "Documentation",
            "Verification"
        ],
        primary_authority=[
            "NIST SP 800-82",
            "IEC 62443-3-3",
            "OFE06 Device Hardening Policy"
        ],
        burden_holder="Field Instrumentation Technician",
        adversary_position="Default configurations are sufficient for field devices.",
        counter_arguments=[
            "Default credentials are a leading cause of OT breaches.",
            "Unused services increase attack surface."
        ],
        resolution_strategy="Commissioning checklists and periodic device audits.",
        entity_scope="OFE06 field devices",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-82 Section 5"
    ),
    DoctrineBlock(
        topic="SCADA Network Monitoring",
        keywords=["SCADA", "network monitoring", "OFE06"],
        conclusion_template="OFE06 SCADA networks must be continuously monitored for anomalies using IDS/IPS and flow analysis.",
        reasoning_framework=(
            "1. Deploy IDS/IPS sensors at key network segments.\n"
            "2. Collect and analyze network flow data for anomalies.\n"
            "3. Integrate alerts with SOC and incident response workflows.\n"
            "4. Review monitoring coverage and update as network evolves."
        ),
        key_factors=[
            "IDS/IPS deployment",
            "Anomaly detection",
            "Alert integration",
            "Coverage review"
        ],
        primary_authority=[
            "NIST SP 800-94",
            "OFE06 Network Monitoring Policy"
        ],
        burden_holder="OT Security Analyst",
        adversary_position="Periodic manual review is sufficient for SCADA networks.",
        counter_arguments=[
            "Automated monitoring detects threats in real time.",
            "Manual review is insufficient for modern threat landscape."
        ],
        resolution_strategy="Continuous monitoring and quarterly coverage reviews.",
        entity_scope="OFE06 SCADA networks",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-94 Section 4"
    ),
    DoctrineBlock(
        topic="SCADA Firmware Management",
        keywords=["SCADA", "firmware management", "OFE06"],
        conclusion_template="OFE06 SCADA field device firmware must be updated annually or as critical patches are released.",
        reasoning_framework=(
            "1. Maintain an inventory of device firmware versions.\n"
            "2. Monitor vendor advisories for firmware updates.\n"
            "3. Schedule annual firmware updates and test in staging environments.\n"
            "4. Expedite critical patches as needed.\n"
            "5. Document all firmware changes."
        ),
        key_factors=[
            "Firmware inventory",
            "Patch monitoring",
            "Update scheduling",
            "Documentation"
        ],
        primary_authority=[
            "IEC 62443-2-3",
            "OFE06 Firmware Management Policy"
        ],
        burden_holder="Field Device Engineer",
        adversary_position="Firmware updates are risky and should be avoided.",
        counter_arguments=[
            "Unpatched firmware exposes devices to known vulnerabilities.",
            "Testing and documentation mitigate update risks."
        ],
        resolution_strategy="Annual firmware reviews and staged rollouts.",
        entity_scope="OFE06 field devices",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IEC 62443-2-3 Section 7"
    ),
    DoctrineBlock(
        topic="SCADA Wireless Security",
        keywords=["SCADA", "wireless security", "OFE06"],
        conclusion_template="All OFE06 SCADA wireless networks must use WPA2-Enterprise or higher with EAP-TLS authentication.",
        reasoning_framework=(
            "1. Configure wireless access points for WPA2-Enterprise or WPA3 security.\n"
            "2. Implement EAP-TLS for mutual authentication.\n"
            "3. Monitor for rogue access points and unauthorized connections.\n"
            "4. Periodically review wireless security settings."
        ),
        key_factors=[
            "Authentication protocol",
            "Encryption strength",
            "Rogue AP detection",
            "Policy enforcement"
        ],
        primary_authority=[
            "NIST SP 800-153",
            "OFE06 Wireless Security Policy"
        ],
        burden_holder="OT Network Engineer",
        adversary_position="WPA2-PSK is sufficient for SCADA wireless networks.",
        counter_arguments=[
            "Enterprise authentication prevents credential sharing and spoofing.",
            "WPA2-PSK is vulnerable to brute-force attacks."
        ],
        resolution_strategy="Annual wireless security audits.",
        entity_scope="OFE06 SCADA wireless networks",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-153 Section 3"
    ),
    DoctrineBlock(
        topic="SCADA Asset Inventory",
        keywords=["SCADA", "asset inventory", "OFE06"],
        conclusion_template="OFE06 SCADA must maintain a real-time asset inventory including hardware, software, and firmware versions.",
        reasoning_framework=(
            "1. Deploy automated asset discovery tools across SCADA networks.\n"
            "2. Record hardware, software, and firmware versions for all assets.\n"
            "3. Update inventory upon commissioning, decommissioning, or changes.\n"
            "4. Review inventory accuracy quarterly."
        ),
        key_factors=[
            "Discovery tool coverage",
            "Inventory accuracy",
            "Update frequency",
            "Version tracking"
        ],
        primary_authority=[
            "NIST SP 800-53 CM-8",
            "OFE06 Asset Management Policy"
        ],
        burden_holder="SCADA Asset Manager",
        adversary_position="Manual spreadsheets are sufficient for asset tracking.",
        counter_arguments=[
            "Manual tracking is error-prone and quickly outdated.",
            "Automated tools improve accuracy and compliance."
        ],
        resolution_strategy="Quarterly inventory audits.",
        entity_scope="OFE06 SCADA assets",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-53 CM-8"
    ),
    DoctrineBlock(
        topic="SCADA Configuration Management",
        keywords=["SCADA", "configuration management", "OFE06"],
        conclusion_template="All OFE06 SCADA configurations must be version controlled and backed up regularly.",
        reasoning_framework=(
            "1. Store all SCADA configurations in a version-controlled repository.\n"
            "2. Backup configurations after every change and before major upgrades.\n"
            "3. Restrict configuration changes to authorized personnel.\n"
            "4. Periodically review configuration management practices."
        ),
        key_factors=[
            "Version control",
            "Backup frequency",
            "Access control",
            "Review process"
        ],
        primary_authority=[
            "NIST SP 800-128",
            "OFE06 Configuration Management Policy"
        ],
        burden_holder="SCADA Configuration Manager",
        adversary_position="Configuration management is unnecessary for small SCADA systems.",
        counter_arguments=[
            "Version control prevents configuration drift and enables rapid recovery.",
            "Backups are essential for disaster recovery."
        ],
        resolution_strategy="Annual configuration management audits.",
        entity_scope="OFE06 SCADA configurations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-128 Section 4"
    ),
    DoctrineBlock(
        topic="SCADA Physical Security",
        keywords=["SCADA", "physical security", "OFE06"],
        conclusion_template="All OFE06 SCADA sites must have physical access controls, surveillance, and intrusion detection.",
        reasoning_framework=(
            "1. Install card access systems at all SCADA site entry points.\n"
            "2. Deploy surveillance cameras and intrusion detection sensors.\n"
            "3. Monitor access logs and investigate anomalies.\n"
            "4. Test physical security controls annually."
        ),
        key_factors=[
            "Access control",
            "Surveillance coverage",
            "Intrusion detection",
            "Monitoring"
        ],
        primary_authority=[
            "NIST SP 800-116",
            "OFE06 Physical Security Policy"
        ],
        burden_holder="Facilities Security Manager",
        adversary_position="Physical security is less important than cybersecurity.",
        counter_arguments=[
            "Physical breaches can bypass all cybersecurity controls.",
            "Regulations require layered physical security."
        ],
        resolution_strategy="Annual physical security audits.",
        entity_scope="OFE06 SCADA sites",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-116 Section 3"
    ),
    DoctrineBlock(
        topic="SCADA Perimeter Defense",
        keywords=["SCADA", "perimeter defense", "firewall", "OFE06"],
        conclusion_template="OFE06 SCADA networks must deploy firewalls at all external and inter-zone boundaries.",
        reasoning_framework=(
            "1. Identify all network boundaries and data flows.\n"
            "2. Deploy firewalls with default-deny rules at each boundary.\n"
            "3. Regularly review and update firewall rules.\n"
            "4. Monitor firewall logs for anomalies."
        ),
        key_factors=[
            "Boundary identification",
            "Firewall rule management",
            "Log monitoring",
            "Policy updates"
        ],
        primary_authority=[
            "NIST SP 800-41",
            "OFE06 Network Security Policy"
        ],
        burden_holder="OT Network Security Engineer",
        adversary_position="Firewalls add unnecessary complexity to SCADA networks.",
        counter_arguments=[
            "Firewalls are essential for defense-in-depth.",
            "Modern SCADA threats require layered perimeter controls."
        ],
        resolution_strategy="Quarterly firewall rule reviews.",
        entity_scope="OFE06 SCADA network boundaries",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="NIST SP 800-41 Section 4"
    ),
    DoctrineBlock(
        topic="SCADA Application Whitelisting",
        keywords=["SCADA", "application whitelisting", "OFE06"],
        conclusion_template="OFE06 SCADA servers must implement application whitelisting to prevent unauthorized software execution.",
        reasoning_framework=(
            "1. Inventory all approved SCADA applications and services.\n"
            "2. Deploy application whitelisting tools on all SCADA servers.\n"
            "3. Monitor for and block unauthorized executables.\n"
            "4. Review and update whitelist as applications change."
        ),
        key_factors=[
            "Application inventory",
            "Whitelisting tool deployment",
            "Monitoring",
            "Whitelist updates"
        ],
        primary_authority=[
            "NIST SP 800-167",
            "OFE06 Application Security Policy"
        ],
        burden_holder="SCADA Systems Administrator",
        adversary_position="Antivirus is sufficient for SCADA server protection.",
        counter_arguments=[
            "Whitelisting blocks unknown and zero-day threats.",
            "Antivirus alone is insufficient for modern OT environments."
        ],
        resolution_strategy="Annual whitelist reviews and incident-driven updates.",
        entity_scope="OFE06 SCADA servers",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-167 Section 5"
    ),
    DoctrineBlock(
        topic="SCADA Logging and Audit Trails",
        keywords=["SCADA", "logging", "audit trails", "OFE06"],
        conclusion_template="OFE06 SCADA systems must log all user actions and security events, with logs retained for a minimum of 2 years.",
        reasoning_framework=(
            "1. Enable detailed logging for all user actions and security events.\n"
            "2. Forward logs to a centralized SIEM for analysis and retention.\n"
            "3. Review logs regularly for anomalies and compliance.\n"
            "4. Retain logs for at least 2 years or as required by regulation."
        ),
        key_factors=[
            "Log detail",
            "Centralization",
            "Retention period",
            "Review frequency"
        ],
        primary_authority=[
            "NIST SP 800-92",
            "OFE06 Logging Policy"
        ],
        burden_holder="SCADA Audit Manager",
        adversary_position="Local logs are sufficient for SCADA systems.",
        counter_arguments=[
            "Centralized logs improve detection and incident response.",
            "Local logs can be lost or tampered with."
        ],
        resolution_strategy="Quarterly log review and retention audits.",
        entity_scope="OFE06 SCADA systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-92 Section 3"
    ),
    DoctrineBlock(
        topic="SCADA Anomaly Detection",
        keywords=["SCADA", "anomaly detection", "OFE06"],
        conclusion_template="OFE06 SCADA networks must implement anomaly detection for both IT and OT traffic.",
        reasoning_framework=(
            "1. Deploy anomaly detection tools capable of analyzing IT and OT protocols.\n"
            "2. Establish baselines for normal network and process behavior.\n"
            "3. Alert on deviations from baseline and investigate promptly.\n"
            "4. Periodically retrain detection models as network evolves."
        ),
        key_factors=[
            "Tool capability",
            "Baseline accuracy",
            "Alert response",
            "Model retraining"
        ],
        primary_authority=[
            "NIST SP 800-94",
            "OFE06 Anomaly Detection Policy"
        ],
        burden_holder="OT Security Analyst",
        adversary_position="Signature-based detection is sufficient for SCADA security.",
        counter_arguments=[
            "Anomaly detection identifies unknown and zero-day threats.",
            "Signature-based tools miss novel attack techniques."
        ],
        resolution_strategy="Annual tool reviews and tuning.",
        entity_scope="OFE06 SCADA networks",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-94 Section 6"
    ),
    DoctrineBlock(
        topic="SCADA Network Redundancy",
        keywords=["SCADA", "network redundancy", "OFE06"],
        conclusion_template="All critical OFE06 SCADA network paths must be redundant to ensure high availability.",
        reasoning_framework=(
            "1. Identify critical SCADA data paths and single points of failure.\n"
            "2. Design redundant network links and failover mechanisms.\n"
            "3. Test redundancy during commissioning and annually.\n"
            "4. Document redundancy architecture and update as network evolves."
        ),
        key_factors=[
            "Critical path identification",
            "Redundant link design",
            "Testing",
            "Documentation"
        ],
        primary_authority=[
            "IEC 62443-3-3",
            "OFE06 Network Design Guide"
        ],
        burden_holder="OT Network Architect",
        adversary_position="Redundancy adds unnecessary cost and complexity.",
        counter_arguments=[
            "Redundancy is essential for high availability and regulatory compliance.",
            "Downtime costs can exceed redundancy investment."
        ],
        resolution_strategy="Annual redundancy testing and cost-benefit reviews.",
        entity_scope="OFE06 SCADA networks",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 62443-3-3 SR 2.2"
    ),
    DoctrineBlock(
        topic="SCADA Protocol Whitelisting",
        keywords=["SCADA", "protocol whitelisting", "OFE06"],
        conclusion_template="OFE06 SCADA firewalls must whitelist only required protocols and ports.",
        reasoning_framework=(
            "1. Inventory all required SCADA protocols and ports for operations.\n"
            "2. Configure firewalls to allow only these protocols and ports.\n"
            "3. Monitor for unauthorized protocol usage and alert on violations.\n"
            "4. Review and update whitelist as system changes."
        ),
        key_factors=[
            "Protocol inventory",
            "Firewall configuration",
            "Monitoring",
            "Review process"
        ],
        primary_authority=[
            "NIST SP 800-41",
            "OFE06 Protocol Policy"
        ],
        burden_holder="OT Network Security Engineer",
        adversary_position="Open port policies simplify troubleshooting.",
        counter_arguments=[
            "Open ports increase attack surface.",
            "Whitelisting is required for defense-in-depth."
        ],
        resolution_strategy="Quarterly protocol reviews and firewall audits.",
        entity_scope="OFE06 SCADA firewalls",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-41 Section 5"
    ),
    DoctrineBlock(
        topic="SCADA Endpoint Protection",
        keywords=["SCADA", "endpoint protection", "OFE06"],
        conclusion_template="All OFE06 SCADA endpoints must run OT-aware endpoint protection with centralized management.",
        reasoning_framework=(
            "1. Deploy endpoint protection solutions designed for OT environments.\n"
            "2. Enable centralized management and alerting.\n"
            "3. Monitor for and respond to endpoint threats.\n"
            "4. Update endpoint protection signatures regularly."
        ),
        key_factors=[
            "OT-aware protection",
            "Centralized management",
            "Alerting",
            "Signature updates"
        ],
        primary_authority=[
            "NIST SP 800-83",
            "OFE06 Endpoint Security Policy"
        ],
        burden_holder="OT Security Engineer",
        adversary_position="Standard antivirus is sufficient for SCADA endpoints.",
        counter_arguments=[
            "OT environments require specialized protection.",
            "Centralized management improves response time and compliance."
        ],
        resolution_strategy="Annual endpoint protection reviews.",
        entity_scope="OFE06 SCADA endpoints",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-83 Section 4"
    ),
    DoctrineBlock(
        topic="SCADA Data Loss Prevention",
        keywords=["SCADA", "data loss prevention", "OFE06"],
        conclusion_template="OFE06 SCADA must implement data loss prevention (DLP) for critical data exfiltration points.",
        reasoning_framework=(
            "1. Identify critical SCADA data and exfiltration vectors.\n"
            "2. Deploy DLP tools at network egress points.\n"
            "3. Monitor and alert on unauthorized data transfers.\n"
            "4. Review DLP effectiveness annually."
        ),
        key_factors=[
            "Data classification",
            "Exfiltration vector identification",
            "DLP tool deployment",
            "Monitoring"
        ],
        primary_authority=[
            "NIST SP 800-53 SC-7",
            "OFE06 DLP Policy"
        ],
        burden_holder="OT Security Analyst",
        adversary_position="DLP is unnecessary for closed SCADA networks.",
        counter_arguments=[
            "Insider threats and misconfigurations can cause data loss.",
            "Regulatory frameworks require DLP for critical infrastructure."
        ],
        resolution_strategy="Annual DLP reviews and incident-driven updates.",
        entity_scope="OFE06 SCADA data flows",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-53 SC-7"
    ),
    DoctrineBlock(
        topic="SCADA Device Commissioning Checklist",
        keywords=["SCADA", "device commissioning", "checklist", "OFE06"],
        conclusion_template="All OFE06 SCADA devices must be commissioned using a standardized checklist covering configuration, security, and documentation.",
        reasoning_framework=(
            "1. Develop a commissioning checklist for all SCADA device types.\n"
            "2. Verify configuration, security settings, and documentation for each device.\n"
            "3. Obtain sign-off from commissioning engineer and OT security.\n"
            "4. Store completed checklists in central repository."
        ),
        key_factors=[
            "Checklist completeness",
            "Security verification",
            "Documentation",
            "Sign-off process"
        ],
        primary_authority=[
            "OFE06 Commissioning Policy"
        ],
        burden_holder="Commissioning Engineer",
        adversary_position="Commissioning checklists are unnecessary overhead.",
        counter_arguments=[
            "Checklists ensure consistency and reduce errors.",
            "Regulatory audits require commissioning documentation."
        ],
        resolution_strategy="Mandatory checklist use and periodic audits.",
        entity_scope="OFE06 SCADA devices",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="OFE06 Commissioning Policy Section 2"
    ),
    DoctrineBlock(
        topic="SCADA Decommissioning Policy",
        keywords=["SCADA", "decommissioning", "policy", "OFE06"],
        conclusion_template="All OFE06 SCADA assets must be decommissioned per policy, including data wiping and access removal.",
        reasoning_framework=(
            "1. Develop decommissioning procedures for all SCADA asset types.\n"
            "2. Wipe all data and remove credentials before asset disposal.\n"
            "3. Update asset inventory and remove from network monitoring.\n"
            "4. Document decommissioning and retain records."
        ),
        key_factors=[
            "Data wiping",
            "Credential removal",
            "Inventory update",
            "Documentation"
        ],
        primary_authority=[
            "NIST SP 800-88",
            "OFE06 Decommissioning Policy"
        ],
        burden_holder="SCADA Asset Manager",
        adversary_position="Physical removal is sufficient for decommissioning.",
        counter_arguments=[
            "Residual data and credentials can be exploited.",
            "Regulations require secure decommissioning."
        ],
        resolution_strategy="Mandatory decommissioning checklists and audits.",
        entity_scope="OFE06 SCADA assets",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-88 Section 4"
    ),
    DoctrineBlock(
        topic="SCADA Third-Party Integration Security",
        keywords=["SCADA", "third-party integration", "security", "OFE06"],
        conclusion_template="All third-party integrations with OFE06 SCADA must be reviewed for security risks and approved by OT security.",
        reasoning_framework=(
            "1. Identify all third-party integrations and data flows.\n"
            "2. Conduct security risk assessments for each integration.\n"
            "3. Require OT security approval before go-live.\n"
            "4. Monitor integrations for anomalous activity."
        ),
        key_factors=[
            "Integration inventory",
            "Risk assessment",
            "Approval process",
            "Monitoring"
        ],
        primary_authority=[
            "NIST SP 800-161",
            "OFE06 Integration Policy"
        ],
        burden_holder="SCADA Integration Manager",
        adversary_position="Integration expedites project delivery.",
        counter_arguments=[
            "Unvetted integrations introduce security risks.",
            "Regulatory frameworks require integration reviews."
        ],
        resolution_strategy="Mandatory integration reviews and monitoring.",
        entity_scope="OFE06 SCADA integrations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-161 Section 6"
    ),
    DoctrineBlock(
        topic="SCADA Mobile Device Policy",
        keywords=["SCADA", "mobile device", "policy", "OFE06"],
        conclusion_template="OFE06 SCADA mobile device access must be restricted to managed, encrypted devices with MDM controls.",
        reasoning_framework=(
            "1. Restrict SCADA access to managed mobile devices only.\n"
            "2. Require device encryption and MDM enrollment.\n"
            "3. Monitor device compliance and revoke access for non-compliance.\n"
            "4. Review mobile device policy annually."
        ),
        key_factors=[
            "Device management",
            "Encryption",
            "Compliance monitoring",
            "Policy review"
        ],
        primary_authority=[
            "NIST SP 800-124",
            "OFE06 Mobile Device Policy"
        ],
        burden_holder="OT Security Administrator",
        adversary_position="Personal devices can be used for SCADA access.",
        counter_arguments=[
            "Personal devices increase risk of data loss and compromise.",
            "MDM ensures policy enforcement and rapid response."
        ],
        resolution_strategy="Annual mobile device audits.",
        entity_scope="OFE06 SCADA mobile access",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-124 Section 5"
    ),
    DoctrineBlock(
        topic="SCADA Cloud Integration Policy",
        keywords=["SCADA", "cloud integration", "policy", "OFE06"],
        conclusion_template="OFE06 SCADA cloud integrations must use secure APIs, encrypted data flows, and be approved by OT security.",
        reasoning_framework=(
            "1. Inventory all SCADA cloud integrations and data flows.\n"
            "2. Require secure API gateways and TLS encryption for all cloud communications.\n"
            "3. Obtain OT security approval before deployment.\n"
            "4. Monitor cloud integrations for compliance and anomalies."
        ),
        key_factors=[
            "API security",
            "Encryption",
            "Approval process",
            "Monitoring"
        ],
        primary_authority=[
            "NIST SP 800-210",
            "OFE06 Cloud Policy"
        ],
        burden_holder="SCADA Cloud Integration Manager",
        adversary_position="Direct cloud connections expedite analytics.",
        counter_arguments=[
            "Unsecured cloud connections expose SCADA to external threats.",
            "Regulatory frameworks require secure integration."
        ],
        resolution_strategy="Mandatory cloud integration reviews.",
        entity_scope="OFE06 SCADA cloud integrations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-210 Section 4"
    ),
    DoctrineBlock(
        topic="SCADA Data Classification",
        keywords=["SCADA", "data classification", "OFE06"],
        conclusion_template="All OFE06 SCADA data must be classified by sensitivity and handled per policy.",
        reasoning_framework=(
            "1. Develop a data classification scheme for SCADA data (e.g., public, internal, confidential, restricted).\n"
            "2. Train personnel on classification and handling procedures.\n"
            "3. Monitor for policy violations and remediate promptly.\n"
            "4. Review classification scheme annually."
        ),
        key_factors=[
            "Classification scheme",
            "Training",
            "Monitoring",
            "Policy review"
        ],
        primary_authority=[
            "NIST SP 800-60",
            "OFE06 Data Classification Policy"
        ],
        burden_holder="SCADA Data Steward",
        adversary_position="All SCADA data can be treated the same.",
        counter_arguments=[
            "Sensitive data requires additional controls.",
            "Classification enables risk-based protection."
        ],
        resolution_strategy="Annual classification audits.",
        entity_scope="OFE06 SCADA data",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-60 Section 3"
    ),
    DoctrineBlock(
        topic="SCADA Maintenance Window Policy",
        keywords=["SCADA", "maintenance window", "policy", "OFE06"],
        conclusion_template="All OFE06 SCADA maintenance must be scheduled during approved maintenance windows with prior notification.",
        reasoning_framework=(
            "1. Define approved maintenance windows for SCADA systems.\n"
            "2. Require advance notification to stakeholders before maintenance.\n"
            "3. Document all maintenance activities and outcomes.\n"
            "4. Review maintenance window policy annually."
        ),
        key_factors=[
            "Window definition",
            "Notification process",
            "Documentation",
            "Policy review"
        ],
        primary_authority=[
            "OFE06 Maintenance Policy"
        ],
        burden_holder="SCADA Maintenance Coordinator",
        adversary_position="Ad hoc maintenance reduces downtime.",
        counter_arguments=[
            "Unscheduled maintenance increases risk of outages and conflicts.",
            "Stakeholder notification is essential for operational continuity."
        ],
        resolution_strategy="Mandatory maintenance scheduling and documentation.",
        entity_scope="OFE06 SCADA systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="OFE06 Maintenance Policy Section 2"
    ),
    DoctrineBlock(
        topic="SCADA System Health Monitoring",
        keywords=["SCADA", "system health", "monitoring", "OFE06"],
        conclusion_template="OFE06 SCADA must continuously monitor system health (CPU, memory, disk, network) with automated alerting.",
        reasoning_framework=(
            "1. Deploy monitoring tools for SCADA servers and network devices.\n"
            "2. Set thresholds for CPU, memory, disk, and network usage.\n"
            "3. Configure automated alerts for threshold violations.\n"
            "4. Review system health data regularly and remediate issues."
        ),
        key_factors=[
            "Monitoring tool deployment",
            "Threshold setting",
            "Alerting",
            "Data review"
        ],
        primary_authority=[
            "OFE06 System Monitoring Policy"
        ],
        burden_holder="SCADA Systems Administrator",
        adversary_position="Manual health checks are sufficient.",
        counter_arguments=[
            "Automated monitoring detects issues before they impact operations.",
            "Manual checks are prone to human error and delays."
        ],
        resolution_strategy="Continuous monitoring and quarterly reviews.",
        entity_scope="OFE06 SCADA infrastructure",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="OFE06 System Monitoring Policy Section 3"
    ),
    DoctrineBlock(
        topic="SCADA Alarm Suppression Policy",
        keywords=["SCADA", "alarm suppression", "policy", "OFE06"],
        conclusion_template="OFE06 SCADA alarm suppression must be documented, justified, and time-limited.",
        reasoning_framework=(
            "1. Document all instances of alarm suppression, including justification and duration.\n"
            "2. Limit suppression to the minimum necessary period.\n"
            "3. Review suppressed alarms regularly and restore as soon as possible.\n"
            "4. Audit alarm suppression records quarterly."
        ),
        key_factors=[
            "Documentation",
            "Justification",
            "Duration control",
            "Audit frequency"
        ],
        primary_authority=[
            "ISA-18.2",
            "OFE06 Alarm Management Policy"
        ],
        burden_holder="SCADA Operations Supervisor",
        adversary_position="Alarm suppression can be indefinite if convenient.",
        counter_arguments=[
            "Indefinite suppression increases operational risk.",
            "ISA-18.2 requires justification and review."
        ],
        resolution_strategy="Quarterly alarm suppression audits.",
        entity_scope="OFE06 SCADA alarm systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ISA-18.2 Section 8"
    ),
    DoctrineBlock(
        topic="SCADA Asset Lifecycle Management",
        keywords=["SCADA", "asset lifecycle", "management", "OFE06"],
        conclusion_template="OFE06 SCADA assets must be managed throughout their lifecycle from procurement to decommissioning.",
        reasoning_framework=(
            "1. Track SCADA assets from procurement through deployment, operation, and decommissioning.\n"
            "2. Update asset inventory at each lifecycle stage.\n"
            "3. Review lifecycle management practices annually.\n"
            "4. Document all asset lifecycle events."
        ),
        key_factors=[
            "Lifecycle tracking",
            "Inventory updates",
            "Annual review",
            "Documentation"
        ],
        primary_authority=[
            "NIST SP 800-53 SA-12",
            "OFE06 Asset Management Policy"
        ],
        burden_holder="SCADA Asset Manager",
        adversary_position="Lifecycle management is unnecessary for small deployments.",
        counter_arguments=[
            "Lifecycle management ensures accountability and regulatory compliance.",
            "Improves asset utilization and planning."
        ],
        resolution_strategy="Annual lifecycle management audits.",
        entity_scope="OFE06 SCADA assets",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-53 SA-12"
    ),
    DoctrineBlock(
        topic="SCADA Configuration Drift Detection",
        keywords=["SCADA", "configuration drift", "detection", "OFE06"],
        conclusion_template="OFE06 SCADA must implement configuration drift detection to identify unauthorized changes.",
        reasoning_framework=(
            "1. Baseline all SCADA configurations and store securely.\n"
            "2. Monitor for changes and alert on unauthorized modifications.\n"
            "3. Review drift alerts and remediate promptly.\n"
            "4. Update baselines after approved changes."
        ),
        key_factors=[
            "Baseline accuracy",
            "Change monitoring",
            "Alert response",
            "Baseline updates"
        ],
        primary_authority=[
            "NIST SP 800-128",
            "OFE06 Configuration Management Policy"
        ],
        burden_holder="SCADA Configuration Manager",
        adversary_position="Drift detection is unnecessary with version control.",
        counter_arguments=[
            "Drift can occur outside version control (e.g., emergency changes).",
            "Automated detection improves security and compliance."
        ],
        resolution_strategy="Continuous drift monitoring and quarterly reviews.",
        entity_scope="OFE06 SCADA configurations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-128 Section 6"
    ),
    DoctrineBlock(
        topic="SCADA Service Level Agreement (SLA) Policy",
        keywords=["SCADA", "SLA", "service level agreement", "policy", "OFE06"],
        conclusion_template="All OFE06 SCADA service providers must adhere to SLAs for uptime, response, and resolution times.",
        reasoning_framework=(
            "1. Define SLAs for SCADA service providers (e.g., uptime, response, resolution times).\n"
            "2. Monitor service performance against SLAs.\n"
            "3. Review and update SLAs annually.\n"
            "4. Enforce penalties for SLA violations."
        ),
        key_factors=[
            "SLA definition",
            "Performance monitoring",
            "Annual review",
            "Enforcement"
        ],
        primary_authority=[
            "OFE06 SLA Policy"
        ],
        burden_holder="SCADA Service Manager",
        adversary_position="SLAs are unnecessary for trusted partners.",
        counter_arguments=[
            "SLAs ensure accountability and service quality.",
            "Penalties incentivize performance."
        ],
        resolution_strategy="Annual SLA reviews and enforcement.",
        entity_scope="OFE06 SCADA service providers",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="OFE06 SLA Policy Section 2"
    ),
    DoctrineBlock(
        topic="SCADA Documentation Standards",
        keywords=["SCADA", "documentation", "standards", "OFE06"],
        conclusion_template="All OFE06 SCADA systems must maintain up-to-date documentation per company standards.",
        reasoning_framework=(
            "1. Develop and enforce documentation standards for all SCADA systems.\n"
            "2. Update documentation after every significant change.\n"
            "3. Store documentation in a central, accessible repository.\n"
            "4. Review documentation for accuracy annually."
        ),
        key_factors=[
            "Standardization",
            "Update frequency",
            "Central storage",
            "Annual review"
        ],
        primary_authority=[
            "OFE06 Documentation Policy"
        ],
        burden_holder="SCADA Documentation Manager",
        adversary_position="Documentation is a low priority compared to operations.",
        counter_arguments=[
            "Accurate documentation reduces errors and speeds up troubleshooting.",
            "Regulatory audits require up-to-date documentation."
        ],
        resolution_strategy="Annual documentation audits.",
        entity_scope="OFE06 SCADA systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="OFE06 Documentation Policy Section 3"
    ),
    DoctrineBlock(
        topic="SCADA Training and Awareness",
        keywords=["SCADA", "training", "awareness", "OFE06"],
        conclusion_template="All OFE06 SCADA personnel must complete annual security and operational training.",
        reasoning_framework=(
            "1. Develop training curriculum for SCADA security and operations.\n"
            "2. Require annual completion for all personnel with SCADA access.\n"
            "3. Track training completion and remediate gaps.\n"
            "4. Update training content as threats and technologies evolve."
        ),
        key_factors=[
            "Curriculum development",
            "Completion tracking",
            "Annual updates",
            "Gap remediation"
        ],
        primary_authority=[
            "NIST SP 800-50",
            "OFE06 Training Policy"
        ],
        burden_holder="SCADA Training Coordinator",
        adversary_position="On-the-job training is sufficient.",
        counter_arguments=[
            "Formal training reduces human error and improves security.",
            "Regulatory frameworks require documented training."
        ],
        resolution_strategy="Annual training audits.",
        entity_scope="OFE06 SCADA personnel",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-50 Section 4"
    ),
    DoctrineBlock(
        topic="SCADA Regulatory Compliance",
        keywords=["SCADA", "regulatory compliance", "OFE06"],
        conclusion_template="OFE06 SCADA systems must comply with all applicable regulations (e.g., PHMSA, NERC CIP, API).",
        reasoning_framework=(
            "1. Identify all regulations applicable to OFE06 SCADA operations.\n"
            "2. Map regulatory requirements to SCADA controls and processes.\n"
            "3. Monitor for regulatory changes and update compliance measures.\n"
            "4. Conduct annual compliance audits."
        ),
        key_factors=[
            "Regulation identification",
            "Control mapping",
            "Change monitoring",
            "Audit frequency"
        ],
        primary_authority=[
            "PHMSA 49 CFR 195",
            "NERC CIP",
            "API RP 1165"
        ],
        burden_holder="SCADA Compliance Manager",
        adversary_position="Compliance is a one-time effort.",
        counter_arguments=[
            "Regulations change and require ongoing monitoring.",
            "Non-compliance can result in fines and operational shutdowns."
        ],
        resolution_strategy="Annual compliance audits and continuous monitoring.",
        entity_scope="OFE06 SCADA operations",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="PHMSA 49 CFR 195"
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
        if (
            keyword_lower in doctrine.topic.lower()
            or any(keyword_lower in kw.lower() for kw in doctrine.keywords)
            or keyword_lower in doctrine.reasoning_framework.lower()
            or keyword_lower in doctrine.conclusion_template.lower()
        ):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]