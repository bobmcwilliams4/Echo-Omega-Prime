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
        topic="Incapacity Standard - Texas Definition",
        keywords=["incapacity", "Texas", "guardianship", "mental competence", "PRB06"],
        conclusion_template="A person is considered incapacitated under Texas law if they lack sufficient capacity to manage their own affairs due to mental or physical impairment.",
        reasoning_framework=(
            "Texas Estates Code § 1002.017 defines 'incapacitated person' as an adult who, because of a physical or mental condition, is substantially unable to provide food, clothing, or shelter for themselves, care for their own physical health, or manage their own financial affairs. "
            "The determination of incapacity must be made by clear and convincing evidence, often supported by medical testimony and functional assessments. "
            "Courts consider the individual's ability to understand and communicate decisions, the nature and extent of their impairment, and the risk of harm if left without guardianship. "
            "The standard is not merely diagnosis-based; functional limitations are paramount. "
            "The doctrine emphasizes protection of autonomy and requires the least restrictive intervention."
        ),
        key_factors=[
            "Medical evidence of impairment",
            "Functional assessment of daily living",
            "Ability to manage financial affairs",
            "Risk of harm without guardianship"
        ],
        primary_authority=[
            "Texas Estates Code § 1002.017",
            "Texas Estates Code § 1101.101",
            "In re Guardianship of L.C., 2017 Tex. App. LEXIS 10452"
        ],
        burden_holder="Petitioner seeking guardianship",
        adversary_position="Respondent contests incapacity",
        counter_arguments=[
            "Respondent retains sufficient capacity",
            "Diagnosis does not equate to incapacity",
            "Supported decision-making is sufficient"
        ],
        resolution_strategy="Court evaluates medical and functional evidence, applies statutory definition, and rules based on clear and convincing evidence.",
        entity_scope="Adult individuals alleged to be incapacitated",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of L.C., 2017 Tex. App. LEXIS 10452"
    ),
    DoctrineBlock(
        topic="Least Restrictive Alternative Requirement",
        keywords=["least restrictive", "alternatives", "guardianship", "Texas", "PRB06"],
        conclusion_template="Guardianship may only be imposed if less restrictive alternatives are insufficient to protect the individual's welfare and property.",
        reasoning_framework=(
            "Texas law mandates that courts must consider and document less restrictive alternatives before appointing a guardian. "
            "Alternatives include powers of attorney, supported decision-making agreements, representative payees, and community supports. "
            "The court must find by clear and convincing evidence that no alternative adequately addresses the individual's needs and risks. "
            "This doctrine is rooted in the principle of maximizing autonomy and minimizing state intervention. "
            "Judges must articulate findings regarding the insufficiency of alternatives in the guardianship order."
        ),
        key_factors=[
            "Existence of alternatives",
            "Effectiveness of alternatives",
            "Risk of harm without guardianship",
            "Autonomy preservation"
        ],
        primary_authority=[
            "Texas Estates Code § 1101.001",
            "Texas Estates Code § 1357.003",
            "In re Guardianship of A.E., 552 S.W.3d 903 (Tex. App. 2018)"
        ],
        burden_holder="Petitioner seeking guardianship",
        adversary_position="Respondent proposes alternatives",
        counter_arguments=[
            "Supported decision-making agreement is sufficient",
            "Power of attorney addresses needs",
            "Community supports mitigate risk"
        ],
        resolution_strategy="Court reviews evidence of alternatives, evaluates their sufficiency, and documents findings before imposing guardianship.",
        entity_scope="Individuals subject to guardianship proceedings",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of A.E., 552 S.W.3d 903 (Tex. App. 2018)"
    ),
    DoctrineBlock(
        topic="Guardian Qualification and Priority",
        keywords=["guardian qualification", "priority", "appointment", "Texas", "PRB06"],
        conclusion_template="The court must appoint a qualified guardian, giving priority to statutorily preferred individuals unless disqualified.",
        reasoning_framework=(
            "Texas Estates Code §§ 1104.051-1104.057 establish a hierarchy of persons eligible for appointment as guardian, favoring relatives and those with close ties to the ward. "
            "Disqualification occurs if an individual has a conflict of interest, felony conviction, or incapacity. "
            "The court may bypass priority if it finds the preferred candidate unsuitable or if the ward expresses a preference. "
            "The doctrine balances statutory priority with the ward's best interests and safety."
        ),
        key_factors=[
            "Statutory priority list",
            "Disqualification grounds",
            "Ward's preference",
            "Suitability for guardianship"
        ],
        primary_authority=[
            "Texas Estates Code §§ 1104.051-1104.057",
            "In re Guardianship of S.M., 2016 Tex. App. LEXIS 13344"
        ],
        burden_holder="Petitioner proposing guardian",
        adversary_position="Opposing party challenges qualification",
        counter_arguments=[
            "Candidate is disqualified",
            "Ward prefers another guardian",
            "Conflict of interest exists"
        ],
        resolution_strategy="Court reviews statutory priority, evaluates disqualification, and considers ward's preference before appointment.",
        entity_scope="Prospective guardians and wards",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of S.M., 2016 Tex. App. LEXIS 13344"
    ),
    DoctrineBlock(
        topic="Guardian of Person Duties and Powers",
        keywords=["guardian of person", "duties", "powers", "Texas", "PRB06"],
        conclusion_template="A guardian of the person is responsible for the ward's care, maintenance, and personal decisions, subject to court supervision.",
        reasoning_framework=(
            "The guardian of the person must provide for the ward's food, clothing, shelter, medical care, and education. "
            "They must make decisions regarding residence, health, and personal welfare, always acting in the ward's best interests. "
            "The guardian is subject to court oversight and must avoid conflicts of interest. "
            "All actions must comply with statutory limitations and respect the ward's rights and preferences where feasible."
        ),
        key_factors=[
            "Ward's needs",
            "Best interests",
            "Court supervision",
            "Statutory limitations"
        ],
        primary_authority=[
            "Texas Estates Code § 1151.051",
            "Texas Estates Code § 1151.101",
            "In re Guardianship of J.D., 2019 Tex. App. LEXIS 12013"
        ],
        burden_holder="Guardian",
        adversary_position="Ward or interested party challenges actions",
        counter_arguments=[
            "Guardian failed to act in best interests",
            "Ward's preferences ignored",
            "Statutory duties violated"
        ],
        resolution_strategy="Court reviews guardian's actions, assesses compliance with duties, and may issue orders or sanctions.",
        entity_scope="Guardians of person and wards",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of J.D., 2019 Tex. App. LEXIS 12013"
    ),
    DoctrineBlock(
        topic="Guardian of Estate Financial Duties",
        keywords=["guardian of estate", "financial duties", "Texas", "PRB06"],
        conclusion_template="A guardian of the estate must manage the ward's assets prudently, maintain records, and seek court approval for major transactions.",
        reasoning_framework=(
            "The guardian of the estate is a fiduciary charged with managing the ward's property for their benefit. "
            "Duties include inventorying assets, investing prudently, paying debts, and preserving property. "
            "Major transactions such as sales, leases, or expenditures require court approval. "
            "The guardian must keep detailed records and file annual accountings. "
            "Failure to comply may result in removal or liability for losses."
        ),
        key_factors=[
            "Fiduciary duty",
            "Asset management",
            "Court approval",
            "Recordkeeping"
        ],
        primary_authority=[
            "Texas Estates Code § 1151.101",
            "Texas Estates Code § 1152.001",
            "Texas Estates Code § 1154.051"
        ],
        burden_holder="Guardian of estate",
        adversary_position="Ward or interested party alleges mismanagement",
        counter_arguments=[
            "Guardian failed to preserve assets",
            "Unauthorized transactions",
            "Inadequate accounting"
        ],
        resolution_strategy="Court audits records, reviews transactions, and may order restitution or removal.",
        entity_scope="Guardians of estate and wards",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Texas Estates Code § 1154.051"
    ),
    DoctrineBlock(
        topic="Annual Report and Accounting Requirements",
        keywords=["annual report", "accounting", "guardian", "Texas", "PRB06"],
        conclusion_template="Guardians must file annual reports and accountings detailing the ward's status and financial transactions.",
        reasoning_framework=(
            "Texas law requires guardians to submit annual reports on the ward's well-being and accountings of estate management. "
            "Reports must include residence, health, and activities, while accountings detail receipts, disbursements, and asset status. "
            "Failure to file timely and accurate reports may result in removal or contempt. "
            "The court reviews submissions for compliance and transparency."
        ),
        key_factors=[
            "Timely filing",
            "Accuracy",
            "Transparency",
            "Compliance with statutory requirements"
        ],
        primary_authority=[
            "Texas Estates Code § 1163.001",
            "Texas Estates Code § 1163.101",
            "Texas Estates Code § 1154.051"
        ],
        burden_holder="Guardian",
        adversary_position="Court or interested party challenges report",
        counter_arguments=[
            "Report is incomplete",
            "Accounting is inaccurate",
            "Guardian failed to file"
        ],
        resolution_strategy="Court reviews filings, orders corrections, or removes guardian for noncompliance.",
        entity_scope="Guardians and wards",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Texas Estates Code § 1163.001"
    ),
    DoctrineBlock(
        topic="Guardian Ad Litem Role and Duties",
        keywords=["guardian ad litem", "role", "duties", "Texas", "PRB06"],
        conclusion_template="A guardian ad litem is appointed to represent the ward's best interests during guardianship proceedings.",
        reasoning_framework=(
            "The guardian ad litem is a neutral party tasked with investigating the ward's circumstances and advocating for their best interests. "
            "They may interview the ward, review records, and make recommendations to the court. "
            "Their role is distinct from the attorney ad litem, who represents the ward's wishes. "
            "The guardian ad litem's findings influence the court's decision on guardianship and scope."
        ),
        key_factors=[
            "Impartial investigation",
            "Best interests advocacy",
            "Reporting to court",
            "Distinction from attorney ad litem"
        ],
        primary_authority=[
            "Texas Estates Code § 1054.151",
            "Texas Estates Code § 1054.152",
            "In re Guardianship of J.C., 2015 Tex. App. LEXIS 10903"
        ],
        burden_holder="Guardian ad litem",
        adversary_position="Parties challenge recommendations",
        counter_arguments=[
            "Guardian ad litem is biased",
            "Findings are unsupported",
            "Ward's wishes not considered"
        ],
        resolution_strategy="Court evaluates guardian ad litem's report and recommendations, weighs against other evidence.",
        entity_scope="Guardianship proceedings",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of J.C., 2015 Tex. App. LEXIS 10903"
    ),
    DoctrineBlock(
        topic="Temporary Guardianship Emergency Appointment",
        keywords=["temporary guardianship", "emergency", "appointment", "Texas", "PRB06"],
        conclusion_template="A temporary guardian may be appointed in emergencies to protect the ward's person or estate pending a full hearing.",
        reasoning_framework=(
            "Texas Estates Code § 1251.001 authorizes temporary guardianship when immediate action is necessary to prevent harm to the ward or their property. "
            "The court must find probable cause and specify the scope and duration of the temporary appointment. "
            "Notice and hearing requirements are relaxed, but due process protections remain. "
            "Temporary guardianship expires upon resolution of the emergency or completion of the full guardianship hearing."
        ),
        key_factors=[
            "Emergency circumstances",
            "Probable cause",
            "Scope and duration",
            "Due process"
        ],
        primary_authority=[
            "Texas Estates Code § 1251.001",
            "Texas Estates Code § 1251.003",
            "In re Guardianship of M.M., 2018 Tex. App. LEXIS 10422"
        ],
        burden_holder="Petitioner seeking temporary guardianship",
        adversary_position="Respondent contests emergency",
        counter_arguments=[
            "No emergency exists",
            "Due process violated",
            "Scope is excessive"
        ],
        resolution_strategy="Court reviews evidence, issues temporary orders, and schedules full hearing.",
        entity_scope="Individuals facing imminent harm",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of M.M., 2018 Tex. App. LEXIS 10422"
    ),
    DoctrineBlock(
        topic="Removal of Guardian for Cause",
        keywords=["removal", "guardian", "cause", "Texas", "PRB06"],
        conclusion_template="A guardian may be removed for cause if they breach duties, commit misconduct, or become disqualified.",
        reasoning_framework=(
            "Texas Estates Code § 1203.051 enumerates grounds for removal, including mismanagement, neglect, conflict of interest, incapacity, or criminal conviction. "
            "The court may act on its own motion or upon petition by an interested party. "
            "Removal proceedings require notice and opportunity to respond. "
            "The doctrine protects the ward's interests and integrity of the guardianship system."
        ),
        key_factors=[
            "Breach of fiduciary duty",
            "Misconduct",
            "Disqualification",
            "Procedural fairness"
        ],
        primary_authority=[
            "Texas Estates Code § 1203.051",
            "Texas Estates Code § 1203.052",
            "In re Guardianship of R.B., 2017 Tex. App. LEXIS 10311"
        ],
        burden_holder="Petitioner seeking removal",
        adversary_position="Guardian contests removal",
        counter_arguments=[
            "No breach occurred",
            "Removal is retaliatory",
            "Procedural defects"
        ],
        resolution_strategy="Court conducts hearing, reviews evidence, and orders removal if cause is proven.",
        entity_scope="Guardians and wards",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of R.B., 2017 Tex. App. LEXIS 10311"
    ),
    DoctrineBlock(
        topic="Ward Rights and Due Process Protections",
        keywords=["ward rights", "due process", "guardianship", "Texas", "PRB06"],
        conclusion_template="Wards are entitled to notice, representation, and participation in guardianship proceedings, with all due process protections.",
        reasoning_framework=(
            "Texas Estates Code §§ 1051.104 and 1054.006 guarantee wards notice of proceedings, opportunity to be heard, and representation by attorney ad litem. "
            "Wards may contest guardianship, present evidence, and appeal orders. "
            "Due process requires fair procedures, impartial decision-making, and protection of fundamental rights. "
            "The doctrine ensures guardianship is not imposed arbitrarily or without adequate safeguards."
        ),
        key_factors=[
            "Notice",
            "Representation",
            "Opportunity to be heard",
            "Appeal rights"
        ],
        primary_authority=[
            "Texas Estates Code § 1051.104",
            "Texas Estates Code § 1054.006",
            "In re Guardianship of K.E., 2014 Tex. App. LEXIS 12903"
        ],
        burden_holder="Court and parties",
        adversary_position="Ward alleges due process violations",
        counter_arguments=[
            "Notice was insufficient",
            "Representation was inadequate",
            "Hearing was unfair"
        ],
        resolution_strategy="Court reviews procedural compliance, remedies violations, and may vacate orders.",
        entity_scope="Wards and guardianship participants",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="In re Guardianship of K.E., 2014 Tex. App. LEXIS 12903"
    ),
    DoctrineBlock(
        topic="Modification and Restoration of Capacity",
        keywords=["modification", "restoration", "capacity", "guardianship", "Texas", "PRB06"],
        conclusion_template="A guardianship may be modified or terminated if the ward regains capacity or circumstances change.",
        reasoning_framework=(
            "Texas Estates Code § 1202.051 allows modification or termination of guardianship upon proof that the ward has regained capacity or that the need for guardianship has changed. "
            "The ward or interested parties may petition for restoration, supported by medical evidence and functional assessments. "
            "The court must find by preponderance of evidence that restoration is warranted. "
            "The doctrine promotes autonomy and periodic review of guardianship necessity."
        ),
        key_factors=[
            "Medical evidence",
            "Functional improvement",
            "Changed circumstances",
            "Petition for restoration"
        ],
        primary_authority=[
            "Texas Estates Code § 1202.051",
            "Texas Estates Code § 1202.053",
            "In re Guardianship of B.A., 2016 Tex. App. LEXIS 11243"
        ],
        burden_holder="Petitioner seeking modification",
        adversary_position="Guardian contests restoration",
        counter_arguments=[
            "Ward remains incapacitated",
            "Circumstances unchanged",
            "Evidence is insufficient"
        ],
        resolution_strategy="Court reviews evidence, conducts hearing, and modifies or terminates guardianship as appropriate.",
        entity_scope="Wards and guardians",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of B.A., 2016 Tex. App. LEXIS 11243"
    ),
    DoctrineBlock(
        topic="Minor Guardianship Distinctions",
        keywords=["minor guardianship", "distinctions", "Texas", "PRB06"],
        conclusion_template="Guardianship of minors differs from adult guardianship, focusing on parental absence, best interests, and statutory requirements.",
        reasoning_framework=(
            "Texas Estates Code §§ 1104.151-1104.155 govern guardianship of minors, typically arising when parents are deceased, incapacitated, or unfit. "
            "Courts prioritize appointment of relatives and consider the minor's best interests. "
            "Procedures differ from adult guardianship, with less emphasis on incapacity and more on parental absence or unfitness. "
            "The doctrine ensures minors receive care and protection until adulthood."
        ),
        key_factors=[
            "Parental absence",
            "Best interests",
            "Relative preference",
            "Statutory requirements"
        ],
        primary_authority=[
            "Texas Estates Code §§ 1104.151-1104.155",
            "Texas Family Code § 153.002",
            "In re Guardianship of C.M., 2017 Tex. App. LEXIS 10194"
        ],
        burden_holder="Petitioner seeking guardianship",
        adversary_position="Other relatives or parties contest appointment",
        counter_arguments=[
            "Relative is unfit",
            "Minor prefers another guardian",
            "Best interests not served"
        ],
        resolution_strategy="Court reviews evidence, applies statutory criteria, and appoints guardian in minor's best interests.",
        entity_scope="Minors and prospective guardians",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of C.M., 2017 Tex. App. LEXIS 10194"
    ),
    DoctrineBlock(
        topic="Guardian Bond Requirements and Waiver",
        keywords=["guardian bond", "requirements", "waiver", "Texas", "PRB06"],
        conclusion_template="Guardians must post a bond to secure faithful performance, unless waived by court for cause.",
        reasoning_framework=(
            "Texas Estates Code §§ 1105.101-1105.104 require guardians to post a bond before letters of guardianship are issued. "
            "The bond protects the ward against losses due to guardian misconduct or mismanagement. "
            "The court may waive the bond for relatives, corporate guardians, or if the estate is minimal. "
            "Failure to post bond precludes guardian from acting."
        ),
        key_factors=[
            "Bond amount",
            "Waiver criteria",
            "Protection of ward",
            "Compliance"
        ],
        primary_authority=[
            "Texas Estates Code §§ 1105.101-1105.104",
            "Texas Estates Code § 1105.151",
            "In re Guardianship of E.L., 2018 Tex. App. LEXIS 10521"
        ],
        burden_holder="Guardian",
        adversary_position="Court or parties challenge waiver",
        counter_arguments=[
            "Bond is necessary for protection",
            "Guardian is not eligible for waiver",
            "Estate is substantial"
        ],
        resolution_strategy="Court reviews waiver request, evaluates statutory criteria, and issues order.",
        entity_scope="Guardians and wards",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of E.L., 2018 Tex. App. LEXIS 10521"
    ),
    DoctrineBlock(
        topic="Guardianship Venue and Jurisdiction",
        keywords=["venue", "jurisdiction", "guardianship", "Texas", "PRB06"],
        conclusion_template="Guardianship proceedings must be filed in the county where the ward resides or where property is located.",
        reasoning_framework=(
            "Texas Estates Code §§ 1021.002-1021.003 establish venue for guardianship in the county of the ward's residence or where the majority of property is situated. "
            "Jurisdiction is vested in statutory probate courts or county courts with probate jurisdiction. "
            "Improper venue may result in transfer or dismissal. "
            "The doctrine ensures proceedings are accessible and efficient."
        ),
        key_factors=[
            "Ward's residence",
            "Property location",
            "Court jurisdiction",
            "Statutory compliance"
        ],
        primary_authority=[
            "Texas Estates Code §§ 1021.002-1021.003",
            "Texas Estates Code § 1022.002",
            "In re Guardianship of D.M., 2016 Tex. App. LEXIS 13444"
        ],
        burden_holder="Petitioner",
        adversary_position="Respondent challenges venue",
        counter_arguments=[
            "Ward resides elsewhere",
            "Property is in another county",
            "Court lacks jurisdiction"
        ],
        resolution_strategy="Court reviews evidence of residence and property, transfers or dismisses as appropriate.",
        entity_scope="Guardianship applicants and wards",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of D.M., 2016 Tex. App. LEXIS 13444"
    ),
    DoctrineBlock(
        topic="Supported Decision-Making Agreement Alternative",
        keywords=["supported decision-making", "agreement", "alternative", "Texas", "PRB06"],
        conclusion_template="Supported decision-making agreements may serve as a less restrictive alternative to guardianship for adults with disabilities.",
        reasoning_framework=(
            "Texas Estates Code § 1357.003 recognizes supported decision-making agreements as a viable alternative to guardianship. "
            "Such agreements allow individuals with disabilities to retain legal capacity while receiving assistance in understanding and making decisions. "
            "Courts must consider the existence and effectiveness of such agreements before imposing guardianship. "
            "The doctrine promotes autonomy and inclusion."
        ),
        key_factors=[
            "Existence of agreement",
            "Effectiveness",
            "Autonomy preservation",
            "Disability status"
        ],
        primary_authority=[
            "Texas Estates Code § 1357.003",
            "Texas Estates Code § 1101.001",
            "In re Guardianship of A.E., 552 S.W.3d 903"
        ],
        burden_holder="Petitioner",
        adversary_position="Respondent proposes agreement",
        counter_arguments=[
            "Agreement is ineffective",
            "Risks remain",
            "Guardianship is necessary"
        ],
        resolution_strategy="Court reviews agreement, assesses sufficiency, and may decline guardianship.",
        entity_scope="Adults with disabilities",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of A.E., 552 S.W.3d 903"
    ),
    DoctrineBlock(
        topic="Interstate Transfer of Guardianship",
        keywords=["interstate transfer", "guardianship", "Texas", "PRB06"],
        conclusion_template="Guardianship may be transferred to or from Texas to facilitate the ward's relocation and continuity of care.",
        reasoning_framework=(
            "Texas Estates Code §§ 1253.001-1253.006 provide procedures for transferring guardianship to or from Texas. "
            "Transfers require court approval, notice to interested parties, and evidence of necessity. "
            "The doctrine ensures continuity of care and avoids jurisdictional conflicts. "
            "Courts coordinate with out-of-state counterparts to protect the ward's interests."
        ),
        key_factors=[
            "Ward's relocation",
            "Continuity of care",
            "Court approval",
            "Jurisdictional coordination"
        ],
        primary_authority=[
            "Texas Estates Code §§ 1253.001-1253.006",
            "Uniform Adult Guardianship and Protective Proceedings Jurisdiction Act",
            "In re Guardianship of S.F., 2019 Tex. App. LEXIS 12014"
        ],
        burden_holder="Petitioner seeking transfer",
        adversary_position="Interested parties contest transfer",
        counter_arguments=[
            "Transfer is unnecessary",
            "Ward's interests are not served",
            "Jurisdictional issues"
        ],
        resolution_strategy="Court reviews petition, coordinates with other jurisdictions, and orders transfer if appropriate.",
        entity_scope="Wards relocating interstate",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of S.F., 2019 Tex. App. LEXIS 12014"
    ),
    DoctrineBlock(
        topic="Guardian Compensation and Expenses",
        keywords=["guardian compensation", "expenses", "Texas", "PRB06"],
        conclusion_template="Guardians may receive reasonable compensation and reimbursement for expenses, subject to court approval.",
        reasoning_framework=(
            "Texas Estates Code §§ 1155.001-1155.004 authorize compensation for guardians based on reasonable services rendered. "
            "Compensation and expenses must be documented and approved by the court. "
            "Excessive or unsupported claims may be denied. "
            "The doctrine balances incentivizing guardianship with protecting the ward's estate."
        ),
        key_factors=[
            "Reasonableness",
            "Documentation",
            "Court approval",
            "Estate preservation"
        ],
        primary_authority=[
            "Texas Estates Code §§ 1155.001-1155.004",
            "Texas Estates Code § 1155.151",
            "In re Guardianship of M.H., 2017 Tex. App. LEXIS 10312"
        ],
        burden_holder="Guardian",
        adversary_position="Interested parties challenge compensation",
        counter_arguments=[
            "Compensation is excessive",
            "Expenses are unsupported",
            "Estate cannot afford"
        ],
        resolution_strategy="Court reviews claims, approves reasonable amounts, and denies improper requests.",
        entity_scope="Guardians and wards",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of M.H., 2017 Tex. App. LEXIS 10312"
    ),
    DoctrineBlock(
        topic="Medical Consent and Treatment Decisions",
        keywords=["medical consent", "treatment", "guardian", "Texas", "PRB06"],
        conclusion_template="Guardians may consent to medical treatment for the ward, subject to statutory limitations and court oversight.",
        reasoning_framework=(
            "Texas Estates Code § 1151.051 authorizes guardians to consent to medical and psychiatric treatment for the ward. "
            "Certain procedures, such as involuntary commitment or sterilization, require specific court orders. "
            "Guardians must act in the ward's best interests and consult with healthcare providers. "
            "The doctrine protects the ward's health while respecting autonomy and legal safeguards."
        ),
        key_factors=[
            "Best interests",
            "Statutory limitations",
            "Court orders",
            "Healthcare consultation"
        ],
        primary_authority=[
            "Texas Estates Code § 1151.051",
            "Texas Estates Code § 1151.101",
            "In re Guardianship of J.D., 2019 Tex. App. LEXIS 12013"
        ],
        burden_holder="Guardian",
        adversary_position="Ward or interested party challenges consent",
        counter_arguments=[
            "Consent is not in best interests",
            "Statutory limits exceeded",
            "Ward's wishes ignored"
        ],
        resolution_strategy="Court reviews medical decisions, issues orders, and may restrict guardian's authority.",
        entity_scope="Guardians and wards",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of J.D., 2019 Tex. App. LEXIS 12013"
    ),
    DoctrineBlock(
        topic="Guardian Duty to Avoid Conflicts of Interest",
        keywords=["conflict of interest", "guardian", "duty", "Texas", "PRB06"],
        conclusion_template="Guardians must avoid conflicts of interest and act solely for the ward's benefit.",
        reasoning_framework=(
            "Texas Estates Code § 1054.003 prohibits guardians from engaging in transactions that present a conflict of interest with the ward. "
            "Guardians must disclose potential conflicts to the court and seek approval for any questionable actions. "
            "Failure to avoid conflicts may result in removal or liability. "
            "The doctrine ensures fiduciary integrity and protects the ward's interests."
        ),
        key_factors=[
            "Disclosure",
            "Court approval",
            "Fiduciary duty",
            "Ward's benefit"
        ],
        primary_authority=[
            "Texas Estates Code § 1054.003",
            "Texas Estates Code § 1203.051",
            "In re Guardianship of R.B., 2017 Tex. App. LEXIS 10311"
        ],
        burden_holder="Guardian",
        adversary_position="Interested party alleges conflict",
        counter_arguments=[
            "Guardian acted for own benefit",
            "Conflict was undisclosed",
            "Ward suffered harm"
        ],
        resolution_strategy="Court reviews disclosures, orders remedies, and may remove guardian.",
        entity_scope="Guardians and wards",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of R.B., 2017 Tex. App. LEXIS 10311"
    ),
    DoctrineBlock(
        topic="Limited Guardianship Tailored to Individual Needs",
        keywords=["limited guardianship", "individual needs", "Texas", "PRB06"],
        conclusion_template="Guardianship should be limited to the ward's specific needs, preserving as much autonomy as possible.",
        reasoning_framework=(
            "Texas Estates Code § 1101.151 requires courts to tailor guardianship orders to the ward's actual limitations, restricting authority to areas where the ward lacks capacity. "
            "The doctrine promotes autonomy and avoids unnecessary deprivation of rights. "
            "Courts must articulate the scope of guardianship and review periodically for possible reduction."
        ),
        key_factors=[
            "Ward's functional abilities",
            "Scope of incapacity",
            "Autonomy preservation",
            "Periodic review"
        ],
        primary_authority=[
            "Texas Estates Code § 1101.151",
            "Texas Estates Code § 1202.051",
            "In re Guardianship of B.A., 2016 Tex. App. LEXIS 11243"
        ],
        burden_holder="Court and petitioner",
        adversary_position="Ward or parties challenge scope",
        counter_arguments=[
            "Scope is excessive",
            "Ward retains abilities",
            "Rights are unnecessarily restricted"
        ],
        resolution_strategy="Court reviews evidence, limits guardianship, and schedules periodic review.",
        entity_scope="Wards and guardians",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of B.A., 2016 Tex. App. LEXIS 11243"
    ),
    DoctrineBlock(
        topic="Powers of Attorney as Guardianship Alternative",
        keywords=["powers of attorney", "alternative", "guardianship", "Texas", "PRB06"],
        conclusion_template="A valid power of attorney may serve as a less restrictive alternative to guardianship if it adequately protects the individual's interests.",
        reasoning_framework=(
            "Texas Estates Code § 1101.001 requires courts to consider powers of attorney as an alternative to guardianship. "
            "The power of attorney must be valid, effective, and sufficient to address the individual's needs. "
            "If the agent is trustworthy and the document covers necessary areas, guardianship may be unnecessary. "
            "The doctrine emphasizes autonomy and minimizes state intervention."
        ),
        key_factors=[
            "Validity of power of attorney",
            "Scope of authority",
            "Agent's trustworthiness",
            "Effectiveness"
        ],
        primary_authority=[
            "Texas Estates Code § 1101.001",
            "Texas Estates Code § 1357.003",
            "In re Guardianship of A.E., 552 S.W.3d 903"
        ],
        burden_holder="Petitioner",
        adversary_position="Respondent proposes power of attorney",
        counter_arguments=[
            "Power of attorney is invalid",
            "Agent is untrustworthy",
            "Needs are unmet"
        ],
        resolution_strategy="Court reviews document, assesses sufficiency, and may decline guardianship.",
        entity_scope="Adults with powers of attorney",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of A.E., 552 S.W.3d 903"
    ),
    DoctrineBlock(
        topic="Guardianship of Veterans and VA Benefits",
        keywords=["veterans", "VA benefits", "guardianship", "Texas", "PRB06"],
        conclusion_template="Guardianship for veterans receiving VA benefits must comply with federal and state requirements, including appointment of VA-approved fiduciaries.",
        reasoning_framework=(
            "Texas Estates Code §§ 1105.151-1105.153 and federal regulations require appointment of guardians for veterans receiving VA benefits. "
            "The VA may designate fiduciaries and require court approval for management of benefits. "
            "Guardians must comply with reporting and oversight requirements. "
            "The doctrine ensures proper management of federal funds and protection of veterans."
        ),
        key_factors=[
            "VA approval",
            "Federal compliance",
            "Reporting requirements",
            "Veteran's interests"
        ],
        primary_authority=[
            "Texas Estates Code §§ 1105.151-1105.153",
            "38 CFR § 13.100",
            "In re Guardianship of J.F., 2015 Tex. App. LEXIS 10904"
        ],
        burden_holder="Guardian",
        adversary_position="VA or interested parties challenge appointment",
        counter_arguments=[
            "Guardian lacks VA approval",
            "Reporting is insufficient",
            "Funds are mismanaged"
        ],
        resolution_strategy="Court coordinates with VA, reviews compliance, and may appoint or remove guardian.",
        entity_scope="Veterans and guardians",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of J.F., 2015 Tex. App. LEXIS 10904"
    ),
    DoctrineBlock(
        topic="Appointment of Corporate or Professional Guardians",
        keywords=["corporate guardian", "professional guardian", "appointment", "Texas", "PRB06"],
        conclusion_template="Corporate or professional guardians may be appointed if no suitable individual is available, subject to statutory qualifications.",
        reasoning_framework=(
            "Texas Estates Code §§ 1104.002-1104.003 permit appointment of corporate or professional guardians when no qualified relative or individual is available. "
            "Such guardians must meet licensing, bonding, and reporting requirements. "
            "The doctrine ensures wards receive care when family is unavailable, while maintaining oversight."
        ),
        key_factors=[
            "Availability of individuals",
            "Licensing",
            "Bonding",
            "Reporting"
        ],
        primary_authority=[
            "Texas Estates Code §§ 1104.002-1104.003",
            "Texas Estates Code § 1105.101",
            "In re Guardianship of S.M., 2016 Tex. App. LEXIS 13344"
        ],
        burden_holder="Petitioner",
        adversary_position="Interested parties challenge appointment",
        counter_arguments=[
            "Individual is available",
            "Guardian lacks qualifications",
            "Oversight is insufficient"
        ],
        resolution_strategy="Court reviews qualifications, appoints guardian, and monitors compliance.",
        entity_scope="Wards and corporate/professional guardians",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of S.M., 2016 Tex. App. LEXIS 13344"
    ),
    DoctrineBlock(
        topic="Guardian's Authority Over Ward's Residence and Living Situation",
        keywords=["residence", "living situation", "guardian authority", "Texas", "PRB06"],
        conclusion_template="Guardians may determine the ward's residence, subject to court approval and consideration of the ward's preferences.",
        reasoning_framework=(
            "Texas Estates Code § 1151.051 grants guardians authority to decide the ward's residence, including placement in facilities. "
            "Court approval is required for moves to restrictive settings. "
            "Guardians must consider the ward's preferences and best interests. "
            "The doctrine balances protection with autonomy."
        ),
        key_factors=[
            "Court approval",
            "Ward's preferences",
            "Best interests",
            "Type of residence"
        ],
        primary_authority=[
            "Texas Estates Code § 1151.051",
            "Texas Estates Code § 1151.101",
            "In re Guardianship of J.D., 2019 Tex. App. LEXIS 12013"
        ],
        burden_holder="Guardian",
        adversary_position="Ward or parties challenge placement",
        counter_arguments=[
            "Placement is inappropriate",
            "Preferences ignored",
            "Court approval not obtained"
        ],
        resolution_strategy="Court reviews placement, considers preferences, and issues orders.",
        entity_scope="Guardians and wards",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of J.D., 2019 Tex. App. LEXIS 12013"
    ),
    DoctrineBlock(
        topic="Emergency Orders and Immediate Protection",
        keywords=["emergency orders", "immediate protection", "guardianship", "Texas", "PRB06"],
        conclusion_template="Courts may issue emergency orders to protect the ward pending full guardianship proceedings.",
        reasoning_framework=(
            "Texas Estates Code § 1251.001 authorizes emergency orders to prevent imminent harm to the ward or estate. "
            "Orders may include restraining actions, freezing assets, or appointing temporary guardians. "
            "Due process protections apply, but urgency may justify expedited procedures. "
            "The doctrine ensures immediate safety and preservation of assets."
        ),
        key_factors=[
            "Imminent harm",
            "Urgency",
            "Due process",
            "Scope of order"
        ],
        primary_authority=[
            "Texas Estates Code § 1251.001",
            "Texas Estates Code § 1251.003",
            "In re Guardianship of M.M., 2018 Tex. App. LEXIS 10422"
        ],
        burden_holder="Petitioner",
        adversary_position="Respondent contests emergency",
        counter_arguments=[
            "No imminent harm",
            "Procedures violated",
            "Order is excessive"
        ],
        resolution_strategy="Court reviews evidence, issues orders, and schedules hearing.",
        entity_scope="Wards and guardianship applicants",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of M.M., 2018 Tex. App. LEXIS 10422"
    ),
    DoctrineBlock(
        topic="Guardian Liability for Negligence or Misconduct",
        keywords=["guardian liability", "negligence", "misconduct", "Texas", "PRB06"],
        conclusion_template="Guardians are liable for losses caused by negligence or misconduct in managing the ward's affairs.",
        reasoning_framework=(
            "Texas Estates Code § 1203.051 imposes liability on guardians for losses resulting from mismanagement, neglect, or breach of fiduciary duty. "
            "Guardians must act prudently and in the ward's best interests. "
            "Courts may order restitution, removal, or damages. "
            "The doctrine deters misconduct and protects the ward's estate."
        ),
        key_factors=[
            "Negligence",
            "Misconduct",
            "Losses",
            "Fiduciary duty"
        ],
        primary_authority=[
            "Texas Estates Code § 1203.051",
            "Texas Estates Code § 1151.101",
            "In re Guardianship of R.B., 2017 Tex. App. LEXIS 10311"
        ],
        burden_holder="Interested party alleging misconduct",
        adversary_position="Guardian denies liability",
        counter_arguments=[
            "Actions were prudent",
            "No losses occurred",
            "Duty was fulfilled"
        ],
        resolution_strategy="Court reviews evidence, orders remedies, and may remove guardian.",
        entity_scope="Guardians and wards",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of R.B., 2017 Tex. App. LEXIS 10311"
    ),
    DoctrineBlock(
        topic="Guardianship for Persons with Intellectual Disabilities",
        keywords=["intellectual disabilities", "guardianship", "Texas", "PRB06"],
        conclusion_template="Guardianship for persons with intellectual disabilities must be tailored to their functional abilities and consider supported decision-making alternatives.",
        reasoning_framework=(
            "Texas Estates Code § 1357.003 and § 1101.151 require courts to assess functional abilities and consider supported decision-making agreements before imposing guardianship. "
            "The doctrine emphasizes autonomy, inclusion, and periodic review of necessity. "
            "Courts must avoid unnecessary deprivation of rights and tailor orders to individual needs."
        ),
        key_factors=[
            "Functional assessment",
            "Supported decision-making",
            "Autonomy",
            "Periodic review"
        ],
        primary_authority=[
            "Texas Estates Code § 1357.003",
            "Texas Estates Code § 1101.151",
            "In re Guardianship of A.E., 552 S.W.3d 903"
        ],
        burden_holder="Petitioner",
        adversary_position="Respondent proposes alternatives",
        counter_arguments=[
            "Supported decision-making is sufficient",
            "Guardianship is excessive",
            "Rights are unnecessarily restricted"
        ],
        resolution_strategy="Court reviews evidence, considers alternatives, and limits guardianship.",
        entity_scope="Persons with intellectual disabilities",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of A.E., 552 S.W.3d 903"
    ),
    DoctrineBlock(
        topic="Guardianship for Persons with Mental Illness",
        keywords=["mental illness", "guardianship", "Texas", "PRB06"],
        conclusion_template="Guardianship for persons with mental illness requires clear and convincing evidence of incapacity and risk of harm.",
        reasoning_framework=(
            "Texas Estates Code § 1002.017 and § 1101.101 require proof that mental illness renders the individual unable to manage their affairs or care for themselves. "
            "Diagnosis alone is insufficient; functional limitations and risk of harm must be demonstrated. "
            "The doctrine protects autonomy and ensures guardianship is imposed only when necessary."
        ),
        key_factors=[
            "Medical evidence",
            "Functional limitations",
            "Risk of harm",
            "Clear and convincing proof"
        ],
        primary_authority=[
            "Texas Estates Code § 1002.017",
            "Texas Estates Code § 1101.101",
            "In re Guardianship of L.C., 2017 Tex. App. LEXIS 10452"
        ],
        burden_holder="Petitioner",
        adversary_position="Respondent contests incapacity",
        counter_arguments=[
            "Diagnosis is insufficient",
            "Functional abilities retained",
            "Risk is minimal"
        ],
        resolution_strategy="Court reviews evidence, applies statutory standard, and rules accordingly.",
        entity_scope="Persons with mental illness",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of L.C., 2017 Tex. App. LEXIS 10452"
    ),
    DoctrineBlock(
        topic="Guardianship for Persons with Dementia",
        keywords=["dementia", "guardianship", "Texas", "PRB06"],
        conclusion_template="Guardianship for persons with dementia requires evidence of impaired decision-making and inability to manage affairs.",
        reasoning_framework=(
            "Texas Estates Code § 1002.017 and § 1101.101 require proof that dementia impairs the individual's ability to manage personal and financial affairs. "
            "Functional assessments and medical testimony are critical. "
            "The doctrine ensures guardianship is imposed only when necessary and tailored to actual needs."
        ),
        key_factors=[
            "Medical diagnosis",
            "Functional impairment",
            "Risk of harm",
            "Clear and convincing evidence"
        ],
        primary_authority=[
            "Texas Estates Code § 1002.017",
            "Texas Estates Code § 1101.101",
            "In re Guardianship of L.C., 2017 Tex. App. LEXIS 10452"
        ],
        burden_holder="Petitioner",
        adversary_position="Respondent contests incapacity",
        counter_arguments=[
            "Functional abilities retained",
            "Diagnosis is insufficient",
            "Risk is minimal"
        ],
        resolution_strategy="Court reviews evidence, applies statutory standard, and rules accordingly.",
        entity_scope="Persons with dementia",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of L.C., 2017 Tex. App. LEXIS 10452"
    ),
    DoctrineBlock(
        topic="Guardianship for Persons with Physical Disabilities",
        keywords=["physical disabilities", "guardianship", "Texas", "PRB06"],
        conclusion_template="Guardianship for persons with physical disabilities requires proof that the disability substantially impairs ability to manage affairs.",
        reasoning_framework=(
            "Texas Estates Code § 1002.017 and § 1101.101 require evidence that physical disability renders the individual unable to provide for themselves or manage property. "
            "Functional limitations, not diagnosis alone, are determinative. "
            "The doctrine ensures guardianship is imposed only when necessary."
        ),
        key_factors=[
            "Functional impairment",
            "Medical evidence",
            "Risk of harm",
            "Clear and convincing proof"
        ],
        primary_authority=[
            "Texas Estates Code § 1002.017",
            "Texas Estates Code § 1101.101",
            "In re Guardianship of L.C., 2017 Tex. App. LEXIS 10452"
        ],
        burden_holder="Petitioner",
        adversary_position="Respondent contests incapacity",
        counter_arguments=[
            "Disability does not impair management",
            "Functional abilities retained",
            "Risk is minimal"
        ],
        resolution_strategy="Court reviews evidence, applies statutory standard, and rules accordingly.",
        entity_scope="Persons with physical disabilities",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of L.C., 2017 Tex. App. LEXIS 10452"
    ),
    DoctrineBlock(
        topic="Guardianship for Persons with Substance Use Disorders",
        keywords=["substance use disorder", "guardianship", "Texas", "PRB06"],
        conclusion_template="Guardianship for persons with substance use disorders requires proof of incapacity and risk of harm, not mere diagnosis.",
        reasoning_framework=(
            "Texas Estates Code § 1002.017 and § 1101.101 require evidence that substance use disorder impairs the individual's ability to manage affairs or care for themselves. "
            "Diagnosis alone is insufficient; functional impairment and risk of harm must be demonstrated. "
            "The doctrine protects autonomy and ensures guardianship is imposed only when necessary."
        ),
        key_factors=[
            "Functional impairment",
            "Medical evidence",
            "Risk of harm",
            "Clear and convincing proof"
        ],
        primary_authority=[
            "Texas Estates Code § 1002.017",
            "Texas Estates Code § 1101.101",
            "In re Guardianship of L.C., 2017 Tex. App. LEXIS 10452"
        ],
        burden_holder="Petitioner",
        adversary_position="Respondent contests incapacity",
        counter_arguments=[
            "Diagnosis is insufficient",
            "Functional abilities retained",
            "Risk is minimal"
        ],
        resolution_strategy="Court reviews evidence, applies statutory standard, and rules accordingly.",
        entity_scope="Persons with substance use disorders",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of L.C., 2017 Tex. App. LEXIS 10452"
    ),
    DoctrineBlock(
        topic="Guardianship for Persons with Developmental Disabilities",
        keywords=["developmental disabilities", "guardianship", "Texas", "PRB06"],
        conclusion_template="Guardianship for persons with developmental disabilities must be tailored to functional abilities and consider alternatives.",
        reasoning_framework=(
            "Texas Estates Code § 1357.003 and § 1101.151 require courts to assess functional abilities and consider supported decision-making agreements before imposing guardianship. "
            "The doctrine emphasizes autonomy, inclusion, and periodic review of necessity. "
            "Courts must avoid unnecessary deprivation of rights and tailor orders to individual needs."
        ),
        key_factors=[
            "Functional assessment",
            "Supported decision-making",
            "Autonomy",
            "Periodic review"
        ],
        primary_authority=[
            "Texas Estates Code § 1357.003",
            "Texas Estates Code § 1101.151",
            "In re Guardianship of A.E., 552 S.W.3d 903"
        ],
        burden_holder="Petitioner",
        adversary_position="Respondent proposes alternatives",
        counter_arguments=[
            "Supported decision-making is sufficient",
            "Guardianship is excessive",
            "Rights are unnecessarily restricted"
        ],
        resolution_strategy="Court reviews evidence, considers alternatives, and limits guardianship.",
        entity_scope="Persons with developmental disabilities",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of A.E., 552 S.W.3d 903"
    ),
    DoctrineBlock(
        topic="Guardianship for Persons with Traumatic Brain Injury",
        keywords=["traumatic brain injury", "guardianship", "Texas", "PRB06"],
        conclusion_template="Guardianship for persons with traumatic brain injury requires evidence of impaired capacity and risk of harm.",
        reasoning_framework=(
            "Texas Estates Code § 1002.017 and § 1101.101 require proof that traumatic brain injury impairs the individual's ability to manage affairs or care for themselves. "
            "Functional assessments and medical testimony are critical. "
            "The doctrine ensures guardianship is imposed only when necessary and tailored to actual needs."
        ),
        key_factors=[
            "Medical diagnosis",
            "Functional impairment",
            "Risk of harm",
            "Clear and convincing evidence"
        ],
        primary_authority=[
            "Texas Estates Code § 1002.017",
            "Texas Estates Code § 1101.101",
            "In re Guardianship of L.C., 2017 Tex. App. LEXIS 10452"
        ],
        burden_holder="Petitioner",
        adversary_position="Respondent contests incapacity",
        counter_arguments=[
            "Functional abilities retained",
            "Diagnosis is insufficient",
            "Risk is minimal"
        ],
        resolution_strategy="Court reviews evidence, applies statutory standard, and rules accordingly.",
        entity_scope="Persons with traumatic brain injury",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of L.C., 2017 Tex. App. LEXIS 10452"
    ),
    DoctrineBlock(
        topic="Guardianship for Persons with Autism Spectrum Disorder",
        keywords=["autism spectrum disorder", "guardianship", "Texas", "PRB06"],
        conclusion_template="Guardianship for persons with autism spectrum disorder must be tailored to functional abilities and consider supported decision-making alternatives.",
        reasoning_framework=(
            "Texas Estates Code § 1357.003 and § 1101.151 require courts to assess functional abilities and consider supported decision-making agreements before imposing guardianship. "
            "The doctrine emphasizes autonomy, inclusion, and periodic review of necessity. "
            "Courts must avoid unnecessary deprivation of rights and tailor orders to individual needs."
        ),
        key_factors=[
            "Functional assessment",
            "Supported decision-making",
            "Autonomy",
            "Periodic review"
        ],
        primary_authority=[
            "Texas Estates Code § 1357.003",
            "Texas Estates Code § 1101.151",
            "In re Guardianship of A.E., 552 S.W.3d 903"
        ],
        burden_holder="Petitioner",
        adversary_position="Respondent proposes alternatives",
        counter_arguments=[
            "Supported decision-making is sufficient",
            "Guardianship is excessive",
            "Rights are unnecessarily restricted"
        ],
        resolution_strategy="Court reviews evidence, considers alternatives, and limits guardianship.",
        entity_scope="Persons with autism spectrum disorder",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of A.E., 552 S.W.3d 903"
    ),
    DoctrineBlock(
        topic="Guardianship for Persons with Down Syndrome",
        keywords=["down syndrome", "guardianship", "Texas", "PRB06"],
        conclusion_template="Guardianship for persons with Down syndrome must be tailored to functional abilities and consider supported decision-making alternatives.",
        reasoning_framework=(
            "Texas Estates Code § 1357.003 and § 1101.151 require courts to assess functional abilities and consider supported decision-making agreements before imposing guardianship. "
            "The doctrine emphasizes autonomy, inclusion, and periodic review of necessity. "
            "Courts must avoid unnecessary deprivation of rights and tailor orders to individual needs."
        ),
        key_factors=[
            "Functional assessment",
            "Supported decision-making",
            "Autonomy",
            "Periodic review"
        ],
        primary_authority=[
            "Texas Estates Code § 1357.003",
            "Texas Estates Code § 1101.151",
            "In re Guardianship of A.E., 552 S.W.3d 903"
        ],
        burden_holder="Petitioner",
        adversary_position="Respondent proposes alternatives",
        counter_arguments=[
            "Supported decision-making is sufficient",
            "Guardianship is excessive",
            "Rights are unnecessarily restricted"
        ],
        resolution_strategy="Court reviews evidence, considers alternatives, and limits guardianship.",
        entity_scope="Persons with Down syndrome",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of A.E., 552 S.W.3d 903"
    ),
    DoctrineBlock(
        topic="Guardianship for Persons with Cerebral Palsy",
        keywords=["cerebral palsy", "guardianship", "Texas", "PRB06"],
        conclusion_template="Guardianship for persons with cerebral palsy requires proof of functional impairment and risk of harm, not diagnosis alone.",
        reasoning_framework=(
            "Texas Estates Code § 1002.017 and § 1101.101 require evidence that cerebral palsy impairs the individual's ability to manage affairs or care for themselves. "
            "Diagnosis alone is insufficient; functional impairment and risk of harm must be demonstrated. "
            "The doctrine protects autonomy and ensures guardianship is imposed only when necessary."
        ),
        key_factors=[
            "Functional impairment",
            "Medical evidence",
            "Risk of harm",
            "Clear and convincing proof"
        ],
        primary_authority=[
            "Texas Estates Code § 1002.017",
            "Texas Estates Code § 1101.101",
            "In re Guardianship of L.C., 2017 Tex. App. LEXIS 10452"
        ],
        burden_holder="Petitioner",
        adversary_position="Respondent contests incapacity",
        counter_arguments=[
            "Disability does not impair management",
            "Functional abilities retained",
            "Risk is minimal"
        ],
        resolution_strategy="Court reviews evidence, applies statutory standard, and rules accordingly.",
        entity_scope="Persons with cerebral palsy",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of L.C., 2017 Tex. App. LEXIS 10452"
    ),
    DoctrineBlock(
        topic="Guardianship for Persons with Prader-Willi Syndrome",
        keywords=["prader-willi syndrome", "guardianship", "Texas", "PRB06"],
        conclusion_template="Guardianship for persons with Prader-Willi syndrome must be tailored to functional abilities and consider supported decision-making alternatives.",
        reasoning_framework=(
            "Texas Estates Code § 1357.003 and § 1101.151 require courts to assess functional abilities and consider supported decision-making agreements before imposing guardianship. "
            "The doctrine emphasizes autonomy, inclusion, and periodic review of necessity. "
            "Courts must avoid unnecessary deprivation of rights and tailor orders to individual needs."
        ),
        key_factors=[
            "Functional assessment",
            "Supported decision-making",
            "Autonomy",
            "Periodic review"
        ],
        primary_authority=[
            "Texas Estates Code § 1357.003",
            "Texas Estates Code § 1101.151",
            "In re Guardianship of A.E., 552 S.W.3d 903"
        ],
        burden_holder="Petitioner",
        adversary_position="Respondent proposes alternatives",
        counter_arguments=[
            "Supported decision-making is sufficient",
            "Guardianship is excessive",
            "Rights are unnecessarily restricted"
        ],
        resolution_strategy="Court reviews evidence, considers alternatives, and limits guardianship.",
        entity_scope="Persons with Prader-Willi syndrome",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of A.E., 552 S.W.3d 903"
    ),
    DoctrineBlock(
        topic="Guardianship for Persons with Williams Syndrome",
        keywords=["williams syndrome", "guardianship", "Texas", "PRB06"],
        conclusion_template="Guardianship for persons with Williams syndrome must be tailored to functional abilities and consider supported decision-making alternatives.",
        reasoning_framework=(
            "Texas Estates Code § 1357.003 and § 1101.151 require courts to assess functional abilities and consider supported decision-making agreements before imposing guardianship. "
            "The doctrine emphasizes autonomy, inclusion, and periodic review of necessity. "
            "Courts must avoid unnecessary deprivation of rights and tailor orders to individual needs."
        ),
        key_factors=[
            "Functional assessment",
            "Supported decision-making",
            "Autonomy",
            "Periodic review"
        ],
        primary_authority=[
            "Texas Estates Code § 1357.003",
            "Texas Estates Code § 1101.151",
            "In re Guardianship of A.E., 552 S.W.3d 903"
        ],
        burden_holder="Petitioner",
        adversary_position="Respondent proposes alternatives",
        counter_arguments=[
            "Supported decision-making is sufficient",
            "Guardianship is excessive",
            "Rights are unnecessarily restricted"
        ],
        resolution_strategy="Court reviews evidence, considers alternatives, and limits guardianship.",
        entity_scope="Persons with Williams syndrome",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of A.E., 552 S.W.3d 903"
    ),
    DoctrineBlock(
        topic="Guardianship for Persons with Fragile X Syndrome",
        keywords=["fragile x syndrome", "guardianship", "Texas", "PRB06"],
        conclusion_template="Guardianship for persons with Fragile X syndrome must be tailored to functional abilities and consider supported decision-making alternatives.",
        reasoning_framework=(
            "Texas Estates Code § 1357.003 and § 1101.151 require courts to assess functional abilities and consider supported decision-making agreements before imposing guardianship. "
            "The doctrine emphasizes autonomy, inclusion, and periodic review of necessity. "
            "Courts must avoid unnecessary deprivation of rights and tailor orders to individual needs."
        ),
        key_factors=[
            "Functional assessment",
            "Supported decision-making",
            "Autonomy",
            "Periodic review"
        ],
        primary_authority=[
            "Texas Estates Code § 1357.003",
            "Texas Estates Code § 1101.151",
            "In re Guardianship of A.E., 552 S.W.3d 903"
        ],
        burden_holder="Petitioner",
        adversary_position="Respondent proposes alternatives",
        counter_arguments=[
            "Supported decision-making is sufficient",
            "Guardianship is excessive",
            "Rights are unnecessarily restricted"
        ],
        resolution_strategy="Court reviews evidence, considers alternatives, and limits guardianship.",
        entity_scope="Persons with Fragile X syndrome",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of A.E., 552 S.W.3d 903"
    ),
    DoctrineBlock(
        topic="Guardianship for Persons with Huntington's Disease",
        keywords=["huntington's disease", "guardianship", "Texas", "PRB06"],
        conclusion_template="Guardianship for persons with Huntington's disease requires evidence of impaired capacity and risk of harm.",
        reasoning_framework=(
            "Texas Estates Code § 1002.017 and § 1101.101 require proof that Huntington's disease impairs the individual's ability to manage affairs or care for themselves. "
            "Functional assessments and medical testimony are critical. "
            "The doctrine ensures guardianship is imposed only when necessary and tailored to actual needs."
        ),
        key_factors=[
            "Medical diagnosis",
            "Functional impairment",
            "Risk of harm",
            "Clear and convincing evidence"
        ],
        primary_authority=[
            "Texas Estates Code § 1002.017",
            "Texas Estates Code § 1101.101",
            "In re Guardianship of L.C., 2017 Tex. App. LEXIS 10452"
        ],
        burden_holder="Petitioner",
        adversary_position="Respondent contests incapacity",
        counter_arguments=[
            "Functional abilities retained",
            "Diagnosis is insufficient",
            "Risk is minimal"
        ],
        resolution_strategy="Court reviews evidence, applies statutory standard, and rules accordingly.",
        entity_scope="Persons with Huntington's disease",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of L.C., 2017 Tex. App. LEXIS 10452"
    ),
    DoctrineBlock(
        topic="Guardianship for Persons with Multiple Sclerosis",
        keywords=["multiple sclerosis", "guardianship", "Texas", "PRB06"],
        conclusion_template="Guardianship for persons with multiple sclerosis requires proof of functional impairment and risk of harm, not diagnosis alone.",
        reasoning_framework=(
            "Texas Estates Code § 1002.017 and § 1101.101 require evidence that multiple sclerosis impairs the individual's ability to manage affairs or care for themselves. "
            "Diagnosis alone is insufficient; functional impairment and risk of harm must be demonstrated. "
            "The doctrine protects autonomy and ensures guardianship is imposed only when necessary."
        ),
        key_factors=[
            "Functional impairment",
            "Medical evidence",
            "Risk of harm",
            "Clear and convincing proof"
        ],
        primary_authority=[
            "Texas Estates Code § 1002.017",
            "Texas Estates Code § 1101.101",
            "In re Guardianship of L.C., 2017 Tex. App. LEXIS 10452"
        ],
        burden_holder="Petitioner",
        adversary_position="Respondent contests incapacity",
        counter_arguments=[
            "Disability does not impair management",
            "Functional abilities retained",
            "Risk is minimal"
        ],
        resolution_strategy="Court reviews evidence, applies statutory standard, and rules accordingly.",
        entity_scope="Persons with multiple sclerosis",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of L.C., 2017 Tex. App. LEXIS 10452"
    ),
    DoctrineBlock(
        topic="Guardianship for Persons with ALS (Amyotrophic Lateral Sclerosis)",
        keywords=["ALS", "amyotrophic lateral sclerosis", "guardianship", "Texas", "PRB06"],
        conclusion_template="Guardianship for persons with ALS requires proof of functional impairment and risk of harm, not diagnosis alone.",
        reasoning_framework=(
            "Texas Estates Code § 1002.017 and § 1101.101 require evidence that ALS impairs the individual's ability to manage affairs or care for themselves. "
            "Diagnosis alone is insufficient; functional impairment and risk of harm must be demonstrated. "
            "The doctrine protects autonomy and ensures guardianship is imposed only when necessary."
        ),
        key_factors=[
            "Functional impairment",
            "Medical evidence",
            "Risk of harm",
            "Clear and convincing proof"
        ],
        primary_authority=[
            "Texas Estates Code § 1002.017",
            "Texas Estates Code § 1101.101",
            "In re Guardianship of L.C., 2017 Tex. App. LEXIS 10452"
        ],
        burden_holder="Petitioner",
        adversary_position="Respondent contests incapacity",
        counter_arguments=[
            "Disability does not impair management",
            "Functional abilities retained",
            "Risk is minimal"
        ],
        resolution_strategy="Court reviews evidence, applies statutory standard, and rules accordingly.",
        entity_scope="Persons with ALS",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="In re Guardianship of L.C., 2017 Tex. App. LEXIS 10452"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(query: str) -> List[DoctrineBlock]:
    results = []
    query_lower = query.lower()
    for doctrine in DOCTRINE_CACHE:
        if query_lower in doctrine.topic.lower():
            results.append(doctrine)
            continue
        for keyword in doctrine.keywords:
            if query_lower in keyword.lower():
                results.append(doctrine)
                break
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]