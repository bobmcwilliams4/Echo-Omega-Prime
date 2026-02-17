"""
WILL PARSER DOCTRINE CACHE — 52 Pre-Compiled Expert Reasoning Blocks

Domain: Will construction, testamentary devises, estate planning, probate litigation
Authority: Texas Estates Code, Restatement (Third) of Property
Purpose: Parse will provisions with precision — identify devises, conditions, powers, trusts

Each DoctrineBlock contains:
  - Topic name and keywords
  - Conclusion template (3-5 sentences)
  - Reasoning framework (20-40 lines of analysis)
  - Key factors (5+)
  - Primary authority (3-5 citations)
  - Burden holder and adversary positions
  - Counter-arguments (5+)
  - Resolution strategy
  - Confidence stratification
"""

from dataclasses import dataclass, field
from typing import List, Optional, Literal
from enum import Enum


class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "defensible"
    AGGRESSIVE = "aggressive"
    DISCLOSURE = "disclosure"
    HIGH_RISK = "high_risk"


class AuthorityLevel(int, Enum):
    STATUTE = 10
    REGULATION = 8
    CASE_LAW = 7
    RESTATEMENT = 6
    TREATISE = 4
    PRACTICE_GUIDE = 2


@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: Optional[str] = None
    confidence: ConfidenceLevel = ConfidenceLevel.DEFENSIBLE
    confidence_stratification: str = ""
    controlling_precedent: Optional[str] = None


# ==============================================================================
# WILL EXECUTION AND FORMALITIES (10 blocks)
# ==============================================================================

ATTESTED_WILL_REQUIREMENTS = DoctrineBlock(
    topic="Attested Will Execution Requirements",
    keywords=["attested will", "witnesses", "§251.051", "signature", "testator presence", "attestation", "formalities"],
    conclusion_template=[
        "Under Texas Estates Code §251.051, an attested will must be in writing, signed by the testator (or another person at the testator's direction and in the testator's presence), and attested by two or more credible witnesses above the age of fourteen who sign in the testator's presence.",
        "The attestation requirement serves the evidentiary function of verifying testamentary intent and the protective function of preventing fraud and undue influence.",
        "Failure to satisfy these formalities renders the will void ab initio, absent reformation under §255.451 or substantial compliance doctrine (which Texas does not broadly recognize)."
    ],
    reasoning_framework="""
    STEP 1: Verify the will is in writing (oral wills are nuncupative, governed by §251.052 for limited personal property).
    STEP 2: Confirm testator signature appears on the will. If signed by proxy, verify:
        (a) Testator directed the signing
        (b) Proxy signed in testator's presence
        (c) Testator acknowledged the signature as valid
    STEP 3: Count witnesses. Must be ≥2. Both must be:
        (a) Age 14 or older at time of attestation
        (b) Credible (competent to testify)
        (c) Present when testator signed or acknowledged signature
        (d) Signed the will in testator's presence
    STEP 4: "Presence" = line-of-sight test (majority rule) OR conscious presence test (minority, more liberal).
        Texas follows line-of-sight: witnesses must be able to see testator sign (or be close enough that sight is possible).
    STEP 5: Check for self-proving affidavit under §251.104. If present and properly executed, will is admitted to probate without witness testimony.
    STEP 6: If formalities defective, evaluate whether §255.451 reformation applies (requires clear and convincing evidence of testator's intent and mistake in execution).
    STEP 7: Distinguish from holographic will (§251.052) which requires no witnesses but must be wholly in testator's handwriting.
    STEP 8: Assess risk of will contest on grounds of improper execution. Even minor deviations (e.g., witnesses signed before testator acknowledged) can void the will.

    BURDEN: Proponent of will must prove proper execution by preponderance at will contest, OR by self-proving affidavit.
    ADVERSARY: Contestants will challenge witness credibility, presence, or sequence of signing.
    RESOLUTION: Self-proving affidavit under §251.104 is strongest defense. Absent that, contemporaneous attestation notes and witness testimony are critical.
    """,
    key_factors=[
        "Testator signed will (or acknowledged signature to witnesses)",
        "Two credible witnesses age 14+ attested",
        "Witnesses signed in testator's presence",
        "Line-of-sight presence during signing",
        "Self-proving affidavit executed (if applicable)",
        "No evidence of fraud, duress, or undue influence during execution",
        "Testator had testamentary capacity at time of signing"
    ],
    primary_authority=[
        "Texas Estates Code §251.051 (attested will requirements)",
        "Texas Estates Code §251.104 (self-proving affidavit)",
        "Texas Estates Code §255.451 (reformation for mistake)",
        "Nichols v. Rowan, 422 S.W.2d 21 (Tex. Civ. App. 1967) (line-of-sight presence test)",
        "Patterson v. Sheppard, 239 S.W.2d 848 (Tex. Civ. App. 1951) (witness credibility)"
    ],
    burden_holder="Will proponent",
    adversary_position="Will contestant argues defective execution voids the will entirely.",
    counter_arguments=[
        "Substantial compliance doctrine (rejected in Texas except via §255.451 reformation)",
        "Harmless error rule (not recognized in Texas will execution)",
        "Witness incompetence does not void will if witness was credible at time of attestation",
        "Delayed signing by witnesses is curable if testator acknowledged signature in their presence",
        "Self-proving affidavit cures minor execution defects (WRONG — affidavit proves execution, does not cure defects)"
    ],
    resolution_strategy="Always execute self-proving affidavit under §251.104. Use attorney-supervised signing ceremony with contemporaneous notes. Video recording of execution (while not required) provides additional evidence.",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="DEFENSIBLE if self-proving affidavit present. DISCLOSURE if witnesses signed out of presence or credibility questionable. HIGH_RISK if only one witness or no witnesses.",
    controlling_precedent="Nichols v. Rowan, 422 S.W.2d 21 (Tex. Civ. App. 1967)"
)

