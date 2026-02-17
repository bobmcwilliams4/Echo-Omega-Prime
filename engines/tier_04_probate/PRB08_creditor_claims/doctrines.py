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
        topic="Notice to Creditors - Publication Requirements",
        keywords=["notice", "creditors", "publication", "probate", "PRB08", "statutory notice", "unknown creditors"],
        conclusion_template="The personal representative must publish notice to creditors in a newspaper of general circulation for at least three consecutive weeks.",
        reasoning_framework=(
            "The statutory framework requires that, upon appointment, the personal representative must provide notice to unknown creditors by publication. "
            "This requirement is designed to ensure due process and provide an opportunity for all potential claimants to assert their claims against the estate. "
            "Failure to comply with the publication requirement may result in the extension of the claims period or personal liability for the representative. "
            "The sufficiency of publication is measured by statutory compliance, not actual notice. "
            "Courts have held that strict adherence to the publication schedule and content is necessary, and that minor deviations may invalidate the notice. "
            "The notice must include the name of the decedent, the court, the case number, and instructions for submitting claims. "
            "Publication must occur in a newspaper that is widely circulated in the county where probate is pending. "
            "If no such newspaper exists, alternative methods may be approved by the court. "
            "The time period for claims by unknown creditors begins to run from the date of first publication. "
            "Known creditors must also be notified directly, but publication is the exclusive method for unknown creditors. "
            "Failure to publish may toll the claims period indefinitely for unknown creditors. "
            "The representative should retain proof of publication for the court file. "
            "If a creditor asserts lack of notice, the court will examine the record for compliance with statutory mandates. "
            "Substantial compliance may suffice if the deviation did not prejudice creditors, but this is rare. "
            "The burden of proof is on the personal representative to demonstrate proper publication."
        ),
        key_factors=[
            "Timeliness and frequency of publication",
            "Content of notice",
            "Circulation of chosen newspaper",
            "Retention of proof",
            "Distinction between known and unknown creditors"
        ],
        primary_authority=[
            "PRB08 § 3-801(a)-(c)",
            "In re Estate of Smith, 234 P.3d 123 (PRB08 2010)",
            "PRB08 Probate Rule 4.01"
        ],
        burden_holder="Personal Representative",
        adversary_position="Creditor may argue lack of notice or insufficient publication",
        counter_arguments=[
            "Substantial compliance with publication requirements",
            "No prejudice to creditor from minor defects",
            "Creditor had actual notice"
        ],
        resolution_strategy="Strict compliance with statutory publication requirements; court may allow late claims if notice was deficient.",
        entity_scope="Personal Representatives, Unknown Creditors",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="In re Estate of Smith, 234 P.3d 123 (PRB08 2010)"
    ),
    DoctrineBlock(
        topic="Four-Month Claims Period for Known Creditors",
        keywords=["claims period", "known creditors", "notice", "probate", "statute of limitations", "PRB08"],
        conclusion_template="A known creditor must present a claim within four months after the date of first publication of notice or be forever barred.",
        reasoning_framework=(
            "Statutory law in PRB08 establishes a four-month window for known creditors to present claims against the estate. "
            "The period begins to run from the date of first publication of notice to creditors. "
            "A creditor is 'known' if the personal representative is aware of the claim or reasonably should be. "
            "Direct notice must be sent to all known creditors. "
            "If a known creditor is not given direct notice, the four-month bar may not apply, and the claim may be allowed later. "
            "The purpose of the time limit is to promote prompt administration and finality. "
            "Courts strictly enforce the bar, but may toll the period if the representative fails to provide required notice. "
            "The creditor bears the burden of proving lack of notice. "
            "If a claim is presented after the four-month period, it is generally barred unless excused by statute or equitable principles. "
            "Exceptions are rare and require a showing of fraud, concealment, or excusable neglect."
        ),
        key_factors=[
            "Date of first publication",
            "Whether creditor was known",
            "Proof of direct notice",
            "Timeliness of claim presentation"
        ],
        primary_authority=[
            "PRB08 § 3-803(a)-(b)",
            "Estate of Jones, 201 P.3d 456 (PRB08 2009)"
        ],
        burden_holder="Creditor",
        adversary_position="Personal representative may assert the claim is time-barred",
        counter_arguments=[
            "No direct notice was provided",
            "Personal representative concealed the claim",
            "Fraud or mistake prevented timely filing"
        ],
        resolution_strategy="Strict enforcement of four-month bar unless statutory or equitable exception applies.",
        entity_scope="Known Creditors, Personal Representatives",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Estate of Jones, 201 P.3d 456 (PRB08 2009)"
    ),
    DoctrineBlock(
        topic="Priority of Claims - Funeral Expenses First Class",
        keywords=["priority", "claims", "funeral expenses", "first class", "probate", "PRB08", "payment order"],
        conclusion_template="Funeral expenses are classified as first priority and must be paid before other unsecured claims.",
        reasoning_framework=(
            "PRB08 law establishes a hierarchy for payment of estate claims. "
            "Funeral expenses are given first priority, reflecting a public policy to ensure proper disposition of the decedent. "
            "The amount allowed is limited to what is reasonable and customary for the decedent's circumstances. "
            "Excessive or extravagant expenses may be disallowed or reduced by the court. "
            "The personal representative must pay funeral expenses before other unsecured debts, except for administrative expenses. "
            "If the estate is insolvent, funeral expenses are paid pro rata with other first-class claims. "
            "Courts may scrutinize the necessity and reasonableness of the charges. "
            "Disputes over classification are resolved by reference to statutory definitions and case law."
        ),
        key_factors=[
            "Reasonableness of expenses",
            "Customary charges in community",
            "Order of payment",
            "Estate solvency"
        ],
        primary_authority=[
            "PRB08 § 3-805(a)(1)",
            "In re Estate of Green, 145 P.3d 789 (PRB08 2007)"
        ],
        burden_holder="Personal Representative",
        adversary_position="Other creditors may challenge classification or amount",
        counter_arguments=[
            "Expenses are excessive or not customary",
            "Improper allocation to funeral category"
        ],
        resolution_strategy="Court reviews reasonableness and necessity of expenses; applies statutory priority.",
        entity_scope="Personal Representatives, Funeral Service Providers",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="In re Estate of Green, 145 P.3d 789 (PRB08 2007)"
    ),
    DoctrineBlock(
        topic="Secured Claims Priority and Rights",
        keywords=["secured claims", "priority", "collateral", "probate", "PRB08", "security interest"],
        conclusion_template="Secured creditors retain their security interest and may enforce against collateral before unsecured claims are paid.",
        reasoning_framework=(
            "Secured creditors are treated differently from unsecured creditors in probate. "
            "A secured creditor may choose to enforce the security interest against the collateral or participate as an unsecured creditor for any deficiency. "
            "The estate is not required to pay secured claims from general assets unless the collateral is insufficient. "
            "If the estate wishes to retain the collateral, it must pay the secured debt in full. "
            "The priority of secured claims is determined by the date and validity of the security interest. "
            "Statutory liens, such as tax liens, may have super-priority. "
            "The personal representative must notify secured creditors of the administration and allow them to assert their rights. "
            "Disputes over the value of collateral or the amount of the secured claim are resolved by the court."
        ),
        key_factors=[
            "Validity of security interest",
            "Value of collateral",
            "Election by secured creditor",
            "Existence of statutory liens"
        ],
        primary_authority=[
            "PRB08 § 3-806",
            "PRB08 § 3-805(b)",
            "Estate of Carter, 167 P.3d 234 (PRB08 2011)"
        ],
        burden_holder="Secured Creditor",
        adversary_position="Personal representative may challenge validity or amount",
        counter_arguments=[
            "Security interest is invalid or unperfected",
            "Collateral is overvalued or undervalued",
            "Statutory lien has priority"
        ],
        resolution_strategy="Court determines validity and amount of secured claim; applies statutory priority rules.",
        entity_scope="Secured Creditors, Personal Representatives",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Estate of Carter, 167 P.3d 234 (PRB08 2011)"
    ),
    DoctrineBlock(
        topic="Family Allowance and Exempt Property",
        keywords=["family allowance", "exempt property", "surviving spouse", "children", "probate", "PRB08"],
        conclusion_template="The surviving spouse and minor children are entitled to a reasonable family allowance and exempt property, which have priority over most creditors.",
        reasoning_framework=(
            "PRB08 law provides for a family allowance and exempt property to protect the decedent's dependents. "
            "The allowance is intended to provide for immediate needs during estate administration. "
            "Exempt property includes household goods, personal effects, and a vehicle up to a statutory value. "
            "These rights are superior to most unsecured claims, but may be subordinate to secured claims and certain statutory liens. "
            "The amount and duration of the allowance are set by statute and may be adjusted by the court for hardship. "
            "The personal representative must set aside exempt property and pay the allowance before distributing to general creditors. "
            "Disputes are resolved by motion and hearing. "
            "If the estate is insolvent, the allowance and exempt property are paid pro rata with other priority claims."
        ),
        key_factors=[
            "Relationship to decedent",
            "Statutory limits on value",
            "Estate solvency",
            "Existence of secured claims"
        ],
        primary_authority=[
            "PRB08 § 2-403",
            "PRB08 § 2-404",
            "In re Estate of Lee, 132 P.3d 567 (PRB08 2008)"
        ],
        burden_holder="Surviving Spouse or Minor Children",
        adversary_position="Creditors may challenge eligibility or amount",
        counter_arguments=[
            "Claimant is not a dependent",
            "Property exceeds statutory limits",
            "Estate is insolvent"
        ],
        resolution_strategy="Court applies statutory limits and priorities; may adjust for hardship.",
        entity_scope="Surviving Spouse, Minor Children, Personal Representatives",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="In re Estate of Lee, 132 P.3d 567 (PRB08 2008)"
    ),
    DoctrineBlock(
        topic="Insolvent Estate Administration and Abatement",
        keywords=["insolvent estate", "administration", "abatement", "priority", "probate", "PRB08"],
        conclusion_template="If the estate is insolvent, claims and distributions abate in the order of statutory priority.",
        reasoning_framework=(
            "When the estate's assets are insufficient to pay all claims, PRB08 law prescribes an order of abatement. "
            "Priority claims, such as administrative expenses, funeral costs, and family allowances, are paid first. "
            "Lower-priority claims are paid only if higher-priority claims are satisfied. "
            "If assets are insufficient within a class, claims abate proportionally. "
            "Devises and bequests abate after claims are paid, in the order of residuary, general, and specific bequests. "
            "The court may adjust abatement to honor the decedent's intent if clearly expressed in the will. "
            "Creditors may petition for an accounting and abatement order. "
            "The personal representative must follow statutory priorities and obtain court approval for distributions in insolvency."
        ),
        key_factors=[
            "Amount of estate assets",
            "Classification of claims",
            "Order of abatement",
            "Decedent's intent in will"
        ],
        primary_authority=[
            "PRB08 § 3-902",
            "PRB08 § 3-805",
            "Estate of Franklin, 188 P.3d 321 (PRB08 2012)"
        ],
        burden_holder="Personal Representative",
        adversary_position="Creditors or beneficiaries may challenge abatement order",
        counter_arguments=[
            "Improper classification of claim",
            "Deviation from statutory order",
            "Will expresses different intent"
        ],
        resolution_strategy="Court reviews abatement order for compliance with statute and will.",
        entity_scope="Personal Representatives, Creditors, Beneficiaries",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Estate of Franklin, 188 P.3d 321 (PRB08 2012)"
    ),
    DoctrineBlock(
        topic="Nonclaim Statute - Two-Year Absolute Bar",
        keywords=["nonclaim statute", "two-year bar", "statute of limitations", "probate", "PRB08"],
        conclusion_template="All claims against the estate are absolutely barred two years after the decedent's death, regardless of notice.",
        reasoning_framework=(
            "The nonclaim statute in PRB08 imposes an absolute two-year bar on all claims against the estate. "
            "This period runs from the date of death, not from the opening of probate or notice to creditors. "
            "The purpose is to provide finality and certainty in estate administration. "
            "No exceptions are made for lack of notice, fraud, or concealment. "
            "Claims not presented within two years are forever barred, and the court lacks jurisdiction to allow them. "
            "This bar applies to all claims, including those of the state and federal government, except for certain tax claims. "
            "The personal representative should verify the date of death and reject any late claims. "
            "Creditors may not seek equitable relief to avoid the bar. "
            "The statute is strictly construed, and courts have no discretion to extend the period."
        ),
        key_factors=[
            "Date of decedent's death",
            "Date claim is presented",
            "Nature of claim"
        ],
        primary_authority=[
            "PRB08 § 3-803(c)",
            "Estate of Harris, 212 P.3d 789 (PRB08 2013)"
        ],
        burden_holder="Creditor",
        adversary_position="Personal representative asserts the two-year bar",
        counter_arguments=[
            "Claim is not subject to nonclaim statute",
            "Claim was presented within two years"
        ],
        resolution_strategy="Strict application of two-year bar; court dismisses untimely claims.",
        entity_scope="All Creditors, Personal Representatives",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="Estate of Harris, 212 P.3d 789 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Contingent and Unliquidated Claims",
        keywords=["contingent claims", "unliquidated claims", "probate", "PRB08", "future liability"],
        conclusion_template="Contingent and unliquidated claims must be presented within the claims period and are allowed if liability becomes fixed.",
        reasoning_framework=(
            "PRB08 recognizes the right of creditors to present contingent or unliquidated claims against the estate. "
            "A contingent claim depends on the occurrence of a future event; an unliquidated claim is one where the amount is not yet determined. "
            "Such claims must be presented within the statutory claims period, even if the contingency is unresolved. "
            "The personal representative may allow, compromise, or reject the claim. "
            "If the claim becomes absolute before distribution, it is paid as any other claim. "
            "If the contingency is unresolved, the court may order the representative to retain assets or require the creditor to post a bond. "
            "Failure to present the claim within the period bars recovery. "
            "The court has discretion to determine the value of unliquidated claims for distribution purposes."
        ),
        key_factors=[
            "Nature of contingency",
            "Timeliness of presentation",
            "Likelihood of liability becoming fixed",
            "Estate solvency"
        ],
        primary_authority=[
            "PRB08 § 3-804",
            "Estate of Daniels, 176 P.3d 678 (PRB08 2010)"
        ],
        burden_holder="Creditor",
        adversary_position="Personal representative may challenge validity or value",
        counter_arguments=[
            "Claim is speculative or remote",
            "Claim was not timely presented"
        ],
        resolution_strategy="Court may estimate value or require retention of assets; applies statutory deadlines.",
        entity_scope="Creditors with Contingent or Unliquidated Claims, Personal Representatives",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Estate of Daniels, 176 P.3d 678 (PRB08 2010)"
    ),
    DoctrineBlock(
        topic="Personal Representative Liability for Improper Payments",
        keywords=["personal representative", "liability", "improper payment", "probate", "PRB08"],
        conclusion_template="A personal representative is personally liable for improper payment of claims if made in bad faith or without statutory authority.",
        reasoning_framework=(
            "The personal representative has a fiduciary duty to pay claims in the order and manner prescribed by law. "
            "Improper payment, such as paying lower-priority claims before higher-priority ones, may result in personal liability. "
            "Liability attaches if the payment was made in bad faith, with gross negligence, or in disregard of statutory priorities. "
            "Good faith reliance on court orders or legal advice may provide a defense. "
            "Beneficiaries or unpaid creditors may sue the representative for breach of duty. "
            "The court may surcharge the representative or order restitution. "
            "The representative should document all payments and seek court approval in cases of doubt."
        ),
        key_factors=[
            "Order of payment",
            "Good faith of representative",
            "Existence of court approval",
            "Documentation of payments"
        ],
        primary_authority=[
            "PRB08 § 3-808",
            "In re Estate of Miller, 154 P.3d 432 (PRB08 2006)"
        ],
        burden_holder="Beneficiary or Creditor",
        adversary_position="Representative may assert good faith or court approval",
        counter_arguments=[
            "Payment was made in good faith",
            "Court approved the payment",
            "No harm resulted"
        ],
        resolution_strategy="Court determines liability based on statutory compliance and good faith.",
        entity_scope="Personal Representatives, Creditors, Beneficiaries",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="In re Estate of Miller, 154 P.3d 432 (PRB08 2006)"
    ),
    DoctrineBlock(
        topic="Federal Tax Lien Priority Over Probate Claims",
        keywords=["federal tax lien", "priority", "probate", "IRS", "PRB08", "tax claims"],
        conclusion_template="Federal tax liens have priority over most probate claims, except for certain administrative expenses and family allowances.",
        reasoning_framework=(
            "Federal law preempts state probate law regarding the priority of federal tax liens. "
            "A properly filed federal tax lien attaches to all estate property and takes priority over most claims, including unsecured creditors. "
            "Certain administrative expenses and family allowances may have limited priority under federal law. "
            "The personal representative must satisfy federal tax liens before distributing assets to lower-priority claimants. "
            "Failure to do so may result in personal liability to the IRS. "
            "Disputes over the amount or validity of the lien are resolved in federal court. "
            "The representative should consult with the IRS and obtain a release before final distribution."
        ),
        key_factors=[
            "Date and validity of tax lien filing",
            "Nature of competing claims",
            "Federal preemption",
            "Estate solvency"
        ],
        primary_authority=[
            "26 U.S.C. § 6321",
            "PRB08 § 3-805",
            "United States v. Estate of Romani, 523 U.S. 517 (1998)"
        ],
        burden_holder="Personal Representative",
        adversary_position="Other creditors may challenge priority or amount",
        counter_arguments=[
            "Lien was not properly filed",
            "Claim qualifies for administrative expense priority",
            "Estate is insolvent"
        ],
        resolution_strategy="Apply federal priority rules; consult IRS for lien satisfaction and release.",
        entity_scope="Personal Representatives, IRS, Creditors",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="United States v. Estate of Romani, 523 U.S. 517 (1998)"
    ),
    DoctrineBlock(
        topic="Medicaid Estate Recovery Claims",
        keywords=["medicaid", "estate recovery", "claims", "probate", "PRB08", "public assistance"],
        conclusion_template="State Medicaid estate recovery claims are allowed but subordinate to administrative expenses, funeral costs, and family allowances.",
        reasoning_framework=(
            "Federal and state law require recovery of Medicaid benefits paid to the decedent from the estate. "
            "The state must present its claim within the statutory claims period. "
            "Medicaid recovery claims are classified below administrative expenses, funeral costs, and family allowances. "
            "The personal representative must pay higher-priority claims first. "
            "If the estate is insolvent, Medicaid may recover only a pro rata share. "
            "The state may not recover from exempt property or assets passing outside probate. "
            "Disputes over the amount or validity of the claim are resolved by the probate court."
        ),
        key_factors=[
            "Timeliness of Medicaid claim",
            "Estate solvency",
            "Classification of claim",
            "Nature of assets"
        ],
        primary_authority=[
            "42 U.S.C. § 1396p(b)",
            "PRB08 § 3-805",
            "Estate of Williams, 199 P.3d 345 (PRB08 2012)"
        ],
        burden_holder="State Medicaid Agency",
        adversary_position="Personal representative may challenge amount or classification",
        counter_arguments=[
            "Claim is untimely",
            "Assets are exempt or non-probate",
            "Higher-priority claims exhaust estate"
        ],
        resolution_strategy="Apply statutory priority; court determines amount and classification.",
        entity_scope="State Medicaid Agency, Personal Representatives",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Estate of Williams, 199 P.3d 345 (PRB08 2012)"
    ),
    DoctrineBlock(
        topic="Claim Rejection and Lawsuit Requirements",
        keywords=["claim rejection", "lawsuit", "probate", "PRB08", "creditor remedies"],
        conclusion_template="A creditor whose claim is rejected must file suit within 60 days or the claim is barred.",
        reasoning_framework=(
            "If the personal representative rejects a claim, the creditor must initiate a lawsuit within the statutory period, usually 60 days from notice of rejection. "
            "Failure to file suit results in the claim being forever barred. "
            "The representative must provide written notice of rejection, stating the reasons and the deadline for suit. "
            "The 60-day period is strictly enforced. "
            "If the creditor files suit timely, the court will adjudicate the claim on the merits. "
            "If the representative fails to give proper notice of rejection, the bar may not apply. "
            "The burden is on the creditor to show timely filing."
        ),
        key_factors=[
            "Date and sufficiency of rejection notice",
            "Timeliness of lawsuit",
            "Content of notice",
            "Creditor diligence"
        ],
        primary_authority=[
            "PRB08 § 3-806",
            "Estate of Nelson, 178 P.3d 567 (PRB08 2011)"
        ],
        burden_holder="Creditor",
        adversary_position="Personal representative may assert claim is barred",
        counter_arguments=[
            "Notice of rejection was defective",
            "Suit was filed within 60 days",
            "Equitable tolling applies"
        ],
        resolution_strategy="Strict enforcement of 60-day deadline; exceptions for defective notice.",
        entity_scope="Creditors, Personal Representatives",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Estate of Nelson, 178 P.3d 567 (PRB08 2011)"
    ),
    DoctrineBlock(
        topic="Child Support Arrearages as Priority Claims",
        keywords=["child support", "arrearages", "priority", "probate", "PRB08", "support claims"],
        conclusion_template="Child support arrearages are classified as priority claims and must be paid before general unsecured creditors.",
        reasoning_framework=(
            "PRB08 law recognizes past-due child support as a priority claim in probate. "
            "The state or custodial parent must present the claim within the statutory period. "
            "The amount is determined by court order or arrearage statement. "
            "Child support claims are paid after administrative expenses and funeral costs, but before general unsecured debts. "
            "If the estate is insolvent, child support claims are paid pro rata with other priority claims. "
            "The personal representative must verify the amount and classification before payment."
        ),
        key_factors=[
            "Existence of court order for support",
            "Amount of arrearage",
            "Timeliness of claim",
            "Estate solvency"
        ],
        primary_authority=[
            "PRB08 § 3-805(a)(3)",
            "PRB08 § 3-803",
            "Estate of Garcia, 190 P.3d 567 (PRB08 2013)"
        ],
        burden_holder="State or Custodial Parent",
        adversary_position="Personal representative may challenge amount or classification",
        counter_arguments=[
            "Claim is not supported by court order",
            "Claim is untimely",
            "Estate is insolvent"
        ],
        resolution_strategy="Court verifies amount and classification; applies statutory priority.",
        entity_scope="State, Custodial Parents, Personal Representatives",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Estate of Garcia, 190 P.3d 567 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Classification Disputes Among Creditors",
        keywords=["classification", "disputes", "creditors", "priority", "probate", "PRB08"],
        conclusion_template="Disputes over claim classification are resolved by the court based on statutory definitions and evidence.",
        reasoning_framework=(
            "Creditors may dispute the classification of their claims to obtain higher priority. "
            "The court examines the nature of the claim, supporting documents, and statutory definitions. "
            "The burden is on the creditor seeking higher priority to prove entitlement. "
            "The personal representative must provide a classification schedule and justification. "
            "The court may hold a hearing and allow discovery. "
            "Decisions are based on the substance of the claim, not labels used by the parties. "
            "Appeals are allowed from classification orders."
        ),
        key_factors=[
            "Nature and documentation of claim",
            "Statutory definitions",
            "Evidence presented",
            "Procedural compliance"
        ],
        primary_authority=[
            "PRB08 § 3-805",
            "Estate of Brown, 175 P.3d 234 (PRB08 2010)"
        ],
        burden_holder="Creditor seeking higher priority",
        adversary_position="Personal representative or other creditors may oppose reclassification",
        counter_arguments=[
            "Claim does not meet statutory criteria",
            "Improper documentation",
            "Classification is supported by evidence"
        ],
        resolution_strategy="Court holds hearing and applies statutory definitions to evidence.",
        entity_scope="Creditors, Personal Representatives",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Estate of Brown, 175 P.3d 234 (PRB08 2010)"
    ),
    DoctrineBlock(
        topic="Setoff and Recoupment Against Estate Claims",
        keywords=["setoff", "recoupment", "estate claims", "probate", "PRB08", "counterclaim"],
        conclusion_template="A creditor may assert setoff or recoupment against the estate to reduce or extinguish its liability.",
        reasoning_framework=(
            "Setoff and recoupment are equitable defenses allowing a creditor to reduce the amount owed to the estate by amounts the estate owes to the creditor. "
            "Setoff applies to mutual debts arising before death; recoupment applies to claims arising from the same transaction. "
            "The creditor must assert the defense in a timely manner, usually in response to a claim by the estate. "
            "The court will determine the validity and amount of setoff or recoupment. "
            "Statutory and equitable limitations apply, and the defense may not be used to circumvent the claims period."
        ),
        key_factors=[
            "Existence of mutual debts",
            "Same transaction requirement",
            "Timeliness of assertion",
            "Statutory limitations"
        ],
        primary_authority=[
            "PRB08 § 3-810",
            "Estate of Evans, 183 P.3d 789 (PRB08 2011)"
        ],
        burden_holder="Creditor asserting setoff or recoupment",
        adversary_position="Personal representative may challenge applicability or amount",
        counter_arguments=[
            "Debts are not mutual or arise from different transactions",
            "Assertion is untimely",
            "Statutory bar applies"
        ],
        resolution_strategy="Court determines validity and amount; applies statutory and equitable principles.",
        entity_scope="Creditors, Personal Representatives",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Estate of Evans, 183 P.3d 789 (PRB08 2011)"
    ),
    # Additional 25+ DoctrineBlocks with real content, as required for 40+ total
    DoctrineBlock(
        topic="Presentment of Claims - Manner and Form",
        keywords=["presentment", "claims", "form", "probate", "PRB08"],
        conclusion_template="A creditor must present a claim in writing, stating the amount and basis, to the personal representative or file with the court.",
        reasoning_framework=(
            "PRB08 requires that all claims against the estate be presented in writing. "
            "The claim must state the amount, the basis for the claim, and be signed by the creditor or authorized agent. "
            "Claims may be delivered or mailed to the personal representative, or filed with the probate court. "
            "Oral claims or informal notices are insufficient. "
            "The personal representative is not required to pay or consider claims not properly presented. "
            "The court may allow amendment of defective claims if no prejudice results."
        ),
        key_factors=[
            "Written form",
            "Content of claim",
            "Timely delivery or filing",
            "Signature of creditor"
        ],
        primary_authority=[
            "PRB08 § 3-804",
            "Estate of Parker, 184 P.3d 456 (PRB08 2010)"
        ],
        burden_holder="Creditor",
        adversary_position="Personal representative may assert claim is defective",
        counter_arguments=[
            "Substantial compliance with form requirements",
            "No prejudice to estate",
            "Amendment allowed by court"
        ],
        resolution_strategy="Court may allow amendment; strict compliance preferred.",
        entity_scope="Creditors, Personal Representatives",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Estate of Parker, 184 P.3d 456 (PRB08 2010)"
    ),
    DoctrineBlock(
        topic="Late Claims - Court Discretion to Allow",
        keywords=["late claims", "court discretion", "probate", "PRB08", "equitable relief"],
        conclusion_template="The court may allow a late claim if the creditor shows excusable neglect and no prejudice to the estate.",
        reasoning_framework=(
            "While PRB08 imposes strict deadlines, the court has limited discretion to allow late claims. "
            "The creditor must show excusable neglect, mistake, or other equitable grounds. "
            "The court considers whether the estate or beneficiaries would be prejudiced by allowing the claim. "
            "If the statutory bar has passed, the court's discretion is limited. "
            "The personal representative may oppose late claims to protect the estate. "
            "The court's decision is reviewed for abuse of discretion."
        ),
        key_factors=[
            "Reason for delay",
            "Prejudice to estate",
            "Timeliness of motion",
            "Good faith of creditor"
        ],
        primary_authority=[
            "PRB08 § 3-803(b)",
            "Estate of Allen, 191 P.3d 789 (PRB08 2012)"
        ],
        burden_holder="Creditor",
        adversary_position="Personal representative may assert prejudice or lack of excusable neglect",
        counter_arguments=[
            "Creditor acted in good faith",
            "No prejudice to estate",
            "Delay was minimal"
        ],
        resolution_strategy="Court balances equities; applies statutory limits.",
        entity_scope="Creditors, Personal Representatives",
        confidence=0.87,
        confidence_zone="Moderate",
        controlling_precedent="Estate of Allen, 191 P.3d 789 (PRB08 2012)"
    ),
    DoctrineBlock(
        topic="Administrative Expenses - Priority and Payment",
        keywords=["administrative expenses", "priority", "payment", "probate", "PRB08"],
        conclusion_template="Administrative expenses have top priority and must be paid before all other claims.",
        reasoning_framework=(
            "Administrative expenses, such as court costs, attorney fees, and personal representative compensation, are given the highest priority in probate. "
            "These expenses are necessary for the proper administration of the estate. "
            "The personal representative must pay administrative expenses before funeral costs, family allowances, or creditor claims. "
            "The court may review and approve the amount and necessity of such expenses. "
            "Disputes are resolved by motion and hearing."
        ),
        key_factors=[
            "Nature of expense",
            "Necessity for administration",
            "Court approval",
            "Estate solvency"
        ],
        primary_authority=[
            "PRB08 § 3-805(a)(1)",
            "Estate of Turner, 186 P.3d 234 (PRB08 2011)"
        ],
        burden_holder="Personal Representative",
        adversary_position="Creditors or beneficiaries may challenge amount or necessity",
        counter_arguments=[
            "Expense is excessive or unnecessary",
            "Improper classification",
            "Lack of court approval"
        ],
        resolution_strategy="Court reviews and approves administrative expenses.",
        entity_scope="Personal Representatives, Creditors, Beneficiaries",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Estate of Turner, 186 P.3d 234 (PRB08 2011)"
    ),
    DoctrineBlock(
        topic="Claims for Tort Liability Against Estate",
        keywords=["tort claims", "liability", "probate", "PRB08", "personal injury"],
        conclusion_template="Tort claims against the decedent must be presented within the claims period and are treated as general unsecured claims.",
        reasoning_framework=(
            "Claims for personal injury, wrongful death, or other torts against the decedent survive death and may be asserted against the estate. "
            "Such claims must be presented in the same manner and within the same period as other claims. "
            "Tort claims are classified as general unsecured claims unless a judgment or lien exists. "
            "The personal representative may compromise or defend the claim. "
            "The court may require proof of liability and damages before allowing payment."
        ),
        key_factors=[
            "Timeliness of claim",
            "Proof of liability and damages",
            "Existence of judgment or lien",
            "Estate solvency"
        ],
        primary_authority=[
            "PRB08 § 3-804",
            "Estate of Young, 193 P.3d 345 (PRB08 2013)"
        ],
        burden_holder="Tort Claimant",
        adversary_position="Personal representative may challenge liability or amount",
        counter_arguments=[
            "Claim is speculative or unsupported",
            "Claim is untimely",
            "Estate is insolvent"
        ],
        resolution_strategy="Court requires proof and applies statutory deadlines.",
        entity_scope="Tort Claimants, Personal Representatives",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Estate of Young, 193 P.3d 345 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Interest on Allowed Claims",
        keywords=["interest", "allowed claims", "probate", "PRB08", "payment"],
        conclusion_template="Interest on allowed claims accrues only to the extent permitted by statute and the estate's solvency.",
        reasoning_framework=(
            "PRB08 limits the accrual of interest on claims against the estate. "
            "Interest may accrue up to the date of death, and post-death interest is allowed only if the estate is solvent and after all principal claims are paid. "
            "The rate and period of interest are governed by statute or contract. "
            "The personal representative must calculate and pay interest only as allowed by law. "
            "Disputes are resolved by the court."
        ),
        key_factors=[
            "Statutory or contractual rate",
            "Estate solvency",
            "Date of death",
            "Classification of claim"
        ],
        primary_authority=[
            "PRB08 § 3-805(c)",
            "Estate of Foster, 187 P.3d 234 (PRB08 2012)"
        ],
        burden_holder="Creditor",
        adversary_position="Personal representative may challenge rate or period",
        counter_arguments=[
            "Interest is not allowed post-death",
            "Estate is insolvent",
            "Statute limits interest"
        ],
        resolution_strategy="Court applies statutory limits and estate solvency test.",
        entity_scope="Creditors, Personal Representatives",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Estate of Foster, 187 P.3d 234 (PRB08 2012)"
    ),
    DoctrineBlock(
        topic="Claims Based on Unenforceable Contracts",
        keywords=["unenforceable contracts", "claims", "probate", "PRB08", "statute of frauds"],
        conclusion_template="Claims based on unenforceable contracts are disallowed unless validated by statute or equity.",
        reasoning_framework=(
            "A claim against the estate based on an unenforceable contract, such as one barred by the statute of frauds or illegality, will generally be disallowed. "
            "The court may allow the claim if statutory or equitable grounds exist, such as part performance or unjust enrichment. "
            "The personal representative may challenge the validity of the contract. "
            "The burden is on the claimant to prove enforceability."
        ),
        key_factors=[
            "Validity of contract",
            "Statutory or equitable exceptions",
            "Proof of performance",
            "Nature of claim"
        ],
        primary_authority=[
            "PRB08 § 3-804",
            "Estate of Adams, 185 P.3d 789 (PRB08 2011)"
        ],
        burden_holder="Claimant",
        adversary_position="Personal representative may assert contract is unenforceable",
        counter_arguments=[
            "Statute of frauds applies",
            "No part performance",
            "Claim is equitable"
        ],
        resolution_strategy="Court reviews contract and applies statutory and equitable principles.",
        entity_scope="Claimants, Personal Representatives",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Estate of Adams, 185 P.3d 789 (PRB08 2011)"
    ),
    DoctrineBlock(
        topic="Claims for Services Rendered to Decedent",
        keywords=["services", "claims", "probate", "PRB08", "quantum meruit"],
        conclusion_template="Claims for services rendered to the decedent are allowed if supported by evidence of agreement or reasonable expectation of payment.",
        reasoning_framework=(
            "A person who provided services to the decedent may assert a claim for compensation. "
            "The claim must be supported by evidence of an express or implied agreement, or a reasonable expectation of payment. "
            "Family members are presumed to provide services gratuitously unless an agreement is shown. "
            "The court may allow recovery in quantum meruit if equity requires. "
            "The personal representative may challenge the claim as unsupported or excessive."
        ),
        key_factors=[
            "Existence of agreement",
            "Nature of relationship",
            "Reasonableness of charges",
            "Proof of services rendered"
        ],
        primary_authority=[
            "PRB08 § 3-804",
            "Estate of Simmons, 192 P.3d 234 (PRB08 2012)"
        ],
        burden_holder="Service Provider",
        adversary_position="Personal representative may assert services were gratuitous",
        counter_arguments=[
            "No agreement or expectation of payment",
            "Charges are excessive",
            "Services were for family"
        ],
        resolution_strategy="Court reviews evidence and applies quantum meruit principles.",
        entity_scope="Service Providers, Personal Representatives",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Estate of Simmons, 192 P.3d 234 (PRB08 2012)"
    ),
    DoctrineBlock(
        topic="Claims for Rent and Lease Obligations",
        keywords=["rent", "lease", "claims", "probate", "PRB08", "landlord"],
        conclusion_template="Claims for unpaid rent or lease obligations are allowed as general unsecured claims if presented timely.",
        reasoning_framework=(
            "A landlord may assert a claim for unpaid rent or lease obligations incurred by the decedent. "
            "The claim must be presented within the statutory period and is classified as a general unsecured claim. "
            "The court may allow the claim for rent accrued before death and for damages resulting from early termination. "
            "The personal representative may challenge the amount or classification."
        ),
        key_factors=[
            "Existence of lease",
            "Amount of unpaid rent",
            "Timeliness of claim",
            "Damages for early termination"
        ],
        primary_authority=[
            "PRB08 § 3-804",
            "Estate of Clark, 194 P.3d 567 (PRB08 2013)"
        ],
        burden_holder="Landlord",
        adversary_position="Personal representative may challenge amount or classification",
        counter_arguments=[
            "Claim is excessive",
            "Lease was terminated",
            "Claim is untimely"
        ],
        resolution_strategy="Court reviews lease and applies statutory deadlines.",
        entity_scope="Landlords, Personal Representatives",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Estate of Clark, 194 P.3d 567 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Claims for Taxes Owed by Decedent",
        keywords=["taxes", "claims", "probate", "PRB08", "IRS", "state tax"],
        conclusion_template="Claims for taxes owed by the decedent are allowed as priority claims and must be paid before general creditors.",
        reasoning_framework=(
            "Federal, state, and local tax claims are given priority in probate. "
            "The personal representative must ascertain all tax liabilities of the decedent and the estate. "
            "Tax claims must be paid before distribution to general creditors. "
            "Disputes over the amount or validity of tax claims are resolved by the probate or tax court. "
            "The representative may be personally liable for failure to pay taxes."
        ),
        key_factors=[
            "Type and amount of tax",
            "Timeliness of claim",
            "Estate solvency",
            "Court orders"
        ],
        primary_authority=[
            "PRB08 § 3-805(a)(2)",
            "26 U.S.C. § 2002",
            "Estate of Martin, 195 P.3d 789 (PRB08 2013)"
        ],
        burden_holder="Tax Authority",
        adversary_position="Personal representative may challenge amount or classification",
        counter_arguments=[
            "Claim is excessive",
            "Tax was paid",
            "Claim is untimely"
        ],
        resolution_strategy="Court applies statutory priority and reviews tax assessments.",
        entity_scope="Tax Authorities, Personal Representatives",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Estate of Martin, 195 P.3d 789 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Claims for Medical Expenses",
        keywords=["medical expenses", "claims", "probate", "PRB08", "healthcare"],
        conclusion_template="Claims for unpaid medical expenses incurred before death are allowed as general unsecured claims.",
        reasoning_framework=(
            "Healthcare providers may assert claims for unpaid medical expenses incurred by the decedent before death. "
            "Such claims must be presented within the statutory period and are classified as general unsecured claims. "
            "The personal representative may challenge the amount or necessity of the charges. "
            "The court may require proof of services and reasonableness of charges."
        ),
        key_factors=[
            "Proof of services rendered",
            "Amount of charges",
            "Timeliness of claim",
            "Reasonableness of charges"
        ],
        primary_authority=[
            "PRB08 § 3-804",
            "Estate of Baker, 196 P.3d 234 (PRB08 2013)"
        ],
        burden_holder="Healthcare Provider",
        adversary_position="Personal representative may challenge amount or necessity",
        counter_arguments=[
            "Charges are excessive",
            "Services were not rendered",
            "Claim is untimely"
        ],
        resolution_strategy="Court reviews evidence and applies statutory deadlines.",
        entity_scope="Healthcare Providers, Personal Representatives",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Estate of Baker, 196 P.3d 234 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Claims for Attorney Fees",
        keywords=["attorney fees", "claims", "probate", "PRB08", "legal services"],
        conclusion_template="Claims for attorney fees for services to the estate are allowed as administrative expenses with top priority.",
        reasoning_framework=(
            "Attorneys who provide services to the estate may assert claims for reasonable fees as administrative expenses. "
            "Such claims have top priority and must be paid before other creditors. "
            "The court reviews the reasonableness and necessity of the fees. "
            "Disputes are resolved by motion and hearing."
        ),
        key_factors=[
            "Reasonableness of fees",
            "Necessity of services",
            "Court approval",
            "Estate solvency"
        ],
        primary_authority=[
            "PRB08 § 3-805(a)(1)",
            "Estate of Johnson, 197 P.3d 456 (PRB08 2013)"
        ],
        burden_holder="Attorney",
        adversary_position="Personal representative or beneficiaries may challenge amount",
        counter_arguments=[
            "Fees are excessive",
            "Services were unnecessary",
            "Lack of court approval"
        ],
        resolution_strategy="Court reviews and approves fees as administrative expenses.",
        entity_scope="Attorneys, Personal Representatives",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Estate of Johnson, 197 P.3d 456 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Claims for Debts Secured by Real Property",
        keywords=["secured debts", "real property", "probate", "PRB08", "mortgage"],
        conclusion_template="Debts secured by real property are paid from the property or proceeds before general estate assets.",
        reasoning_framework=(
            "A mortgage or other debt secured by real property is satisfied from the property or its sale proceeds. "
            "The secured creditor may foreclose or require payment before the property is distributed. "
            "If the estate wishes to retain the property, it must pay the secured debt in full. "
            "Deficiency claims are treated as unsecured claims. "
            "The court may supervise the sale or payment of secured debts."
        ),
        key_factors=[
            "Existence and validity of security interest",
            "Value of property",
            "Amount of debt",
            "Estate's intent to retain or sell"
        ],
        primary_authority=[
            "PRB08 § 3-806",
            "Estate of Reed, 198 P.3d 789 (PRB08 2013)"
        ],
        burden_holder="Secured Creditor",
        adversary_position="Personal representative may challenge validity or amount",
        counter_arguments=[
            "Security interest is invalid",
            "Debt was paid",
            "Property is over-encumbered"
        ],
        resolution_strategy="Court supervises payment or sale; applies statutory priority.",
        entity_scope="Secured Creditors, Personal Representatives",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Estate of Reed, 198 P.3d 789 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Claims for Credit Card Debt",
        keywords=["credit card", "debt", "claims", "probate", "PRB08"],
        conclusion_template="Credit card debt is allowed as a general unsecured claim if presented timely and supported by documentation.",
        reasoning_framework=(
            "Credit card issuers may assert claims for unpaid balances. "
            "The claim must be presented within the statutory period and supported by account statements or contracts. "
            "Such claims are classified as general unsecured debts. "
            "The personal representative may challenge the amount or validity. "
            "The court may require proof of indebtedness."
        ),
        key_factors=[
            "Proof of debt",
            "Timeliness of claim",
            "Documentation",
            "Estate solvency"
        ],
        primary_authority=[
            "PRB08 § 3-804",
            "Estate of Carter, 199 P.3d 234 (PRB08 2013)"
        ],
        burden_holder="Credit Card Issuer",
        adversary_position="Personal representative may challenge amount or validity",
        counter_arguments=[
            "Debt is not supported by documentation",
            "Claim is untimely",
            "Debt was paid"
        ],
        resolution_strategy="Court reviews documentation and applies statutory deadlines.",
        entity_scope="Credit Card Issuers, Personal Representatives",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Estate of Carter, 199 P.3d 234 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Claims for Business Debts",
        keywords=["business debts", "claims", "probate", "PRB08", "commercial obligations"],
        conclusion_template="Business debts incurred by the decedent are allowed as general unsecured claims if presented timely.",
        reasoning_framework=(
            "Creditors may assert claims for business debts or commercial obligations incurred by the decedent. "
            "Such claims must be presented within the statutory period and are classified as general unsecured claims. "
            "The personal representative may challenge the amount, validity, or classification. "
            "The court may require proof of indebtedness and business records."
        ),
        key_factors=[
            "Proof of debt",
            "Timeliness of claim",
            "Nature of business obligation",
            "Estate solvency"
        ],
        primary_authority=[
            "PRB08 § 3-804",
            "Estate of Morris, 200 P.3d 567 (PRB08 2013)"
        ],
        burden_holder="Business Creditor",
        adversary_position="Personal representative may challenge amount or validity",
        counter_arguments=[
            "Debt is not supported by records",
            "Claim is untimely",
            "Debt was paid"
        ],
        resolution_strategy="Court reviews business records and applies statutory deadlines.",
        entity_scope="Business Creditors, Personal Representatives",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Estate of Morris, 200 P.3d 567 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Claims for Loans Made to Decedent",
        keywords=["loans", "claims", "probate", "PRB08", "promissory note"],
        conclusion_template="Claims for loans made to the decedent are allowed if supported by promissory notes or other evidence of indebtedness.",
        reasoning_framework=(
            "A lender may assert a claim for repayment of loans made to the decedent. "
            "The claim must be supported by promissory notes, loan agreements, or other evidence of indebtedness. "
            "The claim must be presented within the statutory period. "
            "The personal representative may challenge the validity or amount. "
            "The court may require proof of loan and payment history."
        ),
        key_factors=[
            "Existence of promissory note",
            "Proof of loan",
            "Timeliness of claim",
            "Payment history"
        ],
        primary_authority=[
            "PRB08 § 3-804",
            "Estate of Hall, 201 P.3d 789 (PRB08 2013)"
        ],
        burden_holder="Lender",
        adversary_position="Personal representative may challenge validity or amount",
        counter_arguments=[
            "No evidence of loan",
            "Claim is untimely",
            "Loan was repaid"
        ],
        resolution_strategy="Court reviews loan documents and applies statutory deadlines.",
        entity_scope="Lenders, Personal Representatives",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Estate of Hall, 201 P.3d 789 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Claims for Guaranty Obligations",
        keywords=["guaranty", "obligations", "claims", "probate", "PRB08"],
        conclusion_template="A creditor may assert a claim for a guaranty obligation signed by the decedent if liability is established.",
        reasoning_framework=(
            "A creditor may assert a claim for payment under a guaranty signed by the decedent. "
            "The creditor must establish the existence and validity of the guaranty, and that the primary obligor defaulted. "
            "The claim must be presented within the statutory period. "
            "The personal representative may challenge the validity or amount. "
            "The court may require proof of default and notice."
        ),
        key_factors=[
            "Existence and validity of guaranty",
            "Default by primary obligor",
            "Timeliness of claim",
            "Notice to guarantor"
        ],
        primary_authority=[
            "PRB08 § 3-804",
            "Estate of King, 202 P.3d 456 (PRB08 2013)"
        ],
        burden_holder="Creditor",
        adversary_position="Personal representative may challenge validity or amount",
        counter_arguments=[
            "No default by primary obligor",
            "Guaranty is invalid",
            "Claim is untimely"
        ],
        resolution_strategy="Court reviews guaranty and proof of default.",
        entity_scope="Creditors, Personal Representatives",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Estate of King, 202 P.3d 456 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Claims for Court Judgments Against Decedent",
        keywords=["court judgments", "claims", "probate", "PRB08", "judgment creditor"],
        conclusion_template="A court judgment against the decedent is allowed as a claim if presented timely and not satisfied before death.",
        reasoning_framework=(
            "A judgment creditor may assert a claim for an unsatisfied judgment against the decedent. "
            "The claim must be presented within the statutory period. "
            "The judgment is classified according to its nature (secured or unsecured). "
            "The personal representative may challenge the amount or satisfaction. "
            "The court may require proof of judgment and nonpayment."
        ),
        key_factors=[
            "Existence of unsatisfied judgment",
            "Timeliness of claim",
            "Classification of judgment",
            "Proof of nonpayment"
        ],
        primary_authority=[
            "PRB08 § 3-804",
            "Estate of Wright, 203 P.3d 789 (PRB08 2013)"
        ],
        burden_holder="Judgment Creditor",
        adversary_position="Personal representative may assert judgment was satisfied",
        counter_arguments=[
            "Judgment was paid",
            "Claim is untimely",
            "Judgment is void"
        ],
        resolution_strategy="Court reviews judgment and applies statutory deadlines.",
        entity_scope="Judgment Creditors, Personal Representatives",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Estate of Wright, 203 P.3d 789 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Claims for Spousal Elective Share",
        keywords=["spousal elective share", "claims", "probate", "PRB08", "surviving spouse"],
        conclusion_template="A surviving spouse may assert a claim for the elective share within the statutory period, which has priority over most creditor claims.",
        reasoning_framework=(
            "PRB08 allows a surviving spouse to claim an elective share of the estate in lieu of the will. "
            "The claim must be asserted within the statutory period, usually six months from notice of probate. "
            "The elective share has priority over most unsecured creditor claims, but not over administrative expenses or secured debts. "
            "The court determines the amount and orders payment. "
            "The personal representative must set aside assets to satisfy the elective share."
        ),
        key_factors=[
            "Timeliness of claim",
            "Marital status",
            "Estate solvency",
            "Existence of will"
        ],
        primary_authority=[
            "PRB08 § 2-201",
            "PRB08 § 3-805",
            "Estate of Sanders, 204 P.3d 234 (PRB08 2013)"
        ],
        burden_holder="Surviving Spouse",
        adversary_position="Personal representative or creditors may challenge eligibility or amount",
        counter_arguments=[
            "Claim is untimely",
            "No valid marriage",
            "Estate is insolvent"
        ],
        resolution_strategy="Court reviews eligibility and applies statutory priority.",
        entity_scope="Surviving Spouses, Personal Representatives",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Estate of Sanders, 204 P.3d 234 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Claims for Unpaid Wages",
        keywords=["unpaid wages", "claims", "probate", "PRB08", "employee"],
        conclusion_template="Claims for unpaid wages owed by the decedent are allowed as priority claims if presented timely.",
        reasoning_framework=(
            "Employees may assert claims for unpaid wages earned before the decedent's death. "
            "Such claims are classified as priority claims under PRB08. "
            "The claim must be presented within the statutory period and supported by payroll records or employment contracts. "
            "The personal representative may challenge the amount or validity."
        ),
        key_factors=[
            "Proof of employment",
            "Amount of unpaid wages",
            "Timeliness of claim",
            "Estate solvency"
        ],
        primary_authority=[
            "PRB08 § 3-805(a)(4)",
            "Estate of Evans, 205 P.3d 567 (PRB08 2013)"
        ],
        burden_holder="Employee",
        adversary_position="Personal representative may challenge amount or validity",
        counter_arguments=[
            "No proof of employment",
            "Claim is untimely",
            "Wages were paid"
        ],
        resolution_strategy="Court reviews employment records and applies statutory deadlines.",
        entity_scope="Employees, Personal Representatives",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Estate of Evans, 205 P.3d 567 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Claims for Support of Dependents",
        keywords=["support", "dependents", "claims", "probate", "PRB08"],
        conclusion_template="Claims for support of dependents are allowed as priority claims if supported by court order or statute.",
        reasoning_framework=(
            "Dependents of the decedent may assert claims for support based on court order or statute. "
            "Such claims are classified as priority claims and must be presented within the statutory period. "
            "The personal representative may challenge the amount or eligibility. "
            "The court may require proof of dependency and support order."
        ),
        key_factors=[
            "Existence of support order",
            "Proof of dependency",
            "Timeliness of claim",
            "Estate solvency"
        ],
        primary_authority=[
            "PRB08 § 3-805(a)(3)",
            "Estate of Foster, 206 P.3d 789 (PRB08 2013)"
        ],
        burden_holder="Dependent",
        adversary_position="Personal representative may challenge eligibility or amount",
        counter_arguments=[
            "No support order",
            "Not a dependent",
            "Claim is untimely"
        ],
        resolution_strategy="Court reviews support order and applies statutory deadlines.",
        entity_scope="Dependents, Personal Representatives",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Estate of Foster, 206 P.3d 789 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Claims for Reimbursement of Funeral Expenses",
        keywords=["funeral expenses", "reimbursement", "claims", "probate", "PRB08"],
        conclusion_template="A person who paid funeral expenses may assert a claim for reimbursement as a first-priority claim.",
        reasoning_framework=(
            "A person who paid funeral expenses on behalf of the decedent may assert a claim for reimbursement from the estate. "
            "Such claims are classified as first-priority claims. "
            "The claimant must provide proof of payment and reasonableness of charges. "
            "The personal representative may challenge the amount or necessity."
        ),
        key_factors=[
            "Proof of payment",
            "Reasonableness of charges",
            "Timeliness of claim",
            "Estate solvency"
        ],
        primary_authority=[
            "PRB08 § 3-805(a)(1)",
            "Estate of Lee, 207 P.3d 234 (PRB08 2013)"
        ],
        burden_holder="Person who paid expenses",
        adversary_position="Personal representative may challenge amount or necessity",
        counter_arguments=[
            "Charges are excessive",
            "No proof of payment",
            "Claim is untimely"
        ],
        resolution_strategy="Court reviews receipts and applies statutory priority.",
        entity_scope="Funeral Expense Payers, Personal Representatives",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Estate of Lee, 207 P.3d 234 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Claims for Breach of Contract",
        keywords=["breach of contract", "claims", "probate", "PRB08"],
        conclusion_template="Claims for breach of contract are allowed as general unsecured claims if supported by evidence and presented timely.",
        reasoning_framework=(
            "A party may assert a claim for breach of contract against the estate. "
            "The claim must be supported by evidence of the contract and breach. "
            "Such claims are classified as general unsecured claims unless secured. "
            "The personal representative may challenge the validity or amount. "
            "The court may require proof of contract and damages."
        ),
        key_factors=[
            "Existence of contract",
            "Proof of breach",
            "Timeliness of claim",
            "Classification of claim"
        ],
        primary_authority=[
            "PRB08 § 3-804",
            "Estate of Harris, 208 P.3d 789 (PRB08 2013)"
        ],
        burden_holder="Claimant",
        adversary_position="Personal representative may challenge validity or amount",
        counter_arguments=[
            "No contract exists",
            "No breach occurred",
            "Claim is untimely"
        ],
        resolution_strategy="Court reviews contract and applies statutory deadlines.",
        entity_scope="Contract Claimants, Personal Representatives",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Estate of Harris, 208 P.3d 789 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Claims for Specific Performance",
        keywords=["specific performance", "claims", "probate", "PRB08"],
        conclusion_template="A claim for specific performance may be allowed if the contract is enforceable and performance is feasible.",
        reasoning_framework=(
            "A party may assert a claim for specific performance of a contract against the estate. "
            "The court will allow the claim if the contract is enforceable and performance is feasible. "
            "If performance is impossible, the court may award damages instead. "
            "The personal representative may challenge the validity or feasibility of performance."
        ),
        key_factors=[
            "Existence of enforceable contract",
            "Feasibility of performance",
            "Timeliness of claim",
            "Estate assets"
        ],
        primary_authority=[
            "PRB08 § 3-804",
            "Estate of Davis, 209 P.3d 234 (PRB08 2013)"
        ],
        burden_holder="Claimant",
        adversary_position="Personal representative may challenge validity or feasibility",
        counter_arguments=[
            "Performance is impossible",
            "Contract is unenforceable",
            "Claim is untimely"
        ],
        resolution_strategy="Court reviews contract and feasibility; may award damages.",
        entity_scope="Claimants, Personal Representatives",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Estate of Davis, 209 P.3d 234 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Claims for Contribution Among Co-Obligors",
        keywords=["contribution", "co-obligors", "claims", "probate", "PRB08"],
        conclusion_template="A co-obligor who paid more than their share may assert a claim for contribution against the estate.",
        reasoning_framework=(
            "A co-obligor who paid more than their share of a joint debt may assert a claim for contribution against the decedent's estate. "
            "The claim must be presented within the statutory period and supported by proof of payment. "
            "The personal representative may challenge the amount or necessity. "
            "The court may require proof of joint obligation and payment."
        ),
        key_factors=[
            "Existence of joint obligation",
            "Proof of payment",
            "Timeliness of claim",
            "Estate solvency"
        ],
        primary_authority=[
            "PRB08 § 3-804",
            "Estate of Brooks, 210 P.3d 567 (PRB08 2013)"
        ],
        burden_holder="Co-obligor",
        adversary_position="Personal representative may challenge amount or necessity",
        counter_arguments=[
            "No joint obligation",
            "No proof of payment",
            "Claim is untimely"
        ],
        resolution_strategy="Court reviews joint obligation and payment records.",
        entity_scope="Co-obligors, Personal Representatives",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Estate of Brooks, 210 P.3d 567 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Claims for Indemnity",
        keywords=["indemnity", "claims", "probate", "PRB08"],
        conclusion_template="A party entitled to indemnity from the decedent may assert a claim if liability is established.",
        reasoning_framework=(
            "A party entitled to indemnity from the decedent may assert a claim against the estate. "
            "The claim must be supported by contract or law, and liability must be established. "
            "The claim must be presented within the statutory period. "
            "The personal representative may challenge the validity or amount. "
            "The court may require proof of indemnity agreement and liability."
        ),
        key_factors=[
            "Existence of indemnity agreement",
            "Proof of liability",
            "Timeliness of claim",
            "Estate solvency"
        ],
        primary_authority=[
            "PRB08 § 3-804",
            "Estate of Mitchell, 211 P.3d 789 (PRB08 2013)"
        ],
        burden_holder="Indemnitee",
        adversary_position="Personal representative may challenge validity or amount",
        counter_arguments=[
            "No indemnity agreement",
            "No liability established",
            "Claim is untimely"
        ],
        resolution_strategy="Court reviews indemnity agreement and applies statutory deadlines.",
        entity_scope="Indemnitees, Personal Representatives",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Estate of Mitchell, 211 P.3d 789 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Claims for Environmental Liabilities",
        keywords=["environmental liabilities", "claims", "probate", "PRB08", "hazardous waste"],
        conclusion_template="Claims for environmental liabilities are allowed if liability is established and presented timely.",
        reasoning_framework=(
            "A party may assert a claim for environmental liabilities, such as cleanup costs, against the estate. "
            "The claim must be supported by evidence of liability under federal or state law. "
            "The claim must be presented within the statutory period. "
            "The personal representative may challenge the validity or amount. "
            "The court may require proof of liability and damages."
        ),
        key_factors=[
            "Proof of environmental liability",
            "Timeliness of claim",
            "Amount of damages",
            "Estate solvency"
        ],
        primary_authority=[
            "PRB08 § 3-804",
            "42 U.S.C. § 9607",
            "Estate of Peterson, 212 P.3d 234 (PRB08 2013)"
        ],
        burden_holder="Environmental Claimant",
        adversary_position="Personal representative may challenge liability or amount",
        counter_arguments=[
            "No liability established",
            "Claim is untimely",
            "Damages are excessive"
        ],
        resolution_strategy="Court reviews liability and applies statutory deadlines.",
        entity_scope="Environmental Claimants, Personal Representatives",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Estate of Peterson, 212 P.3d 234 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Claims for Unjust Enrichment",
        keywords=["unjust enrichment", "claims", "probate", "PRB08", "equity"],
        conclusion_template="A claim for unjust enrichment is allowed if the estate was enriched at the claimant's expense and no adequate remedy exists.",
        reasoning_framework=(
            "A party may assert a claim for unjust enrichment if the estate received a benefit at the claimant's expense and it would be inequitable to retain it. "
            "The claim must be presented within the statutory period. "
            "The personal representative may challenge the existence or value of the benefit. "
            "The court may require proof of enrichment and lack of adequate remedy at law."
        ),
        key_factors=[
            "Proof of benefit to estate",
            "Expense to claimant",
            "Timeliness of claim",
            "Lack of adequate remedy"
        ],
        primary_authority=[
            "PRB08 § 3-804",
            "Estate of Richards, 213 P.3d 567 (PRB08 2013)"
        ],
        burden_holder="Claimant",
        adversary_position="Personal representative may challenge benefit or remedy",
        counter_arguments=[
            "No benefit to estate",
            "Adequate remedy exists",
            "Claim is untimely"
        ],
        resolution_strategy="Court reviews enrichment and applies equitable principles.",
        entity_scope="Claimants, Personal Representatives",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Estate of Richards, 213 P.3d 567 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Claims for Advances Made to Decedent",
        keywords=["advances", "claims", "probate", "PRB08", "loans"],
        conclusion_template="A person who advanced funds to the decedent may assert a claim if supported by evidence of indebtedness.",
        reasoning_framework=(
            "A person who advanced funds to the decedent may assert a claim for repayment. "
            "The claim must be supported by evidence of the advance, such as checks or receipts. "
            "The claim must be presented within the statutory period. "
            "The personal representative may challenge the validity or amount. "
            "The court may require proof of advance and agreement to repay."
        ),
        key_factors=[
            "Proof of advance",
            "Agreement to repay",
            "Timeliness of claim",
            "Estate solvency"
        ],
        primary_authority=[
            "PRB08 § 3-804",
            "Estate of Bennett, 214 P.3d 234 (PRB08 2013)"
        ],
        burden_holder="Advancer",
        adversary_position="Personal representative may challenge validity or amount",
        counter_arguments=[
            "No agreement to repay",
            "Advance was a gift",
            "Claim is untimely"
        ],
        resolution_strategy="Court reviews evidence of advance and applies statutory deadlines.",
        entity_scope="Advancers, Personal Representatives",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Estate of Bennett, 214 P.3d 234 (PRB08 2013)"
    ),
    DoctrineBlock(
        topic="Claims for Lost or Destroyed Evidence",
        keywords=["lost evidence", "destroyed evidence", "claims", "probate", "PRB08"],
        conclusion_template="A claim based on lost or destroyed evidence may be allowed if the claimant proves the claim by clear and convincing evidence.",
        reasoning_framework=(
            "A claimant whose evidence