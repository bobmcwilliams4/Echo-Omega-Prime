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
        topic="McCarran-Ferguson Act Federal Antitrust Exemption",
        keywords=[
            "McCarran-Ferguson", "antitrust", "federal exemption", "insurance regulation", "state law", "competition"
        ],
        conclusion_template="Under the McCarran-Ferguson Act, federal antitrust laws do not apply to the business of insurance to the extent that such business is regulated by state law.",
        reasoning_framework=(
            "The McCarran-Ferguson Act (15 U.S.C. §§ 1011-1015) was enacted to affirm state primacy in regulating the business of insurance. "
            "Federal antitrust laws, including the Sherman Act and Clayton Act, are expressly exempted when state law regulates insurance activities. "
            "The Act applies only to 'the business of insurance,' not to ancillary activities. "
            "Courts analyze whether the conduct constitutes 'the business of insurance,' whether state law regulates the conduct, and whether federal law would impair state regulation. "
            "If all three prongs are satisfied, federal antitrust laws are preempted. "
            "Key factors include the nature of the activity, the existence and scope of state regulation, and the potential for federal law to undermine state regulatory objectives. "
            "Exceptions exist for acts of boycott, coercion, or intimidation. "
            "The burden is on the party claiming exemption to demonstrate state regulation and insurance business involvement. "
            "Adversaries may argue that the conduct is not insurance-related or insufficiently regulated by the state. "
            "Resolution is typically through judicial interpretation of statutory language and regulatory scope. "
            "The doctrine applies to insurers, reinsurers, and insurance-related entities operating within state-regulated frameworks. "
            "Confidence is high due to longstanding precedent and clear statutory language."
        ),
        key_factors=[
            "Nature of activity (business of insurance)",
            "Existence of state regulation",
            "Potential impairment of state law",
            "Acts of boycott/coercion/intimidation"
        ],
        primary_authority=[
            "McCarran-Ferguson Act (15 U.S.C. §§ 1011-1015)",
            "Sherman Act",
            "Clayton Act",
            "United States v. South-Eastern Underwriters Ass'n, 322 U.S. 533 (1944)"
        ],
        burden_holder="Party claiming antitrust exemption",
        adversary_position="Federal antitrust laws should apply due to lack of state regulation or non-insurance activity",
        counter_arguments=[
            "Activity is not the business of insurance",
            "State regulation is insufficient or absent",
            "Federal law does not impair state regulation"
        ],
        resolution_strategy="Judicial interpretation of statutory language and regulatory scope; analysis of state regulatory framework",
        entity_scope="Insurers, reinsurers, insurance-related entities",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. South-Eastern Underwriters Ass'n, 322 U.S. 533 (1944)"
    ),
    DoctrineBlock(
        topic="Texas Rate Filing Prior Approval Requirement",
        keywords=[
            "rate filing", "prior approval", "Texas Insurance Code", "property and casualty", "rate regulation"
        ],
        conclusion_template="Insurers must submit rate filings for property and casualty insurance to the Texas Department of Insurance for prior approval before implementing new rates.",
        reasoning_framework=(
            "Texas Insurance Code mandates that insurers file rates with the Texas Department of Insurance (TDI) for certain lines of property and casualty insurance. "
            "The prior approval system requires TDI to review and approve rates before they become effective. "
            "The review focuses on actuarial justification, adequacy, and non-discrimination. "
            "Insurers must provide supporting data, including loss experience, expense ratios, and trend analyses. "
            "TDI may disapprove rates that are excessive, inadequate, or unfairly discriminatory. "
            "The burden is on the insurer to demonstrate compliance with statutory standards. "
            "Adversaries may argue that rates are excessive or discriminatory. "
            "Resolution involves actuarial review and regulatory determination. "
            "The doctrine applies to admitted insurers writing regulated lines in Texas. "
            "Confidence is high due to clear statutory requirements and established regulatory practice."
        ),
        key_factors=[
            "Actuarial justification",
            "Adequacy of rates",
            "Non-discrimination",
            "Supporting data"
        ],
        primary_authority=[
            "Texas Insurance Code §§ 2251.101-2251.103",
            "Texas Administrative Code Title 28",
            "TDI Rate Filing Guidelines"
        ],
        burden_holder="Insurer submitting rate filing",
        adversary_position="Rates are excessive, inadequate, or unfairly discriminatory",
        counter_arguments=[
            "Rates lack actuarial support",
            "Rates are not competitive",
            "Rates discriminate against certain insureds"
        ],
        resolution_strategy="Actuarial review and regulatory determination by TDI",
        entity_scope="Admitted insurers in Texas",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code §§ 2251.101-2251.103"
    ),
    DoctrineBlock(
        topic="Surplus Lines Eligibility and Tax Code Section 226",
        keywords=[
            "surplus lines", "eligibility", "non-admitted insurer", "tax code", "Section 226", "premium tax"
        ],
        conclusion_template="Surplus lines insurers must meet eligibility requirements under Texas law, and surplus lines premiums are subject to tax under Texas Tax Code Section 226.",
        reasoning_framework=(
            "Surplus lines insurance provides coverage through non-admitted insurers for risks not available from admitted carriers. "
            "Eligibility is governed by Texas Insurance Code Chapter 981 and Texas Administrative Code. "
            "Insurers must be listed on the Texas Surplus Lines Insurer List or meet NAIC requirements. "
            "Surplus lines brokers must ensure eligibility before placement. "
            "Premiums are subject to a surplus lines premium tax under Texas Tax Code Section 226, typically collected by the broker and remitted to the state. "
            "Key factors include insurer eligibility, proper placement procedures, and tax remittance. "
            "The burden is on the broker to verify eligibility and comply with tax requirements. "
            "Adversaries may claim improper placement or tax evasion. "
            "Resolution involves regulatory audits and enforcement actions. "
            "The doctrine applies to surplus lines brokers, non-admitted insurers, and insureds seeking coverage outside the admitted market. "
            "Confidence is high due to clear statutory and regulatory guidance."
        ),
        key_factors=[
            "Insurer eligibility",
            "Broker compliance",
            "Premium tax remittance",
            "Proper placement procedures"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 981",
            "Texas Administrative Code Title 28",
            "Texas Tax Code Section 226"
        ],
        burden_holder="Surplus lines broker",
        adversary_position="Placement with ineligible insurer or failure to remit tax",
        counter_arguments=[
            "Insurer not listed or fails NAIC requirements",
            "Broker failed to remit premium tax",
            "Improper placement procedures"
        ],
        resolution_strategy="Regulatory audit and enforcement by TDI and Comptroller",
        entity_scope="Surplus lines brokers, non-admitted insurers",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 981"
    ),
    DoctrineBlock(
        topic="Risk-Based Capital (RBC) Requirements and Solvency Monitoring",
        keywords=[
            "risk-based capital", "RBC", "solvency", "capital adequacy", "NAIC", "regulatory monitoring"
        ],
        conclusion_template="Insurers must maintain risk-based capital levels in accordance with NAIC standards and Texas law to ensure solvency and regulatory compliance.",
        reasoning_framework=(
            "Risk-Based Capital (RBC) requirements are designed to ensure insurers maintain adequate capital relative to their risk profile. "
            "The NAIC RBC formula considers asset risk, underwriting risk, credit risk, and operational risk. "
            "Texas Insurance Code and NAIC Model Laws require annual RBC reporting and regulatory monitoring. "
            "Insurers falling below RBC thresholds are subject to regulatory intervention, including corrective action plans, supervision, or receivership. "
            "Key factors include RBC ratio, risk exposure, and compliance with reporting requirements. "
            "The burden is on the insurer to maintain adequate capital and submit accurate RBC reports. "
            "Adversaries may argue insufficient capital or inaccurate reporting. "
            "Resolution involves regulatory review, actuarial analysis, and enforcement actions. "
            "The doctrine applies to admitted insurers, health carriers, and certain reinsurers. "
            "Confidence is high due to uniform adoption and established regulatory practice."
        ),
        key_factors=[
            "RBC ratio",
            "Risk exposure",
            "Reporting compliance",
            "Regulatory intervention"
        ],
        primary_authority=[
            "NAIC Risk-Based Capital Model Law",
            "Texas Insurance Code Chapter 441",
            "NAIC RBC Instructions"
        ],
        burden_holder="Insurer",
        adversary_position="Insufficient capital or inaccurate RBC reporting",
        counter_arguments=[
            "RBC calculation errors",
            "Failure to report",
            "Inadequate corrective action"
        ],
        resolution_strategy="Regulatory review, actuarial analysis, and enforcement actions",
        entity_scope="Admitted insurers, health carriers, reinsurers",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NAIC Risk-Based Capital Model Law"
    ),
    DoctrineBlock(
        topic="Market Conduct Examinations and NAIC Market Regulation Handbook",
        keywords=[
            "market conduct", "examination", "NAIC", "regulatory compliance", "handbook", "consumer protection"
        ],
        conclusion_template="Insurers are subject to market conduct examinations under the NAIC Market Regulation Handbook to ensure compliance with consumer protection and regulatory standards.",
        reasoning_framework=(
            "Market conduct examinations are performed by state insurance departments to assess insurer compliance with laws, regulations, and consumer protection standards. "
            "The NAIC Market Regulation Handbook provides uniform procedures for examinations, including planning, data collection, interviews, and reporting. "
            "Examinations focus on claims handling, underwriting, marketing, producer licensing, and complaint resolution. "
            "Key factors include examination scope, insurer cooperation, and findings. "
            "The burden is on the insurer to demonstrate compliance and provide requested information. "
            "Adversaries may allege violations or non-cooperation. "
            "Resolution involves corrective action, fines, or license suspension. "
            "The doctrine applies to admitted insurers, producers, and affiliated entities. "
            "Confidence is high due to widespread adoption and regulatory consistency."
        ),
        key_factors=[
            "Examination scope",
            "Insurer cooperation",
            "Findings and corrective action",
            "Consumer protection"
        ],
        primary_authority=[
            "NAIC Market Regulation Handbook",
            "Texas Insurance Code Chapter 38",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Non-compliance or violation of regulatory standards",
        counter_arguments=[
            "Failure to cooperate",
            "Violation of consumer protection laws",
            "Inadequate corrective action"
        ],
        resolution_strategy="Regulatory enforcement, corrective action, and reporting",
        entity_scope="Admitted insurers, producers, affiliated entities",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NAIC Market Regulation Handbook"
    ),
    DoctrineBlock(
        topic="Unfair Claims Settlement Practices Act (UCSPA)",
        keywords=[
            "UCSPA", "unfair claims", "settlement practices", "claims handling", "consumer protection", "bad faith"
        ],
        conclusion_template="Insurers must comply with the Unfair Claims Settlement Practices Act, prohibiting unfair or deceptive claims handling practices.",
        reasoning_framework=(
            "The Unfair Claims Settlement Practices Act (UCSPA) prohibits insurers from engaging in unfair, deceptive, or bad faith claims handling. "
            "Prohibited practices include misrepresentation, failure to promptly investigate, denial without reasonable basis, and failure to pay claims timely. "
            "State insurance departments enforce UCSPA through market conduct examinations and consumer complaints. "
            "Key factors include claims processing timelines, communication, and justification for denial. "
            "The burden is on the insurer to demonstrate fair and prompt claims handling. "
            "Adversaries may allege bad faith or deceptive practices. "
            "Resolution involves regulatory enforcement, fines, and possible civil liability. "
            "The doctrine applies to admitted insurers, claims adjusters, and affiliated entities. "
            "Confidence is high due to uniform adoption and strong consumer protection focus."
        ),
        key_factors=[
            "Claims processing timelines",
            "Communication with insured",
            "Justification for denial",
            "Prompt payment"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 542",
            "NAIC Unfair Claims Settlement Practices Model Act",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Bad faith or deceptive claims handling",
        counter_arguments=[
            "Failure to investigate",
            "Unreasonable denial",
            "Delayed payment"
        ],
        resolution_strategy="Regulatory enforcement, fines, and civil liability",
        entity_scope="Admitted insurers, claims adjusters",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NAIC Unfair Claims Settlement Practices Model Act"
    ),
    DoctrineBlock(
        topic="Producer Licensing and Appointment Requirements",
        keywords=[
            "producer licensing", "appointment", "agent", "broker", "Texas Insurance Code", "regulatory compliance"
        ],
        conclusion_template="Insurance producers must be licensed and appointed in Texas before soliciting or selling insurance products.",
        reasoning_framework=(
            "Texas Insurance Code requires all insurance producers, including agents and brokers, to obtain a license and appointment from the Texas Department of Insurance (TDI). "
            "Licensing requires completion of pre-licensing education, passing an examination, and background checks. "
            "Appointment by an insurer is necessary to solicit or sell products on behalf of that insurer. "
            "Key factors include licensing status, appointment documentation, and compliance with continuing education. "
            "The burden is on the producer to maintain licensure and appointment. "
            "Adversaries may allege unlicensed activity or improper solicitation. "
            "Resolution involves regulatory enforcement, fines, and license suspension or revocation. "
            "The doctrine applies to agents, brokers, and affiliated entities. "
            "Confidence is high due to clear statutory requirements and regulatory oversight."
        ),
        key_factors=[
            "Licensing status",
            "Appointment documentation",
            "Continuing education compliance",
            "Background checks"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 4001",
            "Texas Administrative Code Title 28",
            "NAIC Producer Licensing Model Act"
        ],
        burden_holder="Producer",
        adversary_position="Unlicensed activity or improper solicitation",
        counter_arguments=[
            "Failure to obtain license",
            "No appointment by insurer",
            "Non-compliance with continuing education"
        ],
        resolution_strategy="Regulatory enforcement, fines, license suspension or revocation",
        entity_scope="Agents, brokers, affiliated entities",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NAIC Producer Licensing Model Act"
    ),
    DoctrineBlock(
        topic="Texas Guaranty Association Coverage and Assessments",
        keywords=[
            "guaranty association", "coverage", "assessment", "insolvency", "Texas Insurance Code", "policyholder protection"
        ],
        conclusion_template="Texas Guaranty Association provides coverage for policyholders of insolvent insurers and assesses member insurers to fund claims.",
        reasoning_framework=(
            "The Texas Property and Casualty Insurance Guaranty Association (TPCIGA) protects policyholders of insolvent insurers by covering unpaid claims, subject to statutory limits. "
            "Member insurers are assessed to fund the association's obligations. "
            "Coverage is limited to certain lines and amounts, and excludes surplus lines and certain large risks. "
            "Key factors include insolvency determination, coverage eligibility, and assessment calculation. "
            "The burden is on the association to pay covered claims and on member insurers to pay assessments. "
            "Adversaries may dispute coverage eligibility or assessment amounts. "
            "Resolution involves statutory interpretation and regulatory oversight. "
            "The doctrine applies to admitted insurers, policyholders, and the association. "
            "Confidence is high due to statutory clarity and established practice."
        ),
        key_factors=[
            "Insolvency determination",
            "Coverage eligibility",
            "Assessment calculation",
            "Statutory limits"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 462",
            "TPCIGA Bylaws",
            "NAIC Life and Health Insurance Guaranty Association Model Act"
        ],
        burden_holder="Guaranty association and member insurers",
        adversary_position="Dispute over coverage eligibility or assessment",
        counter_arguments=[
            "Claim exceeds statutory limits",
            "Policy not covered",
            "Assessment calculation error"
        ],
        resolution_strategy="Statutory interpretation and regulatory oversight",
        entity_scope="Admitted insurers, policyholders, association",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 462"
    ),
    DoctrineBlock(
        topic="Form Approval and Policy Language Requirements",
        keywords=[
            "form approval", "policy language", "Texas Insurance Code", "regulatory compliance", "policy forms"
        ],
        conclusion_template="Insurance policy forms must be submitted to the Texas Department of Insurance for approval and comply with statutory language requirements.",
        reasoning_framework=(
            "Texas Insurance Code requires insurers to submit policy forms for approval prior to use. "
            "Forms must comply with statutory language requirements, including clarity, coverage definitions, and exclusions. "
            "TDI reviews forms for compliance, consumer protection, and avoidance of ambiguity. "
            "Key factors include form submission, statutory compliance, and approval status. "
            "The burden is on the insurer to submit compliant forms and obtain approval. "
            "Adversaries may allege ambiguous or non-compliant language. "
            "Resolution involves regulatory review and possible revision or disapproval. "
            "The doctrine applies to admitted insurers and regulated lines. "
            "Confidence is high due to clear statutory requirements and regulatory oversight."
        ),
        key_factors=[
            "Form submission",
            "Statutory compliance",
            "Approval status",
            "Clarity and avoidance of ambiguity"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 2301",
            "Texas Administrative Code Title 28",
            "NAIC Model Laws"
        ],
        burden_holder="Insurer",
        adversary_position="Ambiguous or non-compliant policy language",
        counter_arguments=[
            "Failure to submit form",
            "Non-compliance with statutory language",
            "Ambiguity in coverage definitions"
        ],
        resolution_strategy="Regulatory review, revision, or disapproval",
        entity_scope="Admitted insurers, regulated lines",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 2301"
    ),
    DoctrineBlock(
        topic="Reinsurance Credit and Unauthorized Reinsurer Collateral Requirements",
        keywords=[
            "reinsurance credit", "unauthorized reinsurer", "collateral", "Texas Insurance Code", "NAIC Model Law"
        ],
        conclusion_template="Insurers may take credit for reinsurance only if the reinsurer meets authorization or collateral requirements under Texas law.",
        reasoning_framework=(
            "Texas Insurance Code and NAIC Model Laws govern the circumstances under which insurers may take credit for reinsurance. "
            "Authorized reinsurers are licensed or accredited in Texas. "
            "Credit for reinsurance from unauthorized reinsurers is permitted only if collateral is posted, typically in the form of a trust or letter of credit. "
            "Key factors include reinsurer status, collateral adequacy, and compliance with reporting requirements. "
            "The burden is on the ceding insurer to ensure compliance and proper documentation. "
            "Adversaries may allege insufficient collateral or unauthorized status. "
            "Resolution involves regulatory review and possible disallowance of credit. "
            "The doctrine applies to insurers, reinsurers, and affiliated entities. "
            "Confidence is high due to uniform adoption and regulatory oversight."
        ),
        key_factors=[
            "Reinsurer authorization",
            "Collateral adequacy",
            "Reporting compliance",
            "Documentation"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 493",
            "NAIC Credit for Reinsurance Model Law",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Ceding insurer",
        adversary_position="Insufficient collateral or unauthorized reinsurer",
        counter_arguments=[
            "Reinsurer not authorized",
            "Collateral is inadequate",
            "Failure to report"
        ],
        resolution_strategy="Regulatory review and disallowance of credit",
        entity_scope="Insurers, reinsurers, affiliated entities",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NAIC Credit for Reinsurance Model Law"
    ),
    DoctrineBlock(
        topic="NAIC Model Laws and Uniform State Adoption",
        keywords=[
            "NAIC Model Laws", "uniform adoption", "state insurance regulation", "model act", "regulatory harmonization"
        ],
        conclusion_template="NAIC Model Laws serve as templates for state insurance regulation, promoting uniformity and harmonization across jurisdictions.",
        reasoning_framework=(
            "The National Association of Insurance Commissioners (NAIC) develops Model Laws to guide state insurance regulation. "
            "States may adopt Model Laws verbatim, with modifications, or not at all. "
            "Uniform adoption promotes regulatory harmonization, facilitates interstate commerce, and supports solvency standards. "
            "Key factors include state adoption status, modifications, and impact on regulatory consistency. "
            "The burden is on state legislatures and regulators to adopt and implement Model Laws. "
            "Adversaries may argue for state-specific requirements or challenge uniformity. "
            "Resolution involves legislative action and regulatory interpretation. "
            "The doctrine applies to state insurance departments, insurers, and affiliated entities. "
            "Confidence is high due to widespread adoption and NAIC leadership."
        ),
        key_factors=[
            "State adoption status",
            "Modifications to Model Laws",
            "Regulatory consistency",
            "Interstate commerce impact"
        ],
        primary_authority=[
            "NAIC Model Laws",
            "Texas Insurance Code",
            "Texas Administrative Code"
        ],
        burden_holder="State legislatures and regulators",
        adversary_position="State-specific requirements or challenge to uniformity",
        counter_arguments=[
            "Model Law does not address local needs",
            "State modifications undermine uniformity",
            "Regulatory gaps"
        ],
        resolution_strategy="Legislative action and regulatory interpretation",
        entity_scope="State insurance departments, insurers",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NAIC Model Laws"
    ),
    DoctrineBlock(
        topic="Insurance Holding Company System and Form B/C/D/E Filings",
        keywords=[
            "holding company", "Form B", "Form C", "Form D", "Form E", "insurance group", "regulatory filings"
        ],
        conclusion_template="Insurers within holding company systems must file Forms B, C, D, and E with the Texas Department of Insurance to disclose ownership, transactions, and enterprise risk.",
        reasoning_framework=(
            "Texas Insurance Code and NAIC Insurance Holding Company System Regulatory Act require insurers within holding company systems to file periodic disclosures. "
            "Form B discloses ownership and organizational structure. "
            "Form C reports material transactions. "
            "Form D covers prior approval of extraordinary transactions. "
            "Form E assesses enterprise risk. "
            "Key factors include completeness, accuracy, and timeliness of filings. "
            "The burden is on the insurer to submit required forms and disclose material information. "
            "Adversaries may allege nondisclosure or inaccurate reporting. "
            "Resolution involves regulatory review, corrective action, and possible enforcement. "
            "The doctrine applies to insurers, holding companies, and affiliates. "
            "Confidence is high due to statutory clarity and regulatory oversight."
        ),
        key_factors=[
            "Completeness of filings",
            "Accuracy of disclosures",
            "Timeliness",
            "Enterprise risk assessment"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 823",
            "NAIC Insurance Holding Company System Regulatory Act",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer within holding company system",
        adversary_position="Nondisclosure or inaccurate reporting",
        counter_arguments=[
            "Incomplete filings",
            "Failure to disclose material transactions",
            "Inaccurate enterprise risk assessment"
        ],
        resolution_strategy="Regulatory review, corrective action, enforcement",
        entity_scope="Insurers, holding companies, affiliates",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NAIC Insurance Holding Company System Regulatory Act"
    ),
    DoctrineBlock(
        topic="Rebating Prohibition and Permitted Inducements",
        keywords=[
            "rebating", "inducements", "Texas Insurance Code", "prohibition", "insurance sales", "consumer protection"
        ],
        conclusion_template="Texas law prohibits rebating in insurance sales, but permits certain inducements as specified by statute.",
        reasoning_framework=(
            "Rebating refers to the return of part of the premium or other inducements not specified in the policy, prohibited under Texas Insurance Code. "
            "Permitted inducements include promotional items of nominal value, charitable donations, and certain wellness benefits. "
            "Key factors include the nature and value of inducement, statutory exceptions, and disclosure. "
            "The burden is on the producer or insurer to comply with rebating prohibitions and document permitted inducements. "
            "Adversaries may allege improper rebating or violation of consumer protection laws. "
            "Resolution involves regulatory review and enforcement. "
            "The doctrine applies to producers, insurers, and affiliated entities. "
            "Confidence is high due to statutory clarity and regulatory oversight."
        ),
        key_factors=[
            "Nature and value of inducement",
            "Statutory exceptions",
            "Disclosure",
            "Documentation"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 541",
            "Texas Administrative Code Title 28",
            "NAIC Model Laws"
        ],
        burden_holder="Producer or insurer",
        adversary_position="Improper rebating or violation of consumer protection",
        counter_arguments=[
            "Inducement exceeds permitted value",
            "Not disclosed to insured",
            "Violation of statutory prohibition"
        ],
        resolution_strategy="Regulatory review and enforcement",
        entity_scope="Producers, insurers, affiliated entities",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 541"
    ),
    DoctrineBlock(
        topic="Twisting and Replacement Regulation",
        keywords=[
            "twisting", "replacement", "insurance sales", "Texas Insurance Code", "consumer protection"
        ],
        conclusion_template="Texas law prohibits twisting and regulates replacement of insurance policies to protect consumers from deceptive sales practices.",
        reasoning_framework=(
            "Twisting involves misrepresentation to induce policyholders to replace existing insurance with new coverage, prohibited under Texas Insurance Code. "
            "Replacement regulations require disclosure, comparison of benefits, and written acknowledgment by the policyholder. "
            "Key factors include sales practices, disclosure compliance, and consumer consent. "
            "The burden is on the producer to avoid twisting and comply with replacement regulations. "
            "Adversaries may allege deceptive practices or failure to disclose. "
            "Resolution involves regulatory enforcement, fines, and possible license suspension. "
            "The doctrine applies to producers, insurers, and policyholders. "
            "Confidence is high due to statutory clarity and strong consumer protection focus."
        ),
        key_factors=[
            "Sales practices",
            "Disclosure compliance",
            "Consumer consent",
            "Written acknowledgment"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 541",
            "Texas Administrative Code Title 28",
            "NAIC Model Laws"
        ],
        burden_holder="Producer",
        adversary_position="Deceptive sales practices or failure to disclose",
        counter_arguments=[
            "Misrepresentation",
            "Failure to provide comparison",
            "Lack of consumer consent"
        ],
        resolution_strategy="Regulatory enforcement, fines, license suspension",
        entity_scope="Producers, insurers, policyholders",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 541"
    ),
    DoctrineBlock(
        topic="Advertising and Marketing Regulation",
        keywords=[
            "advertising", "marketing", "insurance sales", "Texas Insurance Code", "regulatory compliance"
        ],
        conclusion_template="Insurance advertising and marketing must comply with Texas law, prohibiting deceptive or misleading statements.",
        reasoning_framework=(
            "Texas Insurance Code and NAIC Model Laws regulate advertising and marketing of insurance products. "
            "Prohibited practices include false statements, misrepresentation of coverage, and misleading comparisons. "
            "All advertising must be truthful, clear, and not deceptive. "
            "Key factors include content review, compliance with disclosure requirements, and documentation. "
            "The burden is on the insurer or producer to ensure compliance. "
            "Adversaries may allege deceptive advertising or misrepresentation. "
            "Resolution involves regulatory review, corrective action, and enforcement. "
            "The doctrine applies to insurers, producers, and affiliated entities. "
            "Confidence is high due to clear statutory requirements and regulatory oversight."
        ),
        key_factors=[
            "Content review",
            "Disclosure compliance",
            "Documentation",
            "Truthfulness"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 541",
            "Texas Administrative Code Title 28",
            "NAIC Model Laws"
        ],
        burden_holder="Insurer or producer",
        adversary_position="Deceptive advertising or misrepresentation",
        counter_arguments=[
            "False statements",
            "Misleading comparisons",
            "Failure to disclose"
        ],
        resolution_strategy="Regulatory review, corrective action, enforcement",
        entity_scope="Insurers, producers, affiliated entities",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 541"
    ),
    DoctrineBlock(
        topic="Privacy and Information Security (GLBA and State Laws)",
        keywords=[
            "privacy", "information security", "GLBA", "Texas Insurance Code", "data protection", "consumer privacy"
        ],
        conclusion_template="Insurers must comply with federal and state privacy and information security laws, including GLBA and Texas Insurance Code requirements.",
        reasoning_framework=(
            "The Gramm-Leach-Bliley Act (GLBA) and Texas Insurance Code require insurers to protect consumer information and implement information security programs. "
            "GLBA mandates privacy notices, opt-out rights, and safeguarding of nonpublic personal information. "
            "Texas law imposes additional requirements for data breach notification and cybersecurity. "
            "Key factors include privacy policy, security controls, breach response, and consumer rights. "
            "The burden is on the insurer to comply with privacy and security requirements. "
            "Adversaries may allege data breach or inadequate protection. "
            "Resolution involves regulatory review, enforcement, and possible civil liability. "
            "The doctrine applies to insurers, producers, and affiliated entities. "
            "Confidence is high due to federal and state statutory clarity."
        ),
        key_factors=[
            "Privacy policy",
            "Security controls",
            "Breach response",
            "Consumer rights"
        ],
        primary_authority=[
            "Gramm-Leach-Bliley Act (GLBA)",
            "Texas Insurance Code Chapter 601",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Data breach or inadequate protection",
        counter_arguments=[
            "Failure to implement security controls",
            "Inadequate privacy notice",
            "Delayed breach notification"
        ],
        resolution_strategy="Regulatory review, enforcement, civil liability",
        entity_scope="Insurers, producers, affiliated entities",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GLBA and Texas Insurance Code Chapter 601"
    ),
    DoctrineBlock(
        topic="Annual Financial Statement Filing and Statutory Accounting",
        keywords=[
            "annual financial statement", "statutory accounting", "Texas Insurance Code", "NAIC", "regulatory compliance"
        ],
        conclusion_template="Insurers must file annual financial statements in accordance with statutory accounting principles and Texas law.",
        reasoning_framework=(
            "Texas Insurance Code and NAIC Model Laws require insurers to file annual financial statements using statutory accounting principles (SAP). "
            "SAP differs from GAAP, focusing on solvency and regulatory reporting. "
            "Statements must include balance sheet, income statement, and supporting schedules. "
            "Key factors include completeness, accuracy, and timeliness of filings. "
            "The burden is on the insurer to comply with filing requirements. "
            "Adversaries may allege inaccurate reporting or late filing. "
            "Resolution involves regulatory review, audit, and enforcement. "
            "The doctrine applies to admitted insurers and affiliated entities. "
            "Confidence is high due to uniform adoption and regulatory oversight."
        ),
        key_factors=[
            "Completeness of filings",
            "Accuracy",
            "Timeliness",
            "Statutory accounting principles"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 802",
            "NAIC Annual Statement Instructions",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Inaccurate reporting or late filing",
        counter_arguments=[
            "Incomplete filings",
            "Failure to follow SAP",
            "Late submission"
        ],
        resolution_strategy="Regulatory review, audit, enforcement",
        entity_scope="Admitted insurers, affiliated entities",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NAIC Annual Statement Instructions"
    ),
    DoctrineBlock(
        topic="Financial Examination Authority and Examination Report",
        keywords=[
            "financial examination", "authority", "examination report", "Texas Insurance Code", "NAIC"
        ],
        conclusion_template="Texas Department of Insurance has authority to conduct financial examinations of insurers and issue examination reports.",
        reasoning_framework=(
            "Texas Insurance Code and NAIC Model Laws grant TDI authority to conduct financial examinations of insurers. "
            "Examinations assess solvency, compliance, and financial condition. "
            "Reports document findings, recommendations, and corrective actions. "
            "Key factors include examination scope, cooperation, and accuracy of records. "
            "The burden is on the insurer to cooperate and provide documentation. "
            "Adversaries may dispute findings or recommendations. "
            "Resolution involves regulatory review, corrective action, and enforcement. "
            "The doctrine applies to admitted insurers and affiliated entities. "
            "Confidence is high due to statutory clarity and regulatory practice."
        ),
        key_factors=[
            "Examination scope",
            "Cooperation",
            "Accuracy of records",
            "Corrective action"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 401",
            "NAIC Financial Condition Examiners Handbook",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Dispute over findings or recommendations",
        counter_arguments=[
            "Inaccurate records",
            "Failure to cooperate",
            "Disagreement with corrective action"
        ],
        resolution_strategy="Regulatory review, corrective action, enforcement",
        entity_scope="Admitted insurers, affiliated entities",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NAIC Financial Condition Examiners Handbook"
    ),
    DoctrineBlock(
        topic="Own Risk and Solvency Assessment (ORSA) Requirement",
        keywords=[
            "ORSA", "own risk", "solvency assessment", "Texas Insurance Code", "NAIC", "enterprise risk"
        ],
        conclusion_template="Insurers must conduct an Own Risk and Solvency Assessment (ORSA) and submit summary reports to the Texas Department of Insurance.",
        reasoning_framework=(
            "Texas Insurance Code and NAIC Model Laws require insurers to conduct an ORSA, assessing enterprise risk and solvency. "
            "ORSA involves internal analysis of risk exposure, capital adequacy, and risk management processes. "
            "Insurers must submit ORSA summary reports to TDI annually. "
            "Key factors include risk identification, capital adequacy, and governance. "
            "The burden is on the insurer to conduct ORSA and submit reports. "
            "Adversaries may allege inadequate risk assessment or reporting. "
            "Resolution involves regulatory review, corrective action, and enforcement. "
            "The doctrine applies to insurers, holding companies, and affiliates. "
            "Confidence is high due to statutory clarity and regulatory oversight."
        ),
        key_factors=[
            "Risk identification",
            "Capital adequacy",
            "Governance",
            "Reporting compliance"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 404",
            "NAIC ORSA Model Act",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Inadequate risk assessment or reporting",
        counter_arguments=[
            "Failure to identify enterprise risk",
            "Insufficient capital",
            "Incomplete ORSA report"
        ],
        resolution_strategy="Regulatory review, corrective action, enforcement",
        entity_scope="Insurers, holding companies, affiliates",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NAIC ORSA Model Act"
    ),
    # Additional doctrine blocks for completeness (20+ more for 40+ total)
    DoctrineBlock(
        topic="Prompt Payment of Claims Statute",
        keywords=[
            "prompt payment", "claims", "Texas Insurance Code", "timeliness", "interest penalties"
        ],
        conclusion_template="Insurers must pay claims within statutory timelines or face interest penalties under Texas Insurance Code.",
        reasoning_framework=(
            "Texas Insurance Code Chapter 542 requires insurers to pay claims promptly, generally within 15 days of receipt of proof of loss. "
            "Failure to pay within statutory timelines results in interest penalties and possible regulatory action. "
            "Key factors include claim receipt date, payment timeline, and calculation of penalties. "
            "The burden is on the insurer to comply with payment deadlines. "
            "Adversaries may allege delayed payment or improper denial. "
            "Resolution involves regulatory enforcement and civil remedies. "
            "The doctrine applies to admitted insurers and policyholders. "
            "Confidence is high due to statutory clarity and strong consumer protection."
        ),
        key_factors=[
            "Claim receipt date",
            "Payment timeline",
            "Interest penalty calculation",
            "Compliance with deadlines"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 542",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Delayed payment or improper denial",
        counter_arguments=[
            "Failure to pay within deadline",
            "Improper denial",
            "Incorrect penalty calculation"
        ],
        resolution_strategy="Regulatory enforcement and civil remedies",
        entity_scope="Admitted insurers, policyholders",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 542"
    ),
    DoctrineBlock(
        topic="Policy Cancellation and Nonrenewal Requirements",
        keywords=[
            "policy cancellation", "nonrenewal", "notice requirements", "Texas Insurance Code", "consumer protection"
        ],
        conclusion_template="Insurers must comply with statutory notice requirements for policy cancellation and nonrenewal under Texas Insurance Code.",
        reasoning_framework=(
            "Texas Insurance Code mandates specific notice periods and reasons for cancellation and nonrenewal of insurance policies. "
            "Notice must be provided to the insured in writing, typically 30 days prior to cancellation or nonrenewal. "
            "Permissible reasons for cancellation are limited and must be documented. "
            "Key factors include notice period, documentation, and compliance with statutory reasons. "
            "The burden is on the insurer to provide proper notice and justification. "
            "Adversaries may allege improper cancellation or insufficient notice. "
            "Resolution involves regulatory review and possible reinstatement. "
            "The doctrine applies to admitted insurers and policyholders. "
            "Confidence is high due to statutory clarity and regulatory oversight."
        ),
        key_factors=[
            "Notice period",
            "Documentation",
            "Permissible reasons",
            "Compliance with statutory requirements"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 551",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Improper cancellation or insufficient notice",
        counter_arguments=[
            "Failure to provide notice",
            "Unjustified cancellation",
            "Non-compliance with statutory reasons"
        ],
        resolution_strategy="Regulatory review and possible reinstatement",
        entity_scope="Admitted insurers, policyholders",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 551"
    ),
    DoctrineBlock(
        topic="Insurance Fraud Prevention and Reporting",
        keywords=[
            "insurance fraud", "prevention", "reporting", "Texas Insurance Code", "SIU"
        ],
        conclusion_template="Insurers must implement fraud prevention programs and report suspected insurance fraud to regulatory authorities.",
        reasoning_framework=(
            "Texas Insurance Code requires insurers to establish Special Investigative Units (SIU) and implement fraud prevention programs. "
            "Suspected fraud must be reported to TDI and law enforcement. "
            "Key factors include SIU effectiveness, reporting compliance, and investigation outcomes. "
            "The burden is on the insurer to prevent, detect, and report fraud. "
            "Adversaries may allege inadequate prevention or failure to report. "
            "Resolution involves regulatory review, enforcement, and possible civil or criminal penalties. "
            "The doctrine applies to insurers, producers, and affiliated entities. "
            "Confidence is high due to statutory clarity and regulatory oversight."
        ),
        key_factors=[
            "SIU effectiveness",
            "Reporting compliance",
            "Investigation outcomes",
            "Documentation"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 701",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Inadequate fraud prevention or failure to report",
        counter_arguments=[
            "Failure to establish SIU",
            "Delayed reporting",
            "Insufficient investigation"
        ],
        resolution_strategy="Regulatory review, enforcement, civil/criminal penalties",
        entity_scope="Insurers, producers, affiliated entities",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 701"
    ),
    DoctrineBlock(
        topic="Insurance Company Formation and Licensing",
        keywords=[
            "company formation", "licensing", "Texas Insurance Code", "admitted insurer", "regulatory approval"
        ],
        conclusion_template="Insurance companies must comply with formation and licensing requirements under Texas Insurance Code before commencing business.",
        reasoning_framework=(
            "Texas Insurance Code sets forth requirements for the formation and licensing of insurance companies. "
            "Applicants must submit organizational documents, financial statements, and business plans to TDI. "
            "Licensing is contingent on regulatory approval and compliance with capital and surplus requirements. "
            "Key factors include organizational structure, capital adequacy, and regulatory approval. "
            "The burden is on the applicant to demonstrate compliance. "
            "Adversaries may allege insufficient capital or incomplete documentation. "
            "Resolution involves regulatory review and possible denial or approval. "
            "The doctrine applies to new insurers and affiliated entities. "
            "Confidence is high due to statutory clarity and regulatory oversight."
        ),
        key_factors=[
            "Organizational structure",
            "Capital adequacy",
            "Regulatory approval",
            "Compliance with statutory requirements"
        ],
        primary_authority=[
            "Texas Insurance Code Chapters 801-803",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Applicant insurer",
        adversary_position="Insufficient capital or incomplete documentation",
        counter_arguments=[
            "Failure to meet capital requirements",
            "Incomplete organizational documents",
            "Non-compliance with statutory requirements"
        ],
        resolution_strategy="Regulatory review and possible denial or approval",
        entity_scope="New insurers, affiliated entities",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapters 801-803"
    ),
    DoctrineBlock(
        topic="Insurance Policy Rescission and Material Misrepresentation",
        keywords=[
            "policy rescission", "material misrepresentation", "Texas Insurance Code", "fraud", "underwriting"
        ],
        conclusion_template="Insurers may rescind policies for material misrepresentation by the insured, subject to statutory and case law limitations.",
        reasoning_framework=(
            "Texas Insurance Code and case law permit insurers to rescind policies if the insured makes material misrepresentations during underwriting. "
            "Materiality is determined by whether the misrepresentation would have affected underwriting or issuance. "
            "Key factors include nature of misrepresentation, impact on underwriting, and timing. "
            "The burden is on the insurer to prove materiality and reliance. "
            "Adversaries may allege immateriality or lack of reliance. "
            "Resolution involves judicial interpretation and regulatory review. "
            "The doctrine applies to insurers and policyholders. "
            "Confidence is high due to statutory clarity and established precedent."
        ),
        key_factors=[
            "Nature of misrepresentation",
            "Impact on underwriting",
            "Timing",
            "Materiality"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 705",
            "Texas Administrative Code Title 28",
            "Case law: Mayes v. Massachusetts Mutual Life Ins. Co., 608 S.W.2d 612 (Tex. 1980)"
        ],
        burden_holder="Insurer",
        adversary_position="Immaterial misrepresentation or lack of reliance",
        counter_arguments=[
            "Misrepresentation was immaterial",
            "Insurer did not rely",
            "Policy cannot be rescinded after claim"
        ],
        resolution_strategy="Judicial interpretation and regulatory review",
        entity_scope="Insurers, policyholders",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Mayes v. Massachusetts Mutual Life Ins. Co., 608 S.W.2d 612 (Tex. 1980)"
    ),
    DoctrineBlock(
        topic="Group Insurance Policy Requirements",
        keywords=[
            "group insurance", "policy requirements", "Texas Insurance Code", "eligibility", "coverage"
        ],
        conclusion_template="Group insurance policies must comply with eligibility and coverage requirements under Texas Insurance Code.",
        reasoning_framework=(
            "Texas Insurance Code sets forth requirements for group insurance policies, including eligibility, minimum group size, and coverage standards. "
            "Policies must be issued to eligible groups and provide uniform coverage. "
            "Key factors include group eligibility, coverage uniformity, and compliance with statutory requirements. "
            "The burden is on the insurer to comply with group policy standards. "
            "Adversaries may allege improper issuance or non-uniform coverage. "
            "Resolution involves regulatory review and possible corrective action. "
            "The doctrine applies to insurers and group policyholders. "
            "Confidence is high due to statutory clarity and regulatory oversight."
        ),
        key_factors=[
            "Group eligibility",
            "Coverage uniformity",
            "Minimum group size",
            "Compliance with statutory requirements"
        ],
        primary_authority=[
            "Texas Insurance Code Chapters 1251, 1252",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Improper issuance or non-uniform coverage",
        counter_arguments=[
            "Group does not meet eligibility",
            "Coverage is not uniform",
            "Non-compliance with statutory requirements"
        ],
        resolution_strategy="Regulatory review and corrective action",
        entity_scope="Insurers, group policyholders",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapters 1251, 1252"
    ),
    DoctrineBlock(
        topic="Insurance Rate Adequacy and Non-Discrimination",
        keywords=[
            "rate adequacy", "non-discrimination", "Texas Insurance Code", "actuarial justification", "rate regulation"
        ],
        conclusion_template="Insurance rates must be adequate and not unfairly discriminatory under Texas Insurance Code and actuarial standards.",
        reasoning_framework=(
            "Texas Insurance Code and NAIC Model Laws require rates to be adequate, not excessive, and not unfairly discriminatory. "
            "Actuarial justification is required for all rate filings. "
            "Key factors include actuarial analysis, rate adequacy, and compliance with non-discrimination standards. "
            "The burden is on the insurer to demonstrate compliance. "
            "Adversaries may allege excessive or discriminatory rates. "
            "Resolution involves actuarial review and regulatory determination. "
            "The doctrine applies to admitted insurers and regulated lines. "
            "Confidence is high due to statutory clarity and regulatory oversight."
        ),
        key_factors=[
            "Actuarial analysis",
            "Rate adequacy",
            "Non-discrimination",
            "Compliance with statutory standards"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 2251",
            "NAIC Model Laws",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Excessive or discriminatory rates",
        counter_arguments=[
            "Rates lack actuarial support",
            "Rates are excessive",
            "Rates discriminate against certain insureds"
        ],
        resolution_strategy="Actuarial review and regulatory determination",
        entity_scope="Admitted insurers, regulated lines",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 2251"
    ),
    DoctrineBlock(
        topic="Insurance Producer Continuing Education Requirements",
        keywords=[
            "producer", "continuing education", "Texas Insurance Code", "license renewal", "regulatory compliance"
        ],
        conclusion_template="Insurance producers must complete continuing education requirements for license renewal under Texas Insurance Code.",
        reasoning_framework=(
            "Texas Insurance Code requires insurance producers to complete continuing education (CE) hours for license renewal. "
            "CE requirements vary by license type and must be completed within the renewal period. "
            "Key factors include CE completion, documentation, and compliance with renewal deadlines. "
            "The burden is on the producer to comply. "
            "Adversaries may allege non-compliance or incomplete CE. "
            "Resolution involves regulatory review and possible license suspension. "
            "The doctrine applies to producers and affiliated entities. "
            "Confidence is high due to statutory clarity and regulatory oversight."
        ),
        key_factors=[
            "CE completion",
            "Documentation",
            "Renewal deadlines",
            "Compliance with statutory requirements"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 4004",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Producer",
        adversary_position="Non-compliance or incomplete CE",
        counter_arguments=[
            "Failure to complete CE",
            "Incomplete documentation",
            "Missed renewal deadline"
        ],
        resolution_strategy="Regulatory review and license suspension",
        entity_scope="Producers, affiliated entities",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 4004"
    ),
    DoctrineBlock(
        topic="Insurance Company Insolvency and Receivership",
        keywords=[
            "insolvency", "receivership", "Texas Insurance Code", "regulatory intervention", "policyholder protection"
        ],
        conclusion_template="Texas Department of Insurance may place insolvent insurers into receivership to protect policyholders and creditors.",
        reasoning_framework=(
            "Texas Insurance Code authorizes TDI to intervene and place insolvent insurers into receivership. "
            "Receivership protects policyholders, manages assets, and resolves outstanding claims. "
            "Key factors include insolvency determination, asset management, and claim resolution. "
            "The burden is on TDI to manage receivership and protect policyholders. "
            "Adversaries may dispute insolvency or asset management. "
            "Resolution involves judicial oversight and regulatory action. "
            "The doctrine applies to admitted insurers and policyholders. "
            "Confidence is high due to statutory clarity and regulatory oversight."
        ),
        key_factors=[
            "Insolvency determination",
            "Asset management",
            "Claim resolution",
            "Judicial oversight"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 443",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Texas Department of Insurance",
        adversary_position="Dispute over insolvency or asset management",
        counter_arguments=[
            "Insurer is not insolvent",
            "Improper asset management",
            "Failure to protect policyholders"
        ],
        resolution_strategy="Judicial oversight and regulatory action",
        entity_scope="Admitted insurers, policyholders",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 443"
    ),
    DoctrineBlock(
        topic="Insurance Company Redomestication Procedures",
        keywords=[
            "redomestication", "company procedures", "Texas Insurance Code", "regulatory approval", "admitted insurer"
        ],
        conclusion_template="Insurance companies must follow statutory procedures for redomestication and obtain regulatory approval under Texas Insurance Code.",
        reasoning_framework=(
            "Texas Insurance Code sets forth procedures for insurance company redomestication, including regulatory approval and compliance with statutory requirements. "
            "Applicants must submit documentation, obtain approval from TDI, and comply with capital and surplus requirements. "
            "Key factors include documentation, regulatory approval, and compliance with statutory requirements. "
            "The burden is on the insurer to demonstrate compliance. "
            "Adversaries may allege incomplete documentation or insufficient capital. "
            "Resolution involves regulatory review and possible approval or denial. "
            "The doctrine applies to insurers seeking redomestication. "
            "Confidence is high due to statutory clarity and regulatory oversight."
        ),
        key_factors=[
            "Documentation",
            "Regulatory approval",
            "Capital and surplus requirements",
            "Compliance with statutory procedures"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 803",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Incomplete documentation or insufficient capital",
        counter_arguments=[
            "Failure to meet capital requirements",
            "Incomplete documentation",
            "Non-compliance with statutory procedures"
        ],
        resolution_strategy="Regulatory review and possible approval or denial",
        entity_scope="Insurers seeking redomestication",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 803"
    ),
    DoctrineBlock(
        topic="Insurance Policyholder Rights and Disclosure",
        keywords=[
            "policyholder rights", "disclosure", "Texas Insurance Code", "consumer protection", "regulatory compliance"
        ],
        conclusion_template="Insurers must disclose policyholder rights and comply with statutory requirements under Texas Insurance Code.",
        reasoning_framework=(
            "Texas Insurance Code requires insurers to disclose policyholder rights, including cancellation, claims, and complaint procedures. "
            "Disclosure must be clear, accurate, and provided at policy issuance. "
            "Key factors include disclosure content, timing, and compliance. "
            "The burden is on the insurer to comply. "
            "Adversaries may allege inadequate disclosure or violation of rights. "
            "Resolution involves regulatory review and corrective action. "
            "The doctrine applies to insurers and policyholders. "
            "Confidence is high due to statutory clarity and consumer protection focus."
        ),
        key_factors=[
            "Disclosure content",
            "Timing",
            "Compliance with statutory requirements",
            "Consumer protection"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 521",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Inadequate disclosure or violation of rights",
        counter_arguments=[
            "Failure to disclose",
            "Inaccurate disclosure",
            "Violation of statutory requirements"
        ],
        resolution_strategy="Regulatory review and corrective action",
        entity_scope="Insurers, policyholders",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 521"
    ),
    DoctrineBlock(
        topic="Insurance Underwriting Guidelines and Regulatory Review",
        keywords=[
            "underwriting guidelines", "regulatory review", "Texas Insurance Code", "risk selection", "compliance"
        ],
        conclusion_template="Insurers must maintain underwriting guidelines and submit them for regulatory review under Texas Insurance Code.",
        reasoning_framework=(
            "Texas Insurance Code requires insurers to maintain underwriting guidelines and submit them for regulatory review. "
            "Guidelines must comply with statutory standards, including non-discrimination and risk selection. "
            "Key factors include guideline content, compliance, and documentation. "
            "The burden is on the insurer to comply. "
            "Adversaries may allege discriminatory or non-compliant guidelines. "
            "Resolution involves regulatory review and possible corrective action. "
            "The doctrine applies to insurers and affiliated entities. "
            "Confidence is high due to statutory clarity and regulatory oversight."
        ),
        key_factors=[
            "Guideline content",
            "Compliance",
            "Documentation",
            "Risk selection"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 544",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Discriminatory or non-compliant guidelines",
        counter_arguments=[
            "Guidelines are discriminatory",
            "Non-compliance with statutory standards",
            "Failure to submit for review"
        ],
        resolution_strategy="Regulatory review and corrective action",
        entity_scope="Insurers, affiliated entities",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 544"
    ),
    DoctrineBlock(
        topic="Insurance Company Merger and Acquisition Procedures",
        keywords=[
            "merger", "acquisition", "company procedures", "Texas Insurance Code", "regulatory approval"
        ],
        conclusion_template="Insurance companies must follow statutory procedures for mergers and acquisitions and obtain regulatory approval under Texas Insurance Code.",
        reasoning_framework=(
            "Texas Insurance Code sets forth procedures for insurance company mergers and acquisitions, including regulatory approval and compliance with statutory requirements. "
            "Applicants must submit documentation, obtain approval from TDI, and comply with capital and surplus requirements. "
            "Key factors include documentation, regulatory approval, and compliance with statutory requirements. "
            "The burden is on the insurer to demonstrate compliance. "
            "Adversaries may allege incomplete documentation or insufficient capital. "
            "Resolution involves regulatory review and possible approval or denial. "
            "The doctrine applies to insurers seeking merger or acquisition. "
            "Confidence is high due to statutory clarity and regulatory oversight."
        ),
        key_factors=[
            "Documentation",
            "Regulatory approval",
            "Capital and surplus requirements",
            "Compliance with statutory procedures"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 823",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Incomplete documentation or insufficient capital",
        counter_arguments=[
            "Failure to meet capital requirements",
            "Incomplete documentation",
            "Non-compliance with statutory procedures"
        ],
        resolution_strategy="Regulatory review and possible approval or denial",
        entity_scope="Insurers seeking merger or acquisition",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 823"
    ),
    DoctrineBlock(
        topic="Insurance Policy Endorsement and Amendment Procedures",
        keywords=[
            "policy endorsement", "amendment", "Texas Insurance Code", "regulatory approval", "policyholder notification"
        ],
        conclusion_template="Insurance policy endorsements and amendments must comply with statutory procedures and be approved by TDI.",
        reasoning_framework=(
            "Texas Insurance Code requires insurers to submit policy endorsements and amendments for regulatory approval. "
            "Policyholders must be notified of changes. "
            "Key factors include endorsement content, regulatory approval, and notification. "
            "The burden is on the insurer to comply. "
            "Adversaries may allege improper endorsement or lack of notification. "
            "Resolution involves regulatory review and corrective action. "
            "The doctrine applies to insurers and policyholders. "
            "Confidence is high due to statutory clarity and regulatory oversight."
        ),
        key_factors=[
            "Endorsement content",
            "Regulatory approval",
            "Policyholder notification",
            "Compliance with statutory procedures"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 2301",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Improper endorsement or lack of notification",
        counter_arguments=[
            "Failure to notify policyholder",
            "Non-compliance with statutory procedures",
            "Endorsement not approved"
        ],
        resolution_strategy="Regulatory review and corrective action",
        entity_scope="Insurers, policyholders",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 2301"
    ),
    DoctrineBlock(
        topic="Insurance Producer Appointment Termination Procedures",
        keywords=[
            "producer appointment", "termination", "Texas Insurance Code", "regulatory notification", "license"
        ],
        conclusion_template="Insurers must follow statutory procedures for terminating producer appointments and notify TDI under Texas Insurance Code.",
        reasoning_framework=(
            "Texas Insurance Code requires insurers to notify TDI when terminating producer appointments. "
            "Notification must be timely and include reasons for termination. "
            "Key factors include notification, documentation, and compliance. "
            "The burden is on the insurer to comply. "
            "Adversaries may allege improper termination or lack of notification. "
            "Resolution involves regulatory review and possible corrective action. "
            "The doctrine applies to insurers and producers. "
            "Confidence is high due to statutory clarity and regulatory oversight."
        ),
        key_factors=[
            "Notification",
            "Documentation",
            "Compliance with statutory procedures",
            "Reasons for termination"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 4001",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Improper termination or lack of notification",
        counter_arguments=[
            "Failure to notify TDI",
            "Non-compliance with statutory procedures",
            "Improper termination"
        ],
        resolution_strategy="Regulatory review and corrective action",
        entity_scope="Insurers, producers",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 4001"
    ),
    DoctrineBlock(
        topic="Insurance Company Dividend and Surplus Distribution",
        keywords=[
            "dividend", "surplus distribution", "Texas Insurance Code", "regulatory approval", "financial reporting"
        ],
        conclusion_template="Insurance companies must obtain regulatory approval for dividend and surplus distribution under Texas Insurance Code.",
        reasoning_framework=(
            "Texas Insurance Code requires insurers to obtain regulatory approval for dividend and surplus distribution. "
            "Distribution must not impair solvency. "
            "Key factors include financial reporting, solvency, and regulatory approval. "
            "The burden is on the insurer to comply. "
            "Adversaries may allege impairment of solvency or improper distribution. "
            "Resolution involves regulatory review and possible denial. "
            "The doctrine applies to insurers and shareholders. "
            "Confidence is high due to statutory clarity and regulatory oversight."
        ),
        key_factors=[
            "Financial reporting",
            "Solvency",
            "Regulatory approval",
            "Compliance with statutory requirements"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 823",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Impairment of solvency or improper distribution",
        counter_arguments=[
            "Distribution impairs solvency",
            "Non-compliance with statutory requirements",
            "Failure to obtain approval"
        ],
        resolution_strategy="Regulatory review and possible denial",
        entity_scope="Insurers, shareholders",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 823"
    ),
    DoctrineBlock(
        topic="Insurance Company Change of Control Procedures",
        keywords=[
            "change of control", "company procedures", "Texas Insurance Code", "regulatory approval", "ownership"
        ],
        conclusion_template="Insurance companies must follow statutory procedures for change of control and obtain regulatory approval under Texas Insurance Code.",
        reasoning_framework=(
            "Texas Insurance Code requires insurers to obtain regulatory approval for change of control transactions. "
            "Applicants must submit documentation and comply with statutory requirements. "
            "Key factors include documentation, regulatory approval, and compliance. "
            "The burden is on the insurer to comply. "
            "Adversaries may allege incomplete documentation or improper change of control. "
            "Resolution involves regulatory review and possible approval or denial. "
            "The doctrine applies to insurers and new owners. "
            "Confidence is high due to statutory clarity and regulatory oversight."
        ),
        key_factors=[
            "Documentation",
            "Regulatory approval",
            "Compliance with statutory procedures",
            "Ownership structure"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 823",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Incomplete documentation or improper change of control",
        counter_arguments=[
            "Failure to submit documentation",
            "Non-compliance with statutory procedures",
            "Improper change of control"
        ],
        resolution_strategy="Regulatory review and possible approval or denial",
        entity_scope="Insurers, new owners",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 823"
    ),
    DoctrineBlock(
        topic="Insurance Company Withdrawal from Texas Market",
        keywords=[
            "company withdrawal", "Texas market", "Texas Insurance Code", "regulatory procedures", "policyholder protection"
        ],
        conclusion_template="Insurance companies must follow statutory procedures for withdrawal from the Texas market and protect policyholders under Texas Insurance Code.",
        reasoning_framework=(
            "Texas Insurance Code requires insurers to follow procedures for withdrawal from the Texas market, including notification to TDI and policyholders. "
            "Withdrawal must not impair policyholder protection. "
            "Key factors include notification, compliance, and policyholder protection. "
            "The burden is on the insurer to comply. "
            "Adversaries may allege inadequate protection or improper withdrawal. "
            "Resolution involves regulatory review and possible corrective action. "
            "The doctrine applies to insurers withdrawing from Texas. "
            "Confidence is high due to statutory clarity and regulatory oversight."
        ),
        key_factors=[
            "Notification",
            "Compliance with statutory procedures",
            "Policyholder protection",
            "Regulatory review"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 885",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Inadequate protection or improper withdrawal",
        counter_arguments=[
            "Failure to notify",
            "Non-compliance with statutory procedures",
            "Impairment of policyholder protection"
        ],
        resolution_strategy="Regulatory review and corrective action",
        entity_scope="Insurers withdrawing from Texas",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 885"
    ),
    DoctrineBlock(
        topic="Insurance Company Investment Restrictions",
        keywords=[
            "investment restrictions", "Texas Insurance Code", "admitted insurer", "regulatory compliance", "asset management"
        ],
        conclusion_template="Insurance companies must comply with investment restrictions under Texas Insurance Code to ensure solvency and regulatory compliance.",
        reasoning_framework=(
            "Texas Insurance Code sets forth investment restrictions for admitted insurers, including permissible asset classes, diversification, and concentration limits. "
            "Investment must not impair solvency. "
            "Key factors include asset class, diversification, and compliance. "
            "The burden is on the insurer to comply. "
            "Adversaries may allege improper investment or impairment of solvency. "
            "Resolution involves regulatory review and possible corrective action. "
            "The doctrine applies to admitted insurers. "
            "Confidence is high due to statutory clarity and regulatory oversight."
        ),
        key_factors=[
            "Asset class",
            "Diversification",
            "Compliance with statutory requirements",
            "Solvency"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 425",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Improper investment or impairment of solvency",
        counter_arguments=[
            "Investment violates statutory restrictions",
            "Non-compliance with diversification",
            "Impairment of solvency"
        ],
        resolution_strategy="Regulatory review and corrective action",
        entity_scope="Admitted insurers",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 425"
    ),
    DoctrineBlock(
        topic="Insurance Company Holding Company Registration",
        keywords=[
            "holding company registration", "Texas Insurance Code", "regulatory compliance", "ownership disclosure"
        ],
        conclusion_template="Insurance companies must register with TDI as part of holding company systems and disclose ownership under Texas Insurance Code.",
        reasoning_framework=(
            "Texas Insurance Code requires insurers to register as part of holding company systems and disclose ownership, organizational structure, and material transactions. "
            "Registration must be updated annually and upon material changes. "
            "Key factors include disclosure, compliance, and documentation. "
            "The burden is on the insurer to comply. "
            "Adversaries may allege incomplete disclosure or non-compliance. "
            "Resolution involves regulatory review and corrective action. "
            "The doctrine applies to insurers and holding companies. "
            "Confidence is high due to statutory clarity and regulatory oversight."
        ),
        key_factors=[
            "Disclosure",
            "Compliance",
            "Documentation",
            "Ownership structure"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 823",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Incomplete disclosure or non-compliance",
        counter_arguments=[
            "Failure to disclose",
            "Non-compliance with statutory requirements",
            "Incomplete documentation"
        ],
        resolution_strategy="Regulatory review and corrective action",
        entity_scope="Insurers, holding companies",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 823"
    ),
    DoctrineBlock(
        topic="Insurance Company Reporting of Catastrophe Exposure",
        keywords=[
            "catastrophe exposure", "reporting", "Texas Insurance Code", "regulatory compliance", "risk management"
        ],
        conclusion_template="Insurance companies must report catastrophe exposure to TDI and comply with risk management requirements under Texas Insurance Code.",
        reasoning_framework=(
            "Texas Insurance Code requires insurers to report catastrophe exposure, including hurricane, flood, and earthquake risks. "
            "Reporting supports regulatory oversight and risk management. "
            "Key factors include exposure data, compliance, and risk management. "
            "The burden is on the insurer to comply. "
            "Adversaries may allege incomplete reporting or inadequate risk management. "
            "Resolution involves regulatory review and corrective action. "
            "The doctrine applies to admitted insurers. "
            "Confidence is high due to statutory clarity and regulatory oversight."
        ),
        key_factors=[
            "Exposure data",
            "Compliance",
            "Risk management",
            "Regulatory review"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 2251",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Incomplete reporting or inadequate risk management",
        counter_arguments=[
            "Failure to report",
            "Non-compliance with risk management",
            "Incomplete exposure data"
        ],
        resolution_strategy="Regulatory review and corrective action",
        entity_scope="Admitted insurers",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 2251"
    ),
    DoctrineBlock(
        topic="Insurance Company Reporting of Statistical Data",
        keywords=[
            "statistical data", "reporting", "Texas Insurance Code", "regulatory compliance", "data accuracy"
        ],
        conclusion_template="Insurance companies must report statistical data to TDI and ensure data accuracy under Texas Insurance Code.",
        reasoning_framework=(
            "Texas Insurance Code requires insurers to report statistical data, including premium, loss, and exposure information. "
            "Reporting supports regulatory oversight and actuarial analysis. "
            "Key factors include data accuracy, compliance, and timeliness. "
            "The burden is on the insurer to comply. "
            "Adversaries may allege inaccurate or incomplete data. "
            "Resolution involves regulatory review and corrective action. "
            "The doctrine applies to admitted insurers. "
            "Confidence is high due to statutory clarity and regulatory oversight."
        ),
        key_factors=[
            "Data accuracy",
            "Compliance",
            "Timeliness",
            "Regulatory review"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 2251",
            "Texas Administrative Code Title 28"
        ],
        burden_holder="Insurer",
        adversary_position="Inaccurate or incomplete data",
        counter_arguments=[
            "Failure to report",
            "Inaccurate data",
            "Non-compliance with statutory requirements"
        ],
        resolution_strategy="Regulatory review and corrective action",
        entity_scope="Admitted insurers",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code Chapter 2251"
    ),
    DoctrineBlock(
        topic="Insurance Company Reporting of Premium Taxes",
        keywords=[
            "premium taxes", "reporting", "Texas Insurance Code", "regulatory compliance", "tax remittance"
        ],
        conclusion_template="Insurance companies must report and remit premium taxes to the Texas Comptroller under Texas Insurance Code.",
        reasoning_framework=(
            "Texas Insurance Code and Texas Tax Code require insurers to report and remit premium taxes to the Texas Comptroller. "
            "Reporting must be accurate and timely. "
            "Key factors include tax calculation, reporting, and remittance. "
            "The burden is on the insurer to comply. "
            "Adversaries may allege inaccurate reporting or failure to remit. "
            "Resolution involves regulatory review and possible penalties. "
            "The doctrine applies to admitted insurers and surplus lines brokers. "
            "Confidence is high due to statutory clarity and regulatory oversight."
        ),
        key_factors=[
            "Tax calculation",
            "Reporting",
            "Remittance",
            "Compliance"
        ],
        primary_authority=[
            "Texas Insurance Code Chapter 2251",
            "Texas Tax Code Section 226"
        ],
        burden_holder="Insurer",
        adversary_position="Inaccurate reporting or failure to remit",
        counter_arguments=[
            "Failure to report",
            "Incorrect tax calculation",
            "Late remittance"
        ],
        resolution_strategy="Regulatory review and possible penalties