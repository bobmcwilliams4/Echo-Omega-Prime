"""
PRB04 Will Contest Analyzer Engine v1.0.0
TIE-Grade Intelligence Engine for Will Contest Analysis

Doctrine domains: testamentary capacity, undue influence, fraud, duress, forgery,
improper execution, revocation, codicils, holographic wills, nuncupative wills,
no-contest clauses, tortious interference with inheritance.

Port: 9114
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

ENGINE_ID = "PRB04"
ENGINE_NAME = "Will Contest Analyzer"
VERSION = "1.0.0"
PORT = 9114

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class IssueCategory(str, Enum):
    CAPACITY = "testamentary_capacity"
    INFLUENCE = "undue_influence"
    FRAUD = "fraud_duress"
    EXECUTION = "improper_execution"
    REVOCATION = "revocation"
    HOLOGRAPHIC = "holographic_will"
    NUNCUPATIVE = "nuncupative_will"
    NO_CONTEST = "no_contest_clause"
    INTERFERENCE = "tortious_interference"
    FORGERY = "forgery"

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
    entity_scope: str
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=10)
    mode: ResponseMode = ResponseMode.FAST
    context: Dict[str, Any] = Field(default_factory=dict)

class QueryResponse(BaseModel):
    engine_id: str
    engine_name: str
    version: str
    query: str
    mode: str
    response: str
    confidence: str
    authorities: List[str]
    reasoning_chain: List[str]
    issues_detected: List[str]
    determinism_hash: str
    latency_ms: float
    timestamp: str

class HealthResponse(BaseModel):
    engine_id: str
    engine_name: str
    version: str
    status: str
    port: int
    doctrine_blocks: int
    uptime_seconds: float
    timestamp: str

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="testamentary_capacity_standard",
        keywords=["capacity", "sound mind", "mental competence", "testator", "understanding"],
        conclusion_template=[
            "Testamentary capacity requires: (1) understanding nature of act, (2) knowledge of property, (3) knowledge of natural objects of bounty, (4) understanding disposition being made.",
            "Capacity judged at time of execution, not earlier or later periods.",
            "Lower threshold than contractual capacity; lucid intervals count."
        ],
        reasoning_framework="""The testator must possess four elements: (1) understand this is a will disposing of property at death, (2) know the nature and extent of their property, (3) know the natural objects of their bounty (family members who would normally inherit), and (4) understand the disposition being made. Texas requires only that the testator be of sound mind; this is a low threshold. Capacity is judged at the moment of execution. A person who lacks capacity to contract may still have testamentary capacity. Brief lucid intervals suffice. The contestant bears the burden of proving incapacity by preponderance.""",
        key_factors=[
            "Medical diagnosis of dementia or cognitive impairment",
            "Testimony of attesting witnesses regarding testator behavior",
            "Temporal proximity of medical records to execution date",
            "Complexity of estate and whether testator understood it",
            "Whether disposition is rational or irrational",
            "Presence of lucid intervals documented by physicians",
            "Testator's ability to articulate reasons for bequests"
        ],
        primary_authority=[
            "Texas Estates Code Section 251.001 - testamentary capacity required",
            "Restatement Third of Property Section 8.1 - mental capacity standard",
            "Lee v. Lee, 424 S.W.3d 609 (Tex. 2014) - lucid interval doctrine",
            "Howell v. Taylor, 274 S.W.3d 381 (Tex. App. 2008) - low threshold for capacity"
        ],
        burden_holder="contestant",
        adversary_position="Proponent will argue attesting witnesses verified capacity at execution, physician diagnosis does not control, brief lucid interval suffices.",
        counter_arguments=[
            "Attesting witnesses are not medical experts and may miss subtle impairment",
            "Diagnosis of dementia creates strong inference of incapacity",
            "Irrational disposition evidences lack of understanding",
            "No evidence of lucid interval at the precise moment of execution",
            "Testator could not explain distribution scheme when asked"
        ],
        resolution_strategy="Obtain medical records within 30 days of execution. Depose attesting witnesses on specific questions asked and responses given. Depose physician on whether lucid intervals possible. If no lucid interval evidence and strong medical proof, high chance of success.",
        entity_scope="individual testator",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE if strong medical evidence; AGGRESSIVE if relying only on irrational disposition; DISCLOSURE if medical records ambiguous.",
        controlling_precedent="Lee v. Lee - lucid interval doctrine controls in Texas"
    ),
    DoctrineBlock(
        topic="undue_influence_standard",
        keywords=["undue influence", "coercion", "overpowering will", "confidential relationship", "suspicious circumstances"],
        conclusion_template=[
            "Undue influence requires: (1) existence and exertion of influence, (2) effect of overpowering testator's mind and will, (3) producing will that would not have been executed but for the influence.",
            "Burden shifts to proponent if contestant proves confidential relationship plus suspicious circumstances.",
            "Mere opportunity and motive insufficient; must show actual subversion of testator's intent."
        ],
        reasoning_framework="""Undue influence is coercion that overpowers the testator's free will and substitutes the influencer's desires. Three elements: (1) existence and exertion of influence, (2) effect was to overpower the mind and will, (3) but-for causation. Texas follows burden-shifting: if contestant proves confidential relationship (fiduciary or de facto dependency) plus suspicious circumstances, burden shifts to proponent to prove no undue influence by preponderance. Suspicious circumstances include: active procurement by beneficiary, testator's physical/mental weakness, unnatural disposition, secrecy, prior consistent dispositions changed, beneficiary controls testator's access to others.""",
        key_factors=[
            "Confidential relationship - fiduciary, agent, caretaker, or de facto dependency",
            "Active procurement - beneficiary arranged execution, selected attorney, drafted terms",
            "Secrecy - testator kept will secret from family, beneficiary isolated testator",
            "Susceptibility - testator's age, illness, medication, cognitive decline",
            "Unnatural disposition - disinheriting children in favor of recent acquaintance",
            "Prior consistent wills changed suddenly in favor of influencer",
            "Beneficiary controlled testator's information and access to advisors"
        ],
        primary_authority=[
            "Texas Estates Code Section 256.152 - undue influence defined",
            "Restatement Third of Property Section 8.3(b) - undue influence elements",
            "Rothermel v. Duncan, 369 S.W.2d 917 (Tex. 1963) - burden-shifting framework",
            "In re Estate of Canales, 837 S.W.2d 662 (Tex. App. 1992) - suspicious circumstances list"
        ],
        burden_holder="contestant initially; shifts to proponent if confidential relationship + suspicious circumstances proven",
        adversary_position="Proponent will argue testator was independent, made informed choice, had good reasons for disposition, no confidential relationship.",
        counter_arguments=[
            "Testator had independent legal advice from separate attorney",
            "Testator expressed reasons for disinheriting contestant",
            "Disposition reflects testator's prior stated intent",
            "No evidence of isolation or control of information",
            "Testator initiated contact with beneficiary, not vice versa"
        ],
        resolution_strategy="Establish confidential relationship via testimony on dependency and trust. Prove suspicious circumstances: beneficiary's active role in execution, secrecy, unnatural disposition. Once burden shifts, proponent must prove no influence by preponderance. Discovery: emails, texts showing control; medical records showing vulnerability; prior wills showing sudden change.",
        entity_scope="testator and alleged influencer",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="AGGRESSIVE if all suspicious circumstances present; DEFENSIBLE if confidential relationship clear but few suspicious facts; DISCLOSURE if relationship debatable.",
        controlling_precedent="Rothermel v. Duncan - burden-shifting framework is settled Texas law"
    ),
    DoctrineBlock(
        topic="fraud_in_execution",
        keywords=["fraud", "misrepresentation", "deception", "false statement", "inducement"],
        conclusion_template=[
            "Fraud requires: (1) false representation of material fact, (2) known to be false or made recklessly, (3) intent to induce reliance, (4) actual reliance, (5) injury.",
            "Fraud in the execution: testator deceived as to nature of instrument signed.",
            "Fraud in the inducement: testator deceived as to facts inducing execution of will."
        ],
        reasoning_framework="""Fraud in execution occurs when the testator is deceived about the nature of the document being signed (e.g., told it is a power of attorney when it is a will). Fraud in the inducement occurs when the testator is deceived about extrinsic facts that induce execution (e.g., false statement that a child is dead, inducing testator to disinherit that child). Elements: (1) false representation of material fact, (2) known false or reckless, (3) intent to induce reliance, (4) actual reliance, (5) injury. Burden on contestant by clear and convincing evidence. Fraud voids the will or the fraudulently induced provision.""",
        key_factors=[
            "False statement of material fact made to testator",
            "Speaker's knowledge of falsity or reckless disregard",
            "Intent to induce testator to execute or change will",
            "Testator's actual reliance on the false statement",
            "Causation - but-for the fraud, different disposition",
            "Corroborating evidence beyond contestant's testimony",
            "Temporal proximity of false statement to execution"
        ],
        primary_authority=[
            "Texas Estates Code Section 256.153 - fraud as grounds to contest",
            "Restatement Third of Property Section 8.3(d) - fraud defined",
            "Montgomery v. Blankenship, 217 S.W.3d 374 (Tex. App. 2007) - clear and convincing standard",
            "Harrison v. Harrison, 597 S.W.2d 477 (Tex. App. 1980) - fraud in inducement"
        ],
        burden_holder="contestant by clear and convincing evidence",
        adversary_position="Proponent will argue no false statement made, testator knew the truth, disposition was independent decision, no causation.",
        counter_arguments=[
            "Contestant has no proof of the alleged false statement beyond speculation",
            "Testator had independent knowledge of the true facts",
            "Disposition is consistent with testator's prior intent",
            "No evidence of speaker's knowledge of falsity",
            "No credible witnesses to the false statement"
        ],
        resolution_strategy="Obtain direct testimony from witnesses present when false statement made. Prove falsity with objective records (e.g., birth certificate if falsely told child is dead). Prove temporal proximity to execution. Prove testator lacked independent knowledge. Discovery: texts, emails, recorded conversations showing false statements.",
        entity_scope="testator and fraud perpetrator",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="AGGRESSIVE if clear and convincing proof exists; DISCLOSURE if relying on circumstantial evidence; HIGH_RISK if no corroboration.",
        controlling_precedent="Montgomery v. Blankenship - clear and convincing evidence required"
    ),
    DoctrineBlock(
        topic="improper_execution_formalities",
        keywords=["execution", "witnesses", "signature", "attestation", "formalities", "substantial compliance"],
        conclusion_template=[
            "Texas requires: (1) testator sign or acknowledge in presence of two witnesses, (2) witnesses sign in testator's presence.",
            "Substantial compliance doctrine may save will if formalities nearly met and no fraud.",
            "Self-proving affidavit creates presumption of due execution."
        ],
        reasoning_framework="""Texas Estates Code Section 251.051 requires: (1) testator sign the will or another sign at testator's direction in testator's presence, (2) at least two credible witnesses sign in testator's presence after testator signs or acknowledges signature. Witnesses need not sign in each other's presence. Substantial compliance doctrine: if the will substantially complies with formalities and there is clear and convincing evidence of testator's intent, will may be admitted despite technical defects. Self-proving affidavit (notarized statements by testator and witnesses) creates rebuttable presumption of due execution. Harmless error doctrine not adopted in Texas; strict compliance required absent substantial compliance showing.""",
        key_factors=[
            "Testator's signature present or attestation by another at testator's direction",
            "Two credible witnesses who observed testator sign or acknowledge",
            "Witnesses signed in testator's presence",
            "Presence requirement - same room, line of sight (conscious presence test)",
            "Self-proving affidavit executed before notary",
            "Witnesses' testimony on execution ceremony",
            "Whether defect creates fraud risk or evidences lack of testamentary intent"
        ],
        primary_authority=[
            "Texas Estates Code Section 251.051 - execution formalities",
            "Texas Estates Code Section 251.1025 - self-proving affidavit",
            "In re Estate of Marcos, 258 S.W.3d 41 (Tex. App. 2008) - substantial compliance",
            "Nichols v. Rowan, 422 S.W.2d 21 (Tex. Civ. App. 1967) - conscious presence test"
        ],
        burden_holder="proponent must prove due execution; contestant bears burden of proving defect if self-proving affidavit exists",
        adversary_position="Proponent will argue self-proving affidavit creates presumption, witnesses will testify to proper execution, substantial compliance met.",
        counter_arguments=[
            "Witnesses not present in same room when testator signed",
            "Witnesses signed outside testator's presence or after testator left",
            "Self-proving affidavit defective or notary not present",
            "Witness not credible - interested beneficiary or incompetent",
            "Signature forged or not testator's handwriting"
        ],
        resolution_strategy="Depose attesting witnesses on exact sequence: where they stood, what they saw, when they signed. Challenge credibility if interested. If no self-proving affidavit, burden on proponent to prove formalities. If affidavit exists, contestant must rebut presumption with clear evidence of defect. Handwriting expert if forgery alleged.",
        entity_scope="will execution event",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE if clear formality violation and no affidavit; AGGRESSIVE if attacking self-proving affidavit; DISCLOSURE if relying on substantial compliance.",
        controlling_precedent="Estate of Marcos - substantial compliance recognized but narrowly applied"
    ),
    DoctrineBlock(
        topic="revocation_express_implied",
        keywords=["revocation", "destroy", "cancel", "subsequent will", "codicil", "inconsistent provisions"],
        conclusion_template=[
            "Will revoked by: (1) subsequent will or codicil expressly revoking, (2) subsequent testamentary instrument inconsistent with prior will, (3) physical act of destruction with intent to revoke.",
            "Partial revocation permitted if provisions severable.",
            "Lost will presumed revoked if last seen in testator's possession and not found at death."
        ],
        reasoning_framework="""Texas Estates Code Section 253.002 permits revocation by: (1) subsequent will or codicil that expressly revokes or is inconsistent, (2) testator performing physical act of burning, tearing, canceling, obliterating, or destroying the will with intent to revoke. Intent required; accidental destruction does not revoke. If will last seen in testator's possession and not found at death, rebuttable presumption of revocation by destruction. Proponent can overcome by proving loss without revocation (e.g., stolen, misfiled). Partial revocation by physical act permitted in Texas if severable. Revival of revoked will requires re-execution or republication by codicil.""",
        key_factors=[
            "Subsequent will contains express revocation clause",
            "Subsequent will inconsistent with prior will provisions",
            "Physical act of destruction performed by testator or at testator's direction",
            "Intent to revoke evidenced by testator's statements or circumstances",
            "Will last in testator's possession but not found at death",
            "Proponent's explanation for non-production of original will",
            "Duplicate originals - destruction of one revokes all"
        ],
        primary_authority=[
            "Texas Estates Code Section 253.002 - methods of revocation",
            "Texas Estates Code Section 253.003 - revival of revoked will",
            "In re Estate of Glover, 744 S.W.2d 939 (Tex. 1988) - presumption of revocation when will not found",
            "In re Estate of Fox, 676 S.W.2d 773 (Tex. App. 1984) - intent to revoke required"
        ],
        burden_holder="contestant if alleging revocation; proponent if overcoming presumption of revocation",
        adversary_position="Contestant will argue will not produced so presumed revoked, or subsequent will revoked prior will by inconsistency. Proponent will argue no intent to revoke, will lost or stolen, no inconsistency.",
        counter_arguments=[
            "Will was stolen or lost without testator's knowledge",
            "Testator kept will in safe deposit box, not personal possession",
            "Subsequent will intended to supplement, not replace prior will",
            "Physical damage to will was accidental, not intentional",
            "Testator's statements show intent to keep will in effect"
        ],
        resolution_strategy="If will not produced, invoke presumption of revocation. Proponent must explain non-production with credible evidence (e.g., attorney affidavit that will stolen from office). If subsequent will exists, analyze for express revocation clause or inconsistent provisions. If physical destruction alleged, prove testator's intent through statements or circumstances. Discovery: interview custodian of will, obtain affidavits on last known location.",
        entity_scope="original will and any subsequent instruments",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE if will last in testator's possession and not found; AGGRESSIVE if alleging partial revocation; DISCLOSURE if facts on intent ambiguous.",
        controlling_precedent="Estate of Glover - presumption of revocation applies when will not produced"
    ),
    DoctrineBlock(
        topic="holographic_will_validity",
        keywords=["holographic", "handwritten", "unwitnessed", "material provisions", "testator's hand"],
        conclusion_template=[
            "Holographic will valid if: (1) entirely in testator's handwriting, (2) signed by testator, (3) no witnesses required.",
            "Material provisions must be in testator's hand; printed portions ignored unless incorporated by reference.",
            "Testamentary intent must be clear from the document itself."
        ],
        reasoning_framework="""Texas Estates Code Section 251.052 permits holographic wills: a will wholly in the testator's handwriting does not require attesting witnesses. Requirements: (1) material provisions in testator's handwriting, (2) signed by testator. Material provisions are those disposing of property; non-material provisions (date, preamble) may be printed. Testamentary intent must appear from the document - mere notes or letters not sufficient unless clear intent to make testamentary disposition. Signature need not be at end. No specific words required. Courts construe holographic wills liberally to effectuate intent.""",
        key_factors=[
            "Entire will in testator's handwriting or only material provisions handwritten",
            "Testator's signature present anywhere on document",
            "Language evidencing testamentary intent (I give, I bequeath, at my death)",
            "Clear identification of beneficiaries and property",
            "Handwriting verified by witnesses or expert",
            "Date present or absence of date creates ambiguity with other wills",
            "Whether document is letter, note, or formal will"
        ],
        primary_authority=[
            "Texas Estates Code Section 251.052 - holographic will requirements",
            "Succession of Cupit, 635 S.W.2d 127 (Tex. 1982) - material provisions test",
            "In re Estate of Gonzales, 855 S.W.2d 684 (Tex. App. 1993) - testamentary intent from four corners",
            "In re Estate of Teuton, 298 S.W.2d 456 (Tex. Civ. App. 1957) - liberal construction"
        ],
        burden_holder="proponent must prove testator's handwriting and testamentary intent",
        adversary_position="Contestant will argue document is not testamentary (mere notes), handwriting not verified, material provisions not handwritten, lacks signature.",
        counter_arguments=[
            "Document is informal letter not intended as will",
            "No clear dispositive language",
            "Handwriting not authenticated",
            "Testator executed subsequent formal will",
            "Printed fill-in-the-blank form with only blanks handwritten - material provisions not holographic"
        ],
        resolution_strategy="Authenticate handwriting through lay witnesses familiar with testator's writing or handwriting expert. Prove testamentary intent from language (I give, I leave, at my death, my will). If fill-in form, argue blanks contain material provisions. If informal letter, cite liberal construction cases. Discovery: obtain known exemplars of testator's handwriting for comparison.",
        entity_scope="handwritten will document",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="AGGRESSIVE if clear dispositive language and full handwriting; DEFENSIBLE if testamentary intent clear despite informality; DISCLOSURE if fill-in form with mixed handwritten/printed.",
        controlling_precedent="Cupit - material provisions test is key standard"
    ),
    DoctrineBlock(
        topic="no_contest_clause_enforceability",
        keywords=["no-contest", "in terrorem", "forfeiture", "probable cause", "good faith"],
        conclusion_template=[
            "No-contest clause enforceable in Texas if: (1) express forfeiture provision, (2) contestant brings contest without probable cause.",
            "Probable cause exists if reasonable person would believe contest has merit based on facts known at filing.",
            "Declaratory judgment action to construe will does not trigger clause."
        ],
        reasoning_framework="""Texas Estates Code Section 254.005 enforces no-contest (in terrorem) clauses that forfeit contestant's bequest if contest brought without probable cause. Probable cause exists if, at the time of filing, a reasonable person with knowledge of the relevant facts would believe the contest has reasonable likelihood of success. Measured objectively, not by actual outcome. Good faith belief in merit is the test. If probable cause exists, contestant does not forfeit even if contest fails. If no probable cause, forfeiture applies. Courts construe clauses strictly - clause must clearly state forfeiture consequence. Declaratory judgment action to construe ambiguous will does not trigger clause. Contest challenging instrument as not testator's will may have probable cause if facts support claim.""",
        key_factors=[
            "Express no-contest clause in will stating forfeiture consequence",
            "Scope of clause - does it cover all contests or only specific grounds",
            "Facts known to contestant at time of filing contest",
            "Objective reasonable belief that contest has merit",
            "Whether contestant sought legal advice before filing",
            "Whether contest alleged fraud, forgery, or other serious misconduct",
            "Whether declaratory judgment or full contest filed"
        ],
        primary_authority=[
            "Texas Estates Code Section 254.005 - no-contest clause enforceability",
            "In re Estate of Chisholm, 171 S.W.3d 160 (Tex. App. 2005) - probable cause standard",
            "Rothko v. Goetzmann, 320 S.W.3d 637 (Tex. App. 2010) - declaratory judgment not contest",
            "In re Estate of Littlefield, 691 S.W.2d 915 (Tex. App. 1985) - strict construction"
        ],
        burden_holder="proponent asserting forfeiture must prove contestant lacked probable cause",
        adversary_position="Contestant will argue probable cause existed based on facts known, good faith belief, serious allegations justify inquiry. Proponent argues frivolous contest to harass.",
        counter_arguments=[
            "Contestant had medical evidence of incapacity - probable cause exists",
            "Allegations of undue influence supported by suspicious circumstances",
            "Forgery claim supported by handwriting inconsistency",
            "Contest brought after legal consultation",
            "Declaratory judgment action, not direct contest"
        ],
        resolution_strategy="Analyze facts known to contestant at filing. If serious allegations (fraud, forgery, incapacity with medical evidence), probable cause likely exists and clause not triggered. If weak facts or purely vindictive contest, forfeiture may apply. Advise client to seek legal opinion before filing to show good faith. Consider declaratory judgment to construe will rather than direct contest if clause broad. Discovery: contestant's knowledge at time of filing, consultations with counsel.",
        entity_scope="will with no-contest clause and contesting beneficiary",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="AGGRESSIVE if serious allegations with evidentiary support; DEFENSIBLE if facts marginal; DISCLOSURE if clause scope ambiguous.",
        controlling_precedent="Chisholm - probable cause is objective reasonable belief at time of filing"
    ),
    DoctrineBlock(
        topic="tortious_interference_with_inheritance",
        keywords=["tortious interference", "expectancy", "intentional conduct", "wrongful", "damages"],
        conclusion_template=[
            "Tortious interference with inheritance requires: (1) expectancy of inheritance, (2) intentional interference by defendant, (3) through tortious conduct (fraud, undue influence, duress), (4) causation, (5) damages.",
            "Provides alternative remedy when will contest fails or not available.",
            "Defendant must act wrongfully, not merely influence testator."
        ],
        reasoning_framework="""Tortious interference with expectancy of inheritance is recognized in Texas. Elements: (1) plaintiff had reasonable expectancy of inheritance, (2) defendant intentionally interfered with that expectancy, (3) interference was by tortious means (fraud, undue influence, duress, forgery), (4) but for the interference, plaintiff would have received the inheritance, (5) damages. Reasonable expectancy shown by prior will naming plaintiff or intestate succession rights. Interference must be tortious - lawful persuasion of testator does not suffice. This is a tort claim, not probate contest; filed in district court, not probate court. Statute of limitations is two years from death or discovery of fraud. Remedy is damages, not reformation of will.""",
        key_factors=[
            "Plaintiff's reasonable expectancy - prior will, intestate rights, testator's promises",
            "Defendant's intentional conduct aimed at changing disposition",
            "Tortious means - fraud, undue influence, duress, forgery, threat",
            "But-for causation - plaintiff would have inherited absent interference",
            "Damages proven - value of lost inheritance",
            "Distinction from lawful persuasion of testator",
            "Discovery rule for statute of limitations if fraud concealed"
        ],
        primary_authority=[
            "King v. Acker, 725 S.W.2d 750 (Tex. App. 1987) - recognizing tort",
            "Restatement Second of Torts Section 774B - interference with inheritance",
            "Kinzbach Tool Co. v. Corbett-Wallace Corp., 160 S.W.2d 509 (Tex. 1942) - intentional interference",
            "Texas Civil Practice and Remedies Code Section 16.003 - two-year limitations"
        ],
        burden_holder="plaintiff by preponderance of evidence",
        adversary_position="Defendant will argue no reasonable expectancy, interference was lawful persuasion, no causation, plaintiff would not have inherited anyway, statute of limitations bars claim.",
        counter_arguments=[
            "Plaintiff had no reasonable expectancy - testator free to disinherit",
            "Defendant's conduct was lawful advice and persuasion",
            "Testator made independent decision, no causation",
            "Claim barred by statute of limitations",
            "Plaintiff cannot prove but-for causation"
        ],
        resolution_strategy="Establish reasonable expectancy with prior will naming plaintiff or evidence of testator's intent. Prove tortious means - fraud (false statements), undue influence (overpowering will), duress (threats). Prove but-for causation - testator would have left property to plaintiff absent interference. Damages equal value of lost bequest. File in district court within two years of death or discovery. Discovery: testator's prior wills, statements of intent, defendant's communications with testator, evidence of tortious conduct.",
        entity_scope="plaintiff with expectancy and interfering defendant",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="AGGRESSIVE if clear tortious conduct and causation; DEFENSIBLE if expectancy well-documented; DISCLOSURE if conduct arguably lawful persuasion.",
        controlling_precedent="King v. Acker - tort recognized in Texas"
    ),
    DoctrineBlock(
        topic="burden_of_proof_allocation",
        keywords=["burden", "proof", "preponderance", "clear and convincing", "presumption", "shift"],
        conclusion_template=[
            "Proponent bears burden of proving due execution and testamentary capacity by preponderance.",
            "Contestant bears burden of proving incapacity, undue influence, fraud, forgery by preponderance (clear and convincing for fraud).",
            "Self-proving affidavit shifts burden to contestant to rebut presumption of due execution.",
            "Confidential relationship plus suspicious circumstances shifts burden to proponent on undue influence."
        ],
        reasoning_framework="""Burden allocation: Proponent must prove (1) due execution, (2) testamentary capacity by preponderance. If self-proving affidavit exists, creates rebuttable presumption of due execution and capacity; contestant must overcome. Contestant bears burden of proving: incapacity, undue influence, fraud, duress, forgery. Standard is preponderance for incapacity and undue influence; clear and convincing for fraud. Exception: undue influence burden shifts if contestant proves confidential relationship plus suspicious circumstances, then proponent must disprove influence by preponderance. Lost will presumption: if will last in testator's possession and not found, presumed revoked; proponent must explain non-production. Forgery: contestant must prove by clear and convincing evidence.""",
        key_factors=[
            "Existence of self-proving affidavit",
            "Proponent's evidence of due execution and capacity",
            "Contestant's evidence of incapacity, influence, fraud",
            "Confidential relationship established",
            "Suspicious circumstances proven",
            "Medical records on capacity",
            "Witness testimony on execution ceremony"
        ],
        primary_authority=[
            "Texas Estates Code Section 256.153 - grounds for contest and burden",
            "Texas Estates Code Section 251.1025 - self-proving affidavit effect",
            "Rothermel v. Duncan, 369 S.W.2d 917 (Tex. 1963) - burden-shifting on undue influence",
            "In re Estate of Canales, 837 S.W.2d 662 (Tex. App. 1992) - burden allocation"
        ],
        burden_holder="varies by issue - proponent for execution and capacity, contestant for invalidity grounds",
        adversary_position="Each side seeks to shift burden to opponent via presumptions and evidentiary showings.",
        counter_arguments=[
            "Self-proving affidavit rebuts contestant's capacity challenge",
            "Confidential relationship not proven, no burden shift",
            "Contestant failed to produce clear and convincing evidence of fraud",
            "Proponent explained non-production of will, no revocation presumption"
        ],
        resolution_strategy="Identify which party bears burden on each issue. If self-proving affidavit, contestant must produce strong rebuttal evidence. If alleging undue influence, establish confidential relationship and suspicious circumstances to shift burden. If alleging fraud, gather clear and convincing proof. If will not produced, invoke presumption and force proponent to explain. Trial strategy: attack opponent's burden satisfaction, move for directed verdict if burden not met.",
        entity_scope="entire will contest proceeding",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE - burden allocation is well-settled; apply to facts.",
        controlling_precedent="Rothermel and Canales - burden-shifting framework clear"
    ),
    DoctrineBlock(
        topic="interested_witness_rule",
        keywords=["interested witness", "beneficiary", "witness", "purging statute", "disqualification"],
        conclusion_template=[
            "Interested witness (beneficiary) may attest will but bequest purged to extent exceeding intestate share.",
            "If two disinterested witnesses, interested witness's bequest not purged.",
            "Purging statute prevents fraud by interested witness but does not void will."
        ],
        reasoning_framework="""Texas Estates Code Section 251.107: if attesting witness is also a beneficiary (interested witness), the bequest to that witness is void to the extent it exceeds what the witness would receive under intestacy, unless there are two other disinterested credible witnesses. Purpose: prevent fraud where beneficiary attests own bequest. Effect: will valid, but interested witness's bequest purged. If will has three witnesses and one is interested, the two disinterested witnesses suffice and interested witness keeps bequest. If only two witnesses and one interested, that witness's bequest purged. Interested means receiving benefit under will; creditor witnesses not interested unless bequest exceeds debt.""",
        key_factors=[
            "Attesting witness is named beneficiary in will",
            "Value of bequest to interested witness",
            "Witness's intestate share if testator died without will",
            "Presence of two disinterested credible witnesses",
            "Whether witness's bequest exceeds intestate share",
            "Whether witness is creditor and bequest equals debt"
        ],
        primary_authority=[
            "Texas Estates Code Section 251.107 - purging statute",
            "In re Estate of Patterson, 616 S.W.2d 118 (Tex. App. 1981) - application of purging rule",
            "Restatement Third of Property Section 3.1 cmt. j - interested witness rules"
        ],
        burden_holder="contestant asserting purging; proponent proving two disinterested witnesses",
        adversary_position="Contestant argues interested witness invalidates bequest. Proponent argues two other witnesses or bequest within intestate share.",
        counter_arguments=[
            "Will has two disinterested witnesses, so interested witness keeps bequest",
            "Interested witness's bequest does not exceed intestate share",
            "Witness is creditor and bequest equals debt owed, not interest",
            "Witness renounced bequest, no longer interested"
        ],
        resolution_strategy="Identify if attesting witness is beneficiary. Count disinterested witnesses. If only two witnesses and one interested, purge that witness's bequest to intestate share. If three or more witnesses and at least two disinterested, interested witness keeps full bequest. Calculate intestate share to determine amount purged. Purging does not void will, only reduces interested witness's take.",
        entity_scope="attesting witness who is beneficiary",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE - statute clear; apply mechanically.",
        controlling_precedent="Estate of Patterson - purging statute application"
    ),
    DoctrineBlock(
        topic="dependent_relative_revocation",
        keywords=["dependent relative revocation", "DRR", "conditional revocation", "mistake", "intent"],
        conclusion_template=[
            "Dependent relative revocation: if testator revokes will based on mistaken assumption, revocation ineffective if mistake material to revocation decision.",
            "Applies when testator revokes old will intending to execute new will, but new will invalid.",
            "Court revives old will if testator preferred old will to intestacy."
        ],
        reasoning_framework="""Dependent relative revocation (DRR) is an equitable doctrine: if testator revokes a will based on a mistaken assumption of law or fact, and the mistake was material to the decision to revoke, the revocation is ineffective. Classic scenario: testator revokes Will 1 and executes Will 2, but Will 2 is invalid (improper execution, forgery). If testator's intent was to replace Will 1 with Will 2, and testator would not have revoked Will 1 had testator known Will 2 was invalid, DRR revives Will 1. Rationale: testator preferred Will 1 to intestacy. Courts apply DRR narrowly; must show testator's revocation was conditional on validity of new disposition.""",
        key_factors=[
            "Testator revoked prior will",
            "Revocation based on mistaken belief (e.g., new will valid)",
            "Mistake was material to decision to revoke",
            "Testator would not have revoked old will if knew truth",
            "Testator preferred old will to intestacy",
            "Evidence of testator's conditional intent",
            "New will invalid or ineffective"
        ],
        primary_authority=[
            "Restatement Third of Property Section 4.3 - dependent relative revocation",
            "In re Estate of Alburn, 118 N.W.2d 919 (Wis. 1963) - DRR classic case",
            "Texas case law limited; doctrine recognized but rarely applied"
        ],
        burden_holder="proponent seeking to revive revoked will bears burden of proving DRR elements",
        adversary_position="Contestant argues revocation was absolute, not conditional; testator intended intestacy over old will; no mistake proven.",
        counter_arguments=[
            "Testator's revocation was absolute, not conditional",
            "No evidence testator preferred old will to intestacy",
            "Testator knew new will might be invalid and revoked anyway",
            "DRR does not apply because testator's intent unclear"
        ],
        resolution_strategy="Prove testator's intent to replace, not merely revoke. Show evidence testator would not have revoked old will if knew new will invalid (e.g., testator's statements, close temporal proximity of revocation and new will execution). Argue testator preferred old will's disposition to intestate distribution. If new will invalid, DRR may revive old will. Rarely succeeds; requires strong proof of conditional intent.",
        entity_scope="revoked will and invalid new will",
        confidence=ConfidenceLevel.DISCLOSURE,
        confidence_stratification="DISCLOSURE - DRR rarely applied in Texas; high proof burden; uncertain outcome.",
        controlling_precedent="Restatement Third - persuasive authority; Texas cases rare"
    ),
    DoctrineBlock(
        topic="integration_incorporation_by_reference",
        keywords=["integration", "incorporation by reference", "extrinsic document", "present intent", "pages"],
        conclusion_template=[
            "Integration: all pages present at execution are part of will if testator intended them as one instrument.",
            "Incorporation by reference: extrinsic document incorporated if (1) document existed at will execution, (2) will describes it, (3) testator intended to incorporate.",
            "Acts of independent significance: will may refer to future acts or events with significance apart from testamentary effect."
        ],
        reasoning_framework="""Integration: all pages physically present at execution and intended by testator as part of the will are integrated into the will. Evidence: staples, continuous pagination, coherent provisions. Incorporation by reference: Texas recognizes incorporation of extrinsic documents if (1) document in existence at will execution, (2) will sufficiently describes it, (3) testator intended to incorporate it. Document must exist before will executed; cannot incorporate future-created documents. Acts of independent significance: will may refer to contents of safe deposit box, beneficiaries of life insurance, or other acts/events with significance independent of testamentary disposition. These are valid even though they occur after will execution.""",
        key_factors=[
            "Pages stapled or bound together at execution",
            "Continuous pagination or coherent provisions across pages",
            "Extrinsic document existed before will execution",
            "Will describes extrinsic document with sufficient particularity",
            "Testator's intent to incorporate extrinsic document",
            "Act or event has independent non-testamentary significance",
            "No evidence of page substitution after execution"
        ],
        primary_authority=[
            "Texas Estates Code Section 254.008 - incorporation by reference",
            "Restatement Third of Property Section 3.6 - integration and incorporation",
            "In re Estate of Tipton, 245 S.W.3d 670 (Tex. App. 2008) - integration",
            "Simon v. Grayson, 102 P.2d 1081 (Cal. 1940) - acts of independent significance"
        ],
        burden_holder="proponent asserting integration or incorporation",
        adversary_position="Contestant argues pages not integrated, extrinsic document not incorporated, reference invalid.",
        counter_arguments=[
            "Pages not present at execution, added later",
            "No evidence of integration - loose pages, no staple",
            "Extrinsic document created after will execution",
            "Will's description of document insufficient",
            "No testator intent to incorporate"
        ],
        resolution_strategy="Integration: prove pages present at execution via witness testimony, physical evidence (staples, pagination). Incorporation: prove document existed before will, will describes it clearly, testator intended incorporation. Acts of independent significance: argue reference to future act/event is valid because act has non-testamentary purpose. Discovery: interview attesting witnesses on pages present, obtain date of extrinsic document creation.",
        entity_scope="will pages and extrinsic documents",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE if clear evidence of integration or incorporation; AGGRESSIVE if facts ambiguous.",
        controlling_precedent="Tipton - integration requires pages present and intended at execution"
    ),
    DoctrineBlock(
        topic="class_gifts_and_lapse",
        keywords=["class gift", "lapse", "predeceased beneficiary", "anti-lapse", "substitute gift"],
        conclusion_template=[
            "If beneficiary predeceases testator, bequest lapses unless anti-lapse statute applies or will provides alternative.",
            "Anti-lapse statute: if beneficiary is testator's descendant and predeceases, beneficiary's descendants take by substitution.",
            "Class gifts: if class member predeceases, surviving class members take unless anti-lapse applies."
        ],
        reasoning_framework="""Texas Estates Code Section 255.153 (anti-lapse statute): if a beneficiary who is a descendant of the testator predeceases the testator, the beneficiary's descendants take the bequest by substitution, unless the will provides otherwise. Applies only to testator's descendants, not friends or distant relatives. If anti-lapse does not apply, bequest lapses and falls to residue, or if residue, to intestacy. Class gifts: if will gives to a class (e.g., my children, my nieces and nephews) and a class member predeceases, surviving class members take the deceased member's share unless anti-lapse statute diverts it to deceased member's descendants. Will can override anti-lapse by express provision (no substitution, lapsed share to [X]).""",
        key_factors=[
            "Beneficiary predeceased testator",
            "Beneficiary is descendant of testator (anti-lapse applies)",
            "Beneficiary has surviving descendants to take by substitution",
            "Will contains express anti-lapse override provision",
            "Bequest is to individual or to class",
            "Class member predeceased, surviving class members exist",
            "Will provides alternative taker or residue clause"
        ],
        primary_authority=[
            "Texas Estates Code Section 255.153 - anti-lapse statute",
            "Restatement Third of Property Section 5.5 - lapse and anti-lapse",
            "In re Estate of Davenport, 162 S.W.3d 639 (Tex. App. 2005) - anti-lapse application",
            "In re Estate of Moss, 209 S.W.3d 313 (Tex. App. 2006) - class gifts"
        ],
        burden_holder="party asserting anti-lapse application or lapse",
        adversary_position="Competing claimants argue whether anti-lapse applies or bequest lapsed to residue.",
        counter_arguments=[
            "Beneficiary not testator's descendant, anti-lapse does not apply",
            "Will expressly provides no substitution",
            "Beneficiary has no descendants, anti-lapse fails",
            "Class gift - surviving class members take, not descendants",
            "Lapsed share falls to residue per will terms"
        ],
        resolution_strategy="Determine if beneficiary is testator's descendant. If yes and beneficiary predeceased, anti-lapse diverts bequest to beneficiary's descendants. If beneficiary not descendant, bequest lapses to residue. If class gift, surviving class members take unless anti-lapse diverts deceased member's share. Check will for express anti-lapse override. If residuary bequest lapses, intestacy applies to lapsed portion. Discovery: family tree, death certificates, will provisions on alternative takers.",
        entity_scope="predeceased beneficiary and substitute takers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE - anti-lapse statute mechanical application; check family relationship and will language.",
        controlling_precedent="Davenport and Moss - anti-lapse and class gift rules clear"
    ),
    DoctrineBlock(
        topic="ademption_by_extinction",
        keywords=["ademption", "specific bequest", "property no longer in estate", "extinction", "replacement property"],
        conclusion_template=[
            "Ademption: specific bequest fails if property not in estate at death.",
            "Identity theory: if specifically bequeathed property disposed of during life, bequest adeemed regardless of testator's intent.",
            "UPC intent theory not adopted in Texas; ademption automatic if property gone."
        ],
        reasoning_framework="""Ademption by extinction occurs when a specific bequest of property fails because the property is not in the testator's estate at death. Texas follows identity theory: if the specific property is not in the estate, the bequest adeems (fails) regardless of testator's intent or reason for disposing of property. Example: will gives Blackacre to A; testator sells Blackacre before death; bequest to A adeems, A gets nothing. Replacement property does not satisfy specific bequest unless will so provides. UPC intent theory (beneficiary entitled to replacement or proceeds if testator did not intend ademption) is not Texas law. Specific bequest vs. general bequest: specific = particular item, general = dollar amount or fungible property. Only specific bequests adeem.""",
        key_factors=[
            "Bequest is specific (particular property) not general (dollar amount)",
            "Property no longer in testator's estate at death",
            "Property sold, given away, destroyed, or lost during life",
            "Replacement property acquired",
            "Proceeds from sale or insurance traceable",
            "Testator's intent regarding ademption (not controlling in Texas)",
            "Conservator sold property during testator's incapacity"
        ],
        primary_authority=[
            "Texas case law - identity theory of ademption",
            "Restatement Third of Property Section 5.2 - ademption",
            "In re Estate of Gerbing, 337 S.W.3d 324 (Tex. App. 2011) - ademption by extinction",
            "UPC Section 2-606 - intent theory (not adopted in Texas)"
        ],
        burden_holder="party claiming ademption must prove property not in estate",
        adversary_position="Beneficiary argues property still in estate or replacement property satisfies bequest. Contestant argues ademption occurred.",
        counter_arguments=[
            "Property still in estate in different form (e.g., proceeds in bank account)",
            "Replacement property acquired, should satisfy bequest",
            "Sale by conservator during incapacity should not cause ademption",
            "Testator intended beneficiary to receive value, not just specific property",
            "Bequest is general, not specific, so no ademption"
        ],
        resolution_strategy="Determine if bequest is specific or general. If specific, check if property in estate at death. If not, ademption under identity theory. Beneficiary gets nothing unless will provides for replacement or proceeds. If property sold and proceeds traceable, argue proceeds satisfy bequest (weak argument in Texas). If sale by conservator during incapacity, argue exception to ademption (limited case law). Discovery: estate inventory, sale records, replacement property acquisitions, will language.",
        entity_scope="specific bequest and property disposition",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE - identity theory is harsh but clear; ademption automatic if property gone; DISCLOSURE if arguing conservator exception.",
        controlling_precedent="Gerbing - Texas follows identity theory of ademption"
    ),
    DoctrineBlock(
        topic="abatement_order",
        keywords=["abatement", "insufficient assets", "priority", "residue", "general", "specific", "demonstrative"],
        conclusion_template=[
            "Abatement: if estate insufficient to pay all bequests, bequests abate in order: intestate property, residue, general, demonstrative, specific.",
            "Bequests within same class abate pro rata unless will provides otherwise.",
            "Specific bequests last to abate; intestate property first."
        ],
        reasoning_framework="""When estate assets are insufficient to satisfy all bequests and debts, bequests abate (reduce) in this order: (1) property passing by intestacy (if partial intestacy), (2) residuary bequests, (3) general bequests (dollar amounts), (4) demonstrative bequests (dollar amounts from specific source), (5) specific bequests (particular property). Within each class, bequests abate pro rata unless will provides different order. Specific bequests abate last because testator intended beneficiary to receive that particular property. Residuary abates first because it is the catch-all. Debts and taxes paid before abatement to beneficiaries. Will can alter abatement order by express provision.""",
        key_factors=[
            "Estate assets insufficient to pay all bequests and debts",
            "Classification of bequests: specific, demonstrative, general, residuary",
            "Will's express abatement order provision",
            "Pro rata abatement within each class",
            "Debts and administration expenses paid first",
            "Family allowance and homestead protections",
            "Federal estate tax apportionment among beneficiaries"
        ],
        primary_authority=[
            "Texas Estates Code Section 355.109 - abatement order",
            "Restatement Third of Property Section 9.2 - abatement",
            "In re Estate of Dillard, 98 S.W.3d 386 (Tex. App. 2003) - abatement application"
        ],
        burden_holder="executor must apply abatement order; beneficiaries may contest classification or order",
        adversary_position="Beneficiaries argue their bequests should not abate or should abate less; executor argues proper abatement applied.",
        counter_arguments=[
            "Bequest is specific, not general, so should abate last",
            "Will provides different abatement order",
            "Estate has sufficient assets, no abatement needed",
            "Pro rata abatement within class should apply",
            "Beneficiary entitled to exoneration from debts"
        ],
        resolution_strategy="Classify each bequest as specific, demonstrative, general, or residuary. Apply statutory abatement order unless will provides otherwise. Calculate pro rata reduction within each class if needed. Specific bequests preserved unless all other classes exhausted. If will alters order, follow will's provision. Discovery: estate inventory, valuation of assets, total debts and expenses, will provisions on abatement.",
        entity_scope="entire estate and all bequests",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE - abatement order statutory and mechanical; classify bequests correctly.",
        controlling_precedent="Dillard - abatement order application"
    ),
    DoctrineBlock(
        topic="advancements_and_satisfaction",
        keywords=["advancement", "satisfaction", "inter vivos gift", "hotchpot", "intent to advance"],
        conclusion_template=[
            "Advancement: lifetime gift to heir treated as advance on inheritance if testator intended as advancement.",
            "Satisfaction: lifetime gift to legatee treated as satisfaction of bequest if testator intended.",
            "Both require testator's contemporaneous written intent or beneficiary's acknowledgment."
        ],
        reasoning_framework="""Advancement (intestacy context): lifetime gift to heir treated as prepayment of intestate share if testator declared in contemporaneous writing that gift is advancement, or heir acknowledged in writing. Gift's value added to estate for distribution calculation, then subtracted from heir's share. Satisfaction (will context): lifetime gift to legatee treated as satisfaction of bequest if testator declared in will or contemporaneous writing, or legatee acknowledged. If gift equals or exceeds bequest, bequest satisfied (adeemed). If gift less than bequest, legatee receives difference. Texas requires written evidence of intent; oral statements insufficient. Prevents double recovery by beneficiary who received both lifetime gift and bequest.""",
        key_factors=[
            "Lifetime gift made by testator to heir or legatee",
            "Testator's contemporaneous written declaration of intent to advance or satisfy",
            "Beneficiary's written acknowledgment of advancement or satisfaction",
            "Value of gift compared to bequest or intestate share",
            "Whether gift was intended as loan, not advancement",
            "Will provision addressing lifetime gifts",
            "Evidence of testator's intent from circumstances"
        ],
        primary_authority=[
            "Texas Estates Code Section 201.151 - advancements in intestacy",
            "Texas Estates Code Section 255.054 - satisfaction of bequests",
            "Restatement Third of Property Section 5.1 - satisfaction",
            "In re Estate of Barfield, 563 S.W.2d 407 (Tex. Civ. App. 1978) - advancement"
        ],
        burden_holder="party claiming advancement or satisfaction must prove testator's written intent or beneficiary's acknowledgment",
        adversary_position="Beneficiary argues gift was not advancement/satisfaction, but outright gift or loan. Claimant argues gift should reduce beneficiary's share.",
        counter_arguments=[
            "No contemporaneous written declaration by testator",
            "No written acknowledgment by beneficiary",
            "Gift was loan, not advancement, as evidenced by [promissory note, repayment terms]",
            "Testator intended gift as outright present, not advance",
            "Will expressly provides lifetime gifts not to be considered"
        ],
        resolution_strategy="Search for written evidence of testator's intent to advance or satisfy: will provisions, letters, checks with notation, signed statements. Obtain beneficiary's written acknowledgment if any. Calculate value of gift and compare to bequest or intestate share. If no written evidence, advancement/satisfaction claim fails. If gift equals bequest, bequest satisfied. If gift less, beneficiary receives difference. Discovery: testator's writings, beneficiary acknowledgments, evidence of gift value.",
        entity_scope="heir or legatee who received lifetime gift",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="AGGRESSIVE if contemporaneous written intent exists; DISCLOSURE if relying on circumstantial evidence; HIGH_RISK if no writing.",
        controlling_precedent="Barfield - written evidence of intent required"
    ),
    DoctrineBlock(
        topic="elective_share_and_community_property",
        keywords=["elective share", "surviving spouse", "community property", "separate property", "spousal rights"],
        conclusion_template=[
            "Texas is community property state; no elective share statute.",
            "Surviving spouse owns half of community property by operation of law, regardless of will.",
            "Testator can only devise own half of community property and all separate property.",
            "Disinherited spouse may claim community property share but has no elective share in separate property."
        ],
        reasoning_framework="""Texas does not have elective share statute. Community property regime controls. All property acquired during marriage (except by gift, devise, or descent) is community property owned equally by spouses. On death, decedent can devise only their half of community property plus all separate property. Surviving spouse owns their half of community property outright, cannot be defeated by will. If will purports to devise entire community property, surviving spouse can assert their half. Testator can disinherit spouse from separate property and testator's half of community, but spouse retains their community half. Homestead and exempt property protections also apply.""",
        key_factors=[
            "Property classification as community or separate",
            "Surviving spouse's ownership of community property half",
            "Will's attempted disposition of entire community property",
            "Separate property subject to testator's complete testamentary freedom",
            "Homestead rights of surviving spouse",
            "Exempt personal property allowances",
            "Family allowance for support during administration"
        ],
        primary_authority=[
            "Texas Family Code Section 3.001 - community property definition",
            "Texas Constitution Article XVI Section 15 - separate property",
            "Texas Estates Code Section 101.001 - homestead rights",
            "Texas Estates Code Section 353.001 - exempt property and allowances"
        ],
        burden_holder="surviving spouse claiming community property must prove property is community; contestant claiming separate property bears burden",
        adversary_position="Will beneficiaries argue property is separate, not community. Surviving spouse argues property is community.",
        counter_arguments=[
            "Property acquired before marriage is separate",
            "Property acquired by gift or inheritance is separate",
            "Partition or exchange agreement converted community to separate",
            "Inception of title rule - property community if acquired during marriage",
            "Tracing commingled funds to separate source"
        ],
        resolution_strategy="Classify all property as community or separate using inception of title rule. Surviving spouse owns half of community property; assert this against will purporting to devise entire community property. Testator's will can dispose only of testator's half of community and all separate property. If will disinherits spouse, spouse still gets community half plus homestead, exempt property, and family allowance. Discovery: property acquisition dates, sources of funds, partition agreements, gift or inheritance documentation.",
        entity_scope="surviving spouse and marital property",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE - community property law well-settled; classify property correctly.",
        controlling_precedent="Texas Family Code and Estates Code - community property and homestead rights"
    ),
    DoctrineBlock(
        topic="standing_to_contest",
        keywords=["standing", "interested person", "pecuniary interest", "beneficiary", "heir"],
        conclusion_template=[
            "Only interested person has standing to contest will.",
            "Interested person: has pecuniary interest in estate that would be affected by will's probate or denial.",
            "Includes heirs, beneficiaries under prior will, creditors with claims.",
            "Beneficiary under contested will generally lacks standing to contest provisions benefiting others."
        ],
        reasoning_framework="""Texas Estates Code Section 22.018 defines interested person as heir, devisee, spouse, creditor, or any person with property right or claim affected by estate administration. Standing to contest will requires pecuniary interest that would be impaired or defeated if will is probated, or benefited if will is denied. Heir at law has standing because intestacy would benefit them. Beneficiary under prior will has standing if prior will gives them more than contested will. Disinherited child has standing. Person named in contested will as beneficiary generally lacks standing to challenge other provisions unless reduction of other bequests would increase theirs (residuary beneficiary). Nominal beneficiary lacks standing if contest would not increase their share.""",
        key_factors=[
            "Contestant is heir at law who would inherit under intestacy",
            "Contestant is beneficiary under prior will with larger bequest",
            "Contestant is surviving spouse with community property or homestead rights",
            "Contestant is creditor with claim against estate",
            "Contestant's pecuniary interest would be benefited if will denied",
            "Whether contest challenges entire will or specific provisions",
            "Nominal bequest to contestant (e.g., $1) does not defeat standing if intestacy gives more"
        ],
        primary_authority=[
            "Texas Estates Code Section 22.018 - interested person definition",
            "Texas Estates Code Section 256.001 - who may contest",
            "In re Estate of Herring, 934 S.W.2d 760 (Tex. App. 1996) - standing requirement",
            "In re Estate of Gonzales, 855 S.W.2d 684 (Tex. App. 1993) - pecuniary interest"
        ],
        burden_holder="contestant must prove standing as threshold matter",
        adversary_position="Proponent will move to dismiss for lack of standing if contestant has no pecuniary interest.",
        counter_arguments=[
            "Contestant is not heir - no intestate succession rights",
            "Contestant receives same or more under contested will than intestacy",
            "Contestant challenging provisions that do not affect their share",
            "Contestant has no pecuniary interest, only emotional interest",
            "No-contest clause forfeits contestant's bequest, eliminating standing"
        ],
        resolution_strategy="Establish contestant's status as heir, prior will beneficiary, or spouse. Prove pecuniary interest: if will denied, contestant would receive more via intestacy or prior will. If only challenging specific provision, show how invalidating that provision increases contestant's share. If nominal bequest given, argue intestacy share exceeds nominal amount. If no-contest clause forfeited bequest, argue standing exists to challenge clause itself or contest has probable cause. File verified pleadings showing standing. Discovery: family tree, prior wills, estate valuation, contestant's intestate share calculation.",
        entity_scope="contestant's relationship to decedent and estate",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE - standing requirement mechanical; prove pecuniary interest affected.",
        controlling_precedent="Herring and Gonzales - standing requires pecuniary interest"
    ),
    DoctrineBlock(
        topic="venue_and_jurisdiction",
        keywords=["venue", "jurisdiction", "domicile", "residence", "probate court", "county"],
        conclusion_template=[
            "Venue for probate in county of decedent's domicile at death.",
            "If no Texas domicile, venue in county where decedent had property.",
            "Jurisdiction: statutory probate court, county court at law, or constitutional county court.",
            "Probate court has exclusive jurisdiction over will contests."
        ],
        reasoning_framework="""Texas Estates Code Section 32.001: venue proper in county of decedent's domicile at time of death. If decedent not domiciled in Texas, venue in any county where decedent had property. Domicile means fixed permanent home with intent to remain. Mere residence insufficient. If dispute over domicile, probate filed in competing counties - first court to assume jurisdiction controls. Jurisdiction: statutory probate courts have exclusive original jurisdiction in counties with such courts; county courts at law or constitutional county courts in counties without. Will contest must be filed in court with probate jurisdiction. Transfer from county court to district court not permitted; probate court retains exclusive jurisdiction over validity of will.""",
        key_factors=[
            "Decedent's domicile (intent to make permanent home) at death",
            "Decedent's physical residence at death",
            "Decedent's property located in Texas",
            "Competing probate filings in different counties",
            "Court type in county: statutory probate, county court at law, constitutional county court",
            "Exclusive jurisdiction of probate court over will contest",
            "Motion to transfer venue if improper county"
        ],
        primary_authority=[
            "Texas Estates Code Section 32.001 - venue",
            "Texas Estates Code Section 25.0021 - jurisdiction of statutory probate courts",
            "Texas Estates Code Section 256.001 - will contest filed in court with probate jurisdiction",
            "In re Estate of Jones, 197 S.W.3d 894 (Tex. 2006) - domicile determination"
        ],
        burden_holder="party challenging venue bears burden of proving improper venue",
        adversary_position="Opponent argues proper venue; contestant argues improper venue and seeks transfer.",
        counter_arguments=[
            "Decedent domiciled in different county - evidence of intent and residence",
            "Decedent not domiciled in Texas, but had property in this county",
            "First court to assume jurisdiction controls - prior probate filed",
            "Venue proper in any county with decedent's property if no Texas domicile",
            "Motion to transfer venue untimely"
        ],
        resolution_strategy="Establish decedent's domicile at death: physical residence plus intent to remain. Evidence: voter registration, driver's license, homestead, declarations of intent. If multiple probate filings, determine which court assumed jurisdiction first. If improper venue, file motion to transfer within time limits. Probate contest must be in probate court - cannot be removed to district court. Discovery: decedent's residence history, intent declarations, property locations, prior probate filings in other counties.",
        entity_scope="county and court for probate proceeding",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE - venue rules mechanical; prove domicile.",
        controlling_precedent="Jones - domicile is physical presence plus intent"
    ),
    DoctrineBlock(
        topic="statute_of_limitations",
        keywords=["limitations", "deadline", "two years", "four years", "discovery rule", "tolling"],
        conclusion_template=[
            "Will contest must be filed within two years of will admitted to probate, unless fraud or lack of jurisdiction.",
            "If will not probated, contest when application for probate filed.",
            "Discovery rule tolls limitations if fraud concealed until discovery.",
            "Forgery claim not subject to two-year limit if lack of jurisdiction alleged."
        ],
        reasoning_framework="""Texas Estates Code Section 256.003: contest must be filed within two years after will admitted to probate. If will not admitted, contest filed any time before final distribution. Exception: if fraud or lack of jurisdiction, contest may be brought later. Discovery rule: if fraud concealed and not discoverable with reasonable diligence, limitations tolls until discovery or should have discovered. Forgery creates jurisdictional defect (not testator's will), so two-year limit may not apply. Tortious interference with inheritance has two-year tort limitations from death or discovery. Limitations runs from probate order, not death. If probate as muniment of title (no administration), two-year period still applies.""",
        key_factors=[
            "Date will admitted to probate",
            "Whether fraud or lack of jurisdiction alleged",
            "Discovery of fraud - when contestant knew or should have known",
            "Reasonable diligence in discovering fraud",
            "Forgery claim (jurisdictional defect, may avoid two-year limit)",
            "Final distribution - contest barred after final distribution if no fraud",
            "Tolling for minority or incapacity of contestant"
        ],
        primary_authority=[
            "Texas Estates Code Section 256.003 - two-year limitations",
            "Texas Estates Code Section 256.204 - fraud exception",
            "In re Estate of Bell, 168 S.W.3d 259 (Tex. App. 2005) - discovery rule",
            "In re Estate of Luton, 310 S.W.3d 263 (Tex. App. 2010) - forgery jurisdictional defect"
        ],
        burden_holder="proponent asserting limitations bar; contestant asserting exception",
        adversary_position="Proponent argues limitations expired, contest untimely. Contestant argues fraud exception or discovery rule.",
        counter_arguments=[
            "Contest timely filed within two years of probate",
            "Fraud discovered within limitations period after reasonable diligence",
            "Forgery claim - will void ab initio, jurisdictional defect, no limitations",
            "Contestant was minor or incapacitated, tolling applies",
            "Will never probated, no limitations bar until final distribution"
        ],
        resolution_strategy="Calculate two years from probate order date. If beyond two years, assert fraud or lack of jurisdiction exception. Prove fraud was concealed and not discoverable despite reasonable diligence until discovery date. If forgery, argue jurisdictional defect voids will and limitations inapplicable. File contest promptly after discovery if fraud concealed. If will not probated, contest before final distribution. Discovery: probate records, contestant's knowledge timeline, evidence of concealment, reasonableness of diligence.",
        entity_scope="timing of will contest filing",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE if within two years; AGGRESSIVE if asserting fraud exception; DISCLOSURE if discovery rule application unclear.",
        controlling_precedent="Bell and Luton - discovery rule and forgery exception"
    ),
    DoctrineBlock(
        topic="harmless_error_doctrine",
        keywords=["harmless error", "substantial compliance", "technical defect", "clear and convincing", "testamentary intent"],
        conclusion_template=[
            "Texas recognizes substantial compliance for minor formality defects if clear and convincing evidence of testamentary intent.",
            "Harmless error doctrine (UPC Section 2-503) not fully adopted in Texas.",
            "Self-proving affidavit defect may be harmless if execution otherwise valid."
        ],
        reasoning_framework="""Texas has not adopted UPC Section 2-503 harmless error doctrine, which dispenses with formalities if clear and convincing evidence of testamentary intent. Texas requires substantial compliance: will substantially complies with formalities even if technical defect exists. Defect must be minor and no fraud risk. Self-proving affidavit defect (e.g., notary error) may be harmless if will itself properly executed - affidavit creates presumption but defect does not void will if underlying execution valid. Holographic will cases apply liberal construction to find testamentary intent. Execution formality violations (no witnesses, wrong number, witnesses not in presence) generally fatal unless substantial compliance shown.""",
        key_factors=[
            "Nature of formality defect - technical vs. substantial",
            "Clear and convincing evidence of testamentary intent",
            "Whether defect creates fraud risk or undermines purpose of formality",
            "Self-proving affidavit defect vs. will execution defect",
            "Witnesses' testimony that execution ceremony occurred despite defect",
            "Holographic will - liberal construction of testamentary intent",
            "Policy: effectuate testator's intent vs. strict formality compliance"
        ],
        primary_authority=[
            "UPC Section 2-503 - harmless error (not adopted in Texas)",
            "In re Estate of Marcos, 258 S.W.3d 41 (Tex. App. 2008) - substantial compliance",
            "Restatement Third of Property Section 3.3 - harmless error",
            "Texas Estates Code Section 251.1045 - self-proving affidavit defect"
        ],
        burden_holder="proponent seeking to validate defective will bears burden of proving substantial compliance and testamentary intent by clear and convincing evidence",
        adversary_position="Contestant argues strict compliance required, defect is fatal. Proponent argues substantial compliance or harmless error.",
        counter_arguments=[
            "Strict compliance required in Texas, no harmless error doctrine",
            "Defect is substantial, not technical",
            "No clear and convincing evidence of testamentary intent",
            "Fraud risk present due to defect",
            "Substantial compliance inapplicable to this type of defect"
        ],
        resolution_strategy="If defect is technical (e.g., affidavit notary error, misdated), argue substantial compliance or harmless error. Prove clear and convincing evidence of testamentary intent via witnesses, document language, testator's statements. If defect is substantial (no witnesses, signature missing), substantial compliance unlikely to save will. Self-proving affidavit defect does not void will if execution itself valid. Holographic wills - argue liberal construction. Discovery: witness testimony on execution, expert testimony on testamentary intent, extrinsic evidence of testator's intent.",
        entity_scope="defective will and formality violation",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="AGGRESSIVE - substantial compliance uncertain; depends on defect severity and evidence of intent; DISCLOSURE if relying heavily on harmless error not adopted in Texas.",
        controlling_precedent="Marcos - substantial compliance recognized but narrowly applied"
    )
]

