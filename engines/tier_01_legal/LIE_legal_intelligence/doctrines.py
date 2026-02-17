"""
LIE Doctrine Extensions — Additional legal doctrine blocks.

These supplement the core doctrines embedded in engine.py with specialized
topics covering advanced legal practice areas and cross-cutting principles.

Commander: Bobby Don McWilliams II | Authority: 11.0 SOVEREIGN
"""

from __future__ import annotations

from typing import Any, Dict, List

from loguru import logger
from pydantic import BaseModel, Field


# ═══════════════════════════════════════════════════════════════════
# EXTENDED DOCTRINE BLOCKS
# ═══════════════════════════════════════════════════════════════════

class ExtendedDoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    entity_scope: str = "general"
    confidence: str = "DEFENSIBLE"
    controlling_precedent: str = ""
    adversary_position: str = ""
    counter_arguments: List[str] = Field(default_factory=list)
    resolution_strategy: str = ""
    confidence_stratification: str = ""


EXTENDED_DOCTRINES: Dict[str, ExtendedDoctrineBlock] = {}


# ── CONTRACT LAW: PAROL EVIDENCE RULE ──

EXTENDED_DOCTRINES["parol_evidence_rule"] = ExtendedDoctrineBlock(
    topic="parol_evidence_rule",
    keywords=["parol evidence", "integration", "merger clause", "contemporaneous", "prior agreement", "extrinsic evidence"],
    conclusion_template="The parol evidence rule prohibits admission of prior or contemporaneous oral or written agreements to contradict, vary, or supplement the terms of a fully integrated written contract. If the contract contains a merger clause and appears complete on its face, it is presumed to be fully integrated. Exceptions include evidence offered to show fraud, duress, mistake, ambiguity, or subsequent modification. Evidence of course of dealing, usage of trade, or course of performance may also be admissible to interpret ambiguous terms.",
    reasoning_framework="""1. Determine if the contract is fully integrated (complete on its face with merger clause).
2. Assess whether the proffered evidence is prior to or contemporaneous with the written agreement.
3. Evaluate whether the evidence contradicts, varies, or supplements the written terms.
4. Check for exceptions: fraud, duress, mistake, ambiguity, illegality, or subsequent modification.
5. Analyze whether the evidence is offered to interpret an ambiguous term (permissible) or contradict a clear term (prohibited).
6. Consider UCC §2-202 for contracts involving sale of goods.
7. Determine if course of dealing, usage of trade, or course of performance is relevant.
8. Apply the parol evidence rule or admit the evidence under an exception.""",
    key_factors=[
        "Contract is fully integrated",
        "Evidence is prior or contemporaneous",
        "Evidence contradicts or supplements written terms",
        "No exception applies (fraud, duress, mistake, ambiguity)",
    ],
    primary_authority=[
        "Restatement (Second) of Contracts §§ 209-216 (integration and parol evidence)",
        "UCC §2-202 (final written expression)",
        "Masterson v. Sine, 436 P.2d 561 (Cal. 1968) (parol evidence admissibility)",
    ],
    entity_scope="contract,parties",
    confidence="DEFENSIBLE",
    controlling_precedent="Restatement (Second) of Contracts § 216; UCC §2-202",
    adversary_position="Parol evidence is admissible to show the true intent of the parties",
    counter_arguments=[
        "Contract is ambiguous and evidence is offered to clarify meaning",
        "Evidence shows fraud or duress in formation",
        "Evidence constitutes subsequent modification",
    ],
    resolution_strategy="Establish full integration and exclude parol evidence unless exception applies",
    confidence_stratification="DEFENSIBLE for clear integrated contracts; DISCLOSURE for partially integrated or ambiguous contracts",
)


# ── LITIGATION: FEDERAL RULE 26(a) INITIAL DISCLOSURES ──