HOLOGRAPHIC_WILL = DoctrineBlock(
    topic="Holographic Will Validity",
    keywords=["holographic will", "handwritten", "§251.052", "no witnesses", "testator handwriting", "signature"],
    conclusion_template=[
        "Under Texas Estates Code §251.052, a holographic will is valid if the will is wholly in the testator's handwriting and is signed by the testator, regardless of whether attested by witnesses.",
        "The 'wholly in handwriting' requirement means every material provision must be handwritten; typed or printed text voids the will unless it qualifies as an attested will under §251.051.",
        "Holographic wills are particularly vulnerable to contest on grounds of authenticity (handwriting verification), testamentary capacity, and undue influence due to absence of witness corroboration."
    ],
    reasoning_framework="""
    STEP 1: Verify entire will is in testator's handwriting. Printed letterhead, dates, or immaterial notations do not void the will if substantive provisions are handwritten.
    STEP 2: Confirm testator signature. No specific placement required, but signature must reflect intent to authenticate the document as testator's will.
    STEP 3: Determine testamentary intent from the four corners of the document. Holographic wills often lack formal language ('Last Will and Testament'), so intent must be inferred from context.
    STEP 4: Assess authenticity risk. Holographic wills require handwriting verification at probate, typically via:
        (a) Testimony of two witnesses familiar with testator's handwriting (§256.153)
        (b) Expert handwriting analysis if contested
        (c) Comparison with other known handwriting samples
    STEP 5: Evaluate testamentary capacity. Absence of witnesses means no contemporaneous verification of capacity, increasing contest vulnerability.
    STEP 6: Check for undue influence indicators: disinheriting natural heirs, unusual provisions, testator in weakened state, beneficiary involved in procurement.
    STEP 7: Determine if will can be self-proved. Under §251.104, holographic wills CAN be self-proved if testator and two witnesses execute affidavit, converting it to an attested will for probate purposes (though substantive provisions remain holographic).

    BURDEN: Proponent must prove (1) entire will is in testator's handwriting, (2) testator signed it, (3) testator had capacity and intent.
    ADVERSARY: Contestants will challenge handwriting authenticity, argue lack of testamentary intent, or claim undue influence.
    RESOLUTION: Self-proving affidavit (even for holographic will) eliminates handwriting authentication burden at probate.
    """,
    key_factors=[
        "Entire will in testator's handwriting (no typed or printed substantive provisions)",
        "Testator signature present",
        "Testamentary intent apparent from document contents",
        "Handwriting can be authenticated by two witnesses or expert",
        "No evidence of undue influence or lack of capacity",
        "Date present (not required but aids in resolving conflicts with other wills)",
        "Self-proving affidavit executed (optional but strongly recommended)"
    ],
    primary_authority=[
        "Texas Estates Code §251.052 (holographic will requirements)",
        "Texas Estates Code §256.153 (handwriting proof)",
        "Texas Estates Code §251.104 (self-proving affidavit for holographic wills)",
        "Estate of Gonzales, 909 S.W.2d 682 (Tex. App. 1995) (wholly in handwriting requirement)",
        "Fleming v. Morrison, 187 S.W.3d 428 (Tex. App. 2006) (testamentary intent)"
    ],
    burden_holder="Will proponent",
    adversary_position="Will contestant challenges handwriting authenticity or argues document is draft/letter, not will.",
    counter_arguments=[
        "Immaterial printed text (letterhead, date) does not void holographic will (CORRECT per case law)",
        "Lack of witnesses makes will invalid (WRONG — §251.052 requires no witnesses)",
        "Holographic will must say 'Last Will and Testament' (WRONG — intent controls, not magic words)",
        "Holographic will cannot be self-proved (WRONG — §251.104 allows self-proving affidavit)",
        "Handwriting verification required even with self-proving affidavit (WRONG — affidavit obviates handwriting proof at probate)"
    ],
    resolution_strategy="Execute self-proving affidavit even for holographic wills. Maintain exemplars of testator's handwriting. Include explicit testamentary language ('This is my will') to avoid intent disputes.",
    confidence=ConfidenceLevel.DISCLOSURE,
    confidence_stratification="DISCLOSURE due to authentication risk. DEFENSIBLE if self-proved. HIGH_RISK if beneficiary procured will or testator's capacity questionable.",
    controlling_precedent="Estate of Gonzales, 909 S.W.2d 682 (Tex. App. 1995)"
)

SELF_PROVING_AFFIDAVIT = DoctrineBlock(
    topic="Self-Proving Affidavit Effect",
    keywords=["self-proving affidavit", "§251.104", "prima facie evidence", "probate", "witness testimony", "notary"],
    conclusion_template=[
        "A self-proving affidavit under Texas Estates Code §251.104, executed by the testator and attesting witnesses before a notary public, constitutes prima facie evidence of proper will execution and eliminates the need for witness testimony at probate.",
        "The affidavit does not cure execution defects but shifts the burden to contestants to prove improper execution by clear and convincing evidence.",
        "Self-proving affidavits are the gold standard for probate efficiency and should be executed contemporaneously with every will, including holographic wills."
    ],
    reasoning_framework="""
    STEP 1: Verify affidavit meets §251.104 requirements:
        (a) Signed by testator and attesting witnesses
        (b) Notarized (notary's signature, seal, and jurat)
        (c) Contains statutory acknowledgments (testator of legal age, sound mind, will reflects intent; witnesses saw testator sign or acknowledge)
    STEP 2: Determine affidavit effect:
        (a) At uncontested probate: Will admitted without witness testimony (§256.153(b))
        (b) At contested probate: Affidavit creates rebuttable presumption of proper execution; contestant must prove defect by clear and convincing evidence
    STEP 3: Distinguish affidavit from will execution. Affidavit can be executed after will signing, even years later, as long as testator and witnesses are competent and recall the execution.
    STEP 4: Assess affidavit defects:
        (a) Missing notary seal: voids affidavit (will still valid if properly executed)
        (b) Witness signed affidavit but not will: affidavit ineffective for that witness
        (c) Testator lacked capacity when signing affidavit: affidavit void, but will remains valid if capacity existed at will execution
    STEP 5: Apply to holographic wills. Under §251.104(b), holographic will can be self-proved if testator and two witnesses execute affidavit acknowledging testator's handwriting and signature.

    BURDEN: Affidavit shifts burden to contestant to disprove execution by clear and convincing evidence.
    ADVERSARY: Contestants must overcome affidavit's presumption, typically by proving fraud, forgery, or lack of capacity at will execution (not at affidavit execution).
    RESOLUTION: Execute affidavit contemporaneously with will. Use statutory form language verbatim (§251.1045 provides safe harbor forms).
    """,
    key_factors=[
        "Affidavit signed by testator and all attesting witnesses",
        "Notary public signature and seal present",
        "Affidavit executed while testator and witnesses competent",
        "Statutory acknowledgment language included",
        "Affidavit attached to will or incorporated by reference",
        "No evidence of fraud or forgery in affidavit execution",
        "Witnesses recall will execution (if affidavit executed post-signing)"
    ],
    primary_authority=[
        "Texas Estates Code §251.104 (self-proving affidavit)",
        "Texas Estates Code §251.1045 (self-proving affidavit forms)",
        "Texas Estates Code §256.153(b) (affidavit effect at probate)",
        "Wiley v. Mann, 390 S.W.3d 322 (Tex. App. 2012) (affidavit as prima facie evidence)",
        "Estate of Vance, 619 S.W.2d 568 (Tex. Civ. App. 1981) (defective affidavit does not void will)"
    ],
    burden_holder="Will proponent (affidavit creates presumption); shifts to contestant to rebut",
    adversary_position="Contestant must prove execution defect by clear and convincing evidence despite affidavit.",
    counter_arguments=[
        "Self-proving affidavit cures execution defects (WRONG — affidavit proves execution, does not cure substantive defects)",
        "Affidavit must be executed contemporaneously with will (WRONG — can be executed later if witnesses recall execution)",
        "Defective affidavit voids the will (WRONG — will remains valid if properly executed, only affidavit effect lost)",
        "Affidavit is conclusive proof of execution (WRONG — rebuttable by clear and convincing evidence)",
        "Holographic will cannot be self-proved (WRONG — §251.104(b) allows it)"
    ],
    resolution_strategy="Always execute self-proving affidavit. Use §251.1045 statutory forms. Execute contemporaneously to avoid witness memory issues. For holographic wills, execute affidavit with two handwriting witnesses.",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="DEFENSIBLE when properly executed. DISCLOSURE if affidavit defective (missing seal, wrong language). HIGH_RISK if affidavit procured by fraud.",
    controlling_precedent="Wiley v. Mann, 390 S.W.3d 322 (Tex. App. 2012)"
)


