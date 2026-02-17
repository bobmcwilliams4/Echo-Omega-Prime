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
        topic="Duty of Loyalty - Self-Dealing Prohibition",
        keywords=["loyalty", "self-dealing", "fiduciary", "conflict of interest", "trustee"],
        conclusion_template="A trustee breaches the duty of loyalty by engaging in self-dealing unless expressly authorized by the trust instrument or applicable law.",
        reasoning_framework=(
            "The duty of loyalty is a fundamental fiduciary obligation requiring trustees to act solely in the interests of the beneficiaries. "
            "Self-dealing occurs when a trustee benefits personally from trust assets or transactions. Courts scrutinize such actions strictly, "
            "presuming impropriety unless the trustee can demonstrate full disclosure and beneficiary consent, or explicit authorization in the trust. "
            "Relevant factors include the nature of the transaction, disclosure to beneficiaries, and whether the trustee's actions were objectively fair. "
            "Exceptions may exist for independent trustees or where state statutes permit certain self-interested transactions. "
            "Judicial remedies include rescission, surcharge, and removal. The burden shifts to the trustee to prove fairness and compliance."
        ),
        key_factors=[
            "Existence of personal benefit",
            "Disclosure to beneficiaries",
            "Authorization in trust instrument",
            "Fairness of transaction",
            "State statutory exceptions"
        ],
        primary_authority=[
            "Restatement (Third) of Trusts §78",
            "Uniform Trust Code §802",
            "Bogert, Trusts and Trustees §543",
            "In re Estate of Rothko, 43 N.Y.2d 305 (1977)"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiaries allege breach due to self-dealing",
        counter_arguments=[
            "Transaction was fair and reasonable",
            "Full disclosure and beneficiary consent",
            "Express authorization in trust instrument",
            "Statutory exception applies"
        ],
        resolution_strategy="Strict scrutiny of trustee actions; rescission or surcharge if breach found.",
        entity_scope="Trustee actions",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Rothko, Restatement (Third) of Trusts §78"
    ),
    DoctrineBlock(
        topic="Prudent Investor Rule - Modern Portfolio Theory",
        keywords=["prudent investor", "investment", "portfolio", "risk", "trustee"],
        conclusion_template="A trustee must invest and manage trust assets as a prudent investor would, considering the trust's purposes, terms, distribution requirements, and other circumstances.",
        reasoning_framework=(
            "The Prudent Investor Rule requires trustees to exercise reasonable care, skill, and caution in investment decisions. "
            "Modern Portfolio Theory mandates diversification and risk management, viewing the portfolio as a whole rather than individual assets. "
            "Trustees must consider the needs of beneficiaries, time horizon, liquidity, tax consequences, and economic conditions. "
            "Deviation from diversification is permissible only if justified by trust purposes or beneficiary interests. "
            "Trustees may delegate investment functions if done prudently. Failure to comply may result in surcharge or removal."
        ),
        key_factors=[
            "Diversification",
            "Risk tolerance",
            "Trust purposes and terms",
            "Beneficiary needs",
            "Economic conditions"
        ],
        primary_authority=[
            "Uniform Prudent Investor Act §2",
            "Restatement (Third) of Trusts §§90-92",
            "Harvard College v. Amory, 26 Mass. 446 (1830)"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiaries allege imprudent investment or lack of diversification",
        counter_arguments=[
            "Investment strategy aligns with trust purposes",
            "Justified deviation from diversification",
            "Delegation to qualified professionals"
        ],
        resolution_strategy="Review investment strategy for compliance with prudent investor standards.",
        entity_scope="Trustee investment decisions",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Prudent Investor Act §2"
    ),
    DoctrineBlock(
        topic="Duty to Inform - Regular Reporting Requirements",
        keywords=["duty to inform", "accounting", "reporting", "trustee", "beneficiary"],
        conclusion_template="Trustees must keep beneficiaries reasonably informed about the trust and its administration, including providing regular accountings.",
        reasoning_framework=(
            "Trustees are obligated to provide beneficiaries with sufficient information to protect their interests. "
            "This includes periodic accountings, notice of significant transactions, and responses to reasonable requests. "
            "Failure to inform may constitute a breach, subjecting the trustee to remedies. "
            "The frequency and detail of reporting depend on the trust instrument, applicable statutes, and beneficiary status. "
            "Exceptions may exist for revocable trusts or minor beneficiaries. "
            "Courts may compel disclosure and impose sanctions for noncompliance."
        ),
        key_factors=[
            "Frequency of reporting",
            "Content of accountings",
            "Beneficiary status",
            "Trust terms",
            "Statutory requirements"
        ],
        primary_authority=[
            "Uniform Trust Code §§813, 105",
            "Restatement (Third) of Trusts §82",
            "Bogert, Trusts and Trustees §963"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiaries allege lack of information or inadequate accounting",
        counter_arguments=[
            "Trust instrument limits disclosure",
            "Beneficiary is not entitled to information",
            "Information already provided"
        ],
        resolution_strategy="Court may order disclosure or impose sanctions.",
        entity_scope="Trustee reporting obligations",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §813"
    ),
    DoctrineBlock(
        topic="HEMS Distribution Standard - Ascertainable Standard",
        keywords=["HEMS", "distribution", "ascertainable standard", "health", "education", "maintenance", "support"],
        conclusion_template="Distributions under the HEMS standard must be made in accordance with the beneficiary's health, education, maintenance, or support needs.",
        reasoning_framework=(
            "HEMS is a commonly used ascertainable standard in trusts, limiting trustee discretion to distributions for specified purposes. "
            "This standard protects beneficiaries and preserves tax benefits, preventing inclusion in the settlor's estate. "
            "Trustees must evaluate beneficiary needs objectively, considering lifestyle, expenses, and other resources. "
            "Discretion is not absolute; courts may review for abuse or failure to follow the standard. "
            "IRS guidance treats HEMS as sufficiently definite to avoid estate tax inclusion. "
            "Disputes often arise over interpretation and application."
        ),
        key_factors=[
            "Beneficiary needs",
            "Trustee discretion",
            "Trust terms",
            "IRS guidance",
            "Lifestyle and expenses"
        ],
        primary_authority=[
            "IRC §2041",
            "Treas. Reg. §20.2041-1(c)",
            "Restatement (Third) of Trusts §50"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges improper or insufficient distribution",
        counter_arguments=[
            "Distribution aligns with HEMS standard",
            "Beneficiary has other resources",
            "Trustee exercised reasonable discretion"
        ],
        resolution_strategy="Court reviews trustee discretion for abuse or deviation from standard.",
        entity_scope="Trustee distribution decisions",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRC §2041, Treas. Reg. §20.2041-1(c)"
    ),
    DoctrineBlock(
        topic="Spendthrift Clause - Creditor Protection",
        keywords=["spendthrift", "creditor", "protection", "trust", "beneficiary"],
        conclusion_template="A valid spendthrift clause prevents beneficiaries' creditors from reaching trust assets until distributed.",
        reasoning_framework=(
            "Spendthrift provisions restrict beneficiaries' ability to transfer or assign their interests, shielding trust assets from creditors. "
            "Such clauses are generally upheld unless prohibited by statute. "
            "Exceptions include claims for child support, alimony, and certain governmental obligations. "
            "Once assets are distributed, they lose protection. "
            "Courts examine the validity of the clause, beneficiary status, and applicable exceptions. "
            "Some jurisdictions limit protection for self-settled trusts."
        ),
        key_factors=[
            "Validity of spendthrift clause",
            "Beneficiary status",
            "Type of creditor claim",
            "Jurisdictional exceptions",
            "Distribution status"
        ],
        primary_authority=[
            "Uniform Trust Code §§502-503",
            "Restatement (Third) of Trusts §§58-59",
            "Coker v. Coker, 650 S.W.2d 391 (Tex. 1983)"
        ],
        burden_holder="Creditor",
        adversary_position="Creditor seeks to reach trust assets",
        counter_arguments=[
            "Spendthrift clause is valid and enforceable",
            "Claim falls under statutory exception",
            "Assets not yet distributed"
        ],
        resolution_strategy="Enforce spendthrift clause unless statutory exception applies.",
        entity_scope="Trust assets",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §502"
    ),
    DoctrineBlock(
        topic="Trust Modification - Changed Circumstances Doctrine",
        keywords=["trust modification", "changed circumstances", "court", "beneficiary", "settlor"],
        conclusion_template="A court may modify a trust if unforeseen circumstances arise that defeat or substantially impair the trust's purposes.",
        reasoning_framework=(
            "Trusts are generally irrevocable, but courts may modify terms if unforeseen circumstances render original provisions impracticable or contrary to settlor intent. "
            "The doctrine requires evidence of substantial change, impossibility, or frustration of purpose. "
            "Modification must preserve the settlor's intent as much as possible. "
            "Beneficiaries, trustees, or settlors may petition for modification. "
            "Statutory frameworks, such as the Uniform Trust Code, provide guidance. "
            "Courts weigh the impact on beneficiaries, the nature of the change, and alternatives."
        ),
        key_factors=[
            "Unforeseen circumstances",
            "Frustration of trust purpose",
            "Settlor intent",
            "Impact on beneficiaries",
            "Statutory authority"
        ],
        primary_authority=[
            "Uniform Trust Code §412",
            "Restatement (Third) of Trusts §66",
            "Bogert, Trusts and Trustees §994"
        ],
        burden_holder="Petitioner (trustee, beneficiary, or settlor)",
        adversary_position="Opposing party argues modification is unnecessary or contrary to intent",
        counter_arguments=[
            "Circumstances do not warrant modification",
            "Modification would defeat settlor intent",
            "Alternative remedies exist"
        ],
        resolution_strategy="Court balances changed circumstances against settlor intent and trust purpose.",
        entity_scope="Trust terms",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §412"
    ),
    DoctrineBlock(
        topic="Trustee Removal - Cause Standard",
        keywords=["trustee removal", "cause", "court", "breach", "beneficiary"],
        conclusion_template="A trustee may be removed for cause, including breach of trust, incapacity, or persistent failure to administer the trust effectively.",
        reasoning_framework=(
            "Removal of a trustee is a drastic remedy, reserved for serious misconduct or incapacity. "
            "Courts require clear evidence of breach, conflict of interest, or persistent failure. "
            "Beneficiaries may petition for removal, but must show harm or risk to trust assets. "
            "Trust terms may specify grounds for removal. "
            "Judicial discretion is exercised to protect beneficiaries and preserve trust purposes. "
            "Removal may be temporary or permanent, with appointment of a successor."
        ),
        key_factors=[
            "Breach of trust",
            "Incapacity",
            "Persistent failure",
            "Conflict of interest",
            "Beneficiary harm"
        ],
        primary_authority=[
            "Uniform Trust Code §706",
            "Restatement (Third) of Trusts §37",
            "Bogert, Trusts and Trustees §527"
        ],
        burden_holder="Petitioner (beneficiary or co-trustee)",
        adversary_position="Trustee contests removal",
        counter_arguments=[
            "No breach or incapacity",
            "Removal would harm trust administration",
            "Petition is frivolous"
        ],
        resolution_strategy="Court reviews evidence and exercises discretion to protect trust interests.",
        entity_scope="Trustee position",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §706"
    ),
    DoctrineBlock(
        topic="Duty of Impartiality - Income vs Remainder Beneficiaries",
        keywords=["impartiality", "income beneficiary", "remainder beneficiary", "trustee", "allocation"],
        conclusion_template="Trustees must act impartially in managing trust assets and distributing income and principal, balancing the interests of income and remainder beneficiaries.",
        reasoning_framework=(
            "The duty of impartiality requires trustees to treat all beneficiaries equitably, considering their respective interests. "
            "Allocation of receipts and expenses must be fair, avoiding favoritism. "
            "Trust terms may grant discretion, but trustees must justify decisions. "
            "Conflicts arise in allocation of income versus principal, especially under the Uniform Principal and Income Act. "
            "Courts review for abuse of discretion or breach of duty."
        ),
        key_factors=[
            "Beneficiary interests",
            "Trust terms",
            "Allocation decisions",
            "Discretion exercised",
            "Statutory guidance"
        ],
        primary_authority=[
            "Uniform Trust Code §803",
            "Restatement (Third) of Trusts §79",
            "Uniform Principal and Income Act"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges favoritism or unfair allocation",
        counter_arguments=[
            "Allocation is consistent with trust terms",
            "Discretion exercised impartially",
            "Statutory compliance"
        ],
        resolution_strategy="Court reviews allocation for impartiality and fairness.",
        entity_scope="Trustee allocation decisions",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §803"
    ),
    DoctrineBlock(
        topic="Crummey Powers - Annual Exclusion Gifts",
        keywords=["Crummey", "power of withdrawal", "annual exclusion", "gift tax", "trust"],
        conclusion_template="Crummey powers allow beneficiaries to withdraw contributions for a limited period, qualifying gifts for the annual exclusion under IRC §2503(b).",
        reasoning_framework=(
            "Crummey powers are used to ensure that gifts to trusts qualify for the annual gift tax exclusion. "
            "Beneficiaries must have a present, unrestricted right to withdraw contributions for a specified window. "
            "Notice must be given to beneficiaries, and the withdrawal right must be real, even if rarely exercised. "
            "IRS scrutiny focuses on adequacy of notice and actual ability to withdraw. "
            "Failure to comply may result in loss of exclusion and gift tax liability."
        ),
        key_factors=[
            "Present interest",
            "Notice to beneficiaries",
            "Withdrawal window",
            "Actual ability to withdraw",
            "IRS compliance"
        ],
        primary_authority=[
            "IRC §2503(b)",
            "Crummey v. Commissioner, 397 F.2d 82 (9th Cir. 1968)",
            "Treas. Reg. §25.2503-3"
        ],
        burden_holder="Trustee/settlor",
        adversary_position="IRS challenges exclusion",
        counter_arguments=[
            "Withdrawal right is real and unrestricted",
            "Adequate notice provided",
            "Beneficiaries have exercised right"
        ],
        resolution_strategy="Ensure compliance with Crummey requirements and maintain records.",
        entity_scope="Trust contributions",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Crummey v. Commissioner"
    ),
    DoctrineBlock(
        topic="Generation-Skipping Transfer Tax - Dynasty Trust Planning",
        keywords=["GST", "generation-skipping", "dynasty trust", "tax", "transfer"],
        conclusion_template="Dynasty trusts are structured to minimize or avoid GST tax, leveraging exemptions and allocation strategies.",
        reasoning_framework=(
            "Generation-Skipping Transfer (GST) tax applies to transfers to beneficiaries two or more generations below the settlor. "
            "Dynasty trusts use GST exemption allocations to shield assets from repeated taxation. "
            "Trustees and planners must monitor exemption amounts, proper allocation, and trust structure. "
            "Failure to allocate exemptions or improper structuring may trigger GST tax. "
            "IRS guidance and state law impact planning strategies."
        ),
        key_factors=[
            "GST exemption amount",
            "Proper allocation",
            "Trust structure",
            "Beneficiary generations",
            "IRS guidance"
        ],
        primary_authority=[
            "IRC §§2631-2632",
            "Treas. Reg. §26.2632-1",
            "PLR 200846008"
        ],
        burden_holder="Trustee/settlor",
        adversary_position="IRS challenges GST exemption or allocation",
        counter_arguments=[
            "Proper allocation documented",
            "Trust structure complies with law",
            "Exemption amount sufficient"
        ],
        resolution_strategy="Careful allocation and documentation of GST exemption.",
        entity_scope="Trust transfers",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRC §2631"
    ),
    DoctrineBlock(
        topic="Trust Decanting - Trustee Power to Modify",
        keywords=["decanting", "trustee power", "modification", "trust", "beneficiary"],
        conclusion_template="Trustees may decant trust assets to a new trust with modified terms if authorized by statute or trust instrument.",
        reasoning_framework=(
            "Decanting allows trustees to transfer assets from one trust to another, modifying terms to address changed circumstances or improve administration. "
            "Statutory authority varies by state; some require notice or beneficiary consent. "
            "Trustee discretion must be exercised in good faith and consistent with fiduciary duties. "
            "Decanting may be used to correct drafting errors, change situs, or add spendthrift provisions. "
            "Risks include unintended tax consequences and beneficiary challenges."
        ),
        key_factors=[
            "Statutory authority",
            "Trust instrument authorization",
            "Notice to beneficiaries",
            "Fiduciary duty",
            "Purpose of decanting"
        ],
        primary_authority=[
            "Uniform Trust Decanting Act",
            "NY Estates, Powers and Trusts Law §10-6.6",
            "Restatement (Third) of Trusts §64"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary challenges decanting",
        counter_arguments=[
            "Decanting authorized by statute/instrument",
            "Good faith exercise of discretion",
            "Beneficiary interests preserved"
        ],
        resolution_strategy="Review statutory compliance and fiduciary conduct.",
        entity_scope="Trust assets",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NY EPTL §10-6.6"
    ),
    DoctrineBlock(
        topic="Virtual Representation - Binding Absent Beneficiaries",
        keywords=["virtual representation", "absent beneficiary", "court", "trust", "binding"],
        conclusion_template="Courts may bind absent or minor beneficiaries through virtual representation by parties with substantially identical interests.",
        reasoning_framework=(
            "Virtual representation doctrine allows courts to bind beneficiaries who are not present or lack capacity, provided another party represents their interests. "
            "Representation must be adequate and interests substantially identical. "
            "Used to facilitate trust modifications, accountings, and settlements without requiring all beneficiaries to participate. "
            "Statutes and court rules govern adequacy and scope. "
            "Challenges may arise if interests diverge or representation is inadequate."
        ),
        key_factors=[
            "Adequacy of representation",
            "Identity of interests",
            "Beneficiary capacity",
            "Statutory authority",
            "Scope of binding effect"
        ],
        primary_authority=[
            "Uniform Trust Code §301",
            "Restatement (Third) of Trusts §85",
            "Bogert, Trusts and Trustees §964"
        ],
        burden_holder="Party seeking binding effect",
        adversary_position="Absent beneficiary contests adequacy",
        counter_arguments=[
            "Interests are not identical",
            "Representation is inadequate",
            "Statutory requirements not met"
        ],
        resolution_strategy="Court reviews adequacy and identity of interests.",
        entity_scope="Beneficiary interests",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §301"
    ),
    DoctrineBlock(
        topic="Trustee Compensation - Reasonable Fees",
        keywords=["trustee compensation", "fees", "reasonableness", "trust", "beneficiary"],
        conclusion_template="Trustees are entitled to reasonable compensation for services rendered, subject to court review and trust terms.",
        reasoning_framework=(
            "Trustees may receive compensation for their services, but fees must be reasonable and consistent with trust terms. "
            "Factors include complexity, time, skill, and local standards. "
            "Beneficiaries may challenge excessive fees. "
            "Courts may reduce or deny fees for breach of duty. "
            "Corporate trustees often follow published fee schedules."
        ),
        key_factors=[
            "Trust terms",
            "Complexity of administration",
            "Time and skill required",
            "Local standards",
            "Fee schedules"
        ],
        primary_authority=[
            "Uniform Trust Code §708",
            "Restatement (Third) of Trusts §38",
            "Bogert, Trusts and Trustees §977"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary challenges fee amount",
        counter_arguments=[
            "Fee is reasonable and consistent with trust terms",
            "Services rendered justify fee",
            "Local standards support fee"
        ],
        resolution_strategy="Court reviews fee for reasonableness and compliance.",
        entity_scope="Trustee compensation",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §708"
    ),
    DoctrineBlock(
        topic="Revocable Trust - Settlor Rights and Control",
        keywords=["revocable trust", "settlor", "control", "amendment", "revocation"],
        conclusion_template="During the settlor's lifetime, a revocable trust is controlled by the settlor, who may amend or revoke at will unless restricted by the trust instrument.",
        reasoning_framework=(
            "Revocable trusts grant the settlor broad rights to amend, revoke, or direct administration during their lifetime. "
            "Trustees must follow settlor instructions unless contrary to law or trust terms. "
            "Upon settlor's death or incapacity, trust becomes irrevocable and trustee assumes full fiduciary duties. "
            "Beneficiaries have limited rights during settlor's control. "
            "Disputes may arise over amendment, revocation, or settlor capacity."
        ),
        key_factors=[
            "Settlor capacity",
            "Trust terms",
            "Amendment/revocation procedures",
            "Beneficiary rights",
            "Duration of revocability"
        ],
        primary_authority=[
            "Uniform Trust Code §§602-603",
            "Restatement (Third) of Trusts §25",
            "Bogert, Trusts and Trustees §1010"
        ],
        burden_holder="Settlor or party challenging amendment",
        adversary_position="Beneficiary or trustee contests settlor action",
        counter_arguments=[
            "Settlor lacks capacity",
            "Trust instrument restricts amendment",
            "Amendment/revocation not properly executed"
        ],
        resolution_strategy="Court reviews settlor capacity and compliance with procedures.",
        entity_scope="Revocable trust",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §602"
    ),
    DoctrineBlock(
        topic="Trust Protector - Third-Party Oversight Powers",
        keywords=["trust protector", "oversight", "third-party", "powers", "trust"],
        conclusion_template="Trust protectors may exercise oversight powers as granted by the trust instrument, including amendment, removal, or veto authority.",
        reasoning_framework=(
            "Trust protectors are third parties appointed to oversee trustees and ensure compliance with settlor intent. "
            "Their powers are defined by the trust instrument and may include amendment, removal of trustees, or veto of actions. "
            "Protectors owe duties to beneficiaries, but may not be held to full fiduciary standards unless specified. "
            "Courts enforce protector powers as written, subject to public policy and statutory limits."
        ),
        key_factors=[
            "Trust instrument language",
            "Scope of protector powers",
            "Fiduciary status",
            "Beneficiary interests",
            "Statutory authority"
        ],
        primary_authority=[
            "Uniform Trust Code §808",
            "Restatement (Third) of Trusts §64",
            "Bogert, Trusts and Trustees §1012"
        ],
        burden_holder="Trust protector",
        adversary_position="Beneficiary or trustee challenges protector action",
        counter_arguments=[
            "Protector acted within scope of powers",
            "Protector owes fiduciary duties",
            "Protector action violates public policy"
        ],
        resolution_strategy="Court interprets trust instrument and reviews for abuse.",
        entity_scope="Trust protector actions",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §808"
    ),
    DoctrineBlock(
        topic="Breach of Trust - Remedies and Surcharge",
        keywords=["breach of trust", "remedies", "surcharge", "trustee", "beneficiary"],
        conclusion_template="Upon breach of trust, courts may impose remedies including surcharge, removal, or rescission to restore beneficiary interests.",
        reasoning_framework=(
            "A breach of trust occurs when a trustee violates fiduciary duties or trust terms. "
            "Remedies include surcharge (monetary compensation), removal, rescission of transactions, and injunctions. "
            "Courts aim to restore beneficiaries to the position they would have occupied absent the breach. "
            "Trustees may be denied compensation or required to disgorge profits. "
            "Burden of proof lies with the party alleging breach."
        ),
        key_factors=[
            "Nature of breach",
            "Harm to beneficiaries",
            "Trustee conduct",
            "Remedies available",
            "Burden of proof"
        ],
        primary_authority=[
            "Uniform Trust Code §1001",
            "Restatement (Third) of Trusts §§93-94",
            "Bogert, Trusts and Trustees §861"
        ],
        burden_holder="Beneficiary or party alleging breach",
        adversary_position="Trustee contests breach or remedy",
        counter_arguments=[
            "No breach occurred",
            "Beneficiary suffered no harm",
            "Remedy is excessive"
        ],
        resolution_strategy="Court determines breach and appropriate remedy.",
        entity_scope="Trust administration",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §1001"
    ),
    DoctrineBlock(
        topic="Trust Accounting - Principal and Income Allocation",
        keywords=["accounting", "principal", "income", "allocation", "trustee"],
        conclusion_template="Trustees must allocate receipts and expenses between principal and income in accordance with trust terms and applicable statutes.",
        reasoning_framework=(
            "Trust accounting requires trustees to distinguish between principal and income, affecting distributions to beneficiaries. "
            "The Uniform Principal and Income Act provides guidance for allocation. "
            "Trust terms may override statutory rules. "
            "Trustees must exercise discretion impartially and document decisions. "
            "Beneficiaries may challenge allocations as unfair or inconsistent."
        ),
        key_factors=[
            "Trust terms",
            "Statutory guidance",
            "Nature of receipts and expenses",
            "Impartiality",
            "Documentation"
        ],
        primary_authority=[
            "Uniform Principal and Income Act",
            "Restatement (Third) of Trusts §79",
            "Bogert, Trusts and Trustees §965"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary challenges allocation",
        counter_arguments=[
            "Allocation is consistent with trust terms/statute",
            "Impartiality maintained",
            "Adequate documentation"
        ],
        resolution_strategy="Court reviews allocation for compliance and fairness.",
        entity_scope="Trust accounting",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Principal and Income Act"
    ),
    DoctrineBlock(
        topic="Special Needs Trust - Preserving Government Benefits",
        keywords=["special needs trust", "government benefits", "SSI", "Medicaid", "trust"],
        conclusion_template="Special needs trusts are structured to preserve beneficiary eligibility for government benefits by restricting access to principal and income.",
        reasoning_framework=(
            "Special needs trusts supplement, but do not supplant, government benefits for disabled beneficiaries. "
            "Trust terms must restrict distributions to non-essential needs, avoiding direct payments for food or shelter. "
            "Trustees must understand benefit eligibility rules and coordinate with public agencies. "
            "Improper distributions may disqualify beneficiaries. "
            "Statutory authority governs creation and administration."
        ),
        key_factors=[
            "Trust terms",
            "Distribution restrictions",
            "Benefit eligibility",
            "Coordination with agencies",
            "Statutory compliance"
        ],
        primary_authority=[
            "42 U.S.C. §1396p(d)(4)(A)",
            "Social Security POMS SI 01120.200",
            "Restatement (Third) of Trusts §48"
        ],
        burden_holder="Trustee",
        adversary_position="Agency challenges eligibility",
        counter_arguments=[
            "Trust complies with statutory requirements",
            "Distributions are for supplemental needs",
            "No direct payments for food/shelter"
        ],
        resolution_strategy="Careful drafting and administration to preserve benefits.",
        entity_scope="Special needs trust",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="42 U.S.C. §1396p(d)(4)(A)"
    ),
    DoctrineBlock(
        topic="Charitable Remainder Trust - Split Interest Requirements",
        keywords=["charitable remainder trust", "split interest", "charity", "trust", "tax"],
        conclusion_template="Charitable remainder trusts must satisfy split interest requirements, providing a qualifying income interest and remainder to charity.",
        reasoning_framework=(
            "Charitable remainder trusts (CRTs) provide income to non-charitable beneficiaries for a term, with remainder to charity. "
            "IRS rules require fixed or variable payments, minimum remainder value, and compliance with statutory formats. "
            "Failure to meet requirements may result in loss of tax benefits. "
            "Trustees must monitor distributions and remainder value, filing annual returns."
        ),
        key_factors=[
            "Income interest structure",
            "Remainder value",
            "Charity qualification",
            "IRS compliance",
            "Annual reporting"
        ],
        primary_authority=[
            "IRC §664",
            "Treas. Reg. §1.664-1",
            "PLR 201328027"
        ],
        burden_holder="Trustee/settlor",
        adversary_position="IRS challenges CRT qualification",
        counter_arguments=[
            "Trust meets statutory requirements",
            "Remainder value sufficient",
            "Charity is qualified"
        ],
        resolution_strategy="Ensure compliance with CRT rules and maintain documentation.",
        entity_scope="Charitable remainder trust",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRC §664"
    ),
    DoctrineBlock(
        topic="Dynasty Trust - Perpetuities and Asset Protection",
        keywords=["dynasty trust", "perpetuities", "asset protection", "trust", "generation-skipping"],
        conclusion_template="Dynasty trusts are structured to last for multiple generations, avoiding perpetuities limitations and providing asset protection.",
        reasoning_framework=(
            "Dynasty trusts are designed to endure for extended periods, often circumventing traditional Rule Against Perpetuities via state statutes. "
            "They provide asset protection, minimize estate and GST taxes, and preserve wealth. "
            "Trustees must monitor compliance with perpetuities law and asset protection statutes. "
            "Risks include legislative changes and creditor challenges."
        ),
        key_factors=[
            "State perpetuities law",
            "Trust structure",
            "Asset protection provisions",
            "Tax planning",
            "Creditor risks"
        ],
        primary_authority=[
            "Uniform Trust Code §401",
            "Restatement (Third) of Trusts §49",
            "Delaware Trust Act"
        ],
        burden_holder="Trustee/settlor",
        adversary_position="Creditor or IRS challenges trust structure",
        counter_arguments=[
            "Trust complies with state law",
            "Asset protection provisions valid",
            "Perpetuities limitation avoided"
        ],
        resolution_strategy="Careful drafting and monitoring of state law changes.",
        entity_scope="Dynasty trust",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Delaware Trust Act"
    ),
    DoctrineBlock(
        topic="Unitrust Conversion - UPIA Power to Adjust",
        keywords=["unitrust", "conversion", "UPIA", "power to adjust", "trustee"],
        conclusion_template="Trustees may convert income trusts to unitrusts or adjust allocations under UPIA to balance beneficiary interests.",
        reasoning_framework=(
            "The Uniform Principal and Income Act (UPIA) allows trustees to convert traditional income trusts to unitrusts, providing fixed percentage distributions. "
            "Trustees may also adjust allocations between principal and income to address changing circumstances. "
            "Conversion requires notice to beneficiaries and compliance with statutory procedures. "
            "Beneficiaries may challenge conversion as unfair or inconsistent with trust purpose."
        ),
        key_factors=[
            "Statutory authority",
            "Notice to beneficiaries",
            "Trust terms",
            "Beneficiary interests",
            "Conversion procedures"
        ],
        primary_authority=[
            "Uniform Principal and Income Act §104",
            "Restatement (Third) of Trusts §79",
            "Bogert, Trusts and Trustees §965"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary challenges conversion",
        counter_arguments=[
            "Conversion complies with statute",
            "Beneficiary interests balanced",
            "Notice provided"
        ],
        resolution_strategy="Court reviews conversion for compliance and fairness.",
        entity_scope="Trust income/principal allocations",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Principal and Income Act §104"
    ),
    DoctrineBlock(
        topic="Trust Termination - Uneconomic to Continue",
        keywords=["trust termination", "uneconomic", "court", "trustee", "beneficiary"],
        conclusion_template="Trusts may be terminated if continuation is uneconomic, subject to court approval and protection of beneficiary interests.",
        reasoning_framework=(
            "Trusts with insufficient assets or disproportionate administrative costs may be terminated by court or trustee. "
            "Statutory authority often sets minimum value thresholds. "
            "Termination must protect beneficiary interests and comply with trust terms. "
            "Notice and court approval are required in most cases."
        ),
        key_factors=[
            "Trust asset value",
            "Administrative costs",
            "Beneficiary interests",
            "Statutory thresholds",
            "Notice and approval"
        ],
        primary_authority=[
            "Uniform Trust Code §414",
            "Restatement (Third) of Trusts §61",
            "Bogert, Trusts and Trustees §1015"
        ],
        burden_holder="Trustee or beneficiary seeking termination",
        adversary_position="Beneficiary or trustee opposes termination",
        counter_arguments=[
            "Trust has sufficient assets",
            "Termination harms beneficiaries",
            "Statutory requirements not met"
        ],
        resolution_strategy="Court reviews economic analysis and beneficiary impact.",
        entity_scope="Trust existence",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §414"
    ),
    DoctrineBlock(
        topic="Trustee Delegation - Investment and Administrative Functions",
        keywords=["delegation", "investment", "administrative", "trustee", "fiduciary"],
        conclusion_template="Trustees may delegate investment and administrative functions if done prudently and in accordance with trust terms and statutory requirements.",
        reasoning_framework=(
            "Trustees may delegate functions to qualified agents, but must exercise care in selection, instruction, and monitoring. "
            "Delegation does not absolve trustees of ultimate responsibility. "
            "Statutory authority, such as UPIA, governs delegation standards. "
            "Beneficiaries may challenge improper delegation or lack of oversight."
        ),
        key_factors=[
            "Trust terms",
            "Agent qualifications",
            "Oversight and monitoring",
            "Statutory compliance",
            "Scope of delegation"
        ],
        primary_authority=[
            "Uniform Prudent Investor Act §7",
            "Restatement (Third) of Trusts §80",
            "Bogert, Trusts and Trustees §962"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges improper delegation",
        counter_arguments=[
            "Delegation was prudent",
            "Agent was qualified",
            "Oversight maintained"
        ],
        resolution_strategy="Court reviews delegation process and oversight.",
        entity_scope="Trustee functions",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Prudent Investor Act §7"
    ),
    DoctrineBlock(
        topic="Qualified Personal Residence Trust - Estate Tax Reduction",
        keywords=["QPRT", "personal residence", "estate tax", "trust", "gift"],
        conclusion_template="Qualified Personal Residence Trusts (QPRTs) are used to transfer residences at reduced gift tax value, leveraging retained interest and IRS valuation rules.",
        reasoning_framework=(
            "QPRTs allow settlors to transfer residences to trusts, retaining use for a term. "
            "Gift tax value is reduced by the retained interest, calculated under IRS tables. "
            "If settlor survives the term, residence passes to beneficiaries free of estate tax. "
            "Failure to comply with QPRT rules may result in inclusion in settlor's estate."
        ),
        key_factors=[
            "Term of retained interest",
            "IRS valuation",
            "Compliance with QPRT rules",
            "Survival of settlor",
            "Gift tax reporting"
        ],
        primary_authority=[
            "IRC §2702",
            "Treas. Reg. §25.2702-5",
            "PLR 200944002"
        ],
        burden_holder="Settlor/trustee",
        adversary_position="IRS challenges QPRT structure",
        counter_arguments=[
            "QPRT complies with statutory requirements",
            "Valuation is accurate",
            "Residence qualifies"
        ],
        resolution_strategy="Careful drafting and compliance with IRS rules.",
        entity_scope="Personal residence trust",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRC §2702"
    ),
    DoctrineBlock(
        topic="Alaska Self-Settled Asset Protection Trust - Creditor Shield",
        keywords=["Alaska trust", "self-settled", "asset protection", "creditor", "trust"],
        conclusion_template="Alaska self-settled asset protection trusts shield assets from most creditors, subject to statutory exceptions and fraudulent transfer rules.",
        reasoning_framework=(
            "Alaska statutes permit self-settled asset protection trusts, allowing settlors to retain interests while shielding assets from creditors. "
            "Statutory exceptions include child support, alimony, and certain governmental claims. "
            "Transfers must not be fraudulent; courts may set aside transfers if intent to defraud is proven. "
            "Trustees must comply with statutory requirements for creation and administration."
        ),
        key_factors=[
            "Statutory compliance",
            "Settlor interest",
            "Creditor claim type",
            "Fraudulent transfer analysis",
            "Notice and administration"
        ],
        primary_authority=[
            "Alaska Stat. §34.40.110",
            "Restatement (Third) of Trusts §58",
            "Bogert, Trusts and Trustees §1016"
        ],
        burden_holder="Creditor",
        adversary_position="Creditor alleges fraudulent transfer or statutory exception",
        counter_arguments=[
            "Trust complies with Alaska law",
            "No fraudulent intent",
            "Claim falls outside exceptions"
        ],
        resolution_strategy="Court reviews statutory compliance and transfer intent.",
        entity_scope="Self-settled asset protection trust",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Alaska Stat. §34.40.110"
    ),
    DoctrineBlock(
        topic="Nonjudicial Settlement Agreement - Consent Modification",
        keywords=["nonjudicial settlement", "agreement", "consent", "modification", "trust"],
        conclusion_template="Trusts may be modified by nonjudicial settlement agreements if all interested parties consent and modification does not violate material purpose.",
        reasoning_framework=(
            "Nonjudicial settlement agreements allow parties to modify trust terms without court involvement, provided all interested parties consent. "
            "Modification must not violate material purpose of the trust. "
            "Statutory authority, such as Uniform Trust Code §111, governs scope and requirements. "
            "Disputes may arise over identification of interested parties and material purpose."
        ),
        key_factors=[
            "Consent of all interested parties",
            "Material purpose",
            "Statutory authority",
            "Scope of modification",
            "Notice and documentation"
        ],
        primary_authority=[
            "Uniform Trust Code §111",
            "Restatement (Third) of Trusts §65",
            "Bogert, Trusts and Trustees §994"
        ],
        burden_holder="Party seeking modification",
        adversary_position="Party alleges violation of material purpose",
        counter_arguments=[
            "Material purpose preserved",
            "All parties consented",
            "Statutory requirements met"
        ],
        resolution_strategy="Court reviews material purpose and party consent.",
        entity_scope="Trust terms",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §111"
    ),
    DoctrineBlock(
        topic="Trustee Duty to Diversify Investments",
        keywords=["diversification", "investment", "trustee", "risk", "portfolio"],
        conclusion_template="Trustees must diversify trust investments unless the trust instrument or circumstances justify non-diversification.",
        reasoning_framework=(
            "Diversification reduces risk and is a core principle of prudent investment. "
            "Trustees must evaluate the portfolio as a whole, considering beneficiary needs and trust purposes. "
            "Exceptions may exist if the trust instrument directs retention of specific assets or if non-diversification serves beneficiary interests. "
            "Failure to diversify may result in surcharge or removal."
        ),
        key_factors=[
            "Trust instrument directives",
            "Beneficiary needs",
            "Risk profile",
            "Portfolio composition",
            "Statutory authority"
        ],
        primary_authority=[
            "Uniform Prudent Investor Act §3",
            "Restatement (Third) of Trusts §92",
            "Bogert, Trusts and Trustees §684"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges lack of diversification",
        counter_arguments=[
            "Trust instrument directs retention",
            "Non-diversification serves beneficiary interests",
            "Portfolio is sufficiently diversified"
        ],
        resolution_strategy="Court reviews investment strategy and trust terms.",
        entity_scope="Trust investments",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Prudent Investor Act §3"
    ),
    DoctrineBlock(
        topic="Trustee Duty to Avoid Conflicts of Interest",
        keywords=["conflict of interest", "trustee", "fiduciary", "self-dealing", "trust"],
        conclusion_template="Trustees must avoid conflicts of interest and disclose any potential conflicts to beneficiaries.",
        reasoning_framework=(
            "Trustees owe a duty to act solely in the interests of beneficiaries, avoiding conflicts that may compromise impartiality. "
            "Disclosure and consent may mitigate conflicts, but trustees must exercise caution. "
            "Transactions involving trustee interests are subject to strict scrutiny. "
            "Failure to avoid or disclose conflicts may result in removal or surcharge."
        ),
        key_factors=[
            "Existence of conflict",
            "Disclosure to beneficiaries",
            "Beneficiary consent",
            "Trust instrument provisions",
            "Statutory authority"
        ],
        primary_authority=[
            "Uniform Trust Code §802",
            "Restatement (Third) of Trusts §78",
            "Bogert, Trusts and Trustees §543"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges conflict",
        counter_arguments=[
            "Conflict disclosed and consent obtained",
            "Trust instrument authorizes transaction",
            "No harm to beneficiaries"
        ],
        resolution_strategy="Court reviews disclosure and impact on beneficiaries.",
        entity_scope="Trustee actions",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §802"
    ),
    DoctrineBlock(
        topic="Trustee Duty to Maintain Records",
        keywords=["recordkeeping", "trustee", "accounting", "documentation", "trust"],
        conclusion_template="Trustees must maintain accurate records of trust administration and transactions.",
        reasoning_framework=(
            "Trustees are required to document all transactions, maintain accountings, and preserve records for review by beneficiaries and courts. "
            "Failure to maintain records may constitute a breach and hinder defense against claims. "
            "Records must be accessible and retained for statutory periods."
        ),
        key_factors=[
            "Accuracy of records",
            "Retention period",
            "Accessibility",
            "Statutory requirements",
            "Beneficiary review"
        ],
        primary_authority=[
            "Uniform Trust Code §810",
            "Restatement (Third) of Trusts §82",
            "Bogert, Trusts and Trustees §963"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges inadequate recordkeeping",
        counter_arguments=[
            "Records are accurate and accessible",
            "Statutory requirements met",
            "Beneficiary has access"
        ],
        resolution_strategy="Court reviews recordkeeping practices.",
        entity_scope="Trust administration",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §810"
    ),
    DoctrineBlock(
        topic="Trustee Duty to Act with Reasonable Care",
        keywords=["reasonable care", "trustee", "fiduciary", "trust", "administration"],
        conclusion_template="Trustees must administer the trust with reasonable care, skill, and caution.",
        reasoning_framework=(
            "Trustees are held to a standard of reasonable care, skill, and caution in all aspects of trust administration. "
            "Failure to meet this standard may result in breach and liability. "
            "Court evaluates trustee conduct in light of trust terms and circumstances."
        ),
        key_factors=[
            "Trust terms",
            "Trustee skill and experience",
            "Nature of administration",
            "Beneficiary interests",
            "Statutory standards"
        ],
        primary_authority=[
            "Uniform Trust Code §804",
            "Restatement (Third) of Trusts §77",
            "Bogert, Trusts and Trustees §541"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges lack of care",
        counter_arguments=[
            "Trustee acted with reasonable care",
            "Trust terms justified actions",
            "No harm to beneficiaries"
        ],
        resolution_strategy="Court reviews trustee conduct and circumstances.",
        entity_scope="Trust administration",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §804"
    ),
    DoctrineBlock(
        topic="Trustee Duty to Distribute Income Timely",
        keywords=["income distribution", "timeliness", "trustee", "beneficiary", "trust"],
        conclusion_template="Trustees must distribute income to beneficiaries in accordance with trust terms and in a timely manner.",
        reasoning_framework=(
            "Trustees are obligated to distribute income as directed by the trust instrument, avoiding unreasonable delay. "
            "Delays may harm beneficiaries and constitute breach. "
            "Court reviews distribution practices and trust terms."
        ),
        key_factors=[
            "Trust terms",
            "Distribution schedule",
            "Beneficiary needs",
            "Reasonableness of delay",
            "Documentation"
        ],
        primary_authority=[
            "Uniform Trust Code §1001",
            "Restatement (Third) of Trusts §87",
            "Bogert, Trusts and Trustees §861"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges delay",
        counter_arguments=[
            "Distribution was timely",
            "Delay justified by circumstances",
            "Trust terms permit delay"
        ],
        resolution_strategy="Court reviews distribution timing and justification.",
        entity_scope="Trust income distribution",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §1001"
    ),
    DoctrineBlock(
        topic="Trustee Duty to Preserve Trust Assets",
        keywords=["preservation", "trust assets", "trustee", "fiduciary", "trust"],
        conclusion_template="Trustees must take reasonable steps to preserve and protect trust assets from loss or waste.",
        reasoning_framework=(
            "Trustees are required to safeguard trust property, avoid waste, and prevent loss. "
            "Actions include insurance, maintenance, and prudent investment. "
            "Failure to preserve assets may result in surcharge or removal."
        ),
        key_factors=[
            "Nature of assets",
            "Preservation measures",
            "Risk of loss",
            "Trust terms",
            "Statutory standards"
        ],
        primary_authority=[
            "Uniform Trust Code §804",
            "Restatement (Third) of Trusts §77",
            "Bogert, Trusts and Trustees §541"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges failure to preserve assets",
        counter_arguments=[
            "Assets were preserved",
            "Loss was unavoidable",
            "Trust terms justified actions"
        ],
        resolution_strategy="Court reviews preservation efforts and asset nature.",
        entity_scope="Trust assets",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §804"
    ),
    DoctrineBlock(
        topic="Trustee Duty to Avoid Commingling",
        keywords=["commingling", "trustee", "trust assets", "fiduciary", "trust"],
        conclusion_template="Trustees must not commingle trust assets with personal or other property.",
        reasoning_framework=(
            "Commingling trust assets with personal or other property violates fiduciary duty and complicates accounting. "
            "Trustees must maintain separate accounts and records. "
            "Commingling may result in surcharge and removal."
        ),
        key_factors=[
            "Separate accounts",
            "Recordkeeping",
            "Nature of assets",
            "Trustee conduct",
            "Statutory standards"
        ],
        primary_authority=[
            "Uniform Trust Code §810",
            "Restatement (Third) of Trusts §83",
            "Bogert, Trusts and Trustees §963"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges commingling",
        counter_arguments=[
            "Assets were kept separate",
            "Commingling was inadvertent",
            "No harm resulted"
        ],
        resolution_strategy="Court reviews account structure and asset handling.",
        entity_scope="Trust assets",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §810"
    ),
    DoctrineBlock(
        topic="Trustee Duty to Follow Trust Terms",
        keywords=["trust terms", "trustee", "fiduciary", "administration", "trust"],
        conclusion_template="Trustees must administer the trust strictly in accordance with its terms unless contrary to law.",
        reasoning_framework=(
            "Trustees are bound by the terms of the trust instrument, subject to statutory and public policy exceptions. "
            "Deviation may constitute breach. "
            "Court reviews trustee actions for compliance."
        ),
        key_factors=[
            "Trust instrument language",
            "Statutory exceptions",
            "Public policy",
            "Trustee conduct",
            "Beneficiary interests"
        ],
        primary_authority=[
            "Uniform Trust Code §105",
            "Restatement (Third) of Trusts §76",
            "Bogert, Trusts and Trustees §541"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges deviation",
        counter_arguments=[
            "Actions consistent with trust terms",
            "Deviation justified by law",
            "No harm to beneficiaries"
        ],
        resolution_strategy="Court reviews trust instrument and statutory exceptions.",
        entity_scope="Trust administration",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §105"
    ),
    DoctrineBlock(
        topic="Trustee Duty to Provide Notice of Trust Existence",
        keywords=["notice", "trust existence", "trustee", "beneficiary", "trust"],
        conclusion_template="Trustees must provide notice of trust existence to qualified beneficiaries within a reasonable time after acceptance of trusteeship.",
        reasoning_framework=(
            "Trustees are required to inform qualified beneficiaries of the trust's existence, terms, and trustee identity. "
            "Notice must be timely and sufficient to protect beneficiary interests. "
            "Failure to provide notice may constitute breach."
        ),
        key_factors=[
            "Timeliness of notice",
            "Content of notice",
            "Beneficiary qualification",
            "Trust terms",
            "Statutory requirements"
        ],
        primary_authority=[
            "Uniform Trust Code §813",
            "Restatement (Third) of Trusts §82",
            "Bogert, Trusts and Trustees §963"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges lack of notice",
        counter_arguments=[
            "Notice was provided",
            "Beneficiary not qualified",
            "Trust terms limit notice"
        ],
        resolution_strategy="Court reviews notice practices and beneficiary status.",
        entity_scope="Trust administration",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §813"
    ),
    DoctrineBlock(
        topic="Trustee Duty to Avoid Unreasonable Administrative Expenses",
        keywords=["administrative expenses", "trustee", "reasonableness", "trust", "beneficiary"],
        conclusion_template="Trustees must avoid incurring unreasonable administrative expenses in trust administration.",
        reasoning_framework=(
            "Trustees must manage administrative expenses prudently, balancing cost and benefit to beneficiaries. "
            "Excessive or unnecessary expenses may constitute breach. "
            "Court reviews expense decisions for reasonableness."
        ),
        key_factors=[
            "Nature of expenses",
            "Benefit to beneficiaries",
            "Trust terms",
            "Local standards",
            "Documentation"
        ],
        primary_authority=[
            "Uniform Trust Code §805",
            "Restatement (Third) of Trusts §88",
            "Bogert, Trusts and Trustees §541"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges unreasonable expenses",
        counter_arguments=[
            "Expenses were necessary and reasonable",
            "Trust terms authorized expenses",
            "Benefit to beneficiaries justified cost"
        ],
        resolution_strategy="Court reviews expense decisions and documentation.",
        entity_scope="Trust administration",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §805"
    ),
    DoctrineBlock(
        topic="Trustee Duty to Avoid Favoritism Among Beneficiaries",
        keywords=["favoritism", "impartiality", "trustee", "beneficiary", "trust"],
        conclusion_template="Trustees must avoid favoritism and act impartially among beneficiaries.",
        reasoning_framework=(
            "Trustees must treat all beneficiaries fairly, avoiding favoritism in distributions, investment, and administration. "
            "Impartiality is a core fiduciary duty. "
            "Court reviews trustee conduct for fairness and equity."
        ),
        key_factors=[
            "Distribution practices",
            "Investment decisions",
            "Trust terms",
            "Beneficiary interests",
            "Documentation"
        ],
        primary_authority=[
            "Uniform Trust Code §803",
            "Restatement (Third) of Trusts §79",
            "Bogert, Trusts and Trustees §541"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges favoritism",
        counter_arguments=[
            "Actions were impartial",
            "Trust terms justified differences",
            "No harm to beneficiaries"
        ],
        resolution_strategy="Court reviews conduct and trust terms.",
        entity_scope="Trust administration",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §803"
    ),
    DoctrineBlock(
        topic="Trustee Duty to Invest for Total Return",
        keywords=["total return", "investment", "trustee", "fiduciary", "trust"],
        conclusion_template="Trustees must invest for total return, balancing income and capital appreciation for beneficiary interests.",
        reasoning_framework=(
            "Total return investing considers both income and capital appreciation, aligning with modern portfolio theory. "
            "Trustees must balance interests of income and remainder beneficiaries, exercising discretion consistent with trust terms and prudent investor standards."
        ),
        key_factors=[
            "Investment strategy",
            "Beneficiary interests",
            "Trust terms",
            "Risk and return",
            "Statutory standards"
        ],
        primary_authority=[
            "Uniform Prudent Investor Act §2",
            "Restatement (Third) of Trusts §90",
            "Bogert, Trusts and Trustees §684"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges imbalance",
        counter_arguments=[
            "Investment strategy balances interests",
            "Trust terms justify approach",
            "No harm to beneficiaries"
        ],
        resolution_strategy="Court reviews investment strategy and beneficiary impact.",
        entity_scope="Trust investments",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Prudent Investor Act §2"
    ),
    DoctrineBlock(
        topic="Trustee Duty to Avoid Waste",
        keywords=["waste", "trustee", "trust assets", "fiduciary", "trust"],
        conclusion_template="Trustees must avoid waste and unnecessary depletion of trust assets.",
        reasoning_framework=(
            "Waste includes unnecessary depletion, neglect, or imprudent use of trust assets. "
            "Trustees must preserve assets and maximize value for beneficiaries. "
            "Court reviews asset management and preservation efforts."
        ),
        key_factors=[
            "Nature of waste",
            "Preservation efforts",
            "Trust terms",
            "Beneficiary interests",
            "Documentation"
        ],
        primary_authority=[
            "Uniform Trust Code §804",
            "Restatement (Third) of Trusts §77",
            "Bogert, Trusts and Trustees §541"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges waste",
        counter_arguments=[
            "No waste occurred",
            "Preservation efforts were reasonable",
            "Trust terms justified actions"
        ],
        resolution_strategy="Court reviews asset management and impact.",
        entity_scope="Trust assets",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §804"
    ),
    DoctrineBlock(
        topic="Trustee Duty to Act in Good Faith",
        keywords=["good faith", "trustee", "fiduciary", "trust", "administration"],
        conclusion_template="Trustees must act in good faith and in accordance with the purposes of the trust.",
        reasoning_framework=(
            "Good faith requires honesty, fairness, and adherence to trust purposes. "
            "Trustees must avoid self-interest and act for the benefit of beneficiaries. "
            "Court reviews trustee conduct for good faith and compliance."
        ),
        key_factors=[
            "Trustee intent",
            "Trust purposes",
            "Beneficiary interests",
            "Trust terms",
            "Statutory standards"
        ],
        primary_authority=[
            "Uniform Trust Code §105",
            "Restatement (Third) of Trusts §76",
            "Bogert, Trusts and Trustees §541"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges bad faith",
        counter_arguments=[
            "Actions were in good faith",
            "Trust purposes served",
            "No harm to beneficiaries"
        ],
        resolution_strategy="Court reviews conduct and trust purposes.",
        entity_scope="Trust administration",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §105"
    ),
    DoctrineBlock(
        topic="Trustee Duty to Avoid Unauthorized Loans",
        keywords=["unauthorized loans", "trustee", "trust assets", "fiduciary", "trust"],
        conclusion_template="Trustees must not make loans of trust assets unless authorized by the trust instrument or applicable law.",
        reasoning_framework=(
            "Unauthorized loans expose trust assets to risk and may constitute breach. "
            "Trust instrument or statute must authorize lending. "
            "Court reviews loan terms and authorization."
        ),
        key_factors=[
            "Trust instrument authorization",
            "Statutory authority",
            "Loan terms",
            "Beneficiary interests",
            "Documentation"
        ],
        primary_authority=[
            "Uniform Trust Code §815",
            "Restatement (Third) of Trusts §86",
            "Bogert, Trusts and Trustees §541"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges unauthorized loan",
        counter_arguments=[
            "Loan authorized by trust terms",
            "Statutory authority exists",
            "Loan terms are prudent"
        ],
        resolution_strategy="Court reviews authorization and loan prudence.",
        entity_scope="Trust assets",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §815"
    ),
    DoctrineBlock(
        topic="Trustee Duty to Avoid Unauthorized Investments",
        keywords=["unauthorized investments", "trustee", "trust assets", "fiduciary", "trust"],
        conclusion_template="Trustees must not invest trust assets in unauthorized investments unless permitted by the trust instrument or applicable law.",
        reasoning_framework=(
            "Unauthorized investments may expose trust assets to undue risk and constitute breach. "
            "Trust instrument or statute must permit investment. "
            "Court reviews investment authorization and prudence."
        ),
        key_factors=[
            "Trust instrument authorization",
            "Statutory authority",
            "Investment prudence",
            "Beneficiary interests",
            "Documentation"
        ],
        primary_authority=[
            "Uniform Prudent Investor Act §2",
            "Restatement (Third) of Trusts §90",
            "Bogert, Trusts and Trustees §684"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges unauthorized investment",
        counter_arguments=[
            "Investment authorized by trust terms",
            "Statutory authority exists",
            "Investment is prudent"
        ],
        resolution_strategy="Court reviews authorization and investment prudence.",
        entity_scope="Trust assets",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Prudent Investor Act §2"
    ),
    DoctrineBlock(
        topic="Trustee Duty to Avoid Unauthorized Delegation",
        keywords=["unauthorized delegation", "trustee", "fiduciary", "trust", "agent"],
        conclusion_template="Trustees must not delegate duties or powers unless authorized by the trust instrument or applicable law.",
        reasoning_framework=(
            "Unauthorized delegation may compromise fiduciary duties and expose trust assets to risk. "
            "Trust instrument or statute must permit delegation. "
            "Court reviews delegation authorization and oversight."
        ),
        key_factors=[
            "Trust instrument authorization",
            "Statutory authority",
            "Agent qualifications",
            "Oversight and monitoring",
            "Beneficiary interests"
        ],
        primary_authority=[
            "Uniform Trust Code §807",
            "Restatement (Third) of Trusts §80",
            "Bogert, Trusts and Trustees §962"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges unauthorized delegation",
        counter_arguments=[
            "Delegation authorized by trust terms",
            "Statutory authority exists",
            "Oversight maintained"
        ],
        resolution_strategy="Court reviews authorization and oversight.",
        entity_scope="Trustee functions",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §807"
    ),
    DoctrineBlock(
        topic="Trustee Duty to Avoid Unauthorized Distributions",
        keywords=["unauthorized distributions", "trustee", "beneficiary", "trust", "fiduciary"],
        conclusion_template="Trustees must not make distributions to beneficiaries unless authorized by the trust instrument or applicable law.",
        reasoning_framework=(
            "Unauthorized distributions may violate trust terms and harm other beneficiaries. "
            "Trust instrument or statute must authorize distribution. "
            "Court reviews distribution authorization and impact."
        ),
        key_factors=[
            "Trust instrument authorization",
            "Statutory authority",
            "Distribution impact",
            "Beneficiary interests",
            "Documentation"
        ],
        primary_authority=[
            "Uniform Trust Code §1001",
            "Restatement (Third) of Trusts §87",
            "Bogert, Trusts and Trustees §861"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges unauthorized distribution",
        counter_arguments=[
            "Distribution authorized by trust terms",
            "Statutory authority exists",
            "Distribution is fair"
        ],
        resolution_strategy="Court reviews authorization and impact on beneficiaries.",
        entity_scope="Trust distributions",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §1001"
    ),
    DoctrineBlock(
        topic="Trustee Duty to Avoid Unauthorized Compensation",
        keywords=["unauthorized compensation", "trustee", "fees", "trust", "fiduciary"],
        conclusion_template="Trustees must not accept compensation unless authorized by the trust instrument or applicable law.",
        reasoning_framework=(
            "Unauthorized compensation violates fiduciary duty and may constitute breach. "
            "Trust instrument or statute must authorize compensation. "
            "Court reviews compensation authorization and reasonableness."
        ),
        key_factors=[
            "Trust instrument authorization",
            "Statutory authority",
            "Fee reasonableness",
            "Beneficiary interests",
            "Documentation"
        ],
        primary_authority=[
            "Uniform Trust Code §708",
            "Restatement (Third) of Trusts §38",
            "Bogert, Trusts and Trustees §977"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges unauthorized compensation",
        counter_arguments=[
            "Compensation authorized by trust terms",
            "Statutory authority exists",
            "Fee is reasonable"
        ],
        resolution_strategy="Court reviews authorization and fee reasonableness.",
        entity_scope="Trustee compensation",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §708"
    ),
    DoctrineBlock(
        topic="Trustee Duty to Avoid Unauthorized Amendments",
        keywords=["unauthorized amendments", "trustee", "trust terms", "fiduciary", "trust"],
        conclusion_template="Trustees must not amend trust terms unless authorized by the trust instrument or applicable law.",
        reasoning_framework=(
            "Unauthorized amendments may violate settlor intent and harm beneficiaries. "
            "Trust instrument or statute must authorize amendment. "
            "Court reviews amendment authorization and impact."
        ),
        key_factors=[
            "Trust instrument authorization",
            "Statutory authority",
            "Amendment impact",
            "Beneficiary interests",
            "Documentation"
        ],
        primary_authority=[
            "Uniform Trust Code §411",
            "Restatement (Third) of Trusts §65",
            "Bogert, Trusts and Trustees §994"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges unauthorized amendment",
        counter_arguments=[
            "Amendment authorized by trust terms",
            "Statutory authority exists",
            "Amendment is fair"
        ],
        resolution_strategy="Court reviews authorization and impact on beneficiaries.",
        entity_scope="Trust terms",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §411"
    ),
    DoctrineBlock(
        topic="Trustee Duty to Avoid Unauthorized Termination",
        keywords=["unauthorized termination", "trustee", "trust", "fiduciary", "beneficiary"],
        conclusion_template="Trustees must not terminate trusts unless authorized by the trust instrument or applicable law.",
        reasoning_framework=(
            "Unauthorized termination may violate settlor intent and harm beneficiaries. "
            "Trust instrument or statute must authorize termination. "
            "Court reviews termination authorization and impact."
        ),
        key_factors=[
            "Trust instrument authorization",
            "Statutory authority",
            "Termination impact",
            "Beneficiary interests",
            "Documentation"
        ],
        primary_authority=[
            "Uniform Trust Code §414",
            "Restatement (Third) of Trusts §61",
            "Bogert, Trusts and Trustees §1015"
        ],
        burden_holder="Trustee",
        adversary_position="Beneficiary alleges unauthorized termination",
        counter_arguments=[
            "Termination authorized by trust terms",
            "Statutory authority exists",
            "Termination is fair"
        ],
        resolution_strategy="Court reviews authorization and impact on beneficiaries.",
        entity_scope="Trust existence",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Uniform Trust Code §414"
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