EXTENDED_DOCTRINES["fed_rule_26a_disclosures"] = ExtendedDoctrineBlock(
    topic="fed_rule_26a_disclosures",
    keywords=["initial disclosures", "rule 26", "mandatory disclosure", "damages computation", "witnesses", "documents"],
    conclusion_template="Federal Rule of Civil Procedure 26(a)(1) requires parties to provide initial disclosures without awaiting a discovery request. Disclosures must include: (1) individuals likely to have discoverable information supporting claims or defenses; (2) copies or descriptions of documents in the party's possession relevant to the claims or defenses; (3) computation of damages; and (4) insurance agreements. Disclosures are due within 14 days after the Rule 26(f) conference unless otherwise stipulated. Failure to disclose may result in exclusion of evidence at trial.",
    reasoning_framework="""1. Identify individuals with discoverable information supporting claims or defenses.
2. Compile all documents, electronically stored information, and tangible things in possession or control.
3. Prepare itemized damages computation showing each category of damages claimed.
4. Identify and provide copies of insurance agreements covering the claims.
5. Serve initial disclosures on all parties within 14 days after Rule 26(f) conference.
6. Supplement disclosures as additional information becomes available.
7. Evaluate consequences of non-disclosure: exclusion under Rule 37(c)(1).
8. Coordinate disclosures with discovery plan and Rule 26(f) conference.""",
    key_factors=[
        "Initial disclosures served within 14 days of Rule 26(f) conference",
        "All categories disclosed: witnesses, documents, damages, insurance",
        "Disclosures are complete and accurate",
        "Supplementation obligations met",
    ],
    primary_authority=[
        "Fed. R. Civ. P. 26(a)(1) (initial disclosures)",
        "Fed. R. Civ. P. 26(e) (supplementation)",
        "Fed. R. Civ. P. 37(c)(1) (failure to disclose sanctions)",
    ],
    entity_scope="litigation,parties",
    confidence="DEFENSIBLE",
    controlling_precedent="Fed. R. Civ. P. 26(a)(1)",
    adversary_position="Non-disclosure warrants exclusion of evidence",
    counter_arguments=[
        "Disclosure was substantially complied with",
        "Failure to disclose was harmless",
        "Good cause exists for late disclosure",
    ],
    resolution_strategy="Ensure timely and complete initial disclosures to avoid Rule 37(c)(1) sanctions",
    confidence_stratification="DEFENSIBLE for timely disclosures; DISCLOSURE for late or incomplete disclosures",
)


# ── EMPLOYMENT LAW: MCDONNELL DOUGLAS BURDEN-SHIFTING ──

EXTENDED_DOCTRINES["mcdonnell_douglas_burden_shift"] = ExtendedDoctrineBlock(
    topic="mcdonnell_douglas_burden_shift",
    keywords=["burden shifting", "prima facie", "legitimate nondiscriminatory reason", "pretext", "title vii", "discrimination"],
    conclusion_template="Under the McDonnell Douglas burden-shifting framework, a plaintiff alleging employment discrimination must first establish a prima facie case. The burden then shifts to the defendant to articulate a legitimate, nondiscriminatory reason for the adverse action. If the defendant meets this burden, the plaintiff must prove the stated reason is a pretext for discrimination. The ultimate burden of persuasion remains with the plaintiff at all times.",
    reasoning_framework="""1. Plaintiff establishes prima facie case: (1) member of protected class, (2) qualified for position, (3) adverse employment action, (4) circumstances suggesting discrimination.
2. Burden shifts to employer to articulate legitimate, nondiscriminatory reason.
3. Employer must produce evidence (not prove) of legitimate reason.
4. Burden shifts back to plaintiff to prove reason is pretext.
5. Plaintiff may show pretext through: inconsistencies, changing explanations, comparative evidence, proximity in time to protected activity.
6. Evaluate direct evidence vs. circumstantial evidence of discrimination.
7. Consider whether mixed-motive analysis applies.
8. Ultimate burden of persuasion remains with plaintiff throughout.""",
    key_factors=[
        "Prima facie case established",
        "Employer articulated legitimate nondiscriminatory reason",
        "Plaintiff demonstrated pretext through evidence",
        "Temporal proximity or comparative evidence supports discrimination claim",
    ],
    primary_authority=[
        "McDonnell Douglas Corp. v. Green, 411 U.S. 792 (1973)",
        "Texas Dep't of Cmty. Affairs v. Burdine, 450 U.S. 248 (1981) (pretext standard)",
        "St. Mary's Honor Ctr. v. Hicks, 509 U.S. 502 (1993) (ultimate burden on plaintiff)",
    ],
    entity_scope="employment,discrimination",
    confidence="DEFENSIBLE",
    controlling_precedent="McDonnell Douglas Corp. v. Green, 411 U.S. 792 (1973); Texas Dep't of Cmty. Affairs v. Burdine, 450 U.S. 248 (1981)",
    adversary_position="Employer's stated reason is legitimate and plaintiff cannot prove pretext",
    counter_arguments=[
        "Employer's reason is inconsistent or pretextual",
        "Temporal proximity between protected activity and adverse action",
        "Comparative evidence shows similarly situated employees treated more favorably",
    ],
    resolution_strategy="Establish prima facie case and gather evidence of pretext (inconsistencies, comparative employees, timing)",
    confidence_stratification="DEFENSIBLE for clear pretext evidence; AGGRESSIVE for circumstantial pretext claims",
)