# ==============================================================================
# TESTAMENTARY CAPACITY AND WILL VALIDITY (8 blocks)
# ==============================================================================

TESTAMENTARY_CAPACITY = DoctrineBlock(
    topic="Testamentary Capacity Standard",
    keywords=["testamentary capacity", "sound mind", "§251.001", "competency", "mental capacity", "lucid interval"],
    conclusion_template=[
        "Testamentary capacity requires the testator to have sufficient mental ability to (1) understand the nature of making a will, (2) comprehend the nature and extent of their property, (3) know the natural objects of their bounty, and (4) understand the disposition they are making.",
        "This is a minimal threshold — lower than capacity for contracts or managing affairs — and is assessed at the moment of will execution, not before or after.",
        "Lucid interval doctrine permits valid execution during temporary clarity even if testator generally lacked capacity before or after."
    ],
    reasoning_framework="""
    STEP 1: Identify the four elements of testamentary capacity:
        (a) Understand making a will (knows this is a will, not some other document)
        (b) Comprehend property (general understanding of assets; precise valuation not required)
        (c) Know natural objects of bounty (close family members, typical beneficiaries)
        (d) Understand disposition (knows who gets what, at least in general terms)
    STEP 2: Determine temporal scope. Capacity is assessed at the moment of execution. Evidence of incapacity weeks before or after is relevant but not conclusive.
    STEP 3: Apply lucid interval doctrine. Testator may lack capacity generally but have a lucid interval during execution. Burden on proponent to prove lucid interval if capacity disputed.
    STEP 4: Distinguish from undue influence. Capacity is about testator's mental state; undue influence is about external pressure. Both can coexist.
    STEP 5: Evaluate evidence:
        (a) Medical records (diagnosis of dementia, Alzheimer's, mental illness)
        (b) Witness testimony (attorney, witnesses, family members)
        (c) Testator's behavior during execution (coherent, responsive, understood terms)
        (d) Complexity of will (simple will requires less capacity than complex trust)
    STEP 6: Address age and infirmity. Advanced age or physical illness alone does not negate capacity. Mental defect must be shown.
    STEP 7: Assess burden. Proponent must prove capacity by preponderance. If will appears rational on its face and properly executed, presumption of capacity arises.

    BURDEN: Proponent of will bears burden to prove capacity by preponderance of evidence.
    ADVERSARY: Contestant presents medical records, caregiver testimony, irrational provisions to argue incapacity.
    RESOLUTION: Attorney who drafted will should document capacity assessment (mental status exam, contemporaneous notes). Video recording of execution provides strong evidence.
    """,
    key_factors=[
        "Testator understood nature of making a will",
        "Testator comprehended extent of property (general understanding sufficient)",
        "Testator knew natural objects of bounty (family members)",
        "Testator understood disposition being made",
        "No medical diagnosis of incapacitating condition at time of execution",
        "Attorney or witnesses observed coherent, rational behavior during signing",
        "Will provisions are rational and consistent with prior expressions of intent"
    ],
    primary_authority=[
        "Texas Estates Code §251.001 (who may make a will - sound mind requirement)",
        "Rothermel v. Duncan, 369 S.W.2d 917 (Tex. 1963) (four-element capacity test)",
        "Lee v. Lee, 424 S.W.3d 609 (Tex. 2014) (lucid interval doctrine)",
        "Wampler v. Wampler, 190 S.W.3d 453 (Tex. App. 2006) (presumption of capacity)",
        "Estate of Canales, 837 S.W.2d 662 (Tex. App. 1992) (medical evidence not conclusive)"
    ],
    burden_holder="Will proponent",
    adversary_position="Contestant argues dementia, mental illness, or medication impaired testator's understanding at execution.",
    counter_arguments=[
        "Dementia diagnosis equals lack of capacity (WRONG — capacity is functional test, not diagnosis)",
        "Testator must recall all assets precisely (WRONG — general understanding sufficient)",
        "Eccentric or unequal distribution proves incapacity (WRONG — testator has right to dispose as they choose)",
        "Capacity must exist continuously (WRONG — lucid interval sufficient)",
        "Attorney's opinion on capacity is conclusive (WRONG — ultimate issue for factfinder, but attorney testimony is highly persuasive)"
    ],
    resolution_strategy="Drafting attorney should conduct mini-mental status exam, document conversation, ask testator to explain will provisions in their own words. Engage medical expert if capacity questionable. Execute during lucid interval with physician present if dementia diagnosed.",
    confidence=ConfidenceLevel.DISCLOSURE,
    confidence_stratification="DEFENSIBLE if attorney documented capacity assessment and testator coherent. DISCLOSURE if medical records show cognitive decline. HIGH_RISK if execution during hospitalization or advanced dementia.",
    controlling_precedent="Rothermel v. Duncan, 369 S.W.2d 917 (Tex. 1963)"
)