EPISTEMIC_GUARDRAILS = [
    "Consult qualified Texas probate attorney for case-specific advice",
    "This analysis is based on general principles; fact-specific nuances may alter outcome",
    "Will contest litigation is fact-intensive and requires discovery",
    "Medical and handwriting experts may be necessary",
    "Statute of limitations and procedural deadlines are strict",
    "Evidentiary proof required; speculation insufficient",
    "Court decisions vary by county and judge",
    "Consider settlement and alternative dispute resolution",
    "Full disclosure to client of risks and costs required"
]

BANNED_PHRASES = [
    "probably",
    "might want to",
    "consider perhaps",
    "it seems like",
    "I think",
    "in my opinion"
]

START_TIME = time.time()

def get_doctrine_cache() -> List[DoctrineBlock]:
    return DOCTRINE_CACHE

def search_doctrines(query: str, limit: int = 5) -> List[DoctrineBlock]:
    query_lower = query.lower()
    scored = []
    for block in DOCTRINE_CACHE:
        score = 0
        if any(kw in query_lower for kw in block.keywords):
            score += 10
        if block.topic.replace("_", " ") in query_lower:
            score += 20
        if score > 0:
            scored.append((score, block))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [block for _, block in scored[:limit]]

def apply_epistemic_guardrails(text: str) -> str:
    for phrase in BANNED_PHRASES:
        if phrase in text.lower():
            text = text.replace(phrase, "[EPISTEMIC_VIOLATION_REMOVED]")
    return text

