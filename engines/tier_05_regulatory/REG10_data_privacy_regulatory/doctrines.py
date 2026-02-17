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
        topic="CCPA Consumer Right to Access",
        keywords=["CCPA", "consumer rights", "access", "personal information", "California"],
        conclusion_template="Consumers have the right to request access to their personal information collected by a business under the CCPA.",
        reasoning_framework=(
            "Under the California Consumer Privacy Act (CCPA), consumers are granted the right to request disclosure of the categories and specific pieces of personal information that a business has collected about them. "
            "The business must respond within 45 days, providing the requested information in a readily usable format. "
            "The scope of 'personal information' is broad, including identifiers, commercial information, biometric data, and more. "
            "Businesses must verify the identity of the requester before disclosing information. "
            "Exceptions apply where disclosure would compromise security or violate other laws. "
            "The CCPA requires clear procedures for handling access requests, including documentation and tracking. "
            "Failure to comply may result in enforcement actions by the California Attorney General and statutory damages."
        ),
        key_factors=[
            "Consumer identity verification",
            "Scope of personal information",
            "Timeliness of response",
            "Format of disclosure",
            "Applicable exceptions"
        ],
        primary_authority=["CCPA §1798.100", "CCPA §1798.110"],
        burden_holder="Business",
        adversary_position="Business may argue that disclosure is not required due to exceptions or insufficient verification.",
        counter_arguments=[
            "Consumer provides sufficient verification",
            "No applicable exception under CCPA",
            "Business failed to respond timely"
        ],
        resolution_strategy="Implement robust verification and response procedures; consult legal counsel for exceptions.",
        entity_scope="Businesses subject to CCPA (>$25M revenue, >50,000 consumers, or >50% revenue from selling PI)",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="CCPA Regulations §999.313"
    ),
    DoctrineBlock(
        topic="CCPA Consumer Right to Deletion",
        keywords=["CCPA", "consumer rights", "deletion", "personal information", "California"],
        conclusion_template="Consumers have the right to request deletion of their personal information held by a business under the CCPA, subject to exceptions.",
        reasoning_framework=(
            "The CCPA provides consumers the right to request deletion of their personal information collected by businesses. "
            "Upon receiving a verifiable request, businesses must delete the information and direct their service providers to do the same. "
            "Exceptions include situations where retention is necessary for completing transactions, detecting security incidents, complying with legal obligations, or other enumerated purposes. "
            "Businesses must inform consumers of these exceptions in their privacy notices. "
            "The process requires identity verification and tracking of deletion requests. "
            "Non-compliance may result in enforcement actions and statutory damages."
        ),
        key_factors=[
            "Verification of consumer identity",
            "Existence of statutory exceptions",
            "Timeliness of deletion",
            "Communication with service providers"
        ],
        primary_authority=["CCPA §1798.105"],
        burden_holder="Business",
        adversary_position="Business may claim exception or insufficient verification.",
        counter_arguments=[
            "Consumer provides sufficient verification",
            "Business does not qualify for exception",
            "Failure to delete or notify service providers"
        ],
        resolution_strategy="Maintain clear deletion procedures and exception documentation.",
        entity_scope="Businesses subject to CCPA",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="CCPA Regulations §999.312"
    ),
    DoctrineBlock(
        topic="CCPA Consumer Right to Data Portability",
        keywords=["CCPA", "consumer rights", "portability", "personal information", "California"],
        conclusion_template="Consumers may request their personal information in a portable, readily usable format under the CCPA.",
        reasoning_framework=(
            "The CCPA requires businesses to provide personal information to consumers in a format that allows them to transmit the data to another entity. "
            "This right is triggered upon a verified access request. "
            "Businesses must ensure the format is commonly used and does not hinder transmission. "
            "Sensitive information must be protected during transmission, and businesses must verify the identity of the requester. "
            "Exceptions apply where disclosure would compromise security or violate other laws."
        ),
        key_factors=[
            "Format of data",
            "Verification of identity",
            "Security of transmission",
            "Applicability of exceptions"
        ],
        primary_authority=["CCPA §1798.100(d)"],
        burden_holder="Business",
        adversary_position="Business may argue technical infeasibility or exception.",
        counter_arguments=[
            "Consumer requests in a commonly used format",
            "Business has capability to provide data",
            "No applicable exception"
        ],
        resolution_strategy="Develop standardized data export procedures and secure transmission protocols.",
        entity_scope="Businesses subject to CCPA",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="CCPA Regulations §999.313(c)"
    ),
    DoctrineBlock(
        topic="CPRA Amendments - Sensitive Personal Information",
        keywords=["CPRA", "CCPA", "sensitive personal information", "California", "privacy"],
        conclusion_template="Businesses must provide additional protections and disclosures for sensitive personal information under the CPRA.",
        reasoning_framework=(
            "The California Privacy Rights Act (CPRA) expands the CCPA by introducing the concept of 'sensitive personal information' (SPI), which includes data such as social security numbers, driver's license numbers, financial account information, precise geolocation, racial or ethnic origin, religious beliefs, and more. "
            "Businesses must provide clear disclosures regarding the collection and use of SPI, and offer consumers the right to limit its use and disclosure. "
            "The CPRA requires businesses to implement reasonable security measures to protect SPI and to honor consumer requests to limit processing. "
            "Non-compliance may result in enforcement actions by the California Privacy Protection Agency."
        ),
        key_factors=[
            "Definition of SPI",
            "Consumer right to limit use",
            "Security measures",
            "Disclosure requirements"
        ],
        primary_authority=["CPRA §1798.121", "CPRA §1798.140(ae)"],
        burden_holder="Business",
        adversary_position="Business may argue SPI is not collected or processed.",
        counter_arguments=[
            "Consumer demonstrates SPI is collected",
            "Business fails to provide disclosures",
            "Insufficient security measures"
        ],
        resolution_strategy="Update privacy notices and implement SPI-specific controls.",
        entity_scope="Businesses subject to CPRA",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="CPRA Regulations §7002"
    ),
    DoctrineBlock(
        topic="CPRA Opt-Out Rights for Sale/Sharing",
        keywords=["CPRA", "CCPA", "opt-out", "sale", "sharing", "personal information", "California"],
        conclusion_template="Consumers have the right to opt-out of the sale or sharing of their personal information under the CPRA.",
        reasoning_framework=(
            "The CPRA expands opt-out rights to include both the sale and sharing of personal information for cross-context behavioral advertising. "
            "Businesses must provide a clear and conspicuous link titled 'Do Not Sell or Share My Personal Information' on their websites. "
            "Consumers may exercise this right at any time, and businesses must honor the request within 15 days. "
            "Businesses are prohibited from discriminating against consumers for exercising opt-out rights."
        ),
        key_factors=[
            "Definition of sale and sharing",
            "Opt-out mechanism",
            "Timeliness of response",
            "Non-discrimination"
        ],
        primary_authority=["CPRA §1798.115", "CPRA §1798.120"],
        burden_holder="Business",
        adversary_position="Business may argue information is not sold/shared.",
        counter_arguments=[
            "Consumer demonstrates sale/sharing",
            "Business fails to provide opt-out mechanism",
            "Discriminatory practices"
        ],
        resolution_strategy="Implement opt-out links and monitor compliance.",
        entity_scope="Businesses subject to CPRA",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="CPRA Regulations §7012"
    ),
    DoctrineBlock(
        topic="GDPR Lawful Basis for Processing",
        keywords=["GDPR", "lawful basis", "processing", "personal data", "EU"],
        conclusion_template="Organizations must establish a lawful basis for processing personal data under the GDPR.",
        reasoning_framework=(
            "The General Data Protection Regulation (GDPR) requires that all processing of personal data be based on one of six lawful bases: consent, contract, legal obligation, vital interests, public task, or legitimate interests. "
            "Organizations must document the chosen lawful basis and ensure it is appropriate for the processing activity. "
            "Consent must be freely given, specific, informed, and unambiguous. "
            "Legitimate interests require a balancing test to ensure the interests of the organization do not override the rights and freedoms of data subjects. "
            "Failure to establish a lawful basis may result in enforcement actions and significant fines."
        ),
        key_factors=[
            "Selection and documentation of lawful basis",
            "Nature of processing",
            "Balancing test for legitimate interests",
            "Quality of consent"
        ],
        primary_authority=["GDPR Art. 6"],
        burden_holder="Data Controller",
        adversary_position="Data subject may argue lack of lawful basis.",
        counter_arguments=[
            "Controller documents lawful basis",
            "Consent is valid",
            "Balancing test favors controller"
        ],
        resolution_strategy="Conduct regular reviews of processing activities and update documentation.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Consent"
    ),
    DoctrineBlock(
        topic="GDPR Data Minimization Principle",
        keywords=["GDPR", "data minimization", "personal data", "EU", "privacy"],
        conclusion_template="Organizations must collect and process only the minimum personal data necessary for the specified purpose under the GDPR.",
        reasoning_framework=(
            "The GDPR mandates that personal data collected must be adequate, relevant, and limited to what is necessary in relation to the purposes for which it is processed. "
            "Organizations must assess the necessity of each data element and avoid excessive collection. "
            "Data minimization is a core principle that supports privacy by design and reduces risk. "
            "Regular audits and reviews are required to ensure compliance."
        ),
        key_factors=[
            "Necessity of data elements",
            "Purpose specification",
            "Audit and review procedures",
            "Privacy by design"
        ],
        primary_authority=["GDPR Art. 5(1)(c)"],
        burden_holder="Data Controller",
        adversary_position="Data subject may argue excessive collection.",
        counter_arguments=[
            "Controller demonstrates necessity",
            "Purpose is legitimate",
            "Data is limited"
        ],
        resolution_strategy="Implement data minimization policies and conduct periodic reviews.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Data Minimization"
    ),
    DoctrineBlock(
        topic="GDPR Data Subject Right to Access",
        keywords=["GDPR", "data subject rights", "access", "personal data", "EU"],
        conclusion_template="Data subjects have the right to access their personal data processed by a controller under the GDPR.",
        reasoning_framework=(
            "The GDPR grants data subjects the right to obtain confirmation as to whether their personal data is being processed, and access to the data and related information. "
            "Controllers must respond to access requests within one month, providing information on the purposes of processing, categories of data, recipients, retention periods, and sources. "
            "Controllers must verify the identity of the requester and may charge a reasonable fee for excessive requests. "
            "Exceptions apply where disclosure would adversely affect the rights and freedoms of others."
        ),
        key_factors=[
            "Timeliness of response",
            "Scope of information provided",
            "Identity verification",
            "Applicability of exceptions"
        ],
        primary_authority=["GDPR Art. 15"],
        burden_holder="Data Controller",
        adversary_position="Controller may argue exception or excessive request.",
        counter_arguments=[
            "Data subject provides verification",
            "Request is reasonable",
            "No applicable exception"
        ],
        resolution_strategy="Establish access request procedures and train staff.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Data Subject Rights"
    ),
    DoctrineBlock(
        topic="GDPR Data Subject Right to Rectification",
        keywords=["GDPR", "data subject rights", "rectification", "personal data", "EU"],
        conclusion_template="Data subjects have the right to request correction of inaccurate personal data under the GDPR.",
        reasoning_framework=(
            "The GDPR provides data subjects the right to have inaccurate personal data corrected without undue delay. "
            "Controllers must assess the accuracy of the data and implement correction procedures. "
            "If the data is incomplete, data subjects may request completion. "
            "Controllers must notify recipients of the corrected data unless this proves impossible or involves disproportionate effort."
        ),
        key_factors=[
            "Accuracy of personal data",
            "Timeliness of correction",
            "Notification to recipients",
            "Verification of request"
        ],
        primary_authority=["GDPR Art. 16"],
        burden_holder="Data Controller",
        adversary_position="Controller may argue data is accurate or request is unfounded.",
        counter_arguments=[
            "Data subject provides evidence",
            "Controller fails to correct",
            "Notification obligations not met"
        ],
        resolution_strategy="Implement rectification procedures and maintain records.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Data Subject Rights"
    ),
    DoctrineBlock(
        topic="GDPR Data Subject Right to Erasure ('Right to be Forgotten')",
        keywords=["GDPR", "data subject rights", "erasure", "right to be forgotten", "personal data", "EU"],
        conclusion_template="Data subjects may request erasure of their personal data under the GDPR, subject to exceptions.",
        reasoning_framework=(
            "The GDPR grants data subjects the right to have their personal data erased without undue delay where certain grounds apply, such as withdrawal of consent, unlawful processing, or no longer necessary for the purpose. "
            "Controllers must notify recipients of the erased data unless this proves impossible or involves disproportionate effort. "
            "Exceptions include compliance with legal obligations, public interest, or exercise of legal claims."
        ),
        key_factors=[
            "Grounds for erasure",
            "Timeliness of response",
            "Notification to recipients",
            "Applicability of exceptions"
        ],
        primary_authority=["GDPR Art. 17"],
        burden_holder="Data Controller",
        adversary_position="Controller may argue exception or necessity for retention.",
        counter_arguments=[
            "Data subject demonstrates grounds",
            "Controller fails to erase",
            "Notification obligations not met"
        ],
        resolution_strategy="Establish erasure request procedures and exception documentation.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Data Subject Rights"
    ),
    DoctrineBlock(
        topic="GDPR Data Subject Right to Data Portability",
        keywords=["GDPR", "data subject rights", "portability", "personal data", "EU"],
        conclusion_template="Data subjects may request their personal data in a structured, commonly used, and machine-readable format under the GDPR.",
        reasoning_framework=(
            "The GDPR provides data subjects the right to receive their personal data in a format that enables transmission to another controller. "
            "This applies where processing is based on consent or contract and carried out by automated means. "
            "Controllers must ensure the data is provided securely and without hindrance. "
            "Exceptions apply where transmission would adversely affect the rights and freedoms of others."
        ),
        key_factors=[
            "Format of data",
            "Basis for processing",
            "Security of transmission",
            "Applicability of exceptions"
        ],
        primary_authority=["GDPR Art. 20"],
        burden_holder="Data Controller",
        adversary_position="Controller may argue technical infeasibility or exception.",
        counter_arguments=[
            "Data subject requests in valid format",
            "Controller has capability",
            "No applicable exception"
        ],
        resolution_strategy="Develop standardized export procedures and secure transmission protocols.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Data Portability"
    ),
    DoctrineBlock(
        topic="COPPA Parental Consent Requirements",
        keywords=["COPPA", "parental consent", "children", "online privacy", "United States"],
        conclusion_template="Operators of online services directed to children under 13 must obtain verifiable parental consent before collecting personal information under COPPA.",
        reasoning_framework=(
            "The Children's Online Privacy Protection Act (COPPA) requires operators of websites and online services directed to children under 13 to obtain verifiable parental consent prior to collecting, using, or disclosing personal information. "
            "Operators must provide clear notice of their data practices and implement mechanisms for obtaining and verifying consent. "
            "Exceptions exist for internal operations, security, and certain educational purposes. "
            "Failure to comply may result in enforcement by the FTC and civil penalties."
        ),
        key_factors=[
            "Age of users",
            "Verifiability of parental consent",
            "Notice requirements",
            "Applicability of exceptions"
        ],
        primary_authority=["COPPA 15 U.S.C. §6501-6506"],
        burden_holder="Operator",
        adversary_position="Operator may argue consent is not required or obtained.",
        counter_arguments=[
            "Child is under 13",
            "Consent not verifiable",
            "Operator failed to provide notice"
        ],
        resolution_strategy="Implement robust consent mechanisms and maintain records.",
        entity_scope="Operators of websites/services directed to children under 13",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FTC COPPA Rule 16 CFR Part 312"
    ),
    DoctrineBlock(
        topic="COPPA Notice Requirements",
        keywords=["COPPA", "notice", "privacy policy", "children", "online privacy", "United States"],
        conclusion_template="Operators must provide clear and comprehensive notice of their data collection practices under COPPA.",
        reasoning_framework=(
            "COPPA mandates that operators of websites and online services directed to children under 13 provide clear, understandable, and prominent notice of their information practices. "
            "This includes what information is collected, how it is used, disclosure practices, and parental rights. "
            "Notice must be provided both on the website and directly to parents prior to collecting information. "
            "Failure to provide adequate notice may result in enforcement actions."
        ),
        key_factors=[
            "Clarity and prominence of notice",
            "Scope of information disclosed",
            "Timing of notice",
            "Compliance with FTC guidance"
        ],
        primary_authority=["COPPA 15 U.S.C. §6502(b)", "FTC COPPA Rule §312.4"],
        burden_holder="Operator",
        adversary_position="Operator may argue notice is sufficient or not required.",
        counter_arguments=[
            "Notice is unclear or incomplete",
            "Notice not provided prior to collection",
            "Operator failed to update notice"
        ],
        resolution_strategy="Review and update privacy policies regularly.",
        entity_scope="Operators of websites/services directed to children under 13",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FTC COPPA Rule 16 CFR Part 312"
    ),
    DoctrineBlock(
        topic="FERPA Education Records Privacy",
        keywords=["FERPA", "education records", "privacy", "students", "United States"],
        conclusion_template="Educational institutions must protect the privacy of student education records under FERPA.",
        reasoning_framework=(
            "The Family Educational Rights and Privacy Act (FERPA) grants students and parents the right to access and request amendment of education records, and restricts disclosure without consent. "
            "Institutions must implement safeguards to protect records and provide annual notice of rights. "
            "Exceptions permit disclosure without consent for legitimate educational interests, emergencies, or compliance with subpoenas. "
            "Non-compliance may result in loss of federal funding."
        ),
        key_factors=[
            "Definition of education records",
            "Safeguards and access controls",
            "Disclosure exceptions",
            "Annual notice requirements"
        ],
        primary_authority=["FERPA 20 U.S.C. §1232g", "34 CFR Part 99"],
        burden_holder="Educational Institution",
        adversary_position="Institution may argue disclosure is permitted under exception.",
        counter_arguments=[
            "Disclosure not justified",
            "Safeguards insufficient",
            "Failure to provide notice"
        ],
        resolution_strategy="Implement access controls and train staff.",
        entity_scope="Educational institutions receiving federal funds",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Department of Education FERPA Guidance"
    ),
    DoctrineBlock(
        topic="FERPA Disclosure Exceptions",
        keywords=["FERPA", "disclosure", "exceptions", "education records", "students", "United States"],
        conclusion_template="FERPA permits disclosure of education records without consent under specific exceptions.",
        reasoning_framework=(
            "FERPA allows educational institutions to disclose education records without consent for legitimate educational interests, health and safety emergencies, compliance with subpoenas, and certain government audits. "
            "Institutions must document the basis for disclosure and limit the scope to necessary information. "
            "Annual notice must inform students and parents of these exceptions."
        ),
        key_factors=[
            "Legitimacy of exception",
            "Documentation of disclosure",
            "Scope limitation",
            "Annual notice"
        ],
        primary_authority=["FERPA 20 U.S.C. §1232g(b)", "34 CFR §99.31"],
        burden_holder="Educational Institution",
        adversary_position="Institution may argue exception applies.",
        counter_arguments=[
            "Exception not applicable",
            "Disclosure exceeds scope",
            "Failure to document"
        ],
        resolution_strategy="Maintain disclosure logs and review exceptions regularly.",
        entity_scope="Educational institutions receiving federal funds",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Department of Education FERPA Guidance"
    ),
    DoctrineBlock(
        topic="GLBA Privacy Rule for Financial Institutions",
        keywords=["GLBA", "privacy rule", "financial institutions", "personal information", "United States"],
        conclusion_template="Financial institutions must provide privacy notices and limit disclosure of nonpublic personal information under the GLBA Privacy Rule.",
        reasoning_framework=(
            "The Gramm-Leach-Bliley Act (GLBA) Privacy Rule requires financial institutions to provide clear privacy notices describing their information collection and sharing practices. "
            "Consumers must be given the opportunity to opt-out of certain disclosures. "
            "Institutions must implement safeguards to protect nonpublic personal information and restrict disclosure to third parties except as permitted by law."
        ),
        key_factors=[
            "Clarity of privacy notice",
            "Opt-out mechanism",
            "Safeguards for information",
            "Permitted disclosures"
        ],
        primary_authority=["GLBA 15 U.S.C. §6801-6809", "16 CFR Part 313"],
        burden_holder="Financial Institution",
        adversary_position="Institution may argue disclosure is permitted.",
        counter_arguments=[
            "Notice is unclear",
            "Opt-out not provided",
            "Safeguards insufficient"
        ],
        resolution_strategy="Review privacy notices and implement opt-out procedures.",
        entity_scope="Financial institutions subject to GLBA",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FTC GLBA Privacy Rule Guidance"
    ),
    DoctrineBlock(
        topic="GLBA Safeguards Rule",
        keywords=["GLBA", "safeguards rule", "financial institutions", "security", "United States"],
        conclusion_template="Financial institutions must implement administrative, technical, and physical safeguards to protect customer information under the GLBA Safeguards Rule.",
        reasoning_framework=(
            "The GLBA Safeguards Rule requires financial institutions to develop, implement, and maintain a comprehensive information security program. "
            "The program must include risk assessment, employee training, and regular testing of controls. "
            "Institutions must adapt safeguards to the sensitivity of customer information and evolving threats. "
            "Non-compliance may result in enforcement actions and penalties."
        ),
        key_factors=[
            "Risk assessment procedures",
            "Employee training",
            "Testing and monitoring",
            "Adaptation to threats"
        ],
        primary_authority=["GLBA 15 U.S.C. §6801(b)", "16 CFR Part 314"],
        burden_holder="Financial Institution",
        adversary_position="Institution may argue safeguards are sufficient.",
        counter_arguments=[
            "Safeguards inadequate",
            "Risk assessment not conducted",
            "Training insufficient"
        ],
        resolution_strategy="Conduct regular risk assessments and update safeguards.",
        entity_scope="Financial institutions subject to GLBA",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FTC GLBA Safeguards Rule Guidance"
    ),
    DoctrineBlock(
        topic="FTC Act Section 5 Unfair/Deceptive Privacy Practices",
        keywords=["FTC Act", "Section 5", "unfair", "deceptive", "privacy", "security", "United States"],
        conclusion_template="Businesses must not engage in unfair or deceptive privacy and security practices under FTC Act Section 5.",
        reasoning_framework=(
            "Section 5 of the FTC Act prohibits unfair or deceptive acts or practices in commerce, including misrepresentations in privacy policies or failure to implement reasonable security measures. "
            "The FTC may bring enforcement actions against businesses that mislead consumers or expose them to unreasonable risks. "
            "Best practices include transparency, accuracy in disclosures, and implementation of industry-standard security controls."
        ),
        key_factors=[
            "Accuracy of privacy disclosures",
            "Security measures",
            "Consumer harm",
            "Transparency"
        ],
        primary_authority=["FTC Act 15 U.S.C. §45"],
        burden_holder="Business",
        adversary_position="Business may argue practices are not unfair/deceptive.",
        counter_arguments=[
            "Disclosures are misleading",
            "Security controls inadequate",
            "Consumer harm demonstrated"
        ],
        resolution_strategy="Review privacy policies and security controls regularly.",
        entity_scope="Businesses engaged in commerce in the United States",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FTC Enforcement Actions (e.g., Wyndham, LabMD)"
    ),
    DoctrineBlock(
        topic="State Data Breach Notification Laws - General Obligations",
        keywords=["state law", "data breach", "notification", "personal information", "United States"],
        conclusion_template="Businesses must notify affected individuals and regulators of data breaches involving personal information under state laws.",
        reasoning_framework=(
            "All U.S. states have enacted data breach notification laws requiring businesses to notify affected individuals and, in some cases, regulators, when personal information is compromised. "
            "Notification must be provided without unreasonable delay and include details of the breach, types of information affected, and steps individuals can take to protect themselves. "
            "Some states require additional measures, such as credit monitoring or public notice."
        ),
        key_factors=[
            "Timeliness of notification",
            "Content of notification",
            "Scope of affected information",
            "Regulatory reporting"
        ],
        primary_authority=["State breach notification statutes (e.g., Cal. Civ. Code §1798.82)"],
        burden_holder="Business",
        adversary_position="Business may argue breach does not trigger notification.",
        counter_arguments=[
            "Personal information compromised",
            "Delay in notification",
            "Incomplete notification"
        ],
        resolution_strategy="Develop incident response plans and monitor state law changes.",
        entity_scope="Businesses handling personal information in the United States",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="State Attorney General Guidance"
    ),
    DoctrineBlock(
        topic="GDPR Data Protection Impact Assessment (DPIA) Requirements",
        keywords=["GDPR", "DPIA", "data protection impact assessment", "risk", "personal data", "EU"],
        conclusion_template="Controllers must conduct a Data Protection Impact Assessment for high-risk processing activities under the GDPR.",
        reasoning_framework=(
            "The GDPR requires controllers to conduct a DPIA where processing is likely to result in a high risk to the rights and freedoms of data subjects, such as large-scale profiling, automated decision-making, or processing of sensitive data. "
            "The DPIA must assess risks, identify mitigation measures, and document outcomes. "
            "Supervisory authorities may review DPIAs and require additional safeguards. "
            "Failure to conduct a DPIA may result in enforcement actions and fines."
        ),
        key_factors=[
            "Risk assessment",
            "Scope of processing",
            "Mitigation measures",
            "Documentation"
        ],
        primary_authority=["GDPR Art. 35"],
        burden_holder="Data Controller",
        adversary_position="Controller may argue DPIA not required.",
        counter_arguments=[
            "Processing is high-risk",
            "DPIA not conducted",
            "Mitigation measures inadequate"
        ],
        resolution_strategy="Integrate DPIA into project planning and maintain records.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on DPIA"
    ),
    DoctrineBlock(
        topic="GDPR Cross-Border Data Transfers and Standard Contractual Clauses",
        keywords=["GDPR", "cross-border", "data transfers", "SCC", "personal data", "EU"],
        conclusion_template="Controllers must implement appropriate safeguards for cross-border data transfers under the GDPR, including Standard Contractual Clauses.",
        reasoning_framework=(
            "The GDPR restricts transfers of personal data outside the EU/EEA unless adequate safeguards are in place. "
            "Standard Contractual Clauses (SCCs) are a primary mechanism for ensuring compliance. "
            "Controllers must assess the legal environment of the recipient country and implement supplementary measures if necessary. "
            "Transfers must be documented and data subjects informed."
        ),
        key_factors=[
            "Adequacy of recipient country",
            "Implementation of SCCs",
            "Supplementary measures",
            "Documentation"
        ],
        primary_authority=["GDPR Art. 44-46", "EDPB Recommendations 01/2020"],
        burden_holder="Data Controller",
        adversary_position="Controller may argue transfer is permitted.",
        counter_arguments=[
            "Recipient country lacks adequacy",
            "SCCs not implemented",
            "Supplementary measures insufficient"
        ],
        resolution_strategy="Conduct transfer impact assessments and update SCCs.",
        entity_scope="Organizations transferring personal data outside EU/EEA",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="CJEU Schrems II Decision"
    ),
    DoctrineBlock(
        topic="GDPR Right to Restrict Processing",
        keywords=["GDPR", "restrict processing", "data subject rights", "personal data", "EU"],
        conclusion_template="Data subjects may request restriction of processing of their personal data under the GDPR.",
        reasoning_framework=(
            "The GDPR allows data subjects to request restriction of processing where the accuracy of data is contested, processing is unlawful, or the controller no longer needs the data but the data subject requires it for legal claims. "
            "Controllers must mark restricted data and inform recipients. "
            "Restriction may be lifted under certain conditions."
        ),
        key_factors=[
            "Grounds for restriction",
            "Notification to recipients",
            "Marking of restricted data",
            "Conditions for lifting restriction"
        ],
        primary_authority=["GDPR Art. 18"],
        burden_holder="Data Controller",
        adversary_position="Controller may argue restriction not applicable.",
        counter_arguments=[
            "Grounds for restriction met",
            "Controller fails to mark data",
            "Notification obligations not met"
        ],
        resolution_strategy="Implement restriction procedures and maintain records.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Data Subject Rights"
    ),
    DoctrineBlock(
        topic="GDPR Right to Object to Processing",
        keywords=["GDPR", "object", "processing", "data subject rights", "personal data", "EU"],
        conclusion_template="Data subjects may object to processing of their personal data under the GDPR, particularly for direct marketing.",
        reasoning_framework=(
            "The GDPR grants data subjects the right to object to processing of their personal data based on legitimate interests or for direct marketing purposes. "
            "Controllers must cease processing unless they demonstrate compelling legitimate grounds. "
            "For direct marketing, the right to object is absolute."
        ),
        key_factors=[
            "Grounds for objection",
            "Controller response",
            "Direct marketing",
            "Compelling legitimate interests"
        ],
        primary_authority=["GDPR Art. 21"],
        burden_holder="Data Controller",
        adversary_position="Controller may argue legitimate grounds.",
        counter_arguments=[
            "Objection is valid",
            "Controller fails to cease processing",
            "No compelling grounds"
        ],
        resolution_strategy="Review processing activities and update procedures.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Data Subject Rights"
    ),
    DoctrineBlock(
        topic="GDPR Automated Decision-Making and Profiling",
        keywords=["GDPR", "automated decision-making", "profiling", "data subject rights", "personal data", "EU"],
        conclusion_template="Data subjects have the right not to be subject to decisions based solely on automated processing under the GDPR.",
        reasoning_framework=(
            "The GDPR restricts decisions based solely on automated processing, including profiling, that produce legal or similarly significant effects. "
            "Data subjects must be informed of such processing and have the right to request human intervention, express their views, and contest the decision. "
            "Exceptions apply where processing is necessary for contract, authorized by law, or based on explicit consent."
        ),
        key_factors=[
            "Nature of automated processing",
            "Notification to data subjects",
            "Human intervention",
            "Applicability of exceptions"
        ],
        primary_authority=["GDPR Art. 22"],
        burden_holder="Data Controller",
        adversary_position="Controller may argue exception applies.",
        counter_arguments=[
            "Processing is solely automated",
            "No human intervention",
            "No explicit consent"
        ],
        resolution_strategy="Implement procedures for human review and inform data subjects.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Automated Decision-Making"
    ),
    DoctrineBlock(
        topic="GDPR Transparency and Information Requirements",
        keywords=["GDPR", "transparency", "information requirements", "privacy notice", "personal data", "EU"],
        conclusion_template="Controllers must provide clear and comprehensive information to data subjects about processing activities under the GDPR.",
        reasoning_framework=(
            "The GDPR mandates transparency in processing activities, requiring controllers to provide data subjects with information about the purposes, legal basis, recipients, retention periods, and rights. "
            "Privacy notices must be concise, intelligible, and easily accessible. "
            "Controllers must update notices as practices change and ensure data subjects are informed."
        ),
        key_factors=[
            "Clarity and accessibility of notice",
            "Scope of information",
            "Timeliness of updates",
            "Compliance with EDPB guidance"
        ],
        primary_authority=["GDPR Art. 12-14"],
        burden_holder="Data Controller",
        adversary_position="Controller may argue notice is sufficient.",
        counter_arguments=[
            "Notice is unclear",
            "Information incomplete",
            "Failure to update"
        ],
        resolution_strategy="Review privacy notices regularly and train staff.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Transparency"
    ),
    DoctrineBlock(
        topic="GDPR Security of Processing",
        keywords=["GDPR", "security", "processing", "personal data", "EU"],
        conclusion_template="Controllers and processors must implement appropriate security measures to protect personal data under the GDPR.",
        reasoning_framework=(
            "The GDPR requires controllers and processors to implement technical and organizational measures to ensure a level of security appropriate to the risk. "
            "Measures may include encryption, pseudonymization, access controls, and regular testing. "
            "Security incidents must be documented and reported as required."
        ),
        key_factors=[
            "Risk assessment",
            "Technical and organizational measures",
            "Incident response",
            "Documentation"
        ],
        primary_authority=["GDPR Art. 32"],
        burden_holder="Controller/Processor",
        adversary_position="Controller may argue measures are sufficient.",
        counter_arguments=[
            "Measures inadequate",
            "Risk assessment not conducted",
            "Incident response insufficient"
        ],
        resolution_strategy="Conduct regular security reviews and update controls.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Security"
    ),
    DoctrineBlock(
        topic="GDPR Data Breach Notification",
        keywords=["GDPR", "data breach", "notification", "personal data", "EU"],
        conclusion_template="Controllers must notify supervisory authorities and affected data subjects of personal data breaches under the GDPR.",
        reasoning_framework=(
            "The GDPR requires controllers to notify the supervisory authority within 72 hours of becoming aware of a personal data breach, unless the breach is unlikely to result in risk to data subjects. "
            "Affected data subjects must be notified without undue delay if the breach is likely to result in high risk. "
            "Notifications must include details of the breach, mitigation measures, and contact information."
        ),
        key_factors=[
            "Timeliness of notification",
            "Content of notification",
            "Risk assessment",
            "Mitigation measures"
        ],
        primary_authority=["GDPR Art. 33-34"],
        burden_holder="Data Controller",
        adversary_position="Controller may argue breach does not require notification.",
        counter_arguments=[
            "Risk to data subjects",
            "Delay in notification",
            "Incomplete notification"
        ],
        resolution_strategy="Develop incident response plans and train staff.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Breach Notification"
    ),
    DoctrineBlock(
        topic="GDPR Records of Processing Activities",
        keywords=["GDPR", "records", "processing activities", "documentation", "personal data", "EU"],
        conclusion_template="Controllers and processors must maintain records of processing activities under the GDPR.",
        reasoning_framework=(
            "The GDPR requires controllers and processors to document processing activities, including purposes, categories of data, recipients, transfers, and security measures. "
            "Records must be available to supervisory authorities upon request. "
            "Small organizations may be exempt unless processing is high-risk."
        ),
        key_factors=[
            "Scope of records",
            "Availability to authorities",
            "Exemptions",
            "Documentation procedures"
        ],
        primary_authority=["GDPR Art. 30"],
        burden_holder="Controller/Processor",
        adversary_position="Controller may argue exemption applies.",
        counter_arguments=[
            "Processing is high-risk",
            "Records not maintained",
            "Authorities denied access"
        ],
        resolution_strategy="Maintain up-to-date records and review exemptions.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Documentation"
    ),
    DoctrineBlock(
        topic="GDPR Appointment of Data Protection Officer (DPO)",
        keywords=["GDPR", "DPO", "data protection officer", "personal data", "EU"],
        conclusion_template="Controllers and processors must appoint a Data Protection Officer under the GDPR if processing is large-scale or involves sensitive data.",
        reasoning_framework=(
            "The GDPR requires appointment of a DPO where processing is carried out by a public authority, involves large-scale monitoring, or processing of special categories of data. "
            "The DPO must be independent, have expert knowledge, and report to senior management. "
            "Contact details must be provided to data subjects and supervisory authorities."
        ),
        key_factors=[
            "Scope of processing",
            "Expertise of DPO",
            "Independence",
            "Notification to authorities"
        ],
        primary_authority=["GDPR Art. 37-39"],
        burden_holder="Controller/Processor",
        adversary_position="Controller may argue DPO not required.",
        counter_arguments=[
            "Processing meets criteria",
            "DPO lacks independence",
            "Contact details not provided"
        ],
        resolution_strategy="Assess processing activities and appoint qualified DPO.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on DPOs"
    ),
    DoctrineBlock(
        topic="GDPR Children's Data and Consent",
        keywords=["GDPR", "children", "consent", "personal data", "EU"],
        conclusion_template="Processing personal data of children under the GDPR requires parental consent for those under 16 (or lower age set by member state).",
        reasoning_framework=(
            "The GDPR requires parental consent for processing personal data of children under 16, with member states permitted to lower the age to 13. "
            "Controllers must implement mechanisms to verify age and obtain parental consent. "
            "Privacy notices must be tailored to children and parents."
        ),
        key_factors=[
            "Age verification",
            "Parental consent",
            "Tailored privacy notice",
            "Compliance with member state law"
        ],
        primary_authority=["GDPR Art. 8"],
        burden_holder="Data Controller",
        adversary_position="Controller may argue consent obtained or not required.",
        counter_arguments=[
            "Consent not verifiable",
            "Notice not tailored",
            "Age verification inadequate"
        ],
        resolution_strategy="Implement age verification and consent procedures.",
        entity_scope="Organizations processing personal data of children in the EU",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Children's Data"
    ),
    DoctrineBlock(
        topic="GDPR Special Categories of Data",
        keywords=["GDPR", "special categories", "sensitive data", "processing", "personal data", "EU"],
        conclusion_template="Processing special categories of personal data under the GDPR requires explicit consent or other specific grounds.",
        reasoning_framework=(
            "The GDPR prohibits processing of special categories of personal data, such as racial or ethnic origin, health, or sexual orientation, unless explicit consent is obtained or another ground applies. "
            "Controllers must implement additional safeguards and document the basis for processing."
        ),
        key_factors=[
            "Explicit consent",
            "Grounds for processing",
            "Safeguards",
            "Documentation"
        ],
        primary_authority=["GDPR Art. 9"],
        burden_holder="Data Controller",
        adversary_position="Controller may argue ground applies.",
        counter_arguments=[
            "Consent not explicit",
            "Safeguards inadequate",
            "Documentation insufficient"
        ],
        resolution_strategy="Review processing activities and update safeguards.",
        entity_scope="Organizations processing special categories of data in the EU",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Special Categories"
    ),
    DoctrineBlock(
        topic="GDPR Data Retention and Storage Limitation",
        keywords=["GDPR", "data retention", "storage limitation", "personal data", "EU"],
        conclusion_template="Personal data must not be retained longer than necessary for the purpose under the GDPR.",
        reasoning_framework=(
            "The GDPR requires controllers to ensure personal data is not retained longer than necessary for the purposes for which it was collected. "
            "Retention periods must be documented and data securely deleted when no longer needed. "
            "Exceptions apply for legal obligations and archiving in the public interest."
        ),
        key_factors=[
            "Purpose specification",
            "Retention period documentation",
            "Secure deletion",
            "Applicability of exceptions"
        ],
        primary_authority=["GDPR Art. 5(1)(e)"],
        burden_holder="Data Controller",
        adversary_position="Controller may argue retention is justified.",
        counter_arguments=[
            "Retention exceeds necessity",
            "Documentation absent",
            "Deletion not secure"
        ],
        resolution_strategy="Establish retention policies and conduct periodic reviews.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Storage Limitation"
    ),
    DoctrineBlock(
        topic="GDPR Accountability Principle",
        keywords=["GDPR", "accountability", "principle", "personal data", "EU"],
        conclusion_template="Controllers must demonstrate compliance with GDPR principles and obligations.",
        reasoning_framework=(
            "The GDPR requires controllers to implement measures and be able to demonstrate compliance with all data protection principles and obligations. "
            "This includes documentation, training, regular reviews, and cooperation with supervisory authorities."
        ),
        key_factors=[
            "Documentation",
            "Training",
            "Review procedures",
            "Cooperation with authorities"
        ],
        primary_authority=["GDPR Art. 5(2)"],
        burden_holder="Data Controller",
        adversary_position="Controller may argue compliance is demonstrated.",
        counter_arguments=[
            "Documentation inadequate",
            "Training insufficient",
            "Review procedures absent"
        ],
        resolution_strategy="Maintain comprehensive records and conduct regular audits.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Accountability"
    ),
    DoctrineBlock(
        topic="GDPR Privacy by Design and Default",
        keywords=["GDPR", "privacy by design", "privacy by default", "personal data", "EU"],
        conclusion_template="Controllers must implement privacy by design and default in processing activities under the GDPR.",
        reasoning_framework=(
            "The GDPR requires controllers to integrate data protection into processing activities and systems from the outset (privacy by design) and ensure only necessary personal data is processed by default. "
            "Measures include minimization, pseudonymization, and access controls."
        ),
        key_factors=[
            "Integration of privacy measures",
            "Default settings",
            "Minimization",
            "Access controls"
        ],
        primary_authority=["GDPR Art. 25"],
        burden_holder="Data Controller",
        adversary_position="Controller may argue measures are sufficient.",
        counter_arguments=[
            "Measures not integrated",
            "Defaults not privacy-friendly",
            "Minimization absent"
        ],
        resolution_strategy="Review system design and update controls.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Privacy by Design"
    ),
    DoctrineBlock(
        topic="GDPR Supervisory Authority Powers",
        keywords=["GDPR", "supervisory authority", "powers", "enforcement", "personal data", "EU"],
        conclusion_template="Supervisory authorities have broad enforcement powers under the GDPR, including investigation, fines, and orders.",
        reasoning_framework=(
            "The GDPR grants supervisory authorities the power to investigate, issue warnings, impose fines, and order cessation of processing. "
            "Authorities may cooperate across member states and issue binding decisions."
        ),
        key_factors=[
            "Scope of powers",
            "Cooperation",
            "Binding decisions",
            "Enforcement procedures"
        ],
        primary_authority=["GDPR Art. 58"],
        burden_holder="Supervisory Authority",
        adversary_position="Controller may challenge authority actions.",
        counter_arguments=[
            "Authority exceeds powers",
            "Procedures not followed",
            "Decisions not binding"
        ],
        resolution_strategy="Engage with authorities and seek legal review.",
        entity_scope="Supervisory authorities in the EU",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Enforcement"
    ),
    DoctrineBlock(
        topic="GDPR Remedies and Liability",
        keywords=["GDPR", "remedies", "liability", "damages", "personal data", "EU"],
        conclusion_template="Data subjects have the right to seek remedies and compensation for GDPR violations.",
        reasoning_framework=(
            "The GDPR provides data subjects the right to lodge complaints, seek judicial remedies, and obtain compensation for material or non-material damage resulting from violations. "
            "Controllers and processors may be jointly liable."
        ),
        key_factors=[
            "Right to complaint",
            "Judicial remedies",
            "Compensation",
            "Joint liability"
        ],
        primary_authority=["GDPR Art. 77-82"],
        burden_holder="Controller/Processor",
        adversary_position="Controller may argue no damage or liability.",
        counter_arguments=[
            "Damage demonstrated",
            "Controller responsible",
            "Joint liability applies"
        ],
        resolution_strategy="Maintain compliance and respond to complaints promptly.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Remedies"
    ),
    DoctrineBlock(
        topic="GDPR International Cooperation",
        keywords=["GDPR", "international cooperation", "supervisory authority", "personal data", "EU"],
        conclusion_template="Supervisory authorities must cooperate internationally to ensure consistent GDPR enforcement.",
        reasoning_framework=(
            "The GDPR requires supervisory authorities to cooperate with each other and with international counterparts to ensure consistent enforcement and protection of data subjects' rights. "
            "Mechanisms include mutual assistance, joint operations, and information sharing."
        ),
        key_factors=[
            "Mutual assistance",
            "Joint operations",
            "Information sharing",
            "Consistency"
        ],
        primary_authority=["GDPR Art. 60-63"],
        burden_holder="Supervisory Authority",
        adversary_position="Controller may challenge cooperation outcomes.",
        counter_arguments=[
            "Cooperation not effective",
            "Inconsistent enforcement",
            "Information sharing inadequate"
        ],
        resolution_strategy="Engage in international forums and update procedures.",
        entity_scope="Supervisory authorities in the EU",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Cooperation"
    ),
    DoctrineBlock(
        topic="GDPR Right to Withdraw Consent",
        keywords=["GDPR", "withdraw consent", "data subject rights", "personal data", "EU"],
        conclusion_template="Data subjects may withdraw consent for processing personal data at any time under the GDPR.",
        reasoning_framework=(
            "The GDPR allows data subjects to withdraw consent at any time, and controllers must cease processing unless another lawful basis applies. "
            "Withdrawal must be as easy as giving consent."
        ),
        key_factors=[
            "Ease of withdrawal",
            "Alternative lawful basis",
            "Controller response",
            "Notification to data subjects"
        ],
        primary_authority=["GDPR Art. 7"],
        burden_holder="Data Controller",
        adversary_position="Controller may argue alternative basis applies.",
        counter_arguments=[
            "Withdrawal not honored",
            "No alternative basis",
            "Withdrawal process difficult"
        ],
        resolution_strategy="Implement easy withdrawal mechanisms and update records.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Consent"
    ),
    DoctrineBlock(
        topic="GDPR Right to Lodge Complaint",
        keywords=["GDPR", "complaint", "data subject rights", "supervisory authority", "personal data", "EU"],
        conclusion_template="Data subjects may lodge complaints with supervisory authorities under the GDPR.",
        reasoning_framework=(
            "The GDPR provides data subjects the right to lodge complaints with supervisory authorities regarding violations of their rights. "
            "Authorities must investigate and provide remedies."
        ),
        key_factors=[
            "Right to complaint",
            "Investigation",
            "Remedies",
            "Notification"
        ],
        primary_authority=["GDPR Art. 77"],
        burden_holder="Data Subject",
        adversary_position="Controller may argue complaint unfounded.",
        counter_arguments=[
            "Complaint is valid",
            "Violation demonstrated",
            "Remedies not provided"
        ],
        resolution_strategy="Engage with authorities and respond promptly.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Remedies"
    ),
    DoctrineBlock(
        topic="GDPR Right to Judicial Remedy",
        keywords=["GDPR", "judicial remedy", "data subject rights", "personal data", "EU"],
        conclusion_template="Data subjects may seek judicial remedies for GDPR violations.",
        reasoning_framework=(
            "The GDPR allows data subjects to seek judicial remedies in national courts for violations of their rights. "
            "Courts may grant compensation and orders to cease processing."
        ),
        key_factors=[
            "Access to courts",
            "Compensation",
            "Orders to cease processing",
            "Jurisdiction"
        ],
        primary_authority=["GDPR Art. 79-82"],
        burden_holder="Data Subject",
        adversary_position="Controller may argue no violation.",
        counter_arguments=[
            "Violation demonstrated",
            "Compensation justified",
            "Jurisdiction established"
        ],
        resolution_strategy="Consult legal counsel and pursue remedies.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Remedies"
    ),
    DoctrineBlock(
        topic="GDPR Right to Compensation",
        keywords=["GDPR", "compensation", "data subject rights", "personal data", "EU"],
        conclusion_template="Data subjects may claim compensation for material or non-material damage resulting from GDPR violations.",
        reasoning_framework=(
            "The GDPR provides data subjects the right to claim compensation for damage caused by violations of the Regulation. "
            "Controllers and processors may be jointly liable."
        ),
        key_factors=[
            "Material and non-material damage",
            "Joint liability",
            "Proof of violation",
            "Compensation procedures"
        ],
        primary_authority=["GDPR Art. 82"],
        burden_holder="Data Subject",
        adversary_position="Controller may argue no damage or liability.",
        counter_arguments=[
            "Damage demonstrated",
            "Controller responsible",
            "Joint liability applies"
        ],
        resolution_strategy="Maintain compliance and respond to claims promptly.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Remedies"
    ),
    DoctrineBlock(
        topic="GDPR Right to Data Portability for Cloud Services",
        keywords=["GDPR", "data portability", "cloud services", "personal data", "EU"],
        conclusion_template="Data subjects may request their personal data from cloud service providers in a portable format under the GDPR.",
        reasoning_framework=(
            "Cloud service providers acting as controllers must provide personal data in a structured, commonly used, and machine-readable format upon request. "
            "Portability applies where processing is based on consent or contract and carried out by automated means."
        ),
        key_factors=[
            "Format of data",
            "Basis for processing",
            "Security of transmission",
            "Applicability of exceptions"
        ],
        primary_authority=["GDPR Art. 20"],
        burden_holder="Cloud Service Provider",
        adversary_position="Provider may argue technical infeasibility.",
        counter_arguments=[
            "Request is valid",
            "Provider has capability",
            "No applicable exception"
        ],
        resolution_strategy="Develop export procedures and secure protocols.",
        entity_scope="Cloud service providers processing personal data in the EU",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Data Portability"
    ),
    DoctrineBlock(
        topic="GDPR Data Protection by Encryption",
        keywords=["GDPR", "encryption", "security", "personal data", "EU"],
        conclusion_template="Controllers and processors must implement encryption as an appropriate security measure under the GDPR.",
        reasoning_framework=(
            "The GDPR recommends encryption as a technical measure to protect personal data, especially for sensitive information and cross-border transfers. "
            "Controllers must assess risks and implement encryption where appropriate."
        ),
        key_factors=[
            "Risk assessment",
            "Implementation of encryption",
            "Applicability to transfers",
            "Documentation"
        ],
        primary_authority=["GDPR Art. 32"],
        burden_holder="Controller/Processor",
        adversary_position="Controller may argue encryption not required.",
        counter_arguments=[
            "Sensitive data processed",
            "Risk assessment favors encryption",
            "Encryption not implemented"
        ],
        resolution_strategy="Conduct risk assessments and update encryption protocols.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Security"
    ),
    DoctrineBlock(
        topic="GDPR Pseudonymization as Security Measure",
        keywords=["GDPR", "pseudonymization", "security", "personal data", "EU"],
        conclusion_template="Controllers and processors should implement pseudonymization to enhance security and privacy under the GDPR.",
        reasoning_framework=(
            "The GDPR encourages pseudonymization as a means to reduce risks and enhance privacy. "
            "Pseudonymization involves processing data so it cannot be attributed to a specific data subject without additional information, which must be kept separately."
        ),
        key_factors=[
            "Implementation of pseudonymization",
            "Separation of identifiers",
            "Risk reduction",
            "Documentation"
        ],
        primary_authority=["GDPR Art. 32", "Art. 4(5)"],
        burden_holder="Controller/Processor",
        adversary_position="Controller may argue pseudonymization not feasible.",
        counter_arguments=[
            "Feasibility demonstrated",
            "Risk reduction necessary",
            "Pseudonymization not implemented"
        ],
        resolution_strategy="Assess feasibility and update protocols.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Security"
    ),
    DoctrineBlock(
        topic="GDPR Data Protection Training Requirements",
        keywords=["GDPR", "training", "data protection", "personal data", "EU"],
        conclusion_template="Controllers and processors must provide regular data protection training to staff under the GDPR.",
        reasoning_framework=(
            "The GDPR requires controllers and processors to ensure staff are trained in data protection principles, security measures, and incident response. "
            "Training must be documented and updated regularly."
        ),
        key_factors=[
            "Scope of training",
            "Documentation",
            "Frequency",
            "Incident response"
        ],
        primary_authority=["GDPR Art. 39"],
        burden_holder="Controller/Processor",
        adversary_position="Controller may argue training is sufficient.",
        counter_arguments=[
            "Training inadequate",
            "Documentation absent",
            "Frequency insufficient"
        ],
        resolution_strategy="Develop training programs and maintain records.",
        entity_scope="Organizations processing personal data in the EU or of EU residents",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Training"
    ),
    DoctrineBlock(
        topic="GDPR Vendor Management and Processor Agreements",
        keywords=["GDPR", "vendor management", "processor agreements", "personal data", "EU"],
        conclusion_template="Controllers must ensure processor agreements comply with GDPR requirements.",
        reasoning_framework=(
            "The GDPR requires controllers to enter into written agreements with processors, specifying instructions, security measures, and obligations. "
            "Controllers must monitor processor compliance and conduct due diligence."
        ),
        key_factors=[
            "Written agreements",
            "Security measures",
            "Monitoring",
            "Due diligence"
        ],
        primary_authority=["GDPR Art. 28"],
        burden_holder="Controller",
        adversary_position="Controller may argue agreement is sufficient.",
        counter_arguments=[
            "Agreement lacks required terms",
            "Security measures inadequate",
            "Monitoring absent"
        ],
        resolution_strategy="Review agreements and conduct audits.",
        entity_scope="Controllers engaging processors in the EU",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Processor Agreements"
    ),
    DoctrineBlock(
        topic="GDPR Data Subject Rights for Employees",
        keywords=["GDPR", "employee", "data subject rights", "personal data", "EU"],
        conclusion_template="Employees have data subject rights under the GDPR, including access, rectification, erasure, and portability.",
        reasoning_framework=(
            "The GDPR applies to employee data, granting rights to access, rectification, erasure, and portability. "
            "Employers must implement procedures to respond to employee requests and document outcomes."
        ),
        key_factors=[
            "Scope of employee data",
            "Procedures for requests",
            "Documentation",
            "Applicability of exceptions"
        ],
        primary_authority=["GDPR Art. 15-20"],
        burden_holder="Employer",
        adversary_position="Employer may argue exception applies.",
        counter_arguments=[
            "Request is valid",
            "Exception not applicable",
            "Procedures absent"
        ],
        resolution_strategy="Develop employee data request procedures and maintain records.",
        entity_scope="Employers processing employee data in the EU",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Employee Data"
    ),
    DoctrineBlock(
        topic="GDPR Legitimate Interests Assessment",
        keywords=["GDPR", "legitimate interests", "assessment", "personal data", "EU"],
        conclusion_template="Controllers must conduct a legitimate interests assessment before processing personal data under this basis.",
        reasoning_framework=(
            "The GDPR requires controllers to conduct a legitimate interests assessment, balancing their interests against the rights and freedoms of data subjects. "
            "Assessment must be documented and reviewed regularly."
        ),
        key_factors=[
            "Balancing test",
            "Documentation",
            "Review procedures",
            "Transparency"
        ],
        primary_authority=["GDPR Art. 6(1)(f)"],
        burden_holder="Controller",
        adversary_position="Controller may argue assessment is sufficient.",
        counter_arguments=[
            "Assessment inadequate",
            "Rights of data subjects prevail",
            "Documentation absent"
        ],
        resolution_strategy="Conduct assessments and update documentation.",
        entity_scope="Controllers processing personal data under legitimate interests in the EU",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="EDPB Guidelines on Legitimate Interests"
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