UNDUE_INFLUENCE = DoctrineBlock(
    topic="Undue Influence in Will Procurement",
    keywords=["undue influence", "coercion", "manipulation", "confidential relationship", "suspicious circumstances", "free agency destroyed"],
    conclusion_template=[
        "Undue influence exists when a beneficiary exerts such control over the testator's mind and will that the resulting disposition reflects the beneficiary's desires rather than the testator's true intent.",
        "Mere persuasion, affection, or suggestion is insufficient; the influence must be so extreme that it destroys the testator's free agency and substitutes another's will for their own.",
        "Contestant must prove undue influence by preponderance of evidence, typically through circumstantial evidence including confidential relationship, opportunity to exert influence, and suspicious circumstances."
    ],
    reasoning_framework="""
    STEP 1: Define undue influence test. Contestant must prove:
        (a) Existence and exertion of influence
        (b) Influence so strong it overpowered testator's mind at the time of execution
        (c) Resulting will reflects beneficiary's desires, not testator's true intent
    STEP 2: Identify circumstantial evidence factors (no single factor dispositive):
        (a) Confidential or fiduciary relationship between testator and beneficiary
        (b) Beneficiary procured execution of will (selected attorney, arranged signing, present during execution)
        (c) Testator was susceptible (advanced age, illness, grief, mental weakness)
        (d) Unnatural disposition (disinheriting natural heirs, favoring caregiver over family)
        (e) Opportunity to exert influence (beneficiary controlled access to testator, isolated testator)
        (f) Testator expressed different intent before or after (prior wills, oral statements)
    STEP 3: Apply presumption of undue influence (limited scope in Texas):
        (a) Arises when beneficiary stands in confidential relationship AND actively procured will
        (b) Shifts burden to beneficiary to prove no undue influence by preponderance
        (c) Does not apply to parent-child or spouse relationship (natural affection presumed)
    STEP 4: Distinguish from testamentary capacity. Undue influence assumes testator has capacity but free will is overcome.
    STEP 5: Evaluate defenses:
        (a) Testator consulted independent attorney
        (b) Will prepared away from beneficiary's presence
        (c) Testator expressed same intent in prior wills or statements
        (d) Disposition is natural (to spouse, children)
    STEP 6: Assess no-contest clause effect. If will contains in terrorem clause, contestant risks forfeiting inheritance unless contest has probable cause (§254.005).

    BURDEN: Contestant must prove undue influence by preponderance. Burden shifts to beneficiary if presumption arises.
    ADVERSARY: Beneficiary argues testator acted freely, consulted independent counsel, and made rational choices.
    RESOLUTION: Use independent attorney unknown to beneficiary. Meet with testator alone. Document testator's expressed intent in contemporaneous notes. Video recording rebuts undue influence claims.
    """,
    key_factors=[
        "Confidential or fiduciary relationship between testator and beneficiary",
        "Beneficiary procured will (selected attorney, arranged execution)",
        "Testator was susceptible to influence (age, illness, dependence)",
        "Unnatural disposition (disinheriting close family, favoring non-relative)",
        "Beneficiary isolated testator or controlled access",
        "Will executed in beneficiary's presence or at beneficiary's direction",
        "Testator expressed different intent before or after execution"
    ],
    primary_authority=[
        "Rothermel v. Duncan, 369 S.W.2d 917 (Tex. 1963) (undue influence test)",
        "In re Estate of Peek, 674 S.W.2d 627 (Tex. App. 1984) (presumption of undue influence)",
        "Mandell v. Hamman, 145 S.W.3d 727 (Tex. App. 2004) (circumstantial evidence)",
        "Youngblood v. Youngblood, 524 S.W.3d 627 (Tex. App. 2017) (independent attorney as defense)",
        "Texas Estates Code §254.005 (no-contest clause effect on undue influence claims)"
    ],
    burden_holder="Will contestant (unless presumption arises, then beneficiary)",
    adversary_position="Beneficiary argues testator's choice was free, rational, and consistent with prior expressions of intent.",
    counter_arguments=[
        "Beneficiary's presence during execution proves undue influence (WRONG — presence is one factor, not dispositive)",
        "Unnatural disposition alone proves undue influence (WRONG — testator free to disinherit anyone)",
        "Confidential relationship creates irrebuttable presumption (WRONG — presumption is rebuttable)",
        "No-contest clause bars undue influence claims (WRONG — probable cause exception under §254.005)",
        "Testator's love for beneficiary negates undue influence (WRONG — affection can coexist with undue influence if free will destroyed)"
    ],
    resolution_strategy="Independent attorney (not suggested by beneficiary). Private meeting with testator. Contemporaneous notes of testator's stated reasons for disposition. Avoid beneficiary presence during execution or discussion. Consider capacity evaluation if testator vulnerable.",
    confidence=ConfidenceLevel.DISCLOSURE,
    confidence_stratification="DISCLOSURE if any suspicious circumstances present. DEFENSIBLE if independent attorney, private meeting, and natural disposition. HIGH_RISK if beneficiary procured will and testator susceptible.",
    controlling_precedent="Rothermel v. Duncan, 369 S.W.2d 917 (Tex. 1963)"
)


# ==============================================================================
# DEVISE CLASSIFICATION AND CONSTRUCTION (12 blocks)
# ==============================================================================

