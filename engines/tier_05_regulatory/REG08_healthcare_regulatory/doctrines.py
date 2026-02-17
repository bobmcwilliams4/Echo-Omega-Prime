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
        topic="HIPAA Privacy Rule - Protected Health Information",
        keywords=["HIPAA", "Privacy Rule", "PHI", "protected health information", "patient privacy", "45 CFR 164"],
        conclusion_template="The entity's use or disclosure of PHI is {compliant/non-compliant} with the HIPAA Privacy Rule.",
        reasoning_framework=(
            "1. Identify whether the information at issue constitutes PHI under 45 CFR 160.103.\n"
            "2. Determine if the entity is a covered entity or business associate as defined by HIPAA.\n"
            "3. Assess whether the use or disclosure falls under a permitted purpose (treatment, payment, healthcare operations, or as otherwise authorized).\n"
            "4. Evaluate if the minimum necessary standard has been applied (45 CFR 164.502(b)).\n"
            "5. Review for valid patient authorization if required.\n"
            "6. Consider any applicable exceptions (e.g., public health, law enforcement).\n"
            "7. Analyze documentation and policies supporting the use/disclosure.\n"
            "8. Conclude compliance based on alignment with regulatory requirements."
        ),
        key_factors=[
            "Definition of PHI",
            "Status as covered entity/business associate",
            "Purpose of use/disclosure",
            "Minimum necessary standard",
            "Existence of valid authorization",
            "Applicable exceptions"
        ],
        primary_authority=["45 CFR 160.103", "45 CFR 164.502", "HHS OCR Guidance"],
        burden_holder="Entity using or disclosing PHI",
        adversary_position="The use/disclosure was not permitted or lacked proper authorization.",
        counter_arguments=[
            "The information was de-identified per HIPAA standards.",
            "The use was for a permitted purpose.",
            "A valid authorization was obtained.",
            "An exception applies."
        ],
        resolution_strategy="Apply the regulatory definitions and exceptions; verify documentation and intent.",
        entity_scope="Covered entities and business associates",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="HHS OCR Resolution Agreements (e.g., Cignet Health, 2011)"
    ),
    DoctrineBlock(
        topic="HIPAA Security Rule - Technical Safeguards",
        keywords=["HIPAA", "Security Rule", "technical safeguards", "ePHI", "access control", "encryption", "audit controls", "45 CFR 164.312"],
        conclusion_template="The entity's technical safeguards for ePHI are {adequate/inadequate} under the HIPAA Security Rule.",
        reasoning_framework=(
            "1. Determine if the entity handles electronic protected health information (ePHI).\n"
            "2. Review implemented access controls (unique user identification, emergency access, automatic logoff, encryption/decryption).\n"
            "3. Assess audit controls for monitoring activity on systems containing ePHI.\n"
            "4. Evaluate integrity controls to ensure ePHI is not improperly altered or destroyed.\n"
            "5. Examine authentication mechanisms for verifying user identity.\n"
            "6. Consider transmission security (encryption, integrity controls during transmission).\n"
            "7. Compare safeguards with the requirements in 45 CFR 164.312.\n"
            "8. Conclude adequacy based on risk analysis and implementation specifications."
        ),
        key_factors=[
            "Existence of ePHI",
            "Access control measures",
            "Audit and integrity controls",
            "Encryption and transmission security",
            "User authentication",
            "Risk analysis documentation"
        ],
        primary_authority=["45 CFR 164.312", "HHS Security Rule Guidance"],
        burden_holder="Entity maintaining ePHI",
        adversary_position="Technical safeguards are insufficient to protect ePHI.",
        counter_arguments=[
            "All required technical safeguards are implemented.",
            "Equivalent alternative measures are in place.",
            "No ePHI is maintained."
        ],
        resolution_strategy="Map implemented safeguards to regulatory requirements; review risk analysis.",
        entity_scope="Covered entities and business associates",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Anthem, Inc. Resolution Agreement (2018)"
    ),
    DoctrineBlock(
        topic="Stark Law - Physician Self-Referral Prohibition",
        keywords=["Stark Law", "physician self-referral", "financial relationship", "designated health services", "42 USC 1395nn"],
        conclusion_template="The physician's referral is {prohibited/permitted} under the Stark Law.",
        reasoning_framework=(
            "1. Identify if the referral is for designated health services (DHS) payable by Medicare.\n"
            "2. Determine if a financial relationship exists between the physician (or immediate family) and the entity.\n"
            "3. Assess whether any exceptions apply (e.g., in-office ancillary services, bona fide employment).\n"
            "4. Analyze the structure and documentation of the financial relationship.\n"
            "5. Evaluate the intent and compliance with regulatory safe harbors.\n"
            "6. Conclude whether the referral is prohibited or falls within an exception."
        ),
        key_factors=[
            "Type of health service referred",
            "Existence of financial relationship",
            "Applicability of exceptions",
            "Documentation of arrangements",
            "Medicare reimbursement"
        ],
        primary_authority=["42 USC 1395nn", "42 CFR 411.350 et seq."],
        burden_holder="Physician/entity making the referral",
        adversary_position="The referral violates the Stark Law prohibition.",
        counter_arguments=[
            "An exception applies to the financial relationship.",
            "No DHS involved.",
            "No Medicare payment implicated."
        ],
        resolution_strategy="Apply statutory definitions and exceptions; review documentation and intent.",
        entity_scope="Physicians and entities billing Medicare",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Tuomey Healthcare System, 2015"
    ),
    DoctrineBlock(
        topic="Anti-Kickback Statute - Remuneration for Referrals",
        keywords=["Anti-Kickback Statute", "remuneration", "referrals", "federal healthcare programs", "42 USC 1320a-7b"],
        conclusion_template="The arrangement {violates/does not violate} the Anti-Kickback Statute.",
        reasoning_framework=(
            "1. Identify whether remuneration is offered, paid, solicited, or received.\n"
            "2. Determine if the remuneration is intended to induce or reward referrals for services reimbursable by federal healthcare programs.\n"
            "3. Assess whether a statutory safe harbor applies (e.g., employment, personal services, space rental).\n"
            "4. Analyze the intent of the parties and the structure of the arrangement.\n"
            "5. Review documentation supporting compliance with safe harbors.\n"
            "6. Conclude whether the arrangement constitutes a prohibited kickback."
        ),
        key_factors=[
            "Existence of remuneration",
            "Intent to induce referrals",
            "Applicability of safe harbors",
            "Federal program involvement",
            "Documentation of arrangement"
        ],
        primary_authority=["42 USC 1320a-7b(b)", "42 CFR 1001.952"],
        burden_holder="Party offering or receiving remuneration",
        adversary_position="The arrangement is an illegal kickback.",
        counter_arguments=[
            "Arrangement fits within a safe harbor.",
            "No intent to induce referrals.",
            "No federal program funds involved."
        ],
        resolution_strategy="Apply safe harbor analysis; review intent and documentation.",
        entity_scope="Healthcare providers, vendors, and payors",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="U.S. v. Greber, 3rd Cir. 1985"
    ),
    DoctrineBlock(
        topic="False Claims Act - Healthcare Fraud",
        keywords=["False Claims Act", "healthcare fraud", "Medicare", "Medicaid", "31 USC 3729", "qui tam"],
        conclusion_template="The claim is {false/legitimate} under the False Claims Act.",
        reasoning_framework=(
            "1. Determine if a claim was submitted to a federal healthcare program.\n"
            "2. Assess whether the claim was knowingly false or fraudulent (actual knowledge, deliberate ignorance, or reckless disregard).\n"
            "3. Analyze the materiality of the false statement to the government's payment decision.\n"
            "4. Review supporting documentation and billing records.\n"
            "5. Consider whistleblower (qui tam) allegations and government investigations.\n"
            "6. Conclude whether the claim violates the FCA."
        ),
        key_factors=[
            "Submission of claim to federal program",
            "Knowledge of falsity",
            "Materiality of statement",
            "Documentation and intent",
            "Qui tam involvement"
        ],
        primary_authority=["31 USC 3729", "Universal Health Services v. U.S. ex rel. Escobar (2016)"],
        burden_holder="Claimant (provider or supplier)",
        adversary_position="The claim was knowingly false or fraudulent.",
        counter_arguments=[
            "No knowledge or intent to defraud.",
            "Error was inadvertent.",
            "Claim was accurate and supported."
        ],
        resolution_strategy="Review claim documentation, intent, and materiality.",
        entity_scope="Providers, suppliers, billing companies",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Universal Health Services v. Escobar, 2016"
    ),
    DoctrineBlock(
        topic="Medicare Conditions of Participation - Hospital Requirements",
        keywords=["Medicare", "Conditions of Participation", "hospital", "compliance", "42 CFR 482"],
        conclusion_template="The hospital is {in compliance/not in compliance} with Medicare Conditions of Participation.",
        reasoning_framework=(
            "1. Identify the applicable Medicare Conditions of Participation (CoPs) for the hospital.\n"
            "2. Review hospital policies, procedures, and operations for alignment with CoPs (e.g., governing body, QAPI, medical staff, patient rights).\n"
            "3. Assess survey findings and deficiency reports.\n"
            "4. Evaluate corrective actions taken in response to deficiencies.\n"
            "5. Conclude compliance status based on adherence to CoPs."
        ),
        key_factors=[
            "Applicability of CoPs",
            "Survey results",
            "Corrective actions",
            "Hospital policies and procedures",
            "Documentation"
        ],
        primary_authority=["42 CFR 482", "CMS State Operations Manual"],
        burden_holder="Hospital",
        adversary_position="The hospital is non-compliant with one or more CoPs.",
        counter_arguments=[
            "All CoPs are met.",
            "Deficiencies have been corrected.",
            "Survey findings are disputed."
        ],
        resolution_strategy="Compare hospital operations to CoPs; review survey and corrective action documentation.",
        entity_scope="Hospitals participating in Medicare",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="CMS Survey and Certification Letters"
    ),
    DoctrineBlock(
        topic="EMTALA - Emergency Medical Treatment and Labor Act",
        keywords=["EMTALA", "emergency medical treatment", "patient dumping", "screening", "stabilization", "42 USC 1395dd"],
        conclusion_template="The hospital's actions are {compliant/non-compliant} with EMTALA.",
        reasoning_framework=(
            "1. Determine if the patient presented to a hospital with a dedicated emergency department.\n"
            "2. Assess whether an appropriate medical screening examination was provided to determine if an emergency medical condition exists.\n"
            "3. Evaluate whether necessary stabilizing treatment was provided or an appropriate transfer was arranged.\n"
            "4. Review documentation of screening, treatment, and transfer.\n"
            "5. Consider any exceptions (e.g., patient refusal, medical necessity).\n"
            "6. Conclude compliance based on statutory and regulatory requirements."
        ),
        key_factors=[
            "Hospital status as covered by EMTALA",
            "Provision of medical screening",
            "Stabilization of emergency condition",
            "Appropriateness of transfer",
            "Documentation"
        ],
        primary_authority=["42 USC 1395dd", "42 CFR 489.24"],
        burden_holder="Hospital",
        adversary_position="The hospital failed to screen, stabilize, or appropriately transfer the patient.",
        counter_arguments=[
            "Appropriate screening and stabilization were provided.",
            "Patient refused treatment or transfer.",
            "No emergency medical condition existed."
        ],
        resolution_strategy="Review medical records, policies, and transfer documentation.",
        entity_scope="Hospitals with emergency departments",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Burditt v. U.S. Dept. of HHS, 1991"
    ),
    DoctrineBlock(
        topic="340B Drug Pricing Program",
        keywords=["340B", "drug pricing", "covered entity", "HRSA", "discount", "pharmaceuticals"],
        conclusion_template="The entity's participation in the 340B Program is {compliant/non-compliant} with program requirements.",
        reasoning_framework=(
            "1. Determine if the entity is a covered entity as defined by the 340B statute.\n"
            "2. Assess registration and eligibility status with HRSA.\n"
            "3. Evaluate compliance with program requirements (e.g., no duplicate discounts, no diversion of drugs to ineligible patients).\n"
            "4. Review audit findings and corrective actions.\n"
            "5. Conclude compliance based on statutory and regulatory standards."
        ),
        key_factors=[
            "Covered entity status",
            "HRSA registration",
            "Prevention of duplicate discounts",
            "Prevention of drug diversion",
            "Audit and corrective actions"
        ],
        primary_authority=["42 USC 256b", "HRSA 340B Program Guidance"],
        burden_holder="Covered entity",
        adversary_position="The entity violated 340B program requirements.",
        counter_arguments=[
            "All program requirements are met.",
            "No duplicate discounts or diversion occurred.",
            "Audit findings have been addressed."
        ],
        resolution_strategy="Review HRSA guidance, audit reports, and corrective actions.",
        entity_scope="Covered entities and contract pharmacies",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="Genesis Health Care, HRSA Audit (2017)"
    ),
    DoctrineBlock(
        topic="FDA Drug Approval - New Drug Application",
        keywords=["FDA", "drug approval", "NDA", "new drug application", "safety", "efficacy", "21 CFR 314"],
        conclusion_template="The drug's approval status is {approved/not approved} under the FDA's NDA process.",
        reasoning_framework=(
            "1. Confirm that the product qualifies as a 'new drug' under the FD&C Act.\n"
            "2. Review the submission of a complete NDA, including chemistry, manufacturing, and controls (CMC), preclinical, and clinical data.\n"
            "3. Assess FDA review findings regarding safety, efficacy, and labeling.\n"
            "4. Consider any advisory committee recommendations.\n"
            "5. Conclude approval status based on FDA's final action."
        ),
        key_factors=[
            "Product status as a new drug",
            "Completeness of NDA submission",
            "Safety and efficacy data",
            "FDA review and findings",
            "Labeling and post-market requirements"
        ],
        primary_authority=["21 USC 355", "21 CFR 314"],
        burden_holder="Drug sponsor/applicant",
        adversary_position="The drug is not safe or effective for its intended use.",
        counter_arguments=[
            "Adequate and well-controlled studies support approval.",
            "All NDA requirements are met.",
            "Post-market commitments are in place."
        ],
        resolution_strategy="Review NDA submission, FDA review documentation, and advisory committee input.",
        entity_scope="Drug manufacturers and sponsors",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FDA Approval Letters (e.g., NDA 021436, 2002)"
    ),
    DoctrineBlock(
        topic="DEA Controlled Substances - Schedule Classification",
        keywords=["DEA", "controlled substances", "scheduling", "Schedule I-V", "21 CFR 1308"],
        conclusion_template="The substance is classified as {Schedule I-V/Not Controlled} under DEA regulations.",
        reasoning_framework=(
            "1. Identify the chemical substance and its intended use.\n"
            "2. Review the DEA's schedules of controlled substances (21 CFR 1308.11-15).\n"
            "3. Assess any scheduling actions, temporary or permanent, by the DEA.\n"
            "4. Consider the substance's abuse potential, accepted medical use, and safety.\n"
            "5. Conclude the current schedule classification."
        ),
        key_factors=[
            "Chemical identity of substance",
            "Current DEA scheduling",
            "Abuse potential",
            "Accepted medical use",
            "DEA rulemaking actions"
        ],
        primary_authority=["21 USC 812", "21 CFR 1308"],
        burden_holder="Registrant or prescriber",
        adversary_position="The substance is misclassified or improperly handled.",
        counter_arguments=[
            "Substance is not scheduled.",
            "DEA has issued a rescheduling order.",
            "Substance is handled per schedule requirements."
        ],
        resolution_strategy="Check current DEA schedules and Federal Register notices.",
        entity_scope="Pharmacies, prescribers, manufacturers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="DEA Scheduling Orders"
    ),
    DoctrineBlock(
        topic="Telehealth - Interstate Licensure",
        keywords=["telehealth", "interstate licensure", "state medical board", "practice of medicine", "licensure compacts"],
        conclusion_template="The provider's telehealth practice is {authorized/unauthorized} under state licensure laws.",
        reasoning_framework=(
            "1. Identify the state where the patient is located during the telehealth encounter.\n"
            "2. Determine if the provider holds a valid license in that state or participates in an interstate licensure compact.\n"
            "3. Review any applicable state waivers or exceptions (e.g., COVID-19 emergency orders).\n"
            "4. Assess compliance with state-specific telehealth practice requirements.\n"
            "5. Conclude authorization status."
        ),
        key_factors=[
            "Location of patient",
            "Provider licensure status",
            "Participation in licensure compacts",
            "State waivers or exceptions",
            "Telehealth practice requirements"
        ],
        primary_authority=["State Medical Practice Acts", "Interstate Medical Licensure Compact"],
        burden_holder="Telehealth provider",
        adversary_position="The provider is practicing without proper licensure.",
        counter_arguments=[
            "Provider holds a valid license.",
            "Compact participation authorizes practice.",
            "State waiver applies."
        ],
        resolution_strategy="Verify licensure and compact status; review state law and waivers.",
        entity_scope="Physicians and telehealth providers",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="Federation of State Medical Boards Guidance"
    ),
    DoctrineBlock(
        topic="Medicaid Managed Care - Network Adequacy",
        keywords=["Medicaid", "managed care", "network adequacy", "access to care", "provider network", "42 CFR 438"],
        conclusion_template="The managed care plan's network is {adequate/inadequate} under Medicaid requirements.",
        reasoning_framework=(
            "1. Identify the applicable state and Medicaid managed care plan.\n"
            "2. Review network adequacy standards (e.g., time and distance, provider-to-enrollee ratios).\n"
            "3. Assess provider network directories and access reports.\n"
            "4. Evaluate member complaints and access barriers.\n"
            "5. Conclude adequacy based on regulatory standards and evidence."
        ),
        key_factors=[
            "State network adequacy standards",
            "Provider network composition",
            "Access reports and complaints",
            "Provider-to-enrollee ratios",
            "Time and distance standards"
        ],
        primary_authority=["42 CFR 438.68", "State Medicaid contracts"],
        burden_holder="Managed care organization",
        adversary_position="The network fails to provide adequate access to care.",
        counter_arguments=[
            "Network meets all regulatory standards.",
            "Access barriers are addressed.",
            "Provider directory is accurate and up to date."
        ],
        resolution_strategy="Compare network to standards; review access data and complaints.",
        entity_scope="Medicaid managed care organizations",
        confidence=0.87,
        confidence_zone="Moderate",
        controlling_precedent="CMS Network Adequacy Reviews"
    ),
    DoctrineBlock(
        topic="State Medical Board - Scope of Practice",
        keywords=["state medical board", "scope of practice", "licensure", "advanced practice", "practice act"],
        conclusion_template="The provider's actions are {within/outside} the authorized scope of practice.",
        reasoning_framework=(
            "1. Identify the provider's profession and licensure status.\n"
            "2. Review the relevant state practice act and board regulations.\n"
            "3. Assess the specific acts or procedures performed.\n"
            "4. Determine if the acts are expressly authorized, prohibited, or silent in the law.\n"
            "5. Consider board opinions, guidance, and disciplinary actions.\n"
            "6. Conclude scope of practice status."
        ),
        key_factors=[
            "Provider profession and licensure",
            "State practice act provisions",
            "Board regulations and guidance",
            "Nature of acts performed",
            "Precedent disciplinary actions"
        ],
        primary_authority=["State Practice Acts", "State Medical Board Regulations"],
        burden_holder="Provider",
        adversary_position="The provider exceeded the legal scope of practice.",
        counter_arguments=[
            "Acts are authorized by law.",
            "Board guidance supports the practice.",
            "Provider acted within training and competence."
        ],
        resolution_strategy="Review practice act, board regulations, and disciplinary history.",
        entity_scope="Licensed healthcare professionals",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="State Board Disciplinary Decisions"
    ),
    DoctrineBlock(
        topic="HIPAA Breach Notification",
        keywords=["HIPAA", "breach notification", "PHI", "unsecured PHI", "45 CFR 164.400"],
        conclusion_template="The entity's breach notification is {compliant/non-compliant} with HIPAA requirements.",
        reasoning_framework=(
            "1. Determine if a breach of unsecured PHI occurred (45 CFR 164.402).\n"
            "2. Assess the risk of compromise to the PHI's security or privacy.\n"
            "3. Review the timeliness and content of notifications to affected individuals, HHS, and (if applicable) the media.\n"
            "4. Evaluate documentation of risk assessment and mitigation steps.\n"
            "5. Conclude compliance with notification requirements."
        ),
        key_factors=[
            "Occurrence of breach",
            "Risk assessment documentation",
            "Timeliness of notification",
            "Content of notification",
            "Notification to HHS and media"
        ],
        primary_authority=["45 CFR 164.400-414", "HHS Breach Notification Guidance"],
        burden_holder="Entity experiencing the breach",
        adversary_position="The entity failed to provide timely or adequate breach notification.",
        counter_arguments=[
            "No breach occurred.",
            "Notification was timely and complete.",
            "PHI was secured (e.g., encrypted)."
        ],
        resolution_strategy="Review breach assessment, notification records, and HHS guidance.",
        entity_scope="Covered entities and business associates",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Anthem, Inc. Breach Settlement (2018)"
    ),
    DoctrineBlock(
        topic="Medicare Part D - Medication Therapy Management",
        keywords=["Medicare Part D", "medication therapy management", "MTM", "CMS", "prescription drug plans"],
        conclusion_template="The plan's MTM program is {compliant/non-compliant} with Medicare Part D requirements.",
        reasoning_framework=(
            "1. Identify the prescription drug plan's MTM program structure and eligibility criteria.\n"
            "2. Review CMS requirements for MTM (targeting, interventions, documentation).\n"
            "3. Assess delivery of MTM services and beneficiary engagement.\n"
            "4. Evaluate program outcomes and CMS audit findings.\n"
            "5. Conclude compliance status."
        ),
        key_factors=[
            "MTM program structure",
            "CMS requirements",
            "Beneficiary engagement",
            "Documentation of interventions",
            "Audit findings"
        ],
        primary_authority=["42 CFR 423.153(d)", "CMS MTM Guidance"],
        burden_holder="Prescription drug plan sponsor",
        adversary_position="The MTM program fails to meet CMS requirements.",
        counter_arguments=[
            "Program meets all CMS standards.",
            "Beneficiaries are properly targeted and engaged.",
            "Documentation is complete."
        ],
        resolution_strategy="Compare program to CMS requirements; review audit results.",
        entity_scope="Medicare Part D sponsors",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="CMS MTM Program Audits"
    ),
    DoctrineBlock(
        topic="Clinical Laboratory Improvement Amendments (CLIA)",
        keywords=["CLIA", "clinical laboratory", "certification", "testing", "CMS", "42 CFR 493"],
        conclusion_template="The laboratory's operations are {compliant/non-compliant} with CLIA requirements.",
        reasoning_framework=(
            "1. Determine if the laboratory performs testing on human specimens for health assessment or diagnosis.\n"
            "2. Review CLIA certification status and scope.\n"
            "3. Assess compliance with personnel, quality control, proficiency testing, and recordkeeping requirements.\n"
            "4. Evaluate inspection reports and corrective actions.\n"
            "5. Conclude compliance based on regulatory standards."
        ),
        key_factors=[
            "CLIA certification status",
            "Scope of testing",
            "Personnel qualifications",
            "Quality control and proficiency testing",
            "Inspection findings"
        ],
        primary_authority=["42 USC 263a", "42 CFR 493"],
        burden_holder="Laboratory director/owner",
        adversary_position="The laboratory is non-compliant with CLIA.",
        counter_arguments=[
            "All CLIA requirements are met.",
            "Deficiencies have been corrected.",
            "Testing is outside CLIA scope."
        ],
        resolution_strategy="Review certification, inspection, and quality control documentation.",
        entity_scope="Clinical laboratories",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="CMS CLIA Enforcement Actions"
    ),
    DoctrineBlock(
        topic="FDA Medical Device Classification",
        keywords=["FDA", "medical device", "classification", "Class I", "Class II", "Class III", "510(k)", "PMA"],
        conclusion_template="The device is classified as {Class I/II/III} under FDA regulations.",
        reasoning_framework=(
            "1. Identify the intended use and technological characteristics of the device.\n"
            "2. Review FDA classification regulations and product codes.\n"
            "3. Assess whether the device is substantially equivalent to a legally marketed device (510(k)) or requires premarket approval (PMA).\n"
            "4. Consider risk level and applicable controls.\n"
            "5. Conclude classification status."
        ),
        key_factors=[
            "Intended use",
            "Technological characteristics",
            "FDA classification regulation",
            "Substantial equivalence",
            "Risk level"
        ],
        primary_authority=["21 USC 360c", "21 CFR 860"],
        burden_holder="Device manufacturer",
        adversary_position="The device is misclassified or lacks proper clearance.",
        counter_arguments=[
            "Device is properly classified.",
            "510(k) or PMA is in place.",
            "Device is exempt."
        ],
        resolution_strategy="Review classification regulations, product codes, and substantial equivalence.",
        entity_scope="Medical device manufacturers",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FDA Device Classification Orders"
    ),
    DoctrineBlock(
        topic="HIPAA Business Associate Agreements",
        keywords=["HIPAA", "business associate", "BAA", "agreement", "PHI", "45 CFR 164.504"],
        conclusion_template="The entity's business associate agreement is {compliant/non-compliant} with HIPAA.",
        reasoning_framework=(
            "1. Identify whether the relationship involves the use or disclosure of PHI by a business associate.\n"
            "2. Review the written agreement for required elements (per 45 CFR 164.504(e)).\n"
            "3. Assess the allocation of responsibilities for safeguarding PHI and reporting breaches.\n"
            "4. Evaluate the agreement's provisions for permitted uses/disclosures, termination, and return/destruction of PHI.\n"
            "5. Conclude compliance with HIPAA requirements."
        ),
        key_factors=[
            "Existence of PHI exchange",
            "Written agreement",
            "Required contractual elements",
            "Safeguarding and breach reporting",
            "Termination provisions"
        ],
        primary_authority=["45 CFR 164.504(e)", "HHS BAA Guidance"],
        burden_holder="Covered entity and business associate",
        adversary_position="The BAA lacks required elements or is absent.",
        counter_arguments=[
            "All required elements are present.",
            "No PHI is exchanged.",
            "A direct treatment relationship exists."
        ],
        resolution_strategy="Review agreement language and regulatory checklist.",
        entity_scope="Covered entities and business associates",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="HHS Sample BAA"
    ),
    DoctrineBlock(
        topic="Medicare Physician Fee Schedule - Physician Self-Referral",
        keywords=["Medicare", "physician fee schedule", "self-referral", "Stark Law", "42 CFR 414"],
        conclusion_template="The physician's billing is {compliant/non-compliant} with self-referral prohibitions.",
        reasoning_framework=(
            "1. Identify services billed under the Medicare Physician Fee Schedule.\n"
            "2. Determine if a financial relationship exists between the physician and the entity.\n"
            "3. Assess whether billing is permitted under Stark Law exceptions.\n"
            "4. Review documentation of arrangements and billing practices.\n"
            "5. Conclude compliance with self-referral prohibitions."
        ),
        key_factors=[
            "Type of service billed",
            "Financial relationship",
            "Applicability of exceptions",
            "Documentation",
            "Medicare reimbursement"
        ],
        primary_authority=["42 CFR 414", "42 USC 1395nn"],
        burden_holder="Physician/entity billing Medicare",
        adversary_position="Billing violates self-referral prohibitions.",
        counter_arguments=[
            "Exception applies.",
            "No financial relationship exists.",
            "Service is not DHS."
        ],
        resolution_strategy="Apply Stark Law analysis to billing practices.",
        entity_scope="Physicians billing Medicare",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="CMS Physician Fee Schedule Rules"
    ),
    DoctrineBlock(
        topic="State Certificate of Need Laws",
        keywords=["certificate of need", "CON", "state law", "healthcare facility", "expansion", "regulatory approval"],
        conclusion_template="The facility's project is {subject/not subject} to Certificate of Need requirements.",
        reasoning_framework=(
            "1. Identify the state and applicable CON statute.\n"
            "2. Determine if the proposed project (construction, expansion, acquisition) falls within the scope of CON law.\n"
            "3. Review application and approval process requirements.\n"
            "4. Assess public need and opposition.\n"
            "5. Conclude whether CON approval is required."
        ),
        key_factors=[
            "State CON statute",
            "Nature of proposed project",
            "Application process",
            "Public need determination",
            "Opposition or support"
        ],
        primary_authority=["State CON Laws", "State Health Planning Agencies"],
        burden_holder="Facility sponsor/applicant",
        adversary_position="The project is subject to CON and lacks approval.",
        counter_arguments=[
            "Project is exempt.",
            "No CON law applies.",
            "Approval has been granted."
        ],
        resolution_strategy="Review state law, project scope, and application status.",
        entity_scope="Healthcare facilities",
        confidence=0.86,
        confidence_zone="Moderate",
        controlling_precedent="State CON Agency Decisions"
    ),
    DoctrineBlock(
        topic="FDA Dietary Supplement Regulation",
        keywords=["FDA", "dietary supplement", "DSHEA", "labeling", "adulteration", "misbranding", "21 USC 321(ff)"],
        conclusion_template="The product is {compliant/non-compliant} with FDA dietary supplement regulations.",
        reasoning_framework=(
            "1. Determine if the product meets the definition of a dietary supplement under DSHEA.\n"
            "2. Review labeling for required statements and prohibited claims.\n"
            "3. Assess manufacturing practices for compliance with cGMPs.\n"
            "4. Evaluate reports of adulteration or misbranding.\n"
            "5. Conclude compliance with FDA regulations."
        ),
        key_factors=[
            "Product definition under DSHEA",
            "Labeling and claims",
            "Manufacturing practices",
            "Adulteration/misbranding reports",
            "FDA warning letters"
        ],
        primary_authority=["21 USC 321(ff)", "21 CFR 111"],
        burden_holder="Manufacturer/distributor",
        adversary_position="The product is adulterated, misbranded, or makes prohibited claims.",
        counter_arguments=[
            "Product meets all regulatory requirements.",
            "Labeling is accurate and not misleading.",
            "Manufacturing follows cGMPs."
        ],
        resolution_strategy="Review product labeling, manufacturing, and FDA enforcement actions.",
        entity_scope="Dietary supplement manufacturers",
        confidence=0.87,
        confidence_zone="Moderate",
        controlling_precedent="FDA Warning Letters"
    ),
    DoctrineBlock(
        topic="Medicare Advantage Risk Adjustment",
        keywords=["Medicare Advantage", "risk adjustment", "CMS", "coding", "HCC", "payment"],
        conclusion_template="The plan's risk adjustment submissions are {accurate/inaccurate} under CMS requirements.",
        reasoning_framework=(
            "1. Review the plan's risk adjustment data submission process.\n"
            "2. Assess the accuracy and completeness of diagnosis coding (HCCs).\n"
            "3. Evaluate supporting medical records and audit findings.\n"
            "4. Consider CMS payment adjustments and enforcement actions.\n"
            "5. Conclude accuracy of risk adjustment submissions."
        ),
        key_factors=[
            "Diagnosis coding accuracy",
            "Supporting medical records",
            "CMS audit findings",
            "Payment adjustments",
            "Submission process"
        ],
        primary_authority=["42 CFR 422.310", "CMS Risk Adjustment Data Validation"],
        burden_holder="Medicare Advantage plan",
        adversary_position="Submissions are inaccurate or unsupported.",
        counter_arguments=[
            "Coding is accurate and supported.",
            "Audit findings have been addressed.",
            "Submission process is robust."
        ],
        resolution_strategy="Review coding, medical records, and audit results.",
        entity_scope="Medicare Advantage plans",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="CMS RADV Audits"
    ),
    DoctrineBlock(
        topic="HIPAA Right of Access",
        keywords=["HIPAA", "right of access", "patient records", "PHI", "timeliness", "45 CFR 164.524"],
        conclusion_template="The entity's response to a records request is {compliant/non-compliant} with HIPAA Right of Access.",
        reasoning_framework=(
            "1. Determine if the request is from the patient or their personal representative.\n"
            "2. Review the timeliness of the response (generally within 30 days).\n"
            "3. Assess the format and manner of access provided.\n"
            "4. Evaluate any denial and the basis for denial.\n"
            "5. Conclude compliance with the Right of Access requirements."
        ),
        key_factors=[
            "Identity of requestor",
            "Timeliness of response",
            "Format and manner of access",
            "Basis for denial (if any)",
            "Documentation"
        ],
        primary_authority=["45 CFR 164.524", "HHS Right of Access Initiative"],
        burden_holder="Entity holding the records",
        adversary_position="The entity delayed or denied access in violation of HIPAA.",
        counter_arguments=[
            "Access was timely and complete.",
            "Denial was based on a valid exception.",
            "Requestor was not authorized."
        ],
        resolution_strategy="Review request, response, and documentation.",
        entity_scope="Covered entities and business associates",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Cignet Health, HHS OCR Settlement (2011)"
    ),
    DoctrineBlock(
        topic="FDA Accelerated Approval Pathway",
        keywords=["FDA", "accelerated approval", "surrogate endpoint", "serious condition", "post-market studies", "21 CFR 314.500"],
        conclusion_template="The drug's approval via the Accelerated Approval Pathway is {justified/unjustified}.",
        reasoning_framework=(
            "1. Determine if the drug treats a serious or life-threatening condition.\n"
            "2. Assess whether approval is based on a surrogate endpoint reasonably likely to predict clinical benefit.\n"
            "3. Review requirements for post-marketing confirmatory studies.\n"
            "4. Evaluate FDA's rationale for accelerated approval.\n"
            "5. Conclude justification for accelerated approval."
        ),
        key_factors=[
            "Seriousness of condition",
            "Use of surrogate endpoint",
            "Post-market study requirements",
            "FDA review and rationale",
            "Clinical benefit prediction"
        ],
        primary_authority=["21 CFR 314.500", "FD&C Act Section 506(c)"],
        burden_holder="Drug sponsor/applicant",
        adversary_position="Approval is not justified by available evidence.",
        counter_arguments=[
            "Surrogate endpoint is valid.",
            "Post-market studies are ongoing.",
            "Condition is serious and unmet need exists."
        ],
        resolution_strategy="Review FDA approval documents and post-market commitments.",
        entity_scope="Drug manufacturers and sponsors",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FDA Accelerated Approval Decisions"
    ),
    # Additional doctrines to reach 40+ (abbreviated for brevity, but should be expanded in real implementation)
    DoctrineBlock(
        topic="HITECH Act - Meaningful Use of EHRs",
        keywords=["HITECH", "EHR", "meaningful use", "certified EHR technology", "CMS incentive"],
        conclusion_template="The provider's use of EHRs is {meaningful/not meaningful} under HITECH standards.",
        reasoning_framework=(
            "1. Determine if the provider uses certified EHR technology.\n"
            "2. Review attestation and reporting of meaningful use objectives.\n"
            "3. Assess compliance with core and menu objectives.\n"
            "4. Evaluate audit findings and incentive payments.\n"
            "5. Conclude meaningful use status."
        ),
        key_factors=[
            "Certified EHR technology",
            "Attestation and reporting",
            "Meaningful use objectives",
            "Audit findings",
            "Incentive payments"
        ],
        primary_authority=["42 USC 300jj", "CMS EHR Incentive Program"],
        burden_holder="Provider",
        adversary_position="Provider failed to achieve meaningful use.",
        counter_arguments=[
            "All objectives are met.",
            "Certified EHR is used.",
            "Audit findings addressed."
        ],
        resolution_strategy="Review attestation, audit, and technology certification.",
        entity_scope="Eligible providers and hospitals",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="CMS EHR Incentive Audits"
    ),
    DoctrineBlock(
        topic="OSHA Bloodborne Pathogens Standard",
        keywords=["OSHA", "bloodborne pathogens", "exposure control", "training", "29 CFR 1910.1030"],
        conclusion_template="The employer's bloodborne pathogens program is {compliant/non-compliant} with OSHA standards.",
        reasoning_framework=(
            "1. Determine if employees have occupational exposure to bloodborne pathogens.\n"
            "2. Review the written exposure control plan.\n"
            "3. Assess training, engineering controls, and personal protective equipment.\n"
            "4. Evaluate post-exposure procedures and recordkeeping.\n"
            "5. Conclude compliance with OSHA requirements."
        ),
        key_factors=[
            "Occupational exposure",
            "Exposure control plan",
            "Training and PPE",
            "Post-exposure procedures",
            "Recordkeeping"
        ],
        primary_authority=["29 CFR 1910.1030", "OSHA Guidance"],
        burden_holder="Employer",
        adversary_position="The program fails to protect employees from exposure.",
        counter_arguments=[
            "All OSHA requirements are met.",
            "Training and controls are in place.",
            "No occupational exposure exists."
        ],
        resolution_strategy="Review plan, training records, and OSHA inspection findings.",
        entity_scope="Healthcare employers",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="OSHA Enforcement Actions"
    ),
    DoctrineBlock(
        topic="CMS Stark Law Voluntary Self-Disclosure Protocol",
        keywords=["CMS", "Stark Law", "self-disclosure", "voluntary", "financial relationship"],
        conclusion_template="The entity's self-disclosure is {appropriate/inappropriate} under CMS protocol.",
        reasoning_framework=(
            "1. Identify the potential Stark Law violation.\n"
            "2. Review the self-disclosure submission for completeness and accuracy.\n"
            "3. Assess the corrective actions taken.\n"
            "4. Evaluate CMS response and settlement terms.\n"
            "5. Conclude appropriateness of self-disclosure."
        ),
        key_factors=[
            "Nature of violation",
            "Disclosure submission",
            "Corrective actions",
            "CMS response",
            "Settlement terms"
        ],
        primary_authority=["CMS Self-Referral Disclosure Protocol"],
        burden_holder="Disclosing entity",
        adversary_position="Disclosure is incomplete or inappropriate.",
        counter_arguments=[
            "Disclosure is complete and accurate.",
            "Corrective actions are sufficient.",
            "No violation occurred."
        ],
        resolution_strategy="Review submission, corrective actions, and CMS correspondence.",
        entity_scope="Entities subject to Stark Law",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="CMS SRDP Settlements"
    ),
    DoctrineBlock(
        topic="Medicaid Program Integrity - Exclusion Screening",
        keywords=["Medicaid", "exclusion screening", "OIG", "excluded individuals", "federal healthcare programs"],
        conclusion_template="The entity's exclusion screening is {adequate/inadequate} under Medicaid program integrity rules.",
        reasoning_framework=(
            "1. Determine if the entity screens employees and contractors against OIG and state exclusion lists.\n"
            "2. Review frequency and documentation of screening.\n"
            "3. Assess response to identified exclusions.\n"
            "4. Evaluate audit findings and corrective actions.\n"
            "5. Conclude adequacy of exclusion screening."
        ),
        key_factors=[
            "Screening frequency",
            "Documentation",
            "Response to exclusions",
            "Audit findings",
            "Corrective actions"
        ],
        primary_authority=["42 CFR 455.436", "OIG Guidance"],
        burden_holder="Medicaid provider",
        adversary_position="Screening is inadequate or not performed.",
        counter_arguments=[
            "Screening is timely and complete.",
            "No excluded individuals employed.",
            "Audit findings addressed."
        ],
        resolution_strategy="Review screening logs, policies, and audit results.",
        entity_scope="Medicaid providers",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="OIG Exclusion Enforcement"
    ),
    DoctrineBlock(
        topic="CMS Emergency Preparedness Rule",
        keywords=["CMS", "emergency preparedness", "all-hazards", "plan", "training", "42 CFR 482.15"],
        conclusion_template="The facility's emergency preparedness plan is {compliant/non-compliant} with CMS requirements.",
        reasoning_framework=(
            "1. Review the facility's all-hazards emergency preparedness plan.\n"
            "2. Assess training and testing exercises.\n"
            "3. Evaluate communication and coordination with local agencies.\n"
            "4. Review documentation and corrective actions.\n"
            "5. Conclude compliance with CMS requirements."
        ),
        key_factors=[
            "All-hazards plan",
            "Training and exercises",
            "Coordination with agencies",
            "Documentation",
            "Corrective actions"
        ],
        primary_authority=["42 CFR 482.15", "CMS Guidance"],
        burden_holder="Facility",
        adversary_position="Plan is inadequate or not implemented.",
        counter_arguments=[
            "Plan meets all requirements.",
            "Training and exercises are documented.",
            "Coordination is effective."
        ],
        resolution_strategy="Review plan, training records, and after-action reports.",
        entity_scope="CMS-certified facilities",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="CMS Survey Findings"
    ),
    DoctrineBlock(
        topic="FDA Good Manufacturing Practice (GMP) for Drugs",
        keywords=["FDA", "GMP", "good manufacturing practice", "drugs", "cGMP", "21 CFR 210", "21 CFR 211"],
        conclusion_template="The facility's drug manufacturing is {compliant/non-compliant} with FDA GMP requirements.",
        reasoning_framework=(
            "1. Review the facility's GMP policies and procedures.\n"
            "2. Assess manufacturing, quality control, and documentation practices.\n"
            "3. Evaluate FDA inspection findings and warning letters.\n"
            "4. Consider corrective actions taken.\n"
            "5. Conclude compliance with GMP requirements."
        ),
        key_factors=[
            "GMP policies and procedures",
            "Manufacturing practices",
            "Quality control",
            "FDA inspection findings",
            "Corrective actions"
        ],
        primary_authority=["21 CFR 210", "21 CFR 211"],
        burden_holder="Drug manufacturer",
        adversary_position="Manufacturing is non-compliant with GMP.",
        counter_arguments=[
            "All GMP requirements are met.",
            "Deficiencies have been corrected.",
            "No violations found."
        ],
        resolution_strategy="Review policies, inspection findings, and corrective actions.",
        entity_scope="Drug manufacturers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FDA Warning Letters"
    ),
    DoctrineBlock(
        topic="CMS Provider Enrollment - 855 Forms",
        keywords=["CMS", "provider enrollment", "855 forms", "Medicare", "revalidation"],
        conclusion_template="The provider's enrollment is {valid/invalid} under CMS requirements.",
        reasoning_framework=(
            "1. Review the provider's 855 form submission for completeness and accuracy.\n"
            "2. Assess supporting documentation and disclosures.\n"
            "3. Evaluate revalidation and change of information processes.\n"
            "4. Consider CMS enrollment approval or denial.\n"
            "5. Conclude validity of enrollment."
        ),
        key_factors=[
            "Completeness of 855 forms",
            "Supporting documentation",
            "Revalidation status",
            "Change of information",
            "CMS approval"
        ],
        primary_authority=["42 CFR 424.500", "CMS Enrollment Guidance"],
        burden_holder="Provider",
        adversary_position="Enrollment is invalid or incomplete.",
        counter_arguments=[
            "Forms are complete and accurate.",
            "All documentation provided.",
            "CMS approval granted."
        ],
        resolution_strategy="Review forms, documentation, and CMS correspondence.",
        entity_scope="Medicare providers",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="CMS Enrollment Decisions"
    ),
    DoctrineBlock(
        topic="FDA Human Subject Protection - Informed Consent",
        keywords=["FDA", "human subject protection", "informed consent", "clinical trials", "21 CFR 50"],
        conclusion_template="The informed consent process is {adequate/inadequate} under FDA regulations.",
        reasoning_framework=(
            "1. Review the informed consent documentation and process.\n"
            "2. Assess compliance with required elements (21 CFR 50.25).\n"
            "3. Evaluate subject understanding and voluntariness.\n"
            "4. Consider IRB review and approval.\n"
            "5. Conclude adequacy of informed consent."
        ),
        key_factors=[
            "Consent documentation",
            "Required elements",
            "Subject understanding",
            "Voluntariness",
            "IRB approval"
        ],
        primary_authority=["21 CFR 50", "FDA Guidance"],
        burden_holder="Sponsor/investigator",
        adversary_position="Consent process is inadequate or coercive.",
        counter_arguments=[
            "All required elements are present.",
            "Subjects gave informed, voluntary consent.",
            "IRB approved process."
        ],
        resolution_strategy="Review consent forms, process, and IRB records.",
        entity_scope="Clinical trial sponsors/investigators",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FDA Warning Letters"
    ),
    DoctrineBlock(
        topic="OIG Civil Monetary Penalties Law",
        keywords=["OIG", "civil monetary penalties", "CMP", "fraud", "abuse", "42 USC 1320a-7a"],
        conclusion_template="The entity is {liable/not liable} for civil monetary penalties under OIG authority.",
        reasoning_framework=(
            "1. Identify the alleged violation (e.g., false claims, kickbacks, patient dumping).\n"
            "2. Review evidence and documentation.\n"
            "3. Assess intent, materiality, and harm to federal programs.\n"
            "4. Evaluate OIG investigation findings and settlement terms.\n"
            "5. Conclude liability for civil monetary penalties."
        ),
        key_factors=[
            "Nature of violation",
            "Evidence and documentation",
            "Intent and materiality",
            "OIG findings",
            "Settlement terms"
        ],
        primary_authority=["42 USC 1320a-7a", "OIG CMP Regulations"],
        burden_holder="Entity accused of violation",
        adversary_position="Entity is liable for CMPs.",
        counter_arguments=[
            "No violation occurred.",
            "No intent or materiality.",
            "Settlement reached."
        ],
        resolution_strategy="Review evidence, OIG findings, and settlement documents.",
        entity_scope="Healthcare providers and suppliers",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="OIG CMP Settlements"
    ),
    DoctrineBlock(
        topic="CMS Two-Midnight Rule",
        keywords=["CMS", "two-midnight rule", "inpatient admission", "Medicare", "42 CFR 412.3"],
        conclusion_template="The inpatient admission is {appropriate/inappropriate} under the Two-Midnight Rule.",
        reasoning_framework=(
            "1. Review the physician's expectation regarding the patient's need for hospital care spanning two midnights.\n"
            "2. Assess documentation supporting the admission decision.\n"
            "3. Evaluate medical necessity and CMS guidance.\n"
            "4. Consider audit findings and appeals.\n"
            "5. Conclude appropriateness of inpatient admission."
        ),
        key_factors=[
            "Physician expectation",
            "Admission documentation",
            "Medical necessity",
            "CMS guidance",
            "Audit findings"
        ],
        primary_authority=["42 CFR 412.3", "CMS Two-Midnight Guidance"],
        burden_holder="Hospital",
        adversary_position="Admission does not meet Two-Midnight Rule.",
        counter_arguments=[
            "Admission is medically necessary.",
            "Documentation supports expectation.",
            "CMS guidance followed."
        ],
        resolution_strategy="Review admission records, physician notes, and CMS guidance.",
        entity_scope="Hospitals",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="CMS Two-Midnight Rule Audits"
    ),
    DoctrineBlock(
        topic="CMS Hospital Price Transparency Rule",
        keywords=["CMS", "hospital price transparency", "public disclosure", "standard charges", "45 CFR 180"],
        conclusion_template="The hospital's price transparency disclosures are {compliant/non-compliant} with CMS rules.",
        reasoning_framework=(
            "1. Review the hospital's public disclosure of standard charges for items and services.\n"
            "2. Assess accessibility, format, and completeness of data.\n"
            "3. Evaluate compliance with machine-readable file and shoppable services requirements.\n"
            "4. Consider CMS audit findings and enforcement actions.\n"
            "5. Conclude compliance with price transparency rule."
        ),
        key_factors=[
            "Disclosure of standard charges",
            "Accessibility and format",
            "Machine-readable file",
            "Shoppable services list",
            "CMS audit findings"
        ],
        primary_authority=["45 CFR 180", "CMS Price Transparency Guidance"],
        burden_holder="Hospital",
        adversary_position="Disclosures are incomplete or inaccessible.",
        counter_arguments=[
            "All requirements are met.",
            "Data is accessible and complete.",
            "Audit findings addressed."
        ],
        resolution_strategy="Review disclosures, website, and audit results.",
        entity_scope="Hospitals",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="CMS Price Transparency Enforcement"
    ),
    DoctrineBlock(
        topic="CMS Hospital Readmissions Reduction Program",
        keywords=["CMS", "hospital readmissions", "reduction program", "quality", "penalties", "42 CFR 412.150"],
        conclusion_template="The hospital's readmission rates are {acceptable/unacceptable} under CMS program standards.",
        reasoning_framework=(
            "1. Review hospital readmission rates for applicable conditions.\n"
            "2. Assess CMS benchmarks and penalty thresholds.\n"
            "3. Evaluate quality improvement initiatives and outcomes.\n"
            "4. Consider CMS penalty assessments and appeals.\n"
            "5. Conclude acceptability of readmission rates."
        ),
        key_factors=[
            "Readmission rates",
            "CMS benchmarks",
            "Quality improvement",
            "Penalty assessments",
            "Appeals"
        ],
        primary_authority=["42 CFR 412.150", "CMS HRRP Guidance"],
        burden_holder="Hospital",
        adversary_position="Readmission rates exceed acceptable thresholds.",
        counter_arguments=[
            "Rates are within benchmarks.",
            "Improvement initiatives are effective.",
            "Penalty assessments are appealed."
        ],
        resolution_strategy="Review rates, benchmarks, and improvement documentation.",
        entity_scope="Hospitals",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="CMS HRRP Penalty Data"
    ),
    DoctrineBlock(
        topic="FDA Orphan Drug Designation",
        keywords=["FDA", "orphan drug", "rare disease", "designation", "incentives", "21 CFR 316"],
        conclusion_template="The drug's orphan designation is {valid/invalid} under FDA regulations.",
        reasoning_framework=(
            "1. Determine if the drug treats a rare disease or condition (affecting fewer than 200,000 persons in the U.S.).\n"
            "2. Review the orphan drug designation application and supporting data.\n"
            "3. Assess FDA review and approval.\n"
            "4. Evaluate post-designation incentives and exclusivity.\n"
            "5. Conclude validity of orphan drug designation."
        ),
        key_factors=[
            "Rare disease status",
            "Application and data",
            "FDA review",
            "Incentives and exclusivity",
            "Post-designation compliance"
        ],
        primary_authority=["21 USC 360bb", "21 CFR 316"],
        burden_holder="Drug sponsor/applicant",
        adversary_position="Drug does not qualify for orphan designation.",
        counter_arguments=[
            "Disease is rare.",
            "Application is complete.",
            "FDA designation granted."
        ],
        resolution_strategy="Review application, FDA decision, and post-designation compliance.",
        entity_scope="Drug manufacturers and sponsors",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FDA Orphan Drug Designations"
    ),
    DoctrineBlock(
        topic="CMS Hospice Conditions of Participation",
        keywords=["CMS", "hospice", "conditions of participation", "quality", "42 CFR 418"],
        conclusion_template="The hospice is {in compliance/not in compliance} with CMS Conditions of Participation.",
        reasoning_framework=(
            "1. Review hospice policies, procedures, and operations for alignment with CoPs.\n"
            "2. Assess survey findings and deficiency reports.\n"
            "3. Evaluate corrective actions taken in response to deficiencies.\n"
            "4. Consider patient outcomes and quality measures.\n"
            "5. Conclude compliance status."
        ),
        key_factors=[
            "Policies and procedures",
            "Survey findings",
            "Corrective actions",
            "Quality measures",
            "Documentation"
        ],
        primary_authority=["42 CFR 418", "CMS Hospice Guidance"],
        burden_holder="Hospice provider",
        adversary_position="Hospice is non-compliant with CoPs.",
        counter_arguments=[
            "All CoPs are met.",
            "Deficiencies have been corrected.",
            "Survey findings are disputed."
        ],
        resolution_strategy="Compare operations to CoPs; review survey and corrective action documentation.",
        entity_scope="Hospice providers",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="CMS Hospice Survey Results"
    ),
    DoctrineBlock(
        topic="SAMHSA 42 CFR Part 2 - Confidentiality of Substance Use Disorder Patient Records",
        keywords=["SAMHSA", "42 CFR Part 2", "confidentiality", "substance use disorder", "patient records"],
        conclusion_template="The disclosure of SUD patient records is {permitted/prohibited} under 42 CFR Part 2.",
        reasoning_framework=(
            "1. Determine if the records are subject to 42 CFR Part 2 (federally assisted SUD programs).\n"
            "2. Assess the purpose and recipient of the disclosure.\n"
            "3. Review patient consent and exceptions (e.g., medical emergency, court order).\n"
            "4. Evaluate documentation of consent and disclosures.\n"
            "5. Conclude permissibility of disclosure."
        ),
        key_factors=[
            "Applicability of Part 2",
            "Purpose of disclosure",
            "Patient consent",
            "Exceptions",
            "Documentation"
        ],
        primary_authority=["42 CFR Part 2", "SAMHSA Guidance"],
        burden_holder="Program disclosing records",
        adversary_position="Disclosure is prohibited under Part 2.",
        counter_arguments=[
            "Valid consent obtained.",
            "Exception applies.",
            "Records not subject to Part 2."
        ],
        resolution_strategy="Review consent, exceptions, and disclosure documentation.",
        entity_scope="SUD programs and recipients",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SAMHSA Enforcement Guidance"
    ),
    DoctrineBlock(
        topic="CMS Home Health Conditions of Participation",
        keywords=["CMS", "home health", "conditions of participation", "quality", "42 CFR 484"],
        conclusion_template="The home health agency is {in compliance/not in compliance} with CMS Conditions of Participation.",
        reasoning_framework=(
            "1. Review agency policies, procedures, and operations for alignment with CoPs.\n"
            "2. Assess survey findings and deficiency reports.\n"
            "3. Evaluate corrective actions taken in response to deficiencies.\n"
            "4. Consider patient outcomes and quality measures.\n"
            "5. Conclude compliance status."
        ),
        key_factors=[
            "Policies and procedures",
            "Survey findings",
            "Corrective actions",
            "Quality measures",
            "Documentation"
        ],
        primary_authority=["42 CFR 484", "CMS Home Health Guidance"],
        burden_holder="Home health agency",
        adversary_position="Agency is non-compliant with CoPs.",
        counter_arguments=[
            "All CoPs are met.",
            "Deficiencies have been corrected.",
            "Survey findings are disputed."
        ],
        resolution_strategy="Compare operations to CoPs; review survey and corrective action documentation.",
        entity_scope="Home health agencies",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="CMS Home Health Survey Results"
    ),
    DoctrineBlock(
        topic="CMS Nursing Home Requirements of Participation",
        keywords=["CMS", "nursing home", "requirements of participation", "quality", "42 CFR 483"],
        conclusion_template="The nursing home is {in compliance/not in compliance} with CMS Requirements of Participation.",
        reasoning_framework=(
            "1. Review nursing home policies, procedures, and operations for alignment with requirements.\n"
            "2. Assess survey findings and deficiency reports.\n"
            "3. Evaluate corrective actions taken in response to deficiencies.\n"
            "4. Consider resident outcomes and quality measures.\n"
            "5. Conclude compliance status."
        ),
        key_factors=[
            "Policies and procedures",
            "Survey findings",
            "Corrective actions",
            "Quality measures",
            "Documentation"
        ],
        primary_authority=["42 CFR 483", "CMS Nursing Home Guidance"],
        burden_holder="Nursing home",
        adversary_position="Nursing home is non-compliant with requirements.",
        counter_arguments=[
            "All requirements are met.",
            "Deficiencies have been corrected.",
            "Survey findings are disputed."
        ],
        resolution_strategy="Compare operations to requirements; review survey and corrective action documentation.",
        entity_scope="Nursing homes",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="CMS Nursing Home Survey Results"
    ),
    DoctrineBlock(
        topic="CMS Outpatient Prospective Payment System (OPPS)",
        keywords=["CMS", "OPPS", "outpatient", "prospective payment", "Medicare", "42 CFR 419"],
        conclusion_template="The hospital's outpatient billing is {compliant/non-compliant} with OPPS requirements.",
        reasoning_framework=(
            "1. Review outpatient services billed under OPPS.\n"
            "2. Assess coding and documentation for accuracy.\n"
            "3. Evaluate payment rates and bundling rules.\n"
            "4. Consider audit findings and appeals.\n"
            "5. Conclude compliance with OPPS requirements."
        ),
        key_factors=[
            "Outpatient services billed",
            "Coding and documentation",
            "Payment rates",
            "Bundling rules",
            "Audit findings"
        ],
        primary_authority=["42 CFR 419", "CMS OPPS Guidance"],
        burden_holder="Hospital",
        adversary_position="Billing is inaccurate or non-compliant.",
        counter_arguments=[
            "Coding is accurate.",
            "Documentation supports billing.",
            "Audit findings addressed."
        ],
        resolution_strategy="Review billing, coding, and audit results.",
        entity_scope="Hospitals",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="CMS OPPS Audits"
    ),
    DoctrineBlock(
        topic="CMS Ambulatory Surgical Center (ASC) Conditions of Coverage",
        keywords=["CMS", "ASC", "ambulatory surgical center", "conditions of coverage", "42 CFR 416"],
        conclusion_template="The ASC is {in compliance/not in compliance} with CMS Conditions of Coverage.",
        reasoning_framework=(
            "1. Review ASC policies, procedures, and operations for alignment with conditions of coverage.\n"
            "2. Assess survey findings and deficiency reports.\n"
            "3. Evaluate corrective actions taken in response to deficiencies.\n"
            "4. Consider patient outcomes and quality measures.\n"
            "5. Conclude compliance status."
        ),
        key_factors=[
            "Policies and procedures",
            "Survey findings",
            "Corrective actions",
            "Quality measures",
            "Documentation"
        ],
        primary_authority=["42 CFR 416", "CMS ASC Guidance"],
        burden_holder="ASC",
        adversary_position="ASC is non-compliant with conditions.",
        counter_arguments=[
            "All conditions are met.",
            "Deficiencies have been corrected.",
            "Survey findings are disputed."
        ],
        resolution_strategy="Compare operations to conditions; review survey and corrective action documentation.",
        entity_scope="Ambulatory surgical centers",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="CMS ASC Survey Results"
    ),
    DoctrineBlock(
        topic="CMS Rural Health Clinic Conditions of Certification",
        keywords=["CMS", "rural health clinic", "conditions of certification", "quality", "42 CFR 491"],
        conclusion_template="The rural health clinic is {in compliance/not in compliance} with CMS Conditions of Certification.",
        reasoning_framework=(
            "1. Review clinic policies, procedures, and operations for alignment with conditions of certification.\n"
            "2. Assess survey findings and deficiency reports.\n"
            "3. Evaluate corrective actions taken in response to deficiencies.\n"
            "4. Consider patient outcomes and quality measures.\n"
            "5. Conclude compliance status."
        ),
        key_factors=[
            "Policies and procedures",
            "Survey findings",
            "Corrective actions",
            "Quality measures",
            "Documentation"
        ],
        primary_authority=["42 CFR 491", "CMS Rural Health Clinic Guidance"],
        burden_holder="Rural health clinic",
        adversary_position="Clinic is non-compliant with conditions.",
        counter_arguments=[
            "All conditions are met.",
            "Deficiencies have been corrected.",
            "Survey findings are disputed."
        ],
        resolution_strategy="Compare operations to conditions; review survey and corrective action documentation.",
        entity_scope="Rural health clinics",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="CMS Rural Health Clinic Survey Results"
    ),
    DoctrineBlock(
        topic="CMS Federally Qualified Health Center (FQHC) Conditions of Coverage",
        keywords=["CMS", "FQHC", "federally qualified health center", "conditions of coverage", "42 CFR 405"],
        conclusion_template="The FQHC is {in compliance/not in compliance} with CMS Conditions of Coverage.",
        reasoning_framework=(
            "1. Review FQHC policies, procedures, and operations for alignment with conditions of coverage.\n"
            "2. Assess survey findings and deficiency reports.\n"
            "3. Evaluate corrective actions taken in response to deficiencies.\n"
            "4. Consider patient outcomes and quality measures.\n"
            "5. Conclude compliance status."
        ),
        key_factors=[
            "Policies and procedures",
            "Survey findings",
            "Corrective actions",
            "Quality measures",
            "Documentation"
        ],
        primary_authority=["42 CFR 405", "CMS FQHC Guidance"],
        burden_holder="FQHC",
        adversary_position="FQHC is non-compliant with conditions.",
        counter_arguments=[
            "All conditions are met.",
            "Deficiencies have been corrected.",
            "Survey findings are disputed."
        ],
        resolution_strategy="Compare operations to conditions; review survey and corrective action documentation.",
        entity_scope="Federally qualified health centers",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="CMS FQHC Survey Results"
    ),
    DoctrineBlock(
        topic="CMS End-Stage Renal Disease (ESRD) Facility Conditions of Coverage",
        keywords=["CMS", "ESRD", "end-stage renal disease", "facility", "conditions of coverage", "42 CFR 494"],
        conclusion_template="The ESRD facility is {in compliance/not in compliance} with CMS Conditions of Coverage.",
        reasoning_framework=(
            "1. Review ESRD facility policies, procedures, and operations for alignment with conditions of coverage.\n"
            "2. Assess survey findings and deficiency reports.\n"
            "3. Evaluate corrective actions taken in response to deficiencies.\n"
            "4. Consider patient outcomes and quality measures.\n"
            "5. Conclude compliance status."
        ),
        key_factors=[
            "Policies and procedures",
            "Survey findings",
            "Corrective actions",
            "Quality measures",
            "Documentation"
        ],
        primary_authority=["42 CFR 494", "CMS ESRD Guidance"],
        burden_holder="ESRD facility",
        adversary_position="Facility is non-compliant with conditions.",
        counter_arguments=[
            "All conditions are met.",
            "Deficiencies have been corrected.",
            "Survey findings are disputed."
        ],
        resolution_strategy="Compare operations to conditions; review survey and corrective action documentation.",
        entity_scope="ESRD facilities",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="CMS ESRD Survey Results"
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
        if query_lower in doctrine.topic.lower() or any(query_lower in kw.lower() for kw in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]