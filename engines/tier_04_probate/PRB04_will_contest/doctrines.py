import enum
import pathlib
from dataclasses import dataclass, field
from typing import List, Optional

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
        topic="testamentary_capacity_standard",
        keywords=["capacity", "testator", "mental state", "will", "competence"],
        conclusion_template="The testator {has/does not have} testamentary capacity at the time of execution.",
        reasoning_framework=(
            "Testamentary capacity requires that the testator understands the nature and extent of their property, "
            "the natural objects of their bounty, the disposition they are making, and the ability to relate these elements. "
            "Courts presume capacity, placing the burden on the contestant to prove incapacity by a preponderance of the evidence. "
            "Relevant evidence includes medical records, lay and expert testimony, and the circumstances surrounding execution. "
            "Temporary periods of lucidity (lucid intervals) are sufficient if capacity existed at the moment of execution. "
            "Mere old age, eccentricity, or physical frailty do not establish incapacity. "
            "Delusions affecting testamentary disposition may negate capacity if they materially influence the will's provisions. "
            "The standard is generally lower than contractual capacity. "
            "Capacity is assessed at the precise moment of execution, not before or after. "
            "If capacity is challenged, courts examine the testator's conduct, statements, and understanding. "
            "Expert psychiatric evidence is persuasive but not conclusive. "
            "Lay witnesses familiar with the testator may provide valuable insight. "
            "A finding of incapacity renders the will, or affected portions, invalid. "
            "If incapacity is not proven, the will stands. "
            "The contestant must present clear evidence of incapacity; the proponent need only rely on the presumption of capacity. "
            "If the evidence is evenly balanced, the presumption prevails. "
            "The court may consider the complexity of the will and the testator's involvement in its preparation. "
            "A simple will may require less capacity than a complex estate plan. "
            "Capacity is a question of fact for the trier of fact."
        ),
        key_factors=[
            "Understanding of property",
            "Awareness of natural objects of bounty",
            "Knowledge of testamentary act",
            "Ability to relate elements",
            "Presence of delusions",
            "Medical and lay evidence",
            "Timing of capacity"
        ],
        primary_authority=[
            "Uniform Probate Code § 2-501",
            "Estate of Selb, 433 P.2d 420 (Cal. 1967)",
            "Restatement (Third) of Property: Wills and Other Donative Transfers § 8.1"
        ],
        burden_holder="Will contestant",
        adversary_position="Proponent asserts presumption of capacity",
        counter_arguments=[
            "Testator was lucid at execution",
            "No evidence of delusions",
            "Lay and expert testimony support capacity"
        ],
        resolution_strategy="Weigh all evidence regarding testator's mental state at execution; apply presumption of capacity.",
        entity_scope="Individual testator",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Estate of Selb, 433 P.2d 420 (Cal. 1967)"
    ),
    DoctrineBlock(
        topic="undue_influence_standard",
        keywords=["undue influence", "coercion", "overborne will", "confidential relationship", "suspicious circumstances"],
        conclusion_template="The will {is/is not} the product of undue influence.",
        reasoning_framework=(
            "Undue influence occurs when the testator's free agency is destroyed and the resulting disposition reflects the will of another. "
            "The contestant bears the initial burden to show: (1) a confidential or fiduciary relationship, (2) active participation in procurement, and (3) suspicious circumstances. "
            "If a presumption arises, the burden shifts to the proponent to rebut it. "
            "Evidence includes the testator's vulnerability, the influencer's opportunity and disposition, and any unnatural or unexpected dispositions. "
            "Mere influence, advice, or persuasion is insufficient; the influence must be so strong as to substitute another's intent for the testator's. "
            "Indicators include secrecy, haste, isolation of the testator, and involvement in will preparation. "
            "The existence of a confidential relationship (e.g., caregiver, attorney-in-fact) heightens scrutiny. "
            "The court examines whether the testator acted voluntarily, with full knowledge and understanding. "
            "Direct evidence is rare; circumstantial evidence is often determinative. "
            "If undue influence is found, the affected provisions or the entire will may be invalidated. "
            "If not proven, the will stands. "
            "The standard of proof is typically preponderance of the evidence, but some jurisdictions require clear and convincing evidence. "
            "The court may consider the testator's susceptibility due to age, illness, or dependency. "
            "A will favoring a person in a confidential relationship, especially to the exclusion of natural heirs, is suspect. "
            "The proponent may rebut the presumption by showing independent advice or absence of suspicious circumstances."
        ),
        key_factors=[
            "Existence of confidential relationship",
            "Active procurement",
            "Suspicious circumstances",
            "Testator's vulnerability",
            "Unnatural disposition",
            "Isolation or secrecy",
            "Independent advice"
        ],
        primary_authority=[
            "Estate of Lakatosh, 441 Pa. Super. 133 (1995)",
            "Restatement (Third) of Property: Wills and Other Donative Transfers § 8.3",
            "Uniform Probate Code § 2-517"
        ],
        burden_holder="Will contestant (initially); proponent if presumption arises",
        adversary_position="Proponent asserts will reflects testator's intent",
        counter_arguments=[
            "Testator acted independently",
            "No confidential relationship",
            "Natural disposition",
            "Presence of independent legal advice"
        ],
        resolution_strategy="Analyze relationships, procurement, and circumstances; apply presumption and shifting burdens as appropriate.",
        entity_scope="Testator and alleged influencer",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Estate of Lakatosh, 441 Pa. Super. 133 (1995)"
    ),
    DoctrineBlock(
        topic="fraud_in_execution",
        keywords=["fraud", "execution", "will", "deception", "testator", "intent"],
        conclusion_template="The will {is/is not} invalid due to fraud in the execution.",
        reasoning_framework=(
            "Fraud in execution occurs when the testator is deceived about the nature or contents of the document being signed, "
            "resulting in a will that does not reflect their intent. "
            "The contestant must prove that the testator was misled as to the character of the document or its contents, "
            "and that the deception caused the execution of the will. "
            "Typical scenarios include substitution of pages, misrepresentation of the document, or concealment of material facts. "
            "The standard of proof is generally clear and convincing evidence. "
            "If fraud is established, the will or affected provisions are invalid. "
            "The court examines the circumstances of execution, the testator's understanding, and the conduct of those present. "
            "Direct evidence is rare; circumstantial evidence, such as inconsistencies or irregularities, is considered. "
            "The proponent may rebut by showing the testator read or was read the will, or had independent advice. "
            "If the testator knew and approved the contents, fraud is not established. "
            "The presence of trusted advisors or witnesses may negate claims of fraud. "
            "If fraud is not proven, the will stands."
        ),
        key_factors=[
            "Testator's understanding of document",
            "Deceptive conduct",
            "Opportunity for fraud",
            "Testator's review of will",
            "Presence of independent advice"
        ],
        primary_authority=[
            "Restatement (Third) of Property: Wills and Other Donative Transfers § 8.3",
            "In re Estate of Newhall, 190 P.2d 885 (Cal. 1948)"
        ],
        burden_holder="Will contestant",
        adversary_position="Proponent asserts testator knew and approved contents",
        counter_arguments=[
            "Testator read or was read will",
            "No evidence of deception",
            "Independent legal advice present"
        ],
        resolution_strategy="Assess evidence of deception and testator's knowledge; invalidate will if fraud proven.",
        entity_scope="Testator and alleged perpetrator",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="In re Estate of Newhall, 190 P.2d 885 (Cal. 1948)"
    ),
    DoctrineBlock(
        topic="improper_execution_formalities",
        keywords=["execution", "formalities", "will", "witnesses", "signature", "compliance"],
        conclusion_template="The will {complies/does not comply} with statutory execution formalities.",
        reasoning_framework=(
            "A valid will must comply with statutory formalities, typically requiring the testator's signature and attestation by witnesses. "
            "The number of witnesses (usually two), their presence, and the sequence of signing are critical. "
            "Substantial compliance may suffice in some jurisdictions if the testator's intent is clear. "
            "The harmless error doctrine may excuse minor defects if clear and convincing evidence shows the testator intended the document as their will. "
            "Failure to comply with essential formalities (e.g., lack of signature or witnesses) is generally fatal. "
            "The court examines the circumstances of execution, witness testimony, and the document itself. "
            "Self-proving affidavits may establish compliance. "
            "If formalities are not met, the will is invalid unless excused by statute. "
            "If compliance is found, the will is admitted to probate. "
            "Strict compliance is required in some states; others permit substantial compliance or harmless error."
        ),
        key_factors=[
            "Testator's signature",
            "Number and presence of witnesses",
            "Sequence of signing",
            "Substantial compliance",
            "Harmless error doctrine"
        ],
        primary_authority=[
            "Uniform Probate Code § 2-502",
            "Estate of Saueressig, 38 Cal. 4th 1045 (2006)"
        ],
        burden_holder="Will proponent",
        adversary_position="Contestant alleges noncompliance",
        counter_arguments=[
            "Substantial compliance with statutory requirements",
            "Harmless error doctrine applies",
            "Testator's intent is clear"
        ],
        resolution_strategy="Determine compliance with statutory requirements; consider substantial compliance or harmless error if available.",
        entity_scope="Testator and witnesses",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Estate of Saueressig, 38 Cal. 4th 1045 (2006)"
    ),
    DoctrineBlock(
        topic="revocation_express_implied",
        keywords=["revocation", "express", "implied", "will", "destruction", "inconsistency"],
        conclusion_template="The will {has/has not} been revoked by express act or implication.",
        reasoning_framework=(
            "A will may be revoked by express act (e.g., physical destruction, cancellation, or a subsequent writing declaring revocation) "
            "or by implication (e.g., execution of a later inconsistent will or codicil). "
            "Revocation by physical act requires intent and act (e.g., burning, tearing, obliterating) performed by the testator or at their direction in their presence. "
            "Revocation by subsequent instrument must comply with execution formalities. "
            "Implied revocation occurs when a later will is inconsistent with the prior will's terms. "
            "Lost or destroyed wills are presumed revoked unless evidence rebuts the presumption. "
            "Partial revocation is permitted in some states. "
            "The proponent of the prior will bears the burden to prove non-revocation. "
            "The court examines evidence of intent, physical acts, and subsequent writings. "
            "If revocation is established, the will or affected provisions are invalid. "
            "If not, the will stands."
        ),
        key_factors=[
            "Physical act of revocation",
            "Intent to revoke",
            "Subsequent inconsistent will",
            "Compliance with formalities",
            "Evidence of destruction"
        ],
        primary_authority=[
            "Uniform Probate Code § 2-507",
            "Estate of Oliva, 257 Cal. App. 2d 597 (1967)"
        ],
        burden_holder="Proponent of prior will",
        adversary_position="Opponent asserts revocation",
        counter_arguments=[
            "No intent to revoke",
            "No physical act performed",
            "Subsequent will not inconsistent"
        ],
        resolution_strategy="Analyze evidence of revocation by act or writing; apply presumption for lost or destroyed wills.",
        entity_scope="Testator and will(s)",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Estate of Oliva, 257 Cal. App. 2d 597 (1967)"
    ),
    DoctrineBlock(
        topic="holographic_will_validity",
        keywords=["holographic", "will", "handwritten", "signature", "formalities"],
        conclusion_template="The holographic will {is/is not} valid under applicable law.",
        reasoning_framework=(
            "A holographic will is valid if it is entirely, or substantially, in the testator's handwriting and signed by the testator. "
            "Witnesses are not required in most states, but the testator's intent must be clear from the document. "
            "Material provisions must be in the testator's handwriting. "
            "The court may consider extrinsic evidence to establish intent. "
            "If the will is not wholly in the testator's handwriting, it may be invalid. "
            "The document must reflect testamentary intent, not merely instructions or notes. "
            "If valid, the will is admitted to probate; if not, it is denied."
        ),
        key_factors=[
            "Handwriting of testator",
            "Signature",
            "Testamentary intent",
            "Material provisions in handwriting",
            "Absence of witnesses"
        ],
        primary_authority=[
            "Uniform Probate Code § 2-502(b)",
            "Estate of Southworth, 38 Cal. App. 2d 294 (1940)"
        ],
        burden_holder="Will proponent",
        adversary_position="Contestant alleges noncompliance",
        counter_arguments=[
            "Not wholly in testator's handwriting",
            "No testamentary intent",
            "Material provisions missing"
        ],
        resolution_strategy="Examine handwriting, signature, and intent; admit if statutory requirements met.",
        entity_scope="Testator",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Estate of Southworth, 38 Cal. App. 2d 294 (1940)"
    ),
    DoctrineBlock(
        topic="no_contest_clause_enforceability",
        keywords=["no contest", "in terrorem", "forfeiture", "will contest", "enforceability"],
        conclusion_template="The no contest clause {is/is not} enforceable under the circumstances.",
        reasoning_framework=(
            "A no contest clause provides that a beneficiary who contests the will forfeits their interest. "
            "Such clauses are generally enforceable unless the contest is brought in good faith and with probable cause. "
            "Statutes may limit enforceability, especially where the contest is based on forgery, revocation, or undue influence. "
            "The court examines the language of the clause, the nature of the contest, and the evidence supporting the challenge. "
            "A contest based on probable cause does not trigger forfeiture in most jurisdictions. "
            "If the clause is enforced, the contestant's share is forfeited; if not, the contest proceeds without penalty. "
            "Public policy disfavors enforcement where the will is procured by fraud or undue influence."
        ),
        key_factors=[
            "Language of clause",
            "Nature of contest",
            "Probable cause",
            "Good faith",
            "Statutory limitations"
        ],
        primary_authority=[
            "Uniform Probate Code § 2-517",
            "Cal. Prob. Code § 21310 et seq.",
            "Estate of Ferber, 66 Cal. App. 3d 244 (1977)"
        ],
        burden_holder="Will proponent",
        adversary_position="Contestant asserts good faith/probable cause",
        counter_arguments=[
            "Contest lacked probable cause",
            "Contest not in good faith",
            "Statute precludes enforcement"
        ],
        resolution_strategy="Interpret clause and evaluate contest's basis; apply statutory and public policy exceptions.",
        entity_scope="Beneficiaries",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Estate of Ferber, 66 Cal. App. 3d 244 (1977)"
    ),
    DoctrineBlock(
        topic="tortious_interference_with_inheritance",
        keywords=["tortious interference", "inheritance", "intentional act", "damages", "remedy"],
        conclusion_template="The elements of tortious interference with inheritance {are/are not} satisfied.",
        reasoning_framework=(
            "Tortious interference with inheritance is a recognized tort in some jurisdictions. "
            "The plaintiff must prove: (1) an expectancy of inheritance, (2) intentional interference by the defendant, "
            "(3) wrongful means (e.g., fraud, duress, undue influence), (4) causation, and (5) damages. "
            "The remedy is typically damages or equitable relief. "
            "The tort is generally available only if probate remedies are inadequate. "
            "The court examines the nature of the expectancy, the defendant's conduct, and the causal connection. "
            "If all elements are proven, the plaintiff may recover damages. "
            "If not, the claim fails. "
            "Some states do not recognize this tort."
        ),
        key_factors=[
            "Existence of expectancy",
            "Intentional interference",
            "Wrongful means",
            "Causation",
            "Damages",
            "Availability of probate remedies"
        ],
        primary_authority=[
            "Restatement (Second) of Torts § 774B",
            "Munn v. Munn, 189 Cal. App. 3d 1081 (1987)"
        ],
        burden_holder="Plaintiff",
        adversary_position="Defendant asserts lack of expectancy or wrongful means",
        counter_arguments=[
            "No valid expectancy",
            "No intentional interference",
            "Probate remedies adequate"
        ],
        resolution_strategy="Analyze elements and determine availability of tort remedy; defer to probate if adequate.",
        entity_scope="Potential beneficiaries",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Munn v. Munn, 189 Cal. App. 3d 1081 (1987)"
    ),
    DoctrineBlock(
        topic="burden_of_proof_allocation",
        keywords=["burden of proof", "allocation", "presumption", "contest", "evidence"],
        conclusion_template="The burden of proof {rests/does not rest} with the {proponent/contestant} on the issue.",
        reasoning_framework=(
            "The allocation of the burden of proof depends on the issue contested. "
            "The proponent of the will bears the initial burden to establish due execution and testamentary capacity. "
            "Once established, the burden shifts to the contestant to prove undue influence, fraud, or other grounds for invalidity. "
            "If a presumption arises (e.g., confidential relationship and suspicious circumstances), the burden may shift back to the proponent. "
            "The standard is typically preponderance of the evidence, but clear and convincing evidence may be required for certain issues. "
            "The court must identify the precise issue and allocate the burden accordingly. "
            "Failure to meet the burden results in an adverse finding."
        ),
        key_factors=[
            "Nature of issue",
            "Presumptions",
            "Statutory allocation",
            "Standard of proof",
            "Evidence presented"
        ],
        primary_authority=[
            "Uniform Probate Code § 3-407",
            "Estate of Fritschi, 60 Cal. 2d 367 (1963)"
        ],
        burden_holder="Varies by issue",
        adversary_position="Opposing party asserts contrary burden",
        counter_arguments=[
            "Burden not met",
            "Presumption not applicable",
            "Higher standard required"
        ],
        resolution_strategy="Identify issue and allocate burden per statute and precedent.",
        entity_scope="All parties",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Estate of Fritschi, 60 Cal. 2d 367 (1963)"
    ),
    DoctrineBlock(
        topic="interested_witness_rule",
        keywords=["interested witness", "witness", "will", "beneficiary", "purging statute"],
        conclusion_template="The interested witness rule {applies/does not apply}, affecting the witness's share.",
        reasoning_framework=(
            "An interested witness is a person who witnesses the execution of a will and is also a beneficiary. "
            "At common law, this invalidated the will; modern statutes typically 'purge' the excess benefit, "
            "limiting the interested witness to the share they would receive in intestacy. "
            "Some states do not penalize interested witnesses if there are sufficient disinterested witnesses. "
            "The court examines the number of witnesses, their interests, and applicable statutes. "
            "If the rule applies, the witness's share is reduced; if not, the will is admitted as executed."
        ),
        key_factors=[
            "Witness's interest",
            "Number of witnesses",
            "Statutory purging",
            "Intestate share",
            "Disinterested witnesses"
        ],
        primary_authority=[
            "Uniform Probate Code § 2-505(b)",
            "Cal. Prob. Code § 6112",
            "Estate of Ainsworth, 45 Cal. 2d 524 (1955)"
        ],
        burden_holder="Will proponent",
        adversary_position="Contestant asserts witness is interested",
        counter_arguments=[
            "Sufficient disinterested witnesses",
            "Statute does not purge",
            "Witness not a beneficiary"
        ],
        resolution_strategy="Determine witness's interest and apply statutory purging or validation.",
        entity_scope="Witness-beneficiaries",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Estate of Ainsworth, 45 Cal. 2d 524 (1955)"
    ),
    DoctrineBlock(
        topic="dependent_relative_revocation",
        keywords=["dependent relative revocation", "DRR", "revocation", "mistake", "conditional"],
        conclusion_template="Dependent relative revocation {applies/does not apply} to restore the prior will.",
        reasoning_framework=(
            "Dependent relative revocation (DRR) is an equitable doctrine allowing the court to disregard a revocation if it was based on a mistaken belief that a new disposition would be effective. "
            "The doctrine applies if the testator would not have revoked the prior will but for the mistaken assumption. "
            "The court compares the dispositions under the revoked and new instruments. "
            "If the new instrument is invalid and the testator's intent is clear, the prior will may be revived. "
            "DRR does not apply if the testator intended absolute revocation regardless of the new instrument's validity. "
            "The doctrine is invoked to avoid intestacy or frustration of the testator's intent."
        ),
        key_factors=[
            "Mistake in revocation",
            "Testator's intent",
            "Comparison of dispositions",
            "Validity of new instrument",
            "Avoidance of intestacy"
        ],
        primary_authority=[
            "Restatement (Third) of Property: Wills and Other Donative Transfers § 4.3",
            "Estate of Kaufman, 25 Cal. 2d 854 (1945)"
        ],
        burden_holder="Proponent of prior will",
        adversary_position="Opponent asserts absolute revocation",
        counter_arguments=[
            "Testator intended absolute revocation",
            "No mistake present",
            "Prior will not preferred"
        ],
        resolution_strategy="Assess testator's intent and mistake; apply DRR to effectuate intent if appropriate.",
        entity_scope="Testator and prior will",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Estate of Kaufman, 25 Cal. 2d 854 (1945)"
    ),
    DoctrineBlock(
        topic="integration_incorporation_by_reference",
        keywords=["integration", "incorporation by reference", "will", "extrinsic document", "intent"],
        conclusion_template="The extrinsic document {is/is not} integrated or incorporated by reference into the will.",
        reasoning_framework=(
            "Integration allows documents present at execution and intended to be part of the will to be treated as a single instrument. "
            "Incorporation by reference permits a will to include extrinsic documents if: (1) the document exists at execution, "
            "(2) the will manifests intent to incorporate, and (3) the document is sufficiently described. "
            "The court examines the language of the will, the circumstances of execution, and the existence of the document. "
            "A document not in existence at execution generally cannot be incorporated. "
            "If integration or incorporation is established, the document is given testamentary effect."
        ),
        key_factors=[
            "Existence of document at execution",
            "Manifest intent to incorporate",
            "Sufficient description",
            "Physical presence (for integration)",
            "Testator's intent"
        ],
        primary_authority=[
            "Uniform Probate Code § 2-510",
            "Estate of Rigsby, 34 Cal. 2d 279 (1949)"
        ],
        burden_holder="Will proponent",
        adversary_position="Contestant alleges lack of intent or description",
        counter_arguments=[
            "Document not in existence",
            "No intent to incorporate",
            "Insufficient description"
        ],
        resolution_strategy="Apply statutory and common law requirements for integration or incorporation.",
        entity_scope="Testator and extrinsic documents",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Estate of Rigsby, 34 Cal. 2d 279 (1949)"
    ),
    DoctrineBlock(
        topic="class_gifts_and_lapse",
        keywords=["class gift", "lapse", "anti-lapse", "beneficiary", "substitution"],
        conclusion_template="The class gift {lapses/does not lapse}, and the anti-lapse statute {applies/does not apply}.",
        reasoning_framework=(
            "A class gift is a bequest to a group described by relationship or status (e.g., 'children'). "
            "If a class member predeceases the testator, the gift may lapse unless the anti-lapse statute applies. "
            "Anti-lapse statutes substitute the deceased beneficiary's descendants if the beneficiary is related to the testator. "
            "The court examines the language of the will, the relationship, and statutory provisions. "
            "If the anti-lapse statute applies, the descendants take per stirpes. "
            "If not, the gift lapses and passes to the surviving class members or residuary."
        ),
        key_factors=[
            "Nature of class gift",
            "Relationship to testator",
            "Language of will",
            "Application of anti-lapse statute",
            "Surviving class members"
        ],
        primary_authority=[
            "Uniform Probate Code § 2-603",
            "Estate of Russell, 69 Cal. 2d 200 (1968)"
        ],
        burden_holder="Will proponent",
        adversary_position="Contestant asserts lapse or anti-lapse",
        counter_arguments=[
            "Anti-lapse statute does not apply",
            "Gift not to a class",
            "Will provides otherwise"
        ],
        resolution_strategy="Interpret will and apply anti-lapse statute as appropriate.",
        entity_scope="Class beneficiaries",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Estate of Russell, 69 Cal. 2d 200 (1968)"
    ),
    DoctrineBlock(
        topic="ademption_by_extinction",
        keywords=["ademption", "extinction", "specific devise", "property not in estate", "replacement"],
        conclusion_template="The specific gift {is/is not} adeemed by extinction.",
        reasoning_framework=(
            "Ademption by extinction occurs when specifically devised property is not in the testator's estate at death. "
            "If the property is missing, sold, or destroyed, the gift fails unless a statutory exception applies. "
            "The court examines the testator's intent, the nature of the gift, and any replacement property. "
            "Some statutes provide for tracing or replacement value if the property was sold by a conservator or agent. "
            "General or demonstrative gifts are not subject to ademption. "
            "If ademption applies, the beneficiary takes nothing; if not, they may receive substitute property or value."
        ),
        key_factors=[
            "Nature of gift (specific/general)",
            "Existence of property at death",
            "Testator's intent",
            "Replacement or tracing statutes",
            "Actions by conservator or agent"
        ],
        primary_authority=[
            "Uniform Probate Code § 2-606",
            "Estate of Mason, 62 Cal. 2d 213 (1965)"
        ],
        burden_holder="Beneficiary",
        adversary_position="Executor asserts ademption",
        counter_arguments=[
            "Gift is general or demonstrative",
            "Statutory exception applies",
            "Replacement property available"
        ],
        resolution_strategy="Determine nature of gift and apply ademption or statutory exceptions.",
        entity_scope="Beneficiaries of specific gifts",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Estate of Mason, 62 Cal. 2d 213 (1965)"
    ),
    DoctrineBlock(
        topic="abatement_order",
        keywords=["abatement", "order of abatement", "insufficient assets", "priority", "residuary"],
        conclusion_template="The abatement order {requires/does not require} reduction of the specified gift.",
        reasoning_framework=(
            "Abatement refers to the reduction of gifts when the estate's assets are insufficient to pay debts, expenses, and all bequests. "
            "The order of abatement is typically: (1) property not disposed of by will, (2) residuary gifts, (3) general gifts, and (4) specific gifts. "
            "The will may specify a different order. "
            "The court applies statutory or common law priorities to reduce gifts as needed. "
            "If abatement is required, lower-priority gifts are reduced or eliminated first."
        ),
        key_factors=[
            "Sufficiency of estate assets",
            "Type of gift (residuary, general, specific)",
            "Will provisions",
            "Statutory order",
            "Debts and expenses"
        ],
        primary_authority=[
            "Uniform Probate Code § 3-902",
            "Estate of Buckhantz, 120 Cal. App. 2d 92 (1953)"
        ],
        burden_holder="Executor",
        adversary_position="Beneficiary asserts different order",
        counter_arguments=[
            "Will specifies different order",
            "Gift is specific and higher priority",
            "Statutory exceptions apply"
        ],
        resolution_strategy="Apply statutory or will-specified order to reduce gifts as necessary.",
        entity_scope="All beneficiaries",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Estate of Buckhantz, 120 Cal. App. 2d 92 (1953)"
    ),
    DoctrineBlock(
        topic="advancements_and_satisfaction",
        keywords=["advancement", "satisfaction", "lifetime gift", "intended as advancement", "evidence"],
        conclusion_template="The lifetime gift {is/is not} treated as an advancement or satisfaction of the inheritance.",
        reasoning_framework=(
            "An advancement is a lifetime gift intended to be applied against the recipient's share of the estate. "
            "Satisfaction applies to testamentary gifts. "
            "The intent must be contemporaneously expressed in writing by the testator or acknowledged in writing by the recipient. "
            "The court examines evidence of intent, the nature of the gift, and statutory requirements. "
            "If proven, the value of the advancement is deducted from the recipient's share. "
            "If not, the gift is treated as separate."
        ),
        key_factors=[
            "Contemporaneous writing",
            "Acknowledgment by recipient",
            "Nature of gift",
            "Testator's intent",
            "Statutory requirements"
        ],
        primary_authority=[
            "Uniform Probate Code § 2-109",
            "Cal. Prob. Code § 6409",
            "Estate of Shaver, 131 Cal. App. 2d 267 (1955)"
        ],
        burden_holder="Executor or contesting beneficiary",
        adversary_position="Recipient asserts gift was not advancement",
        counter_arguments=[
            "No writing or acknowledgment",
            "Gift not intended as advancement",
            "Statute not satisfied"
        ],
        resolution_strategy="Review writings and evidence of intent; apply statutory requirements.",
        entity_scope="Heirs and beneficiaries",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Estate of Shaver, 131 Cal. App. 2d 267 (1955)"
    ),
    DoctrineBlock(
        topic="elective_share_and_community_property",
        keywords=["elective share", "community property", "spouse", "forced share", "waiver"],
        conclusion_template="The surviving spouse {is/is not} entitled to an elective share or community property interest.",
        reasoning_framework=(
            "The elective share protects a surviving spouse from disinheritance by allowing election against the will for a statutory share. "
            "In community property states, the spouse is entitled to one-half of community property. "
            "The court determines the nature of the property (community or separate), the validity of any waiver, and the spouse's election. "
            "Prenuptial or postnuptial agreements may waive the elective share. "
            "The elective share is calculated based on the augmented estate, including certain non-probate transfers. "
            "If the spouse elects, the share is distributed accordingly; if not, the will controls."
        ),
        key_factors=[
            "Marital status",
            "Nature of property",
            "Validity of waiver",
            "Augmented estate calculation",
            "Spouse's election"
        ],
        primary_authority=[
            "Uniform Probate Code §§ 2-201 to 2-214",
            "Cal. Fam. Code § 760",
            "Estate of Cross, 60 Cal. 2d 692 (1964)"
        ],
        burden_holder="Surviving spouse",
        adversary_position="Estate asserts waiver or separate property",
        counter_arguments=[
            "Valid waiver executed",
            "Property is separate",
            "Spouse did not elect"
        ],
        resolution_strategy="Classify property, review waivers, and apply elective share or community property law.",
        entity_scope="Surviving spouse",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Estate of Cross, 60 Cal. 2d 692 (1964)"
    ),
    DoctrineBlock(
        topic="standing_to_contest",
        keywords=["standing", "contest", "interested person", "beneficiary", "heir"],
        conclusion_template="The contestant {has/does not have} standing to challenge the will.",
        reasoning_framework=(
            "To contest a will, a person must have standing as an 'interested person,' typically a beneficiary, heir, or creditor with a pecuniary interest. "
            "The court examines the contestant's relationship to the decedent and the impact of the will on their interest. "
            "Mere moral or emotional interest is insufficient. "
            "If standing is established, the contest proceeds; if not, it is dismissed."
        ),
        key_factors=[
            "Relationship to decedent",
            "Pecuniary interest",
            "Heirship or beneficiary status",
            "Statutory definition of interested person"
        ],
        primary_authority=[
            "Uniform Probate Code § 1-201(27)",
            "Cal. Prob. Code § 48",
            "Estate of Plaut, 27 Cal. 2d 424 (1945)"
        ],
        burden_holder="Contestant",
        adversary_position="Proponent asserts lack of standing",
        counter_arguments=[
            "No pecuniary interest",
            "Not an heir or beneficiary",
            "Statute excludes contestant"
        ],
        resolution_strategy="Determine pecuniary interest and apply statutory definition.",
        entity_scope="Contestants",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Estate of Plaut, 27 Cal. 2d 424 (1945)"
    ),
    DoctrineBlock(
        topic="venue_and_jurisdiction",
        keywords=["venue", "jurisdiction", "probate", "residence", "property location"],
        conclusion_template="The court {has/does not have} proper venue and jurisdiction over the probate proceeding.",
        reasoning_framework=(
            "Venue and jurisdiction for probate are determined by the decedent's domicile at death and the location of property. "
            "The primary probate is typically in the county of domicile; ancillary proceedings may occur where real property is located. "
            "The court examines statutory provisions, the decedent's residence, and the situs of assets. "
            "If venue or jurisdiction is improper, the proceeding may be transferred or dismissed."
        ),
        key_factors=[
            "Decedent's domicile",
            "Location of property",
            "Statutory venue provisions",
            "Ancillary probate"
        ],
        primary_authority=[
            "Uniform Probate Code § 3-201",
            "Cal. Prob. Code § 7051",
            "Estate of Fritschi, 60 Cal. 2d 367 (1963)"
        ],
        burden_holder="Petitioner",
        adversary_position="Respondent asserts improper venue/jurisdiction",
        counter_arguments=[
            "Decedent domiciled elsewhere",
            "Property located in another jurisdiction",
            "Statute requires transfer"
        ],
        resolution_strategy="Establish domicile and property location; apply statutory venue and jurisdiction rules.",
        entity_scope="Probate courts",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Estate of Fritschi, 60 Cal. 2d 367 (1963)"
    ),
    DoctrineBlock(
        topic="statute_of_limitations",
        keywords=["statute of limitations", "timeliness", "will contest", "probate", "bar"],
        conclusion_template="The contest {is/is not} barred by the statute of limitations.",
        reasoning_framework=(
            "A will contest must be filed within the statutory period after notice of probate or issuance of letters. "
            "The court examines the date of notice, the filing date, and statutory deadlines. "
            "Late-filed contests are barred unless an exception applies (e.g., fraud or lack of notice). "
            "If timely, the contest proceeds; if not, it is dismissed."
        ),
        key_factors=[
            "Date of notice or probate",
            "Filing date of contest",
            "Statutory deadline",
            "Exceptions (fraud, lack of notice)"
        ],
        primary_authority=[
            "Uniform Probate Code § 3-108",
            "Cal. Prob. Code § 8270",
            "Estate of Horn, 219 Cal. App. 2d 477 (1963)"
        ],
        burden_holder="Contestant",
        adversary_position="Proponent asserts time bar",
        counter_arguments=[
            "Contest timely filed",
            "Exception applies",
            "Notice defective"
        ],
        resolution_strategy="Compare filing date to statutory deadline; consider exceptions.",
        entity_scope="Contestants",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Estate of Horn, 219 Cal. App. 2d 477 (1963)"
    ),
    DoctrineBlock(
        topic="harmless_error_doctrine",
        keywords=["harmless error", "excuse", "execution defect", "testator's intent", "substantial compliance"],
        conclusion_template="The harmless error doctrine {applies/does not apply} to excuse the execution defect.",
        reasoning_framework=(
            "The harmless error doctrine allows courts to excuse minor defects in execution if there is clear and convincing evidence "
            "that the decedent intended the document to be their will. "
            "The court examines the nature of the defect, the evidence of intent, and statutory authority. "
            "Substantial compliance may suffice for admission to probate. "
            "The doctrine does not excuse major defects (e.g., lack of signature or testamentary intent). "
            "If applied, the will is admitted; if not, it is denied."
        ),
        key_factors=[
            "Nature of execution defect",
            "Evidence of testator's intent",
            "Statutory authority",
            "Substantial compliance",
            "Clear and convincing evidence"
        ],
        primary_authority=[
            "Uniform Probate Code § 2-503",
            "Estate of Hall, 573 N.W.2d 852 (Minn. 1998)"
        ],
        burden_holder="Will proponent",
        adversary_position="Contestant asserts defect is not harmless",
        counter_arguments=[
            "Defect is substantial",
            "No clear evidence of intent",
            "Statute does not permit harmless error"
        ],
        resolution_strategy="Assess evidence of intent and statutory authority; excuse defect if requirements met.",
        entity_scope="Testator",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Estate of Hall, 573 N.W.2d 852 (Minn. 1998)"
    ),
    # Additional doctrine blocks to reach 40+ entries
    DoctrineBlock(
        topic="execution_of_codiCil",
        keywords=["codicil", "execution", "formalities", "will amendment", "attestation"],
        conclusion_template="The codicil {is/is not} validly executed and effective to amend the will.",
        reasoning_framework=(
            "A codicil is an amendment or supplement to a will and must be executed with the same formalities as a will. "
            "The court examines whether the codicil is signed by the testator and attested by the required number of witnesses. "
            "A valid codicil republishes the will as of the date of the codicil. "
            "If formalities are not met, the codicil is invalid. "
            "A holographic codicil is permitted if allowed by statute."
        ),
        key_factors=[
            "Testator's signature",
            "Witness attestation",
            "Compliance with statutory formalities",
            "Holographic execution",
            "Intent to amend"
        ],
        primary_authority=[
            "Uniform Probate Code § 2-502",
            "Cal. Prob. Code § 6120",
            "Estate of Button, 209 Cal. 325 (1930)"
        ],
        burden_holder="Codicil proponent",
        adversary_position="Contestant alleges improper execution",
        counter_arguments=[
            "Formalities not satisfied",
            "No intent to amend",
            "Codicil not signed"
        ],
        resolution_strategy="Review execution and attestation; admit codicil if requirements met.",
        entity_scope="Testator and codicil",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Estate of Button, 209 Cal. 325 (1930)"
    ),
    DoctrineBlock(
        topic="lost_or_destroyed_will",
        keywords=["lost will", "destroyed will", "probate", "secondary evidence", "presumption of revocation"],
        conclusion_template="The lost or destroyed will {is/is not} admitted to probate.",
        reasoning_framework=(
            "A lost or destroyed will may be admitted to probate if its contents and due execution are proven by clear and convincing evidence. "
            "There is a presumption of revocation if the will was last in the testator's possession and cannot be found. "
            "The proponent must rebut the presumption by showing the will was lost or destroyed without intent to revoke. "
            "Secondary evidence (e.g., copies, witness testimony) may be used to prove the will's contents. "
            "If the presumption is not rebutted, the will is deemed revoked."
        ),
        key_factors=[
            "Evidence of due execution",
            "Contents of will",
            "Presumption of revocation",
            "Secondary evidence",
            "Testator's intent"
        ],
        primary_authority=[
            "Uniform Probate Code § 2-507",
            "Cal. Prob. Code § 8223",
            "Estate of Oliva, 257 Cal. App. 2d 597 (1967)"
        ],
        burden_holder="Will proponent",
        adversary_position="Contestant asserts revocation",
        counter_arguments=[
            "Will last in testator's possession",
            "No evidence of loss without intent to revoke",
            "Insufficient evidence of contents"
        ],
        resolution_strategy="Present clear and convincing evidence of execution and contents; rebut presumption of revocation.",
        entity_scope="Testator and will",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Estate of Oliva, 257 Cal. App. 2d 597 (1967)"
    ),
    DoctrineBlock(
        topic="simultaneous_death_and_survivorship",
        keywords=["simultaneous death", "survivorship", "commorientes", "120-hour rule"],
        conclusion_template="The simultaneous death rule {applies/does not apply}, and survivorship {is/is not} established.",
        reasoning_framework=(
            "If two or more persons die simultaneously or it is uncertain who survived, the Uniform Simultaneous Death Act or 120-hour rule applies. "
            "A person must survive the decedent by 120 hours to inherit unless the will provides otherwise. "
            "If survivorship cannot be established by clear and convincing evidence, the property is distributed as if the beneficiary predeceased the decedent. "
            "The court examines death certificates, witness testimony, and other evidence of survivorship."
        ),
        key_factors=[
            "Evidence of survivorship",
            "120-hour rule",
            "Will provisions",
            "Death certificates",
            "Statutory application"
        ],
        primary_authority=[
            "Uniform Probate Code § 2-104",
            "Cal. Prob. Code § 220",
            "Estate of Rowley, 257 Cal. App. 2d 324 (1967)"
        ],
        burden_holder="Claimant of inheritance",
        adversary_position="Opponent asserts lack of survivorship",
        counter_arguments=[
            "No clear evidence of survivorship",
            "120-hour rule not satisfied",
            "Will provides alternative disposition"
        ],
        resolution_strategy="Apply statutory survivorship rule; distribute as if predeceased if not satisfied.",
        entity_scope="Heirs and beneficiaries",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Estate of Rowley, 257 Cal. App. 2d 324 (1967)"
    ),
    DoctrineBlock(
        topic="pour_over_will_and_trusts",
        keywords=["pour-over will", "trust", "incorporation", "residuary", "testamentary trust"],
        conclusion_template="The pour-over provision {is/is not} effective to transfer assets to the trust.",
        reasoning_framework=(
            "A pour-over will directs assets to a trust existing at the testator's death. "
            "The trust must be identified in the will and either exist or be created concurrently. "
            "The court examines the will, trust instrument, and statutory requirements for incorporation by reference or acts of independent significance. "
            "If valid, the assets pour over into the trust; if not, they pass under intestacy or residuary."
        ),
        key_factors=[
            "Existence of trust at death",
            "Identification in will",
            "Statutory requirements",
            "Acts of independent significance",
            "Testator's intent"
        ],
        primary_authority=[
            "Uniform Probate Code § 2-511",
            "Cal. Prob. Code § 6300",
            "Estate of Duke, 61 Cal. 4th 871 (2015)"
        ],
        burden_holder="Will proponent",
        adversary_position="Contestant alleges invalid trust or incorporation",
        counter_arguments=[
            "Trust not in existence",
            "No identification in will",
            "Statute not satisfied"
        ],
        resolution_strategy="Verify trust's existence and compliance with statutory requirements.",
        entity_scope="Testator and trust",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Estate of Duke, 61 Cal. 4th 871 (2015)"
    ),
    DoctrineBlock(
        topic="spousal_omission_and_pretermitted_heir",
        keywords=["spousal omission", "pretermitted heir", "unintentional disinheritance", "statutory share"],
        conclusion_template="The omitted spouse or child {is/is not} entitled to a statutory share.",
        reasoning_framework=(
            "A spouse or child omitted from a will may be entitled to a statutory share if the omission was unintentional. "
            "The court examines the will, evidence of intent, and statutory provisions. "
            "If the omission was intentional or the spouse/child was otherwise provided for, the statute does not apply. "
            "If entitled, the omitted person receives the share they would have taken under intestacy."
        ),
        key_factors=[
            "Omission from will",
            "Intentionality",
            "Provision outside will",
            "Statutory entitlement",
            "Relationship to decedent"
        ],
        primary_authority=[
            "Uniform Probate Code §§ 2-301, 2-302",
            "Cal. Prob. Code §§ 21610, 21620",
            "Estate of Duke, 61 Cal. 4th 871 (2015)"
        ],
        burden_holder="Omitted spouse or child",
        adversary_position="Estate asserts intentional omission or other provision",
        counter_arguments=[
            "Omission was intentional",
            "Provided for outside will",
            "Statute does not apply"
        ],
        resolution_strategy="Review will and extrinsic evidence; apply statutory share if requirements met.",
        entity_scope="Omitted spouse or child",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Estate of Duke, 61 Cal. 4th 871 (2015)"
    ),
    DoctrineBlock(
        topic="forgery_and_alteration",
        keywords=["forgery", "alteration", "will", "signature", "invalidity"],
        conclusion_template="The will {is/is not} invalid due to forgery or unauthorized alteration.",
        reasoning_framework=(
            "A will is invalid if the testator's signature is forged or if material alterations are made without proper execution. "
            "The court examines handwriting analysis, witness testimony, and the circumstances of execution. "
            "If forgery or unauthorized alteration is proven, the will or affected provisions are invalid."
        ),
        key_factors=[
            "Authenticity of signature",
            "Handwriting analysis",
            "Witness testimony",
            "Materiality of alteration",
            "Proper execution of changes"
        ],
        primary_authority=[
            "Restatement (Third) of Property: Wills and Other Donative Transfers § 8.3",
            "Estate of Newhall, 190 P.2d 885 (Cal. 1948)"
        ],
        burden_holder="Contestant",
        adversary_position="Proponent asserts authenticity",
        counter_arguments=[
            "Signature is genuine",
            "Alteration properly executed",
            "No material change"
        ],
        resolution_strategy="Analyze evidence of authenticity and execution; invalidate if forgery or improper alteration proven.",
        entity_scope="Testator and will",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Estate of Newhall, 190 P.2d 885 (Cal. 1948)"
    ),
    DoctrineBlock(
        topic="partial_invalidity_and_severability",
        keywords=["partial invalidity", "severability", "will", "provision", "remainder"],
        conclusion_template="The invalid provision {is/is not} severable, and the remainder of the will {stands/falls}.",
        reasoning_framework=(
            "If a provision of a will is invalid (e.g., due to undue influence or illegality), the court determines whether it is severable from the remainder. "
            "If the invalid provision can be excised without defeating the testator's overall intent, the remainder stands. "
            "If not, the entire will may be invalid. "
            "The court examines the will's structure, the importance of the invalid provision, and the testator's intent."
        ),
        key_factors=[
            "Nature of invalid provision",
            "Severability",
            "Testator's overall intent",
            "Impact on remainder",
            "Statutory guidance"
        ],
        primary_authority=[
            "Restatement (Third) of Property: Wills and Other Donative Transfers § 12.1",
            "Estate of Duke, 61 Cal. 4th 871 (2015)"
        ],
        burden_holder="Proponent of remainder",
        adversary_position="Contestant asserts entire will is invalid",
        counter_arguments=[
            "Provision not severable",
            "Intent defeated by excision",
            "Statute requires invalidation"
        ],
        resolution_strategy="Assess severability and intent; uphold remainder if possible.",
        entity_scope="Will and beneficiaries",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Estate of Duke, 61 Cal. 4th 871 (2015)"
    ),
    DoctrineBlock(
        topic="specific_vs_general_devises",
        keywords=["specific devise", "general devise", "bequest", "classification", "distribution"],
        conclusion_template="The gift {is/is not} a specific devise, and distribution {follows/does not follow} accordingly.",
        reasoning_framework=(
            "A specific devise is a gift of a particular item or property, while a general devise is a gift from the general assets of the estate. "
            "The court interprets the will to determine the nature of the gift. "
            "Specific devises are subject to ademption by extinction; general devises are not. "
            "The classification affects abatement and distribution."
        ),
        key_factors=[
            "Language of will",
            "Identification of property",
            "Intent of testator",
            "Ademption implications",
            "Statutory definitions"
        ],
        primary_authority=[
            "Uniform Probate Code § 2-606",
            "Estate of Mason, 62 Cal. 2d 213 (1965)"
        ],
        burden_holder="Beneficiary",
        adversary_position="Executor asserts different classification",
        counter_arguments=[
            "Gift is general, not specific",
            "Will language ambiguous",
            "Statute controls classification"
        ],
        resolution_strategy="Interpret will and apply statutory definitions; classify gift accordingly.",
        entity_scope="Beneficiaries",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Estate of Mason, 62 Cal. 2d 213 (1965)"
    ),
    DoctrineBlock(
        topic="residuary_clause_and_omitted_property",
        keywords=["residuary clause", "omitted property", "catch-all", "distribution", "intestacy"],
        conclusion_template="The residuary clause {does/does not} dispose of omitted property.",
        reasoning_framework=(
            "A residuary clause disposes of all property not specifically devised. "
            "If the will omits property, the residuary clause typically captures it. "
            "If there is no residuary clause, omitted property passes by intestacy. "
            "The court interprets the will to determine the scope of the residuary clause."
        ),
        key_factors=[
            "Presence of residuary clause",
            "Language of will",
            "Nature of omitted property",
            "Testator's intent",
            "Statutory rules"
        ],
        primary_authority=[
            "Uniform Probate Code § 2-604",
            "Cal. Prob. Code § 21117",
            "Estate of Duke, 61 Cal. 4th 871 (2015)"
        ],
        burden_holder="Residuary beneficiary",
        adversary_position="Heir asserts intestacy",
        counter_arguments=[
            "No residuary clause",
            "Will language ambiguous",
            "Statute requires intestacy"
        ],
        resolution_strategy="Interpret will; distribute omitted property per residuary or intestacy.",
        entity_scope="Residuary beneficiaries and heirs",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Estate of Duke, 61 Cal. 4th 871 (2015)"
    ),
    DoctrineBlock(
        topic="probate_vs_nonprobate_transfers",
        keywords=["probate", "nonprobate", "joint tenancy", "POD", "TOD", "trust", "will substitute"],
        conclusion_template="The asset {is/is not} subject to probate administration.",
        reasoning_framework=(
            "Nonprobate transfers (e.g., joint tenancy, payable-on-death accounts, trusts) pass outside the will and are not subject to probate. "
            "The court examines title, beneficiary designations, and the nature of the asset. "
            "If the asset is nonprobate, it passes to the designated beneficiary regardless of the will. "
            "If probate, it is distributed per the will or intestacy."
        ),
        key_factors=[
            "Title to asset",
            "Beneficiary designation",
            "Nature of transfer",
            "Will provisions",
            "Statutory classification"
        ],
        primary_authority=[
            "Uniform Probate Code § 6-101",
            "Cal. Prob. Code § 5000",
            "Estate of Duke, 61 Cal. 4th 871 (2015)"
        ],
        burden_holder="Claimant of asset",
        adversary_position="Executor asserts probate asset",
        counter_arguments=[
            "Asset is probate property",
            "No valid beneficiary designation",
            "Statute requires probate"
        ],
        resolution_strategy="Review title and designations; classify asset as probate or nonprobate.",
        entity_scope="Beneficiaries and heirs",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Estate of Duke, 61 Cal. 4th 871 (2015)"
    ),
    DoctrineBlock(
        topic="testamentary_intent",
        keywords=["testamentary intent", "will", "animus testandi", "document", "execution"],
        conclusion_template="The document {does/does not} reflect testamentary intent.",
        reasoning_framework=(
            "A valid will requires testamentary intent: the testator must intend the document to operate as their will. "
            "The court examines the language, circumstances of execution, and extrinsic evidence. "
            "Instructions, drafts, or notes lacking intent are not wills. "
            "If intent is established, the document may be admitted to probate."
        ),
        key_factors=[
            "Language of document",
            "Circumstances of execution",
            "Extrinsic evidence",
            "Testator's statements",
            "Statutory requirements"
        ],
        primary_authority=[
            "Uniform Probate Code § 2-502",
            "Estate of Button, 209 Cal. 325 (1930)"
        ],
        burden_holder="Will proponent",
        adversary_position="Contestant asserts lack of intent",
        counter_arguments=[
            "Document is not a will",
            "No intent to make testamentary disposition",
            "Extrinsic evidence contradicts intent"
        ],
        resolution_strategy="Assess language and circumstances; admit if testamentary intent shown.",
        entity_scope="Testator",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Estate of Button, 209 Cal. 325 (1930)"
    ),
    DoctrineBlock(
        topic="will_construction_and_ambiguity",
        keywords=["will construction", "ambiguity", "interpretation", "extrinsic evidence", "intent"],
        conclusion_template="The ambiguity {is/is not} resolved in favor of the proponent's construction.",
        reasoning_framework=(
            "When a will is ambiguous, the court seeks to ascertain the testator's intent from the language and admissible extrinsic evidence. "
            "Patent ambiguities are apparent on the face; latent ambiguities arise from application. "
            "The court may consider surrounding circumstances, declarations, and other evidence. "
            "If intent cannot be determined, the ambiguity may be resolved by rules of construction or result in intestacy."
        ),
        key_factors=[
            "Type of ambiguity",
            "Language of will",
            "Extrinsic evidence",
            "Testator's intent",
            "Rules of construction"
        ],
        primary_authority=[
            "Restatement (Third) of Property: Wills and Other Donative Transfers § 11.1",
            "Estate of Russell, 69 Cal. 2d 200 (1968)"
        ],
        burden_holder="Proponent of construction",
        adversary_position="Contestant asserts contrary intent",
        counter_arguments=[
            "Ambiguity cannot be resolved",
            "Extrinsic evidence inadmissible",
            "Statute requires intestacy"
        ],
        resolution_strategy="Admit extrinsic evidence; apply rules of construction if intent remains unclear.",
        entity_scope="Will and beneficiaries",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Estate of Russell, 69 Cal. 2d 200 (1968)"
    ),
    DoctrineBlock(
        topic="reformation_of_will",
        keywords=["reformation", "mistake", "will", "testator's intent", "clear and convincing evidence"],
        conclusion_template="The will {is/is not} subject to reformation to correct a mistake.",
        reasoning_framework=(
            "A court may reform a will to correct a mistake of fact or law if clear and convincing evidence shows the testator's intent and the terms were affected by the mistake. "
            "The court examines the language, extrinsic evidence, and the nature of the mistake. "
            "Reformation is not permitted to supply omitted provisions unless intent is clear."
        ),
        key_factors=[
            "Existence of mistake",
            "Testator's intent",
            "Clear and convincing evidence",
            "Nature of correction",
            "Statutory authority"
        ],
        primary_authority=[
            "Uniform Probate Code § 2-805",
            "Estate of Duke, 61 Cal. 4th 871 (2015)"
        ],
        burden_holder="Party seeking reformation",
        adversary_position="Opponent asserts no mistake or insufficient evidence",
        counter_arguments=[
            "No mistake present",
            "Evidence not clear and convincing",
            "Statute does not permit reformation"
        ],
        resolution_strategy="Review evidence and statutory authority; reform if requirements met.",
        entity_scope="Will and beneficiaries",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Estate of Duke, 61 Cal. 4th 871 (2015)"
    ),
    DoctrineBlock(
        topic="cy_pres_and_charitable_gifts",
        keywords=["cy pres", "charitable gift", "impossibility", "approximate intent", "reformation"],
        conclusion_template="The cy pres doctrine {applies/does not apply} to reform the charitable gift.",
        reasoning_framework=(
            "If a charitable gift cannot be carried out as written due to impossibility or impracticability, the court may apply the cy pres doctrine to reform the gift in a manner approximating the testator's intent. "
            "The court examines the language of the will, the nature of the charity, and evidence of general charitable intent. "
            "If cy pres applies, the gift is redirected to a similar charitable purpose."
        ),
        key_factors=[
            "Impossibility or impracticability",
            "General charitable intent",
            "Language of will",
            "Nature of charity",
            "Statutory authority"
        ],
        primary_authority=[
            "Uniform Probate Code § 3-110",
            "Restatement (Third) of Trusts § 67",
            "Estate of Tarrant, 38 Cal. App. 3d 1 (1974)"
        ],
        burden_holder="Charity or executor",
        adversary_position="Heir asserts gift fails",
        counter_arguments=[
            "No general charitable intent",
            "Gift is specific and not reformable",
            "Statute does not permit cy pres"
        ],
        resolution_strategy="Determine impossibility and general intent; reform gift if cy pres applies.",
        entity_scope="Charitable beneficiaries",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Estate of Tarrant, 38 Cal. App. 3d 1 (1974)"
    ),
    DoctrineBlock(
        topic="creditor_claims_and_priority",
        keywords=["creditor claims", "priority", "payment of debts", "estate administration", "notice"],
        conclusion_template="The creditor's claim {has/does not have} priority for payment from the estate.",
        reasoning_framework=(
            "Creditors must present claims within the statutory period after notice. "
            "The court determines the validity and priority of claims based on statutory classifications. "
            "Priority is typically: (1) administration expenses, (2) funeral expenses, (3) debts with preference, (4) general debts. "
            "Late or invalid claims are barred. "
            "If assets are insufficient, claims are paid in order of priority."
        ),
        key_factors=[
            "Timeliness of claim",
            "Statutory priority",
            "Notice to creditors",
            "Validity of debt",
            "Sufficiency of assets"
        ],
        primary_authority=[
            "Uniform Probate Code §§ 3-803, 3-805",
            "Cal. Prob. Code §§ 9050, 9051",
            "Estate of Buckhantz, 120 Cal. App. 2d 92 (1953)"
        ],
        burden_holder="Creditor",
        adversary_position="Executor asserts late or invalid claim",
        counter_arguments=[
            "Claim untimely",
            "Debt not valid",
            "Insufficient assets"
        ],
        resolution_strategy="Review timeliness and validity; pay claims by statutory priority.",
        entity_scope="Creditors and estate",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Estate of Buckhantz, 120 Cal. App. 2d 92 (1953)"
    ),
    DoctrineBlock(
        topic="family_allowance_and_exempt_property",
        keywords=["family allowance", "exempt property", "surviving spouse", "minor children", "statutory entitlement"],
        conclusion_template="The family allowance and exempt property {are/are not} available to the claimant.",
        reasoning_framework=(
            "Statutes provide a family allowance and exempt property to the surviving spouse and minor children during estate administration. "
            "The court determines eligibility, amount, and duration based on statutory provisions. "
            "These allowances have priority over most other claims and are not subject to creditors. "
            "If eligible, the claimant receives the allowance and exempt property."
        ),
        key_factors=[
            "Relationship to decedent",
            "Eligibility under statute",
            "Amount and duration",
            "Priority over claims",
            "Notice and application"
        ],
        primary_authority=[
            "Uniform Probate Code §§ 2-402, 2-403",
            "Cal. Prob. Code §§ 6500, 6510",
            "Estate of Cross, 60 Cal. 2d 692 (1964)"
        ],
        burden_holder="Claimant",
        adversary_position="Executor asserts ineligibility",
        counter_arguments=[
            "Not a spouse or minor child",
            "Statutory requirements not met",
            "Allowance already provided"
        ],
        resolution_strategy="Review eligibility and statutory provisions; award allowance and exempt property if appropriate.",
        entity_scope="Surviving spouse and minor children",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Estate of Cross, 60 Cal. 2d 692 (1964)"
    ),
    DoctrineBlock(
        topic="disclaimer_and_renunciation",
        keywords=["disclaimer", "renunciation", "beneficiary", "qualified disclaimer", "IRS requirements"],
        conclusion_template="The disclaimer {is/is not} effective, and the property {passes/does not pass} as if the beneficiary predeceased.",
        reasoning_framework=(
            "A beneficiary may disclaim an inheritance by timely, written, and unequivocal disclaimer. "
            "The disclaimer must comply with state law and, for tax purposes, with IRC § 2518. "
            "The court examines the form, timing, and effect of the disclaimer. "
            "A valid disclaimer causes the property to pass as if the beneficiary predeceased the decedent."
        ),
        key_factors=[
            "Written disclaimer",
            "Timeliness",
            "Compliance with statute",
            "IRS requirements",
            "Effect on distribution"
        ],
        primary_authority=[
            "Uniform Probate Code § 2-1105",
            "Cal. Prob. Code § 282",
            "IRC § 2518"
        ],
        burden_holder="Beneficiary",
        adversary_position="Executor asserts ineffective disclaimer",
        counter_arguments=[
            "Disclaimer not timely",
            "Form not compliant",
            "Statute or IRS requirements not met"
        ],
        resolution_strategy="Review disclaimer for compliance; distribute property as if predeceased if valid.",
        entity_scope="Beneficiaries",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="IRC § 2518"
    ),
    DoctrineBlock(
        topic="joint_tenancy_and_right_of_survivorship",
        keywords=["joint tenancy", "right of survivorship", "probate avoidance", "title", "severance"],
        conclusion_template="The joint tenancy {is/is not} effective to transfer property by right of survivorship.",
        reasoning_framework=(
            "Joint tenancy with right of survivorship allows property to pass automatically to surviving joint tenants outside probate. "
            "The court examines the title, intent to create joint tenancy, and any severance prior to death. "
            "If joint tenancy exists and is not severed, the property passes to the survivor. "
            "If severed, the property passes by will or intestacy."
        ),
        key_factors=[
            "Title to property",
            "Creation of joint tenancy",
            "Intent of parties",
            "Severance prior to death",
            "Statutory requirements"
        ],
        primary_authority=[
            "Uniform Probate Code § 6-202",
            "Cal. Civ. Code § 683",
            "Estate of Propst, 50 Cal. 3d 448 (1990)"
        ],
        burden_holder="Surviving joint tenant",
        adversary_position="Executor asserts severance or no joint tenancy",
        counter_arguments=[
            "Property not held in joint tenancy",
            "Severance occurred",
            "Statute not satisfied"
        ],
        resolution_strategy="Review title and intent; distribute by survivorship if joint tenancy exists.",
        entity_scope="Joint tenants",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Estate of Propst, 50 Cal. 3d 448 (1990)"
    ),
    DoctrineBlock(
        topic="capacity_to_make_codiCil",
        keywords=["capacity", "codicil", "testamentary capacity", "amendment", "mental state"],
        conclusion_template="The testator {has/does not have} capacity to execute the codicil.",
        reasoning_framework=(
            "The standard for capacity to execute a codicil is the same as for a will. "
            "The testator must understand the nature and extent of their property, the natural objects of their bounty, and the disposition being made. "
            "The court examines medical evidence, witness testimony, and the circumstances of execution."
        ),
        key_factors=[
            "Understanding of property",
            "Awareness of beneficiaries",
            "Knowledge of codicil's effect",
            "Medical and lay evidence",
            "Timing of execution"
        ],
        primary_authority=[
            "Uniform Probate Code § 2-501",
            "Estate of Selb, 433 P.2d 420 (Cal. 1967)"
        ],
        burden_holder="Codicil proponent",
        adversary_position="Contestant asserts incapacity",
        counter_arguments=[
            "Testator was lucid",
            "No evidence of incapacity",
            "Expert testimony supports capacity"
        ],
        resolution_strategy="Apply testamentary capacity standard to codicil execution.",
        entity_scope="Testator",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Estate of Selb, 433 P.2d 420 (Cal. 1967)"
    ),
    DoctrineBlock(
        topic="presumption_of_due_execution",
        keywords=["presumption", "due execution", "will", "attestation", "formalities"],
        conclusion_template="The presumption of due execution {applies/does not apply} to the will.",
        reasoning_framework=(
            "A will that appears regular on its face and is attested by witnesses is presumed duly executed. "
            "The contestant must produce evidence of irregularity to rebut the presumption. "
            "The court examines the will, witness affidavits, and any evidence of improper execution."
        ),
        key_factors=[
            "Facial regularity",
            "Witness attestation",
            "Affidavits",
            "Evidence of irregularity",
            "Statutory requirements"
        ],
        primary_authority=[
            "Uniform Probate Code § 3-406",
            "Estate of Button, 209 Cal. 325 (1930)"
        ],
        burden_holder="Contestant (to rebut presumption)",
        adversary_position="Proponent relies on presumption",
        counter_arguments=[
            "Irregularity in execution",
            "Witnesses not present",
            "Formalities not satisfied"
        ],
        resolution_strategy="Apply presumption unless evidence rebuts; admit will if regular.",
        entity_scope="Testator and witnesses",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Estate of Button, 209 Cal. 325 (1930)"
    ),
    DoctrineBlock(
        topic="attestation_clause_and_self_proving_affidavit",
        keywords=["attestation clause", "self-proving affidavit", "witnesses", "probate", "execution"],
        conclusion_template="The attestation clause and self-proving affidavit {are/are not} sufficient to establish due execution.",
        reasoning_framework=(
            "An attestation clause recites compliance with execution formalities and, if accompanied by a self-proving affidavit, may eliminate the need for witness testimony. "
            "The court examines the language