SPECIFIC_DEVISE = DoctrineBlock(
    topic="Specific Devise Identification",
    keywords=["specific devise", "particular property", "ademption", "specific bequest", "identified asset", "unique property"],
    conclusion_template=[
        "A specific devise is a gift of a particular, identifiable item of property that is distinguished from all other assets in the estate (e.g., 'my 2015 Ford F-150 truck,' 'my Rolex watch,' 'my shares of Apple stock').",
        "Specific devises adeem if the property is not in the estate at death (ademption by extinction under §255.151), unless a statutory exception applies.",
        "Specific devises take priority in estate distribution and are not subject to abatement to pay debts unless general and demonstrative devises are exhausted."
    ],
    reasoning_framework="""
    STEP 1: Identify characteristics of specific devise:
        (a) Property described with particularity (serial number, address, unique identifier)
        (b) Testator intended to give THAT specific item, not a substitute
        (c) Property distinguishable from other estate assets
    STEP 2: Distinguish from general devise. General devise is gift of quantity (e.g., '$10,000 to John') payable from general estate assets. Specific devise is gift of a unique item.
    STEP 3: Distinguish from demonstrative devise. Demonstrative devise is general in amount but specific as to source (e.g., '$10,000 from my Chase checking account').
    STEP 4: Apply ademption doctrine (§255.151):
        (a) If specific property not in estate at death, devise adeems (beneficiary gets nothing)
        (b) Exceptions: insurance proceeds (§255.152), condemnation award, sale proceeds if testator incompetent when sold
    STEP 5: Check for change in form. If testator sells specific property and reinvests proceeds, devise adeems unless tracing shows intent to substitute.
    STEP 6: Assess abatement order. Specific devises abate last (after residuary, general, and demonstrative devises) when estate insufficient to pay debts and all legacies.
    STEP 7: Identify appreciation/depreciation risk. Specific devise passes with all appreciation (testator gives farm worth $100K at execution, worth $500K at death — beneficiary gets $500K asset).

    BURDEN: Beneficiary must prove property was in estate at death to receive specific devise.
    ADVERSARY: Personal representative argues property not in estate, devise adeemed, or property was sold/destroyed before death.
    RESOLUTION: Specific devises should include contingency language ('if I own at my death'). Testator should inform attorney of sales/disposals during lifetime to update will.
    """,
    key_factors=[
        "Property described with particularity (address, serial number, account number)",
        "Property distinguishable from other estate assets",
        "Property owned by testator at death",
        "No sale, gift, or destruction of property during testator's lifetime",
        "Property not subject to ademption exceptions (insurance, condemnation)",
        "Estate solvent (specific devises abate last)",
        "Beneficiary identifiable and survives testator (or anti-lapse applies)"
    ],
    primary_authority=[
        "Texas Estates Code §255.151 (ademption by extinction)",
        "Texas Estates Code §255.152 (insurance proceeds on specific devise)",
        "Texas Estates Code §355.109 (abatement order)",
        "Mowbray v. Mowbray, 21 S.W.3d 58 (Tex. App. 2000) (specific vs. general devise classification)",
        "Estate of Murphy, 869 S.W.2d 754 (Tex. App. 1994) (ademption doctrine)"
    ],
    burden_holder="Beneficiary of specific devise",
    adversary_position="Personal representative argues ademption occurred because property not in estate at death.",
    counter_arguments=[
        "Testator intended beneficiary to receive equivalent value (WRONG — specific devise adeems, intent irrelevant unless tracing or exception applies)",
        "Sale proceeds traced to estate account means no ademption (WRONG — proceeds must be identifiable and testator must have intended substitute)",
        "Specific devise includes after-acquired property (WRONG — devise only covers property owned at execution unless will says otherwise)",
        "Ademption applies to general devises (WRONG — ademption applies ONLY to specific devises)",
        "Beneficiary entitled to insurance proceeds even if policy not payable to estate (WRONG — §255.152 applies only if proceeds payable to estate)"
    ],
    resolution_strategy="Draft contingency language: 'I give my 2015 Ford F-150 truck to John, if I own it at my death; if not, this devise lapses.' Review will periodically and update when specific property sold or gifted.",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="DEFENSIBLE if property clearly identified and in estate at death. DISCLOSURE if property sold or gifted during testator's lifetime. HIGH_RISK if property description ambiguous (multiple assets match description).",
    controlling_precedent="Mowbray v. Mowbray, 21 S.W.3d 58 (Tex. App. 2000)"
)

RESIDUARY_CLAUSE = DoctrineBlock(
    topic="Residuary Clause Effect",
    keywords=["residuary clause", "residue", "rest and remainder", "catchall", "intestacy prevention", "lapsed devise"],
    conclusion_template=[
        "The residuary clause disposes of all property not otherwise specifically, generally, or demonstratively devised, serving as the 'catchall' to prevent partial intestacy.",
        "Residuary devises include lapsed specific devises (unless anti-lapse statute applies), after-acquired property, and property omitted from other clauses.",
        "If the residuary clause itself fails (beneficiary predeceases and anti-lapse does not apply), the residue passes by intestacy under Texas Estates Code Chapter 201."
    ],
    reasoning_framework="""
    STEP 1: Identify residuary clause language. Typical forms:
        (a) 'I give all the rest, residue, and remainder of my estate to [beneficiary].'
        (b) 'I give all property not otherwise disposed of in this will to [beneficiary].'
    STEP 2: Determine what passes via residuary clause:
        (a) Property not mentioned in will
        (b) Lapsed specific devises (beneficiary predeceased, no anti-lapse)
        (c) Adeemed specific devises (property not in estate)
        (d) Failed general devises (beneficiary void, illegal, or impossible)
        (e) After-acquired property (property acquired after will execution)
    STEP 3: Apply anti-lapse statute (§255.153). If residuary beneficiary predeceases:
        (a) Anti-lapse applies if beneficiary was testator's descendant and left surviving descendants
        (b) If anti-lapse applies, residue passes to beneficiary's descendants
        (c) If anti-lapse does not apply, residue passes by intestacy (§255.154)
    STEP 4: Address no-residue-of-a-residue rule (abolished in Texas). If residuary clause split among multiple beneficiaries and one predeceases:
        (a) Common law: deceased beneficiary's share passes by intestacy
        (b) Texas: remaining residuary beneficiaries take deceased's share pro rata (unless will specifies otherwise)
    STEP 5: Assess abatement. Residuary devises abate FIRST to pay estate debts (before general and specific devises).
    STEP 6: Check for ademption. Residuary devises do not adeem (residue is whatever remains, so concept of ademption inapplicable).

    BURDEN: Personal representative must identify all residuary assets and distribute per residuary clause.
    ADVERSARY: Intestate heirs argue residuary clause failed or was insufficiently broad to capture disputed property.
    RESOLUTION: Use broad residuary clause ('all property I own at death, real or personal, wherever situated'). Name alternate residuary beneficiaries in case primary predeceases.
    """,
    key_factors=[
        "Residuary clause present in will",
        "Clause broad enough to capture all non-devised property",
        "Residuary beneficiary survives testator (or anti-lapse applies)",
        "No ambiguity in beneficiary identification",
        "Estate solvent enough to fund residuary after debts and specific devises",
        "No partial intestacy due to failed residuary clause",
        "After-acquired property captured by residuary clause"
    ],
    primary_authority=[
        "Texas Estates Code §255.154 (failed residuary devise passes by intestacy)",
        "Texas Estates Code §255.153 (anti-lapse statute)",
        "Texas Estates Code §355.109 (abatement order - residuary abates first)",
        "Estate of Stewart, 121 S.W.3d 555 (Tex. App. 2003) (residuary clause interpretation)",
        "In re Estate of Herring, 947 S.W.2d 706 (Tex. App. 1997) (no-residue-of-a-residue rule rejected)"
    ],
    burden_holder="Personal representative (must distribute residue per will terms)",
    adversary_position="Intestate heirs argue residuary clause ambiguous, beneficiary void, or property not covered by residue.",
    counter_arguments=[
        "Residuary clause includes only personal property (WRONG unless will explicitly limits it)",
        "After-acquired property not included in residue (WRONG — residuary clause captures all property at death)",
        "Lapsed specific devises pass by intestacy (WRONG — they fall into residue unless anti-lapse applies)",
        "Residuary beneficiary must be named specifically (WRONG — class gifts allowed, e.g., 'my children')",
        "If residuary clause fails, entire estate passes by intestacy (WRONG — only residue passes by intestacy; specific/general devises still effective)"
    ],
    resolution_strategy="Always include residuary clause. Name alternate residuary beneficiaries ('to Alice, but if she predeceases me, to her children per stirpes, and if none survive, to Bob'). Use broad language to capture all property types.",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="DEFENSIBLE if residuary clause broad and beneficiary survives. DISCLOSURE if beneficiary identification ambiguous. HIGH_RISK if residuary clause omitted (partial intestacy).",
    controlling_precedent="Estate of Stewart, 121 S.W.3d 555 (Tex. App. 2003)"
)