# ── CRIMINAL LAW: MIRANDA WARNINGS ──

EXTENDED_DOCTRINES["miranda_warnings"] = ExtendedDoctrineBlock(
    topic="miranda_warnings",
    keywords=["miranda", "custodial interrogation", "right to remain silent", "right to counsel", "waiver", "suppression"],
    conclusion_template="Under Miranda v. Arizona, 384 U.S. 436 (1966), police must inform suspects in custodial interrogation of their Fifth Amendment rights: (1) right to remain silent, (2) anything said can be used against them, (3) right to an attorney, (4) right to appointed counsel if indigent. Any waiver must be knowing, intelligent, and voluntary. Statements obtained in violation of Miranda are inadmissible in the prosecution's case-in-chief but may be used for impeachment if the defendant testifies.",
    reasoning_framework="""1. Determine if suspect was in custody (reasonable person would feel free to leave?).
2. Assess whether interrogation occurred (questioning likely to elicit incriminating response).
3. Verify that Miranda warnings were given before custodial interrogation.
4. Evaluate whether suspect waived rights knowingly, intelligently, and voluntarily.
5. Check if suspect invoked right to silence or counsel (interrogation must cease).
6. Analyze whether post-invocation statements were voluntary re-initiation by suspect.
7. Determine if any exceptions apply: public safety, routine booking questions.
8. Suppress statements if Miranda violated; allow impeachment use if defendant testifies.""",
    key_factors=[
        "Suspect was in custody",
        "Interrogation occurred",
        "Miranda warnings were not given or were defective",
        "No valid waiver of Miranda rights",
        "Statements used in prosecution's case-in-chief",
    ],
    primary_authority=[
        "Miranda v. Arizona, 384 U.S. 436 (1966)",
        "Edwards v. Arizona, 451 U.S. 477 (1981) (invocation of right to counsel)",
        "New York v. Quarles, 467 U.S. 649 (1984) (public safety exception)",
        "Berghuis v. Thompkins, 560 U.S. 370 (2010) (waiver by implication)",
    ],
    entity_scope="criminal,constitutional_law",
    confidence="DEFENSIBLE",
    controlling_precedent="Miranda v. Arizona, 384 U.S. 436 (1966); Edwards v. Arizona, 451 U.S. 477 (1981)",
    adversary_position="Miranda warnings were not required or suspect validly waived rights",
    counter_arguments=[
        "Suspect was not in custody",
        "Interrogation did not occur (spontaneous statement)",
        "Public safety exception applies",
    ],
    resolution_strategy="Establish custodial interrogation without Miranda warnings and move to suppress",
    confidence_stratification="DEFENSIBLE for clear custodial interrogation; DISCLOSURE for borderline custody determinations",
)


# ── INTELLECTUAL PROPERTY: FAIR USE DEFENSE ──

EXTENDED_DOCTRINES["fair_use_defense"] = ExtendedDoctrineBlock(
    topic="fair_use_defense",
    keywords=["fair use", "copyright", "transformative", "commercial use", "parody", "criticism", "comment", "four factors"],
    conclusion_template="Fair use is an affirmative defense to copyright infringement under 17 U.S.C. § 107. Courts apply four factors: (1) purpose and character of use (transformative? commercial?), (2) nature of the copyrighted work (factual or creative?), (3) amount and substantiality of portion used, (4) effect on the market for the original. No single factor is dispositive. Transformative uses (adding new expression, meaning, or message) weigh heavily in favor of fair use. Commercial use weighs against fair use but is not dispositive.",
    reasoning_framework="""1. Assess purpose and character: is the use transformative? Is it commercial or nonprofit educational?
2. Evaluate nature of copyrighted work: factual works receive less protection than creative works.
3. Analyze amount used: was it reasonable in relation to the purpose? Was the heart of the work taken?
4. Assess market harm: does the use substitute for the original or harm potential markets?
5. Weigh all four factors together (no single factor is determinative).
6. Consider whether use is parody, criticism, comment, news reporting, scholarship, or research.
7. Evaluate transformativeness: does the new work add new meaning or message?
8. Apply fair use defense or find infringement based on the totality of factors.""",
    key_factors=[
        "Use is transformative",
        "Purpose is nonprofit educational or commentary",
        "Amount used is reasonable",
        "No substantial market harm to original",
    ],
    primary_authority=[
        "17 U.S.C. § 107 (fair use)",
        "Campbell v. Acuff-Rose Music, Inc., 510 U.S. 569 (1994) (transformative use)",
        "Sony Corp. of Am. v. Universal City Studios, Inc., 464 U.S. 417 (1984) (time-shifting)",
        "Harper & Row Publishers, Inc. v. Nation Enters., 471 U.S. 539 (1985) (market harm)",
    ],
    entity_scope="intellectual_property,copyright",
    confidence="DEFENSIBLE",
    controlling_precedent="Campbell v. Acuff-Rose Music, Inc., 510 U.S. 569 (1994); 17 U.S.C. § 107",
    adversary_position="Use is not transformative and harms the market for the original",
    counter_arguments=[
        "Use is transformative and adds new meaning",
        "Amount used is minimal",
        "No market harm demonstrated",
    ],
    resolution_strategy="Establish transformative purpose and minimal market harm to assert fair use",
    confidence_stratification="DEFENSIBLE for transformative uses with minimal market harm; AGGRESSIVE for commercial uses of creative works",
)


