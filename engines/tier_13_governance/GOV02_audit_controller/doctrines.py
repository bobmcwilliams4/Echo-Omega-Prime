from dataclasses import dataclass, field
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
        topic="Open Government Principle",
        keywords=["transparency", "public access", "accountability", "FOIA", "sunshine laws"],
        conclusion_template="The government must provide access to records unless a specific exemption applies.",
        reasoning_framework=(
            "The open government principle is rooted in the presumption that government actions and records "
            "should be accessible to the public to ensure accountability and foster trust. Statutes such as the "
            "Freedom of Information Act (FOIA) and state-level sunshine laws codify this presumption, placing the "
            "burden on the government to justify any withholding of information. Courts interpret exemptions narrowly, "
            "requiring clear statutory authority for non-disclosure. The reasoning framework involves analyzing the "
            "requested information, identifying any applicable exemptions, and assessing whether the public interest "
            "in disclosure outweighs the government's interest in confidentiality. Precedents emphasize that "
            "transparency is the default, and secrecy is the exception."
        ),
        key_factors=[
            "Nature of the information requested",
            "Statutory exemptions",
            "Public interest in disclosure",
            "Potential harm from disclosure",
            "Precedent interpreting open government statutes"
        ],
        primary_authority=[
            "Freedom of Information Act (5 U.S.C. § 552)",
            "Sunshine Act (5 U.S.C. § 552b)",
            "Relevant state open records laws"
        ],
        burden_holder="Government agency",
        adversary_position="Disclosure would harm governmental interests or violate privacy/confidentiality.",
        counter_arguments=[
            "Exemptions are to be construed narrowly.",
            "Public interest in transparency outweighs asserted harms.",
            "Redaction can mitigate privacy/confidentiality concerns."
        ],
        resolution_strategy="Apply statutory framework, interpret exemptions narrowly, balance interests, and consider redaction.",
        entity_scope="All government agencies subject to FOIA or equivalent state law.",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Department of the Air Force v. Rose, 425 U.S. 352 (1976)"
    ),
    DoctrineBlock(
        topic="Deliberative Process Privilege",
        keywords=["exemption", "predecisional", "policy formation", "internal communications", "FOIA Exemption 5"],
        conclusion_template="Predecisional and deliberative documents may be withheld under the deliberative process privilege.",
        reasoning_framework=(
            "The deliberative process privilege protects documents that are both predecisional and deliberative, "
            "to encourage open and frank discussion within agencies during policy formulation. The privilege is "
            "codified in FOIA Exemption 5 and interpreted by courts to apply only to documents generated before "
            "a final decision and reflecting the give-and-take of the consultative process. The analysis requires "
            "determining whether the document was created prior to a policy decision and whether it contains opinions, "
            "recommendations, or advice, as opposed to purely factual material. Courts may order disclosure of factual "
            "segments if they are reasonably segregable. The privilege does not protect documents explaining or "
            "implementing final policy."
        ),
        key_factors=[
            "Timing of document creation relative to decision",
            "Content (opinion vs. fact)",
            "Role in policy formulation",
            "Segregability of factual material"
        ],
        primary_authority=[
            "5 U.S.C. § 552(b)(5)",
            "NLRB v. Sears, Roebuck & Co., 421 U.S. 132 (1975)",
            "EPA v. Mink, 410 U.S. 73 (1973)"
        ],
        burden_holder="Government agency",
        adversary_position="The document is postdecisional or contains segregable factual information.",
        counter_arguments=[
            "Document is not predecisional or deliberative.",
            "Factual material can be disclosed.",
            "Privilege is waived if the policy is adopted."
        ],
        resolution_strategy="Analyze document's function and timing, segregate factual content, apply privilege narrowly.",
        entity_scope="Federal and state executive agencies.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NLRB v. Sears, Roebuck & Co., 421 U.S. 132 (1975)"
    ),
    DoctrineBlock(
        topic="Personal Privacy Exemption",
        keywords=["privacy", "FOIA Exemption 6", "personnel files", "unwarranted invasion"],
        conclusion_template="Information may be withheld if disclosure would constitute a clearly unwarranted invasion of personal privacy.",
        reasoning_framework=(
            "FOIA Exemption 6 protects personnel, medical, and similar files from disclosure when it would result in a "
            "clearly unwarranted invasion of personal privacy. The analysis requires balancing the individual's privacy "
            "interest against the public interest in disclosure. Courts interpret 'similar files' broadly to include "
            "any information that applies to a particular individual. The public interest is limited to shedding light "
            "on government operations, not satisfying curiosity about private citizens. If the privacy interest "
            "outweighs the public interest, the information may be withheld."
        ),
        key_factors=[
            "Nature of the information",
            "Identifiability of individuals",
            "Magnitude of privacy interest",
            "Public interest in disclosure"
        ],
        primary_authority=[
            "5 U.S.C. § 552(b)(6)",
            "Department of State v. Washington Post Co., 456 U.S. 595 (1982)"
        ],
        burden_holder="Government agency",
        adversary_position="The public interest in disclosure outweighs the privacy interest.",
        counter_arguments=[
            "Information is not 'similar file' material.",
            "Redaction can protect privacy.",
            "Public interest in government accountability is compelling."
        ],
        resolution_strategy="Balance privacy and public interests, consider redaction, apply statutory language.",
        entity_scope="All agencies holding personnel or similar records.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Department of State v. Washington Post Co., 456 U.S. 595 (1982)"
    ),
    DoctrineBlock(
        topic="Law Enforcement Records Exemption",
        keywords=["FOIA Exemption 7", "law enforcement", "investigatory records", "interference", "privacy"],
        conclusion_template="Law enforcement records may be withheld if disclosure would cause enumerated harms under Exemption 7.",
        reasoning_framework=(
            "FOIA Exemption 7 protects records compiled for law enforcement purposes if disclosure could reasonably be "
            "expected to cause one of several specified harms, such as interfering with enforcement proceedings, "
            "invading personal privacy, disclosing confidential sources, or endangering life or safety. The agency "
            "must demonstrate a rational nexus between the records and law enforcement purposes, and articulate the "
            "foreseeable harm. Courts require a fact-specific showing and may order disclosure if the risk is "
            "speculative or minimal. Segregable, non-exempt information must be disclosed."
        ),
        key_factors=[
            "Purpose for which records were compiled",
            "Specific harm from disclosure",
            "Nature of ongoing proceedings",
            "Identifiability of individuals"
        ],
        primary_authority=[
            "5 U.S.C. § 552(b)(7)",
            "FBI v. Abramson, 456 U.S. 615 (1982)"
        ],
        burden_holder="Government agency",
        adversary_position="No foreseeable harm or records are not for law enforcement purposes.",
        counter_arguments=[
            "Records are not law enforcement related.",
            "No specific harm is articulated.",
            "Information is already public."
        ],
        resolution_strategy="Analyze purpose, articulate harm, segregate non-exempt material, apply exemption strictly.",
        entity_scope="Law enforcement and regulatory agencies.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FBI v. Abramson, 456 U.S. 615 (1982)"
    ),
    DoctrineBlock(
        topic="Agency Records Definition",
        keywords=["agency", "record", "FOIA", "control", "creation", "possession"],
        conclusion_template="A document is an agency record if it is created or obtained by an agency and under its control.",
        reasoning_framework=(
            "The definition of 'agency record' under FOIA requires that the document be both created or obtained by "
            "the agency and under its control at the time of the request. Courts apply a two-part test: (1) whether "
            "the agency created or obtained the document, and (2) whether the agency controls the document. Control "
            "is determined by factors such as the agency's ability to use and dispose of the record, the extent to "
            "which personnel have read or relied on it, and its integration into agency files. Personal notes or "
            "records not used for agency business are generally not agency records."
        ),
        key_factors=[
            "Origin of the document",
            "Agency control",
            "Integration into agency files",
            "Use in agency business"
        ],
        primary_authority=[
            "5 U.S.C. § 552(f)",
            "Department of Justice v. Tax Analysts, 492 U.S. 136 (1989)"
        ],
        burden_holder="Requester",
        adversary_position="The document is not under agency control or not used for agency business.",
        counter_arguments=[
            "Document is not integrated into agency files.",
            "Agency lacks control over the document.",
            "Document is purely personal."
        ],
        resolution_strategy="Apply two-part test, examine control and use, reference controlling precedent.",
        entity_scope="All federal agencies.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Department of Justice v. Tax Analysts, 492 U.S. 136 (1989)"
    ),
    DoctrineBlock(
        topic="Segregability Requirement",
        keywords=["redaction", "non-exempt", "FOIA", "segregable", "partial disclosure"],
        conclusion_template="Agencies must disclose all reasonably segregable, non-exempt information.",
        reasoning_framework=(
            "FOIA requires agencies to provide all reasonably segregable, non-exempt portions of a record after "
            "deleting exempt material. Courts strictly enforce this requirement, mandating that agencies justify "
            "withholding any portion and demonstrate that non-exempt information cannot be separated without "
            "revealing exempt content. Agencies must provide detailed justifications, often through Vaughn indices, "
            "and courts may conduct in camera review. The policy favors maximum disclosure consistent with statutory "
            "exemptions."
        ),
        key_factors=[
            "Nature of exempt and non-exempt material",
            "Feasibility of redaction",
            "Agency justifications",
            "Judicial review"
        ],
        primary_authority=[
            "5 U.S.C. § 552(b)",
            "Department of Justice v. Julian, 486 U.S. 1 (1988)"
        ],
        burden_holder="Government agency",
        adversary_position="Non-exempt information can be segregated and disclosed.",
        counter_arguments=[
            "Agency has not demonstrated non-segregability.",
            "Redaction is feasible.",
            "Agency's Vaughn index is insufficient."
        ],
        resolution_strategy="Review agency justifications, require detailed explanation, order in camera review if necessary.",
        entity_scope="All agencies subject to FOIA.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Department of Justice v. Julian, 486 U.S. 1 (1988)"
    ),
    DoctrineBlock(
        topic="Exemption 1: National Security",
        keywords=["classified", "national defense", "foreign policy", "FOIA Exemption 1", "security clearance"],
        conclusion_template="Classified information may be withheld if properly classified under an executive order.",
        reasoning_framework=(
            "FOIA Exemption 1 allows agencies to withhold information that is properly classified under an executive "
            "order in the interest of national defense or foreign policy. The agency must demonstrate that the "
            "information is in fact classified, the classification was proper, and the executive order requirements "
            "were followed. Courts give substantial deference to agency affidavits but require a plausible nexus "
            "between disclosure and national security harm. Over-classification or improper classification can be "
            "challenged."
        ),
        key_factors=[
            "Classification status",
            "Compliance with executive order",
            "Nexus to national security",
            "Agency affidavits"
        ],
        primary_authority=[
            "5 U.S.C. § 552(b)(1)",
            "Executive Order 13526"
        ],
        burden_holder="Government agency",
        adversary_position="Information is not properly classified or no national security risk exists.",
        counter_arguments=[
            "Classification was improper or overbroad.",
            "No real national security risk.",
            "Agency affidavits are conclusory."
        ],
        resolution_strategy="Review classification, require detailed affidavits, apply deference but scrutinize claims.",
        entity_scope="Agencies handling classified information.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="CIA v. Sims, 471 U.S. 159 (1985)"
    ),
    DoctrineBlock(
        topic="Exemption 3: Statutory Exemptions",
        keywords=["FOIA Exemption 3", "statute", "withholding", "specificity", "federal law"],
        conclusion_template="Information may be withheld if a statute specifically exempts it from disclosure.",
        reasoning_framework=(
            "FOIA Exemption 3 incorporates other statutes that require information to be withheld from the public. "
            "The statute must either leave no discretion or establish particular criteria for withholding. Courts "
            "analyze whether the statute qualifies under Exemption 3 and whether the withheld information falls "
            "within its scope. Examples include the Privacy Act, the Bank Secrecy Act, and the Internal Revenue Code. "
            "Agencies must cite the specific statute and justify the application."
        ),
        key_factors=[
            "Existence of qualifying statute",
            "Specificity of withholding criteria",
            "Application to requested information"
        ],
        primary_authority=[
            "5 U.S.C. § 552(b)(3)",
            "Privacy Act of 1974",
            "Internal Revenue Code § 6103"
        ],
        burden_holder="Government agency",
        adversary_position="Statute does not qualify or information is not covered.",
        counter_arguments=[
            "Statute is not sufficiently specific.",
            "Information does not fall within statute.",
            "Agency has discretion to disclose."
        ],
        resolution_strategy="Identify qualifying statute, analyze criteria, require precise justification.",
        entity_scope="All agencies subject to FOIA.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="CIA v. Sims, 471 U.S. 159 (1985)"
    ),
    DoctrineBlock(
        topic="Exemption 4: Confidential Business Information",
        keywords=["trade secrets", "commercial", "confidential", "FOIA Exemption 4", "competitive harm"],
        conclusion_template="Confidential commercial or financial information may be withheld if disclosure would cause competitive harm.",
        reasoning_framework=(
            "FOIA Exemption 4 protects trade secrets and confidential commercial or financial information obtained "
            "from a person. The Supreme Court clarified in Food Marketing Institute v. Argus Leader Media that "
            "information is 'confidential' if it is customarily and actually treated as private by its owner and "
            "provided to the government under an assurance of privacy. Agencies must show that disclosure would cause "
            "substantial competitive harm or impair the government's ability to obtain such information in the future."
        ),
        key_factors=[
            "Nature of the information",
            "Customary treatment as confidential",
            "Assurances of privacy",
            "Competitive harm"
        ],
        primary_authority=[
            "5 U.S.C. § 552(b)(4)",
            "Food Marketing Institute v. Argus Leader Media, 139 S. Ct. 2356 (2019)"
        ],
        burden_holder="Government agency",
        adversary_position="Information is not confidential or no competitive harm exists.",
        counter_arguments=[
            "Information is public or routinely disclosed.",
            "No competitive harm from disclosure.",
            "No assurance of privacy was given."
        ],
        resolution_strategy="Apply Argus Leader test, require evidence of confidentiality and harm.",
        entity_scope="All agencies receiving business information.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Food Marketing Institute v. Argus Leader Media, 139 S. Ct. 2356 (2019)"
    ),
    DoctrineBlock(
        topic="Exemption 5: Inter-Agency or Intra-Agency Memoranda",
        keywords=["FOIA Exemption 5", "privilege", "internal", "policy", "attorney-client"],
        conclusion_template="Inter- or intra-agency memoranda may be withheld if privileged under civil discovery rules.",
        reasoning_framework=(
            "Exemption 5 incorporates civil discovery privileges, including the deliberative process, attorney-client, "
            "and attorney work-product privileges. The document must be both inter- or intra-agency and privileged. "
            "The analysis mirrors that of civil litigation, requiring the agency to demonstrate the privilege applies. "
            "Factual material is generally not protected unless inextricably intertwined with privileged content."
        ),
        key_factors=[
            "Nature of the privilege claimed",
            "Agency relationship",
            "Content (fact vs. opinion)",
            "Segregability"
        ],
        primary_authority=[
            "5 U.S.C. § 552(b)(5)",
            "NLRB v. Sears, Roebuck & Co., 421 U.S. 132 (1975)"
        ],
        burden_holder="Government agency",
        adversary_position="Document is not privileged or factual material is segregable.",
        counter_arguments=[
            "Privilege does not apply.",
            "Factual content can be disclosed.",
            "Document is not inter- or intra-agency."
        ],
        resolution_strategy="Analyze privilege, segregate factual material, apply civil discovery standards.",
        entity_scope="All agencies subject to FOIA.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="NLRB v. Sears, Roebuck & Co., 421 U.S. 132 (1975)"
    ),
    DoctrineBlock(
        topic="Exemption 7(C): Law Enforcement Privacy",
        keywords=["law enforcement", "privacy", "FOIA Exemption 7(C)", "investigation", "unwarranted invasion"],
        conclusion_template="Personal information in law enforcement records may be withheld if disclosure would constitute an unwarranted invasion of privacy.",
        reasoning_framework=(
            "Exemption 7(C) allows agencies to withhold law enforcement records if disclosure could reasonably be "
            "expected to constitute an unwarranted invasion of personal privacy. The analysis balances the privacy "
            "interest against the public interest in disclosure, with the privacy interest receiving substantial "
            "weight. The public interest must relate to shedding light on government operations, not curiosity about "
            "private individuals. Courts have upheld broad application of this exemption to protect witnesses, "
            "suspects, and investigators."
        ),
        key_factors=[
            "Identifiability of individuals",
            "Nature of information",
            "Public interest in disclosure",
            "Potential harm to privacy"
        ],
        primary_authority=[
            "5 U.S.C. § 552(b)(7)(C)",
            "Department of Justice v. Reporters Committee, 489 U.S. 749 (1989)"
        ],
        burden_holder="Government agency",
        adversary_position="Public interest in disclosure outweighs privacy interest.",
        counter_arguments=[
            "Information is already public.",
            "Redaction can protect privacy.",
            "Public interest is compelling."
        ],
        resolution_strategy="Balance interests, consider redaction, apply privacy protection broadly.",
        entity_scope="Law enforcement and regulatory agencies.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Department of Justice v. Reporters Committee, 489 U.S. 749 (1989)"
    ),
    DoctrineBlock(
        topic="Exemption 7(E): Law Enforcement Techniques",
        keywords=["law enforcement", "techniques", "procedures", "FOIA Exemption 7(E)", "circumvention"],
        conclusion_template="Information may be withheld if disclosure would risk circumvention of the law.",
        reasoning_framework=(
            "Exemption 7(E) protects law enforcement records that would disclose techniques and procedures for law "
            "enforcement investigations or prosecutions if such disclosure could reasonably be expected to risk "
            "circumvention of the law. The agency must demonstrate that the technique is not generally known and that "
            "disclosure would aid wrongdoers. Courts require a logical connection between disclosure and risk, but "
            "deference is given to agency expertise."
        ),
        key_factors=[
            "Nature of technique or procedure",
            "Public availability of information",
            "Risk of circumvention",
            "Agency justification"
        ],
        primary_authority=[
            "5 U.S.C. § 552(b)(7)(E)",
            "Blackwell v. FBI, 646 F.3d 37 (D.C. Cir. 2011)"
        ],
        burden_holder="Government agency",
        adversary_position="Technique is publicly known or risk is speculative.",
        counter_arguments=[
            "Technique is not secret.",
            "No real risk of circumvention.",
            "Agency justification is insufficient."
        ],
        resolution_strategy="Require agency explanation, assess public knowledge, apply deference but scrutinize claims.",
        entity_scope="Law enforcement and regulatory agencies.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Blackwell v. FBI, 646 F.3d 37 (D.C. Cir. 2011)"
    ),
    DoctrineBlock(
        topic="Vaughn Index Requirement",
        keywords=["Vaughn index", "justification", "FOIA litigation", "exemption", "segregability"],
        conclusion_template="Agencies must provide a detailed Vaughn index justifying each withholding.",
        reasoning_framework=(
            "In FOIA litigation, agencies must provide a Vaughn index, which is a detailed itemization and justification "
            "for each withheld or redacted record. The index must describe the document, the exemption claimed, and "
            "the rationale for withholding, sufficient for the court and requester to assess the claim. Courts may "
            "order in camera review if the index is inadequate. The Vaughn index ensures transparency and enables "
            "meaningful judicial review."
        ),
        key_factors=[
            "Specificity of descriptions",
            "Clarity of exemption claims",
            "Adequacy for judicial review",
            "Segregability analysis"
        ],
        primary_authority=[
            "Vaughn v. Rosen, 484 F.2d 820 (D.C. Cir. 1973)",
            "FOIA litigation practice"
        ],
        burden_holder="Government agency",
        adversary_position="Index is vague, conclusory, or insufficient for review.",
        counter_arguments=[
            "Descriptions are too general.",
            "Exemption claims are not justified.",
            "Segregability is not addressed."
        ],
        resolution_strategy="Require detailed, document-by-document index, order in camera review if necessary.",
        entity_scope="All agencies in FOIA litigation.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Vaughn v. Rosen, 484 F.2d 820 (D.C. Cir. 1973)"
    ),
    DoctrineBlock(
        topic="Expedited Processing",
        keywords=["expedited", "urgency", "FOIA", "compelling need", "public interest"],
        conclusion_template="Expedited processing must be granted if the request demonstrates a compelling need.",
        reasoning_framework=(
            "FOIA provides for expedited processing of requests upon a showing of compelling need, such as imminent "
            "threat to life or the urgency to inform the public about actual or alleged government activity. Agencies "
            "must decide on expedited processing within 10 calendar days. Courts require agencies to apply the "
            "standard consistently and provide reasons for denial. Journalists and public interest groups often "
            "invoke this provision."
        ),
        key_factors=[
            "Nature of the need",
            "Imminence of harm",
            "Public interest in information",
            "Timeliness of agency response"
        ],
        primary_authority=[
            "5 U.S.C. § 552(a)(6)(E)",
            "Al-Fayed v. CIA, 254 F.3d 300 (D.C. Cir. 2001)"
        ],
        burden_holder="Requester",
        adversary_position="No compelling need or urgency exists.",
        counter_arguments=[
            "Request does not meet statutory criteria.",
            "No imminent harm or urgency.",
            "Information is not time-sensitive."
        ],
        resolution_strategy="Apply statutory criteria, require agency explanation, allow judicial review.",
        entity_scope="All agencies subject to FOIA.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Al-Fayed v. CIA, 254 F.3d 300 (D.C. Cir. 2001)"
    ),
    DoctrineBlock(
        topic="Fee Waiver Standard",
        keywords=["fee waiver", "public interest", "FOIA", "disclosure", "significant contribution"],
        conclusion_template="Fees must be waived if disclosure is in the public interest and not primarily for commercial benefit.",
        reasoning_framework=(
            "FOIA permits agencies to waive fees if disclosure is likely to contribute significantly to public "
            "understanding of government operations and is not primarily in the commercial interest of the requester. "
            "The analysis considers the subject of the request, the informative value, the contribution to public "
            "understanding, and the requester's commercial interest. Courts require agencies to articulate reasons "
            "for denial and favor waivers for journalists and public interest groups."
        ),
        key_factors=[
            "Subject and informative value",
            "Contribution to public understanding",
            "Requester's commercial interest",
            "Agency justification"
        ],
        primary_authority=[
            "5 U.S.C. § 552(a)(4)(A)(iii)",
            "Judicial Watch, Inc. v. Rossotti, 326 F.3d 1309 (D.C. Cir. 2003)"
        ],
        burden_holder="Requester",
        adversary_position="Disclosure is primarily for commercial benefit.",
        counter_arguments=[
            "Request is for commercial gain.",
            "No significant contribution to public understanding.",
            "Subject matter is not of public interest."
        ],
        resolution_strategy="Apply statutory factors, require agency explanation, allow judicial review.",
        entity_scope="All agencies subject to FOIA.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Judicial Watch, Inc. v. Rossotti, 326 F.3d 1309 (D.C. Cir. 2003)"
    ),
    DoctrineBlock(
        topic="Agency Search Adequacy",
        keywords=["search", "adequacy", "reasonable", "FOIA", "good faith"],
        conclusion_template="An agency's search is adequate if it is reasonably calculated to uncover all relevant documents.",
        reasoning_framework=(
            "FOIA requires agencies to conduct a search reasonably calculated to uncover all relevant documents. "
            "The adequacy of the search is judged by the methods used, not the results. Agencies must search all "
            "locations likely to contain responsive records and provide affidavits describing their efforts. "
            "Courts defer to agency affidavits if made in good faith but may order further search if evidence shows "
            "the search was inadequate."
        ),
        key_factors=[
            "Scope of search",
            "Methods and locations searched",
            "Agency affidavits",
            "Evidence of missing records"
        ],
        primary_authority=[
            "Oglesby v. U.S. Dep't of Army, 920 F.2d 57 (D.C. Cir. 1990)",
            "5 U.S.C. § 552(a)(3)"
        ],
        burden_holder="Government agency",
        adversary_position="Search was inadequate or failed to locate all responsive records.",
        counter_arguments=[
            "Agency failed to search all likely locations.",
            "Affidavits are conclusory.",
            "Evidence suggests additional records exist."
        ],
        resolution_strategy="Review agency affidavits, require detail, order supplemental search if necessary.",
        entity_scope="All agencies subject to FOIA.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Oglesby v. U.S. Dep't of Army, 920 F.2d 57 (D.C. Cir. 1990)"
    ),
    DoctrineBlock(
        topic="Constructive Denial and Agency Delay",
        keywords=["delay", "constructive denial", "FOIA", "timeliness", "litigation"],
        conclusion_template="Unreasonable agency delay constitutes constructive denial and may be challenged in court.",
        reasoning_framework=(
            "FOIA sets statutory deadlines for agency responses to requests. If an agency fails to comply within the "
            "time limits, the requester is deemed to have exhausted administrative remedies and may file suit. "
            "Courts may order prompt disclosure or set deadlines for compliance. Agencies may justify delay by "
            "demonstrating unusual circumstances, but excessive delay is disfavored."
        ),
        key_factors=[
            "Length of delay",
            "Agency explanation",
            "Complexity of request",
            "Efforts to comply"
        ],
        primary_authority=[
            "5 U.S.C. § 552(a)(6)(C)",
            "Judicial Watch, Inc. v. U.S. Dep't of Homeland Security, 895 F.3d 770 (D.C. Cir. 2018)"
        ],
        burden_holder="Requester",
        adversary_position="Delay is justified by unusual circumstances.",
        counter_arguments=[
            "Delay is excessive and unjustified.",
            "Agency has not communicated status.",
            "Request is not unusually complex."
        ],
        resolution_strategy="Assess reasonableness of delay, require agency explanation, allow judicial remedy.",
        entity_scope="All agencies subject to FOIA.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Judicial Watch, Inc. v. U.S. Dep't of Homeland Security, 895 F.3d 770 (D.C. Cir. 2018)"
    ),
    DoctrineBlock(
        topic="Presidential Records Act",
        keywords=["PRA", "presidential records", "FOIA", "White House", "archival"],
        conclusion_template="Presidential records are governed by the PRA, not FOIA, and have unique access provisions.",
        reasoning_framework=(
            "The Presidential Records Act (PRA) governs the preservation and public access to presidential records. "
            "FOIA does not apply to presidential records; instead, the PRA provides a separate framework, including "
            "timelines for public access and specific exemptions. The National Archives administers access, and "
            "records become available after the President leaves office, subject to restrictions for up to 12 years."
        ),
        key_factors=[
            "Nature of the records",
            "Custody by National Archives",
            "Timing of request",
            "PRA restrictions"
        ],
        primary_authority=[
            "44 U.S.C. §§ 2201-2207",
            "Presidential Records Act"
        ],
        burden_holder="Requester",
        adversary_position="Records are not subject to PRA or are still restricted.",
        counter_arguments=[
            "Records are not presidential in nature.",
            "Access restrictions have expired.",
            "FOIA does not apply."
        ],
        resolution_strategy="Determine record status, apply PRA, consult National Archives.",
        entity_scope="Presidential records held by National Archives.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Judicial Watch, Inc. v. National Archives & Records Admin., 845 F. Supp. 2d 288 (D.D.C. 2012)"
    ),
    DoctrineBlock(
        topic="Exemption 2: Internal Personnel Rules",
        keywords=["FOIA Exemption 2", "internal", "personnel", "rules", "practices"],
        conclusion_template="Internal personnel rules and practices may be withheld if they are trivial or risk circumvention.",
        reasoning_framework=(
            "Exemption 2 allows agencies to withhold information related solely to the internal personnel rules and "
            "practices of an agency. Courts distinguish between 'low 2' (trivial administrative matters) and 'high 2' "
            "(information that, if disclosed, would risk circumvention of agency regulation). The Supreme Court in "
            "Milner v. Department of the Navy narrowed the scope to cover only trivial administrative matters."
        ),
        key_factors=[
            "Nature of the rule or practice",
            "Risk of circumvention",
            "Triviality",
            "Public interest"
        ],
        primary_authority=[
            "5 U.S.C. § 552(b)(2)",
            "Milner v. Department of the Navy, 562 U.S. 562 (2011)"
        ],
        burden_holder="Government agency",
        adversary_position="Information is not trivial or does not risk circumvention.",
        counter_arguments=[
            "Information is substantive, not administrative.",
            "No risk of circumvention.",
            "Public interest outweighs agency interest."
        ],
        resolution_strategy="Apply Milner standard, distinguish between trivial and substantive information.",
        entity_scope="All agencies subject to FOIA.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Milner v. Department of the Navy, 562 U.S. 562 (2011)"
    ),
    DoctrineBlock(
        topic="Exemption 6: Personnel, Medical, and Similar Files",
        keywords=["FOIA Exemption 6", "personnel files", "medical files", "privacy", "unwarranted invasion"],
        conclusion_template="Personnel, medical, and similar files may be withheld if disclosure would be a clearly unwarranted invasion of privacy.",
        reasoning_framework=(
            "Exemption 6 protects personnel, medical, and similar files from disclosure if it would constitute a "
            "clearly unwarranted invasion of personal privacy. The analysis balances the individual's privacy against "
            "the public interest in disclosure, with privacy interests given significant weight. The exemption is "
            "interpreted broadly to cover any information that applies to a particular individual."
        ),
        key_factors=[
            "Nature of the information",
            "Identifiability of individuals",
            "Magnitude of privacy interest",
            "Public interest in disclosure"
        ],
        primary_authority=[
            "5 U.S.C. § 552(b)(6)",
            "Department of State v. Washington Post Co., 456 U.S. 595 (1982)"
        ],
        burden_holder="Government agency",
        adversary_position="Public interest in disclosure outweighs privacy interest.",
        counter_arguments=[
            "Information is not a personnel or similar file.",
            "Redaction can protect privacy.",
            "Public interest is compelling."
        ],
        resolution_strategy="Balance privacy and public interests, consider redaction, apply statutory language.",
        entity_scope="All agencies holding personnel or similar records.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Department of State v. Washington Post Co., 456 U.S. 595 (1982)"
    ),
    DoctrineBlock(
        topic="Exemption 8: Financial Institutions",
        keywords=["FOIA Exemption 8", "financial", "examination", "bank", "confidential"],
        conclusion_template="Information related to the regulation or supervision of financial institutions may be withheld.",
        reasoning_framework=(
            "Exemption 8 protects information contained in or related to examination, operation, or condition reports "
            "prepared by, on behalf of, or for the use of an agency responsible for the regulation or supervision of "
            "financial institutions. The exemption is interpreted broadly to encourage candor in regulatory "
            "communications and protect the stability of financial institutions."
        ),
        key_factors=[
            "Nature of the information",
            "Relationship to financial institution supervision",
            "Potential harm from disclosure",
            "Regulatory context"
        ],
        primary_authority=[
            "5 U.S.C. § 552(b)(8)",
            "Consumers Union of U.S., Inc. v. Heimann, 589 F.2d 531 (D.C. Cir. 1978)"
        ],
        burden_holder="Government agency",
        adversary_position="Information is not related to supervision or no harm would result.",
        counter_arguments=[
            "Information is not within scope of exemption.",
            "No risk to financial stability.",
            "Public interest outweighs harm."
        ],
        resolution_strategy="Apply exemption broadly, protect regulatory communications, consider public interest.",
        entity_scope="Financial regulatory agencies.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Consumers Union of U.S., Inc. v. Heimann, 589 F.2d 531 (D.C. Cir. 1978)"
    ),
    DoctrineBlock(
        topic="Exemption 9: Geological and Geophysical Data",
        keywords=["FOIA Exemption 9", "geological", "geophysical", "wells", "confidential"],
        conclusion_template="Geological and geophysical information concerning wells may be withheld.",
        reasoning_framework=(
            "Exemption 9 protects geological and geophysical information and data, including maps, concerning wells. "
            "The exemption is intended to protect proprietary interests and prevent competitive harm in the oil, gas, "
            "and mineral industries. The scope is limited to information directly related to wells."
        ),
        key_factors=[
            "Nature of the information",
            "Relationship to wells",
            "Proprietary interest",
            "Potential competitive harm"
        ],
        primary_authority=[
            "5 U.S.C. § 552(b)(9)",
            "FOIA legislative history"
        ],
        burden_holder="Government agency",
        adversary_position="Information is not related to wells or is not proprietary.",
        counter_arguments=[
            "Information is not within scope of exemption.",
            "No competitive harm.",
            "Public interest outweighs harm."
        ],
        resolution_strategy="Apply exemption narrowly, confirm relationship to wells, consider competitive interests.",
        entity_scope="Agencies regulating natural resources.",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="No controlling Supreme Court precedent"
    ),
    DoctrineBlock(
        topic="Reverse FOIA Actions",
        keywords=["reverse FOIA", "confidentiality", "business information", "injunction", "trade secret"],
        conclusion_template="Submitters may seek judicial review to prevent agency disclosure of confidential information.",
        reasoning_framework=(
            "Reverse FOIA actions allow submitters of confidential business information to challenge an agency's "
            "decision to disclose information under FOIA. Courts review whether the agency's decision was arbitrary, "
            "capricious, or contrary to law, focusing on whether the information is protected by Exemption 4 or other "
            "statutory provisions. The submitter bears the burden of demonstrating confidentiality and competitive harm."
        ),
        key_factors=[
            "Nature of the information",
            "Confidentiality",
            "Competitive harm",
            "Agency decision process"
        ],
        primary_authority=[
            "Chrysler Corp. v. Brown, 441 U.S. 281 (1979)",
            "5 U.S.C. § 552(b)(4)"
        ],
        burden_holder="Submitter",
        adversary_position="Information is not confidential or no competitive harm exists.",
        counter_arguments=[
            "Information is public or not confidential.",
            "No competitive harm.",
            "Agency followed proper procedures."
        ],
        resolution_strategy="Apply APA standard of review, require evidence of confidentiality and harm.",
        entity_scope="All agencies receiving business information.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Chrysler Corp. v. Brown, 441 U.S. 281 (1979)"
    ),
    DoctrineBlock(
        topic="Glomar Response",
        keywords=["Glomar", "neither confirm nor deny", "existence", "national security", "FOIA"],
        conclusion_template="Agencies may refuse to confirm or deny the existence of records if acknowledgment would itself reveal exempt information.",
        reasoning_framework=(
            "A Glomar response allows an agency to neither confirm nor deny the existence of records if doing so would "
            "itself reveal information protected by an exemption, such as national security or privacy. Courts require "
            "the agency to demonstrate that the mere acknowledgment would cause harm protected by the exemption. The "
            "response is subject to judicial review for adequacy and justification."
        ),
        key_factors=[
            "Nature of the request",
            "Potential harm from acknowledgment",
            "Applicability of exemption",
            "Agency justification"
        ],
        primary_authority=[
            "Phillippi v. CIA, 546 F.2d 1009 (D.C. Cir. 1976)",
            "5 U.S.C. § 552"
        ],
        burden_holder="Government agency",
        adversary_position="Acknowledgment would not cause harm or exemption does not apply.",
        counter_arguments=[
            "No harm from acknowledgment.",
            "Exemption is inapplicable.",
            "Agency justification is insufficient."
        ],
        resolution_strategy="Require detailed agency justification, apply exemption, allow judicial review.",
        entity_scope="Agencies handling sensitive information.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Phillippi v. CIA, 546 F.2d 1009 (D.C. Cir. 1976)"
    ),
    DoctrineBlock(
        topic="Proactive Disclosure",
        keywords=["proactive disclosure", "reading room", "electronic records", "FOIA", "agency website"],
        conclusion_template="Agencies must proactively disclose frequently requested records and other specified categories.",
        reasoning_framework=(
            "FOIA requires agencies to make certain records available for public inspection in electronic reading rooms, "
            "including final opinions, policy statements, administrative staff manuals, and records requested three or "
            "more times. Agencies must update disclosures regularly and provide electronic access. Failure to comply "
            "may result in judicial orders to compel disclosure."
        ),
        key_factors=[
            "Nature of the record",
            "Frequency of requests",
            "Electronic availability",
            "Agency compliance"
        ],
        primary_authority=[
            "5 U.S.C. § 552(a)(2)",
            "E-FOIA Amendments of 1996"
        ],
        burden_holder="Government agency",
        adversary_position="Records are not subject to proactive disclosure or are already available.",
        counter_arguments=[
            "Record is not covered by statute.",
            "Agency has not disclosed as required.",
            "Electronic access is inadequate."
        ],
        resolution_strategy="Review statutory categories, require agency compliance, allow judicial enforcement.",
        entity_scope="All agencies subject to FOIA.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="No controlling Supreme Court precedent"
    ),
    DoctrineBlock(
        topic="FOIA Administrative Appeal",
        keywords=["administrative appeal", "FOIA", "exhaustion", "agency decision", "timeliness"],
        conclusion_template="Requesters must exhaust administrative remedies before seeking judicial review.",
        reasoning_framework=(
            "FOIA requires requesters to appeal adverse agency decisions through administrative channels before filing "
            "suit. The appeal must be timely and comply with agency procedures. Failure to exhaust remedies may result "
            "in dismissal of the lawsuit. Agencies must respond to appeals within statutory deadlines."
        ),
        key_factors=[
            "Timeliness of appeal",
            "Compliance with agency procedures",
            "Agency response",
            "Exhaustion of remedies"
        ],
        primary_authority=[
            "5 U.S.C. § 552(a)(6)",
            "Hidalgo v. FBI, 344 F.3d 1256 (D.C. Cir. 2003)"
        ],
        burden_holder="Requester",
        adversary_position="Remedies are not exhausted or appeal is untimely.",
        counter_arguments=[
            "Appeal was timely and proper.",
            "Agency failed to respond.",
            "Statutory deadlines were not met."
        ],
        resolution_strategy="Verify exhaustion, review timeliness, allow judicial review if remedies are exhausted.",
        entity_scope="All agencies subject to FOIA.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Hidalgo v. FBI, 344 F.3d 1256 (D.C. Cir. 2003)"
    ),
    DoctrineBlock(
        topic="Attorney Fees and Litigation Costs",
        keywords=["attorney fees", "litigation costs", "FOIA", "substantially prevailed", "court order"],
        conclusion_template="Courts may award attorney fees and costs if the requester substantially prevails in litigation.",
        reasoning_framework=(
            "FOIA authorizes courts to award reasonable attorney fees and litigation costs to requesters who "
            "substantially prevail in litigation. Substantial prevailing may be shown by a court order or a voluntary "
            "change in agency position. Courts consider factors such as the public benefit, commercial interest, and "
            "reasonableness of the agency's position in awarding fees."
        ),
        key_factors=[
            "Substantial prevailing",
            "Court order or voluntary change",
            "Public benefit",
            "Reasonableness of agency position"
        ],
        primary_authority=[
            "5 U.S.C. § 552(a)(4)(E)",
            "Buckhannon Board & Care Home, Inc. v. West Virginia Dep't of Health and Human Resources, 532 U.S. 598 (2001)"
        ],
        burden_holder="Requester",
        adversary_position="Requester did not substantially prevail or fees are unreasonable.",
        counter_arguments=[
            "No court order or change in position.",
            "Fees are excessive.",
            "Agency acted reasonably."
        ],
        resolution_strategy="Apply statutory factors, assess prevailing status, determine reasonable fees.",
        entity_scope="All agencies subject to FOIA litigation.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Buckhannon Board & Care Home, Inc. v. West Virginia Dep't of Health and Human Resources, 532 U.S. 598 (2001)"
    ),
    DoctrineBlock(
        topic="Sunshine Act Open Meetings",
        keywords=["Sunshine Act", "open meetings", "government transparency", "public access", "federal agencies"],
        conclusion_template="Federal agency meetings must be open to the public unless a statutory exemption applies.",
        reasoning_framework=(
            "The Government in the Sunshine Act requires that meetings of federal agencies be open to public "
            "observation, subject to specific exemptions such as national security, internal personnel matters, or "
            "law enforcement investigations. Agencies must provide advance notice and justify any closure. The Act "
            "promotes transparency and public participation in government decision-making."
        ),
        key_factors=[
            "Nature of the meeting",
            "Applicability of exemptions",
            "Notice requirements",
            "Public interest"
        ],
        primary_authority=[
            "5 U.S.C. § 552b",
            "Government in the Sunshine Act"
        ],
        burden_holder="Agency",
        adversary_position="Exemption does not apply or notice was inadequate.",
        counter_arguments=[
            "Meeting is not covered by exemption.",
            "Public interest outweighs need for closure.",
            "Notice requirements were not met."
        ],
        resolution_strategy="Review statutory exemptions, require agency justification, ensure compliance with notice.",
        entity_scope="Federal agencies subject to Sunshine Act.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="No controlling Supreme Court precedent"
    ),
    DoctrineBlock(
        topic="Privacy Act Interaction with FOIA",
        keywords=["Privacy Act", "FOIA", "personal information", "disclosure", "exemptions"],
        conclusion_template="Disclosure of personal information is governed by both FOIA and the Privacy Act; the more restrictive rule applies.",
        reasoning_framework=(
            "The Privacy Act and FOIA both regulate disclosure of personal information held by federal agencies. "
            "When both statutes apply, courts generally apply the more restrictive rule to protect privacy. "
            "FOIA exemptions may justify withholding, while the Privacy Act may prohibit disclosure absent consent "
            "or statutory exception. Agencies must analyze both statutes before releasing information."
        ),
        key_factors=[
            "Nature of the information",
            "Applicability of both statutes",
            "Consent or statutory exception",
            "Public interest"
        ],
        primary_authority=[
            "5 U.S.C. § 552a",
            "5 U.S.C. § 552",
            "Department of Defense v. FLRA, 510 U.S. 487 (1994)"
        ],
        burden_holder="Agency",
        adversary_position="Disclosure is not prohibited by either statute.",
        counter_arguments=[
            "Consent has been given.",
            "No Privacy Act prohibition applies.",
            "FOIA exemption is not justified."
        ],
        resolution_strategy="Apply both statutes, use more restrictive rule, document analysis.",
        entity_scope="All agencies subject to FOIA and Privacy Act.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Department of Defense v. FLRA, 510 U.S. 487 (1994)"
    ),
    DoctrineBlock(
        topic="FOIA and State Open Records Laws",
        keywords=["state law", "open records", "FOIA", "preemption", "public access"],
        conclusion_template="FOIA applies to federal agencies; state open records laws govern state and local entities.",
        reasoning_framework=(
            "FOIA applies only to federal executive branch agencies. State and local government records are governed "
            "by state open records laws, which may differ in scope, exemptions, and procedures. FOIA does not preempt "
            "state law, and requesters must use the appropriate statute for the entity in question."
        ),
        key_factors=[
            "Jurisdiction of the agency",
            "Nature of the records",
            "Applicable state law",
            "Preemption issues"
        ],
        primary_authority=[
            "5 U.S.C. § 552",
            "Relevant state open records statutes"
        ],
        burden_holder="Requester",
        adversary_position="Wrong statute invoked or records are not federal.",
        counter_arguments=[
            "Records are held by federal agency.",
            "FOIA does not apply to state/local records.",
            "State law provides for access."
        ],
        resolution_strategy="Determine jurisdiction, apply correct statute, advise requester.",
        entity_scope="Federal, state, and local agencies.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="No controlling Supreme Court precedent"
    ),
    DoctrineBlock(
        topic="Exemption 7(A): Pending Law Enforcement Proceedings",
        keywords=["FOIA Exemption 7(A)", "pending investigation", "interference", "law enforcement", "records"],
        conclusion_template="Records may be withheld if disclosure could reasonably be expected to interfere with pending law enforcement proceedings.",
        reasoning_framework=(
            "Exemption 7(A) allows agencies to withhold law enforcement records if disclosure could reasonably be "
            "expected to interfere with pending investigations or proceedings. The agency must show how disclosure "
            "would cause harm, such as revealing strategy, compromising evidence, or endangering witnesses. The "
            "exemption applies only while proceedings are pending."
        ),
        key_factors=[
            "Existence of pending proceedings",
            "Nature of the harm",
            "Specificity of agency justification",
            "Timing of request"
        ],
        primary_authority=[
            "5 U.S.C. § 552(b)(7)(A)",
            "NLRB v. Robbins Tire & Rubber Co., 437 U.S. 214 (1978)"
        ],
        burden_holder="Government agency",
        adversary_position="No pending proceedings or harm is speculative.",
        counter_arguments=[
            "Proceedings have concluded.",
            "No specific harm is articulated.",
            "Information is already public."
        ],
        resolution_strategy="Require agency explanation, assess pending status, apply exemption strictly.",
        entity_scope="Law enforcement and regulatory agencies.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="NLRB v. Robbins Tire & Rubber Co., 437 U.S. 214 (1978)"
    ),
    DoctrineBlock(
        topic="Exemption 7(D): Confidential Sources",
        keywords=["FOIA Exemption 7(D)", "confidential source", "law enforcement", "informant", "assurance of confidentiality"],
        conclusion_template="Information identifying confidential sources may be withheld if provided under an express or implied assurance of confidentiality.",
        reasoning_framework=(
            "Exemption 7(D) protects the identity of confidential sources who provide information to law enforcement. "
            "The agency must show that the source received an express or implied assurance of confidentiality. Courts "
            "consider the nature of the crime, the circumstances of the communication, and agency practice. The "
            "exemption also protects information that would reveal the source's identity."
        ),
        key_factors=[
            "Assurance of confidentiality",
            "Nature of the crime",
            "Circumstances of communication",
            "Potential harm to source"
        ],
        primary_authority=[
            "5 U.S.C. § 552(b)(7)(D)",
            "U.S. Dep't of Justice v. Landano, 508 U.S. 165 (1993)"
        ],
        burden_holder="Government agency",
        adversary_position="No assurance of confidentiality or source is not at risk.",
        counter_arguments=[
            "No assurance was given.",
            "Source is not confidential.",
            "Information is already public."
        ],
        resolution_strategy="Assess assurance, review circumstances, protect source identity.",
        entity_scope="Law enforcement and regulatory agencies.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="U.S. Dep't of Justice v. Landano, 508 U.S. 165 (1993)"
    ),
    DoctrineBlock(
        topic="Exemption 7(F): Endangerment to Life or Safety",
        keywords=["FOIA Exemption 7(F)", "endangerment", "life", "safety", "law enforcement"],
        conclusion_template="Information may be withheld if disclosure could reasonably be expected to endanger the life or safety of any individual.",
        reasoning_framework=(
            "Exemption 7(F) allows agencies to withhold law enforcement information if disclosure could endanger the "
            "life or physical safety of any individual. The agency must articulate a reasonable expectation of harm, "
            "which may include threats to witnesses, law enforcement personnel, or others. Courts require a logical "
            "connection between disclosure and risk."
        ),
        key_factors=[
            "Nature of the threat",
            "Identifiability of individuals",
            "Specificity of agency justification",
            "Potential harm"
        ],
        primary_authority=[
            "5 U.S.C. § 552(b)(7)(F)",
            "FOIA legislative history"
        ],
        burden_holder="Government agency",
        adversary_position="Risk is speculative or no individual is endangered.",
        counter_arguments=[
            "No specific threat exists.",
            "Information is not identifying.",
            "Agency justification is insufficient."
        ],
        resolution_strategy="Require agency explanation, assess risk, apply exemption strictly.",
        entity_scope="Law enforcement and regulatory agencies.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="No controlling Supreme Court precedent"
    ),
    DoctrineBlock(
        topic="FOIA and Electronic Records",
        keywords=["electronic records", "E-FOIA", "search", "format", "agency obligations"],
        conclusion_template="Agencies must provide electronic records in any format requested if readily reproducible.",
        reasoning_framework=(
            "The E-FOIA Amendments require agencies to provide records in any form or format requested if the record is "
            "readily reproducible in that format. Agencies must search electronic databases and provide metadata if "
            "available. The obligation extends to emails, databases, and other electronic files. Agencies may not "
            "deny requests solely because of format."
        ),
        key_factors=[
            "Requested format",
            "Reproducibility",
            "Agency technical capability",
            "Nature of electronic record"
        ],
        primary_authority=[
            "5 U.S.C. § 552(a)(3)(B)-(C)",
            "E-FOIA Amendments of 1996"
        ],
        burden_holder="Government agency",
        adversary_position="Record is not readily reproducible or format is burdensome.",
        counter_arguments=[
            "Format is readily available.",
            "Agency has technical capability.",
            "No undue burden exists."
        ],
        resolution_strategy="Assess reproducibility, require agency explanation, provide in requested format if feasible.",
        entity_scope="All agencies subject to FOIA.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="No controlling Supreme Court precedent"
    ),
    DoctrineBlock(
        topic="FOIA and Contractor Records",
        keywords=["contractor", "records", "agency control", "FOIA", "outsourcing"],
        conclusion_template="Records in the possession of government contractors may be subject to FOIA if under agency control.",
        reasoning_framework=(
            "FOIA applies to records created or obtained by government contractors if the agency controls the records. "
            "Courts examine the agency's ability to direct the use, retention, and disposition of the records. "
            "Records maintained solely for contractor business are not subject to FOIA. Agencies must ensure contract "
            "terms provide for agency access and control."
        ),
        key_factors=[
            "Agency control",
            "Purpose of the record",
            "Contract terms",
            "Integration into agency files"
        ],
        primary_authority=[
            "5 U.S.C. § 552(f)",
            "Department of Justice v. Tax Analysts, 492 U.S. 136 (1989)"
        ],
        burden_holder="Requester",
        adversary_position="Records are not under agency control or are contractor business records.",
        counter_arguments=[
            "Agency has access and control.",
            "Records are used for agency business.",
            "Contract terms require agency access."
        ],
        resolution_strategy="Review contract terms, assess agency control, apply FOIA definition.",
        entity_scope="All agencies using contractors.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Department of Justice v. Tax Analysts, 492 U.S. 136 (1989)"
    ),
    DoctrineBlock(
        topic="FOIA and National Security Letters",
        keywords=["national security letter", "NSL", "FOIA", "gag order", "disclosure"],
        conclusion_template="Records related to NSLs may be withheld under national security and law enforcement exemptions.",
        reasoning_framework=(
            "National Security Letters (NSLs) are administrative subpoenas issued by federal agencies for national "
            "security investigations. Records related to NSLs may be withheld under FOIA Exemption 1 (national "
            "security) and Exemption 7 (law enforcement). Agencies may also issue gag orders prohibiting disclosure. "
            "Courts review the justification for withholding and the necessity of any gag order."
        ),
        key_factors=[
            "Nature of the NSL",
            "National security interest",
            "Law enforcement interest",
            "Agency justification"
        ],
        primary_authority=[
            "18 U.S.C. §§ 2709, 3511",
            "5 U.S.C. § 552(b)(1), (7)"
        ],
        burden_holder="Government agency",
        adversary_position="No national security or law enforcement interest justifies withholding.",
        counter_arguments=[
            "No harm from disclosure.",
            "Gag order is not justified.",
            "Information is not classified."
        ],
        resolution_strategy="Review agency justification, apply relevant exemptions, allow judicial review.",
        entity_scope="Agencies authorized to issue NSLs.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="No controlling Supreme Court precedent"
    ),
    DoctrineBlock(
        topic="FOIA and Congressional Records",
        keywords=["congressional records", "FOIA", "legislative branch", "separation of powers"],
        conclusion_template="FOIA does not apply to congressional records; access is governed by congressional rules.",
        reasoning_framework=(
            "FOIA applies only to executive branch agencies. Congressional records are excluded from FOIA's scope, "
            "reflecting the separation of powers. Access to congressional records is governed by internal rules and "
            "procedures of the House and Senate. Courts have consistently rejected FOIA claims for legislative records."
        ),
        key_factors=[
            "Nature of the record",
            "Custody by legislative branch",
            "Congressional rules",
            "Separation of powers"
        ],
        primary_authority=[
            "5 U.S.C. § 551(1)",
            "Kissinger v. Reporters Committee, 445 U.S. 136 (1980)"
        ],
        burden_holder="Requester",
        adversary_position="Record is not a congressional record or is held by an agency.",
        counter_arguments=[
            "Record is held by executive agency.",
            "Congressional rules permit access.",
            "FOIA does not apply."
        ],
        resolution_strategy="Determine record custody, apply FOIA definition, refer to congressional rules.",
        entity_scope="Congressional records.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Kissinger v. Reporters Committee, 445 U.S. 136 (1980)"
    ),
    DoctrineBlock(
        topic="FOIA and Judicial Records",
        keywords=["judicial records", "FOIA", "court records", "separation of powers"],
        conclusion_template="FOIA does not apply to judicial records; access is governed by court rules.",
        reasoning_framework=(
            "FOIA does not apply to records of the federal judiciary. Access to judicial records is governed by "
            "court rules, local procedures, and the common law right of access. Courts have consistently held that "
            "judicial records are not agency records under FOIA."
        ),
        key_factors=[
            "Nature of the record",
            "Custody by judiciary",
            "Court rules",
            "Separation of powers"
        ],
        primary_authority=[
            "5 U.S.C. § 551(1)",
            "United States v. El-Sayegh, 131 F.3d 158 (D.C. Cir. 1997)"
        ],
        burden_holder="Requester",
        adversary_position="Record is not a judicial record or is held by an agency.",
        counter_arguments=[
            "Record is held by executive agency.",
            "Court rules permit access.",
            "FOIA does not apply."
        ],
        resolution_strategy="Determine record custody, apply FOIA definition, refer to court rules.",
        entity_scope="Judicial records.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="United States v. El-Sayegh, 131 F.3d 158 (D.C. Cir. 1997)"
    ),
    DoctrineBlock(
        topic="FOIA and Third-Party Requests",
        keywords=["third-party", "request", "FOIA", "privacy", "authorization"],
        conclusion_template="Agencies may require authorization or proof of death for third-party requests for personal information.",
        reasoning_framework=(
            "When a FOIA request seeks personal information about a third party, agencies may require written "
            "authorization from the individual or proof of death. This practice protects privacy interests and "
            "complies with Exemptions 6 and 7(C). Without authorization, agencies may withhold information or issue "
            "a Glomar response."
        ),
        key_factors=[
            "Nature of the information",
            "Authorization or proof of death",
            "Privacy interest",
            "Public interest"
        ],
        primary_authority=[
            "5 U.S.C. § 552(b)(6), (7)(C)",
            "Department of Justice v. Reporters Committee, 489 U.S. 749 (1989)"
        ],
        burden_holder="Requester",
        adversary_position="No authorization or proof of death provided.",
        counter_arguments=[
            "Public interest outweighs privacy.",
            "Authorization is not required.",
            "Information is already public."
        ],
        resolution_strategy="Require authorization or proof, balance privacy and public interest, apply exemptions.",
        entity_scope="All agencies subject to FOIA.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Department of Justice v. Reporters Committee, 489 U.S. 749 (1989)"
    ),
    DoctrineBlock(
        topic="FOIA and Redaction Standards",
        keywords=["redaction", "segregability", "FOIA", "partial disclosure", "justification"],
        conclusion_template="Agencies must redact only exempt information and disclose all reasonably segregable material.",
        reasoning_framework=(
            "FOIA requires agencies to redact only the portions of records that are exempt, providing all reasonably "
            "segregable non-exempt information. Agencies must justify redactions and demonstrate that further "
            "segregation is not possible. Courts may review redactions in camera and require detailed explanations."
        ),
        key_factors=[
            "Nature of exempt and non-exempt material",
            "Feasibility of redaction",
            "Agency justification",
            "Judicial review"
        ],
        primary_authority=[
            "5 U.S.C. § 552(b)",
            "Department of Justice v. Julian, 486 U.S. 1 (1988)"
        ],
        burden_holder="Government agency",
        adversary_position="Non-exempt information can be segregated and disclosed.",
        counter_arguments=[
            "Redaction is feasible.",
            "Agency has not justified withholding.",
            "Court review is warranted."
        ],
        resolution_strategy="Require detailed justification, order in camera review if necessary, favor disclosure.",
        entity_scope="All agencies subject to FOIA.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Department of Justice v. Julian, 486 U.S. 1 (1988)"
    ),
    DoctrineBlock(
        topic="FOIA and Agency Regulations",
        keywords=["agency regulations", "FOIA", "procedures", "compliance", "publication"],
        conclusion_template="Agencies must publish FOIA regulations specifying procedures for requests and appeals.",
        reasoning_framework=(
            "FOIA requires agencies to publish regulations describing the procedures for submitting requests, "
            "appeals, and fee schedules. Agencies must comply with their own regulations, and failure to do so may "
            "result in judicial remedies. Regulations must be published in the Federal Register and made available "
            "to the public."
        ),
        key_factors=[
            "Publication of regulations",
            "Compliance with procedures",
            "Notice to public",
            "Judicial enforcement"
        ],
        primary_authority=[
            "5 U.S.C. § 552(a)(1), (a)(3)",
            "Federal Register Act"
        ],
        burden_holder="Agency",
        adversary_position="Agency failed to comply with regulations or did not publish procedures.",
        counter_arguments=[
            "Procedures are not published.",
            "Agency did not follow its own rules.",
            "Public was not notified."
        ],
        resolution_strategy="Review agency regulations, require compliance, allow judicial remedy.",
        entity_scope="All agencies subject to FOIA.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="No controlling Supreme Court precedent"
    ),
    DoctrineBlock(
        topic="FOIA and Data Breach Notification",
        keywords=["data breach", "notification", "FOIA", "personal information", "agency obligation"],
        conclusion_template="Agencies must consider privacy and security risks before disclosing breached data under FOIA.",
        reasoning_framework=(
            "When a FOIA request seeks information involved in a data breach, agencies must carefully assess privacy "
            "and security risks under Exemptions 6 and 7(C). Disclosure may further harm affected individuals. "
            "Agencies should consult with privacy officers and may notify affected individuals before disclosure. "
            "The public interest in disclosure must be balanced against privacy and security risks."
        ),
        key_factors=[
            "Nature of breached data",
            "Privacy and security risks",
            "Notification to affected individuals",
            "Public interest"
        ],
        primary_authority=[
            "5 U.S.C. § 552(b)(6), (7)(C)",
            "OMB Guidance on Data Breach Response"
        ],
        burden_holder="Agency",
        adversary_position="Public interest in disclosure outweighs privacy risk.",
        counter_arguments=[
            "Information is already public.",
            "Redaction can protect privacy.",
            "Notification is not required."
        ],
        resolution_strategy="Assess risks, consult privacy officers, balance interests, consider notification.",
        entity_scope="All agencies subject to FOIA.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="No controlling Supreme Court precedent"
    ),
    DoctrineBlock(
        topic="FOIA and Whistleblower Protections",
        keywords=["whistleblower", "protection", "FOIA", "confidentiality", "retaliation"],
        conclusion_template="Agencies must protect the identity of whistleblowers when responding to FOIA requests.",
        reasoning_framework=(
            "FOIA Exemptions 6 and 7(C) may justify withholding information that could identify whistleblowers, to "
            "protect against retaliation and encourage reporting of misconduct. Agencies must assess the risk of "
            "identification and may withhold or redact information accordingly. Courts support broad protection for "
            "whistleblower confidentiality."
        ),
        key_factors=[
            "Identifiability of whistleblower",
            "Risk of retaliation",
            "Public interest",
            "Agency justification"
        ],
        primary_authority=[
            "5 U.S.C. § 552(b)(6), (7)(C)",
            "Whistleblower Protection Act"
        ],
        burden_holder="Agency",
        adversary_position="Public interest outweighs need for confidentiality.",
        counter_arguments=[
            "Information is not identifying.",
            "No risk of retaliation.",
            "Public interest is compelling."
        ],
        resolution_strategy="Assess risk, redact identifying information, apply exemptions.",
        entity_scope="All agencies subject to FOIA.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="No controlling Supreme Court precedent"
    ),
    DoctrineBlock(
        topic="FOIA and Law Enforcement Dashcam/Bodycam Footage",
        keywords=["bodycam", "dashcam", "video", "FOIA", "privacy", "law enforcement"],
        conclusion_template="Disclosure of law enforcement video footage is subject to privacy, law enforcement, and evidentiary exemptions.",
        reasoning_framework=(
            "Requests for law enforcement dashcam or bodycam footage are analyzed under FOIA Exemptions 6, 7(C), and "
            "7(A). Agencies must balance privacy interests of individuals depicted, potential interference with "
            "ongoing investigations, and evidentiary concerns. Redaction of faces, voices, or other identifying "
            "features may be required. Courts favor disclosure when public interest in accountability is strong."
        ),
        key_factors=[
            "Identifiability of individuals",
            "Ongoing investigations",
            "Public interest",
            "Feasibility of redaction"
        ],
        primary_authority=[
            "5 U.S.C. § 552(b)(6), (7)(A), (7)(C)",
            "Relevant case law"
        ],
        burden_holder="Agency",
        adversary_position="Public interest in disclosure outweighs privacy or law enforcement concerns.",
        counter_arguments=[
            "Redaction can protect privacy.",
            "Investigation is concluded.",
            "Public interest is compelling."
        ],
        resolution_strategy="Balance interests, redact as necessary, apply exemptions.",
        entity_scope="Law enforcement agencies.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="No controlling Supreme Court precedent"
    ),
    DoctrineBlock(
        topic="FOIA and Artificial Intelligence Records",
        keywords=["artificial intelligence", "AI", "algorithms", "FOIA", "exemption", "source code"],
        conclusion_template="Disclosure of AI algorithms and source code may be limited by Exemptions 1, 3, and 4.",
        reasoning_framework=(
            "Requests for AI algorithms, source code, or related documentation are analyzed under Exemptions 1 "
            "(national security), 3 (statutory), and 4 (confidential business information). Agencies must assess "
            "whether disclosure would harm national security, violate statutory restrictions, or reveal trade secrets. "
            "Courts may require in camera review and detailed agency justification."
        ),
        key_factors=[
            "Nature of the AI record",
            "National security interest",
            "Statutory restrictions",
            "Confidentiality and competitive harm"
        ],
        primary_authority=[
            "5 U.S.C. § 552(b)(1), (3), (4)",
            "Relevant statutes and executive orders"
        ],
        burden_holder="Agency",
        adversary_position="No exemption applies or public interest outweighs harm.",
        counter_arguments=[
            "Information is not classified or restricted.",
            "No competitive harm.",
            "Public interest is compelling."
        ],
        resolution_strategy="Review exemptions, require agency justification, allow judicial review.",
        entity_scope="All agencies using AI systems.",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="No controlling Supreme Court precedent"
    ),
    DoctrineBlock(
        topic="FOIA and Social Media Records",
        keywords=["social media", "records", "FOIA", "agency use", "public communication"],
        conclusion_template="Agency social media content may be subject to FOIA if used for official business.",
        reasoning_framework=(
            "Social media posts, messages, and other content created or received by agencies in the course of official "
            "business are subject to FOIA. Agencies must preserve such records and respond to requests. Personal use "
            "accounts are not covered unless used for agency business. Agencies must ensure compliance with recordkeeping "
            "and disclosure obligations."
        ),
        key_factors=[
            "Official vs. personal use",
            "Preservation of records",
            "Agency control",
            "Nature of the content"
        ],
        primary_authority=[
            "5 U.S.C. § 552",
            "National Archives guidance"
        ],
        burden_holder="Agency",
        adversary_position="Content is not an agency record or is personal.",
        counter_arguments=[
            "Account was used for official business.",
            "Agency controls the content.",
            "Recordkeeping obligations apply."
        ],
        resolution_strategy="Determine official use, preserve records, apply FOIA definition.",
        entity_scope="All agencies using social media.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="No controlling Supreme Court precedent"
    ),
    DoctrineBlock(
        topic="FOIA and Email Records",
        keywords=["email", "records", "agency control", "FOIA", "preservation"],
        conclusion_template="Agency email communications are subject to FOIA if used for official business.",
        reasoning_framework=(
            "Emails created or received by agency employees in the course of official business are subject to FOIA, "
            "regardless of whether they are on government or personal accounts. Agencies must preserve such emails and "
            "respond to requests. Personal emails not used for agency business are not covered."
        ),
        key_factors=[
            "Official vs. personal use",
            "Preservation of records",
            "Agency control",
            "Nature of the communication"
        ],
        primary_authority=[
            "5 U.S.C. § 552",
            "National Archives guidance"
        ],
        burden_holder="Agency",
        adversary_position="Email is not an agency record or is personal.",
        counter_arguments