import enum
from dataclasses import dataclass, field
from typing import List, Optional
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
        topic="Will Validity: Formalities",
        keywords=["will", "validity", "formalities", "execution", "attestation", "signature", "witnesses", "self-proving"],
        conclusion_template="The will is {valid/invalid} due to compliance/noncompliance with statutory formalities.",
        reasoning_framework=(
            "To determine will validity, analyze whether the instrument was executed in compliance with statutory requirements. "
            "Typically, the will must be in writing, signed by the testator (or by another at the testator's direction and in their presence), "
            "and attested by at least two credible witnesses who sign in the testator's presence. "
            "Self-proving affidavits can shift the burden of proof regarding execution. "
            "Substantial compliance may suffice in some jurisdictions, but strict compliance is often required. "
            "Examine whether any interested party acted as a witness, which may affect the disposition to that witness. "
            "Review whether the will was executed under circumstances that satisfy the presence and signature requirements. "
            "Consider harmless error statutes, if applicable, that may excuse minor defects. "
            "Assess whether the will is holographic or nuncupative, and if so, whether those forms are recognized and the requirements met. "
            "If the will is not properly executed, it is invalid unless an exception applies."
        ),
        key_factors=[
            "Presence of testator's signature",
            "Number and credibility of witnesses",
            "Witnesses' signatures in testator's presence",
            "Self-proving affidavit",
            "Interested witness issues",
            "Substantial vs. strict compliance",
            "Jurisdictional recognition of holographic/nuncupative wills",
            "Harmless error statute applicability"
        ],
        primary_authority=[
            "Texas Estates Code §§ 251.051, 251.052, 251.053",
            "In re Estate of Wilson, 252 S.W.3d 708 (Tex. App.—Texarkana 2008, no pet.)",
            "Estate of Brown, 507 S.W.3d 273 (Tex. App.—San Antonio 2016, no pet.)"
        ],
        burden_holder="Proponent of the will",
        adversary_position="Challenger asserts noncompliance with execution formalities",
        counter_arguments=[
            "Substantial compliance with formalities",
            "Harmless error statute applies",
            "Will is holographic and meets requirements",
            "Interested witness did not affect disposition"
        ],
        resolution_strategy="Examine the will and affidavits; apply statutory requirements; consider exceptions and case law.",
        entity_scope="Testator, witnesses, beneficiaries",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Estate of Brown, 507 S.W.3d 273"
    ),
    DoctrineBlock(
        topic="Testamentary Capacity",
        keywords=["testamentary capacity", "mental capacity", "sound mind", "testator", "lucid interval"],
        conclusion_template="The testator {had/did not have} testamentary capacity at the time of execution.",
        reasoning_framework=(
            "Testamentary capacity requires that at the time of execution, the testator understood the nature of the act, "
            "the nature and extent of their property, the natural objects of their bounty, and the disposition they are making. "
            "Capacity is determined at the time of execution, not before or after, though evidence of prior or subsequent condition may be relevant. "
            "A lucid interval may suffice for capacity. "
            "The burden is on the will proponent to show capacity if challenged. "
            "Medical evidence, witness testimony, and the circumstances surrounding execution are considered. "
            "Mere old age, eccentricity, or physical frailty do not negate capacity. "
            "Severe mental illness or delusions affecting the will's provisions may defeat capacity. "
            "The court weighs all evidence to determine if the testator met the legal standard."
        ),
        key_factors=[
            "Testator's understanding of will's nature",
            "Awareness of property and beneficiaries",
            "Evidence of mental illness or delusions",
            "Timing of capacity assessment",
            "Testimony of witnesses and medical professionals"
        ],
        primary_authority=[
            "Texas Estates Code § 251.001",
            "In re Estate of Graham, 69 S.W.3d 598 (Tex. App.—Corpus Christi 2001, no pet.)",
            "In re Estate of Capps, 154 S.W.3d 242 (Tex. App.—Texarkana 2005, no pet.)"
        ],
        burden_holder="Will proponent (if challenged)",
        adversary_position="Challenger alleges lack of capacity",
        counter_arguments=[
            "Testator had a lucid interval",
            "No evidence of incapacity at execution",
            "Testator understood the consequences"
        ],
        resolution_strategy="Review medical and lay testimony; focus on testator's state at execution; apply legal standard.",
        entity_scope="Testator, beneficiaries, heirs",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="In re Estate of Graham, 69 S.W.3d 598"
    ),
    DoctrineBlock(
        topic="Intestate Succession Hierarchy",
        keywords=["intestate", "succession", "heirship", "descent", "distribution", "no will"],
        conclusion_template="The decedent's estate passes to {heirs} according to statutory intestate succession hierarchy.",
        reasoning_framework=(
            "In the absence of a valid will, the estate passes according to the intestate succession statutes. "
            "The hierarchy typically prioritizes surviving spouse, children, descendants, parents, siblings, and more remote relatives. "
            "Community and separate property are distributed differently. "
            "For community property, the surviving spouse often takes all if there are no children or all children are also the spouse's. "
            "Separate property is divided among spouse, children, and parents according to statutory shares. "
            "If no heirs are found, the estate escheats to the state. "
            "Adopted children and, in some cases, children born outside marriage are included. "
            "Half-blood and whole-blood relatives may take different shares. "
            "Heirship proceedings may be necessary to determine rightful heirs."
        ),
        key_factors=[
            "Marital status of decedent",
            "Existence and relationship of children",
            "Type of property (community/separate)",
            "Surviving parents and siblings",
            "Adopted and non-marital children",
            "Heirship affidavits or proceedings"
        ],
        primary_authority=[
            "Texas Estates Code §§ 201.001–201.003",
            "Texas Estates Code §§ 201.051–201.054",
            "Shepherd v. Ledford, 962 S.W.2d 28 (Tex. 1998)"
        ],
        burden_holder="Heir or applicant for administration",
        adversary_position="Other claimants to heirship",
        counter_arguments=[
            "Existence of a valid will",
            "Disqualification of heir (e.g., slayer statute)",
            "Omitted or unknown heirs"
        ],
        resolution_strategy="Apply statutory hierarchy; verify relationships through evidence and heirship proceedings.",
        entity_scope="Heirs, spouse, descendants",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Shepherd v. Ledford, 962 S.W.2d 28"
    ),
    DoctrineBlock(
        topic="Homestead Exemption in Probate",
        keywords=["homestead", "exemption", "probate", "family allowance", "spousal rights", "surviving spouse", "minor children"],
        conclusion_template="The homestead is {exempt/not exempt} from creditors' claims and passes according to probate homestead rules.",
        reasoning_framework=(
            "The homestead is generally exempt from most creditor claims during probate, except for purchase money, taxes, and certain other debts. "
            "The surviving spouse and minor children have the right to occupy the homestead during administration. "
            "The exemption protects the homestead from forced sale for general debts. "
            "Homestead rights are determined by the use and occupancy at the time of death. "
            "The exemption does not prevent partition among heirs after administration, but occupancy rights may persist. "
            "The court may set aside the homestead for the benefit of the family. "
            "Creditors may challenge the exemption if the property does not qualify as a homestead."
        ),
        key_factors=[
            "Nature and use of the property",
            "Surviving spouse or minor children",
            "Type of creditor claim",
            "Homestead designation and occupancy",
            "Compliance with statutory requirements"
        ],
        primary_authority=[
            "Texas Estates Code §§ 102.001–102.007",
            "Texas Property Code §§ 41.001–41.002",
            "Williams v. Williams, 569 S.W.2d 867 (Tex. 1978)"
        ],
        burden_holder="Party asserting exemption",
        adversary_position="Creditor challenges homestead status",
        counter_arguments=[
            "Property does not qualify as homestead",
            "No surviving spouse or minor children",
            "Exemption does not apply to specific debts"
        ],
        resolution_strategy="Determine homestead status; apply statutory exemptions; resolve creditor objections.",
        entity_scope="Surviving spouse, minor children, creditors",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Williams v. Williams, 569 S.W.2d 867"
    ),
    DoctrineBlock(
        topic="Independent Administration",
        keywords=["independent administration", "executor", "administrator", "probate", "court supervision", "letters testamentary"],
        conclusion_template="Independent administration is {available/not available} based on will provisions or court order.",
        reasoning_framework=(
            "Independent administration allows the estate to be administered with minimal court supervision. "
            "A will may expressly authorize independent administration, or all distributees may agree, or the court may order it if in the best interest of the estate. "
            "The independent executor has broad powers to collect assets, pay debts, and distribute property without court approval. "
            "The court issues letters testamentary or of administration. "
            "Interested parties may object to independent administration, but the court may overrule if statutory requirements are met. "
            "The independent executor must still provide notice to creditors and file an inventory, appraisement, and list of claims. "
            "The court may remove the independent executor for cause."
        ),
        key_factors=[
            "Will provisions regarding administration",
            "Agreement of distributees",
            "Court's determination of best interest",
            "Objections by interested parties",
            "Executor's compliance with statutory duties"
        ],
        primary_authority=[
            "Texas Estates Code §§ 401.001–401.007",
            "Texas Estates Code §§ 401.101–401.107",
            "Kappus v. Kappus, 284 S.W.3d 831 (Tex. 2009)"
        ],
        burden_holder="Applicant for independent administration",
        adversary_position="Objecting distributee or creditor",
        counter_arguments=[
            "Will does not authorize independent administration",
            "Not all distributees agree",
            "Independent administration not in estate's best interest"
        ],
        resolution_strategy="Review will and distributee agreements; apply statutory criteria; resolve objections in court.",
        entity_scope="Executor, distributees, court",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Kappus v. Kappus, 284 S.W.3d 831"
    ),
    DoctrineBlock(
        topic="Will Contest: Grounds",
        keywords=["will contest", "undue influence", "fraud", "duress", "mistake", "improper execution"],
        conclusion_template="The will is {valid/invalid} due to {presence/absence} of contestable grounds.",
        reasoning_framework=(
            "A will may be contested on grounds including lack of testamentary capacity, undue influence, fraud, duress, mistake, or improper execution. "
            "Undue influence requires proof that another exerted such influence over the testator that the will reflects the influencer's intent, not the testator's. "
            "Fraud may be in the execution or inducement. "
            "Duress involves threats or coercion. "
            "Mistake may relate to the nature of the instrument or its contents. "
            "Improper execution concerns failure to comply with statutory formalities. "
            "The contestant bears the burden of proof, except for execution formalities, where the proponent must show compliance. "
            "Evidence includes medical records, witness testimony, and circumstances of execution."
        ),
        key_factors=[
            "Testator's vulnerability",
            "Relationship between testator and influencer",
            "Opportunity and motive for undue influence",
            "Evidence of coercion, fraud, or mistake",
            "Compliance with execution formalities"
        ],
        primary_authority=[
            "Texas Estates Code §§ 256.204, 256.202",
            "In re Estate of Johnson, 340 S.W.3d 769 (Tex. App.—San Antonio 2011, pet. denied)",
            "Long v. Long, 133 S.W.3d 726 (Tex. App.—Fort Worth 2003, pet. denied)"
        ],
        burden_holder="Contestant (except for execution formalities)",
        adversary_position="Will proponent asserts validity",
        counter_arguments=[
            "Testator acted freely and knowingly",
            "No evidence of undue influence or fraud",
            "Will executed in compliance with law"
        ],
        resolution_strategy="Analyze evidence for each ground; apply burden of proof; court determines validity.",
        entity_scope="Testator, beneficiaries, contestants",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="In re Estate of Johnson, 340 S.W.3d 769"
    ),
    DoctrineBlock(
        topic="Creditor Claims Priority",
        keywords=["creditor claims", "priority", "payment", "administration expenses", "secured claims", "unsecured claims"],
        conclusion_template="Claims are paid in the following priority: {list of classes}, subject to statutory exceptions.",
        reasoning_framework=(
            "Claims against the estate are paid according to statutory priority. "
            "First are expenses of administration and funeral expenses, followed by secured claims, taxes, and then general unsecured claims. "
            "Secured creditors may elect to have their claims treated as matured secured or preferred debt and lien. "
            "The executor must classify, allow, or reject claims, and pay them in order of priority. "
            "If assets are insufficient, lower-priority claims may go unpaid. "
            "Notice to creditors is required, and claims must be presented within statutory deadlines. "
            "Late or improperly presented claims may be barred."
        ),
        key_factors=[
            "Classification of claims",
            "Timely presentation of claims",
            "Secured creditor election",
            "Sufficiency of estate assets",
            "Executor's allowance or rejection"
        ],
        primary_authority=[
            "Texas Estates Code §§ 355.001–355.009",
            "Texas Estates Code §§ 403.051–403.058",
            "In re Estate of Nash, 220 S.W.3d 914 (Tex. 2007)"
        ],
        burden_holder="Creditor seeking payment",
        adversary_position="Executor or other creditors",
        counter_arguments=[
            "Claim is untimely or defective",
            "Claim is not supported by evidence",
            "Higher-priority claims exhaust estate"
        ],
        resolution_strategy="Classify and prioritize claims; pay in statutory order; resolve disputes in court.",
        entity_scope="Creditors, executor, beneficiaries",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="In re Estate of Nash, 220 S.W.3d 914"
    ),
    DoctrineBlock(
        topic="Elective Share and Spousal Rights",
        keywords=["elective share", "spousal rights", "community property", "forced share", "surviving spouse"],
        conclusion_template="The surviving spouse is {entitled/not entitled} to an elective share or statutory spousal rights.",
        reasoning_framework=(
            "A surviving spouse may have rights to a share of the estate regardless of will provisions. "
            "In community property states, the spouse retains their half of community property. "
            "The spouse may claim homestead rights, family allowance, and exempt property. "
            "If the will attempts to disinherit the spouse, statutory protections may override. "
            "The spouse may elect to take under the will or claim statutory rights. "
            "Waiver of rights may occur via prenuptial or postnuptial agreement. "
            "The court will enforce spousal rights unless validly waived."
        ),
        key_factors=[
            "Marital status at death",
            "Nature of property (community/separate)",
            "Will provisions affecting spouse",
            "Existence of waiver agreements",
            "Statutory spousal protections"
        ],
        primary_authority=[
            "Texas Estates Code §§ 201.002, 201.003",
            "Texas Family Code §§ 3.002, 3.102",
            "Estate of Dillard, 98 S.W.3d 386 (Tex. App.—Amarillo 2003, pet. denied)"
        ],
        burden_holder="Surviving spouse",
        adversary_position="Other heirs or beneficiaries",
        counter_arguments=[
            "Spouse waived rights",
            "Marriage invalid or dissolved",
            "Property is not subject to spousal rights"
        ],
        resolution_strategy="Determine marital status and property type; review will and agreements; apply statutory protections.",
        entity_scope="Surviving spouse, heirs, beneficiaries",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Estate of Dillard, 98 S.W.3d 386"
    ),
    DoctrineBlock(
        topic="Executor's Fiduciary Duties",
        keywords=["executor", "fiduciary duty", "loyalty", "prudence", "accounting", "conflict of interest"],
        conclusion_template="The executor {fulfilled/did not fulfill} fiduciary duties in estate administration.",
        reasoning_framework=(
            "The executor owes fiduciary duties of loyalty, care, and impartiality to the estate and beneficiaries. "
            "The executor must collect and preserve assets, pay debts and taxes, and distribute property according to the will or law. "
            "Self-dealing, conflicts of interest, or failure to account may breach fiduciary duty. "
            "The executor must keep accurate records and provide accountings when required. "
            "Beneficiaries may seek removal or damages for breach. "
            "The court evaluates the executor's conduct against the prudent person standard."
        ),
        key_factors=[
            "Executor's management of estate assets",
            "Disclosure and avoidance of conflicts",
            "Accuracy of accountings",
            "Timeliness of administration",
            "Beneficiary complaints or objections"
        ],
        primary_authority=[
            "Texas Estates Code §§ 351.101–351.104",
            "Texas Estates Code §§ 404.001–404.003",
            "Huie v. DeShazo, 922 S.W.2d 920 (Tex. 1996)"
        ],
        burden_holder="Beneficiary alleging breach",
        adversary_position="Executor defends conduct",
        counter_arguments=[
            "Executor acted in good faith",
            "No loss or harm to estate",
            "Actions authorized by will or court"
        ],
        resolution_strategy="Review executor's actions and records; compare to fiduciary standards; court may order remedies.",
        entity_scope="Executor, beneficiaries, court",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Huie v. DeShazo, 922 S.W.2d 920"
    ),
    DoctrineBlock(
        topic="Pour-Over Will and Trust Integration",
        keywords=["pour-over will", "trust", "integration", "revocable trust", "testamentary trust", "incorporation"],
        conclusion_template="The pour-over provision is {effective/ineffective} to transfer assets to the trust.",
        reasoning_framework=(
            "A pour-over will directs assets to a trust upon death. "
            "The trust must be identified in the will and exist at the time of execution or be created concurrently. "
            "The doctrine of incorporation by reference may apply if the trust is sufficiently described. "
            "The trust may be revocable or irrevocable. "
            "Assets pour over into the trust and are distributed according to its terms. "
            "The pour-over provision is valid if statutory and common law requirements are met. "
            "Failure to properly identify or create the trust may invalidate the provision."
        ),
        key_factors=[
            "Existence and identification of trust",
            "Timing of trust creation",
            "Language of pour-over provision",
            "Compliance with incorporation by reference",
            "Jurisdictional recognition of pour-over wills"
        ],
        primary_authority=[
            "Texas Estates Code § 254.001",
            "Restatement (Third) of Property: Wills and Other Donative Transfers § 3.8",
            "In re Estate of Canales, 837 S.W.2d 662 (Tex. App.—San Antonio 1992, no writ)"
        ],
        burden_holder="Proponent of pour-over provision",
        adversary_position="Challenger disputes trust's existence or identification",
        counter_arguments=[
            "Trust not properly identified",
            "Trust not in existence at execution",
            "Provision fails for lack of certainty"
        ],
        resolution_strategy="Examine will and trust documents; apply statutory and common law requirements.",
        entity_scope="Testator, trustee, beneficiaries",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="In re Estate of Canales, 837 S.W.2d 662"
    ),
    DoctrineBlock(
        topic="Muniment of Title",
        keywords=["muniment of title", "probate", "no administration", "title transfer", "will"],
        conclusion_template="Probate as a muniment of title is {appropriate/inappropriate} under the circumstances.",
        reasoning_framework=(
            "Probate as a muniment of title is available when there are no unpaid debts (other than secured debts, taxes, or administration expenses) "
            "and no need for formal administration. "
            "The will is admitted to probate solely to establish title to estate property. "
            "The applicant must prove the absence of debts and that the will is valid. "
            "Creditors may object if debts are outstanding. "
            "The court issues an order admitting the will as a muniment of title, which may be used to transfer property. "
            "If later debts are discovered, administration may be reopened."
        ),
        key_factors=[
            "Existence of unpaid debts",
            "Validity of the will",
            "Applicant's relationship to the estate",
            "Need for administration",
            "Objections by creditors"
        ],
        primary_authority=[
            "Texas Estates Code §§ 257.001–257.103",
            "In re Estate of Kurtz, 54 S.W.3d 353 (Tex. App.—Waco 2001, pet. denied)"
        ],
        burden_holder="Applicant for muniment of title",
        adversary_position="Creditor or interested party objects",
        counter_arguments=[
            "Unpaid debts exist",
            "Will is invalid",
            "Formal administration is necessary"
        ],
        resolution_strategy="Verify absence of debts; confirm will validity; court determines appropriateness.",
        entity_scope="Heirs, beneficiaries, creditors",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="In re Estate of Kurtz, 54 S.W.3d 353"
    ),
    DoctrineBlock(
        topic="Ademption and Abatement",
        keywords=["ademption", "abatement", "specific devise", "general devise", "insufficient assets", "bequest"],
        conclusion_template="The gift is {adeemed/not adeemed} or {abated/not abated} due to {facts}.",
        reasoning_framework=(
            "Ademption occurs when specifically devised property is not in the estate at death; the gift fails unless statute provides otherwise. "
            "Abatement is the reduction of gifts when estate assets are insufficient to pay debts, expenses, and all bequests. "
            "Specific devises abate last, general and residuary devises abate first. "
            "Intent of the testator is considered in ademption, but strict rules often apply. "
            "Statutes may provide for replacement property or proceeds in some cases. "
            "Abatement order is set by statute unless the will provides otherwise."
        ),
        key_factors=[
            "Nature of the devise (specific/general/residuary)",
            "Existence of property at death",
            "Testator's intent",
            "Sufficiency of estate assets",
            "Statutory abatement order"
        ],
        primary_authority=[
            "Texas Estates Code §§ 255.001–255.103",
            "In re Estate of Dillard, 98 S.W.3d 386 (Tex. App.—Amarillo 2003, pet. denied)",
            "Restatement (Third) of Property: Wills § 5.2"
        ],
        burden_holder="Beneficiary claiming gift",
        adversary_position="Executor or other beneficiaries",
        counter_arguments=[
            "Gift is adeemed by extinction",
            "Gift abates under statutory order",
            "Testator intended different result"
        ],
        resolution_strategy="Determine nature of devise; apply ademption and abatement rules; consider testator's intent and statutory exceptions.",
        entity_scope="Beneficiaries, executor",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="In re Estate of Dillard, 98 S.W.3d 386"
    ),
    DoctrineBlock(
        topic="Will Interpretation and Testator's Intent",
        keywords=["will interpretation", "testator's intent", "ambiguity", "construction", "extrinsic evidence"],
        conclusion_template="The will is interpreted to mean: {interpretation}, based on testator's intent.",
        reasoning_framework=(
            "The paramount rule in will interpretation is to ascertain and effectuate the testator's intent as expressed in the will. "
            "The court examines the entire instrument, giving effect to every provision if possible. "
            "If language is unambiguous, the plain meaning controls. "
            "If ambiguous, extrinsic evidence may be admitted to determine intent. "
            "No provision is ignored if a reasonable construction exists. "
            "Technical rules yield to clear intent. "
            "Surrounding circumstances at execution may be considered if ambiguity exists."
        ),
        key_factors=[
            "Language of the will",
            "Existence of ambiguity",
            "Testator's circumstances and relationships",
            "Consistency with overall plan",
            "Admissibility of extrinsic evidence"
        ],
        primary_authority=[
            "San Antonio Area Foundation v. Lang, 35 S.W.3d 636 (Tex. 2000)",
            "Shriner's Hospital v. Stahl, 610 S.W.2d 147 (Tex. 1980)",
            "Texas Estates Code § 255.151"
        ],
        burden_holder="Party seeking particular interpretation",
        adversary_position="Opposing party asserts different meaning",
        counter_arguments=[
            "Plain meaning is clear and unambiguous",
            "Extrinsic evidence is inadmissible",
            "Alternative construction better fits intent"
        ],
        resolution_strategy="Analyze will language; admit extrinsic evidence if ambiguous; effectuate testator's intent.",
        entity_scope="Beneficiaries, executor, court",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="San Antonio Area Foundation v. Lang, 35 S.W.3d 636"
    ),
    DoctrineBlock(
        topic="Heirship Determination",
        keywords=["heirship", "determination", "intestate", "proceeding", "affidavit of heirship"],
        conclusion_template="The following individuals are determined to be heirs: {list of heirs}.",
        reasoning_framework=(
            "Heirship determination is necessary when a person dies intestate or when the heirs are unclear. "
            "A court proceeding may be required to establish the identity and shares of heirs. "
            "Affidavits of heirship may be used for real property but are not conclusive. "
            "The court considers evidence of familial relationships, marriage, children, and prior deaths. "
            "Heirship may be challenged by interested parties. "
            "The court's judgment is binding as to the rights of heirs."
        ),
        key_factors=[
            "Evidence of family relationships",
            "Marital status and children",
            "Prior deaths and survivorship",
            "Affidavits and testimony",
            "Challenges by interested parties"
        ],
        primary_authority=[
            "Texas Estates Code §§ 202.001–202.206",
            "Texas Estates Code §§ 203.001–203.002",
            "In re Estate of Claveria, 615 S.W.2d 164 (Tex. 1981)"
        ],
        burden_holder="Applicant for heirship determination",
        adversary_position="Challenger to heirship",
        counter_arguments=[
            "Omitted or unknown heirs",
            "Disqualification of claimed heir",
            "Contradictory evidence"
        ],
        resolution_strategy="Gather and present evidence; court determines heirship and shares.",
        entity_scope="Heirs, court, interested parties",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="In re Estate of Claveria, 615 S.W.2d 164"
    ),
    DoctrineBlock(
        topic="Anti-Lapse Statute",
        keywords=["anti-lapse", "statute", "predeceased beneficiary", "descendants", "substitute gift"],
        conclusion_template="The gift {lapses/passes to descendants} under the anti-lapse statute.",
        reasoning_framework=(
            "If a will beneficiary predeceases the testator, the gift may lapse unless the anti-lapse statute applies. "
            "The statute saves gifts to certain relatives (e.g., descendants of testator's parents) by substituting their descendants. "
            "If the will provides a contrary intent, the statute does not apply. "
            "The court examines the relationship of the beneficiary, will language, and survivorship requirements. "
            "If no substitute takers exist, the gift falls into the residue or passes by intestacy."
        ),
        key_factors=[
            "Relationship of beneficiary to testator",
            "Existence of descendants",
            "Will language regarding lapse or substitution",
            "Jurisdictional anti-lapse statute",
            "Survivorship requirements"
        ],
        primary_authority=[
            "Texas Estates Code § 255.153",
            "Restatement (Third) of Property: Wills § 5.5",
            "In re Estate of Deneve, 341 S.W.3d 391 (Tex. App.—Amarillo 2011, pet. denied)"
        ],
        burden_holder="Beneficiary's descendants",
        adversary_position="Other beneficiaries or heirs",
        counter_arguments=[
            "Will expresses contrary intent",
            "No qualifying descendants",
            "Gift lapses into residue"
        ],
        resolution_strategy="Determine relationship and will language; apply anti-lapse statute if applicable.",
        entity_scope="Beneficiaries, descendants, heirs",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="In re Estate of Deneve, 341 S.W.3d 391"
    ),
    DoctrineBlock(
        topic="Small Estate Affidavit",
        keywords=["small estate", "affidavit", "summary procedure", "no administration", "value threshold"],
        conclusion_template="A small estate affidavit is {appropriate/inappropriate} for estate transfer.",
        reasoning_framework=(
            "A small estate affidavit allows transfer of property without formal administration if the estate value is below a statutory threshold "
            "and the decedent died intestate. "
            "The affidavit must list all assets, debts, and heirs, and be sworn to by two disinterested witnesses. "
            "It cannot be used to transfer real property except the homestead. "
            "The court must approve the affidavit. "
            "Creditors may object if debts are not paid. "
            "If requirements are not met, formal administration is necessary."
        ),
        key_factors=[
            "Estate value below statutory limit",
            "No will",
            "All heirs join in affidavit",
            "No unpaid debts except secured debts",
            "Court approval"
        ],
        primary_authority=[
            "Texas Estates Code §§ 205.001–205.008",
            "In re Estate of Loveless, 64 S.W.3d 564 (Tex. App.—Texarkana 2001, no pet.)"
        ],
        burden_holder="Applicant for small estate affidavit",
        adversary_position="Creditor or omitted heir",
        counter_arguments=[
            "Estate exceeds value limit",
            "Not all heirs join",
            "Unpaid debts exist"
        ],
        resolution_strategy="Verify statutory requirements; obtain court approval; resolve objections.",
        entity_scope="Heirs, creditors, court",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="In re Estate of Loveless, 64 S.W.3d 564"
    ),
    # Additional doctrine blocks for depth and coverage
    DoctrineBlock(
        topic="Lost or Destroyed Will",
        keywords=["lost will", "destroyed will", "probate", "secondary evidence", "presumption of revocation"],
        conclusion_template="The lost or destroyed will is {admitted/not admitted} to probate.",
        reasoning_framework=(
            "A lost or destroyed will may be admitted to probate if its contents and due execution are proved by credible evidence. "
            "There is a presumption that a will last in the testator's possession and not found was revoked. "
            "The proponent must rebut the presumption by clear and convincing evidence. "
            "Secondary evidence, such as copies or witness testimony, may be used to establish the will's terms. "
            "The court must be satisfied that the will was not revoked and that its contents are established."
        ),
        key_factors=[
            "Evidence of due execution",
            "Proof of contents",
            "Circumstances of loss or destruction",
            "Rebuttal of revocation presumption",
            "Testimony of witnesses"
        ],
        primary_authority=[
            "Texas Estates Code §§ 256.156–256.157",
            "In re Estate of Standefer, 541 S.W.3d 320 (Tex. App.—Fort Worth 2017, no pet.)"
        ],
        burden_holder="Proponent of lost will",
        adversary_position="Challenger asserts revocation",
        counter_arguments=[
            "Will was revoked by destruction",
            "Insufficient evidence of contents",
            "Improper execution"
        ],
        resolution_strategy="Gather credible evidence; rebut presumption of revocation; satisfy statutory requirements.",
        entity_scope="Testator, beneficiaries, court",
        confidence=0.85,
        confidence_zone="Medium",
        controlling_precedent="In re Estate of Standefer, 541 S.W.3d 320"
    ),
    DoctrineBlock(
        topic="No-Contest Clause Enforcement",
        keywords=["no-contest clause", "in terrorem", "will contest", "forfeiture", "good faith"],
        conclusion_template="The no-contest clause is {enforced/not enforced} against the contestant.",
        reasoning_framework=(
            "A no-contest (in terrorem) clause seeks to penalize beneficiaries who contest the will. "
            "Such clauses are generally enforceable, but not if the contest is brought in good faith and with just cause. "
            "The court examines the nature of the contest, the beneficiary's motives, and the evidence supporting the challenge. "
            "If the contest is frivolous or in bad faith, the clause is enforced. "
            "If the contest is reasonable and based on probable cause, the clause may not be enforced."
        ),
        key_factors=[
            "Language of the no-contest clause",
            "Nature of the contest",
            "Good faith and just cause",
            "Evidence supporting contest",
            "Court's discretion"
        ],
        primary_authority=[
            "Texas Estates Code § 254.005",
            "Badouh v. Hale, 22 S.W.3d 392 (Tex. 2000)"
        ],
        burden_holder="Proponent of forfeiture",
        adversary_position="Contestant asserts good faith",
        counter_arguments=[
            "Contest brought in good faith and with just cause",
            "Clause is ambiguous or unenforceable",
            "Contest does not trigger clause"
        ],
        resolution_strategy="Analyze contest and clause; determine good faith and just cause; apply statute and precedent.",
        entity_scope="Beneficiaries, contestants, court",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Badouh v. Hale, 22 S.W.3d 392"
    ),
    DoctrineBlock(
        topic="Self-Proving Affidavit",
        keywords=["self-proving affidavit", "will execution", "witnesses", "presumption of validity"],
        conclusion_template="The will is {self-proved/not self-proved} by affidavit.",
        reasoning_framework=(
            "A self-proving affidavit attached to a will creates a presumption of due execution, "
            "eliminating the need for witness testimony unless contested. "
            "The affidavit must be executed contemporaneously with the will or thereafter, "
            "and must be signed by the testator and witnesses before a notary. "
            "If the affidavit is defective or missing, witnesses may be required to prove execution."
        ),
        key_factors=[
            "Presence and form of affidavit",
            "Signatures of testator and witnesses",
            "Notarization",
            "Timing of execution",
            "Challenge to execution"
        ],
        primary_authority=[
            "Texas Estates Code §§ 251.1045, 251.104",
            "In re Estate of Silverman, 631 S.W.2d 332 (Tex. App.—Dallas 1982, writ ref'd n.r.e.)"
        ],
        burden_holder="Will proponent",
        adversary_position="Challenger disputes execution",
        counter_arguments=[
            "Affidavit is missing or defective",
            "Witnesses are unavailable",
            "Execution not in compliance with law"
        ],
        resolution_strategy="Review affidavit; confirm compliance with statutory requirements; call witnesses if necessary.",
        entity_scope="Testator, witnesses, beneficiaries",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="In re Estate of Silverman, 631 S.W.2d 332"
    ),
    DoctrineBlock(
        topic="Revocation of Will",
        keywords=["will revocation", "physical act", "subsequent instrument", "intent", "presumption"],
        conclusion_template="The will is {revoked/not revoked} by {act or subsequent instrument}.",
        reasoning_framework=(
            "A will may be revoked by a subsequent will or codicil, or by physical act (e.g., destruction) with intent to revoke. "
            "Revocation by physical act requires proof of destruction and intent. "
            "If the will was last in the testator's possession and cannot be found, a presumption of revocation arises. "
            "A subsequent will may revoke expressly or by inconsistency. "
            "Revocation may be partial or total. "
            "The burden is on the party asserting revocation."
        ),
        key_factors=[
            "Existence of subsequent instrument",
            "Evidence of destruction",
            "Testator's intent",
            "Possession and custody of will",
            "Presumption of revocation"
        ],
        primary_authority=[
            "Texas Estates Code §§ 253.002, 253.003",
            "In re Estate of Glover, 744 S.W.2d 939 (Tex. 1988)"
        ],
        burden_holder="Party asserting revocation",
        adversary_position="Will proponent",
        counter_arguments=[
            "No intent to revoke",
            "Will destroyed by another without consent",
            "Subsequent instrument is invalid"
        ],
        resolution_strategy="Examine evidence of revocation; apply statutory and common law rules.",
        entity_scope="Testator, beneficiaries, court",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="In re Estate of Glover, 744 S.W.2d 939"
    ),
    DoctrineBlock(
        topic="Dependent Relative Revocation",
        keywords=["dependent relative revocation", "revocation", "mistake", "conditional revocation", "failed disposition"],
        conclusion_template="The doctrine of dependent relative revocation {applies/does not apply} to revive the prior will.",
        reasoning_framework=(
            "Dependent relative revocation (DRR) is an equitable doctrine that disregards a revocation if the testator revoked a will under a mistaken belief "
            "that a new disposition would be effective, but the new disposition fails. "
            "The court must find that the testator would not have revoked the prior will but for the mistaken belief. "
            "DRR applies only if the evidence of mistake and intent is clear. "
            "If DRR applies, the prior will or provision is revived."
        ),
        key_factors=[
            "Evidence of testator's mistake",
            "Intent regarding revocation",
            "Failure of new disposition",
            "Existence of prior will",
            "Equitable considerations"
        ],
        primary_authority=[
            "Restatement (Third) of Property: Wills § 4.3",
            "In re Estate of Allen, 407 S.W.3d 335 (Tex. App.—Eastland 2013, no pet.)"
        ],
        burden_holder="Proponent of prior will",
        adversary_position="Proponent of revocation",
        counter_arguments=[
            "No mistake or conditional intent",
            "Testator intended absolute revocation",
            "Evidence is insufficient"
        ],
        resolution_strategy="Analyze evidence of intent and mistake; apply DRR if equitable.",
        entity_scope="Testator, beneficiaries, court",
        confidence=0.87,
        confidence_zone="Medium",
        controlling_precedent="In re Estate of Allen, 407 S.W.3d 335"
    ),
    DoctrineBlock(
        topic="Pretermitted Child Statute",
        keywords=["pretermitted child", "omitted child", "statute", "will", "inheritance"],
        conclusion_template="The pretermitted child is {entitled/not entitled} to a share of the estate.",
        reasoning_framework=(
            "A pretermitted child is a child born or adopted after the execution of the will and not provided for or mentioned in the will. "
            "The statute provides that such a child is entitled to a share as if the testator had died intestate, unless the will indicates otherwise "
            "or the child is otherwise provided for. "
            "The court examines will language, timing of birth or adoption, and evidence of other provision."
        ),
        key_factors=[
            "Timing of child's birth or adoption",
            "Will provisions regarding children",
            "Evidence of other provision",
            "Testator's intent",
            "Statutory requirements"
        ],
        primary_authority=[
            "Texas Estates Code §§ 255.051–255.054",
            "In re Estate of Slaughter, 305 S.W.3d 804 (Tex. App.—Texarkana 2010, no pet.)"
        ],
        burden_holder="Pretermitted child or representative",
        adversary_position="Other beneficiaries",
        counter_arguments=[
            "Child provided for outside the will",
            "Will expressly excludes after-born children",
            "Child not pretermitted under statute"
        ],
        resolution_strategy="Determine status of child; review will and other evidence; apply statute.",
        entity_scope="Children, beneficiaries, executor",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="In re Estate of Slaughter, 305 S.W.3d 804"
    ),
    DoctrineBlock(
        topic="Simultaneous Death Act",
        keywords=["simultaneous death", "commorientes", "survivorship", "120-hour rule", "distribution"],
        conclusion_template="The Simultaneous Death Act {applies/does not apply}, and property passes accordingly.",
        reasoning_framework=(
            "If it cannot be established by clear and convincing evidence that one person survived another by 120 hours, "
            "each is deemed to have predeceased the other for purposes of inheritance. "
            "This prevents property from passing from one decedent to another and then to the other's heirs. "
            "The 120-hour rule applies unless the will provides otherwise. "
            "The court examines evidence of survivorship and will language."
        ),
        key_factors=[
            "Evidence of survivorship",
            "Will provisions regarding survivorship",
            "Application of 120-hour rule",
            "Effect on distribution",
            "Statutory exceptions"
        ],
        primary_authority=[
            "Texas Estates Code §§ 121.001–121.152",
            "Janus v. Tarasewicz, 484 N.E.2d 797 (Ill. 1985)"
        ],
        burden_holder="Party asserting survivorship",
        adversary_position="Opposing party asserts simultaneous death",
        counter_arguments=[
            "No clear and convincing evidence of survivorship",
            "Will overrides statutory rule",
            "Rule does not affect distribution"
        ],
        resolution_strategy="Review evidence and will; apply 120-hour rule unless overridden.",
        entity_scope="Heirs, beneficiaries, executor",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Texas Estates Code § 121.052"
    ),
    DoctrineBlock(
        topic="Disinheritance and Negative Bequests",
        keywords=["disinheritance", "negative bequest", "will", "intestate succession"],
        conclusion_template="The disinherited individual {takes/does not take} under the will or by intestacy.",
        reasoning_framework=(
            "A will may expressly disinherit an individual, known as a negative bequest. "
            "The statute gives effect to negative bequests, so the disinherited person is treated as having predeceased the testator "
            "for purposes of distribution. "
            "The court examines will language and applies the statute to intestate shares. "
            "If the will is silent or ambiguous, the court may look to extrinsic evidence."
        ),
        key_factors=[
            "Express language of disinheritance",
            "Relationship to testator",
            "Statutory effect of negative bequest",
            "Distribution of omitted shares",
            "Ambiguity or silence in will"
        ],
        primary_authority=[
            "Texas Estates Code § 255.451",
            "Restatement (Third) of Property: Wills § 3.5"
        ],
        burden_holder="Party asserting disinheritance",
        adversary_position="Disinherited individual",
        counter_arguments=[
            "Will is ambiguous or silent",
            "Statute does not apply",
            "Disinheritance is contrary to public policy"
        ],
        resolution_strategy="Review will and statute; treat disinherited person as predeceased; distribute accordingly.",
        entity_scope="Heirs, beneficiaries, executor",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Texas Estates Code § 255.451"
    ),
    DoctrineBlock(
        topic="Slayer Statute",
        keywords=["slayer statute", "forfeiture", "homicide", "public policy", "bar to inheritance"],
        conclusion_template="The slayer is {barred/not barred} from inheriting from the decedent.",
        reasoning_framework=(
            "A person who unlawfully and intentionally kills the decedent is barred from inheriting under the slayer statute. "
            "The court requires proof of unlawful and intentional killing. "
            "The slayer is treated as having predeceased the decedent for purposes of distribution. "
            "Conviction is strong evidence but not required; civil standard of proof applies. "
            "The statute enforces public policy against profiting from wrongdoing."
        ),
        key_factors=[
            "Proof of unlawful and intentional killing",
            "Criminal conviction or civil finding",
            "Relationship to decedent",
            "Effect on distribution",
            "Public policy considerations"
        ],
        primary_authority=[
            "Texas Estates Code § 201.058",
            "Restatement (Third) of Property: Wills § 8.4",
            "In re Estate of Stafford, 244 S.W.3d 368 (Tex. App.—Beaumont 2007, no pet.)"
        ],
        burden_holder="Party asserting bar to inheritance",
        adversary_position="Alleged slayer",
        counter_arguments=[
            "Killing was not intentional or unlawful",
            "Insufficient proof",
            "Statute does not apply"
        ],
        resolution_strategy="Review evidence of killing; apply statute; treat slayer as predeceased.",
        entity_scope="Heirs, beneficiaries, executor",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="In re Estate of Stafford, 244 S.W.3d 368"
    ),
    DoctrineBlock(
        topic="Advancements Against Inheritance",
        keywords=["advancement", "inheritance", "intestate", "lifetime gift", "hotchpot"],
        conclusion_template="The lifetime gift is {an advancement/not an advancement} against the heir's share.",
        reasoning_framework=(
            "A lifetime gift is treated as an advancement against an heir's intestate share if declared in writing by the decedent "
            "or acknowledged in writing by the heir. "
            "The value of the advancement is added to the estate for distribution (hotchpot) and deducted from the heir's share. "
            "If the advancement exceeds the share, the heir takes nothing but is not required to return the excess. "
            "The court examines evidence of intent and documentation."
        ),
        key_factors=[
            "Written declaration or acknowledgment",
            "Value of advancement",
            "Relationship to intestate share",
            "Evidence of intent",
            "Effect on distribution"
        ],
        primary_authority=[
            "Texas Estates Code §§ 201.151–201.152",
            "Restatement (Third) of Property: Wills § 2.6"
        ],
        burden_holder="Party asserting advancement",
        adversary_position="Heir disputes advancement",
        counter_arguments=[
            "No written declaration or acknowledgment",
            "Gift was not intended as advancement",
            "Statute does not apply"
        ],
        resolution_strategy="Review documentation and evidence; apply statutory rules.",
        entity_scope="Heirs, executor, court",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="Texas Estates Code §§ 201.151–201.152"
    ),
    DoctrineBlock(
        topic="Renunciation and Disclaimer of Interest",
        keywords=["disclaimer", "renunciation", "interest", "beneficiary", "estate"],
        conclusion_template="The beneficiary's disclaimer is {valid/invalid}, and interest passes accordingly.",
        reasoning_framework=(
            "A beneficiary may disclaim or renounce an interest in the estate by a written, signed, and filed disclaimer. "
            "The disclaimer must be filed within nine months of death or as required by statute. "
            "A valid disclaimer is irrevocable and relates back to the date of death. "
            "The disclaimed interest passes as if the disclaimant predeceased the decedent. "
            "The court examines compliance with statutory requirements and the effect on distribution."
        ),
        key_factors=[
            "Form and timing of disclaimer",
            "Compliance with statutory requirements",
            "Effect on distribution",
            "Irrevocability",
            "Notice to interested parties"
        ],
        primary_authority=[
            "Texas Estates Code §§ 122.001–122.107",
            "Internal Revenue Code § 2518",
            "In re Estate of Parr, 993 S.W.2d 887 (Tex. App.—Corpus Christi 1999, no pet.)"
        ],
        burden_holder="Beneficiary or party asserting disclaimer",
        adversary_position="Other beneficiaries or creditors",
        counter_arguments=[
            "Disclaimer is untimely or defective",
            "Disclaimant accepted benefits",
            "Statute does not apply"
        ],
        resolution_strategy="Review disclaimer document; confirm statutory compliance; distribute as if disclaimant predeceased.",
        entity_scope="Beneficiaries, executor, court",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="In re Estate of Parr, 993 S.W.2d 887"
    ),
    DoctrineBlock(
        topic="Omitted Spouse",
        keywords=["omitted spouse", "marriage after will", "statute", "inheritance"],
        conclusion_template="The omitted spouse is {entitled/not entitled} to a share of the estate.",
        reasoning_framework=(
            "Some jurisdictions provide for an omitted spouse—one who marries the testator after execution of the will and is not provided for. "
            "Texas does not have a specific omitted spouse statute, but community property rights and spousal protections may apply. "
            "The court examines will language, timing of marriage, and statutory spousal rights."
        ),
        key_factors=[
            "Timing of marriage",
            "Will provisions regarding spouse",
            "Community property rights",
            "Statutory spousal protections",
            "Evidence of intent"
        ],
        primary_authority=[
            "Texas Estates Code §§ 201.002, 201.003",
            "Texas Family Code §§ 3.002, 3.102"
        ],
        burden_holder="Omitted spouse or representative",
        adversary_position="Other beneficiaries",
        counter_arguments=[
            "Spouse provided for in will",
            "Marriage occurred before will execution",
            "Statute does not apply"
        ],
        resolution_strategy="Determine marital status and timing; review will and statutes; apply spousal rights.",
        entity_scope="Spouse, beneficiaries, executor",
        confidence=0.85,
        confidence_zone="Medium",
        controlling_precedent="Texas Estates Code §§ 201.002, 201.003"
    ),
    DoctrineBlock(
        topic="Family Allowance",
        keywords=["family allowance", "probate", "support", "surviving spouse", "minor children"],
        conclusion_template="A family allowance is {granted/denied} to the surviving spouse or minor children.",
        reasoning_framework=(
            "The court may set aside a reasonable allowance for the support of the surviving spouse and minor children during estate administration. "
            "The allowance is in addition to homestead and exempt property. "
            "The court considers the needs of the family and the resources available. "
            "The allowance has priority over most debts except secured claims. "
            "The executor must pay the allowance as ordered by the court."
        ),
        key_factors=[
            "Needs of surviving spouse and minor children",
            "Resources available",
            "Amount and duration of allowance",
            "Priority over debts",
            "Court order"
        ],
        primary_authority=[
            "Texas Estates Code §§ 353.101–353.107",
            "In re Estate of Brown, 507 S.W.3d 273 (Tex. App.—San Antonio 2016, no pet.)"
        ],
        burden_holder="Applicant for allowance",
        adversary_position="Creditor or other interested party",
        counter_arguments=[
            "Sufficient resources exist",
            "Allowance is excessive",
            "Statute does not apply"
        ],
        resolution_strategy="Assess needs and resources; court sets allowance; executor pays as ordered.",
        entity_scope="Surviving spouse, minor children, executor",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="In re Estate of Brown, 507 S.W.3d 273"
    ),
    DoctrineBlock(
        topic="Exempt Property Set-Aside",
        keywords=["exempt property", "set-aside", "probate", "surviving spouse", "minor children"],
        conclusion_template="Exempt property is {set aside/not set aside} for the benefit of the family.",
        reasoning_framework=(
            "Certain property is exempt from creditors and must be set aside for the surviving spouse and minor children during administration. "
            "Exempt property includes homestead, household furnishings, and other items listed by statute. "
            "The executor must identify and set aside exempt property. "
            "The court may resolve disputes regarding the nature or value of exempt property."
        ),
        key_factors=[
            "Nature and value of property",
            "Family's needs",
            "Statutory list of exempt items",
            "Executor's compliance",
            "Creditor claims"
        ],
        primary_authority=[
            "Texas Estates Code §§ 353.051–353.054",
            "Texas Property Code §§ 42.001–42.002"
        ],
        burden_holder="Surviving spouse or minor children",
        adversary_position="Creditor or other interested party",
        counter_arguments=[
            "Property is not exempt",
            "Statutory requirements not met",
            "Family is not entitled"
        ],
        resolution_strategy="Identify exempt property; set aside as required; resolve disputes in court.",
        entity_scope="Surviving spouse, minor children, executor",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Texas Estates Code §§ 353.051–353.054"
    ),
    DoctrineBlock(
        topic="Ancillary Probate",
        keywords=["ancillary probate", "foreign will", "out-of-state assets", "domicile", "Texas property"],
        conclusion_template="Ancillary probate is {required/not required} for out-of-state decedent's Texas assets.",
        reasoning_framework=(
            "Ancillary probate is used to administer property located in Texas when the decedent was domiciled elsewhere. "
            "A foreign will may be admitted to probate in Texas if it is valid under the law of the domicile. "
            "The court may require authentication of the will and evidence of its validity. "
            "Ancillary administration is limited to Texas assets."
        ),
        key_factors=[
            "Decedent's domicile",
            "Location of assets",
            "Validity of foreign will",
            "Authentication requirements",
            "Scope of administration"
        ],
        primary_authority=[
            "Texas Estates Code §§ 501.001–501.101",
            "Texas Estates Code §§ 503.001–503.007"
        ],
        burden_holder="Applicant for ancillary probate",
        adversary_position="Challenger to foreign will",
        counter_arguments=[
            "Will is invalid under domicile law",
            "Assets are not located in Texas",
            "Authentication is insufficient"
        ],
        resolution_strategy="Authenticate foreign will; limit administration to Texas assets; comply with statutory requirements.",
        entity_scope="Executor, beneficiaries, court",
        confidence=0.87,
        confidence_zone="Medium",
        controlling_precedent="Texas Estates Code §§ 501.001–501.101"
    ),
    DoctrineBlock(
        topic="Appointment of Temporary Administrator",
        keywords=["temporary administrator", "probate", "emergency", "preservation of estate"],
        conclusion_template="A temporary administrator is {appointed/not appointed} to preserve the estate.",
        reasoning_framework=(
            "A temporary administrator may be appointed when immediate action is necessary to preserve the estate or protect interested parties. "
            "The appointment is limited in scope and duration. "
            "The applicant must show necessity and urgency. "
            "The court specifies the powers and duties of the temporary administrator."
        ),
        key_factors=[
            "Necessity and urgency",
            "Risk to estate assets",
            "Scope and duration of appointment",
            "Applicant's qualifications",
            "Court's discretion"
        ],
        primary_authority=[
            "Texas Estates Code §§ 452.001–452.006",
            "In re Estate of Padilla, 103 S.W.3d 563 (Tex. App.—San Antonio 2003, no pet.)"
        ],
        burden_holder="Applicant for temporary administration",
        adversary_position="Interested party objects",
        counter_arguments=[
            "No emergency exists",
            "Permanent administration is preferable",
            "Applicant is unqualified"
        ],
        resolution_strategy="Assess need for temporary administration; court determines appointment and powers.",
        entity_scope="Administrator, court, interested parties",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="In re Estate of Padilla, 103 S.W.3d 563"
    ),
    DoctrineBlock(
        topic="Removal of Executor or Administrator",
        keywords=["removal", "executor", "administrator", "misconduct", "neglect", "probate"],
        conclusion_template="The executor/administrator is {removed/not removed} for cause.",
        reasoning_framework=(
            "The court may remove an executor or administrator for cause, including mismanagement, neglect, conflict of interest, or incapacity. "
            "Interested parties may petition for removal. "
            "The court considers evidence of misconduct and the best interests of the estate. "
            "Removal may be with or without notice, depending on circumstances."
        ),
        key_factors=[
            "Evidence of misconduct or neglect",
            "Conflict of interest",
            "Impact on estate",
            "Notice and hearing",
            "Court's discretion"
        ],
        primary_authority=[
            "Texas Estates Code §§ 404.003–404.004",
            "In re Estate of Miller, 243 S.W.3d 831 (Tex. App.—Dallas 2008, no pet.)"
        ],
        burden_holder="Party seeking removal",
        adversary_position="Executor/administrator",
        counter_arguments=[
            "No cause for removal",
            "Executor acted in good faith",
            "Removal not in estate's best interest"
        ],
        resolution_strategy="Present evidence; court determines removal based on statutory grounds.",
        entity_scope="Executor, administrator, court",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="In re Estate of Miller, 243 S.W.3d 831"
    ),
    DoctrineBlock(
        topic="Bond Requirement for Personal Representative",
        keywords=["bond", "personal representative", "executor", "administrator", "surety"],
        conclusion_template="A bond is {required/waived} for the personal representative.",
        reasoning_framework=(
            "A personal representative must generally post bond to ensure faithful performance of duties, unless waived by the will or court. "
            "The court sets the amount and approves the surety. "
            "The bond protects beneficiaries and creditors. "
            "The court may waive the bond for independent executors if the will so provides or all distributees agree."
        ),
        key_factors=[
            "Will provisions regarding bond",
            "Court's discretion",
            "Agreement of distributees",
            "Nature of administration",
            "Protection of estate"
        ],
        primary_authority=[
            "Texas Estates Code §§ 305.001–305.006",
            "Texas Estates Code §§ 401.005–401.006"
        ],
        burden_holder="Personal representative",
        adversary_position="Interested party objects to waiver",
        counter_arguments=[
            "Bond is necessary for protection",
            "Will does not waive bond",
            "Court should require bond"
        ],
        resolution_strategy="Review will and agreements; court determines bond requirement.",
        entity_scope="Personal representative, beneficiaries, court",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Texas Estates Code §§ 305.001–305.006"
    ),
    DoctrineBlock(
        topic="Letters Testamentary and Letters of Administration",
        keywords=["letters testamentary", "letters of administration", "authority", "executor", "administrator"],
        conclusion_template="Letters {are/are not} issued to the applicant.",
        reasoning_framework=(
            "Letters testamentary or of administration confer authority to act on behalf of the estate. "
            "The applicant must qualify by taking oath and posting bond if required. "
            "The court issues letters upon finding the applicant is qualified and entitled. "
            "Interested parties may object to issuance."
        ),
        key_factors=[
            "Applicant's qualification",
            "Oath and bond requirements",
            "Will provisions",
            "Objections by interested parties",
            "Court's discretion"
        ],
        primary_authority=[
            "Texas Estates Code §§ 301.051–301.056",
            "Texas Estates Code §§ 306.001–306.007"
        ],
        burden_holder="Applicant for letters",
        adversary_position="Objecting party",
        counter_arguments=[
            "Applicant is unqualified",
            "Bond or oath not provided",
            "Will does not nominate applicant"
        ],
        resolution_strategy="Verify qualifications; satisfy statutory requirements; court issues or denies letters.",
        entity_scope="Executor, administrator, court",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Texas Estates Code §§ 301.051–301.056"
    ),
    DoctrineBlock(
        topic="Notice to Creditors",
        keywords=["notice to creditors", "probate", "publication", "secured claims", "unsecured claims"],
        conclusion_template="Notice to creditors is {sufficient/insufficient} under statutory requirements.",
        reasoning_framework=(
            "The personal representative must give notice to creditors by publication and, for known creditors, by mail or personal delivery. "
            "Secured creditors must be notified within two months. "
            "Failure to give proper notice may affect the validity of claims and the representative's liability. "
            "The court reviews compliance with statutory notice requirements."
        ),
        key_factors=[
            "Method and timing of notice",
            "Identification of creditors",
            "Compliance with publication and delivery",
            "Effect on claims",
            "Representative's liability"
        ],
        primary_authority=[
            "Texas Estates Code §§ 308.051–308.056",
            "Texas Estates Code §§ 309.051–309.056"
        ],
        burden_holder="Personal representative",
        adversary_position="Creditor or interested party",
        counter_arguments=[
            "Notice was not given or was defective",
            "Creditor was not identified",
            "Statute not followed"
        ],
        resolution_strategy="Review notice procedures; confirm compliance; resolve disputes as necessary.",
        entity_scope="Personal representative, creditors, court",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Texas Estates Code §§ 308.051–308.056"
    ),
    DoctrineBlock(
        topic="Inventory, Appraisement, and List of Claims",
        keywords=["inventory", "appraisement", "list of claims", "executor", "administrator"],
        conclusion_template="The inventory, appraisement, and list of claims is {approved/rejected} by the court.",
        reasoning_framework=(
            "The personal representative must file a verified inventory, appraisement, and list of claims within 90 days of qualification, "
            "unless an affidavit in lieu is permitted. "
            "The inventory must list all estate property and claims, with values. "
            "The court reviews and approves or rejects the inventory. "
            "Interested parties may object to the inventory's accuracy."
        ),
        key_factors=[
            "Completeness and accuracy of inventory",
            "Timeliness of filing",
            "Appraisal of property",
            "Affidavit in lieu of inventory",
            "Objections by interested parties"
        ],
        primary_authority=[
            "Texas Estates Code §§ 309.051–309.056",
            "Texas Estates Code §§ 309.101–309.104"
        ],
        burden_holder="Personal representative",
        adversary_position="Objecting party",
        counter_arguments=[
            "Inventory is incomplete or inaccurate",
            "Not filed timely",
            "Affidavit in lieu is improper"
        ],
        resolution_strategy="Review inventory and objections; court approves or requires correction.",
        entity_scope="Personal representative, beneficiaries, court",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Texas Estates Code §§ 309.051–309.056"
    ),
    DoctrineBlock(
        topic="Distribution of Estate Assets",
        keywords=["distribution", "estate assets", "executor", "beneficiaries", "final accounting"],
        conclusion_template="Estate assets are {distributed/not distributed} according to will or law.",
        reasoning_framework=(
            "After payment of debts and expenses, the executor must distribute estate assets to beneficiaries or heirs. "
            "Distribution must comply with the will or intestate succession statutes. "
            "A final accounting is typically required. "
            "Disputes regarding shares or entitlement may be resolved by the court."
        ),
        key_factors=[
            "Payment of debts and expenses",
            "Compliance with will or law",
            "Final accounting",
            "Objections by beneficiaries or heirs",
            "Court approval"
        ],
        primary_authority=[
            "Texas Estates Code §§ 360.001–360.253",
            "Texas Estates Code §§ 355.001–355.009"
        ],
        burden_holder="Executor or administrator",
        adversary_position="Objecting beneficiary or heir",
        counter_arguments=[
            "Distribution is premature",
            "Shares are incorrect",
            "Accounting is incomplete"
        ],
        resolution_strategy="Complete administration; provide accounting; distribute as ordered by court.",
        entity_scope="Executor, beneficiaries, heirs, court",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Texas Estates Code §§ 360.001–360.253"
    ),
    DoctrineBlock(
        topic="Partial Distribution Before Final Settlement",
        keywords=["partial distribution", "interim distribution", "executor", "beneficiaries", "court approval"],
        conclusion_template="Partial distribution is {approved/denied} prior to final settlement.",
        reasoning_framework=(
            "The court may authorize partial distribution of estate assets before final settlement if sufficient assets remain to pay debts and expenses. "
            "The executor must apply for approval and provide an accounting. "
            "The court considers the needs of beneficiaries and the status of administration. "
            "Creditors and other interested parties may object."
        ),
        key_factors=[
            "Sufficiency of remaining assets",
            "Status of debts and expenses",
            "Beneficiaries' needs",
            "Accounting provided",
            "Court's discretion"
        ],
        primary_authority=[
            "Texas Estates Code §§ 360.251–360.253"
        ],
        burden_holder="Executor or applicant for distribution",
        adversary_position="Creditor or objecting party",
        counter_arguments=[
            "Distribution jeopardizes payment of debts",
            "Accounting is incomplete",
            "Premature distribution"
        ],
        resolution_strategy="Review application and accounting; court approves or denies partial distribution.",
        entity_scope="Executor, beneficiaries, creditors, court",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Texas Estates Code §§ 360.251–360.253"
    ),
    DoctrineBlock(
        topic="Closing and Discharge of Personal Representative",
        keywords=["closing estate", "discharge", "personal representative", "final settlement", "court order"],
        conclusion_template="The estate is {closed/not closed} and the personal representative is {discharged/not discharged}.",
        reasoning_framework=(
            "After administration is complete and assets are distributed, the personal representative may apply for discharge. "
            "The court reviews the final accounting and confirms all duties are fulfilled. "
            "Upon approval, the court enters an order closing the estate and discharging the representative. "
            "Interested parties may object if administration is incomplete."
        ),
        key_factors=[
            "Completion of administration",
            "Final accounting",
            "Distribution of assets",
            "Objections by interested parties",
            "Court order"
        ],
        primary_authority=[
            "Texas Estates Code §§ 360.301–360.306"
        ],
        burden_holder="Personal representative",
        adversary_position="Objecting party",
        counter_arguments=[
            "Administration is incomplete",
            "Final accounting is deficient",
            "Assets remain undistributed"
        ],
        resolution_strategy="Review final accounting; confirm completion; court orders discharge.",
        entity_scope="Personal representative, beneficiaries, court",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Texas Estates Code §§ 360.301–360.306"
    ),
    DoctrineBlock(
        topic="Statute of Limitations in Probate",
        keywords=["statute of limitations", "probate", "will contest", "creditor claims", "timeliness"],
        conclusion_template="The action is {timely/untimely} under the applicable statute of limitations.",
        reasoning_framework=(
            "Probate actions are subject to statutory time limits. "
            "A will must generally be probated within four years of death, unless the applicant shows no default in failing to present it. "
            "Creditor claims and will contests also have deadlines. "
            "The court determines timeliness based on statute and evidence of diligence."
        ),
        key_factors=[
            "Date of decedent's death",
            "Date of filing",
            "Reason for delay",
            "Statutory deadlines",
            "Evidence of diligence"
        ],
        primary_authority=[
            "Texas Estates Code §§ 256.003, 256.204",
            "Texas Estates Code §§ 355.060–355.061"
        ],
        burden_holder="Applicant or claimant",
        adversary_position="Objecting party",
        counter_arguments=[
            "Action is barred by limitations",
            "Applicant was in default",
            "Statutory exception does not apply"
        ],
        resolution_strategy="Review filing dates and reasons; apply statutory deadlines and exceptions.",
        entity_scope="Applicants, creditors, court",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Texas Estates Code §§ 256.003, 256.204"
    ),
    DoctrineBlock(
        topic="Jurisdiction and Venue in Probate",
        keywords=["jurisdiction", "venue", "probate court", "county court", "original probate"],
        conclusion_template="Jurisdiction and venue are {proper/improper} for the probate proceeding.",
        reasoning_framework=(
            "Probate jurisdiction lies in the county court, statutory probate court, or district court as provided by law. "
            "Venue is generally proper in the county where the decedent resided or where property is located. "
            "The court examines residence, location of assets, and statutory provisions. "
            "Improper venue may be challenged by motion."
        ),
        key_factors=[
            "Decedent's residence",
            "Location of property",
            "Type of court",
            "Statutory venue provisions",
            "Objections to venue"
        ],
        primary_authority=[
            "Texas Estates Code §§ 33.001–33.004",
            "Texas Estates Code §§ 33.101–33.103"
        ],
        burden_holder="Applicant for probate",
        adversary_position="Objecting party",
        counter_arguments=[
            "Venue is improper",
            "Court lacks jurisdiction",
            "Statute requires different forum"
        ],
        resolution_strategy="Review residence and property; confirm jurisdiction and venue; resolve objections.",
        entity_scope="Applicants, court, interested parties",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Texas Estates Code §§ 33.001–33.004"
    ),
    DoctrineBlock(
        topic="Foreign Will Admission",
        keywords=["foreign will", "admission", "probate", "authentication", "out-of-state"],
        conclusion_template="The foreign will is {admitted