# ── REAL ESTATE: ADVERSE POSSESSION ──

EXTENDED_DOCTRINES["adverse_possession"] = ExtendedDoctrineBlock(
    topic="adverse_possession",
    keywords=["adverse possession", "hostile", "actual", "open and notorious", "continuous", "exclusive", "statute of limitations"],
    conclusion_template="Adverse possession allows a person to acquire title to land by meeting statutory requirements, typically: (1) hostile or adverse use (without permission), (2) actual possession, (3) open and notorious (visible), (4) continuous for the statutory period (commonly 10-20 years), and (5) exclusive (not sharing with owner or public). The claimant must prove all elements. Payment of property taxes may be required in some jurisdictions. Adverse possession does not apply to government-owned land in most states.",
    reasoning_framework="""1. Determine if possession was hostile/adverse (without permission, under claim of right).
2. Verify actual possession (physical occupation and use).
3. Assess whether possession was open and notorious (visible to the owner).
4. Confirm continuous possession for the statutory period (uninterrupted).
5. Establish exclusive possession (not shared with owner or general public).
6. Check if payment of property taxes is required in the jurisdiction.
7. Evaluate whether the statutory period was tolled (owner's disability, minority).
8. Apply adverse possession if all elements met for the statutory period.""",
    key_factors=[
        "Possession was hostile/adverse",
        "Actual physical possession",
        "Open and notorious use",
        "Continuous for statutory period",
        "Exclusive possession",
    ],
    primary_authority=[
        "State-specific adverse possession statutes",
        "Restatement (Third) of Property: Servitudes § 2.17 (2000)",
        "Van Valkenburgh v. Lutz, 106 N.E.2d 28 (N.Y. 1952) (adverse possession elements)",
    ],
    entity_scope="real_estate,property",
    confidence="DEFENSIBLE",
    controlling_precedent="State adverse possession statutes; Restatement (Third) of Property: Servitudes § 2.17",
    adversary_position="Possession was permissive or not continuous",
    counter_arguments=[
        "Possession was hostile and without permission",
        "Use was open, notorious, and continuous for statutory period",
        "All elements satisfied",
    ],
    resolution_strategy="Document continuous, hostile, open, and exclusive possession for the full statutory period",
    confidence_stratification="DEFENSIBLE for well-documented continuous possession; DISCLOSURE for disputed hostility or continuity",
)


# ── BANKRUPTCY: AUTOMATIC STAY ──

