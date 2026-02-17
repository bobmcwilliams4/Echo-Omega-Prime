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
        topic="physical_security_threat",
        keywords=["access control", "intrusion", "facility", "perimeter", "surveillance"],
        conclusion_template="The likelihood and impact of a physical security breach at the facility is {assessment}, requiring {recommended_action}.",
        reasoning_framework="""
        1. Assess current access control mechanisms (e.g., card readers, biometric systems).
        2. Evaluate perimeter security, including fencing, lighting, and surveillance coverage.
        3. Review incident history for unauthorized entries or attempted breaches.
        4. Analyze response protocols and staff training adequacy.
        5. Consider local crime rates and threat intelligence.
        6. Synthesize findings to determine overall risk and recommend mitigation steps.
        """,
        key_factors=[
            "Access control system robustness",
            "Surveillance system coverage",
            "Incident response capability",
            "Local threat environment",
            "Staff security awareness"
        ],
        primary_authority=[
            "ASIS International Physical Asset Protection Standard",
            "ISO 27001 Annex A.11"
        ],
        burden_holder="Security Operations Manager",
        adversary_position="Physical intruders may exploit access control gaps or surveillance blind spots.",
        counter_arguments=[
            "Existing controls are sufficient given historical incident rates.",
            "Upgrades may not be cost-effective relative to risk."
        ],
        resolution_strategy="Conduct a physical security audit and implement prioritized improvements.",
        entity_scope="Corporate facilities and critical infrastructure",
        confidence=0.85,
        confidence_zone="High",
        controlling_precedent="ASIS Physical Security Guidelines (2020)"
    ),
    DoctrineBlock(
        topic="cybersecurity_threat_framework",
        keywords=["cybersecurity", "threat modeling", "risk assessment", "NIST", "framework"],
        conclusion_template="The organization's cybersecurity threat posture is {assessment}, with primary risks identified as {primary_risks}.",
        reasoning_framework="""
        1. Map organizational assets and data flows.
        2. Identify potential cyber threats using NIST SP 800-30 methodology.
        3. Evaluate existing controls against CIS Controls and NIST CSF.
        4. Prioritize risks based on likelihood and impact.
        5. Recommend mitigation strategies aligned with business objectives.
        """,
        key_factors=[
            "Asset inventory completeness",
            "Threat intelligence integration",
            "Control maturity",
            "Incident response readiness"
        ],
        primary_authority=[
            "NIST Cybersecurity Framework (CSF)",
            "CIS Critical Security Controls"
        ],
        burden_holder="Chief Information Security Officer",
        adversary_position="Advanced persistent threats may exploit unpatched vulnerabilities or misconfigurations.",
        counter_arguments=[
            "Resource constraints limit full framework implementation.",
            "Business operations may be disrupted by aggressive controls."
        ],
        resolution_strategy="Adopt a risk-based approach to framework implementation, focusing on critical assets.",
        entity_scope="Enterprise IT and OT environments",
        confidence=0.80,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-53 Rev. 5"
    ),
    DoctrineBlock(
        topic="financial_threat_detection",
        keywords=["fraud", "embezzlement", "money laundering", "financial controls", "audit"],
        conclusion_template="The risk of financial fraud within the organization is assessed as {assessment}, necessitating {recommended_action}.",
        reasoning_framework="""
        1. Review internal financial controls and segregation of duties.
        2. Analyze transaction monitoring systems for anomaly detection.
        3. Examine audit logs and reconciliation processes.
        4. Assess employee background checks and whistleblower policies.
        5. Synthesize findings to determine exposure and recommend enhancements.
        """,
        key_factors=[
            "Segregation of duties",
            "Transaction monitoring effectiveness",
            "Audit trail integrity",
            "Employee vetting"
        ],
        primary_authority=[
            "Sarbanes-Oxley Act (SOX)",
            "COSO Internal Control Framework"
        ],
        burden_holder="Chief Financial Officer",
        adversary_position="Insiders may collude to bypass controls or exploit process gaps.",
        counter_arguments=[
            "Existing controls have prevented past incidents.",
            "Additional controls may slow down business processes."
        ],
        resolution_strategy="Enhance monitoring and conduct regular independent audits.",
        entity_scope="Finance and accounting departments",
        confidence=0.78,
        confidence_zone="Medium",
        controlling_precedent="SOX Section 404"
    ),
    DoctrineBlock(
        topic="legal_threat_assessment",
        keywords=["compliance", "litigation", "regulatory", "sanctions", "legal risk"],
        conclusion_template="Legal exposure is determined to be {assessment}, with primary vulnerabilities in {vulnerable_areas}.",
        reasoning_framework="""
        1. Identify applicable laws and regulations (e.g., GDPR, FCPA).
        2. Assess compliance program maturity and documentation.
        3. Review history of regulatory inquiries or litigation.
        4. Analyze contractual obligations and indemnity clauses.
        5. Evaluate whistleblower and reporting mechanisms.
        """,
        key_factors=[
            "Regulatory environment complexity",
            "Compliance program effectiveness",
            "Litigation history",
            "Contractual risk allocation"
        ],
        primary_authority=[
            "General Data Protection Regulation (GDPR)",
            "Foreign Corrupt Practices Act (FCPA)"
        ],
        burden_holder="General Counsel",
        adversary_position="Regulators and litigants may exploit compliance gaps or ambiguous contracts.",
        counter_arguments=[
            "Current controls meet minimum legal requirements.",
            "Litigation risk is inherent and cannot be fully mitigated."
        ],
        resolution_strategy="Strengthen compliance training and contract review processes.",
        entity_scope="All business units",
        confidence=0.75,
        confidence_zone="Medium",
        controlling_precedent="GDPR Recital 39"
    ),
    DoctrineBlock(
        topic="reputation_threat_monitoring",
        keywords=["brand", "public relations", "media", "social media", "crisis communication"],
        conclusion_template="Reputational risk is currently {assessment}, with key drivers being {drivers}.",
        reasoning_framework="""
        1. Monitor media and social platforms for negative mentions.
        2. Assess crisis communication plans and spokesperson training.
        3. Analyze past incidents and response effectiveness.
        4. Evaluate stakeholder engagement and transparency.
        5. Recommend proactive measures to strengthen reputation.
        """,
        key_factors=[
            "Media monitoring coverage",
            "Crisis communication readiness",
            "Stakeholder trust",
            "Incident response speed"
        ],
        primary_authority=[
            "ISO 22361:2022 Crisis Management",
            "PRSA Code of Ethics"
        ],
        burden_holder="Chief Communications Officer",
        adversary_position="Competitors or activists may amplify negative events to damage reputation.",
        counter_arguments=[
            "Negative coverage is transient and has limited impact.",
            "Overreaction may draw more attention to minor incidents."
        ],
        resolution_strategy="Maintain active monitoring and regularly test crisis response plans.",
        entity_scope="Corporate communications and executive leadership",
        confidence=0.82,
        confidence_zone="High",
        controlling_precedent="ISO 22361:2022"
    ),
    DoctrineBlock(
        topic="insider_threat_detection",
        keywords=["insider", "employee", "malicious", "data theft", "privilege abuse"],
        conclusion_template="Insider threat risk is rated as {assessment}, with primary concerns in {concern_areas}.",
        reasoning_framework="""
        1. Identify users with privileged access to sensitive data.
        2. Monitor for anomalous behavior (e.g., large data transfers, off-hours access).
        3. Assess effectiveness of user activity monitoring and alerting.
        4. Review employee termination and access revocation procedures.
        5. Recommend enhancements to detection and deterrence mechanisms.
        """,
        key_factors=[
            "Privileged access management",
            "User behavior analytics",
            "Termination procedures",
            "Employee awareness training"
        ],
        primary_authority=[
            "CERT Insider Threat Center Guidelines",
            "NIST SP 800-53 AC-6"
        ],
        burden_holder="Information Security Manager",
        adversary_position="Disgruntled employees may exfiltrate data or sabotage systems.",
        counter_arguments=[
            "Strict monitoring may erode employee trust.",
            "Most employees are trustworthy and pose minimal risk."
        ],
        resolution_strategy="Implement least privilege and continuous monitoring.",
        entity_scope="All staff and contractors",
        confidence=0.77,
        confidence_zone="Medium",
        controlling_precedent="CERT Insider Threat Guide"
    ),
    DoctrineBlock(
        topic="supply_chain_threat_analysis",
        keywords=["third party", "vendor", "supplier", "supply chain", "resilience"],
        conclusion_template="Supply chain threat exposure is {assessment}, with critical dependencies identified as {dependencies}.",
        reasoning_framework="""
        1. Map supply chain and identify critical vendors.
        2. Assess vendor risk management and due diligence processes.
        3. Evaluate business continuity and disaster recovery plans.
        4. Review contract terms for risk allocation and SLAs.
        5. Recommend diversification or contingency planning as needed.
        """,
        key_factors=[
            "Vendor risk assessment frequency",
            "Contractual protections",
            "Supply chain visibility",
            "Business continuity planning"
        ],
        primary_authority=[
            "NIST SP 800-161",
            "ISO 28000:2022 Supply Chain Security"
        ],
        burden_holder="Procurement Director",
        adversary_position="Adversaries may compromise suppliers to reach the organization.",
        counter_arguments=[
            "Vendor risk is inherent and cannot be fully eliminated.",
            "Diversification may increase costs and complexity."
        ],
        resolution_strategy="Enhance due diligence and require robust vendor controls.",
        entity_scope="Procurement and supply chain management",
        confidence=0.74,
        confidence_zone="Medium",
        controlling_precedent="NIST SP 800-161"
    ),
    DoctrineBlock(
        topic="geopolitical_permian_basin_risk",
        keywords=["geopolitical", "Permian Basin", "oil", "energy", "regional instability"],
        conclusion_template="Geopolitical risk in the Permian Basin is assessed as {assessment}, with primary threats being {primary_threats}.",
        reasoning_framework="""
        1. Monitor regional political developments and regulatory changes.
        2. Assess impact of international sanctions or trade disputes.
        3. Evaluate security of critical infrastructure and logistics.
        4. Analyze local stakeholder relations and community sentiment.
        5. Recommend scenario planning for high-impact events.
        """,
        key_factors=[
            "Regulatory stability",
            "Infrastructure security",
            "Community relations",
            "International trade exposure"
        ],
        primary_authority=[
            "U.S. Department of Energy Reports",
            "EIA Country Analysis Briefs"
        ],
        burden_holder="Head of Risk Management",
        adversary_position="State or non-state actors may disrupt operations through regulatory or physical means.",
        counter_arguments=[
            "Regional stability has improved in recent years.",
            "Contingency plans are already in place."
        ],
        resolution_strategy="Maintain active intelligence and update contingency plans regularly.",
        entity_scope="Energy sector operations in the Permian Basin",
        confidence=0.70,
        confidence_zone="Medium",
        controlling_precedent="DOE Permian Basin Security Assessment (2021)"
    ),
    DoctrineBlock(
        topic="credential_compromise_threat",
        keywords=["credential", "password", "phishing", "account takeover", "authentication"],
        conclusion_template="Credential compromise risk is {assessment}, with main attack vectors being {attack_vectors}.",
        reasoning_framework="""
        1. Review authentication mechanisms and password policies.
        2. Assess prevalence of phishing and credential stuffing attempts.
        3. Evaluate multi-factor authentication (MFA) adoption.
        4. Monitor for leaked credentials on dark web sources.
        5. Recommend improvements to user awareness and technical controls.
        """,
        key_factors=[
            "Password policy strength",
            "MFA coverage",
            "Phishing simulation results",
            "Credential leak monitoring"
        ],
        primary_authority=[
            "NIST SP 800-63B",
            "OWASP Authentication Cheat Sheet"
        ],
        burden_holder="IT Security Lead",
        adversary_position="Attackers may use phishing or brute force to obtain credentials.",
        counter_arguments=[
            "MFA adoption is sufficient to mitigate most risks.",
            "User education is ongoing and effective."
        ],
        resolution_strategy="Expand MFA and enhance credential monitoring.",
        entity_scope="All users with system access",
        confidence=0.81,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-63B"
    ),
    DoctrineBlock(
        topic="ransomware_threat",
        keywords=["ransomware", "malware", "encryption", "extortion", "data recovery"],
        conclusion_template="Ransomware threat level is {assessment}, with vulnerabilities in {vulnerable_areas}.",
        reasoning_framework="""
        1. Assess endpoint protection and patch management practices.
        2. Review backup and recovery procedures for resilience.
        3. Analyze email filtering and user awareness training.
        4. Monitor for indicators of compromise and lateral movement.
        5. Recommend layered defense and incident response enhancements.
        """,
        key_factors=[
            "Endpoint protection effectiveness",
            "Backup frequency and isolation",
            "User training coverage",
            "Incident response plan maturity"
        ],
        primary_authority=[
            "CISA Ransomware Guide",
            "NIST SP 1800-25"
        ],
        burden_holder="Incident Response Team Lead",
        adversary_position="Ransomware operators may exploit unpatched systems or user errors.",
        counter_arguments=[
            "Backups are sufficient to recover from attacks.",
            "Ransomware is less likely due to industry sector."
        ],
        resolution_strategy="Harden defenses and test recovery procedures regularly.",
        entity_scope="All IT and OT systems",
        confidence=0.76,
        confidence_zone="Medium",
        controlling_precedent="CISA Ransomware Guide"
    ),
    DoctrineBlock(
        topic="social_engineering_threats",
        keywords=["social engineering", "phishing", "pretexting", "vishing", "impersonation"],
        conclusion_template="Social engineering risk is {assessment}, with primary exposure through {exposure_points}.",
        reasoning_framework="""
        1. Review frequency and results of phishing simulations.
        2. Assess user training and awareness program effectiveness.
        3. Analyze incident reports for social engineering attempts.
        4. Evaluate reporting and escalation mechanisms.
        5. Recommend targeted training and process improvements.
        """,
        key_factors=[
            "Phishing simulation click rates",
            "Employee training participation",
            "Incident reporting culture",
            "Process for verifying requests"
        ],
        primary_authority=[
            "SANS Security Awareness Program",
            "NIST SP 800-50"
        ],
        burden_holder="Security Awareness Officer",
        adversary_position="Attackers may exploit human error to gain unauthorized access.",
        counter_arguments=[
            "Technical controls mitigate most risks.",
            "User training fatigue may reduce effectiveness."
        ],
        resolution_strategy="Increase simulation frequency and tailor training to high-risk groups.",
        entity_scope="All employees and contractors",
        confidence=0.73,
        confidence_zone="Medium",
        controlling_precedent="SANS Social Engineering Whitepaper"
    ),
    DoctrineBlock(
        topic="environmental_compliance_threat",
        keywords=["environmental", "compliance", "EPA", "pollution", "regulatory"],
        conclusion_template="Environmental compliance risk is {assessment}, with main concerns in {concern_areas}.",
        reasoning_framework="""
        1. Identify applicable environmental regulations and permits.
        2. Assess monitoring and reporting processes.
        3. Review incident history and regulatory inspections.
        4. Evaluate training and awareness among operational staff.
        5. Recommend improvements to compliance management systems.
        """,
        key_factors=[
            "Regulatory coverage",
            "Monitoring and reporting accuracy",
            "Incident history",
            "Staff training"
        ],
        primary_authority=[
            "U.S. Environmental Protection Agency (EPA)",
            "ISO 14001:2015"
        ],
        burden_holder="Environmental Compliance Manager",
        adversary_position="Regulators may impose fines or sanctions for non-compliance.",
        counter_arguments=[
            "Compliance costs are high relative to risk.",
            "Current controls have passed recent inspections."
        ],
        resolution_strategy="Enhance monitoring and conduct regular self-audits.",
        entity_scope="Operations and facilities",
        confidence=0.79,
        confidence_zone="Medium",
        controlling_precedent="EPA Enforcement Actions"
    ),
    DoctrineBlock(
        topic="ddos_service_disruption",
        keywords=["DDoS", "service disruption", "availability", "network", "mitigation"],
        conclusion_template="DDoS threat level is {assessment}, with critical services at risk including {services}.",
        reasoning_framework="""
        1. Assess current DDoS mitigation capabilities (e.g., scrubbing, rate limiting).
        2. Review network architecture and redundancy.
        3. Analyze incident history and response times.
        4. Evaluate vendor SLAs for mitigation services.
        5. Recommend improvements to detection and response.
        """,
        key_factors=[
            "Mitigation service coverage",
            "Network redundancy",
            "Incident response speed",
            "Vendor SLA terms"
        ],
        primary_authority=[
            "NIST SP 800-61",
            "Cloud Security Alliance Guidance"
        ],
        burden_holder="Network Operations Center Lead",
        adversary_position="Attackers may disrupt critical services via volumetric or application-layer attacks.",
        counter_arguments=[
            "Current bandwidth is sufficient to absorb most attacks.",
            "DDoS is less likely due to industry profile."
        ],
        resolution_strategy="Enhance mitigation services and test incident response.",
        entity_scope="Public-facing and critical internal services",
        confidence=0.72,
        confidence_zone="Medium",
        controlling_precedent="NIST SP 800-61"
    ),
    DoctrineBlock(
        topic="intellectual_property_theft",
        keywords=["intellectual property", "trade secrets", "patents", "data exfiltration", "espionage"],
        conclusion_template="Intellectual property theft risk is {assessment}, with primary vulnerabilities in {vulnerable_areas}.",
        reasoning_framework="""
        1. Identify and classify intellectual property assets.
        2. Assess access controls and monitoring for sensitive data.
        3. Review employee and third-party agreements.
        4. Analyze incident history and current controls.
        5. Recommend enhancements to detection and legal protections.
        """,
        key_factors=[
            "Asset classification",
            "Access control strength",
            "Third-party agreements",
            "Incident history"
        ],
        primary_authority=[
            "WIPO IP Protection Guidelines",
            "Defend Trade Secrets Act (DTSA)"
        ],
        burden_holder="Legal and Information Security Teams",
        adversary_position="Insiders or competitors may seek to exfiltrate IP for competitive advantage.",
        counter_arguments=[
            "Legal remedies are sufficient deterrent.",
            "Technical controls are already robust."
        ],
        resolution_strategy="Strengthen monitoring and update legal agreements.",
        entity_scope="R&D, engineering, and legal departments",
        confidence=0.74,
        confidence_zone="Medium",
        controlling_precedent="DTSA (2016)"
    ),
    DoctrineBlock(
        topic="economic_downturn_market_risk",
        keywords=["economic", "market risk", "downturn", "recession", "financial planning"],
        conclusion_template="Market risk due to economic downturn is {assessment}, with key exposures in {exposures}.",
        reasoning_framework="""
        1. Monitor macroeconomic indicators and forecasts.
        2. Assess revenue diversification and customer concentration.
        3. Review financial reserves and cost structures.
        4. Analyze historical performance during downturns.
        5. Recommend scenario planning and cost optimization strategies.
        """,
        key_factors=[
            "Revenue diversification",
            "Financial reserves",
            "Customer concentration",
            "Cost structure flexibility"
        ],
        primary_authority=[
            "Federal Reserve Economic Data",
            "OECD Economic Outlook"
        ],
        burden_holder="Chief Financial Officer",
        adversary_position="Market volatility may reduce demand or disrupt supply chains.",
        counter_arguments=[
            "Industry is less sensitive to economic cycles.",
            "Reserves are sufficient to weather downturns."
        ],
        resolution_strategy="Conduct stress testing and update financial contingency plans.",
        entity_scope="Corporate finance and strategy",
        confidence=0.68,
        confidence_zone="Medium",
        controlling_precedent="OECD Economic Outlook"
    ),
    # Additional 25+ doctrine blocks for coverage, variety, and depth:
    DoctrineBlock(
        topic="cloud_security_threat",
        keywords=["cloud", "SaaS", "IaaS", "data breach", "shared responsibility"],
        conclusion_template="Cloud security risk is {assessment}, with main concerns in {concern_areas}.",
        reasoning_framework="""
        1. Review cloud provider security certifications and audit reports.
        2. Assess configuration management and access controls.
        3. Evaluate data encryption in transit and at rest.
        4. Analyze incident response integration with cloud providers.
        5. Recommend improvements to monitoring and contract terms.
        """,
        key_factors=[
            "Provider certifications",
            "Configuration management",
            "Data encryption",
            "Incident response integration"
        ],
        primary_authority=[
            "Cloud Security Alliance (CSA) CCM",
            "NIST SP 800-144"
        ],
        burden_holder="Cloud Security Architect",
        adversary_position="Attackers may exploit misconfigurations or weak provider controls.",
        counter_arguments=[
            "Provider controls are sufficient.",
            "On-premises risks are higher."
        ],
        resolution_strategy="Enhance configuration reviews and clarify provider responsibilities.",
        entity_scope="All cloud-hosted assets",
        confidence=0.77,
        confidence_zone="Medium",
        controlling_precedent="CSA Cloud Controls Matrix"
    ),
    DoctrineBlock(
        topic="third_party_risk_management",
        keywords=["third party", "vendor", "risk management", "outsourcing", "due diligence"],
        conclusion_template="Third-party risk is {assessment}, with critical vendors identified as {critical_vendors}.",
        reasoning_framework="""
        1. Maintain an inventory of all third-party relationships.
        2. Assess vendor risk through questionnaires and audits.
        3. Monitor for changes in vendor security posture.
        4. Review contract terms for liability and data protection.
        5. Recommend enhanced oversight for high-risk vendors.
        """,
        key_factors=[
            "Vendor inventory accuracy",
            "Risk assessment frequency",
            "Contractual protections",
            "Ongoing monitoring"
        ],
        primary_authority=[
            "ISO 27036",
            "NIST SP 800-171"
        ],
        burden_holder="Vendor Risk Manager",
        adversary_position="Vendors may introduce security or compliance risks.",
        counter_arguments=[
            "Vendor oversight is resource-intensive.",
            "Long-term partners are low risk."
        ],
        resolution_strategy="Prioritize oversight based on risk tiering.",
        entity_scope="All outsourced services",
        confidence=0.73,
        confidence_zone="Medium",
        controlling_precedent="ISO 27036"
    ),
    DoctrineBlock(
        topic="business_continuity_threat",
        keywords=["business continuity", "BCP", "disaster recovery", "resilience", "crisis"],
        conclusion_template="Business continuity risk is {assessment}, with main vulnerabilities in {vulnerabilities}.",
        reasoning_framework="""
        1. Review business continuity and disaster recovery plans.
        2. Assess plan testing frequency and results.
        3. Evaluate critical process and resource dependencies.
        4. Analyze past disruptions and recovery times.
        5. Recommend improvements to plan scope and testing.
        """,
        key_factors=[
            "Plan coverage",
            "Testing frequency",
            "Resource dependencies",
            "Recovery time objectives"
        ],
        primary_authority=[
            "ISO 22301:2019",
            "FEMA Continuity Guidance"
        ],
        burden_holder="Business Continuity Manager",
        adversary_position="Natural or man-made disasters may disrupt operations.",
        counter_arguments=[
            "Plans have proven effective in past incidents.",
            "Resource constraints limit testing."
        ],
        resolution_strategy="Increase testing and update plans for emerging threats.",
        entity_scope="All business units",
        confidence=0.80,
        confidence_zone="High",
        controlling_precedent="ISO 22301:2019"
    ),
    DoctrineBlock(
        topic="data_privacy_threat",
        keywords=["data privacy", "PII", "GDPR", "CCPA", "data protection"],
        conclusion_template="Data privacy risk is {assessment}, with main exposure in {exposure_areas}.",
        reasoning_framework="""
        1. Identify personal data processed and stored.
        2. Assess privacy policy and consent mechanisms.
        3. Evaluate data subject rights handling.
        4. Review data retention and deletion practices.
        5. Recommend improvements to privacy controls and transparency.
        """,
        key_factors=[
            "Personal data inventory",
            "Consent management",
            "Data subject rights process",
            "Retention policy"
        ],
        primary_authority=[
            "GDPR",
            "California Consumer Privacy Act (CCPA)"
        ],
        burden_holder="Data Protection Officer",
        adversary_position="Regulators or litigants may act on privacy violations.",
        counter_arguments=[
            "Data is anonymized where possible.",
            "User consent is always obtained."
        ],
        resolution_strategy="Enhance privacy impact assessments and user transparency.",
        entity_scope="All systems processing personal data",
        confidence=0.78,
        confidence_zone="Medium",
        controlling_precedent="GDPR Article 5"
    ),
    DoctrineBlock(
        topic="regulatory_change_threat",
        keywords=["regulation", "compliance", "law", "policy", "change management"],
        conclusion_template="Regulatory change risk is {assessment}, with main impact on {impacted_areas}.",
        reasoning_framework="""
        1. Monitor regulatory developments in relevant jurisdictions.
        2. Assess compliance program adaptability.
        3. Review history of regulatory changes and responses.
        4. Analyze resource allocation for compliance updates.
        5. Recommend proactive engagement with regulators.
        """,
        key_factors=[
            "Regulatory monitoring",
            "Compliance program flexibility",
            "Resource allocation",
            "Stakeholder engagement"
        ],
        primary_authority=[
            "LexisNexis Regulatory Change Management",
            "ISO 37301:2021"
        ],
        burden_holder="Compliance Officer",
        adversary_position="Rapid regulatory changes may outpace compliance updates.",
        counter_arguments=[
            "Change management processes are mature.",
            "Industry lobbying can influence outcomes."
        ],
        resolution_strategy="Increase regulatory horizon scanning and scenario planning.",
        entity_scope="All regulated operations",
        confidence=0.71,
        confidence_zone="Medium",
        controlling_precedent="ISO 37301:2021"
    ),
    DoctrineBlock(
        topic="mobile_device_threat",
        keywords=["mobile", "BYOD", "endpoint", "MDM", "app security"],
        conclusion_template="Mobile device risk is {assessment}, with main vulnerabilities in {vulnerabilities}.",
        reasoning_framework="""
        1. Assess mobile device management (MDM) coverage and policies.
        2. Review app vetting and patching processes.
        3. Evaluate network segmentation for mobile access.
        4. Analyze incident history involving mobile endpoints.
        5. Recommend improvements to controls and user awareness.
        """,
        key_factors=[
            "MDM coverage",
            "App vetting process",
            "Network segmentation",
            "User training"
        ],
        primary_authority=[
            "NIST SP 800-124",
            "OWASP Mobile Security Project"
        ],
        burden_holder="Endpoint Security Lead",
        adversary_position="Attackers may exploit unvetted apps or lost devices.",
        counter_arguments=[
            "MDM is fully deployed.",
            "Mobile access is limited to low-risk data."
        ],
        resolution_strategy="Increase app vetting and enforce device encryption.",
        entity_scope="All mobile device users",
        confidence=0.75,
        confidence_zone="Medium",
        controlling_precedent="NIST SP 800-124"
    ),
    DoctrineBlock(
        topic="iot_security_threat",
        keywords=["IoT", "internet of things", "device", "OT", "vulnerability"],
        conclusion_template="IoT security risk is {assessment}, with main exposure in {exposure_areas}.",
        reasoning_framework="""
        1. Inventory all IoT and OT devices.
        2. Assess device patching and lifecycle management.
        3. Evaluate network segmentation and monitoring.
        4. Review incident history involving IoT devices.
        5. Recommend improvements to procurement and decommissioning processes.
        """,
        key_factors=[
            "Device inventory accuracy",
            "Patch management",
            "Network segmentation",
            "Procurement controls"
        ],
        primary_authority=[
            "NIST SP 800-213",
            "ISA/IEC 62443"
        ],
        burden_holder="OT Security Manager",
        adversary_position="Attackers may exploit unpatched or poorly secured devices.",
        counter_arguments=[
            "IoT devices are isolated from critical systems.",
            "Device updates are managed centrally."
        ],
        resolution_strategy="Enhance segmentation and enforce device security baselines.",
        entity_scope="All IoT and OT environments",
        confidence=0.70,
        confidence_zone="Medium",
        controlling_precedent="NIST SP 800-213"
    ),
    DoctrineBlock(
        topic="malware_infection_threat",
        keywords=["malware", "virus", "trojan", "endpoint", "antivirus"],
        conclusion_template="Malware infection risk is {assessment}, with main vulnerabilities in {vulnerabilities}.",
        reasoning_framework="""
        1. Assess endpoint protection deployment and update status.
        2. Review user training on suspicious file handling.
        3. Evaluate incident detection and response capabilities.
        4. Analyze incident history for infection vectors.
        5. Recommend improvements to defense in depth.
        """,
        key_factors=[
            "Endpoint protection coverage",
            "User training",
            "Incident response speed",
            "Patch management"
        ],
        primary_authority=[
            "AV-TEST Institute Reports",
            "NIST SP 800-83"
        ],
        burden_holder="Endpoint Security Lead",
        adversary_position="Attackers may use malware to gain initial access or persistence.",
        counter_arguments=[
            "Antivirus solutions are best-in-class.",
            "User training is frequent and effective."
        ],
        resolution_strategy="Increase endpoint hardening and test incident response.",
        entity_scope="All endpoints",
        confidence=0.76,
        confidence_zone="Medium",
        controlling_precedent="NIST SP 800-83"
    ),
    DoctrineBlock(
        topic="data_exfiltration_threat",
        keywords=["data exfiltration", "DLP", "monitoring", "data loss", "insider"],
        conclusion_template="Data exfiltration risk is {assessment}, with main exposure in {exposure_areas}.",
        reasoning_framework="""
        1. Assess data loss prevention (DLP) coverage and policies.
        2. Review monitoring for large or unusual data transfers.
        3. Evaluate access controls for sensitive data.
        4. Analyze incident history for exfiltration attempts.
        5. Recommend improvements to DLP and user awareness.
        """,
        key_factors=[
            "DLP coverage",
            "Access controls",
            "Monitoring effectiveness",
            "Incident history"
        ],
        primary_authority=[
            "NIST SP 800-53 SC-7",
            "ISO 27002:2022"
        ],
        burden_holder="Data Security Officer",
        adversary_position="Insiders or attackers may exfiltrate sensitive data.",
        counter_arguments=[
            "DLP generates too many false positives.",
            "Access controls are sufficient."
        ],
        resolution_strategy="Tune DLP and enhance user training.",
        entity_scope="All data repositories",
        confidence=0.74,
        confidence_zone="Medium",
        controlling_precedent="NIST SP 800-53 SC-7"
    ),
    DoctrineBlock(
        topic="network_intrusion_threat",
        keywords=["network", "intrusion", "IDS", "IPS", "monitoring"],
        conclusion_template="Network intrusion risk is {assessment}, with main vulnerabilities in {vulnerabilities}.",
        reasoning_framework="""
        1. Assess deployment and tuning of IDS/IPS solutions.
        2. Review network segmentation and firewall rules.
        3. Analyze incident history for successful intrusions.
        4. Evaluate incident response integration.
        5. Recommend improvements to monitoring and segmentation.
        """,
        key_factors=[
            "IDS/IPS coverage",
            "Network segmentation",
            "Firewall rule management",
            "Incident response integration"
        ],
        primary_authority=[
            "NIST SP 800-94",
            "SANS Network Security Handbook"
        ],
        burden_holder="Network Security Lead",
        adversary_position="Attackers may bypass perimeter defenses or exploit lateral movement.",
        counter_arguments=[
            "IDS/IPS generate too many false positives.",
            "Segmentation is already robust."
        ],
        resolution_strategy="Tune detection rules and increase network visibility.",
        entity_scope="All network segments",
        confidence=0.75,
        confidence_zone="Medium",
        controlling_precedent="NIST SP 800-94"
    ),
    DoctrineBlock(
        topic="application_security_threat",
        keywords=["application", "web", "appsec", "OWASP", "vulnerability"],
        conclusion_template="Application security risk is {assessment}, with main vulnerabilities in {vulnerabilities}.",
        reasoning_framework="""
        1. Review secure development lifecycle (SDLC) practices.
        2. Assess vulnerability scanning and penetration testing frequency.
        3. Evaluate third-party library management.
        4. Analyze incident history for exploited vulnerabilities.
        5. Recommend improvements to code review and testing.
        """,
        key_factors=[
            "SDLC maturity",
            "Testing frequency",
            "Third-party library management",
            "Incident history"
        ],
        primary_authority=[
            "OWASP Top Ten",
            "NIST SP 800-64"
        ],
        burden_holder="Application Security Lead",
        adversary_position="Attackers may exploit web app vulnerabilities for unauthorized access.",
        counter_arguments=[
            "Testing is frequent and comprehensive.",
            "Legacy applications are low risk."
        ],
        resolution_strategy="Increase testing and update legacy applications.",
        entity_scope="All internally and externally developed applications",
        confidence=0.78,
        confidence_zone="Medium",
        controlling_precedent="OWASP Top Ten"
    ),
    DoctrineBlock(
        topic="email_security_threat",
        keywords=["email", "phishing", "spam", "malware", "gateway"],
        conclusion_template="Email security risk is {assessment}, with main exposure in {exposure_areas}.",
        reasoning_framework="""
        1. Assess email gateway filtering and sandboxing.
        2. Review user training on phishing and suspicious attachments.
        3. Evaluate incident response for email-borne threats.
        4. Analyze incident history for successful attacks.
        5. Recommend improvements to filtering and user awareness.
        """,
        key_factors=[
            "Gateway filtering effectiveness",
            "User training",
            "Incident response speed",
            "Incident history"
        ],
        primary_authority=[
            "NIST SP 800-45",
            "SANS Email Security Whitepaper"
        ],
        burden_holder="Email Security Lead",
        adversary_position="Attackers may use email as a primary entry vector.",
        counter_arguments=[
            "Gateway filtering is best-in-class.",
            "User training is frequent and effective."
        ],
        resolution_strategy="Enhance filtering and increase phishing simulations.",
        entity_scope="All email users",
        confidence=0.76,
        confidence_zone="Medium",
        controlling_precedent="NIST SP 800-45"
    ),
    DoctrineBlock(
        topic="privilege_escalation_threat",
        keywords=["privilege escalation", "admin", "access control", "least privilege", "RBAC"],
        conclusion_template="Privilege escalation risk is {assessment}, with main vulnerabilities in {vulnerabilities}.",
        reasoning_framework="""
        1. Assess access control policies and RBAC implementation.
        2. Review privileged account management and monitoring.
        3. Evaluate patch management for privilege escalation vulnerabilities.
        4. Analyze incident history for privilege misuse.
        5. Recommend improvements to access reviews and monitoring.
        """,
        key_factors=[
            "RBAC coverage",
            "Privileged account management",
            "Patch management",
            "Access review frequency"
        ],
        primary_authority=[
            "NIST SP 800-53 AC-6",
            "CIS Control 4"
        ],
        burden_holder="Access Control Manager",
        adversary_position="Attackers may exploit privilege escalation flaws to gain admin access.",
        counter_arguments=[
            "Least privilege is enforced.",
            "Patch management is mature."
        ],
        resolution_strategy="Increase access reviews and monitor privileged activity.",
        entity_scope="All privileged accounts",
        confidence=0.77,
        confidence_zone="Medium",
        controlling_precedent="NIST SP 800-53 AC-6"
    ),
    DoctrineBlock(
        topic="patch_management_threat",
        keywords=["patch management", "vulnerability", "update", "remediation", "endpoint"],
        conclusion_template="Patch management risk is {assessment}, with main vulnerabilities in {vulnerabilities}.",
        reasoning_framework="""
        1. Assess patch management process and coverage.
        2. Review patch deployment timelines and exceptions.
        3. Evaluate vulnerability scanning and reporting.
        4. Analyze incident history for unpatched exploits.
        5. Recommend improvements to automation and reporting.
        """,
        key_factors=[
            "Patch deployment speed",
            "Coverage",
            "Exception management",
            "Vulnerability scanning"
        ],
        primary_authority=[
            "NIST SP 800-40",
            "CIS Control 7"
        ],
        burden_holder="Patch Management Lead",
        adversary_position="Attackers may exploit unpatched vulnerabilities.",
        counter_arguments=[
            "Critical patches are prioritized.",
            "Legacy systems are out of scope."
        ],
        resolution_strategy="Automate patching and increase scanning frequency.",
        entity_scope="All endpoints and servers",
        confidence=0.78,
        confidence_zone="Medium",
        controlling_precedent="NIST SP 800-40"
    ),
    DoctrineBlock(
        topic="remote_work_threat",
        keywords=["remote work", "telework", "VPN", "endpoint", "access"],
        conclusion_template="Remote work risk is {assessment}, with main vulnerabilities in {vulnerabilities}.",
        reasoning_framework="""
        1. Assess VPN and remote access controls.
        2. Review endpoint security for remote devices.
        3. Evaluate user training on remote work risks.
        4. Analyze incident history for remote access breaches.
        5. Recommend improvements to controls and monitoring.
        """,
        key_factors=[
            "VPN security",
            "Endpoint protection",
            "User training",
            "Incident history"
        ],
        primary_authority=[
            "NIST SP 800-46",
            "CISA Telework Guidance"
        ],
        burden_holder="Remote Access Manager",
        adversary_position="Attackers may target remote workers with phishing or malware.",
        counter_arguments=[
            "VPN is mandatory for all remote access.",
            "Endpoints are centrally managed."
        ],
        resolution_strategy="Enhance endpoint monitoring and user training.",
        entity_scope="All remote workers",
        confidence=0.74,
        confidence_zone="Medium",
        controlling_precedent="NIST SP 800-46"
    ),
    DoctrineBlock(
        topic="phishing_attack_threat",
        keywords=["phishing", "email", "social engineering", "credential theft", "awareness"],
        conclusion_template="Phishing attack risk is {assessment}, with main exposure in {exposure_areas}.",
        reasoning_framework="""
        1. Assess email filtering and anti-phishing controls.
        2. Review user training and simulation results.
        3. Evaluate incident response for phishing incidents.
        4. Analyze incident history for successful attacks.
        5. Recommend improvements to controls and awareness.
        """,
        key_factors=[
            "Email filtering",
            "User training",
            "Incident response",
            "Simulation results"
        ],
        primary_authority=[
            "SANS Phishing Defense Guide",
            "NIST SP 800-177"
        ],
        burden_holder="Security Awareness Officer",
        adversary_position="Attackers may use phishing to steal credentials or deliver malware.",
        counter_arguments=[
            "Filtering is highly effective.",
            "User training is frequent."
        ],
        resolution_strategy="Increase simulation frequency and tailor training.",
        entity_scope="All email users",
        confidence=0.75,
        confidence_zone="Medium",
        controlling_precedent="NIST SP 800-177"
    ),
    DoctrineBlock(
        topic="insider_fraud_threat",
        keywords=["insider", "fraud", "embezzlement", "collusion", "monitoring"],
        conclusion_template="Insider fraud risk is {assessment}, with main vulnerabilities in {vulnerabilities}.",
        reasoning_framework="""
        1. Assess segregation of duties and monitoring controls.
        2. Review whistleblower and reporting mechanisms.
        3. Evaluate incident history for insider fraud.
        4. Analyze employee background checks and vetting.
        5. Recommend improvements to controls and culture.
        """,
        key_factors=[
            "Segregation of duties",
            "Monitoring controls",
            "Whistleblower mechanisms",
            "Employee vetting"
        ],
        primary_authority=[
            "COSO Internal Control Framework",
            "ACFE Report to the Nations"
        ],
        burden_holder="Internal Audit Lead",
        adversary_position="Insiders may collude to bypass controls.",
        counter_arguments=[
            "Controls have prevented past incidents.",
            "Fraud risk is low in current environment."
        ],
        resolution_strategy="Enhance monitoring and reinforce reporting culture.",
        entity_scope="Finance and operations",
        confidence=0.72,
        confidence_zone="Medium",
        controlling_precedent="ACFE Report to the Nations"
    ),
    DoctrineBlock(
        topic="critical_infrastructure_threat",
        keywords=["critical infrastructure", "CIP", "NERC", "resilience", "physical security"],
        conclusion_template="Critical infrastructure risk is {assessment}, with main vulnerabilities in {vulnerabilities}.",
        reasoning_framework="""
        1. Identify critical infrastructure assets and dependencies.
        2. Assess physical and cyber protection measures.
        3. Review incident history and response plans.
        4. Evaluate regulatory compliance with CIP standards.
        5. Recommend improvements to resilience and redundancy.
        """,
        key_factors=[
            "Asset identification",
            "Protection measures",
            "Incident response",
            "Regulatory compliance"
        ],
        primary_authority=[
            "NERC CIP Standards",
            "DHS Critical Infrastructure Guidance"
        ],
        burden_holder="Critical Infrastructure Protection Lead",
        adversary_position="Adversaries may target critical assets for maximum disruption.",
        counter_arguments=[
            "Redundancy is sufficient.",
            "Regulatory compliance is maintained."
        ],
        resolution_strategy="Increase testing and enhance redundancy.",
        entity_scope="Critical infrastructure assets",
        confidence=0.80,
        confidence_zone="High",
        controlling_precedent="NERC CIP Standards"
    ),
    DoctrineBlock(
        topic="regulatory_fines_threat",
        keywords=["regulatory", "fines", "sanctions", "compliance", "penalties"],
        conclusion_template="Regulatory fines risk is {assessment}, with main exposure in {exposure_areas}.",
        reasoning_framework="""
        1. Assess compliance with applicable laws and regulations.
        2. Review incident history for past fines or sanctions.
        3. Evaluate compliance monitoring and reporting processes.
        4. Analyze resource allocation for compliance activities.
        5. Recommend improvements to controls and reporting.
        """,
        key_factors=[
            "Compliance monitoring",
            "Incident history",
            "Reporting processes",
            "Resource allocation"
        ],
        primary_authority=[
            "GDPR",
            "FCPA"
        ],
        burden_holder="Compliance Officer",
        adversary_position="Regulators may impose fines for non-compliance.",
        counter_arguments=[
            "Controls are sufficient.",
            "Fines are rare in the industry."
        ],
        resolution_strategy="Increase monitoring and enhance reporting.",
        entity_scope="All regulated operations",
        confidence=0.73,
        confidence_zone="Medium",
        controlling_precedent="GDPR Article 83"
    ),
    DoctrineBlock(
        topic="data_integrity_threat",
        keywords=["data integrity", "tampering", "hashing", "audit", "logging"],
        conclusion_template="Data integrity risk is {assessment}, with main vulnerabilities in {vulnerabilities}.",
        reasoning_framework="""
        1. Assess controls for detecting and preventing data tampering.
        2. Review audit logging and monitoring.
        3. Evaluate incident history for integrity breaches.
        4. Analyze backup and recovery processes.
        5. Recommend improvements to controls and monitoring.
        """,
        key_factors=[
            "Tampering detection",
            "Audit logging",
            "Incident history",
            "Backup processes"
        ],
        primary_authority=[
            "NIST SP 800-92",
            "ISO 27001 A.12.4"
        ],
        burden_holder="Data Integrity Lead",
        adversary_position="Attackers may tamper with data to disrupt operations.",
        counter_arguments=[
            "Controls are sufficient.",
            "Incidents are rare."
        ],
        resolution_strategy="Enhance logging and increase monitoring.",
        entity_scope="All data repositories",
        confidence=0.76,
        confidence_zone="Medium",
        controlling_precedent="NIST SP 800-92"
    ),
    DoctrineBlock(
        topic="physical_asset_theft_threat",
        keywords=["physical asset", "theft", "inventory", "tracking", "security"],
        conclusion_template="Physical asset theft risk is {assessment}, with main vulnerabilities in {vulnerabilities}.",
        reasoning_framework="""
        1. Assess physical security controls for asset storage.
        2. Review asset inventory and tracking processes.
        3. Evaluate incident history for thefts.
        4. Analyze access control and monitoring.
        5. Recommend improvements to controls and tracking.
        """,
        key_factors=[
            "Physical security controls",
            "Inventory tracking",
            "Incident history",
            "Access control"
        ],
        primary_authority=[
            "ASIS Physical Asset Protection Standard",
            "ISO 27001 A.11"
        ],
        burden_holder="Asset Protection Lead",
        adversary_position="Thieves may exploit weak controls to steal assets.",
        counter_arguments=[
            "Controls are sufficient.",
            "Incidents are rare."
        ],
        resolution_strategy="Enhance controls and improve tracking.",
        entity_scope="All physical assets",
        confidence=0.78,
        confidence_zone="Medium",
        controlling_precedent="ASIS Physical Asset Protection Standard"
    ),
    DoctrineBlock(
        topic="contractual_risk_threat",
        keywords=["contract", "liability", "indemnity", "risk allocation", "legal"],
        conclusion_template="Contractual risk is {assessment}, with main exposure in {exposure_areas}.",
        reasoning_framework="""
        1. Review contract terms for liability and indemnity clauses.
        2. Assess risk allocation and dispute resolution mechanisms.
        3. Evaluate incident history for contractual disputes.
        4. Analyze contract management processes.
        5. Recommend improvements to review and negotiation.
        """,
        key_factors=[
            "Liability clauses",
            "Indemnity provisions",
            "Dispute resolution",
            "Contract management"
        ],
        primary_authority=[
            "Uniform Commercial Code (UCC)",
            "ISO 31000"
        ],
        burden_holder="Legal Counsel",
        adversary_position="Counterparties may exploit ambiguous terms.",
        counter_arguments=[
            "Contracts are reviewed by counsel.",
            "Disputes are rare."
        ],
        resolution_strategy="Enhance review and standardize terms.",
        entity_scope="All contracts",
        confidence=0.74,
        confidence_zone="Medium",
        controlling_precedent="UCC Article 2"
    ),
    DoctrineBlock(
        topic="brand_impersonation_threat",
        keywords=["brand", "impersonation", "phishing", "fraud", "domain"],
        conclusion_template="Brand impersonation risk is {assessment}, with main vulnerabilities in {vulnerabilities}.",
        reasoning_framework="""
        1. Monitor for unauthorized use of brand and domains.
        2. Assess takedown and enforcement processes.
        3. Evaluate incident history for impersonation.
        4. Analyze user awareness and reporting.
        5. Recommend improvements to monitoring and enforcement.
        """,
        key_factors=[
            "Brand monitoring",
            "Takedown processes",
            "Incident history",
            "User awareness"
        ],
        primary_authority=[
            "WIPO Brand Protection Guidelines",
            "ICANN Domain Dispute Policy"
        ],
        burden_holder="Brand Protection Lead",
        adversary_position="Attackers may impersonate the brand for fraud.",
        counter_arguments=[
            "Monitoring is comprehensive.",
            "Incidents are rare."
        ],
        resolution_strategy="Enhance monitoring and streamline takedowns.",
        entity_scope="All brand assets",
        confidence=0.75,
        confidence_zone="Medium",
        controlling_precedent="WIPO Brand Protection Guidelines"
    ),
    DoctrineBlock(
        topic="misconfiguration_threat",
        keywords=["misconfiguration", "cloud", "network", "security group", "firewall"],
        conclusion_template="Misconfiguration risk is {assessment}, with main vulnerabilities in {vulnerabilities}.",
        reasoning_framework="""
        1. Assess configuration management processes.
        2. Review automated scanning and alerting.
        3. Evaluate incident history for misconfiguration exploits.
        4. Analyze change management and approval workflows.
        5. Recommend improvements to automation and reviews.
        """,
        key_factors=[
            "Configuration management",
            "Automated scanning",
            "Change management",
            "Incident history"
        ],
        primary_authority=[
            "NIST SP 800-128",
            "CIS Control 5"
        ],
        burden_holder="Configuration Management Lead",
        adversary_position="Attackers may exploit misconfigurations for access.",
        counter_arguments=[
            "Automation reduces risk.",
            "Reviews are frequent."
        ],
        resolution_strategy="Increase automation and review frequency.",
        entity_scope="All systems",
        confidence=0.77,
        confidence_zone="Medium",
        controlling_precedent="NIST SP 800-128"
    ),
    DoctrineBlock(
        topic="third_party_data_breach_threat",
        keywords=["third party", "data breach", "vendor", "incident", "notification"],
        conclusion_template="Third-party data breach risk is {assessment}, with main exposure in {exposure_areas}.",
        reasoning_framework="""
        1. Assess vendor data protection controls.
        2. Review contract terms for breach notification.
        3. Evaluate incident history for third-party breaches.
        4. Analyze vendor monitoring and audits.
        5. Recommend improvements to oversight and contracts.
        """,
        key_factors=[
            "Vendor controls",
            "Breach notification terms",
            "Monitoring",
            "Incident history"
        ],
        primary_authority=[
            "ISO 27036",
            "NIST SP 800-171"
        ],
        burden_holder="Vendor Risk Manager",
        adversary_position="Vendors may be breached, exposing sensitive data.",
        counter_arguments=[
            "Vendors are audited regularly.",
            "Contracts are comprehensive."
        ],
        resolution_strategy="Enhance monitoring and update contracts.",
        entity_scope="All third-party relationships",
        confidence=0.74,
        confidence_zone="Medium",
        controlling_precedent="ISO 27036"
    ),
    DoctrineBlock(
        topic="spearphishing_threat",
        keywords=["spearphishing", "targeted attack", "email", "executive", "fraud"],
        conclusion_template="Spearphishing risk is {assessment}, with main exposure in {exposure_areas}.",
        reasoning_framework="""
        1. Monitor for targeted phishing attempts.
        2. Assess executive and high-value target training.
        3. Review incident history for successful attacks.
        4. Evaluate reporting and escalation processes.
        5. Recommend improvements to controls and awareness.
        """,
        key_factors=[
            "Targeted monitoring",
            "Executive training",
            "Incident history",
            "Reporting"
        ],
        primary_authority=[
            "SANS Spearphishing Whitepaper",
            "NIST SP 800-177"
        ],
        burden_holder="Security Awareness Officer",
        adversary_position="Attackers may target executives for high-value fraud.",
        counter_arguments=[
            "Executives are well-trained.",
            "Incidents are rare."
        ],
        resolution_strategy="Increase monitoring and tailor training.",
        entity_scope="Executives and high-value targets",
        confidence=0.76,
        confidence_zone="Medium",
        controlling_precedent="SANS Spearphishing Whitepaper"
    ),
    DoctrineBlock(
        topic="insider_sabotage_threat",
        keywords=["insider", "sabotage", "disgruntled employee", "critical systems", "monitoring"],
        conclusion_template="Insider sabotage risk is {assessment}, with main vulnerabilities in {vulnerabilities}.",
        reasoning_framework="""
        1. Assess monitoring for critical system changes.
        2. Review access controls for sensitive operations.
        3. Evaluate incident history for sabotage attempts.
        4. Analyze employee support and grievance processes.
        5. Recommend improvements to monitoring and support.
        """,
        key_factors=[
            "Critical system monitoring",
            "Access controls",
            "Incident history",
            "Employee support"
        ],
        primary_authority=[
            "CERT Insider Threat Guide",
            "NIST SP 800-53 AU-6"
        ],
        burden_holder="Operations Security Lead",
        adversary_position="Disgruntled insiders may sabotage systems.",
        counter_arguments=[
            "Support processes reduce risk.",
            "Monitoring is comprehensive."
        ],
        resolution_strategy="Enhance monitoring and employee support.",
        entity_scope="Critical systems",
        confidence=0.75,
        confidence_zone="Medium",
        controlling_precedent="CERT Insider Threat Guide"
    ),
    DoctrineBlock(
        topic="ransomware_extortion_threat",
        keywords=["ransomware", "extortion", "payment", "negotiation", "recovery"],
        conclusion_template="Ransomware extortion risk is {assessment}, with main vulnerabilities in {vulnerabilities}.",
        reasoning_framework="""
        1. Assess incident response and negotiation policies.
        2. Review backup and recovery capabilities.
        3. Evaluate legal and regulatory considerations for payment.
        4. Analyze incident history for extortion attempts.
        5. Recommend improvements to response and recovery.
        """,
        key_factors=[
            "Incident response",
            "Backup and recovery",
            "Legal considerations",
            "Incident history"
        ],
        primary_authority=[
            "CISA Ransomware Guide",
            "FBI Ransomware Guidance"
        ],
        burden_holder="Incident Response Lead",
        adversary_position="Attackers may demand payment for data decryption.",
        counter_arguments=[
            "Backups are sufficient.",
            "Payment is not permitted by policy."
        ],
        resolution_strategy="Enhance response and test recovery.",
        entity_scope="All systems",
        confidence=0.76,
        confidence_zone="Medium",
        controlling_precedent="CISA Ransomware Guide"
    ),
    DoctrineBlock(
        topic="regulatory_investigation_threat",
        keywords=["regulatory", "investigation", "audit", "compliance", "enforcement"],
        conclusion_template="Regulatory investigation risk is {assessment}, with main exposure in {exposure_areas}.",
        reasoning_framework="""
        1. Monitor for regulatory inquiries and audits.
        2. Assess compliance documentation and readiness.
        3. Review incident history for investigations.
        4. Evaluate legal support and response processes.
        5. Recommend improvements to readiness and engagement.
        """,
        key_factors=[
            "Monitoring",
            "Documentation",
            "Incident history",
            "Legal support"
        ],
        primary_authority=[
            "ISO 37301:2021",
            "LexisNexis Regulatory Guidance"
        ],
        burden_holder="Compliance Lead",
        adversary_position="Regulators may investigate for potential violations.",
        counter_arguments=[
            "Documentation is comprehensive.",
            "Engagement is proactive."
        ],
        resolution_strategy="Enhance readiness and maintain engagement.",
        entity_scope="All regulated operations",
        confidence=0.74,
        confidence_zone="Medium",
        controlling_precedent="ISO 37301:2021"
    ),
    DoctrineBlock(
        topic="external_fraud_threat",
        keywords=["external fraud", "scam", "payment fraud", "business email compromise", "fraud monitoring"],
        conclusion_template="External fraud risk is {assessment}, with main vulnerabilities in {vulnerabilities}.",
        reasoning_framework="""
        1. Assess fraud monitoring and detection systems.
        2. Review user training for fraud awareness.
        3. Evaluate incident history for fraud losses.
        4. Analyze payment and approval processes.
        5. Recommend improvements to controls and awareness.
        """,
        key_factors=[
            "Monitoring systems",
            "User training",
            "Incident history",
            "Payment processes"
        ],
        primary_authority=[
            "ACFE Fraud Prevention Guidance",
            "NIST SP 800-30"
        ],
        burden_holder="Fraud Risk Manager",
        adversary_position="External actors may attempt payment or business email compromise fraud.",
        counter_arguments=[
            "Controls are robust.",
            "Incidents are rare."
        ],
        resolution_strategy="Enhance monitoring and user training.",
        entity_scope="Finance and operations",
        confidence=0.73,
        confidence_zone="Medium",
        controlling_precedent="ACFE Fraud Prevention Guidance"
    ),
    DoctrineBlock(
        topic="data_retention_threat",
        keywords=["data retention", "deletion", "privacy", "compliance", "storage"],
        conclusion_template="Data retention risk is {assessment}, with main exposure in {exposure_areas}.",
        reasoning_framework="""
        1. Assess data retention and deletion policies.
        2. Review compliance with regulatory requirements.
        3. Evaluate incident history for retention violations.
        4. Analyze storage and backup processes.
        5. Recommend improvements to policy and enforcement.
        """,
        key_factors=[
            "Retention policies",
            "Regulatory compliance",
            "Incident history",
            "Storage processes"
        ],
        primary_authority=[
            "GDPR Article 5",
            "ISO 27001 A.8.3"
        ],
        burden_holder="Data Governance Lead",
        adversary_position="Excessive retention may violate privacy laws.",
        counter_arguments=[
            "Policies are sufficient.",
            "Incidents are rare."
        ],
        resolution_strategy="Enhance policy and automate enforcement.",
        entity_scope="All data repositories",
        confidence=0.75,
        confidence_zone="Medium",
        controlling_precedent="GDPR Article 5"
    ),
    DoctrineBlock(
        topic="regulatory_reporting_threat",
        keywords=["regulatory", "reporting", "compliance", "transparency", "enforcement"],
        conclusion_template="Regulatory reporting risk is {assessment}, with main exposure in {exposure_areas}.",
        reasoning_framework="""
        1. Assess reporting processes and controls.
        2. Review compliance with reporting requirements.
        3. Evaluate incident history for reporting violations.
        4. Analyze resource allocation for reporting.
        5. Recommend improvements to controls and automation.
        """,
        key_factors=[
            "Reporting processes",
            "Compliance",
            "Incident history",
            "Resource allocation"
        ],
        primary_authority=[
            "SEC Reporting Guidance",
            "ISO 37301:2021"
        ],
        burden_holder="Reporting Lead",
        adversary_position="Regulators may sanction for inaccurate or late reporting.",
        counter_arguments=[
            "Processes are robust.",
            "Incidents are rare."
        ],
        resolution_strategy="Enhance controls and automate reporting.",
        entity_scope="All regulated operations",
        confidence=0.74,
        confidence_zone="Medium",
        controlling_precedent="SEC Reporting Guidance"
    ),
    DoctrineBlock(
        topic="third_party_operational_threat",
        keywords=["third party", "operational risk", "outsourcing", "vendor", "resilience"],
        conclusion_template="Third-party operational risk is {assessment}, with main exposure in {exposure_areas}.",
        reasoning_framework="""
        1. Assess vendor operational resilience.
        2. Review incident history for vendor disruptions.
        3. Evaluate contract terms for operational risk allocation.
        4. Analyze monitoring and oversight processes.
        5. Recommend improvements to resilience and oversight.
        """,
        key_factors=[
            "Vendor resilience",
            "Incident history",
            "Contract terms",
            "Oversight"
        ],
        primary_authority=[
            "ISO 22301:2019",
            "NIST SP 800-161"
        ],
        burden_holder="Vendor Risk Manager",
        adversary_position="Vendors may disrupt operations through failures.",
        counter_arguments=[
            "Vendors are resilient.",
            "Oversight is comprehensive."
        ],
        resolution_strategy="Enhance resilience and increase oversight.",
        entity_scope="All outsourced operations",
        confidence=0.75,
        confidence_zone="Medium",
        controlling_precedent="ISO 22301:2019"
    ),
    DoctrineBlock(
        topic="data_classification_threat",
        keywords=["data classification", "sensitivity", "access control", "labeling", "policy"],
        conclusion_template="Data classification risk is {assessment}, with main vulnerabilities in {vulnerabilities}.",
        reasoning_framework="""
        1. Assess data classification policy and implementation.
        2. Review labeling and access control enforcement.
        3. Evaluate incident history for misclassification.
        4. Analyze user training and awareness.
        5. Recommend improvements to policy and enforcement.
        """,
        key_factors=[
            "Policy",
            "Labeling",
            "Access control",
            "User training"
        ],
        primary_authority=[
            "ISO 27001 A.8.2",
            "NIST SP 800-60"
        ],
        burden_holder="Data Governance Lead",
        adversary_position="Misclassification may expose sensitive data.",
        counter_arguments=[
            "Policy is robust.",
            "Incidents are rare."
        ],
        resolution_strategy="Enhance policy and automate enforcement.",
        entity_scope="All data repositories",
        confidence=0.76,
        confidence_zone="Medium",
        controlling_precedent="ISO 27001 A.8.2"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic == topic:
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