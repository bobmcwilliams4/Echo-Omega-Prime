from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

class ConfidenceZone(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    UNCERTAIN = "Uncertain"

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
        topic="STRIDE Threat Modeling: Spoofing",
        keywords=["STRIDE", "Threat Modeling", "Spoofing", "Authentication", "Identity"],
        conclusion_template="If authentication mechanisms are insufficient, spoofing threats are likely present.",
        reasoning_framework=(
            "STRIDE identifies spoofing as a threat where an attacker pretends to be someone else. "
            "Analysis involves reviewing authentication controls, credential management, and session handling. "
            "Evaluate the use of multi-factor authentication, password policies, and identity verification. "
            "Consider threat actors capable of credential theft or social engineering. "
            "Assess the risk based on the value of the asset and likelihood of attack. "
            "Review logs for anomalous login attempts and failed authentications. "
            "Map the authentication flow and identify points of weakness. "
            "Cross-reference with OWASP Top 10: Broken Authentication. "
            "Determine if adversaries can bypass authentication via technical or procedural flaws. "
            "Apply mitigations such as strong password hashing, account lockout, and MFA. "
            "Document the impact of successful spoofing on system integrity and confidentiality. "
            "Consider regulatory requirements for identity assurance. "
            "Evaluate the effectiveness of user education against phishing. "
            "Review historical incidents of spoofing in similar environments. "
            "Use risk assessment frameworks to prioritize remediation."
        ),
        key_factors=[
            "Strength of authentication mechanisms",
            "Credential management practices",
            "Session handling security",
            "User education",
            "Regulatory requirements"
        ],
        primary_authority=[
            "Microsoft STRIDE Model",
            "OWASP Top 10: Broken Authentication",
            "NIST SP 800-63"
        ],
        burden_holder="System Owner",
        adversary_position="Attacker seeks unauthorized access by impersonating legitimate users.",
        counter_arguments=[
            "Authentication controls are robust and regularly tested.",
            "No evidence of credential compromise.",
            "User awareness training reduces phishing risk."
        ],
        resolution_strategy="Enhance authentication controls, implement MFA, conduct regular audits.",
        entity_scope="User authentication subsystem",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NIST SP 800-63B"
    ),
    DoctrineBlock(
        topic="STRIDE Threat Modeling: Tampering",
        keywords=["STRIDE", "Threat Modeling", "Tampering", "Data Integrity", "Code Integrity"],
        conclusion_template="Tampering threats are mitigated if integrity controls are enforced throughout the system.",
        reasoning_framework=(
            "Tampering involves unauthorized modification of data or code. "
            "STRIDE recommends identifying all points where data or code can be altered. "
            "Review cryptographic controls such as hashing, digital signatures, and checksums. "
            "Assess the use of secure coding practices and code reviews. "
            "Evaluate the effectiveness of input validation and output encoding. "
            "Monitor for unauthorized changes via integrity monitoring tools. "
            "Consider insider threats and privilege escalation scenarios. "
            "Analyze the impact of tampering on system reliability and trust. "
            "Cross-reference with OWASP Top 10: Injection and DREAD Risk Assessment. "
            "Document controls for protecting data at rest and in transit. "
            "Review historical incidents of tampering in similar systems. "
            "Apply mitigations such as write protection, audit trails, and anomaly detection."
        ),
        key_factors=[
            "Integrity controls",
            "Cryptographic protections",
            "Secure coding practices",
            "Monitoring and auditing",
            "Privilege management"
        ],
        primary_authority=[
            "Microsoft STRIDE Model",
            "OWASP Top 10: Injection",
            "NIST SP 800-53"
        ],
        burden_holder="System Owner",
        adversary_position="Attacker modifies data or code to disrupt operations or gain advantage.",
        counter_arguments=[
            "Integrity controls are comprehensive and enforced.",
            "Audit logs show no unauthorized changes.",
            "Code reviews and testing reduce tampering risk."
        ],
        resolution_strategy="Implement integrity monitoring, enforce cryptographic protections, conduct regular audits.",
        entity_scope="Data and code storage and transmission",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NIST SP 800-53 SI-7"
    ),
    DoctrineBlock(
        topic="STRIDE Threat Modeling: Repudiation",
        keywords=["STRIDE", "Threat Modeling", "Repudiation", "Non-repudiation", "Audit"],
        conclusion_template="Repudiation threats are controlled if audit trails are comprehensive and tamper-proof.",
        reasoning_framework=(
            "Repudiation refers to the ability of users to deny their actions. "
            "STRIDE recommends implementing non-repudiation controls such as logging, digital signatures, and audit trails. "
            "Evaluate the completeness and integrity of logs. "
            "Assess the use of secure timestamping and log protection mechanisms. "
            "Review access controls for log files and audit data. "
            "Consider regulatory requirements for auditability. "
            "Analyze the impact of repudiation on accountability and forensic investigations. "
            "Cross-reference with DREAD Risk Assessment and SIEM Integration. "
            "Document procedures for log review and incident response. "
            "Apply mitigations such as centralized logging, immutable storage, and regular log analysis."
        ),
        key_factors=[
            "Audit trail completeness",
            "Log integrity",
            "Access controls",
            "Regulatory requirements",
            "Incident response procedures"
        ],
        primary_authority=[
            "Microsoft STRIDE Model",
            "NIST SP 800-92",
            "PCI DSS"
        ],
        burden_holder="System Owner",
        adversary_position="User denies actions to avoid accountability.",
        counter_arguments=[
            "Audit trails are comprehensive and protected.",
            "Digital signatures ensure non-repudiation.",
            "Regular log reviews detect anomalies."
        ],
        resolution_strategy="Enhance audit trail integrity, implement secure logging, enforce access controls.",
        entity_scope="User actions and system events",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NIST SP 800-92"
    ),
    DoctrineBlock(
        topic="STRIDE Threat Modeling: Information Disclosure",
        keywords=["STRIDE", "Threat Modeling", "Information Disclosure", "Confidentiality", "Data Leakage"],
        conclusion_template="Information disclosure threats are minimized if confidentiality controls are robust.",
        reasoning_framework=(
            "Information disclosure involves unauthorized access to sensitive data. "
            "STRIDE recommends identifying all data flows and storage locations. "
            "Evaluate encryption at rest and in transit. "
            "Assess access controls and data classification schemes. "
            "Review the effectiveness of input validation and output encoding. "
            "Monitor for data leakage via DLP tools and SIEM correlation. "
            "Consider external threats such as SSRF and XSS. "
            "Analyze the impact of disclosure on privacy and regulatory compliance. "
            "Cross-reference with OWASP Top 10: Sensitive Data Exposure. "
            "Document mitigations such as encryption, access control, and monitoring."
        ),
        key_factors=[
            "Encryption",
            "Access controls",
            "Data classification",
            "Monitoring",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Microsoft STRIDE Model",
            "OWASP Top 10: Sensitive Data Exposure",
            "GDPR"
        ],
        burden_holder="System Owner",
        adversary_position="Attacker seeks unauthorized access to sensitive data.",
        counter_arguments=[
            "Encryption is enforced throughout.",
            "Access controls are regularly reviewed.",
            "Monitoring detects unauthorized access."
        ],
        resolution_strategy="Strengthen confidentiality controls, enhance monitoring, conduct regular audits.",
        entity_scope="Sensitive data flows and storage",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GDPR Article 32"
    ),
    DoctrineBlock(
        topic="STRIDE Threat Modeling: Denial of Service",
        keywords=["STRIDE", "Threat Modeling", "Denial of Service", "Availability", "Resilience"],
        conclusion_template="Denial of Service threats are mitigated if availability controls and resilience strategies are implemented.",
        reasoning_framework=(
            "Denial of Service (DoS) involves attacks that disrupt system availability. "
            "STRIDE recommends identifying critical services and resources. "
            "Evaluate capacity planning, redundancy, and failover mechanisms. "
            "Assess the effectiveness of rate limiting, filtering, and anomaly detection. "
            "Monitor for unusual traffic patterns and resource exhaustion. "
            "Consider distributed denial of service (DDoS) scenarios. "
            "Analyze the impact of DoS on business continuity and service level agreements. "
            "Cross-reference with Intrusion Detection and SIEM Integration. "
            "Document mitigations such as load balancing, caching, and emergency response procedures."
        ),
        key_factors=[
            "Redundancy",
            "Capacity planning",
            "Rate limiting",
            "Anomaly detection",
            "Incident response"
        ],
        primary_authority=[
            "Microsoft STRIDE Model",
            "NIST SP 800-53",
            "OWASP Top 10: Availability"
        ],
        burden_holder="System Owner",
        adversary_position="Attacker disrupts system availability via resource exhaustion.",
        counter_arguments=[
            "Redundancy and failover are implemented.",
            "Anomaly detection identifies DoS attempts.",
            "Incident response procedures are established."
        ],
        resolution_strategy="Enhance availability controls, implement resilience strategies, conduct regular testing.",
        entity_scope="Critical services and resources",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NIST SP 800-53 CP-10"
    ),
    DoctrineBlock(
        topic="STRIDE Threat Modeling: Elevation of Privilege",
        keywords=["STRIDE", "Threat Modeling", "Elevation of Privilege", "Authorization", "Access Control"],
        conclusion_template="Elevation of privilege threats are mitigated if authorization controls are enforced and privilege boundaries are clear.",
        reasoning_framework=(
            "Elevation of privilege involves attackers gaining higher access than intended. "
            "STRIDE recommends reviewing authorization mechanisms and privilege boundaries. "
            "Evaluate role-based access control (RBAC), least privilege, and separation of duties. "
            "Assess the effectiveness of privilege escalation detection. "
            "Monitor for anomalous access patterns and privilege changes. "
            "Consider insider threats and misconfigurations. "
            "Analyze the impact of privilege escalation on system integrity and confidentiality. "
            "Cross-reference with DREAD Risk Assessment and OWASP Top 10: Access Control. "
            "Document mitigations such as privilege auditing, RBAC enforcement, and incident response."
        ),
        key_factors=[
            "Authorization controls",
            "Privilege boundaries",
            "RBAC",
            "Monitoring",
            "Incident response"
        ],
        primary_authority=[
            "Microsoft STRIDE Model",
            "OWASP Top 10: Broken Access Control",
            "NIST SP 800-53"
        ],
        burden_holder="System Owner",
        adversary_position="Attacker seeks unauthorized privilege escalation.",
        counter_arguments=[
            "Authorization controls are enforced.",
            "Privilege boundaries are clear.",
            "Monitoring detects privilege escalation."
        ],
        resolution_strategy="Enforce RBAC, conduct privilege audits, enhance monitoring.",
        entity_scope="Access control subsystem",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NIST SP 800-53 AC-6"
    ),
    DoctrineBlock(
        topic="PASTA Threat Modeling: Stage 1 - Definition of Objectives",
        keywords=["PASTA", "Threat Modeling", "Objectives", "Business Impact", "Risk"],
        conclusion_template="Threat modeling objectives are defined if business impact and risk tolerance are documented.",
        reasoning_framework=(
            "PASTA Stage 1 focuses on defining objectives for threat modeling. "
            "Identify business goals, critical assets, and acceptable risk levels. "
            "Document regulatory requirements and stakeholder expectations. "
            "Establish scope and boundaries for the threat model. "
            "Align objectives with organizational strategy and compliance mandates. "
            "Review historical incidents and lessons learned. "
            "Ensure objectives are measurable and actionable. "
            "Cross-reference with DREAD Risk Assessment and CVSS Scoring. "
            "Document objectives in a formal threat modeling charter."
        ),
        key_factors=[
            "Business impact",
            "Risk tolerance",
            "Regulatory requirements",
            "Stakeholder expectations",
            "Scope definition"
        ],
        primary_authority=[
            "PASTA Threat Modeling Methodology",
            "ISO/IEC 27001",
            "NIST SP 800-30"
        ],
        burden_holder="Risk Management Team",
        adversary_position="Threat actors seek to exploit gaps in objectives.",
        counter_arguments=[
            "Objectives are aligned with business strategy.",
            "Risk tolerance is documented.",
            "Regulatory requirements are considered."
        ],
        resolution_strategy="Document objectives, align with business goals, review regularly.",
        entity_scope="Threat modeling process",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO/IEC 27001 Clause 6"
    ),
    DoctrineBlock(
        topic="PASTA Threat Modeling: Stage 2 - Definition of Technical Scope",
        keywords=["PASTA", "Threat Modeling", "Technical Scope", "Architecture", "Assets"],
        conclusion_template="Technical scope is defined if architecture and assets are documented and mapped.",
        reasoning_framework=(
            "PASTA Stage 2 involves defining the technical scope of the threat model. "
            "Identify all system components, data flows, and interfaces. "
            "Document architecture diagrams and asset inventories. "
            "Map dependencies and external integrations. "
            "Assess the impact of technical scope on threat modeling accuracy. "
            "Review historical vulnerabilities and attack patterns. "
            "Ensure scope includes all critical assets and interfaces. "
            "Cross-reference with STRIDE and Attack Trees. "
            "Document scope in technical specifications and threat model artifacts."
        ),
        key_factors=[
            "Architecture documentation",
            "Asset inventory",
            "Dependency mapping",
            "Interface identification",
            "Historical vulnerabilities"
        ],
        primary_authority=[
            "PASTA Threat Modeling Methodology",
            "NIST SP 800-53",
            "OWASP Application Security Verification Standard"
        ],
        burden_holder="Security Architect",
        adversary_position="Threat actors exploit undocumented assets and interfaces.",
        counter_arguments=[
            "Technical scope is comprehensive.",
            "Assets and interfaces are documented.",
            "Historical vulnerabilities are reviewed."
        ],
        resolution_strategy="Document technical scope, review regularly, update as needed.",
        entity_scope="System architecture and assets",
        confidence=0.84,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OWASP ASVS Section 1"
    ),
    DoctrineBlock(
        topic="PASTA Threat Modeling: Stage 3 - Application Decomposition and Analysis",
        keywords=["PASTA", "Threat Modeling", "Application Decomposition", "Analysis", "Data Flow"],
        conclusion_template="Application decomposition is complete if all components and data flows are mapped and analyzed.",
        reasoning_framework=(
            "PASTA Stage 3 focuses on decomposing the application for threat analysis. "
            "Identify all components, data flows, and trust boundaries. "
            "Document interactions between components and external systems. "
            "Analyze data flow diagrams for potential vulnerabilities. "
            "Assess the impact of decomposition on threat identification. "
            "Review historical attack patterns and vulnerabilities. "
            "Ensure decomposition includes all critical assets and interfaces. "
            "Cross-reference with STRIDE and Attack Trees. "
            "Document decomposition in threat model artifacts."
        ),
        key_factors=[
            "Component identification",
            "Data flow mapping",
            "Trust boundary analysis",
            "Historical vulnerabilities",
            "External interactions"
        ],
        primary_authority=[
            "PASTA Threat Modeling Methodology",
            "OWASP Threat Modeling Cheat Sheet",
            "NIST SP 800-53"
        ],
        burden_holder="Security Analyst",
        adversary_position="Threat actors exploit gaps in decomposition.",
        counter_arguments=[
            "Decomposition is comprehensive.",
            "Data flows and trust boundaries are mapped.",
            "Historical vulnerabilities are reviewed."
        ],
        resolution_strategy="Document decomposition, review regularly, update as needed.",
        entity_scope="Application components and data flows",
        confidence=0.83,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OWASP Threat Modeling Cheat Sheet"
    ),
    DoctrineBlock(
        topic="PASTA Threat Modeling: Stage 4 - Threat Analysis",
        keywords=["PASTA", "Threat Modeling", "Threat Analysis", "Attack Patterns", "Vulnerabilities"],
        conclusion_template="Threat analysis is complete if attack patterns and vulnerabilities are identified and documented.",
        reasoning_framework=(
            "PASTA Stage 4 involves analyzing threats based on attack patterns and vulnerabilities. "
            "Identify potential threat actors and their motivations. "
            "Document attack patterns relevant to the application. "
            "Assess vulnerabilities in components and data flows. "
            "Evaluate the likelihood and impact of identified threats. "
            "Review historical incidents and lessons learned. "
            "Ensure threat analysis is comprehensive and actionable. "
            "Cross-reference with DREAD Risk Assessment and Attack Trees. "
            "Document analysis in threat model artifacts."
        ),
        key_factors=[
            "Threat actor identification",
            "Attack pattern documentation",
            "Vulnerability assessment",
            "Likelihood and impact evaluation",
            "Historical incidents"
        ],
        primary_authority=[
            "PASTA Threat Modeling Methodology",
            "MITRE ATT&CK",
            "OWASP Top 10"
        ],
        burden_holder="Threat Analyst",
        adversary_position="Threat actors exploit identified vulnerabilities.",
        counter_arguments=[
            "Threat analysis is comprehensive.",
            "Attack patterns and vulnerabilities are documented.",
            "Historical incidents are reviewed."
        ],
        resolution_strategy="Document threat analysis, review regularly, update as needed.",
        entity_scope="Application and system vulnerabilities",
        confidence=0.82,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="MITRE ATT&CK Framework"
    ),
    DoctrineBlock(
        topic="PASTA Threat Modeling: Stage 5 - Vulnerability and Weakness Analysis",
        keywords=["PASTA", "Threat Modeling", "Vulnerability Analysis", "Weakness", "Risk"],
        conclusion_template="Vulnerability analysis is complete if weaknesses are identified, documented, and prioritized.",
        reasoning_framework=(
            "PASTA Stage 5 focuses on analyzing vulnerabilities and weaknesses. "
            "Identify all potential weaknesses in components and data flows. "
            "Document vulnerabilities using standardized frameworks such as CVSS. "
            "Assess the impact and likelihood of exploitation. "
            "Prioritize vulnerabilities based on risk and business impact. "
            "Review historical incidents and lessons learned. "
            "Ensure analysis is comprehensive and actionable. "
            "Cross-reference with DREAD Risk Assessment and OWASP Top 10. "
            "Document analysis in vulnerability management artifacts."
        ),
        key_factors=[
            "Weakness identification",
            "Vulnerability documentation",
            "Risk prioritization",
            "Business impact assessment",
            "Historical incidents"
        ],
        primary_authority=[
            "PASTA Threat Modeling Methodology",
            "CVSS",
            "OWASP Top 10"
        ],
        burden_holder="Vulnerability Analyst",
        adversary_position="Threat actors exploit prioritized weaknesses.",
        counter_arguments=[
            "Vulnerability analysis is comprehensive.",
            "Weaknesses are documented and prioritized.",
            "Historical incidents are reviewed."
        ],
        resolution_strategy="Document vulnerability analysis, prioritize remediation, review regularly.",
        entity_scope="Application and system vulnerabilities",
        confidence=0.81,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CVSS v3.1"
    ),
    DoctrineBlock(
        topic="PASTA Threat Modeling: Stage 6 - Attack Modeling",
        keywords=["PASTA", "Threat Modeling", "Attack Modeling", "Attack Trees", "Scenario Analysis"],
        conclusion_template="Attack modeling is complete if attack trees and scenarios are documented and analyzed.",
        reasoning_framework=(
            "PASTA Stage 6 involves modeling attacks using attack trees and scenarios. "
            "Document attack trees for critical assets and components. "
            "Analyze attack scenarios for likelihood and impact. "
            "Assess the effectiveness of existing controls against modeled attacks. "
            "Review historical incidents and lessons learned. "
            "Ensure attack modeling is comprehensive and actionable. "
            "Cross-reference with STRIDE and DREAD Risk Assessment. "
            "Document modeling in threat model artifacts."
        ),
        key_factors=[
            "Attack tree documentation",
            "Scenario analysis",
            "Control effectiveness assessment",
            "Historical incidents",
            "Critical asset identification"
        ],
        primary_authority=[
            "PASTA Threat Modeling Methodology",
            "Bruce Schneier: Attack Trees",
            "OWASP Threat Modeling Cheat Sheet"
        ],
        burden_holder="Attack Modeler",
        adversary_position="Threat actors exploit modeled attack scenarios.",
        counter_arguments=[
            "Attack modeling is comprehensive.",
            "Attack trees and scenarios are documented.",
            "Historical incidents are reviewed."
        ],
        resolution_strategy="Document attack modeling, review regularly, update as needed.",
        entity_scope="Critical assets and attack scenarios",
        confidence=0.80,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Bruce Schneier: Attack Trees"
    ),
    DoctrineBlock(
        topic="PASTA Threat Modeling: Stage 7 - Risk Analysis and Mitigation",
        keywords=["PASTA", "Threat Modeling", "Risk Analysis", "Mitigation", "Remediation"],
        conclusion_template="Risk analysis and mitigation are complete if risks are documented, prioritized, and mitigations are implemented.",
        reasoning_framework=(
            "PASTA Stage 7 focuses on analyzing risks and implementing mitigations. "
            "Document risks based on threat and vulnerability analysis. "
            "Prioritize risks based on business impact and likelihood. "
            "Identify and implement mitigations for high-priority risks. "
            "Review effectiveness of mitigations and residual risk. "
            "Ensure risk analysis and mitigation are comprehensive and actionable. "
            "Cross-reference with DREAD Risk Assessment and CVSS Scoring. "
            "Document analysis and mitigation in risk management artifacts."
        ),
        key_factors=[
            "Risk documentation",
            "Risk prioritization",
            "Mitigation identification",
            "Effectiveness review",
            "Residual risk assessment"
        ],
        primary_authority=[
            "PASTA Threat Modeling Methodology",
            "ISO/IEC 27005",
            "NIST SP 800-30"
        ],
        burden_holder="Risk Manager",
        adversary_position="Threat actors exploit unmitigated risks.",
        counter_arguments=[
            "Risk analysis is comprehensive.",
            "Risks are prioritized and mitigated.",
            "Residual risk is assessed."
        ],
        resolution_strategy="Document risk analysis, implement mitigations, review regularly.",
        entity_scope="Application and system risks",
        confidence=0.79,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO/IEC 27005"
    ),
    DoctrineBlock(
        topic="DREAD Risk Assessment: Damage Potential",
        keywords=["DREAD", "Risk Assessment", "Damage Potential", "Impact", "Business Continuity"],
        conclusion_template="Damage potential is high if exploitation leads to significant business impact.",
        reasoning_framework=(
            "DREAD assesses damage potential by evaluating the impact of exploitation. "
            "Document potential consequences for business continuity, financial loss, and reputation. "
            "Assess the impact on critical assets and services. "
            "Review historical incidents and lessons learned. "
            "Prioritize vulnerabilities with high damage potential. "
            "Cross-reference with CVSS Impact Metrics and PASTA Risk Analysis. "
            "Document damage potential in risk assessment artifacts."
        ),
        key_factors=[
            "Business impact",
            "Financial loss",
            "Reputation damage",
            "Critical asset impact",
            "Historical incidents"
        ],
        primary_authority=[
            "DREAD Risk Assessment Model",
            "CVSS Impact Metrics",
            "ISO/IEC 27005"
        ],
        burden_holder="Risk Analyst",
        adversary_position="Threat actors exploit vulnerabilities with high damage potential.",
        counter_arguments=[
            "Damage potential is assessed and documented.",
            "Critical assets are protected.",
            "Historical incidents are reviewed."
        ],
        resolution_strategy="Prioritize high-damage vulnerabilities, implement mitigations, review regularly.",
        entity_scope="Critical assets and vulnerabilities",
        confidence=0.78,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CVSS v3.1 Impact Metrics"
    ),
    DoctrineBlock(
        topic="DREAD Risk Assessment: Reproducibility",
        keywords=["DREAD", "Risk Assessment", "Reproducibility", "Attack Feasibility", "Exploitability"],
        conclusion_template="Reproducibility is high if attacks can be easily repeated by adversaries.",
        reasoning_framework=(
            "DREAD assesses reproducibility by evaluating the feasibility of repeated attacks. "
            "Document attack methods and tools used by adversaries. "
            "Assess the ease of exploitation and availability of public exploits. "
            "Review historical incidents and lessons learned. "
            "Prioritize vulnerabilities with high reproducibility. "
            "Cross-reference with CVSS Exploitability Metrics and PASTA Threat Analysis. "
            "Document reproducibility in risk assessment artifacts."
        ),
        key_factors=[
            "Attack method documentation",
            "Tool availability",
            "Exploit feasibility",
            "Historical incidents",
            "Public exploit availability"
        ],
        primary_authority=[
            "DREAD Risk Assessment Model",
            "CVSS Exploitability Metrics",
            "MITRE ATT&CK"
        ],
        burden_holder="Risk Analyst",
        adversary_position="Threat actors exploit vulnerabilities with high reproducibility.",
        counter_arguments=[
            "Reproducibility is assessed and documented.",
            "Exploit feasibility is reviewed.",
            "Historical incidents are analyzed."
        ],
        resolution_strategy="Prioritize high-reproducibility vulnerabilities, implement mitigations, review regularly.",
        entity_scope="Vulnerabilities and attack methods",
        confidence=0.77,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CVSS v3.1 Exploitability Metrics"
    ),
    DoctrineBlock(
        topic="DREAD Risk Assessment: Exploitability",
        keywords=["DREAD", "Risk Assessment", "Exploitability", "Attack Complexity", "Vulnerability"],
        conclusion_template="Exploitability is high if vulnerabilities can be exploited with minimal effort.",
        reasoning_framework=(
            "DREAD assesses exploitability by evaluating the complexity and effort required to exploit vulnerabilities. "
            "Document attack vectors and required conditions. "
            "Assess the skill level and resources needed by adversaries. "
            "Review historical incidents and lessons learned. "
            "Prioritize vulnerabilities with high exploitability. "
            "Cross-reference with CVSS Attack Complexity and PASTA Vulnerability Analysis. "
            "Document exploitability in risk assessment artifacts."
        ),
        key_factors=[
            "Attack vector documentation",
            "Required conditions",
            "Skill level assessment",
            "Historical incidents",
            "Resource requirements"
        ],
        primary_authority=[
            "DREAD Risk Assessment Model",
            "CVSS Attack Complexity",
            "MITRE ATT&CK"
        ],
        burden_holder="Risk Analyst",
        adversary_position="Threat actors exploit vulnerabilities with high exploitability.",
        counter_arguments=[
            "Exploitability is assessed and documented.",
            "Attack complexity is reviewed.",
            "Historical incidents are analyzed."
        ],
        resolution_strategy="Prioritize high-exploitability vulnerabilities, implement mitigations, review regularly.",
        entity_scope="Vulnerabilities and attack vectors",
        confidence=0.76,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CVSS v3.1 Attack Complexity"
    ),
    DoctrineBlock(
        topic="DREAD Risk Assessment: Affected Users",
        keywords=["DREAD", "Risk Assessment", "Affected Users", "User Impact", "Exposure"],
        conclusion_template="User impact is high if a large number of users are affected by exploitation.",
        reasoning_framework=(
            "DREAD assesses affected users by evaluating the scope of impact. "
            "Document user populations and exposure levels. "
            "Assess the impact on user privacy, security, and experience. "
            "Review historical incidents and lessons learned. "
            "Prioritize vulnerabilities affecting large user populations. "
            "Cross-reference with CVSS Scope and PASTA Risk Analysis. "
            "Document affected users in risk assessment artifacts."
        ),
        key_factors=[
            "User population documentation",
            "Exposure assessment",
            "Privacy impact",
            "Security impact",
            "Historical incidents"
        ],
        primary_authority=[
            "DREAD Risk Assessment Model",
            "CVSS Scope",
            "GDPR"
        ],
        burden_holder="Risk Analyst",
        adversary_position="Threat actors exploit vulnerabilities affecting many users.",
        counter_arguments=[
            "User impact is assessed and documented.",
            "Exposure levels are reviewed.",
            "Historical incidents are analyzed."
        ],
        resolution_strategy="Prioritize vulnerabilities affecting many users, implement mitigations, review regularly.",
        entity_scope="User populations and vulnerabilities",
        confidence=0.75,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CVSS v3.1 Scope"
    ),
    DoctrineBlock(
        topic="DREAD Risk Assessment: Discoverability",
        keywords=["DREAD", "Risk Assessment", "Discoverability", "Vulnerability Exposure", "Attack Surface"],
        conclusion_template="Discoverability is high if vulnerabilities are easily found by adversaries.",
        reasoning_framework=(
            "DREAD assesses discoverability by evaluating how easily vulnerabilities can be found. "
            "Document exposure of assets and attack surface. "
            "Assess the use of automated tools and public information. "
            "Review historical incidents and lessons learned. "
            "Prioritize vulnerabilities with high discoverability. "
            "Cross-reference with CVSS Attack Vector and PASTA Threat Analysis. "
            "Document discoverability in risk assessment artifacts."
        ),
        key_factors=[
            "Asset exposure",
            "Attack surface documentation",
            "Automated tool use",
            "Public information availability",
            "Historical incidents"
        ],
        primary_authority=[
            "DREAD Risk Assessment Model",
            "CVSS Attack Vector",
            "OWASP Top 10"
        ],
        burden_holder="Risk Analyst",
        adversary_position="Threat actors exploit easily discoverable vulnerabilities.",
        counter_arguments=[
            "Discoverability is assessed and documented.",
            "Attack surface is minimized.",
            "Historical incidents are analyzed."
        ],
        resolution_strategy="Prioritize high-discoverability vulnerabilities, implement mitigations, review regularly.",
        entity_scope="Assets and vulnerabilities",
        confidence=0.74,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CVSS v3.1 Attack Vector"
    ),
    DoctrineBlock(
        topic="Attack Trees for Threat Analysis: Root Node Identification",
        keywords=["Attack Trees", "Threat Analysis", "Root Node", "Critical Asset", "Scenario"],
        conclusion_template="Root node is identified if critical asset or scenario is documented as the starting point.",
        reasoning_framework=(
            "Attack trees begin with the identification of the root node, representing the critical asset or scenario. "
            "Document the asset or scenario at risk. "
            "Assess the impact of compromise on business continuity and security. "
            "Review historical incidents and lessons learned. "
            "Ensure root node identification is comprehensive and actionable. "
            "Cross-reference with PASTA Attack Modeling and STRIDE Threat Modeling. "
            "Document root node in attack tree artifacts."
        ),
        key_factors=[
            "Critical asset documentation",
            "Scenario identification",
            "Business impact assessment",
            "Historical incidents",
            "Threat modeling integration"
        ],
        primary_authority=[
            "Bruce Schneier: Attack Trees",
            "PASTA Threat Modeling Methodology",
            "NIST SP 800-30"
        ],
        burden_holder="Attack Modeler",
        adversary_position="Threat actors target critical assets or scenarios.",
        counter_arguments=[
            "Root node is identified and documented.",
            "Business impact is assessed.",
            "Historical incidents are reviewed."
        ],
        resolution_strategy="Document root node, review regularly, update as needed.",
        entity_scope="Critical assets and scenarios",
        confidence=0.73,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Bruce Schneier: Attack Trees"
    ),
    DoctrineBlock(
        topic="Attack Trees for Threat Analysis: Branch Node Analysis",
        keywords=["Attack Trees", "Threat Analysis", "Branch Node", "Attack Path", "Vulnerability"],
        conclusion_template="Branch node analysis is complete if attack paths and vulnerabilities are documented and mapped.",
        reasoning_framework=(
            "Attack trees use branch nodes to represent attack paths and vulnerabilities. "
            "Document all possible attack paths from the root node. "
            "Assess vulnerabilities and conditions required for each path. "
            "Review historical incidents and lessons learned. "
            "Ensure branch node analysis is comprehensive and actionable. "
            "Cross-reference with PASTA Vulnerability Analysis and DREAD Risk Assessment. "
            "Document branch node analysis in attack tree artifacts."
        ),
        key_factors=[
            "Attack path documentation",
            "Vulnerability assessment",
            "Condition identification",
            "Historical incidents",
            "Threat modeling integration"
        ],
        primary_authority=[
            "Bruce Schneier: Attack Trees",
            "PASTA Threat Modeling Methodology",
            "CVSS"
        ],
        burden_holder="Attack Modeler",
        adversary_position="Threat actors exploit attack paths and vulnerabilities.",
        counter_arguments=[
            "Branch node analysis is comprehensive.",
            "Attack paths and vulnerabilities are documented.",
            "Historical incidents are reviewed."
        ],
        resolution_strategy="Document branch node analysis, review regularly, update as needed.",
        entity_scope="Attack paths and vulnerabilities",
        confidence=0.72,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Bruce Schneier: Attack Trees"
    ),
    DoctrineBlock(
        topic="Attack Trees for Threat Analysis: Leaf Node Analysis",
        keywords=["Attack Trees", "Threat Analysis", "Leaf Node", "Attack Outcome", "Mitigation"],
        conclusion_template="Leaf node analysis is complete if attack outcomes and mitigations are documented.",
        reasoning_framework=(
            "Attack trees use leaf nodes to represent attack outcomes and mitigations. "
            "Document the outcome of each attack path. "
            "Assess the effectiveness of mitigations for each outcome. "
            "Review historical incidents and lessons learned. "
            "Ensure leaf node analysis is comprehensive and actionable. "
            "Cross-reference with PASTA Risk Analysis and DREAD Risk Assessment. "
            "Document leaf node analysis in attack tree artifacts."
        ),
        key_factors=[
            "Attack outcome documentation",
            "Mitigation assessment",
            "Historical incidents",
            "Threat modeling integration",
            "Residual risk evaluation"
        ],
        primary_authority=[
            "Bruce Schneier: Attack Trees",
            "PASTA Threat Modeling Methodology",
            "ISO/IEC 27005"
        ],
        burden_holder="Attack Modeler",
        adversary_position="Threat actors exploit attack outcomes and mitigations.",
        counter_arguments=[
            "Leaf node analysis is comprehensive.",
            "Attack outcomes and mitigations are documented.",
            "Historical incidents are reviewed."
        ],
        resolution_strategy="Document leaf node analysis, implement mitigations, review regularly.",
        entity_scope="Attack outcomes and mitigations",
        confidence=0.71,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO/IEC 27005"
    ),
    DoctrineBlock(
        topic="OWASP Top 10: Injection",
        keywords=["OWASP Top 10", "Injection", "SQL Injection", "Command Injection", "Input Validation"],
        conclusion_template="Injection threats are mitigated if input validation and parameterization are enforced.",
        reasoning_framework=(
            "Injection vulnerabilities occur when untrusted data is sent to an interpreter as part of a command or query. "
            "OWASP recommends input validation, parameterized queries, and escaping user input. "
            "Assess the use of ORM frameworks and prepared statements. "
            "Review historical incidents of injection attacks. "
            "Monitor for anomalous query patterns and failed input validation. "
            "Cross-reference with STRIDE Tampering and DREAD Exploitability. "
            "Document mitigations such as input validation, parameterization, and least privilege."
        ),
        key_factors=[
            "Input validation",
            "Parameterized queries",
            "Escaping user input",
            "ORM framework usage",
            "Historical incidents"
        ],
        primary_authority=[
            "OWASP Top 10",
            "NIST SP 800-53",
            "PCI DSS"
        ],
        burden_holder="Application Developer",
        adversary_position="Attacker exploits injection vulnerabilities to execute arbitrary commands.",
        counter_arguments=[
            "Input validation and parameterization are enforced.",
            "ORM frameworks reduce injection risk.",
            "Historical incidents are reviewed."
        ],
        resolution_strategy="Implement input validation, enforce parameterization, review regularly.",
        entity_scope="Application input and queries",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OWASP Top 10 Injection"
    ),
    DoctrineBlock(
        topic="OWASP Top 10: Cross-Site Scripting (XSS)",
        keywords=["OWASP Top 10", "XSS", "Cross-Site Scripting", "Output Encoding", "Input Validation"],
        conclusion_template="XSS threats are mitigated if output encoding and input validation are enforced.",
        reasoning_framework=(
            "Cross-Site Scripting (XSS) occurs when attackers inject malicious scripts into web applications. "
            "OWASP recommends output encoding, input validation, and use of CSP headers. "
            "Assess the use of secure frameworks and libraries. "
            "Review historical incidents of XSS attacks. "
            "Monitor for anomalous script execution and failed input validation. "
            "Cross-reference with STRIDE Information Disclosure and DREAD Exploitability. "
            "Document mitigations such as output encoding, input validation, and CSP enforcement."
        ),
        key_factors=[
            "Output encoding",
            "Input validation",
            "CSP enforcement",
            "Secure framework usage",
            "Historical incidents"
        ],
        primary_authority=[
            "OWASP Top 10",
            "NIST SP 800-53",
            "PCI DSS"
        ],
        burden_holder="Application Developer",
        adversary_position="Attacker exploits XSS vulnerabilities to execute malicious scripts.",
        counter_arguments=[
            "Output encoding and input validation are enforced.",
            "CSP headers reduce XSS risk.",
            "Historical incidents are reviewed."
        ],
        resolution_strategy="Implement output encoding, enforce input validation, review regularly.",
        entity_scope="Application output and scripts",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OWASP Top 10 XSS"
    ),
    DoctrineBlock(
        topic="OWASP Top 10: CSRF",
        keywords=["OWASP Top 10", "CSRF", "Cross-Site Request Forgery", "Token", "Session"],
        conclusion_template="CSRF threats are mitigated if anti-CSRF tokens and session management are enforced.",
        reasoning_framework=(
            "Cross-Site Request Forgery (CSRF) occurs when attackers trick users into executing unwanted actions. "
            "OWASP recommends anti-CSRF tokens, secure session management, and user authentication. "
            "Assess the use of secure frameworks and libraries. "
            "Review historical incidents of CSRF attacks. "
            "Monitor for anomalous request patterns and failed token validation. "
            "Cross-reference with STRIDE Spoofing and DREAD Exploitability. "
            "Document mitigations such as anti-CSRF tokens, session management, and user authentication."
        ),
        key_factors=[
            "Anti-CSRF tokens",
            "Session management",
            "User authentication",
            "Secure framework usage",
            "Historical incidents"
        ],
        primary_authority=[
            "OWASP Top 10",
            "NIST SP 800-53",
            "PCI DSS"
        ],
        burden_holder="Application Developer",
        adversary_position="Attacker exploits CSRF vulnerabilities to execute unwanted actions.",
        counter_arguments=[
            "Anti-CSRF tokens and session management are enforced.",
            "User authentication reduces CSRF risk.",
            "Historical incidents are reviewed."
        ],
        resolution_strategy="Implement anti-CSRF tokens, enforce session management, review regularly.",
        entity_scope="Application requests and sessions",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OWASP Top 10 CSRF"
    ),
    DoctrineBlock(
        topic="OWASP Top 10: SSRF",
        keywords=["OWASP Top 10", "SSRF", "Server-Side Request Forgery", "Input Validation", "Network Segmentation"],
        conclusion_template="SSRF threats are mitigated if input validation and network segmentation are enforced.",
        reasoning_framework=(
            "Server-Side Request Forgery (SSRF) occurs when attackers induce the server to make requests to unintended locations. "
            "OWASP recommends input validation, network segmentation, and whitelisting of allowed endpoints. "
            "Assess the use of secure frameworks and libraries. "
            "Review historical incidents of SSRF attacks. "
            "Monitor for anomalous request patterns and failed input validation. "
            "Cross-reference with STRIDE Information Disclosure and DREAD Exploitability. "
            "Document mitigations such as input validation, network segmentation, and endpoint whitelisting."
        ),
        key_factors=[
            "Input validation",
            "Network segmentation",
            "Endpoint whitelisting",
            "Secure framework usage",
            "Historical incidents"
        ],
        primary_authority=[
            "OWASP Top 10",
            "NIST SP 800-53",
            "PCI DSS"
        ],
        burden_holder="Application Developer",
        adversary_position="Attacker exploits SSRF vulnerabilities to access internal resources.",
        counter_arguments=[
            "Input validation and network segmentation are enforced.",
            "Endpoint whitelisting reduces SSRF risk.",
            "Historical incidents are reviewed."
        ],
        resolution_strategy="Implement input validation, enforce network segmentation, review regularly.",
        entity_scope="Application requests and network",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OWASP Top 10 SSRF"
    ),
    DoctrineBlock(
        topic="CVSS Scoring: Base Metrics",
        keywords=["CVSS", "Scoring", "Base Metrics", "Severity", "Vulnerability"],
        conclusion_template="CVSS base metrics are accurate if severity and exploitability are assessed and documented.",
        reasoning_framework=(
            "CVSS base metrics assess the severity and exploitability of vulnerabilities. "
            "Document attack vector, complexity, privileges required, and user interaction. "
            "Assess impact on confidentiality, integrity, and availability. "
            "Review historical incidents and lessons learned. "
            "Ensure base metrics are comprehensive and actionable. "
            "Cross-reference with DREAD Risk Assessment and PASTA Vulnerability Analysis. "
            "Document base metrics in vulnerability management artifacts."
        ),
        key_factors=[
            "Attack vector documentation",
            "Complexity assessment",
            "Privilege requirement",
            "User interaction",
            "Impact assessment"
        ],
        primary_authority=[
            "CVSS v3.1",
            "NIST SP 800-53",
            "MITRE ATT&CK"
        ],
        burden_holder="Vulnerability Manager",
        adversary_position="Threat actors exploit vulnerabilities with high base metrics.",
        counter_arguments=[
            "Base metrics are assessed and documented.",
            "Severity and exploitability are reviewed.",
            "Historical incidents are analyzed."
        ],
        resolution_strategy="Document base metrics, review regularly, update as needed.",
        entity_scope="Vulnerabilities and severity",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CVSS v3.1"
    ),
    DoctrineBlock(
        topic="CVSS Scoring: Temporal Metrics",
        keywords=["CVSS", "Scoring", "Temporal Metrics", "Exploit Code Maturity", "Remediation"],
        conclusion_template="CVSS temporal metrics are accurate if exploit code maturity and remediation are assessed and documented.",
        reasoning_framework=(
            "CVSS temporal metrics assess the maturity of exploit code and availability of remediation. "
            "Document exploit code maturity, remediation level, and report confidence. "
            "Assess the impact of temporal metrics on risk prioritization. "
            "Review historical incidents and lessons learned. "
            "Ensure temporal metrics are comprehensive and actionable. "
            "Cross-reference with DREAD Risk Assessment and PASTA Risk Analysis. "
            "Document temporal metrics in vulnerability management artifacts."
        ),
        key_factors=[
            "Exploit code maturity",
            "Remediation level",
            "Report confidence",
            "Risk prioritization",
            "Historical incidents"
        ],
        primary_authority=[
            "CVSS v3.1",
            "NIST SP 800-53",
            "MITRE ATT&CK"
        ],
        burden_holder="Vulnerability Manager",
        adversary_position="Threat actors exploit vulnerabilities with mature exploit code.",
        counter_arguments=[
            "Temporal metrics are assessed and documented.",
            "Remediation is available.",
            "Historical incidents are analyzed."
        ],
        resolution_strategy="Document temporal metrics, review regularly, update as needed.",
        entity_scope="Vulnerabilities and exploit code",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CVSS v3.1"
    ),
    DoctrineBlock(
        topic="CVSS Scoring: Environmental Metrics",
        keywords=["CVSS", "Scoring", "Environmental Metrics", "Business Impact", "Asset Value"],
        conclusion_template="CVSS environmental metrics are accurate if business impact and asset value are assessed and documented.",
        reasoning_framework=(
            "CVSS environmental metrics assess the impact of vulnerabilities on business and asset value. "
            "Document asset value, business impact, and modified base metrics. "
            "Assess the impact of environmental metrics on risk prioritization. "
            "Review historical incidents and lessons learned. "
            "Ensure environmental metrics are comprehensive and actionable. "
            "Cross-reference with DREAD Risk Assessment and PASTA Risk Analysis. "
            "Document environmental metrics in vulnerability management artifacts."
        ),
        key_factors=[
            "Asset value documentation",
            "Business impact assessment",
            "Modified base metrics",
            "Risk prioritization",
            "Historical incidents"
        ],
        primary_authority=[
            "CVSS v3.1",
            "NIST SP 800-53",
            "ISO/IEC 27005"
        ],
        burden_holder="Vulnerability Manager",
        adversary_position="Threat actors exploit vulnerabilities with high environmental impact.",
        counter_arguments=[
            "Environmental metrics are assessed and documented.",
            "Business impact is reviewed.",
            "Historical incidents are analyzed."
        ],
        resolution_strategy="Document environmental metrics, review regularly, update as needed.",
        entity_scope="Vulnerabilities and business impact",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CVSS v3.1"
    ),
    DoctrineBlock(
        topic="Intrusion Detection: Signature-Based",
        keywords=["Intrusion Detection", "Signature-Based", "IDS", "SIEM", "Log Correlation"],
        conclusion_template="Signature-based intrusion detection is effective if signatures are updated and log correlation is enforced.",
        reasoning_framework=(
            "Signature-based intrusion detection relies on known patterns to identify threats. "
            "Document signature libraries and update frequency. "
            "Assess the effectiveness of log correlation and SIEM integration. "
            "Review historical incidents and lessons learned. "
            "Monitor for anomalous activity and signature matches. "
            "Cross-reference with Anomaly-Based Detection and DREAD Risk Assessment. "
            "Document signature-based detection in security monitoring artifacts."
        ),
        key_factors=[
            "Signature library documentation",
            "Update frequency",
            "Log correlation",
            "SIEM integration",
            "Historical incidents"
        ],
        primary_authority=[
            "NIST SP 800-94",
            "MITRE ATT&CK",
            "PCI DSS"
        ],
        burden_holder="Security Operations Center",
        adversary_position="Threat actors evade signature-based detection with novel attacks.",
        counter_arguments=[
            "Signatures are updated regularly.",
            "Log correlation enhances detection.",
            "Historical incidents are reviewed."
        ],
        resolution_strategy="Update signatures, enhance log correlation, integrate with SIEM.",
        entity_scope="Network and application logs",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NIST SP 800-94"
    ),
    DoctrineBlock(
        topic="Intrusion Detection: Anomaly-Based",
        keywords=["Intrusion Detection", "Anomaly-Based", "IDS", "SIEM", "Behavior Analysis"],
        conclusion_template="Anomaly-based intrusion detection is effective if behavioral baselines and anomaly detection are enforced.",
        reasoning_framework=(
            "Anomaly-based intrusion detection relies on behavioral baselines to identify threats. "
            "Document baseline behaviors and anomaly detection algorithms. "
            "Assess the effectiveness of SIEM integration and log correlation. "
            "Review historical incidents and lessons learned. "
            "Monitor for anomalous activity and deviations from baseline. "
            "Cross-reference with Signature-Based Detection and DREAD Risk Assessment. "
            "Document anomaly-based detection in security monitoring artifacts."
        ),
        key_factors=[
            "Behavioral baseline documentation",
            "Anomaly detection algorithms",
            "SIEM integration",
            "Log correlation",
            "Historical incidents"
        ],
        primary_authority=[
            "NIST SP 800-94",
            "MITRE ATT&CK",
            "PCI DSS"
        ],
        burden_holder="Security Operations Center",
        adversary_position="Threat actors evade anomaly-based detection by mimicking normal behavior.",
        counter_arguments=[
            "Behavioral baselines are documented.",
            "Anomaly detection algorithms are effective.",
            "Historical incidents are reviewed."
        ],
        resolution_strategy="Document baselines, enhance anomaly detection, integrate with SIEM.",
        entity_scope="Network and application logs",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NIST SP 800-94"
    ),
    DoctrineBlock(
        topic="Intrusion Detection: Hybrid Approaches",
        keywords=["Intrusion Detection", "Hybrid", "IDS", "SIEM", "Log Correlation"],
        conclusion_template="Hybrid intrusion detection is effective if signature and anomaly-based methods are integrated and log correlation is enforced.",
        reasoning_framework=(
            "Hybrid intrusion detection combines signature and anomaly-based methods. "
            "Document integration strategies and effectiveness. "
            "Assess the impact on detection accuracy and false positives. "
            "Review historical incidents and lessons learned. "
            "Monitor for anomalous activity and signature matches. "
            "Cross-reference with Signature-Based and Anomaly-Based Detection. "
            "Document hybrid detection in security monitoring artifacts."
        ),
        key_factors=[
            "Integration strategy documentation",
            "Detection accuracy",
            "False positive assessment",
            "SIEM integration",
            "Historical incidents"
        ],
        primary_authority=[
            "NIST SP 800-94",
            "MITRE ATT&CK",
            "PCI DSS"
        ],
        burden_holder="Security Operations Center",
        adversary_position="Threat actors evade hybrid detection with sophisticated attacks.",
        counter_arguments=[
            "Integration strategies are documented.",
            "Detection accuracy is reviewed.",
            "Historical incidents are analyzed."
        ],
        resolution_strategy="Integrate signature and anomaly-based methods, enhance log correlation, review regularly.",
        entity_scope="Network and application logs",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NIST SP 800-94"
    ),
    DoctrineBlock(
        topic="SIEM Integration and Log Correlation",
        keywords=["SIEM", "Log Correlation", "Intrusion Detection", "Monitoring", "Incident Response"],
        conclusion_template="SIEM integration and log correlation are effective if logs are comprehensive and correlation rules are enforced.",
        reasoning_framework=(
            "SIEM integration and log correlation enhance intrusion detection and incident response. "
            "Document log sources and correlation rules. "
            "Assess the effectiveness of SIEM integration and log correlation. "
            "Review historical incidents and lessons learned. "
            "Monitor for anomalous activity and correlated events. "
            "Cross-reference with Intrusion Detection and DREAD Risk Assessment. "
            "Document SIEM integration and log correlation in security monitoring artifacts."
        ),
        key_factors=[
            "Log source documentation",
            "Correlation rule assessment",
            "SIEM integration",
            "Incident response procedures",
            "Historical incidents"
        ],
        primary_authority=[
            "NIST SP 800-92",
            "MITRE ATT&CK",
            "PCI DSS"
        ],
        burden_holder="Security Operations Center",
        adversary_position="Threat actors evade detection by exploiting gaps in log correlation.",
        counter_arguments=[
            "Log sources are comprehensive.",
            "Correlation rules are enforced.",
            "Historical incidents are reviewed."
        ],
        resolution_strategy="Enhance log correlation, integrate with SIEM, review regularly.",
        entity_scope="Network and application logs",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NIST SP 800-92"
    ),
    DoctrineBlock(
        topic="OWASP Top 10: Broken Authentication",
        keywords=["OWASP Top 10", "Authentication", "Broken Authentication", "Credential Management", "Session"],
        conclusion_template="Broken authentication threats are mitigated if credential management and session controls are enforced.",
        reasoning_framework=(
            "Broken authentication occurs when attackers can compromise credentials or session tokens. "
            "OWASP recommends strong password policies, secure credential storage, and session management. "
            "Assess the use of multi-factor authentication and account lockout mechanisms. "
            "Review historical incidents of authentication attacks. "
            "Monitor for anomalous login attempts and failed authentications. "
            "Cross-reference with STRIDE Spoofing and DREAD Exploitability. "
            "Document mitigations such as credential management, session controls, and MFA."
        ),
        key_factors=[
            "Password policy",
            "Credential storage",
            "Session management",
            "Multi-factor authentication",
            "Historical incidents"
        ],
        primary_authority=[
            "OWASP Top 10",
            "NIST SP 800-63",
            "PCI DSS"
        ],
        burden_holder="Application Developer",
        adversary_position="Attacker exploits broken authentication to gain unauthorized access.",
        counter_arguments=[
            "Credential management and session controls are enforced.",
            "Multi-factor authentication reduces risk.",
            "Historical incidents are reviewed."
        ],
        resolution_strategy="Implement credential management, enforce session controls, review regularly.",
        entity_scope="Authentication subsystem",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OWASP Top 10 Broken Authentication"
    ),
    DoctrineBlock(
        topic="OWASP Top 10: Sensitive Data Exposure",
        keywords=["OWASP Top 10", "Sensitive Data Exposure", "Encryption", "Access Control", "Data Leakage"],
        conclusion_template="Sensitive data exposure threats are mitigated if encryption and access controls are enforced.",
        reasoning_framework=(
            "Sensitive data exposure occurs when attackers access confidential data. "
            "OWASP recommends encryption at rest and in transit, access controls, and data classification. "
            "Assess the use of secure storage and transmission protocols. "
            "Review historical incidents of data exposure. "
            "Monitor for anomalous access patterns and data leakage. "
            "Cross-reference with STRIDE Information Disclosure and DREAD Damage Potential. "
            "Document mitigations such as encryption, access controls, and monitoring."
        ),
        key_factors=[
            "Encryption",
            "Access controls",
            "Data classification",
            "Secure storage",
            "Historical incidents"
        ],
        primary_authority=[
            "OWASP Top 10",
            "NIST SP 800-53",
            "GDPR"
        ],
        burden_holder="Application Developer",
        adversary_position="Attacker exploits sensitive data exposure to access confidential information.",
        counter_arguments=[
            "Encryption and access controls are enforced.",
            "Data classification reduces exposure risk.",
            "Historical incidents are reviewed."
        ],
        resolution_strategy="Implement encryption, enforce access controls, review regularly.",
        entity_scope="Sensitive data flows and storage",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OWASP Top 10 Sensitive Data Exposure"
    ),
    DoctrineBlock(
        topic="OWASP Top 10: Broken Access Control",
        keywords=["OWASP Top 10", "Access Control", "Broken Access Control", "Authorization", "Privilege"],
        conclusion_template="Broken access control threats are mitigated if authorization and privilege boundaries are enforced.",
        reasoning_framework=(
            "Broken access control occurs when attackers gain unauthorized access to resources. "
            "OWASP recommends enforcing authorization, privilege boundaries, and RBAC. "
            "Assess the use of access control mechanisms and privilege escalation detection. "
            "Review historical incidents of access control failures. "
            "Monitor for anomalous access patterns and privilege changes. "
            "Cross-reference with STRIDE Elevation of Privilege and DREAD Exploitability. "
            "Document mitigations such as authorization, privilege boundaries, and RBAC."
        ),
        key_factors=[
            "Authorization",
            "Privilege boundaries",
            "RBAC",
            "Access control mechanisms",
            "Historical incidents"
        ],
        primary_authority=[
            "OWASP Top 10",
            "NIST SP 800-53",
            "PCI DSS"
        ],
        burden_holder="Application Developer",
        adversary_position="Attacker exploits broken access control to gain unauthorized privileges.",
        counter_arguments=[
            "Authorization and privilege boundaries are enforced.",
            "RBAC reduces access control risk.",
            "Historical incidents are reviewed."
        ],
        resolution_strategy="Implement authorization, enforce privilege boundaries, review regularly.",
        entity_scope="Access control subsystem",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OWASP Top 10 Broken Access Control"
    ),
    DoctrineBlock(
        topic="OWASP Top 10: Security Misconfiguration",
        keywords=["OWASP Top 10", "Security Misconfiguration", "Configuration", "Hardening", "Patch Management"],
        conclusion_template="Security misconfiguration threats are mitigated if configuration hardening and patch management are enforced.",
        reasoning_framework=(
            "Security misconfiguration occurs when systems are not securely configured. "
            "OWASP recommends configuration hardening, patch management, and regular reviews. "
            "Assess the use of secure defaults and automated configuration tools. "
            "Review historical incidents of misconfiguration. "
            "Monitor for anomalous configuration changes and vulnerabilities. "
            "Cross-reference with STRIDE Tampering and DREAD Exploitability. "
            "Document mitigations such as configuration hardening, patch management, and reviews."
        ),
        key_factors=[
            "Configuration hardening",
            "Patch management",
            "Secure defaults",
            "Automated tools",
            "Historical incidents"
        ],
        primary_authority=[
            "OWASP Top 10",
            "NIST SP 800-53",
            "PCI DSS"
        ],
        burden_holder="System Administrator",
        adversary_position="Attacker exploits security misconfiguration to gain unauthorized access.",
        counter_arguments=[
            "Configuration hardening and patch management are enforced.",
            "Secure defaults reduce misconfiguration risk.",
            "Historical incidents are reviewed."
        ],
        resolution_strategy="Implement configuration hardening, enforce patch management, review regularly.",
        entity_scope="System configuration",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OWASP Top 10 Security Misconfiguration"
    ),
    DoctrineBlock(
        topic="OWASP Top 10: Insecure Deserialization",
        keywords=["OWASP Top 10", "Insecure Deserialization", "Serialization", "Input Validation", "Code Execution"],
        conclusion_template="Insecure deserialization threats are mitigated if input validation and secure serialization are enforced.",
        reasoning_framework=(
            "Insecure deserialization occurs when untrusted data is deserialized, leading to code execution. "
            "OWASP recommends input validation, secure serialization libraries, and restricting object types. "
            "Assess the use of secure frameworks and libraries. "
            "Review historical incidents of insecure deserialization. "
            "Monitor for anomalous deserialization patterns and failed input validation. "
            "Cross-reference with STRIDE Tampering and DREAD Exploitability. "
            "Document mitigations such as input validation, secure serialization, and object restriction."
        ),
        key_factors=[
            "Input validation",
            "Secure serialization",
            "Object restriction",
            "Secure framework usage",
            "Historical incidents"
        ],
        primary_authority=[
            "OWASP Top 10",
            "NIST SP 800-53",
            "PCI DSS"
        ],
        burden_holder="Application Developer",
        adversary_position="Attacker exploits insecure deserialization to execute arbitrary code.",
        counter_arguments=[
            "Input validation and secure serialization are enforced.",
            "Object restriction reduces deserialization risk.",
            "Historical incidents are reviewed."
        ],
        resolution_strategy="Implement input validation, enforce secure serialization, review regularly.",
        entity_scope="Serialization subsystem",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OWASP Top 10 Insecure Deserialization"
    ),
    DoctrineBlock(
        topic="OWASP Top 10: Using Components with Known Vulnerabilities",
        keywords=["OWASP Top 10", "Components", "Known Vulnerabilities", "Dependency Management", "Patch"],
        conclusion_template="Threats from components with known vulnerabilities are mitigated if dependency management and patching are enforced.",
        reasoning_framework=(
            "Using components with known vulnerabilities exposes applications to risk. "
            "OWASP recommends dependency management, patching, and vulnerability scanning. "
            "Assess the use of automated tools and secure repositories. "
            "Review historical incidents of component vulnerabilities. "
            "Monitor for anomalous component usage and vulnerabilities. "
            "Cross-reference with STRIDE Tampering and DREAD Exploitability. "
            "Document mitigations such as dependency management, patching, and scanning."
        ),
        key_factors=[
            "Dependency management",
            "Patching",
            "Vulnerability scanning",
            "Automated tools",
            "Historical incidents"
        ],
        primary_authority=[
            "OWASP Top 10",
            "NIST SP 800-53",
            "PCI DSS"
        ],
        burden_holder="Application Developer",
        adversary_position="Attacker exploits known vulnerabilities in components.",
        counter_arguments=[
            "Dependency management and patching are enforced.",
            "Vulnerability scanning reduces risk.",
            "Historical incidents are reviewed."
        ],
        resolution_strategy="Implement dependency management, enforce patching, review regularly.",
        entity_scope="Application components",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OWASP Top 10 Using Components with Known Vulnerabilities"
    ),
    DoctrineBlock(
        topic="OWASP Top 10: Insufficient Logging and Monitoring",
        keywords=["OWASP Top 10", "Logging", "Monitoring", "Incident Response", "SIEM"],
        conclusion_template="Insufficient logging and monitoring threats are mitigated if comprehensive logging and SIEM integration are enforced.",
        reasoning_framework=(
            "Insufficient logging and monitoring occurs when attacks go undetected due to lack of visibility. "
            "OWASP recommends comprehensive logging, monitoring, and SIEM integration. "
            "Assess the use of log correlation and incident response procedures. "
            "Review historical incidents of undetected attacks. "
            "Monitor for anomalous activity and correlated events. "
            "Cross-reference with Intrusion Detection and DREAD Risk Assessment. "
            "Document mitigations such as logging, monitoring, and SIEM integration."
        ),
        key_factors=[
            "Comprehensive logging",
            "Monitoring",
            "SIEM integration",
            "Incident response",
            "Historical incidents"
        ],
        primary_authority=[
            "OWASP Top 10",
            "NIST SP 800-92",
            "PCI DSS"
        ],
        burden_holder="Security Operations Center",
        adversary_position="Attacker exploits insufficient logging and monitoring to evade detection.",
        counter_arguments=[
            "Logging and monitoring are comprehensive.",
            "SIEM integration enhances detection.",
            "Historical incidents are reviewed."
        ],
        resolution_strategy="Implement comprehensive logging, enforce SIEM integration, review regularly.",
        entity_scope="Application and system logs",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OWASP Top 10 Insufficient Logging and Monitoring"
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