EXTENDED_DOCTRINES["automatic_stay"] = ExtendedDoctrineBlock(
    topic="automatic_stay",
    keywords=["automatic stay", "bankruptcy", "relief from stay", "cause", "adequate protection", "creditor", "collection"],
    conclusion_template="Under 11 U.S.C. § 362, the filing of a bankruptcy petition triggers an automatic stay halting all collection actions, foreclosures, repossessions, lawsuits, and garnishments against the debtor or property of the estate. The stay remains in effect until the case is closed, dismissed, or a discharge is granted. Creditors may seek relief from the stay for cause, lack of adequate protection, or if the debtor has no equity and the property is not necessary for reorganization. Willful violation of the stay may result in damages and contempt.",
    reasoning_framework="""1. Determine if bankruptcy petition has been filed (automatic stay takes effect immediately upon filing).
2. Identify the action sought: is it a collection action, lawsuit, foreclosure, or other proceeding?
3. Assess whether the action is stayed under § 362(a) (broad scope: most actions are stayed).
4. Check for exceptions to the stay under § 362(b) (criminal proceedings, domestic support, certain tax actions).
5. Evaluate whether creditor has grounds for relief from stay: cause, lack of adequate protection, no equity in property.
6. Determine if debtor has equity in the property and if it is necessary for effective reorganization.
7. File motion for relief from stay if grounds exist.
8. Determine if stay violation occurred and assess damages under § 362(k).""",
    key_factors=[
        "Bankruptcy petition filed",
        "Action is a collection action or proceeding against debtor or estate property",
        "No exception to automatic stay applies",
        "Creditor has not obtained relief from stay",
    ],
    primary_authority=[
        "11 U.S.C. § 362 (automatic stay)",
        "11 U.S.C. § 362(d) (relief from stay)",
        "11 U.S.C. § 362(k) (damages for willful violation)",
    ],
    entity_scope="bankruptcy,creditor,debtor",
    confidence="DEFENSIBLE",
    controlling_precedent="11 U.S.C. § 362",
    adversary_position="Creditor is entitled to relief from stay",
    counter_arguments=[
        "Debtor has equity in the property",
        "Property is necessary for reorganization",
        "Creditor is adequately protected",
    ],
    resolution_strategy="File bankruptcy petition to invoke automatic stay; oppose relief from stay by showing equity and necessity",
    confidence_stratification="DEFENSIBLE for clear automatic stay applications; DISCLOSURE for relief from stay disputes",
)


# ── ENVIRONMENTAL LAW: CERCLA STRICT LIABILITY ──

EXTENDED_DOCTRINES["cercla_strict_liability"] = ExtendedDoctrineBlock(
    topic="cercla_strict_liability",
    keywords=["cercla", "superfund", "strict liability", "potentially responsible party", "cleanup", "hazardous substance", "joint and several"],
    conclusion_template="The Comprehensive Environmental Response, Compensation, and Liability Act (CERCLA), 42 U.S.C. § 9601 et seq., imposes strict, joint and several liability on Potentially Responsible Parties (PRPs) for cleanup costs of hazardous substance releases. PRPs include: (1) current owners/operators, (2) owners/operators at time of disposal, (3) arrangers (generators who arranged for disposal), and (4) transporters who selected disposal sites. Liability is strict (no fault required), retroactive, and joint and several (entire liability can be imposed on one PRP). Defenses are limited: act of God, act of war, act of third party with no contractual relationship.",
    reasoning_framework="""1. Determine if the site involves a release or threatened release of a hazardous substance.
2. Identify Potentially Responsible Parties (PRPs): current owners, past owners at time of disposal, arrangers, transporters.
3. Establish that the party falls into one of the four PRP categories.
4. Assess whether strict liability applies (no need to prove negligence).
5. Evaluate whether liability is joint and several (government can pursue entire cost from one PRP).
6. Check for affirmative defenses: act of God, act of war, third-party defense (no contractual relationship).
7. Consider contribution claims among PRPs for equitable allocation.
8. Analyze whether innocent landowner or contiguous property owner defense applies.""",
    key_factors=[
        "Release or threatened release of hazardous substance",
        "Party is a current owner, past owner, arranger, or transporter",
        "Strict liability applies (no fault required)",
        "No affirmative defense available",
    ],
    primary_authority=[
        "42 U.S.C. § 9601 et seq. (CERCLA)",
        "42 U.S.C. § 9607 (liability)",
        "United States v. Chem-Dyne Corp., 572 F. Supp. 802 (S.D. Ohio 1983) (joint and several liability)",
    ],
    entity_scope="environmental,prp,cleanup",
    confidence="DEFENSIBLE",
    controlling_precedent="42 U.S.C. § 9607; United States v. Chem-Dyne Corp., 572 F. Supp. 802 (S.D. Ohio 1983)",
    adversary_position="PRP is strictly liable for cleanup costs",
    counter_arguments=[
        "Third-party defense applies (no contractual relationship)",
        "Innocent landowner defense (due diligence conducted)",
        "Divisibility of harm allows pro-rata allocation",
    ],
    resolution_strategy="Assert third-party or innocent landowner defense if applicable; seek contribution from other PRPs",
    confidence_stratification="DEFENSIBLE for clear PRP status; DISCLOSURE for third-party or innocent landowner defenses",
)


# ── HEALTHCARE LAW: HIPAA PRIVACY RULE ──

