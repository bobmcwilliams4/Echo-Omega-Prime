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
        topic="Automatic Stay - 11 USC Section 362",
        keywords=["automatic stay", "section 362", "bankruptcy", "protection", "debtor", "creditor", "injunction"],
        conclusion_template="The automatic stay under 11 USC §362 prohibits most creditor actions against the debtor or the estate upon filing.",
        reasoning_framework=(
            "The automatic stay is triggered immediately upon the filing of a bankruptcy petition. It operates as a broad injunction against "
            "the commencement or continuation of judicial, administrative, or other proceedings against the debtor, enforcement of judgments, "
            "collection actions, and attempts to obtain possession or control of estate property. Exceptions exist for criminal proceedings, "
            "domestic support obligations, and certain regulatory actions. Relief from stay may be granted for cause, including lack of adequate "
            "protection or if the property is not necessary for reorganization. The scope and duration of the stay depend on the chapter filed, "
            "prior filings, and the nature of the action. Violations of the stay may result in damages, including punitive damages if willful. "
            "Courts analyze the stay's applicability by examining the nature of the action, the parties involved, and statutory exceptions. "
            "The burden is on the party seeking relief to demonstrate cause. The stay protects the debtor's assets and facilitates orderly "
            "restructuring. Creditors may challenge the stay's applicability or seek relief, but must comply pending court determination."
        ),
        key_factors=[
            "Timing of bankruptcy petition",
            "Nature of creditor action",
            "Statutory exceptions",
            "Adequate protection",
            "Necessity for reorganization",
            "Prior bankruptcy filings"
        ],
        primary_authority=["11 USC §362", "In re Calder, 907 F.2d 953 (10th Cir. 1990)", "In re Chugach Forest Products, Inc., 23 F.3d 241 (9th Cir. 1994)"],
        burden_holder="Party seeking relief from stay",
        adversary_position="Creditor seeking to continue action or enforce judgment",
        counter_arguments=[
            "Action falls within statutory exception",
            "Debtor lacks equity in property",
            "Property not necessary for reorganization",
            "Stay not applicable to non-debtor parties"
        ],
        resolution_strategy="Motion for relief from stay, evidentiary hearing, court order",
        entity_scope="Debtor, creditors, estate property",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Calder, 907 F.2d 953 (10th Cir. 1990)"
    ),
    DoctrineBlock(
        topic="Priority Claims - 11 USC Section 507",
        keywords=["priority claims", "section 507", "administrative expenses", "taxes", "wages", "bankruptcy priorities"],
        conclusion_template="Priority claims under 11 USC §507 are paid ahead of general unsecured claims in bankruptcy distributions.",
        reasoning_framework=(
            "Section 507 establishes a hierarchy of claims entitled to priority in bankruptcy distributions. Administrative expenses, "
            "domestic support obligations, certain wage claims, and specific tax obligations are among the highest priorities. The court "
            "must determine the nature and timing of the claim, whether it qualifies under the enumerated categories, and whether it was "
            "incurred during the bankruptcy or prepetition. Priority claims are paid from estate assets before general unsecured claims, "
            "but after secured claims. Disputes often arise regarding classification, timing, and eligibility. The burden is on the claimant "
            "to establish priority status. Courts rely on statutory interpretation and precedent to resolve ambiguities. Misclassification "
            "may result in subordination or denial of priority. The doctrine ensures essential creditors and obligations are satisfied to "
            "facilitate reorganization and protect vulnerable parties."
        ),
        key_factors=[
            "Nature of claim",
            "Timing of claim",
            "Statutory category",
            "Eligibility criteria",
            "Impact on estate assets"
        ],
        primary_authority=["11 USC §507", "Howard Delivery Service, Inc. v. Zurich American Ins. Co., 547 U.S. 651 (2006)"],
        burden_holder="Claimant seeking priority",
        adversary_position="Other creditors challenging priority status",
        counter_arguments=[
            "Claim does not fit statutory category",
            "Claim incurred outside relevant period",
            "Misclassification of claim"
        ],
        resolution_strategy="Claim objection, evidentiary hearing, judicial determination",
        entity_scope="Creditors, debtor, estate",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Howard Delivery Service, Inc. v. Zurich American Ins. Co., 547 U.S. 651 (2006)"
    ),
    DoctrineBlock(
        topic="Chapter 11 Plan Confirmation - 11 USC Section 1129",
        keywords=["plan confirmation", "section 1129", "chapter 11", "reorganization", "feasibility", "best interests", "cramdown"],
        conclusion_template="A Chapter 11 plan is confirmed if it satisfies the requirements of 11 USC §1129, including feasibility and creditor protections.",
        reasoning_framework=(
            "Plan confirmation under §1129 requires satisfaction of multiple statutory criteria: the plan must be proposed in good faith, "
            "provide for payment of priority claims, be feasible, and meet the 'best interests of creditors' test. If all impaired classes "
            "accept the plan, confirmation is straightforward. If not, the court may confirm via 'cramdown' if the plan does not discriminate "
            "unfairly and is fair and equitable to dissenting classes. Feasibility requires a showing that the debtor can implement the plan "
            "without likely liquidation or further financial distress. The best interests test requires that creditors receive at least as much "
            "as they would in liquidation. Courts scrutinize projections, management competence, and creditor objections. The burden is on the "
            "plan proponent, but objecting creditors may challenge feasibility, fairness, or compliance. Precedent guides interpretation of "
            "good faith, feasibility, and fairness. Confirmation is essential for restructuring and discharge."
        ),
        key_factors=[
            "Good faith proposal",
            "Feasibility",
            "Best interests of creditors",
            "Fair and equitable treatment",
            "Acceptance by impaired classes",
            "Compliance with statutory requirements"
        ],
        primary_authority=["11 USC §1129", "Bank of America Nat. Trust v. 203 North LaSalle Street Partnership, 526 U.S. 434 (1999)"],
        burden_holder="Plan proponent",
        adversary_position="Creditor objecting to plan confirmation",
        counter_arguments=[
            "Plan is not feasible",
            "Plan discriminates unfairly",
            "Plan not proposed in good faith",
            "Plan fails best interests test"
        ],
        resolution_strategy="Confirmation hearing, evidentiary submissions, judicial determination",
        entity_scope="Debtor, creditors, equity holders",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Bank of America Nat. Trust v. 203 North LaSalle Street Partnership, 526 U.S. 434 (1999)"
    ),
    DoctrineBlock(
        topic="Fraudulent Transfers - 11 USC Section 548",
        keywords=["fraudulent transfer", "section 548", "avoidance", "actual fraud", "constructive fraud", "insolvency"],
        conclusion_template="Transfers made with actual intent to hinder, delay, or defraud creditors, or for less than reasonably equivalent value while insolvent, are avoidable under 11 USC §548.",
        reasoning_framework=(
            "Section 548 authorizes avoidance of transfers made within two years of bankruptcy filing if made with actual fraudulent intent "
            "or for less than reasonably equivalent value while the debtor was insolvent, intended to incur debts beyond ability to pay, or "
            "was engaged in business with unreasonably small capital. Courts analyze badges of fraud, value exchanged, timing, and debtor's "
            "financial condition. Actual intent is inferred from circumstantial evidence. Constructive fraud focuses on value and insolvency. "
            "The burden is on the trustee or debtor-in-possession to establish avoidability. Defenses include good faith, ordinary course of "
            "business, and subsequent transferee protections. Avoidance remedies include recovery of property or value for the estate. The "
            "doctrine protects creditors and preserves estate assets."
        ),
        key_factors=[
            "Timing of transfer",
            "Intent to hinder, delay, or defraud",
            "Reasonably equivalent value",
            "Debtor's insolvency",
            "Badges of fraud",
            "Defenses available"
        ],
        primary_authority=["11 USC §548", "In re Acequia, Inc., 34 F.3d 800 (9th Cir. 1994)"],
        burden_holder="Trustee or debtor-in-possession",
        adversary_position="Transferee defending against avoidance",
        counter_arguments=[
            "Transfer was for reasonably equivalent value",
            "Debtor was solvent",
            "Transfer in ordinary course of business",
            "Good faith defense"
        ],
        resolution_strategy="Adversary proceeding, evidentiary hearing, court order",
        entity_scope="Debtor, transferee, estate",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Acequia, Inc., 34 F.3d 800 (9th Cir. 1994)"
    ),
    DoctrineBlock(
        topic="Preference Actions - 11 USC Section 547",
        keywords=["preference", "section 547", "avoidance", "insider", "90 days", "ordinary course", "new value"],
        conclusion_template="Payments or transfers to creditors within 90 days (or one year for insiders) before bankruptcy may be avoided as preferences under 11 USC §547.",
        reasoning_framework=(
            "Preference actions under §547 allow the trustee to avoid transfers made to creditors within 90 days of bankruptcy (one year for "
            "insiders) that enable the creditor to receive more than they would in liquidation. The elements include antecedent debt, insolvency, "
            "timing, and effect on creditor's recovery. Defenses include ordinary course of business, contemporaneous exchange for new value, and "
            "subsequent new value. The burden is on the trustee to prove avoidability, while the creditor must establish defenses. Courts examine "
            "the nature of the debt, timing, relationship, and business practices. The doctrine prevents unequal treatment and discourages "
            "creditor 'race to the courthouse.'"
        ),
        key_factors=[
            "Timing of transfer",
            "Antecedent debt",
            "Debtor's insolvency",
            "Insider status",
            "Ordinary course defense",
            "New value defense"
        ],
        primary_authority=["11 USC §547", "Barnhill v. Johnson, 503 U.S. 393 (1992)"],
        burden_holder="Trustee",
        adversary_position="Creditor defending transfer",
        counter_arguments=[
            "Transfer in ordinary course of business",
            "Contemporaneous exchange for new value",
            "Subsequent new value defense",
            "Transfer outside preference period"
        ],
        resolution_strategy="Adversary proceeding, evidentiary hearing, court order",
        entity_scope="Debtor, creditor, estate",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Barnhill v. Johnson, 503 U.S. 393 (1992)"
    ),
    DoctrineBlock(
        topic="DIP Financing - 11 USC Section 364",
        keywords=["DIP financing", "debtor-in-possession", "section 364", "superpriority", "secured credit", "bankruptcy financing"],
        conclusion_template="Debtors may obtain postpetition financing under 11 USC §364, subject to court approval and possible superpriority status.",
        reasoning_framework=(
            "Section 364 authorizes debtors to obtain postpetition financing to fund operations and restructuring. The court may approve unsecured "
            "credit, secured credit, or superpriority financing if the debtor cannot obtain credit otherwise. The process requires notice, hearing, "
            "and demonstration of necessity. Existing creditors may object, especially if their collateral is primed or diluted. The court weighs "
            "the debtor's need, terms of financing, impact on estate, and creditor protections. Superpriority status may be granted if necessary "
            "and justified. The burden is on the debtor to show inability to obtain credit on less onerous terms. The doctrine facilitates "
            "reorganization and preserves value, but must balance creditor interests."
        ),
        key_factors=[
            "Necessity for financing",
            "Terms of proposed credit",
            "Impact on existing creditors",
            "Superpriority status",
            "Adequate protection",
            "Notice and hearing"
        ],
        primary_authority=["11 USC §364", "In re FCX, Inc., 54 B.R. 49 (Bankr. E.D.N.C. 1985)"],
        burden_holder="Debtor-in-possession",
        adversary_position="Existing creditors objecting to financing",
        counter_arguments=[
            "Financing not necessary",
            "Terms unfairly prejudice creditors",
            "Adequate protection lacking",
            "Alternative financing available"
        ],
        resolution_strategy="Motion for approval, evidentiary hearing, court order",
        entity_scope="Debtor, creditors, lenders",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re FCX, Inc., 54 B.R. 49 (Bankr. E.D.N.C. 1985)"
    ),
    DoctrineBlock(
        topic="Executory Contracts - 11 USC Section 365",
        keywords=["executory contract", "section 365", "assumption", "rejection", "cure", "lease", "bankruptcy"],
        conclusion_template="Debtors may assume or reject executory contracts and unexpired leases under 11 USC §365, subject to court approval and cure obligations.",
        reasoning_framework=(
            "Section 365 allows debtors to assume or reject executory contracts and unexpired leases. Assumption requires curing defaults, providing "
            "adequate assurance of future performance, and court approval. Rejection is treated as a breach, giving rise to a claim for damages. The "
            "debtor must decide within statutory deadlines, especially for real property leases. The court evaluates business judgment, impact on estate, "
            "and creditor interests. Non-debtor parties may object, especially regarding cure and assurance. The doctrine enables restructuring by "
            "allowing debtors to shed burdensome contracts or preserve valuable ones. The burden is on the debtor to justify assumption or rejection."
        ),
        key_factors=[
            "Nature of contract",
            "Business judgment",
            "Cure of defaults",
            "Adequate assurance",
            "Timing of decision",
            "Impact on estate"
        ],
        primary_authority=["11 USC §365", "In re Bildisco, 465 U.S. 513 (1984)"],
        burden_holder="Debtor",
        adversary_position="Non-debtor party to contract",
        counter_arguments=[
            "Failure to cure defaults",
            "Inadequate assurance of performance",
            "Assumption not in best interests",
            "Improper rejection"
        ],
        resolution_strategy="Motion to assume/reject, evidentiary hearing, court order",
        entity_scope="Debtor, contract counterparties, estate",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Bildisco, 465 U.S. 513 (1984)"
    ),
    DoctrineBlock(
        topic="Discharge - 11 USC Sections 727, 523, 1141, 1328",
        keywords=["discharge", "section 727", "section 523", "section 1141", "section 1328", "exceptions", "bankruptcy"],
        conclusion_template="Bankruptcy discharge releases the debtor from most prepetition debts, subject to exceptions under 11 USC §§727, 523, 1141, and 1328.",
        reasoning_framework=(
            "Discharge is the release of the debtor from liability for most prepetition debts. Section 727 governs discharge in Chapter 7, with exceptions "
            "for fraud, misconduct, and certain debts. Section 523 enumerates non-dischargeable debts, including taxes, domestic support, student loans, "
            "and debts arising from fraud or willful injury. Section 1141 provides discharge in Chapter 11, subject to plan confirmation and exceptions. "
            "Section 1328 governs Chapter 13 discharge, with broader coverage but some exceptions. The court examines debtor conduct, nature of debt, and "
            "statutory exclusions. Creditors may object to discharge or specific debts. The burden is on the objecting party to prove exceptions. The doctrine "
            "balances debtor relief and creditor protection."
        ),
        key_factors=[
            "Debtor conduct",
            "Nature of debt",
            "Statutory exceptions",
            "Plan confirmation",
            "Creditor objections"
        ],
        primary_authority=[
            "11 USC §727",
            "11 USC §523",
            "11 USC §1141",
            "11 USC §1328",
            "Grogan v. Garner, 498 U.S. 279 (1991)"
        ],
        burden_holder="Creditor objecting to discharge",
        adversary_position="Debtor seeking discharge",
        counter_arguments=[
            "Debt is non-dischargeable",
            "Debtor engaged in fraud or misconduct",
            "Debt arises from willful injury"
        ],
        resolution_strategy="Adversary proceeding, evidentiary hearing, court order",
        entity_scope="Debtor, creditors, estate",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Grogan v. Garner, 498 U.S. 279 (1991)"
    ),
    DoctrineBlock(
        topic="Secured Claims - 11 USC Section 506",
        keywords=["secured claim", "section 506", "collateral", "valuation", "bifurcation", "bankruptcy"],
        conclusion_template="Secured claims are valued under 11 USC §506, with bifurcation into secured and unsecured portions based on collateral value.",
        reasoning_framework=(
            "Section 506 governs the valuation of secured claims in bankruptcy. Claims are secured to the extent of the value of collateral, and "
            "unsecured for any deficiency. The court determines collateral value, often through appraisals and expert testimony. Bifurcation affects "
            "treatment under the plan and creditor rights. Debtors may seek to 'strip down' liens if collateral value is less than debt. Creditors may "
            "challenge valuation or assert additional collateral. The burden is on the party seeking valuation. The doctrine ensures fair treatment and "
            "aligns recovery with asset values."
        ),
        key_factors=[
            "Collateral value",
            "Claim amount",
            "Valuation method",
            "Bifurcation",
            "Impact on plan",
            "Creditor rights"
        ],
        primary_authority=["11 USC §506", "Associates Commercial Corp. v. Rash, 520 U.S. 953 (1997)"],
        burden_holder="Party seeking valuation",
        adversary_position="Creditor disputing valuation",
        counter_arguments=[
            "Collateral undervalued",
            "Improper bifurcation",
            "Additional collateral exists"
        ],
        resolution_strategy="Valuation hearing, expert testimony, court order",
        entity_scope="Debtor, secured creditors, estate",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Associates Commercial Corp. v. Rash, 520 U.S. 953 (1997)"
    ),
    DoctrineBlock(
        topic="Cramdown and Absolute Priority Rule",
        keywords=["cramdown", "absolute priority", "section 1129", "plan confirmation", "fair and equitable", "junior interests"],
        conclusion_template="A plan may be confirmed over dissenting class objections via cramdown if it complies with the absolute priority rule and is fair and equitable.",
        reasoning_framework=(
            "Cramdown allows confirmation of a plan over the objection of impaired classes if the plan does not discriminate unfairly and is fair and equitable. "
            "The absolute priority rule requires that junior classes (e.g., equity holders) cannot retain interests unless senior classes are paid in full. Exceptions "
            "exist for new value contributions. Courts analyze plan structure, distributions, and compliance with statutory requirements. The burden is on the plan "
            "proponent to demonstrate fairness and adherence to the absolute priority rule. Objecting creditors may challenge new value, retention of interests, or "
            "plan discrimination. Precedent guides interpretation and application."
        ),
        key_factors=[
            "Impaired class objection",
            "Plan fairness",
            "Absolute priority compliance",
            "New value exception",
            "Distribution structure",
            "Creditor rights"
        ],
        primary_authority=["11 USC §1129(b)", "Bank of America Nat. Trust v. 203 North LaSalle Street Partnership, 526 U.S. 434 (1999)"],
        burden_holder="Plan proponent",
        adversary_position="Dissenting creditor class",
        counter_arguments=[
            "Plan violates absolute priority rule",
            "New value is insufficient",
            "Plan discriminates unfairly"
        ],
        resolution_strategy="Confirmation hearing, judicial determination, evidentiary submissions",
        entity_scope="Debtor, creditors, equity holders",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Bank of America Nat. Trust v. 203 North LaSalle Street Partnership, 526 U.S. 434 (1999)"
    ),
    DoctrineBlock(
        topic="Small Business Debtor - Subchapter V",
        keywords=["small business", "subchapter V", "chapter 11", "plan confirmation", "debtor eligibility", "simplified process"],
        conclusion_template="Subchapter V provides streamlined Chapter 11 procedures for eligible small business debtors, with relaxed requirements and expedited timelines.",
        reasoning_framework=(
            "Subchapter V was enacted to facilitate reorganization for small business debtors. Eligibility is based on debt limits and business activity. The process "
            "features simplified plan confirmation, no creditors' committee unless ordered, and expedited deadlines. The debtor retains control and may confirm a plan "
            "without impaired class acceptance. The court appoints a trustee to oversee but not operate the business. The doctrine aims to reduce costs, speed resolution, "
            "and preserve value for small businesses. Creditors may object to eligibility or plan terms. The burden is on the debtor to demonstrate eligibility and plan "
            "feasibility. Courts rely on statutory criteria and business judgment."
        ),
        key_factors=[
            "Debtor eligibility",
            "Debt limits",
            "Business activity",
            "Plan feasibility",
            "Creditor objections",
            "Expedited timelines"
        ],
        primary_authority=["11 USC §§1181-1195", "In re Ventura, 615 B.R. 1 (Bankr. E.D.N.Y. 2020)"],
        burden_holder="Debtor",
        adversary_position="Creditor objecting to eligibility or plan",
        counter_arguments=[
            "Debtor exceeds debt limits",
            "Business not eligible",
            "Plan not feasible"
        ],
        resolution_strategy="Eligibility hearing, plan confirmation hearing, court order",
        entity_scope="Small business debtor, creditors, trustee",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Ventura, 615 B.R. 1 (Bankr. E.D.N.Y. 2020)"
    ),
    DoctrineBlock(
        topic="Adequate Protection",
        keywords=["adequate protection", "secured creditor", "section 361", "relief from stay", "value preservation"],
        conclusion_template="Secured creditors are entitled to adequate protection to prevent diminution of collateral value during bankruptcy.",
        reasoning_framework=(
            "Adequate protection is a statutory requirement to safeguard secured creditors against loss of collateral value during bankruptcy. It may be provided "
            "through periodic cash payments, replacement liens, or other relief. The court evaluates the risk of diminution, debtor's operations, and proposed "
            "protections. Creditors may seek relief from stay if protection is inadequate. The burden is on the debtor to propose and justify protection. The doctrine "
            "ensures fairness and preserves creditor rights while facilitating reorganization."
        ),
        key_factors=[
            "Collateral value",
            "Risk of diminution",
            "Protection measures",
            "Debtor operations",
            "Creditor objections"
        ],
        primary_authority=["11 USC §361", "In re Timbers of Inwood Forest, 484 U.S. 365 (1988)"],
        burden_holder="Debtor",
        adversary_position="Secured creditor",
        counter_arguments=[
            "Protection is inadequate",
            "Collateral value is at risk",
            "Relief from stay warranted"
        ],
        resolution_strategy="Motion for adequate protection, evidentiary hearing, court order",
        entity_scope="Debtor, secured creditors, estate",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Timbers of Inwood Forest, 484 U.S. 365 (1988)"
    ),
    DoctrineBlock(
        topic="Claims Objection and Allowance",
        keywords=["claims objection", "claims allowance", "section 502", "proof of claim", "disputed claim"],
        conclusion_template="Claims are allowed unless objected to and disallowed under 11 USC §502; objections must be substantiated and timely.",
        reasoning_framework=(
            "Section 502 governs the allowance and disallowance of claims. Creditors file proofs of claim, which are presumed valid unless objected to. The debtor, trustee, "
            "or other parties may object, citing lack of documentation, improper classification, or legal defects. The court conducts a hearing and determines validity. The "
            "burden shifts: objector must produce evidence, then claimant must prove claim. Disallowed claims are excluded from distributions. The doctrine ensures accuracy "
            "and fairness in estate distributions."
        ),
        key_factors=[
            "Proof of claim",
            "Objection grounds",
            "Documentation",
            "Classification",
            "Timeliness"
        ],
        primary_authority=["11 USC §502", "Fed. R. Bankr. P. 3007", "In re Fidelity Holding Co., Ltd., 837 F.2d 696 (5th Cir. 1988)"],
        burden_holder="Objecting party",
        adversary_position="Claimant",
        counter_arguments=[
            "Claim is valid and documented",
            "Objection is untimely",
            "Improper classification"
        ],
        resolution_strategy="Objection hearing, evidentiary submissions, court order",
        entity_scope="Debtor, creditors, trustee",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Fidelity Holding Co., Ltd., 837 F.2d 696 (5th Cir. 1988)"
    ),
    DoctrineBlock(
        topic="Rejection Damages",
        keywords=["rejection damages", "executory contract", "section 365", "claim calculation", "lease rejection"],
        conclusion_template="Rejection of executory contracts or leases results in a claim for damages, subject to statutory caps and calculation rules.",
        reasoning_framework=(
            "When a debtor rejects an executory contract or lease, the non-debtor party is entitled to a claim for damages. Section 365 governs the process, and Section 502(b)(6) "
            "caps damages for lease rejection. The court calculates damages based on contract terms, mitigation, and statutory limits. The burden is on the claimant to prove damages. "
            "The doctrine balances debtor relief and creditor compensation, ensuring claims are reasonable and not punitive."
        ),
        key_factors=[
            "Contract terms",
            "Mitigation",
            "Statutory caps",
            "Timing of rejection",
            "Claim calculation"
        ],
        primary_authority=["11 USC §365", "11 USC §502(b)(6)", "In re Klein, 940 F.2d 1079 (9th Cir. 1991)"],
        burden_holder="Non-debtor party",
        adversary_position="Debtor",
        counter_arguments=[
            "Damages exceed statutory cap",
            "Claim is speculative",
            "Mitigation not considered"
        ],
        resolution_strategy="Claim objection, evidentiary hearing, court order",
        entity_scope="Debtor, contract counterparties, estate",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Klein, 940 F.2d 1079 (9th Cir. 1991)"
    ),
    DoctrineBlock(
        topic="Assumption of Collective Bargaining Agreements",
        keywords=["collective bargaining", "section 1113", "assumption", "rejection", "labor union", "bankruptcy"],
        conclusion_template="Debtors must comply with 11 USC §1113 procedures to assume or reject collective bargaining agreements, including negotiation and court approval.",
        reasoning_framework=(
            "Section 1113 provides special procedures for assumption or rejection of collective bargaining agreements. The debtor must propose modifications, negotiate in good faith, "
            "and seek court approval. The court evaluates necessity, fairness, and impact on employees. Labor unions may object or negotiate terms. The burden is on the debtor to justify "
            "rejection or assumption. The doctrine protects employee rights while allowing necessary restructuring."
        ),
        key_factors=[
            "Negotiation",
            "Good faith",
            "Necessity",
            "Fairness",
            "Court approval"
        ],
        primary_authority=["11 USC §1113", "In re Wheeling-Pittsburgh Steel Corp., 791 F.2d 1074 (3d Cir. 1986)"],
        burden_holder="Debtor",
        adversary_position="Labor union",
        counter_arguments=[
            "Modification not necessary",
            "Negotiation lacked good faith",
            "Impact on employees is excessive"
        ],
        resolution_strategy="Motion under §1113, evidentiary hearing, court order",
        entity_scope="Debtor, employees, labor unions",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Wheeling-Pittsburgh Steel Corp., 791 F.2d 1074 (3d Cir. 1986)"
    ),
    DoctrineBlock(
        topic="Executory Contract Cure Requirements",
        keywords=["executory contract", "cure", "section 365", "assumption", "default", "adequate assurance"],
        conclusion_template="Assumption of executory contracts requires cure of defaults and adequate assurance of future performance under 11 USC §365.",
        reasoning_framework=(
            "To assume an executory contract, the debtor must cure all monetary and non-monetary defaults and provide adequate assurance of future performance. The court reviews the "
            "proposed cure, assurance, and objections from counterparties. The burden is on the debtor to demonstrate compliance. The doctrine ensures counterparties are protected from "
            "past breaches and future risk."
        ),
        key_factors=[
            "Default status",
            "Cure amount",
            "Adequate assurance",
            "Counterparty objections",
            "Court approval"
        ],
        primary_authority=["11 USC §365(b)", "In re U.S. Wireless Corp., 384 B.R. 713 (Bankr. D. Del. 2008)"],
        burden_holder="Debtor",
        adversary_position="Contract counterparty",
        counter_arguments=[
            "Cure is insufficient",
            "Assurance is inadequate",
            "Default is non-curable"
        ],
        resolution_strategy="Motion to assume, evidentiary hearing, court order",
        entity_scope="Debtor, contract counterparties, estate",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re U.S. Wireless Corp., 384 B.R. 713 (Bankr. D. Del. 2008)"
    ),
    DoctrineBlock(
        topic="Critical Vendor Payments",
        keywords=["critical vendor", "section 363", "payment", "postpetition", "bankruptcy", "business operations"],
        conclusion_template="Courts may authorize critical vendor payments to preserve business operations, subject to necessity and fairness under 11 USC §363.",
        reasoning_framework=(
            "Critical vendor payments are authorized to preserve essential business operations. The debtor must demonstrate necessity, potential harm from non-payment, and fairness. "
            "Courts weigh impact on estate, creditor equality, and business continuity. Creditors may object to preferential treatment. The burden is on the debtor to justify payments. "
            "The doctrine is controversial but recognized in practice."
        ),
        key_factors=[
            "Necessity",
            "Business operations",
            "Impact on estate",
            "Creditor equality",
            "Court approval"
        ],
        primary_authority=["11 USC §363", "In re Kmart Corp., 359 F.3d 866 (7th Cir. 2004)"],
        burden_holder="Debtor",
        adversary_position="Non-critical creditors",
        counter_arguments=[
            "Payments are unnecessary",
            "Preferential treatment",
            "Impact on estate is negative"
        ],
        resolution_strategy="Motion for approval, evidentiary hearing, court order",
        entity_scope="Debtor, vendors, creditors",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Kmart Corp., 359 F.3d 866 (7th Cir. 2004)"
    ),
    DoctrineBlock(
        topic="Section 363 Sales",
        keywords=["section 363", "asset sale", "bankruptcy", "court approval", "free and clear", "auction"],
        conclusion_template="Debtors may sell estate assets under 11 USC §363, subject to court approval, notice, and sale free and clear of liens.",
        reasoning_framework=(
            "Section 363 authorizes sale of estate assets, often free and clear of liens. The process requires notice, hearing, and court approval. Creditors and stakeholders may object, "
            "especially regarding price, process, or impact on claims. The court evaluates business judgment, fairness, and compliance with statutory requirements. Sales may be conducted "
            "by auction or private negotiation. The doctrine facilitates value maximization and efficient restructuring."
        ),
        key_factors=[
            "Business judgment",
            "Sale terms",
            "Notice and hearing",
            "Free and clear requirements",
            "Creditor objections"
        ],
        primary_authority=["11 USC §363", "In re Chrysler LLC, 576 F.3d 108 (2d Cir. 2009)"],
        burden_holder="Debtor",
        adversary_position="Creditors or stakeholders",
        counter_arguments=[
            "Sale price is inadequate",
            "Process is unfair",
            "Sale not free and clear"
        ],
        resolution_strategy="Motion for approval, auction, court order",
        entity_scope="Debtor, buyers, creditors, estate",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Chrysler LLC, 576 F.3d 108 (2d Cir. 2009)"
    ),
    DoctrineBlock(
        topic="Section 1111(b) Election",
        keywords=["section 1111(b)", "secured claim", "plan confirmation", "election", "bankruptcy"],
        conclusion_template="Secured creditors may elect under 11 USC §1111(b) to treat their claim as fully secured, affecting plan treatment and recovery.",
        reasoning_framework=(
            "Section 1111(b) allows secured creditors to elect to have their entire claim treated as secured, even if collateral value is less than debt. The election affects plan treatment, "
            "distribution, and deficiency claims. The court reviews eligibility, timing, and impact. The burden is on the creditor to make a timely election. The doctrine protects secured "
            "creditors from undervaluation and ensures fair recovery."
        ),
        key_factors=[
            "Eligibility",
            "Timing",
            "Collateral value",
            "Plan treatment",
            "Creditor election"
        ],
        primary_authority=["11 USC §1111(b)", "In re L&J Anaheim Associates, 995 F.2d 940 (9th Cir. 1993)"],
        burden_holder="Secured creditor",
        adversary_position="Debtor",
        counter_arguments=[
            "Election is untimely",
            "Creditor is not eligible",
            "Plan treatment is unfair"
        ],
        resolution_strategy="Confirmation hearing, judicial determination",
        entity_scope="Debtor, secured creditors, estate",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re L&J Anaheim Associates, 995 F.2d 940 (9th Cir. 1993)"
    ),
    DoctrineBlock(
        topic="Section 1126 Voting",
        keywords=["section 1126", "plan voting", "acceptance", "impaired class", "chapter 11"],
        conclusion_template="Plan acceptance under 11 USC §1126 requires approval by a majority in number and two-thirds in amount of claims in each impaired class.",
        reasoning_framework=(
            "Section 1126 governs plan voting and acceptance. Impaired classes vote to accept or reject the plan. Acceptance requires a majority in number and two-thirds in amount of claims "
            "voting in each class. The court reviews ballots, eligibility, and disputes. The burden is on the plan proponent to demonstrate acceptance. The doctrine ensures democratic approval "
            "and protects minority interests."
        ),
        key_factors=[
            "Impaired class",
            "Voting eligibility",
            "Ballot count",
            "Majority and supermajority",
            "Disputed ballots"
        ],
        primary_authority=["11 USC §1126", "In re M & J Birmingham, LLC, 545 B.R. 401 (Bankr. N.D. Ala. 2015)"],
        burden_holder="Plan proponent",
        adversary_position="Dissenting creditors",
        counter_arguments=[
            "Ballots are improper",
            "Class is not impaired",
            "Voting process is flawed"
        ],
        resolution_strategy="Ballot review, confirmation hearing, court order",
        entity_scope="Debtor, creditors, estate",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re M & J Birmingham, LLC, 545 B.R. 401 (Bankr. N.D. Ala. 2015)"
    ),
    DoctrineBlock(
        topic="Section 1123 Plan Requirements",
        keywords=["section 1123", "plan requirements", "classification", "treatment", "bankruptcy"],
        conclusion_template="A Chapter 11 plan must comply with 11 USC §1123 requirements, including classification, treatment, and disclosure.",
        reasoning_framework=(
            "Section 1123 sets forth mandatory and permissive requirements for Chapter 11 plans. Plans must classify claims, specify treatment, provide for implementation, and include necessary "
            "disclosures. The court reviews compliance, fairness, and creditor objections. The burden is on the plan proponent to demonstrate compliance. The doctrine ensures transparency and "
            "structured reorganization."
        ),
        key_factors=[
            "Classification",
            "Treatment",
            "Implementation",
            "Disclosure",
            "Creditor objections"
        ],
        primary_authority=["11 USC §1123", "In re S & I Properties, Inc., 137 F.3d 1174 (9th Cir. 1998)"],
        burden_holder="Plan proponent",
        adversary_position="Creditor",
        counter_arguments=[
            "Plan fails to classify claims",
            "Treatment is unfair",
            "Disclosure is inadequate"
        ],
        resolution_strategy="Confirmation hearing, judicial determination",
        entity_scope="Debtor, creditors, estate",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re S & I Properties, Inc., 137 F.3d 1174 (9th Cir. 1998)"
    ),
    DoctrineBlock(
        topic="Section 1145 Exempt Securities",
        keywords=["section 1145", "exempt securities", "plan confirmation", "bankruptcy", "registration exemption"],
        conclusion_template="Securities issued under a Chapter 11 plan may be exempt from registration under 11 USC §1145, subject to compliance.",
        reasoning_framework=(
            "Section 1145 provides an exemption from securities registration for securities issued under a Chapter 11 plan. The exemption applies to certain recipients and types of securities. "
            "The court reviews plan compliance, recipient eligibility, and objections. The burden is on the plan proponent to demonstrate exemption. The doctrine facilitates restructuring and "
            "capital raising."
        ),
        key_factors=[
            "Plan compliance",
            "Recipient eligibility",
            "Type of security",
            "Registration requirements",
            "Objections"
        ],
        primary_authority=["11 USC §1145", "SEC v. Universal Express, Inc., 475 F.Supp.2d 412 (S.D.N.Y. 2007)"],
        burden_holder="Plan proponent",
        adversary_position="SEC or objecting parties",
        counter_arguments=[
            "Exemption does not apply",
            "Security is not eligible",
            "Recipient is not qualified"
        ],
        resolution_strategy="Confirmation hearing, judicial determination",
        entity_scope="Debtor, creditors, investors",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SEC v. Universal Express, Inc., 475 F.Supp.2d 412 (S.D.N.Y. 2007)"
    ),
    DoctrineBlock(
        topic="Section 105 Equitable Powers",
        keywords=["section 105", "equitable powers", "court authority", "bankruptcy"],
        conclusion_template="Bankruptcy courts may issue orders necessary to carry out the provisions of the Bankruptcy Code under 11 USC §105.",
        reasoning_framework=(
            "Section 105 grants bankruptcy courts broad equitable powers to issue orders, enforce provisions, and remedy violations. The court must act within statutory boundaries and cannot "
            "contradict explicit Code provisions. The doctrine allows flexibility and fairness, but is subject to appellate review. The burden is on the party seeking relief to justify necessity."
        ),
        key_factors=[
            "Necessity",
            "Statutory boundaries",
            "Equitable relief",
            "Court authority",
            "Appellate review"
        ],
        primary_authority=["11 USC §105", "In re Continental Airlines, 203 F.3d 203 (3d Cir. 2000)"],
        burden_holder="Party seeking relief",
        adversary_position="Objecting parties",
        counter_arguments=[
            "Relief exceeds statutory authority",
            "Contradicts Code provisions",
            "Not necessary"
        ],
        resolution_strategy="Motion, evidentiary hearing, court order",
        entity_scope="Debtor, creditors, court",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Continental Airlines, 203 F.3d 203 (3d Cir. 2000)"
    ),
    DoctrineBlock(
        topic="Section 502(b)(6) Lease Rejection Cap",
        keywords=["section 502(b)(6)", "lease rejection", "damages cap", "bankruptcy", "claim calculation"],
        conclusion_template="Damages for lease rejection are capped under 11 USC §502(b)(6), limiting landlord claims in bankruptcy.",
        reasoning_framework=(
            "Section 502(b)(6) limits landlord claims for lease rejection to the greater of one year's rent or rent for the remaining lease term, not to exceed three years. The court calculates "
            "damages based on lease terms, mitigation, and statutory cap. The burden is on the landlord to prove claim. The doctrine prevents excessive claims and preserves estate assets."
        ),
        key_factors=[
            "Lease terms",
            "Mitigation",
            "Statutory cap",
            "Claim calculation",
            "Court approval"
        ],
        primary_authority=["11 USC §502(b)(6)", "In re Klein, 940 F.2d 1079 (9th Cir. 1991)"],
        burden_holder="Landlord",
        adversary_position="Debtor",
        counter_arguments=[
            "Claim exceeds cap",
            "Mitigation not considered",
            "Calculation is improper"
        ],
        resolution_strategy="Claim objection, evidentiary hearing, court order",
        entity_scope="Debtor, landlords, estate",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Klein, 940 F.2d 1079 (9th Cir. 1991)"
    ),
    DoctrineBlock(
        topic="Section 547(c) Defenses",
        keywords=["section 547(c)", "preference defense", "ordinary course", "new value", "bankruptcy"],
        conclusion_template="Creditors may defend preference actions under 11 USC §547(c) by demonstrating ordinary course, new value, or contemporaneous exchange.",
        reasoning_framework=(
            "Section 547(c) provides defenses to preference actions, including ordinary course of business, contemporaneous exchange for new value, and subsequent new value. The creditor must "
            "prove eligibility, timing, and business practices. The court reviews evidence and objections. The doctrine prevents avoidance of legitimate transactions and protects creditor rights."
        ),
        key_factors=[
            "Ordinary course",
            "New value",
            "Contemporaneous exchange",
            "Timing",
            "Business practices"
        ],
        primary_authority=["11 USC §547(c)", "Barnhill v. Johnson, 503 U.S. 393 (1992)"],
        burden_holder="Creditor",
        adversary_position="Trustee",
        counter_arguments=[
            "Defense is inapplicable",
            "Transaction is not ordinary",
            "New value is insufficient"
        ],
        resolution_strategy="Adversary proceeding, evidentiary hearing, court order",
        entity_scope="Debtor, creditors, trustee",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Barnhill v. Johnson, 503 U.S. 393 (1992)"
    ),
    DoctrineBlock(
        topic="Section 548(a)(2) Constructive Fraud",
        keywords=["section 548(a)(2)", "constructive fraud", "fraudulent transfer", "reasonably equivalent value", "insolvency"],
        conclusion_template="Transfers for less than reasonably equivalent value while insolvent may be avoided as constructive fraud under 11 USC §548(a)(2).",
        reasoning_framework=(
            "Section 548(a)(2) allows avoidance of transfers made for less than reasonably equivalent value while the debtor was insolvent, intended to incur debts beyond ability to pay, or "
            "engaged in business with unreasonably small capital. The court reviews value, timing, and financial condition. The burden is on the trustee to prove avoidability. The doctrine "
            "protects creditors and preserves estate assets."
        ),
        key_factors=[
            "Value exchanged",
            "Insolvency",
            "Timing",
            "Financial condition",
            "Defenses"
        ],
        primary_authority=["11 USC §548(a)(2)", "In re Acequia, Inc., 34 F.3d 800 (9th Cir. 1994)"],
        burden_holder="Trustee",
        adversary_position="Transferee",
        counter_arguments=[
            "Value was reasonably equivalent",
            "Debtor was solvent",
            "Transfer was in ordinary course"
        ],
        resolution_strategy="Adversary proceeding, evidentiary hearing, court order",
        entity_scope="Debtor, transferee, estate",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Acequia, Inc., 34 F.3d 800 (9th Cir. 1994)"
    ),
    DoctrineBlock(
        topic="Section 523(a) Non-Dischargeable Debts",
        keywords=["section 523(a)", "non-dischargeable", "exceptions", "fraud", "student loans", "domestic support"],
        conclusion_template="Certain debts are excepted from discharge under 11 USC §523(a), including fraud, student loans, and domestic support obligations.",
        reasoning_framework=(
            "Section 523(a) enumerates debts excepted from discharge, including taxes, domestic support, student loans, and debts arising from fraud or willful injury. The court reviews debtor "
            "conduct, nature of debt, and statutory exclusions. Creditors may object to dischargeability. The burden is on the creditor to prove exception. The doctrine balances debtor relief "
            "and creditor protection."
        ),
        key_factors=[
            "Debtor conduct",
            "Nature of debt",
            "Statutory exceptions",
            "Creditor objections",
            "Court determination"
        ],
        primary_authority=["11 USC §523(a)", "Grogan v. Garner, 498 U.S. 279 (1991)"],
        burden_holder="Creditor",
        adversary_position="Debtor",
        counter_arguments=[
            "Debt is dischargeable",
            "Exception does not apply",
            "Creditor lacks evidence"
        ],
        resolution_strategy="Adversary proceeding, evidentiary hearing, court order",
        entity_scope="Debtor, creditors, estate",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Grogan v. Garner, 498 U.S. 279 (1991)"
    ),
    DoctrineBlock(
        topic="Section 364(d) Priming Liens",
        keywords=["section 364(d)", "priming lien", "DIP financing", "secured creditor", "adequate protection"],
        conclusion_template="Courts may authorize priming liens for DIP financing under 11 USC §364(d) if adequate protection is provided to existing secured creditors.",
        reasoning_framework=(
            "Section 364(d) allows courts to authorize priming liens for DIP financing if the debtor cannot otherwise obtain credit and provides adequate protection to existing secured creditors. "
            "The court reviews necessity, terms, and impact. Creditors may object to priming and adequacy of protection. The burden is on the debtor to justify priming. The doctrine balances "
            "restructuring needs and creditor rights."
        ),
        key_factors=[
            "Necessity",
            "Adequate protection",
            "Terms of financing",
            "Creditor objections",
            "Court approval"
        ],
        primary_authority=["11 USC §364(d)", "In re FCX, Inc., 54 B.R. 49 (Bankr. E.D.N.C. 1985)"],
        burden_holder="Debtor",
        adversary_position="Secured creditors",
        counter_arguments=[
            "Protection is inadequate",
            "Priming is unnecessary",
            "Terms are unfair"
        ],
        resolution_strategy="Motion for approval, evidentiary hearing, court order",
        entity_scope="Debtor, secured creditors, lenders",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re FCX, Inc., 54 B.R. 49 (Bankr. E.D.N.C. 1985)"
    ),
    DoctrineBlock(
        topic="Section 365(h) Tenant Rights",
        keywords=["section 365(h)", "tenant rights", "lease rejection", "bankruptcy", "real property"],
        conclusion_template="Tenants may retain rights under rejected real property leases under 11 USC §365(h), subject to statutory limitations.",
        reasoning_framework=(
            "Section 365(h) protects tenant rights in real property leases upon rejection. Tenants may elect to retain possession for the remainder of the lease term, subject to rent and other "
            "obligations. The court reviews lease terms, tenant election, and objections. The burden is on the tenant to assert rights. The doctrine balances debtor relief and tenant protection."
        ),
        key_factors=[
            "Lease terms",
            "Tenant election",
            "Statutory limitations",
            "Obligations",
            "Court approval"
        ],
        primary_authority=["11 USC §365(h)", "In re Flagstaff Realty Assocs., 60 F.3d 1031 (3d Cir. 1995)"],
        burden_holder="Tenant",
        adversary_position="Debtor",
        counter_arguments=[
            "Election is improper",
            "Lease is not eligible",
            "Obligations are unmet"
        ],
        resolution_strategy="Motion, evidentiary hearing, court order",
        entity_scope="Debtor, tenants, estate",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Flagstaff Realty Assocs., 60 F.3d 1031 (3d Cir. 1995)"
    ),
    DoctrineBlock(
        topic="Section 365(n) Intellectual Property Licensee Rights",
        keywords=["section 365(n)", "intellectual property", "licensee", "bankruptcy", "contract rejection"],
        conclusion_template="Licensees of intellectual property may retain rights under rejected contracts under 11 USC §365(n).",
        reasoning_framework=(
            "Section 365(n) protects licensees of intellectual property upon contract rejection. Licensees may elect to retain rights to use intellectual property, subject to contract terms and "
            "obligations. The court reviews license terms, election, and objections. The burden is on the licensee to assert rights. The doctrine balances debtor relief and licensee protection."
        ),
        key_factors=[
            "License terms",
            "Election",
            "Intellectual property definition",
            "Obligations",
            "Court approval"
        ],
        primary_authority=["11 USC §365(n)", "In re Exide Technologies, 607 F.3d 957 (3d Cir. 2010)"],
        burden_holder="Licensee",
        adversary_position="Debtor",
        counter_arguments=[
            "Election is improper",
            "IP is not eligible",
            "Obligations are unmet"
        ],
        resolution_strategy="Motion, evidentiary hearing, court order",
        entity_scope="Debtor, licensees, estate",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Exide Technologies, 607 F.3d 957 (3d Cir. 2010)"
    ),
    DoctrineBlock(
        topic="Section 1125 Disclosure Statement",
        keywords=["section 1125", "disclosure statement", "plan confirmation", "adequate information", "bankruptcy"],
        conclusion_template="A disclosure statement must provide adequate information for creditors to evaluate the Chapter 11 plan under 11 USC §1125.",
        reasoning_framework=(
            "Section 1125 requires a disclosure statement containing adequate information for creditors to make informed decisions about the plan. The court reviews content, adequacy, and objections. "
            "The burden is on the plan proponent to demonstrate adequacy. The doctrine ensures transparency and informed voting."
        ),
        key_factors=[
            "Adequate information",
            "Content",
            "Creditor objections",
            "Court approval",
            "Plan evaluation"
        ],
        primary_authority=["11 USC §1125", "In re Ferretti, 128 B.R. 16 (Bankr. S.D. Tex. 1991)"],
        burden_holder="Plan proponent",
        adversary_position="Creditor",
        counter_arguments=[
            "Disclosure is inadequate",
            "Information is misleading",
            "Objections are unresolved"
        ],
        resolution_strategy="Disclosure hearing, court order",
        entity_scope="Debtor, creditors, estate",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Ferretti, 128 B.R. 16 (Bankr. S.D. Tex. 1991)"
    ),
    DoctrineBlock(
        topic="Section 1122 Classification",
        keywords=["section 1122", "classification", "claims", "plan confirmation", "bankruptcy"],
        conclusion_template="Claims must be classified in a Chapter 11 plan under 11 USC §1122, subject to fairness and statutory requirements.",
        reasoning_framework=(
            "Section 1122 requires classification of claims in a Chapter 11 plan. Claims may be grouped by similarity, but cannot be classified to manipulate voting or unfairly discriminate. The court "
            "reviews classification, fairness, and objections. The burden is on the plan proponent to justify classification. The doctrine ensures structured and fair reorganization."
        ),
        key_factors=[
            "Similarity of claims",
            "Classification",
            "Fairness",
            "Voting manipulation",
            "Court approval"
        ],
        primary_authority=["11 USC §1122", "In re Holywell Corp., 913 F.2d 873 (11th Cir. 1990)"],
        burden_holder="Plan proponent",
        adversary_position="Creditor",
        counter_arguments=[
            "Classification is improper",
            "Manipulates voting",
            "Discriminates unfairly"
        ],
        resolution_strategy="Confirmation hearing, judicial determination",
        entity_scope="Debtor, creditors, estate",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Holywell Corp., 913 F.2d 873 (11th Cir. 1990)"
    ),
    DoctrineBlock(
        topic="Section 363(m) Good Faith Purchaser Protection",
        keywords=["section 363(m)", "good faith purchaser", "asset sale", "bankruptcy", "appeal"],
        conclusion_template="Good faith purchasers of estate assets are protected from reversal on appeal under 11 USC §363(m).",
        reasoning_framework=(
            "Section 363(m) protects good faith purchasers of estate assets from reversal on appeal, provided the sale was authorized and notice was adequate. The court reviews purchaser conduct, "
            "sale process, and objections. The burden is on the purchaser to demonstrate good faith. The doctrine encourages participation and preserves sale integrity."
        ),
        key_factors=[
            "Good faith",
            "Sale process",
            "Notice",
            "Court approval",
            "Appeal"
        ],
        primary_authority=["11 USC §363(m)", "In re Gucci, 126 F.3d 380 (2d Cir. 1997)"],
        burden_holder="Purchaser",
        adversary_position="Objecting parties",
        counter_arguments=[
            "Purchaser lacked good faith",
            "Notice was inadequate",
            "Sale was unauthorized"
        ],
        resolution_strategy="Motion, evidentiary hearing, court order",
        entity_scope="Debtor, purchasers, estate",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Gucci, 126 F.3d 380 (2d Cir. 1997)"
    ),
    DoctrineBlock(
        topic="Section 363(f) Sale Free and Clear",
        keywords=["section 363(f)", "free and clear", "asset sale", "bankruptcy", "liens"],
        conclusion_template="Estate assets may be sold free and clear of liens under 11 USC §363(f), subject to statutory conditions and court approval.",
        reasoning_framework=(
            "Section 363(f) allows sale of estate assets free and clear of liens if certain conditions are met: consent, lien can be paid, price exceeds lien, lien is in bona fide dispute, or lienholder "
            "could be compelled to accept money satisfaction. The court reviews conditions, objections, and sale terms. The burden is on the debtor to demonstrate compliance. The doctrine facilitates "
            "efficient restructuring and value maximization."
        ),
        key_factors=[
            "Statutory conditions",
            "Consent",
            "Price",
            "Lien dispute",
            "Court approval"
        ],
        primary_authority=["11 USC §363(f)", "In re P.K.R. Convalescent Centers, Inc., 189 B.R. 90 (Bankr. E.D. Tex. 1995)"],
        burden_holder="Debtor",
        adversary_position="Lienholders",
        counter_arguments=[
            "Conditions are unmet",
            "Sale is not free and clear",
            "Objections unresolved"
        ],
        resolution_strategy="Motion for approval, evidentiary hearing, court order",
        entity_scope="Debtor, lienholders, estate",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re P.K.R. Convalescent Centers, Inc., 189 B.R. 90 (Bankr. E.D. Tex. 1995)"
    ),
    DoctrineBlock(
        topic="Section 362(d) Relief from Stay",
        keywords=["section 362(d)", "relief from stay", "automatic stay", "secured creditor", "bankruptcy"],
        conclusion_template="Courts may grant relief from automatic stay under 11 USC §362(d) for cause, including lack of adequate protection or unnecessary property.",
        reasoning_framework=(
            "Section 362(d) authorizes courts to grant relief from automatic stay for cause, including lack of adequate protection, property not necessary for reorganization, or debtor misconduct. "
            "The court reviews creditor motion, debtor response, and evidence. The burden is on the creditor to demonstrate cause. The doctrine balances creditor rights and debtor protection."
        ),
        key_factors=[
            "Cause",
            "Adequate protection",
            "Necessity for reorganization",
            "Creditor motion",
            "Court approval"
        ],
        primary_authority=["11 USC §362(d)", "In re Timbers of Inwood Forest, 484 U.S. 365 (1988)"],
        burden_holder="Creditor",
        adversary_position="Debtor",
        counter_arguments=[
            "Protection is adequate",
            "Property is necessary",
            "Motion lacks cause"
        ],
        resolution_strategy="Motion, evidentiary hearing, court order",
        entity_scope="Debtor, secured creditors, estate",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Timbers of Inwood Forest, 484 U.S. 365 (1988)"
    ),
    DoctrineBlock(
        topic="Section 1129(a)(3) Good Faith Plan Proposal",
        keywords=["section 1129(a)(3)", "good faith", "plan confirmation", "chapter 11", "bankruptcy"],
        conclusion_template="A Chapter 11 plan must be proposed in good faith under 11 USC §1129(a)(3), subject to court review and creditor objections.",
        reasoning_framework=(
            "Section 1129(a)(3) requires that a Chapter 11 plan be proposed in good faith. The court reviews plan purpose, debtor conduct, and creditor objections. Good faith is judged by honesty, "
            "fairness, and compliance with law. The burden is on the plan proponent to demonstrate good faith. The doctrine ensures integrity and protects creditor interests."
        ),
        key_factors=[
            "Plan purpose",
            "Debtor conduct",
            "Creditor objections",
            "Compliance",
            "Court review"
        ],
        primary_authority=["11 USC §1129(a)(3)", "In re Madison Hotel Associates, 749 F.2d 410 (7th Cir. 1984)"],
        burden_holder="Plan proponent",
        adversary_position="Creditor",
        counter_arguments=[
            "Plan is not in good faith",
            "Purpose is improper",
            "Conduct is dishonest"
        ],
        resolution_strategy="Confirmation hearing, judicial determination",
        entity_scope="Debtor, creditors, estate",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Madison Hotel Associates, 749 F.2d 410 (7th Cir. 1984)"
    ),
    DoctrineBlock(
        topic="Section 1129(a)(11) Feasibility",
        keywords=["section 1129(a)(11)", "feasibility", "plan confirmation", "chapter 11", "bankruptcy"],
        conclusion_template="A Chapter 11 plan must be feasible under 11 USC §1129(a)(11), meaning it is not likely to result in liquidation or further financial distress.",
        reasoning_framework=(
            "Section 1129(a)(11) requires that a Chapter 11 plan be feasible. The court reviews financial projections, management competence, and creditor objections. Feasibility means the debtor "
            "can implement the plan without likely liquidation or further distress. The burden is on the plan proponent to demonstrate feasibility. The doctrine ensures realistic restructuring "
            "and protects creditor interests."
        ),
        key_factors=[
            "Financial projections",
            "Management competence",
            "Creditor objections",
            "Plan implementation",
            "Court review"
        ],
        primary_authority=["11 USC §1129(a)(11)", "In re Clarkson, 767 F.2d 417 (8th Cir. 1985)"],
        burden_holder="Plan proponent",
        adversary_position="Creditor",
        counter_arguments=[
            "Plan is not feasible",
            "Projections are unrealistic",
            "Management is incompetent"
        ],
        resolution_strategy="Confirmation hearing, evidentiary submissions, court order",
        entity_scope="Debtor, creditors, estate",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Clarkson, 767 F.2d 417 (8th Cir. 1985)"
    ),
    DoctrineBlock(
        topic="Section 1129(a)(7) Best Interests Test",
        keywords=["section 1129(a)(7)", "best interests", "plan confirmation", "chapter 11", "liquidation"],
        conclusion_template="A Chapter 11 plan must satisfy the best interests of creditors test under 11 USC §1129(a)(7), ensuring creditors receive at least as much as in liquidation.",
        reasoning_framework=(
            "Section 1129(a)(7) requires that creditors receive at least as much under the plan as they would in liquidation. The court reviews liquidation analysis, plan distributions, and creditor "
            "objections. The burden is on the plan proponent to demonstrate compliance. The doctrine protects creditor interests and ensures fairness."
        ),
        key_factors=[
            "Liquidation analysis",
            "Plan distributions",
            "Creditor objections",
            "Court review",
            "Compliance"
        ],
        primary_authority=["11 USC §1129(a)(7)", "In re Drexel Burnham Lambert Group, Inc., 138 B.R. 723 (Bankr. S.D.N.Y. 1992)"],
        burden_holder="Plan proponent",
        adversary_position="Creditor",
        counter_arguments=[
            "Distribution is inadequate",
            "Liquidation analysis is flawed",
            "Test is unmet"
        ],
        resolution_strategy="Confirmation hearing, evidentiary submissions, court order",
        entity_scope="Debtor, creditors, estate",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Drexel Burnham Lambert Group, Inc., 138 B.R. 723 (Bankr. S.D.N.Y. 1992)"
    ),
    DoctrineBlock(
        topic="Section 1129(a)(9) Priority Claim Treatment",
        keywords=["section 1129(a)(9)", "priority claims", "plan confirmation", "chapter 11", "bankruptcy"],
        conclusion_template="A Chapter 11 plan must provide for payment of priority claims under 11 USC §1129(a)(9), subject to statutory requirements.",
        reasoning_framework=(
            "Section 1129(a)(9) requires that priority claims be paid in full under the plan, unless the claimant agrees to different treatment. The court reviews claim classification, payment terms, "
            "and creditor objections. The burden is on the plan proponent to demonstrate compliance. The doctrine protects priority creditors and ensures statutory compliance."
        ),
        key_factors=[
            "Claim classification",
            "Payment terms",
            "Creditor objections",
            "Court review",
            "Compliance"
        ],
        primary_authority=["11 USC §1129(a)(9)", "In re Johnson, 346 B.R. 190 (Bankr. S.D. Ga. 2006)"],
        burden_holder="Plan proponent",
        adversary_position="Priority creditors",
        counter_arguments=[
            "Payment is inadequate",
            "Classification is improper",
            "Compliance is lacking"
        ],
        resolution_strategy="Confirmation hearing, judicial determination",
        entity_scope="Debtor, priority creditors, estate",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Johnson, 346 B.R. 190 (Bankr. S.D. Ga. 2006)"
    ),
    DoctrineBlock(
        topic="Section 1129(b) Cramdown",
        keywords=["section 1129(b)", "cramdown", "plan confirmation", "absolute priority", "fair and equitable"],
        conclusion_template="A Chapter 11 plan may be confirmed over dissenting class objections via cramdown under 11 USC §1129(b) if it is fair and equitable.",
        reasoning_framework=(
            "Section 1129(b) authorizes cramdown confirmation if the plan does not discriminate unfairly and is fair and equitable to dissenting classes. The court reviews plan structure, distributions, "
            "and compliance. The burden is on the plan proponent to demonstrate fairness. The doctrine protects minority interests and ensures statutory compliance."
        ),
        key_factors=[
            "Plan structure",
            "Distributions",
            "Fairness",
            "Absolute priority",
            "Court review"
        ],
        primary_authority=["11 USC §1129(b)", "Bank of America Nat. Trust v. 203 North LaSalle Street Partnership, 526 U.S. 434 (1999)"],
        burden_holder="Plan proponent",
        adversary_position="Dissenting creditors",
        counter_arguments=[
            "Plan is unfair",
            "Absolute priority is violated",
            "Discrimination is present"
        ],
        resolution_strategy="Confirmation hearing, judicial determination",
        entity_scope="Debtor, creditors, estate",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Bank of America Nat. Trust v. 203 North LaSalle Street Partnership, 526 U.S. 434 (1999)"
    ),
    DoctrineBlock(
        topic="Section 1191 Subchapter V Plan Confirmation",
        keywords=["section 1191", "subchapter V", "plan confirmation", "small business", "cramdown"],
        conclusion_template="Subchapter V plans may be confirmed without impaired class acceptance under 11 USC §1191, subject to fairness and feasibility.",
        reasoning_framework=(
            "Section 1191 allows confirmation of Subchapter V plans without impaired class acceptance if the plan is fair and equitable and feasible. The court reviews plan terms, creditor objections, "
            "and compliance. The burden is on the debtor to demonstrate fairness and feasibility. The doctrine facilitates small business restructuring and protects creditor interests."
        ),
        key_factors=[
            "Plan terms",
            "Fairness",
            "Feasibility",
            "Creditor objections",
            "Court review"
        ],
        primary_authority=["11 USC §1191", "In re Ventura, 615 B.R. 1 (Bankr. E.D.N.Y. 2020)"],
        burden_holder="Debtor",
        adversary_position="Creditors",
        counter_arguments=[
            "Plan is unfair",
            "Feasibility is lacking",
            "Objections are unresolved"
        ],
        resolution_strategy="Confirmation hearing, judicial determination",
        entity_scope="Small business debtor, creditors, estate",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Ventura, 615 B.R. 1 (Bankr. E.D.N.Y. 2020)"
    ),
    DoctrineBlock(
        topic="Section 1181 Subchapter V Trustee Role",
        keywords=["section 1181", "subchapter V", "trustee", "small business", "plan confirmation"],
        conclusion_template="Subchapter V trustees oversee but do not operate the debtor's business under 11 USC §1181, facilitating plan confirmation and creditor protection.",
        reasoning_framework=(
            "Section 1181 defines the role of Subchapter V trustees as oversight, not operation, of the debtor's business. Trustees facilitate plan confirmation, creditor communication, and compliance. "
            "The court reviews trustee actions, debtor conduct, and objections. The burden is on the trustee to fulfill statutory duties. The doctrine ensures fairness and efficient restructuring."
        ),
        key_factors=[
            "Trustee duties",
            "Oversight",
            "Plan facilitation",
            "Creditor communication",
            "Court review"
        ],
        primary_authority=["11 USC §1181", "In re Ventura, 615 B.R. 1 (Bankr. E.D.N.Y. 2020)"],
        burden_holder="Trustee",
        adversary_position="Debtor or creditors",
        counter_arguments=[
            "Trustee actions are improper",
            "Oversight is lacking",
            "Duties are unmet"
        ],
        resolution_strategy="Court review, evidentiary hearing, order",
        entity_scope="Small business debtor, trustee, creditors",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Ventura, 615 B.R. 1 (Bankr. E.D.N.Y. 2020)"
    ),
    DoctrineBlock(
        topic="Section 1192 Subchapter V Discharge",
        keywords=["section 1192", "subchapter V", "discharge", "small business", "plan confirmation"],
        conclusion_template="Subchapter V debtors may receive discharge under 11 USC §1192 upon plan confirmation, subject to exceptions and compliance.",
        reasoning_framework=(
            "Section 1192 provides for discharge of debts upon Subchapter V plan confirmation, subject to exceptions for certain debts and compliance with plan terms. The court reviews debtor conduct, "
            "plan compliance, and creditor objections. The burden is on the debtor to demonstrate eligibility. The doctrine facilitates small business relief and protects creditor interests."
        ),
        key_factors=[
            "Plan confirmation",
            "Debtor conduct",
            "Exceptions",
            "Compliance",
            "Court review"
        ],
        primary_authority=["11 USC §1192", "In re Ventura, 615 B.R. 1 (Bankr. E.D.N.Y. 2020)"],
        burden_holder="Debtor",
        adversary_position="Creditors",
        counter_arguments=[
            "Discharge is improper",
            "Exceptions apply",
            "Compliance is lacking"
        ],
        resolution_strategy="Confirmation hearing, judicial determination",
        entity_scope="Small business debtor, creditors, estate",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re Ventura, 615 B.R. 1 (Bankr. E.D.N.Y. 2020)"
    ),
    DoctrineBlock(
        topic="Section 1194 Subchapter V Distribution",
        keywords=["section 1194", "subchapter V", "distribution", "small business", "plan confirmation"],
        conclusion_template="Subchapter V distributions are governed by 11 USC §1194, prioritizing administrative expenses and creditor claims.",
        reasoning_framework=(
            "Section 1194 governs distributions under Subchapter V, prioritizing administrative expenses and