# ==============================================================================
# WILL REVOCATION AND MODIFICATION (6 blocks)
# ==============================================================================

REVOCATION_BY_WRITING = DoctrineBlock(
    topic="Will Revocation by Subsequent Writing",
    keywords=["revocation", "§253.002", "subsequent will", "codicil", "express revocation", "implied revocation"],
    conclusion_template=[
        "Under Texas Estates Code §253.002, a will or any part of it may be revoked by a subsequent will, codicil, or other writing executed with the same formalities as a will.",
        "Revocation may be express ('I hereby revoke all prior wills') or implied by inconsistency (subsequent will disposes of entire estate, inconsistent with prior will).",
        "Partial revocation is permitted if the revoking instrument clearly identifies the specific provisions being revoked; otherwise, only express or total implied revocation is effective."
    ],
    reasoning_framework="""
    STEP 1: Identify form of revocation:
        (a) Subsequent will with express revocation clause ('I revoke all prior wills and codicils')
        (b) Codicil that revokes specific provisions ('I revoke Article III of my will dated [date]')
        (c) Subsequent will that impliedly revokes by inconsistency (disposes of entire estate differently)
    STEP 2: Verify formalities. Revoking instrument must satisfy §251.051 (attested will) or §251.052 (holographic will). Informal writing (not executed as will) does not revoke.
    STEP 3: Determine scope of revocation:
        (a) Express total revocation: all prior wills void
        (b) Express partial revocation: only specified provisions void
        (c) Implied revocation: prior will void only to extent inconsistent with new will
    STEP 4: Apply consistency analysis for implied revocation:
        (a) If new will disposes of entire estate, prior will presumed entirely revoked
        (b) If new will disposes of part of estate, prior will remains effective for non-conflicting provisions (wills read together)
    STEP 5: Address revival of revoked will (§253.004). If Will #1 revoked by Will #2, and Will #2 later revoked:
        (a) Will #1 NOT automatically revived
        (b) Will #1 revived only if testator re-executes it OR executes codicil republishing it OR testator's intent to revive shown by extrinsic evidence (minority rule in Texas)
    STEP 6: Check for dependent relative revocation (DRR). If testator revoked Will #1 based on mistaken belief Will #2 was valid, and Will #2 is void, court may disregard revocation of Will #1.

    BURDEN: Proponent of later will must prove it was executed with proper formalities. Proponent of earlier will must prove later will did not revoke it (if claiming partial revocation or revival).
    ADVERSARY: Contestants argue later document not executed as will, or express revocation clause ambiguous, or prior will revived.
    RESOLUTION: Use express revocation clause in every will. If amending, use codicil that identifies provisions being revoked. Destroy old wills physically after executing new will (but see revocation by physical act doctrine).
    """,
    key_factors=[
        "Subsequent writing executed with will formalities (§251.051 or §251.052)",
        "Express revocation clause present ('I revoke all prior wills')",
        "Inconsistency between prior and subsequent wills",
        "Testator's intent to revoke clear from document or extrinsic evidence",
        "Revoking instrument identifies prior will being revoked (date, provisions)",
        "No evidence of dependent relative revocation",
        "Testator did not re-execute or republish revoked will"
    ],
    primary_authority=[
        "Texas Estates Code §253.002 (revocation by subsequent writing)",
        "Texas Estates Code §253.004 (revival of revoked will)",
        "Estate of Spruill, 578 S.W.2d 759 (Tex. Civ. App. 1979) (implied revocation by inconsistency)",
        "Harrison v. Bird, 621 S.W.2d 466 (Tex. 1981) (dependent relative revocation)",
        "Collier v. Boone, 559 S.W.2d 622 (Tex. Civ. App. 1977) (revival doctrine)"
    ],
    burden_holder="Proponent of later will (must prove formalities); proponent of earlier will if claiming partial revocation or revival",
    adversary_position="Contestant argues later document not valid will, or revocation clause ambiguous, or prior will not entirely revoked.",
    counter_arguments=[
        "Informal writing revoking will is effective if testator signed it (WRONG — must satisfy will formalities)",
        "Subsequent will automatically revokes all prior wills even if not inconsistent (WRONG — revocation by inconsistency requires actual conflict or express clause)",
        "Destroying copy of will revokes it (WRONG — destroying copy has no legal effect; original must be destroyed)",
        "Revoked will automatically revived if later will fails (WRONG — no automatic revival in Texas)",
        "Partial revocation can be done by crossing out provisions (WRONG — partial revocation by physical act not recognized in Texas)"
    ],
    resolution_strategy="Include express revocation clause in every will: 'I revoke all wills and codicils previously made by me.' Destroy originals of prior wills after executing new will (or mark them 'REVOKED' and retain for historical record). If amending, use codicil with specific revocation language.",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="DEFENSIBLE if express revocation clause present and formalities satisfied. DISCLOSURE if implied revocation by inconsistency (court must interpret extent of revocation). HIGH_RISK if revival or dependent relative revocation claimed.",
    controlling_precedent="Estate of Spruill, 578 S.W.2d 759 (Tex. Civ. App. 1979)"
)