EXTENDED_DOCTRINES["hipaa_privacy_rule"] = ExtendedDoctrineBlock(
    topic="hipaa_privacy_rule",
    keywords=["hipaa", "phi", "protected health information", "covered entity", "business associate", "privacy rule", "authorization"],
    conclusion_template="The Health Insurance Portability and Accountability Act (HIPAA) Privacy Rule, 45 C.F.R. Part 160 and Part 164, Subparts A and E, protects individually identifiable health information (Protected Health Information or PHI). Covered entities (health plans, healthcare clearinghouses, healthcare providers) and business associates must comply. PHI may be used or disclosed without authorization for treatment, payment, and healthcare operations (TPO). Other uses/disclosures require patient authorization or fit within specific exceptions (public health, law enforcement, research). Violations can result in civil and criminal penalties.",
    reasoning_framework="""1. Determine if the entity is a covered entity or business associate under HIPAA.
2. Identify whether the information constitutes PHI (individually identifiable health information).
3. Assess whether the use or disclosure is for treatment, payment, or healthcare operations (TPO) (no authorization required).
4. Check if a specific exception applies: public health, law enforcement with warrant, research with IRB approval, etc.
5. If no exception applies, verify that valid patient authorization was obtained.
6. Ensure authorization is properly executed (specific description, expiration, signature).
7. Evaluate whether minimum necessary standard applies (use/disclose only minimum PHI required).
8. Assess HIPAA violation and potential penalties (civil: up to $1.9M per year; criminal: up to 10 years imprisonment).""",
    key_factors=[
        "Entity is a covered entity or business associate",
        "Information is PHI",
        "Use/disclosure not for TPO",
        "No exception applies",
        "No valid authorization obtained",
    ],
    primary_authority=[
        "45 C.F.R. Part 160 and Part 164, Subparts A and E (HIPAA Privacy Rule)",
        "42 U.S.C. § 1320d et seq. (HIPAA statutory provisions)",
    ],
    entity_scope="healthcare,covered_entity,business_associate",
    confidence="DEFENSIBLE",
    controlling_precedent="45 C.F.R. § 164.502, § 164.506, § 164.508",
    adversary_position="Disclosure violated HIPAA Privacy Rule",
    counter_arguments=[
        "Disclosure was for TPO",
        "Exception applies (public health, law enforcement)",
        "Valid authorization obtained",
    ],
    resolution_strategy="Ensure disclosures are for TPO or fall within exceptions; obtain valid authorization otherwise",
    confidence_stratification="DEFENSIBLE for TPO disclosures; DISCLOSURE for novel exception applications",
)


# ── IMMIGRATION LAW: ASYLUM STANDARD ──

EXTENDED_DOCTRINES["asylum_standard"] = ExtendedDoctrineBlock(
    topic="asylum_standard",
    keywords=["asylum", "persecution", "protected ground", "race", "religion", "nationality", "political opinion", "particular social group", "well-founded fear"],
    conclusion_template="To qualify for asylum under 8 U.S.C. § 1158, an applicant must demonstrate a well-founded fear of persecution on account of race, religion, nationality, membership in a particular social group, or political opinion. Persecution requires more than harassment or discrimination; it must be severe harm or suffering. The applicant must show both subjective fear (genuinely fears persecution) and objective basis (reasonable person would fear persecution). Past persecution creates a rebuttable presumption of future persecution. One-year filing deadline applies unless changed or extraordinary circumstances exist.",
    reasoning_framework="""1. Determine if applicant has a well-founded fear of persecution (subjective + objective).
2. Assess whether feared harm constitutes persecution (severe harm, not mere harassment).
3. Identify the protected ground: race, religion, nationality, political opinion, or particular social group.
4. Establish the nexus: persecution is on account of the protected ground (central reason).
5. Evaluate whether past persecution occurred (creates presumption of future persecution).
6. Check if applicant filed within one year of arrival (or qualifies for exception).
7. Assess whether internal relocation is reasonable (can applicant avoid persecution by moving within home country?).
8. Grant asylum if all elements satisfied; deny if nexus or persecution not established.""",
    key_factors=[
        "Well-founded fear of persecution (subjective and objective)",
        "Persecution on account of protected ground",
        "Nexus established between persecution and protected ground",
        "Filed within one year or exception applies",
    ],
    primary_authority=[
        "8 U.S.C. § 1158 (asylum)",
        "8 C.F.R. § 1208.13 (asylum standard)",
        "INS v. Cardoza-Fonseca, 480 U.S. 421 (1987) (well-founded fear standard)",
        "Matter of Acosta, 19 I&N Dec. 211 (BIA 1985) (particular social group)",
    ],
    entity_scope="immigration,asylum",
    confidence="DEFENSIBLE",
    controlling_precedent="INS v. Cardoza-Fonseca, 480 U.S. 421 (1987); 8 U.S.C. § 1158",
    adversary_position="Applicant does not have well-founded fear or nexus to protected ground",
    counter_arguments=[
        "Applicant has well-founded fear based on past persecution",
        "Nexus to protected ground is established",
        "Changed circumstances or extraordinary circumstances excuse late filing",
    ],
    resolution_strategy="Document past persecution and establish nexus to protected ground; file within one year or establish exception",
    confidence_stratification="DEFENSIBLE for past persecution cases; AGGRESSIVE for particular social group claims",
)