def three_layer_response(query: str, mode: ResponseMode, context: Dict[str, Any]) -> Tuple[str, List[str], List[str], str]:
    doctrines = search_doctrines(query, limit=5)
    issues = [d.topic for d in doctrines]

    if mode == ResponseMode.FAST:
        if doctrines:
            primary = doctrines[0]
            response = f"Will contest issue detected: {primary.topic.replace('_', ' ').title()}. "
            response += primary.conclusion_template[0] + " "
            response += f"Burden: {primary.burden_holder}. "
            response += f"Key authority: {primary.primary_authority[0]}."
            authorities = primary.primary_authority[:2]
            reasoning = [primary.conclusion_template[0]]
            confidence = primary.confidence.value
        else:
            response = "No matching doctrine. Consult probate attorney for case analysis."
            authorities = []
            reasoning = ["General will contest principles apply"]
            confidence = ConfidenceLevel.DISCLOSURE.value

    elif mode == ResponseMode.DEFENSE:
        response_parts = []
        authorities = []
        reasoning = []
        for doctrine in doctrines[:3]:
            response_parts.append(f"\n{doctrine.topic.replace('_', ' ').upper()}:\n")
            response_parts.append(doctrine.reasoning_framework + "\n")
            response_parts.append(f"Burden: {doctrine.burden_holder}.\n")
            response_parts.append(f"Strategy: {doctrine.resolution_strategy}\n")
            authorities.extend(doctrine.primary_authority[:2])
            reasoning.append(doctrine.reasoning_framework[:200])
        response = "".join(response_parts)
        confidence = doctrines[0].confidence.value if doctrines else ConfidenceLevel.DISCLOSURE.value

    else:  # MEMO
        response_parts = []
        authorities = []
        reasoning = []
        for doctrine in doctrines[:5]:
            response_parts.append(f"\n{'='*60}\n")
            response_parts.append(f"{doctrine.topic.replace('_', ' ').upper()}\n")
            response_parts.append(f"{'='*60}\n\n")
            response_parts.append(f"CONCLUSION:\n{' '.join(doctrine.conclusion_template)}\n\n")
            response_parts.append(f"REASONING:\n{doctrine.reasoning_framework}\n\n")
            response_parts.append(f"KEY FACTORS:\n")
            for factor in doctrine.key_factors:
                response_parts.append(f"  - {factor}\n")
            response_parts.append(f"\nPRIMARY AUTHORITY:\n")
            for auth in doctrine.primary_authority:
                response_parts.append(f"  - {auth}\n")
            response_parts.append(f"\nBURDEN: {doctrine.burden_holder}\n")
            response_parts.append(f"ADVERSARY POSITION: {doctrine.adversary_position}\n\n")
            response_parts.append(f"COUNTER-ARGUMENTS:\n")
            for counter in doctrine.counter_arguments:
                response_parts.append(f"  - {counter}\n")
            response_parts.append(f"\nRESOLUTION STRATEGY:\n{doctrine.resolution_strategy}\n\n")
            response_parts.append(f"CONFIDENCE: {doctrine.confidence_stratification}\n")
            authorities.extend(doctrine.primary_authority)
            reasoning.append(doctrine.reasoning_framework)

        response_parts.append(f"\n{'='*60}\n")
        response_parts.append("EPISTEMIC GUARDRAILS:\n")
        response_parts.append(f"{'='*60}\n")
        for guardrail in EPISTEMIC_GUARDRAILS[:5]:
            response_parts.append(f"  - {guardrail}\n")

        response = "".join(response_parts)
        confidence = doctrines[0].confidence.value if doctrines else ConfidenceLevel.DISCLOSURE.value

    response = apply_epistemic_guardrails(response)
    return response, authorities, reasoning, confidence