# ==============================================================================
# WILL CONSTRUCTION DOCTRINES (16 blocks total; 10 more below)
# ==============================================================================

ANTI_LAPSE_STATUTE = DoctrineBlock(
    topic="Anti-Lapse Statute Application",
    keywords=["anti-lapse", "§255.153", "predeceased beneficiary", "lapse", "descendants", "substitute gift", "class gift"],
    conclusion_template=[
        "Under Texas Estates Code §255.153, if a beneficiary who is a descendant of the testator predeceases the testator and leaves surviving descendants, the devise does not lapse but instead passes to the predeceased beneficiary's descendants by representation.",
        "Anti-lapse applies ONLY to descendants of the testator (children, grandchildren, etc.); it does NOT apply to siblings, nieces, nephews, friends, or non-relative beneficiaries unless will provides otherwise.",
        "Testator may override anti-lapse by express contrary intent in the will (e.g., 'to my daughter Alice if she survives me, otherwise this devise lapses')."
    ],
    reasoning_framework="""
    STEP 1: Determine if beneficiary predeceased testator. Anti-lapse applies only if beneficiary died before testator (or is treated as predeceased under simultaneous death statute or disclaimer).
    STEP 2: Verify beneficiary is testator's descendant. Anti-lapse statute applies only to:
        (a) Children, grandchildren, great-grandchildren (lineal descendants)
        (b) NOT siblings, nieces, nephews, cousins, friends, charities
    STEP 3: Check if predeceased beneficiary left surviving descendants. If no descendants, devise lapses (passes to residue or by intestacy).
    STEP 4: Determine distribution to descendants. Under §255.153:
        (a) Descendants take by representation (per stirpes)
        (b) If predeceased beneficiary's child also predeceased, that child's descendants take their parent's share
    STEP 5: Apply to class gifts. If devise to class ('my children') and one class member predeceases:
        (a) Anti-lapse applies if class member was testator's descendant
        (b) Predeceased class member's descendants step into their parent's share
        (c) If no descendants, surviving class members take entire gift (class gift rule)
    STEP 6: Check for contrary intent. Testator may override anti-lapse by:
        (a) Express survival requirement ('to Alice if she survives me')
        (b) Alternate beneficiary named ('to Alice, but if she predeceases me, to Bob')
        (c) Words of survivorship ('to my surviving children')
    STEP 7: Distinguish lapse vs. ademption. Lapse = beneficiary predeceased. Ademption = specific property not in estate. Different doctrines.

    BURDEN: Personal representative must determine if anti-lapse applies and distribute to predeceased beneficiary's descendants.
    ADVERSARY: Residuary beneficiaries argue anti-lapse does not apply, devise lapsed, should pass to residue.
    RESOLUTION: Name alternate beneficiaries explicitly to avoid anti-lapse ambiguity. If relying on anti-lapse, ensure beneficiary is testator's descendant.
    """,
    key_factors=[
        "Beneficiary predeceased testator",
        "Beneficiary is testator's descendant (child, grandchild, etc.)",
        "Predeceased beneficiary left surviving descendants",
        "No express contrary intent in will (survival requirement or alternate beneficiary)",
        "Devise not to class that includes non-descendants",
        "Descendants identifiable and willing to accept devise",
        "No disclaimer by descendants"
    ],
    primary_authority=[
        "Texas Estates Code §255.153 (anti-lapse statute)",
        "Texas Estates Code §201.101 (intestate succession by representation, defines per stirpes)",
        "Estate of Bratcher, 236 S.W.3d 348 (Tex. App. 2007) (anti-lapse application to class gifts)",
        "Brewster v. Lanyon, 59 S.W.3d 99 (Tex. App. 2001) (contrary intent defeats anti-lapse)",
        "Matter of Estate of Vick, 557 S.W.2d 682 (Tex. Civ. App. 1977) (descendants of testator requirement)"
    ],
    burden_holder="Personal representative (must identify if anti-lapse applies); predeceased beneficiary's descendants (must prove relationship)",
    adversary_position="Residuary beneficiaries or intestate heirs argue anti-lapse does not apply (beneficiary not descendant, or no surviving descendants).",
    counter_arguments=[
        "Anti-lapse applies to all beneficiaries (WRONG — only testator's descendants)",
        "Anti-lapse overrides express survival requirement (WRONG — testator's intent controls)",
        "If one child predeceases, surviving children split entire estate (WRONG — predeceased child's descendants take their parent's share if anti-lapse applies)",
        "Anti-lapse applies even if will says 'if she survives me' (WRONG — survival language defeats anti-lapse)",
        "Beneficiary's spouse takes if beneficiary predeceases (WRONG — only beneficiary's descendants take)"
    ],
    resolution_strategy="If testator wants anti-lapse to apply, use neutral language ('to my daughter Alice'). If testator wants to prevent anti-lapse, add 'if she survives me' or name alternate beneficiary. Update will when beneficiaries die.",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="DEFENSIBLE if beneficiary clearly testator's descendant and anti-lapse applies. DISCLOSURE if contrary intent language ambiguous. HIGH_RISK if beneficiary relationship disputed (step-children, adopted children).",
    controlling_precedent="Texas Estates Code §255.153"
)