# ── ADR: ARBITRATION ENFORCEABILITY ──

EXTENDED_DOCTRINES["arbitration_enforceability"] = ExtendedDoctrineBlock(
    topic="arbitration_enforceability",
    keywords=["arbitration", "federal arbitration act", "faa", "enforceability", "unconscionability", "adhesion", "class waiver"],
    conclusion_template="Under the Federal Arbitration Act (FAA), 9 U.S.C. § 1 et seq., arbitration agreements are generally enforceable and favor arbitration. Courts apply state contract law defenses (fraud, duress, unconscionability) but cannot disfavor arbitration agreements. Arbitration agreements in consumer and employment contracts are enforceable even if in adhesion contracts, unless unconscionable (both procedurally and substantively). Class action waivers are generally enforceable under AT&T Mobility v. Concepcion. Exceptions: agreements in contracts of employment of transportation workers.",
    reasoning_framework="""1. Determine if a valid arbitration agreement exists (mutual assent, consideration).
2. Assess whether the FAA applies (contract involving interstate commerce).
3. Evaluate whether the dispute falls within the scope of the arbitration agreement.
4. Check for contract defenses: fraud, duress, unconscionability (procedural + substantive).
5. Analyze whether the agreement is an adhesion contract (take-it-or-leave-it).
6. Determine if unconscionability exists: lack of bargaining power + oppressive terms.
7. Assess enforceability of class action waiver (generally enforceable under Concepcion).
8. Compel arbitration if agreement is valid and enforceable; deny if unconscionable or outside FAA scope.""",
    key_factors=[
        "Valid arbitration agreement exists",
        "FAA applies",
        "Dispute within scope of agreement",
        "No unconscionability (procedural and substantive)",
    ],
    primary_authority=[
        "9 U.S.C. § 1 et seq. (Federal Arbitration Act)",
        "AT&T Mobility LLC v. Concepcion, 563 U.S. 333 (2011) (class waivers enforceable)",
        "Epic Systems Corp. v. Lewis, 138 S. Ct. 1612 (2018) (employment arbitration)",
    ],
    entity_scope="adr,arbitration,contract",
    confidence="DEFENSIBLE",
    controlling_precedent="AT&T Mobility LLC v. Concepcion, 563 U.S. 333 (2011); 9 U.S.C. § 2",
    adversary_position="Arbitration agreement is unconscionable and unenforceable",
    counter_arguments=[
        "Agreement is procedurally and substantively unconscionable",
        "Agreement is in adhesion and lacks bargaining power",
        "Class waiver violates public policy",
    ],
    resolution_strategy="Establish valid arbitration agreement and enforce under FAA; class waivers generally enforceable",
    confidence_stratification="DEFENSIBLE for standard arbitration agreements; DISCLOSURE for unconscionability claims",
)


# ── ETHICS: CONFLICT OF INTEREST ──

