from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from pathlib import Path

class ConfidenceZone(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    UNCERTAIN = "Uncertain"

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
        topic="Topic Definition",
        keywords=["topic", "definition", "scope"],
        conclusion_template="The topic is defined as: {definition}.",
        reasoning_framework=(
            "1. Identify the core subject matter and its boundaries.\n"
            "2. Review authoritative sources for definitions.\n"
            "3. Compare with similar topics to ensure clarity.\n"
            "4. Consider the historical evolution of the topic.\n"
            "5. Synthesize a concise, operational definition.\n"
            "6. Validate with domain experts.\n"
            "7. Document any ambiguities or contested aspects.\n"
            "8. Reference primary statutes or standards.\n"
            "9. Ensure the definition aligns with the engine's operational scope.\n"
            "10. Update as necessary based on new precedents or authorities."
        ),
        key_factors=[
            "Clarity of boundaries",
            "Authoritative definitions",
            "Historical context",
            "Operational relevance"
        ],
        primary_authority=[
            "Oxford English Dictionary",
            "Relevant Statutes",
            "Domain-specific Standards"
        ],
        burden_holder="Proponent",
        adversary_position="The topic is broader or narrower than defined.",
        counter_arguments=[
            "Alternative definitions exist in other domains.",
            "Scope creep concerns.",
            "Ambiguity in statutory language."
        ],
        resolution_strategy="Rely on the most authoritative and widely accepted definition, with explicit notation of any deviations.",
        entity_scope="All entities subject to the engine's domain.",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OED, Black's Law Dictionary"
    ),
    DoctrineBlock(
        topic="Topic Relevance",
        keywords=["topic", "relevance", "materiality"],
        conclusion_template="The topic is relevant to the proceeding because: {reason}.",
        reasoning_framework=(
            "1. Assess the direct connection between the topic and the issue at hand.\n"
            "2. Determine if the topic materially affects the outcome.\n"
            "3. Examine prior cases where similar topics were deemed relevant.\n"
            "4. Consider statutory or regulatory mandates regarding relevance.\n"
            "5. Evaluate the probative value versus prejudicial effect.\n"
            "6. Document the rationale for inclusion or exclusion.\n"
            "7. Reference controlling authority on relevance standards.\n"
            "8. Update relevance assessment as new facts emerge."
        ),
        key_factors=[
            "Material impact on outcome",
            "Statutory mandates",
            "Precedent on relevance"
        ],
        primary_authority=[
            "Federal Rules of Evidence 401",
            "Leading Case Law"
        ],
        burden_holder="Proponent",
        adversary_position="The topic is not material to the current issue.",
        counter_arguments=[
            "Topic is tangential or cumulative.",
            "Potential for confusion or prejudice."
        ],
        resolution_strategy="Apply the materiality standard as articulated in FRE 401 and controlling precedent.",
        entity_scope="All proceedings under engine jurisdiction.",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Daubert v. Merrell Dow Pharmaceuticals"
    ),
    DoctrineBlock(
        topic="Topic Admissibility",
        keywords=["topic", "admissibility", "exclusion"],
        conclusion_template="The topic is admissible because: {justification}.",
        reasoning_framework=(
            "1. Identify the legal standard for admissibility.\n"
            "2. Analyze whether the topic meets threshold requirements.\n"
            "3. Consider exclusionary rules (e.g., hearsay, privilege).\n"
            "4. Weigh probative value against potential prejudice.\n"
            "5. Reference relevant statutes and case law.\n"
            "6. Document the chain of custody or authentication if applicable.\n"
            "7. Address any objections raised by the adversary.\n"
            "8. Conclude with a clear admissibility determination."
        ),
        key_factors=[
            "Legal standard for admissibility",
            "Exclusionary rules",
            "Probative value"
        ],
        primary_authority=[
            "Federal Rules of Evidence 402, 403",
            "Controlling Case Law"
        ],
        burden_holder="Proponent",
        adversary_position="The topic is inadmissible under exclusionary rules.",
        counter_arguments=[
            "Lack of authentication.",
            "Hearsay concerns.",
            "Prejudicial impact outweighs probative value."
        ],
        resolution_strategy="Follow the balancing test under FRE 403 and apply relevant precedent.",
        entity_scope="Judicial and quasi-judicial proceedings.",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Huddleston v. United States"
    ),
    DoctrineBlock(
        topic="Topic Materiality",
        keywords=["topic", "materiality", "significance"],
        conclusion_template="The topic is material because: {analysis}.",
        reasoning_framework=(
            "1. Define materiality in the context of the proceeding.\n"
            "2. Identify the elements of the claim or defense affected by the topic.\n"
            "3. Determine if the topic could affect the outcome.\n"
            "4. Review statutory and case law definitions of materiality.\n"
            "5. Consider the adversary's position on materiality.\n"
            "6. Document the analysis and conclusion."
        ),
        key_factors=[
            "Effect on claim or defense",
            "Statutory definitions",
            "Case law interpretations"
        ],
        primary_authority=[
            "Federal Rules of Civil Procedure 26(b)(1)",
            "Relevant Case Law"
        ],
        burden_holder="Proponent",
        adversary_position="The topic is not material to any claim or defense.",
        counter_arguments=[
            "No impact on outcome.",
            "Topic is collateral or cumulative."
        ],
        resolution_strategy="Apply the materiality standard from FRCP 26(b)(1) and relevant precedent.",
        entity_scope="Civil litigation under engine jurisdiction.",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TSC Industries, Inc. v. Northway, Inc."
    ),
    DoctrineBlock(
        topic="Topic Privilege",
        keywords=["topic", "privilege", "confidentiality"],
        conclusion_template="The topic is privileged and not subject to disclosure because: {basis}.",
        reasoning_framework=(
            "1. Identify the type of privilege asserted (e.g., attorney-client, work product).\n"
            "2. Determine if the communication meets the elements of the privilege.\n"
            "3. Review any waiver or exceptions to privilege.\n"
            "4. Reference statutory and case law authority.\n"
            "5. Consider the adversary's arguments for disclosure.\n"
            "6. Document the privilege analysis and conclusion."
        ),
        key_factors=[
            "Type of privilege",
            "Elements of privilege",
            "Waiver or exceptions"
        ],
        primary_authority=[
            "Federal Rules of Evidence 501",
            "Upjohn Co. v. United States"
        ],
        burden_holder="Party asserting privilege",
        adversary_position="Privilege does not apply or has been waived.",
        counter_arguments=[
            "Privilege was waived.",
            "Communication was not confidential.",
            "Crime-fraud exception applies."
        ],
        resolution_strategy="Apply the privilege doctrine as articulated in Upjohn and FRE 501.",
        entity_scope="All parties asserting privilege.",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Upjohn Co. v. United States"
    ),
    DoctrineBlock(
        topic="Topic Authentication",
        keywords=["topic", "authentication", "evidence"],
        conclusion_template="The topic is authenticated by: {method}.",
        reasoning_framework=(
            "1. Identify the evidence requiring authentication.\n"
            "2. Determine the standard for authentication under applicable rules.\n"
            "3. Review methods for authentication (e.g., witness testimony, chain of custody).\n"
            "4. Reference statutory and case law authority.\n"
            "5. Consider objections to authenticity.\n"
            "6. Document the authentication process and conclusion."
        ),
        key_factors=[
            "Standard for authentication",
            "Method used",
            "Objections to authenticity"
        ],
        primary_authority=[
            "Federal Rules of Evidence 901",
            "Case Law on Authentication"
        ],
        burden_holder="Proponent",
        adversary_position="Evidence is not authentic.",
        counter_arguments=[
            "Break in chain of custody.",
            "Forgery or alteration.",
            "Insufficient foundation."
        ],
        resolution_strategy="Follow FRE 901 and controlling precedent on authentication.",
        entity_scope="All evidentiary submissions.",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Tropeano"
    ),
    DoctrineBlock(
        topic="Topic Hearsay",
        keywords=["topic", "hearsay", "out-of-court statement"],
        conclusion_template="The topic is hearsay and inadmissible unless an exception applies.",
        reasoning_framework=(
            "1. Define hearsay under the applicable rules.\n"
            "2. Determine if the statement is offered for the truth of the matter asserted.\n"
            "3. Review exceptions and exclusions to the hearsay rule.\n"
            "4. Reference statutory and case law authority.\n"
            "5. Consider the adversary's arguments for admissibility.\n"
            "6. Document the analysis and conclusion."
        ),
        key_factors=[
            "Definition of hearsay",
            "Purpose of statement",
            "Exceptions or exclusions"
        ],
        primary_authority=[
            "Federal Rules of Evidence 801-803",
            "Relevant Case Law"
        ],
        burden_holder="Proponent seeking admission",
        adversary_position="Statement is inadmissible hearsay.",
        counter_arguments=[
            "Statement falls within an exception.",
            "Statement is not offered for the truth.",
            "Statement is a party admission."
        ],
        resolution_strategy="Apply the hearsay rule and exceptions as articulated in FRE 801-803.",
        entity_scope="All evidentiary matters.",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Crawford v. Washington"
    ),
    DoctrineBlock(
        topic="Topic Judicial Notice",
        keywords=["topic", "judicial notice", "fact"],
        conclusion_template="The topic is subject to judicial notice because: {reason}.",
        reasoning_framework=(
            "1. Define judicial notice under the applicable rules.\n"
            "2. Determine if the fact is generally known or capable of accurate determination.\n"
            "3. Reference statutory and case law authority.\n"
            "4. Consider the adversary's objections.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "General knowledge",
            "Capability of accurate determination",
            "Legal standards"
        ],
        primary_authority=[
            "Federal Rules of Evidence 201",
            "Case Law on Judicial Notice"
        ],
        burden_holder="Proponent",
        adversary_position="Fact is not appropriate for judicial notice.",
        counter_arguments=[
            "Fact is subject to reasonable dispute.",
            "Not generally known.",
            "Requires expert testimony."
        ],
        resolution_strategy="Apply FRE 201 and controlling precedent.",
        entity_scope="All proceedings.",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Bello"
    ),
    DoctrineBlock(
        topic="Topic Preclusion",
        keywords=["topic", "preclusion", "res judicata", "collateral estoppel"],
        conclusion_template="The topic is precluded by prior adjudication because: {analysis}.",
        reasoning_framework=(
            "1. Identify the type of preclusion (claim or issue).\n"
            "2. Determine if the elements of preclusion are met.\n"
            "3. Reference statutory and case law authority.\n"
            "4. Consider exceptions or limitations to preclusion.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Prior adjudication",
            "Identity of parties and issues",
            "Final judgment"
        ],
        primary_authority=[
            "Restatement (Second) of Judgments",
            "Case Law on Preclusion"
        ],
        burden_holder="Party asserting preclusion",
        adversary_position="Preclusion does not apply.",
        counter_arguments=[
            "Different parties or issues.",
            "No final judgment.",
            "Exception applies."
        ],
        resolution_strategy="Apply the Restatement and controlling precedent.",
        entity_scope="All adjudicative proceedings.",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Parklane Hosiery Co. v. Shore"
    ),
    DoctrineBlock(
        topic="Topic Standing",
        keywords=["topic", "standing", "justiciability"],
        conclusion_template="The party has standing because: {basis}.",
        reasoning_framework=(
            "1. Define standing under constitutional and statutory law.\n"
            "2. Identify the injury, causation, and redressability elements.\n"
            "3. Reference statutory and case law authority.\n"
            "4. Consider prudential limitations.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Injury in fact",
            "Causation",
            "Redressability"
        ],
        primary_authority=[
            "Lujan v. Defenders of Wildlife",
            "Relevant Statutes"
        ],
        burden_holder="Party asserting standing",
        adversary_position="No injury, causation, or redressability.",
        counter_arguments=[
            "No concrete injury.",
            "Speculative harm.",
            "No causal connection."
        ],
        resolution_strategy="Apply the Lujan standard and relevant statutes.",
        entity_scope="All parties seeking relief.",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Lujan v. Defenders of Wildlife"
    ),
    DoctrineBlock(
        topic="Topic Mootness",
        keywords=["topic", "mootness", "justiciability"],
        conclusion_template="The topic is moot because: {reason}.",
        reasoning_framework=(
            "1. Define mootness under constitutional law.\n"
            "2. Determine if there remains a live controversy.\n"
            "3. Reference statutory and case law authority.\n"
            "4. Consider exceptions to mootness (e.g., capable of repetition yet evading review).\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Live controversy",
            "Exceptions to mootness",
            "Judicial economy"
        ],
        primary_authority=[
            "DeFunis v. Odegaard",
            "Relevant Case Law"
        ],
        burden_holder="Party asserting mootness",
        adversary_position="Controversy remains live.",
        counter_arguments=[
            "Exception applies.",
            "Collateral consequences.",
            "Capable of repetition."
        ],
        resolution_strategy="Apply mootness doctrine and controlling precedent.",
        entity_scope="All justiciable controversies.",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="DeFunis v. Odegaard"
    ),
    DoctrineBlock(
        topic="Topic Ripeness",
        keywords=["topic", "ripeness", "justiciability"],
        conclusion_template="The topic is ripe for adjudication because: {analysis}.",
        reasoning_framework=(
            "1. Define ripeness under constitutional and statutory law.\n"
            "2. Assess whether the controversy is fit for judicial resolution.\n"
            "3. Reference statutory and case law authority.\n"
            "4. Consider hardship to parties of withholding review.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Fitness for judicial resolution",
            "Hardship to parties",
            "Factual development"
        ],
        primary_authority=[
            "Abbott Laboratories v. Gardner",
            "Relevant Statutes"
        ],
        burden_holder="Party asserting ripeness",
        adversary_position="Controversy is not ripe.",
        counter_arguments=[
            "Factual record is incomplete.",
            "No immediate hardship.",
            "Speculative dispute."
        ],
        resolution_strategy="Apply the Abbott Laboratories standard.",
        entity_scope="All parties seeking adjudication.",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Abbott Laboratories v. Gardner"
    ),
    DoctrineBlock(
        topic="Topic Jurisdiction",
        keywords=["topic", "jurisdiction", "authority"],
        conclusion_template="The tribunal has jurisdiction because: {basis}.",
        reasoning_framework=(
            "1. Identify the source of jurisdiction (statutory, constitutional).\n"
            "2. Determine if the parties and subject matter fall within the scope.\n"
            "3. Reference statutory and case law authority.\n"
            "4. Consider any jurisdictional objections.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Source of jurisdiction",
            "Subject matter",
            "Personal jurisdiction"
        ],
        primary_authority=[
            "28 U.S.C. § 1331",
            "Relevant Case Law"
        ],
        burden_holder="Party asserting jurisdiction",
        adversary_position="Tribunal lacks jurisdiction.",
        counter_arguments=[
            "No statutory basis.",
            "Lack of personal jurisdiction.",
            "Improper venue."
        ],
        resolution_strategy="Apply jurisdictional statutes and controlling precedent.",
        entity_scope="All tribunals under engine domain.",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Steel Co. v. Citizens for a Better Environment"
    ),
    DoctrineBlock(
        topic="Topic Venue",
        keywords=["topic", "venue", "location"],
        conclusion_template="Venue is proper because: {analysis}.",
        reasoning_framework=(
            "1. Identify the statutory provisions governing venue.\n"
            "2. Determine if the action was filed in the correct location.\n"
            "3. Reference statutory and case law authority.\n"
            "4. Consider any motions to transfer or dismiss for improper venue.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Statutory venue provisions",
            "Location of parties and events",
            "Convenience of parties"
        ],
        primary_authority=[
            "28 U.S.C. § 1391",
            "Relevant Case Law"
        ],
        burden_holder="Party asserting venue",
        adversary_position="Venue is improper.",
        counter_arguments=[
            "Improper location.",
            "Forum non conveniens.",
            "Agreement to different venue."
        ],
        resolution_strategy="Apply statutory venue rules and controlling precedent.",
        entity_scope="All civil actions.",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Atlantic Marine Construction Co. v. United States District Court"
    ),
    DoctrineBlock(
        topic="Topic Statute of Limitations",
        keywords=["topic", "statute of limitations", "timeliness"],
        conclusion_template="The claim is timely because: {analysis}.",
        reasoning_framework=(
            "1. Identify the applicable statute of limitations.\n"
            "2. Determine the accrual date of the claim.\n"
            "3. Reference statutory and case law authority.\n"
            "4. Consider tolling doctrines or exceptions.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Applicable limitations period",
            "Date of accrual",
            "Tolling or exceptions"
        ],
        primary_authority=[
            "28 U.S.C. § 1658",
            "Relevant Case Law"
        ],
        burden_holder="Party asserting timeliness",
        adversary_position="Claim is time-barred.",
        counter_arguments=[
            "Limitations period expired.",
            "No tolling applies.",
            "Delayed discovery not justified."
        ],
        resolution_strategy="Apply statutory limitations period and controlling precedent.",
        entity_scope="All claims subject to limitations.",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Rotkiske v. Klemm"
    ),
    DoctrineBlock(
        topic="Topic Estoppel",
        keywords=["topic", "estoppel", "preclusion"],
        conclusion_template="The party is estopped from asserting the topic because: {basis}.",
        reasoning_framework=(
            "1. Identify the type of estoppel (equitable, collateral, judicial).\n"
            "2. Determine if the elements of estoppel are met.\n"
            "3. Reference statutory and case law authority.\n"
            "4. Consider exceptions or limitations.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Prior conduct or representation",
            "Reliance by adversary",
            "Detriment to adversary"
        ],
        primary_authority=[
            "Restatement (Second) of Judgments",
            "Case Law on Estoppel"
        ],
        burden_holder="Party asserting estoppel",
        adversary_position="Elements of estoppel not met.",
        counter_arguments=[
            "No reliance.",
            "No detriment.",
            "Change in law or facts."
        ],
        resolution_strategy="Apply the Restatement and controlling precedent.",
        entity_scope="All parties to prior proceedings.",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Heckler v. Community Health Services"
    ),
    DoctrineBlock(
        topic="Topic Laches",
        keywords=["topic", "laches", "delay"],
        conclusion_template="The doctrine of laches bars the claim because: {analysis}.",
        reasoning_framework=(
            "1. Define laches and its elements.\n"
            "2. Determine if there was unreasonable delay in asserting the claim.\n"
            "3. Assess prejudice to the adversary.\n"
            "4. Reference statutory and case law authority.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Unreasonable delay",
            "Prejudice to adversary",
            "Knowledge of claim"
        ],
        primary_authority=[
            "Petrella v. Metro-Goldwyn-Mayer, Inc.",
            "Relevant Case Law"
        ],
        burden_holder="Party asserting laches",
        adversary_position="Delay was reasonable or no prejudice.",
        counter_arguments=[
            "Delay justified.",
            "No prejudice.",
            "Statute of limitations governs."
        ],
        resolution_strategy="Apply laches doctrine and controlling precedent.",
        entity_scope="All equitable claims.",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Petrella v. Metro-Goldwyn-Mayer, Inc."
    ),
    DoctrineBlock(
        topic="Topic Waiver",
        keywords=["topic", "waiver", "forfeiture"],
        conclusion_template="The party has waived the topic because: {basis}.",
        reasoning_framework=(
            "1. Define waiver and its elements.\n"
            "2. Determine if the party intentionally relinquished a known right.\n"
            "3. Reference statutory and case law authority.\n"
            "4. Consider exceptions or limitations.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Knowledge of right",
            "Intentional relinquishment",
            "Conduct indicating waiver"
        ],
        primary_authority=[
            "Johnson v. Zerbst",
            "Relevant Case Law"
        ],
        burden_holder="Party asserting waiver",
        adversary_position="No intentional relinquishment.",
        counter_arguments=[
            "No knowledge of right.",
            "No intent to waive.",
            "Waiver not voluntary."
        ],
        resolution_strategy="Apply waiver doctrine and controlling precedent.",
        entity_scope="All parties to proceedings.",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Johnson v. Zerbst"
    ),
    DoctrineBlock(
        topic="Topic Severability",
        keywords=["topic", "severability", "contract"],
        conclusion_template="The severability clause applies because: {analysis}.",
        reasoning_framework=(
            "1. Identify the severability clause in the contract or statute.\n"
            "2. Determine if the invalid provision can be severed without affecting the remainder.\n"
            "3. Reference statutory and case law authority.\n"
            "4. Consider the parties' intent.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Existence of severability clause",
            "Effect on remainder",
            "Parties' intent"
        ],
        primary_authority=[
            "Restatement (Second) of Contracts § 184",
            "Case Law on Severability"
        ],
        burden_holder="Party seeking severance",
        adversary_position="Provision is not severable.",
        counter_arguments=[
            "Provision is integral to contract.",
            "No severability clause.",
            "Severance alters parties' bargain."
        ],
        resolution_strategy="Apply Restatement and controlling precedent.",
        entity_scope="All contractual and statutory provisions.",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Buckley v. Valeo"
    ),
    DoctrineBlock(
        topic="Topic Interpretation",
        keywords=["topic", "interpretation", "construction"],
        conclusion_template="The topic is interpreted as: {interpretation}.",
        reasoning_framework=(
            "1. Identify the text to be interpreted.\n"
            "2. Apply the plain meaning rule.\n"
            "3. Consider extrinsic evidence if ambiguity exists.\n"
            "4. Reference statutory and case law authority.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Plain meaning",
            "Context",
            "Extrinsic evidence"
        ],
        primary_authority=[
            "Chevron U.S.A., Inc. v. Natural Resources Defense Council, Inc.",
            "Relevant Statutes"
        ],
        burden_holder="Party proposing interpretation",
        adversary_position="Alternative interpretation controls.",
        counter_arguments=[
            "Plain meaning is clear.",
            "Legislative intent differs.",
            "Ambiguity resolved by precedent."
        ],
        resolution_strategy="Apply plain meaning and controlling precedent.",
        entity_scope="All statutes and contracts.",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Chevron U.S.A., Inc. v. NRDC"
    ),
    DoctrineBlock(
        topic="Topic Preemption",
        keywords=["topic", "preemption", "federal law"],
        conclusion_template="Federal law preempts state law because: {analysis}.",
        reasoning_framework=(
            "1. Identify the federal and state laws at issue.\n"
            "2. Determine if express, implied, or conflict preemption applies.\n"
            "3. Reference statutory and case law authority.\n"
            "4. Consider the presumption against preemption.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Express or implied preemption",
            "Conflict between laws",
            "Congressional intent"
        ],
        primary_authority=[
            "Supremacy Clause, U.S. Const. art. VI, cl. 2",
            "Relevant Case Law"
        ],
        burden_holder="Party asserting preemption",
        adversary_position="State law is not preempted.",
        counter_arguments=[
            "No conflict exists.",
            "Congress did not intend preemption.",
            "State law complements federal law."
        ],
        resolution_strategy="Apply Supremacy Clause and controlling precedent.",
        entity_scope="Federal and state law conflicts.",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Arizona v. United States"
    ),
    DoctrineBlock(
        topic="Topic Supremacy",
        keywords=["topic", "supremacy", "federal law"],
        conclusion_template="Federal law is supreme over conflicting state law.",
        reasoning_framework=(
            "1. Reference the Supremacy Clause of the U.S. Constitution.\n"
            "2. Identify the federal and state laws in conflict.\n"
            "3. Determine if the federal law is valid and applicable.\n"
            "4. Reference statutory and case law authority.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Supremacy Clause",
            "Conflict between laws",
            "Validity of federal law"
        ],
        primary_authority=[
            "U.S. Const. art. VI, cl. 2",
            "Relevant Case Law"
        ],
        burden_holder="Party asserting supremacy",
        adversary_position="No conflict or federal law invalid.",
        counter_arguments=[
            "No actual conflict.",
            "Federal law exceeds authority.",
            "State law operates independently."
        ],
        resolution_strategy="Apply Supremacy Clause and controlling precedent.",
        entity_scope="Federal and state law conflicts.",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="McCulloch v. Maryland"
    ),
    DoctrineBlock(
        topic="Topic Severance",
        keywords=["topic", "severance", "joinder"],
        conclusion_template="Severance is appropriate because: {analysis}.",
        reasoning_framework=(
            "1. Identify the parties or claims subject to severance.\n"
            "2. Determine if joinder would prejudice any party.\n"
            "3. Reference statutory and case law authority.\n"
            "4. Consider judicial economy and fairness.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Prejudice to parties",
            "Judicial economy",
            "Fairness"
        ],
        primary_authority=[
            "Federal Rules of Civil Procedure 21",
            "Relevant Case Law"
        ],
        burden_holder="Party seeking severance",
        adversary_position="Severance is not justified.",
        counter_arguments=[
            "No prejudice.",
            "Joinder promotes efficiency.",
            "Claims are related."
        ],
        resolution_strategy="Apply FRCP 21 and controlling precedent.",
        entity_scope="All civil actions.",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Mosley v. General Motors Corp."
    ),
    DoctrineBlock(
        topic="Topic Consolidation",
        keywords=["topic", "consolidation", "joinder"],
        conclusion_template="Consolidation is appropriate because: {analysis}.",
        reasoning_framework=(
            "1. Identify the actions or claims to be consolidated.\n"
            "2. Determine if consolidation promotes efficiency and avoids inconsistent results.\n"
            "3. Reference statutory and case law authority.\n"
            "4. Consider prejudice to any party.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Efficiency",
            "Avoidance of inconsistent results",
            "Prejudice to parties"
        ],
        primary_authority=[
            "Federal Rules of Civil Procedure 42(a)",
            "Relevant Case Law"
        ],
        burden_holder="Party seeking consolidation",
        adversary_position="Consolidation is prejudicial.",
        counter_arguments=[
            "Claims are unrelated.",
            "Prejudice outweighs efficiency.",
            "Separate trials are preferable."
        ],
        resolution_strategy="Apply FRCP 42(a) and controlling precedent.",
        entity_scope="All civil actions.",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Johnson v. Manhattan Ry. Co."
    ),
    DoctrineBlock(
        topic="Topic Discovery",
        keywords=["topic", "discovery", "evidence"],
        conclusion_template="Discovery of the topic is permitted because: {analysis}.",
        reasoning_framework=(
            "1. Identify the scope of permissible discovery.\n"
            "2. Determine if the topic is relevant and proportional to the needs of the case.\n"
            "3. Reference statutory and case law authority.\n"
            "4. Consider objections and protective orders.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Relevance",
            "Proportionality",
            "Objections"
        ],
        primary_authority=[
            "Federal Rules of Civil Procedure 26(b)(1)",
            "Relevant Case Law"
        ],
        burden_holder="Party seeking discovery",
        adversary_position="Discovery is not permitted.",
        counter_arguments=[
            "Undue burden.",
            "Irrelevant information.",
            "Privilege applies."
        ],
        resolution_strategy="Apply FRCP 26(b)(1) and controlling precedent.",
        entity_scope="All civil actions.",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Oppenheimer Fund, Inc. v. Sanders"
    ),
    DoctrineBlock(
        topic="Topic Protective Order",
        keywords=["topic", "protective order", "discovery"],
        conclusion_template="A protective order is warranted because: {basis}.",
        reasoning_framework=(
            "1. Identify the grounds for a protective order.\n"
            "2. Determine if disclosure would cause annoyance, embarrassment, oppression, or undue burden.\n"
            "3. Reference statutory and case law authority.\n"
            "4. Consider less restrictive alternatives.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Grounds for protection",
            "Potential harm",
            "Alternatives"
        ],
        primary_authority=[
            "Federal Rules of Civil Procedure 26(c)",
            "Relevant Case Law"
        ],
        burden_holder="Party seeking protection",
        adversary_position="Protective order is unnecessary.",
        counter_arguments=[
            "No harm shown.",
            "Information is public.",
            "Order is overbroad."
        ],
        resolution_strategy="Apply FRCP 26(c) and controlling precedent.",
        entity_scope="All discovery matters.",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Seattle Times Co. v. Rhinehart"
    ),
    DoctrineBlock(
        topic="Topic Summary Judgment",
        keywords=["topic", "summary judgment", "disposition"],
        conclusion_template="Summary judgment is appropriate because: {analysis}.",
        reasoning_framework=(
            "1. Identify the standard for summary judgment.\n"
            "2. Determine if there is a genuine dispute of material fact.\n"
            "3. Reference statutory and case law authority.\n"
            "4. Consider the evidence in the light most favorable to the non-movant.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Genuine dispute",
            "Material fact",
            "Standard of review"
        ],
        primary_authority=[
            "Federal Rules of Civil Procedure 56",
            "Relevant Case Law"
        ],
        burden_holder="Party seeking summary judgment",
        adversary_position="Genuine dispute exists.",
        counter_arguments=[
            "Material facts are disputed.",
            "Credibility issues.",
            "Further discovery needed."
        ],
        resolution_strategy="Apply FRCP 56 and controlling precedent.",
        entity_scope="All civil actions.",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Celotex Corp. v. Catrett"
    ),
    DoctrineBlock(
        topic="Topic Dismissal",
        keywords=["topic", "dismissal", "pleading"],
        conclusion_template="Dismissal is appropriate because: {analysis}.",
        reasoning_framework=(
            "1. Identify the grounds for dismissal (e.g., failure to state a claim).\n"
            "2. Reference statutory and case law authority.\n"
            "3. Consider whether amendment would cure the defect.\n"
            "4. Document the analysis and conclusion."
        ),
        key_factors=[
            "Grounds for dismissal",
            "Opportunity to amend",
            "Legal sufficiency"
        ],
        primary_authority=[
            "Federal Rules of Civil Procedure 12(b)(6)",
            "Relevant Case Law"
        ],
        burden_holder="Party seeking dismissal",
        adversary_position="Claim is legally sufficient.",
        counter_arguments=[
            "Facts support claim.",
            "Amendment is possible.",
            "Dismissal is premature."
        ],
        resolution_strategy="Apply FRCP 12(b)(6) and controlling precedent.",
        entity_scope="All civil actions.",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Ashcroft v. Iqbal"
    ),
    DoctrineBlock(
        topic="Topic Default Judgment",
        keywords=["topic", "default judgment", "failure to appear"],
        conclusion_template="Default judgment is appropriate because: {basis}.",
        reasoning_framework=(
            "1. Identify the grounds for default judgment.\n"
            "2. Reference statutory and case law authority.\n"
            "3. Consider whether the defaulting party was properly served.\n"
            "4. Assess the sufficiency of the claim.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Failure to appear",
            "Proper service",
            "Sufficiency of claim"
        ],
        primary_authority=[
            "Federal Rules of Civil Procedure 55",
            "Relevant Case Law"
        ],
        burden_holder="Party seeking default judgment",
        adversary_position="Default is not justified.",
        counter_arguments=[
            "Improper service.",
            "Excusable neglect.",
            "Insufficient claim."
        ],
        resolution_strategy="Apply FRCP 55 and controlling precedent.",
        entity_scope="All civil actions.",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. $55,518.05 in U.S. Currency"
    ),
    DoctrineBlock(
        topic="Topic Remand",
        keywords=["topic", "remand", "jurisdiction"],
        conclusion_template="Remand is appropriate because: {analysis}.",
        reasoning_framework=(
            "1. Identify the grounds for remand.\n"
            "2. Reference statutory and case law authority.\n"
            "3. Determine if the court lacks subject matter jurisdiction.\n"
            "4. Consider procedural defects.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Jurisdictional defects",
            "Procedural defects",
            "Statutory authority"
        ],
        primary_authority=[
            "28 U.S.C. § 1447",
            "Relevant Case Law"
        ],
        burden_holder="Party seeking remand",
        adversary_position="Removal was proper.",
        counter_arguments=[
            "Jurisdiction exists.",
            "No procedural defect.",
            "Timely removal."
        ],
        resolution_strategy="Apply 28 U.S.C. § 1447 and controlling precedent.",
        entity_scope="All removed actions.",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Caterpillar Inc. v. Lewis"
    ),
    DoctrineBlock(
        topic="Topic Removal",
        keywords=["topic", "removal", "jurisdiction"],
        conclusion_template="Removal is appropriate because: {basis}.",
        reasoning_framework=(
            "1. Identify the statutory grounds for removal.\n"
            "2. Reference statutory and case law authority.\n"
            "3. Determine if the action could have been brought in federal court.\n"
            "4. Consider timeliness and procedural requirements.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Statutory grounds",
            "Federal jurisdiction",
            "Timeliness"
        ],
        primary_authority=[
            "28 U.S.C. § 1441",
            "Relevant Case Law"
        ],
        burden_holder="Party seeking removal",
        adversary_position="Removal is improper.",
        counter_arguments=[
            "No federal jurisdiction.",
            "Untimely removal.",
            "Procedural defect."
        ],
        resolution_strategy="Apply 28 U.S.C. § 1441 and controlling precedent.",
        entity_scope="All civil actions.",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Lincoln Property Co. v. Roche"
    ),
    DoctrineBlock(
        topic="Topic Injunction",
        keywords=["topic", "injunction", "equitable relief"],
        conclusion_template="An injunction is warranted because: {analysis}.",
        reasoning_framework=(
            "1. Identify the elements for injunctive relief.\n"
            "2. Reference statutory and case law authority.\n"
            "3. Assess irreparable harm, likelihood of success, balance of equities, and public interest.\n"
            "4. Document the analysis and conclusion."
        ),
        key_factors=[
            "Irreparable harm",
            "Likelihood of success",
            "Balance of equities",
            "Public interest"
        ],
        primary_authority=[
            "Winter v. Natural Resources Defense Council, Inc.",
            "Relevant Statutes"
        ],
        burden_holder="Party seeking injunction",
        adversary_position="Injunction is not warranted.",
        counter_arguments=[
            "No irreparable harm.",
            "Success on merits unlikely.",
            "Harm to public interest."
        ],
        resolution_strategy="Apply Winter standard and controlling precedent.",
        entity_scope="All equitable actions.",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Winter v. NRDC"
    ),
    DoctrineBlock(
        topic="Topic Contempt",
        keywords=["topic", "contempt", "sanctions"],
        conclusion_template="Contempt is appropriate because: {basis}.",
        reasoning_framework=(
            "1. Identify the order or obligation violated.\n"
            "2. Reference statutory and case law authority.\n"
            "3. Determine if the violation was willful.\n"
            "4. Consider defenses or justifications.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Existence of order",
            "Willful violation",
            "Defenses"
        ],
        primary_authority=[
            "18 U.S.C. § 401",
            "Relevant Case Law"
        ],
        burden_holder="Party seeking contempt",
        adversary_position="No willful violation.",
        counter_arguments=[
            "Order was ambiguous.",
            "Good faith compliance.",
            "No notice of obligation."
        ],
        resolution_strategy="Apply statutory authority and controlling precedent.",
        entity_scope="All parties subject to court orders.",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="International Union, UMWA v. Bagwell"
    ),
    DoctrineBlock(
        topic="Topic Sanctions",
        keywords=["topic", "sanctions", "misconduct"],
        conclusion_template="Sanctions are appropriate because: {analysis}.",
        reasoning_framework=(
            "1. Identify the misconduct warranting sanctions.\n"
            "2. Reference statutory and case law authority.\n"
            "3. Determine the appropriate type and amount of sanction.\n"
            "4. Consider due process and proportionality.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Nature of misconduct",
            "Authority for sanctions",
            "Proportionality"
        ],
        primary_authority=[
            "Federal Rules of Civil Procedure 11",
            "Relevant Case Law"
        ],
        burden_holder="Party seeking sanctions",
        adversary_position="Sanctions are not warranted.",
        counter_arguments=[
            "No misconduct.",
            "Sanction is excessive.",
            "Due process violation."
        ],
        resolution_strategy="Apply FRCP 11 and controlling precedent.",
        entity_scope="All civil actions.",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Chambers v. NASCO, Inc."
    ),
    DoctrineBlock(
        topic="Topic Appeal",
        keywords=["topic", "appeal", "review"],
        conclusion_template="Appeal is appropriate because: {basis}.",
        reasoning_framework=(
            "1. Identify the grounds for appeal.\n"
            "2. Reference statutory and case law authority.\n"
            "3. Determine if the order is final or appealable.\n"
            "4. Consider timeliness and procedural requirements.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Grounds for appeal",
            "Finality of order",
            "Timeliness"
        ],
        primary_authority=[
            "28 U.S.C. § 1291",
            "Relevant Case Law"
        ],
        burden_holder="Party seeking appeal",
        adversary_position="Appeal is improper.",
        counter_arguments=[
            "Order is not final.",
            "Untimely appeal.",
            "No appealable issue."
        ],
        resolution_strategy="Apply statutory authority and controlling precedent.",
        entity_scope="All civil actions.",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Cohen v. Beneficial Industrial Loan Corp."
    ),
    DoctrineBlock(
        topic="Topic Mandamus",
        keywords=["topic", "mandamus", "extraordinary relief"],
        conclusion_template="Mandamus is warranted because: {analysis}.",
        reasoning_framework=(
            "1. Identify the legal duty to be enforced.\n"
            "2. Reference statutory and case law authority.\n"
            "3. Determine if there is no other adequate remedy.\n"
            "4. Assess whether the right to relief is clear and indisputable.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Legal duty",
            "No adequate remedy",
            "Clear right to relief"
        ],
        primary_authority=[
            "28 U.S.C. § 1651",
            "Relevant Case Law"
        ],
        burden_holder="Party seeking mandamus",
        adversary_position="Mandamus is not warranted.",
        counter_arguments=[
            "Adequate remedy exists.",
            "Right to relief is not clear.",
            "Discretionary act."
        ],
        resolution_strategy="Apply statutory authority and controlling precedent.",
        entity_scope="All extraordinary writs.",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Kerr v. United States District Court"
    ),
    DoctrineBlock(
        topic="Topic Res Judicata",
        keywords=["topic", "res judicata", "claim preclusion"],
        conclusion_template="Res judicata applies because: {analysis}.",
        reasoning_framework=(
            "1. Identify the prior judgment.\n"
            "2. Determine if the parties and claims are identical.\n"
            "3. Reference statutory and case law authority.\n"
            "4. Consider exceptions or limitations.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Final judgment",
            "Identity of parties",
            "Identity of claims"
        ],
        primary_authority=[
            "Restatement (Second) of Judgments",
            "Case Law on Res Judicata"
        ],
        burden_holder="Party asserting res judicata",
        adversary_position="Res judicata does not apply.",
        counter_arguments=[
            "Different parties.",
            "Different claims.",
            "No final judgment."
        ],
        resolution_strategy="Apply Restatement and controlling precedent.",
        entity_scope="All adjudicative proceedings.",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Federated Department Stores, Inc. v. Moitie"
    ),
    DoctrineBlock(
        topic="Topic Collateral Estoppel",
        keywords=["topic", "collateral estoppel", "issue preclusion"],
        conclusion_template="Collateral estoppel applies because: {analysis}.",
        reasoning_framework=(
            "1. Identify the issue previously litigated.\n"
            "2. Determine if the issue was actually and necessarily decided.\n"
            "3. Reference statutory and case law authority.\n"
            "4. Consider exceptions or limitations.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Identical issue",
            "Actually litigated",
            "Necessarily decided"
        ],
        primary_authority=[
            "Restatement (Second) of Judgments",
            "Case Law on Collateral Estoppel"
        ],
        burden_holder="Party asserting collateral estoppel",
        adversary_position="Collateral estoppel does not apply.",
        counter_arguments=[
            "Issue not identical.",
            "Not actually litigated.",
            "No final judgment."
        ],
        resolution_strategy="Apply Restatement and controlling precedent.",
        entity_scope="All adjudicative proceedings.",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Parklane Hosiery Co. v. Shore"
    ),
    DoctrineBlock(
        topic="Topic Declaratory Judgment",
        keywords=["topic", "declaratory judgment", "relief"],
        conclusion_template="Declaratory judgment is appropriate because: {analysis}.",
        reasoning_framework=(
            "1. Identify the controversy for which declaratory relief is sought.\n"
            "2. Reference statutory and case law authority.\n"
            "3. Determine if an actual controversy exists.\n"
            "4. Consider the appropriateness of declaratory relief.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Actual controversy",
            "Statutory authority",
            "Appropriateness of relief"
        ],
        primary_authority=[
            "28 U.S.C. § 2201",
            "Relevant Case Law"
        ],
        burden_holder="Party seeking declaratory judgment",
        adversary_position="Declaratory relief is not appropriate.",
        counter_arguments=[
            "No actual controversy.",
            "Relief is advisory.",
            "Alternative remedy exists."
        ],
        resolution_strategy="Apply statutory authority and controlling precedent.",
        entity_scope="All civil actions.",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="MedImmune, Inc. v. Genentech, Inc."
    ),
    DoctrineBlock(
        topic="Topic Abstention",
        keywords=["topic", "abstention", "federalism"],
        conclusion_template="Abstention is appropriate because: {analysis}.",
        reasoning_framework=(
            "1. Identify the grounds for abstention (e.g., Pullman, Younger, Burford).\n"
            "2. Reference statutory and case law authority.\n"
            "3. Determine if abstention is warranted to avoid interference with state proceedings.\n"
            "4. Consider the interests of federalism and comity.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Grounds for abstention",
            "State proceedings",
            "Federalism and comity"
        ],
        primary_authority=[
            "Younger v. Harris",
            "Relevant Case Law"
        ],
        burden_holder="Party seeking abstention",
        adversary_position="Abstention is not warranted.",
        counter_arguments=[
            "No parallel state proceeding.",
            "Federal rights at issue.",
            "No risk of interference."
        ],
        resolution_strategy="Apply abstention doctrine and controlling precedent.",
        entity_scope="All federal actions.",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Younger v. Harris"
    ),
    DoctrineBlock(
        topic="Topic Intervention",
        keywords=["topic", "intervention", "joinder"],
        conclusion_template="Intervention is appropriate because: {analysis}.",
        reasoning_framework=(
            "1. Identify the grounds for intervention (as of right or permissive).\n"
            "2. Reference statutory and case law authority.\n"
            "3. Determine if the intervenor's interests are adequately represented.\n"
            "4. Consider timeliness and prejudice.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Interest in action",
            "Adequate representation",
            "Timeliness"
        ],
        primary_authority=[
            "Federal Rules of Civil Procedure 24",
            "Relevant Case Law"
        ],
        burden_holder="Party seeking intervention",
        adversary_position="Intervention is not warranted.",
        counter_arguments=[
            "Interests are represented.",
            "Untimely motion.",
            "Prejudice to parties."
        ],
        resolution_strategy="Apply FRCP 24 and controlling precedent.",
        entity_scope="All civil actions.",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Trbovich v. United Mine Workers"
    ),
    DoctrineBlock(
        topic="Topic Amicus Curiae",
        keywords=["topic", "amicus curiae", "friend of the court"],
        conclusion_template="Amicus curiae participation is appropriate because: {analysis}.",
        reasoning_framework=(
            "1. Identify the grounds for amicus participation.\n"
            "2. Reference statutory and case law authority.\n"
            "3. Determine if the amicus will assist the court.\n"
            "4. Consider potential prejudice to parties.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Assistance to court",
            "Impartiality",
            "Prejudice to parties"
        ],
        primary_authority=[
            "Federal Rules of Appellate Procedure 29",
            "Relevant Case Law"
        ],
        burden_holder="Party seeking amicus participation",
        adversary_position="Amicus is unnecessary or biased.",
        counter_arguments=[
            "No unique perspective.",
            "Potential bias.",
            "Delay or prejudice."
        ],
        resolution_strategy="Apply FRAP 29 and controlling precedent.",
        entity_scope="All appellate actions.",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Miller-Wohl Co. v. Commissioner of Labor & Industry"
    ),
    DoctrineBlock(
        topic="Topic Reconsideration",
        keywords=["topic", "reconsideration", "relief from judgment"],
        conclusion_template="Reconsideration is appropriate because: {analysis}.",
        reasoning_framework=(
            "1. Identify the grounds for reconsideration (e.g., new evidence, clear error).\n"
            "2. Reference statutory and case law authority.\n"
            "3. Determine if the motion is timely.\n"
            "4. Assess the impact on the proceedings.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "New evidence",
            "Clear error",
            "Timeliness"
        ],
        primary_authority=[
            "Federal Rules of Civil Procedure 59(e), 60(b)",
            "Relevant Case Law"
        ],
        burden_holder="Party seeking reconsideration",
        adversary_position="No grounds for reconsideration.",
        counter_arguments=[
            "Evidence was available earlier.",
            "No clear error.",
            "Delay is prejudicial."
        ],
        resolution_strategy="Apply FRCP 59(e), 60(b) and controlling precedent.",
        entity_scope="All civil actions.",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gonzalez v. Crosby"
    ),
    DoctrineBlock(
        topic="Topic Substitution",
        keywords=["topic", "substitution", "party"],
        conclusion_template="Substitution of party is appropriate because: {analysis}.",
        reasoning_framework=(
            "1. Identify the grounds for substitution (e.g., death, incompetency).\n"
            "2. Reference statutory and case law authority.\n"
            "3. Determine if the motion is timely and parties are proper.\n"
            "4. Consider prejudice to parties.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Grounds for substitution",
            "Timeliness",
            "Proper parties"
        ],
        primary_authority=[
            "Federal Rules of Civil Procedure 25",
            "Relevant Case Law"
        ],
        burden_holder="Party seeking substitution",
        adversary_position="Substitution is not warranted.",
        counter_arguments=[
            "Improper party.",
            "Untimely motion.",
            "Prejudice to parties."
        ],
        resolution_strategy="Apply FRCP 25 and controlling precedent.",
        entity_scope="All civil actions.",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Rohan ex rel. Gates v. Woodford"
    ),
    DoctrineBlock(
        topic="Topic Consolidated Appeals",
        keywords=["topic", "consolidated appeals", "appellate procedure"],
        conclusion_template="Consolidated appeals are appropriate because: {analysis}.",
        reasoning_framework=(
            "1. Identify the cases suitable for consolidation on appeal.\n"
            "2. Reference statutory and case law authority.\n"
            "3. Assess commonality of issues and parties.\n"
            "4. Consider judicial efficiency and fairness.\n"
            "5. Document the analysis and conclusion."
        ),
        key_factors=[
            "Common issues",
            "Common parties",
            "Judicial efficiency"
        ],
        primary_authority=[
            "Federal Rules of Appellate Procedure 3(b)(2)",
            "Relevant Case Law"
        ],
        burden_holder="Party seeking consolidation",
        adversary_position="Consolidation is not warranted.",
        counter_arguments=[
            "Cases are unrelated.",
            "Prejudice to parties.",
            "Separate appeals are preferable."
        ],
        resolution_strategy="Apply FRAP 3(b)(2) and controlling precedent.",
        entity_scope="All appellate actions.",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Real Property Located at 475 Martin Lane"
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
        if (
            query_lower in doctrine.topic.lower()
            or any(query_lower in kw.lower() for kw in doctrine.keywords)
            or query_lower in doctrine.reasoning_framework.lower()
            or query_lower in doctrine.conclusion_template.lower()
        ):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]