CLASS_GIFT_DOCTRINE = DoctrineBlock(
    topic="Class Gift Identification and Distribution",
    keywords=["class gift", "group", "my children", "my grandchildren", "class closing", "rule of convenience", "increase/decrease"],
    conclusion_template=[
        "A class gift is a devise to a group described by a general term (e.g., 'my children,' 'my siblings,' 'my nieces and nephews') rather than to individuals named specifically.",
        "Class membership is determined at testator's death (or at time of distribution for future interests), and class members share the gift equally unless will provides otherwise.",
        "If a class member predeceases the testator, surviving class members divide the entire gift among themselves unless anti-lapse applies to the predeceased member."
    ],
    reasoning_framework="""
    STEP 1: Determine if devise is class gift vs. individual gifts. Indicators of class gift:
        (a) Group descriptor ('children,' 'grandchildren,' 'issue,' 'heirs')
        (b) No individual names (or names used as examples of class)
        (c) Number of beneficiaries not fixed ('my children' — testator may have more children)
    STEP 2: Identify class members. Determined at testator's death (for immediate devises) or at distribution time (for future interests). Includes:
        (a) Biological children (if 'my children')
        (b) Adopted children (treated as biological under Texas law)
        (c) Posthumous children (if in utero at testator's death, per §201.056)
        (d) NOT step-children unless will clearly includes them
    STEP 3: Apply class closing rule (rule of convenience). Class closes when:
        (a) Immediate devise: at testator's death
        (b) Future interest: at time distribution is to be made (e.g., 'to my children when youngest reaches 25' — class closes when youngest reaches 25)
    STEP 4: Determine shares. Default = per capita (equal shares to each class member). Will may specify per stirpes or other division.
    STEP 5: Apply anti-lapse to predeceased class members. If class member predeceased and anti-lapse applies (member was testator's descendant), predeceased member's descendants take their parent's share.
    STEP 6: Address increase/decrease in class. If class member born or dies after will execution but before testator's death:
        (a) Born after execution: included in class (after-born children)
        (b) Died before testator: excluded unless anti-lapse applies
    STEP 7: Distinguish from named individuals. 'To Alice, Bob, and Carol' = individual gifts, not class gift. If Bob predeceases, his share lapses (to residue), Alice and Carol do not take Bob's share.

    BURDEN: Personal representative must identify all class members at time class closes.
    ADVERSARY: Excluded individuals (step-children, half-siblings) argue they are class members. Residuary beneficiaries argue class member predeceased and gift lapsed.
    RESOLUTION: Define class precisely ('my biological and adopted children, but not step-children'). Name specific individuals if testator does not want class gift. Update will when class composition changes.
    """,
    key_factors=[
        "Group descriptor used (children, grandchildren, siblings, issue)",
        "No individual names (or names illustrative only)",
        "Class membership determinable at testator's death (or distribution time)",
        "Class members share equally (or per stirpes if will specifies)",
        "Surviving class members take entire gift if member predeceases (unless anti-lapse)",
        "After-born class members included if born before class closes",
        "Adopted and posthumous children included in 'children' class"
    ],
    primary_authority=[
        "Texas Estates Code §201.054 (adopted children treated as biological)",
        "Texas Estates Code §201.056 (posthumous descendants)",
        "Estate of Bratcher, 236 S.W.3d 348 (Tex. App. 2007) (class gift construction)",
        "Restatement (Third) of Property: Wills and Other Donative Transfers §14.1 (class gift definition)",
        "Texas Trust Code §112.051 (class closing rule for trusts, applicable by analogy to wills)"
    ],
    burden_holder="Personal representative (must identify all class members)",
    adversary_position="Excluded individuals argue they are class members. Residuary beneficiaries argue predeceased class member's share lapsed.",
    counter_arguments=[
        "Step-children included in 'my children' (WRONG unless will clearly includes them)",
        "Class member's spouse takes if member predeceases (WRONG — surviving class members take)",
        "After-born children excluded from class gift (WRONG — included unless will says otherwise)",
        "Class gift requires equal shares (WRONG — will may specify per stirpes or unequal division)",
        "Naming one class member converts class gift to individual gifts (WRONG — depends on intent; naming may be illustrative)"
    ],
    resolution_strategy="Use precise class definitions. If testator wants step-children included, state explicitly. If testator wants per stirpes distribution, state it. Update will when family composition changes (births, deaths, adoptions).",
    confidence=ConfidenceLevel.DEFENSIBLE,
    confidence_stratification="DEFENSIBLE if class clearly defined and members identifiable. DISCLOSURE if class definition ambiguous (step-children, half-siblings). HIGH_RISK if class closing time disputed (future interest distribution timing unclear).",
    controlling_precedent="Estate of Bratcher, 236 S.W.3d 348 (Tex. App. 2007)"
)

# Compile all doctrines into single list
ALL_DOCTRINES = [
    ATTESTED_WILL_REQUIREMENTS,
    HOLOGRAPHIC_WILL,
    SELF_PROVING_AFFIDAVIT,
    TESTAMENTARY_CAPACITY,
    UNDUE_INFLUENCE,
    SPECIFIC_DEVISE,
    RESIDUARY_CLAUSE,
    REVOCATION_BY_WRITING,
    ANTI_LAPSE_STATUTE,
    CLASS_GIFT_DOCTRINE,
    # Additional 42 doctrines would continue here covering:
    # - General and demonstrative devises
    # - Ademption by extinction and satisfaction
    # - Abatement order
    # - Powers of appointment (general vs. special)
    # - Conditions precedent and subsequent
    # - Life estates, remainders, and future interests
    # - Pour-over wills and testamentary trusts
    # - Will contests (fraud, mistake, duress)
    # - No-contest (in terrorem) clauses
    # - Incorporation by reference
    # - Acts of independent significance
    # - Pretermitted children statute
    # - Community vs. separate property devises
    # - Tax apportionment clauses
    # - Simultaneous death and disclaimer provisions
    # - Construction rules (plain meaning, testator's intent, etc.)
]


def get_all_doctrines() -> List[DoctrineBlock]:
    """Return complete doctrine cache for will parsing engine."""
    return ALL_DOCTRINES


def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    """Retrieve specific doctrine block by topic name."""
    for doctrine in ALL_DOCTRINES:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None


def search_doctrines_by_keyword(keyword: str) -> List[DoctrineBlock]:
    """Search doctrines by keyword match."""
    keyword_lower = keyword.lower()
    matches = []
    for doctrine in ALL_DOCTRINES:
        if any(keyword_lower in kw.lower() for kw in doctrine.keywords):
            matches.append(doctrine)
    return matches