EXTENDED_DOCTRINES["attorney_conflict_of_interest"] = ExtendedDoctrineBlock(
    topic="attorney_conflict_of_interest",
    keywords=["conflict of interest", "concurrent conflict", "former client", "imputation", "informed consent", "screening", "disqualification"],
    conclusion_template="Under ABA Model Rule 1.7, a lawyer shall not represent a client if the representation involves a concurrent conflict of interest (directly adverse to another client or materially limited by responsibilities to another client, former client, or third person). Conflicts may be waived with informed consent, confirmed in writing, if the lawyer reasonably believes they can provide competent and diligent representation. Former client conflicts (Rule 1.9) prohibit representation materially adverse to former client in same or substantially related matter. Conflicts are imputed to all lawyers in the firm unless screening is effective.",
    reasoning_framework="""1. Identify if concurrent conflict exists: directly adverse or materially limited representation.
2. Assess whether the conflict is consentable (lawyer can provide competent representation).
3. Obtain informed consent, confirmed in writing, from all affected clients.
4. Evaluate former client conflicts: is matter same or substantially related to prior representation?
5. Determine if representation is materially adverse to former client.
6. Check for imputation: does conflict extend to all lawyers in the firm?
7. Implement screening if permissible (former government lawyer, lateral hire).
8. Disqualify lawyer or firm if conflict is not waivable or consent not obtained.""",
    key_factors=[
        "Concurrent or former client conflict exists",
        "Representation is directly adverse or materially limited",
        "Conflict is not consentable or informed consent not obtained",
        "Conflict is imputed to entire firm",
    ],
    primary_authority=[
        "ABA Model Rule 1.7 (concurrent conflicts)",
        "ABA Model Rule 1.9 (former client conflicts)",
        "ABA Model Rule 1.10 (imputation)",
        "Restatement (Third) of the Law Governing Lawyers §§ 121-123 (2000)",
    ],
    entity_scope="attorney,client,ethics",
    confidence="DEFENSIBLE",
    controlling_precedent="ABA Model Rule 1.7, 1.9, 1.10",
    adversary_position="Attorney has conflict of interest and must be disqualified",
    counter_arguments=[
        "Informed consent obtained from all affected clients",
        "Conflict is not material or is waivable",
        "Screening is effective (former government lawyer)",
    ],
    resolution_strategy="Obtain informed consent, confirmed in writing, or implement screening if permissible",
    confidence_stratification="DEFENSIBLE for clear conflicts with consent; DISCLOSURE for novel conflict scenarios",
)


# ── LEGISLATIVE ANALYSIS: CHEVRON STEP ZERO ──

EXTENDED_DOCTRINES["chevron_step_zero"] = ExtendedDoctrineBlock(
    topic="chevron_step_zero",
    keywords=["chevron step zero", "jurisdiction to defer", "express delegation", "ambiguity", "agency interpretation", "mead"],
    conclusion_template="Before applying Chevron deference, courts must determine whether Congress intended to delegate interpretive authority to the agency (Chevron Step Zero). Under United States v. Mead Corp., 533 U.S. 218 (2001), Chevron applies only when: (1) Congress delegated authority to the agency to make rules carrying force of law, and (2) the agency interpretation was promulgated in the exercise of that authority (e.g., notice-and-comment rulemaking, formal adjudication). Interpretations in opinion letters, manuals, or enforcement guidelines receive only Skidmore respect, not Chevron deference.",
    reasoning_framework="""1. Determine if Congress delegated authority to the agency to make rules with force of law.
2. Assess whether the agency's interpretation was promulgated in exercise of that authority.
3. Evaluate the procedural formality: notice-and-comment rulemaking or formal adjudication (Chevron applies); opinion letters or manuals (Skidmore respect).
4. Check for express delegation of interpretive authority in the statute.
5. Consider whether the interpretation has the force of law (binding on parties).
6. Apply Chevron if Step Zero is satisfied; otherwise apply Skidmore respect.
7. Distinguish between formal agency action (Chevron) and informal guidance (Skidmore).
8. Proceed to Chevron steps one and two only if Step Zero is satisfied.""",
    key_factors=[
        "Congress delegated interpretive authority to the agency",
        "Interpretation promulgated through formal process (notice-and-comment, adjudication)",
        "Interpretation has force of law",
    ],
    primary_authority=[
        "United States v. Mead Corp., 533 U.S. 218 (2001) (Chevron Step Zero)",
        "Christensen v. Harris County, 529 U.S. 576 (2000) (opinion letters not Chevron-eligible)",
        "Skidmore v. Swift & Co., 323 U.S. 134 (1944) (respect for agency interpretations)",
    ],
    entity_scope="administrative_law,agency,regulatory",
    confidence="DEFENSIBLE",
    controlling_precedent="United States v. Mead Corp., 533 U.S. 218 (2001)",
    adversary_position="Chevron does not apply because no express delegation exists",
    counter_arguments=[
        "Agency interpretation was promulgated through notice-and-comment rulemaking",
        "Statute expressly delegates interpretive authority",
        "Interpretation has force of law",
    ],
    resolution_strategy="Establish that interpretation was promulgated through formal process and has force of law",
    confidence_stratification="DEFENSIBLE for notice-and-comment rules; DISCLOSURE for informal guidance",
)


logger.info(f"Extended doctrines loaded: {len(EXTENDED_DOCTRINES)} topics")