def compute_determinism_hash(query: str, response: str) -> str:
    content = f"{query}::{response}".encode('utf-8')
    return hashlib.sha256(content).hexdigest()

app = FastAPI(title=ENGINE_NAME, version=VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info(f"{ENGINE_NAME} v{VERSION} starting on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")

@app.get("/health", response_model=HealthResponse)
async def health():
    uptime = time.time() - START_TIME
    return HealthResponse(
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        version=VERSION,
        status="operational",
        port=PORT,
        doctrine_blocks=len(DOCTRINE_CACHE),
        uptime_seconds=round(uptime, 2),
        timestamp=datetime.utcnow().isoformat()
    )

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    start = time.time()

    response_text, authorities, reasoning, confidence = three_layer_response(
        request.query, request.mode, request.context
    )

    issues = [d.topic for d in search_doctrines(request.query, limit=5)]

    determinism = compute_determinism_hash(request.query, response_text)
    latency = (time.time() - start) * 1000

    logger.info(f"Query processed in {latency:.2f}ms, mode={request.mode}, issues={len(issues)}")

    return QueryResponse(
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        version=VERSION,
        query=request.query,
        mode=request.mode.value,
        response=response_text,
        confidence=confidence,
        authorities=authorities,
        reasoning_chain=reasoning,
        issues_detected=issues,
        determinism_hash=determinism,
        latency_ms=round(latency, 2),
        timestamp=datetime.utcnow().isoformat()
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
