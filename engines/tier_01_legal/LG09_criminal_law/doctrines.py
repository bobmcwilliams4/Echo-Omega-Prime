"""
LG09 Criminal Law Engine - Doctrine Cache
==========================================
Pre-loaded criminal law doctrine blocks covering federal and Texas state
criminal law. Each block contains: topic, summary, key_statutes, elements,
defenses, remedies, and leading_cases.

Coverage:
    - Elements of crimes (actus reus, mens rea, concurrence, causation)
    - Homicide (murder degrees, manslaughter, capital, felony murder)
    - Assault and battery (simple, aggravated, domestic)
    - Property crimes (theft, burglary, robbery, arson, fraud)
    - Drug offenses (scheduling, possession, distribution, trafficking)
    - White collar (embezzlement, money laundering, RICO, securities fraud)
    - Constitutional protections (4th/5th/6th/8th Amendments)
    - Search and seizure (warrant, exceptions, exclusionary rule)
    - Miranda rights and custodial interrogation
    - Sentencing guidelines (federal, Texas, mandatory minimums)
    - Defenses (self-defense, insanity, duress, entrapment, necessity)
    - Texas Penal Code specifics
    - Title 18 USC federal crimes
    - Juvenile justice
    - Inchoate offenses (attempt, conspiracy, solicitation)

Author: ECHO OMEGA PRIME
Engine: LG09 Criminal Law
"""

from __future__ import annotations

import hashlib
import json
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from loguru import logger


# =============================================================================
# DOCTRINE BLOCK MODEL
# =============================================================================

@dataclass
class DoctrineBlock:
    """A single doctrine cache entry with structured criminal law content."""
    topic: str
    summary: str
    key_statutes: List[str]
    elements: List[str]
    defenses: List[str]
    remedies: List[str]
    leading_cases: List[str]
    jurisdiction: str = "federal"
    category: str = "general"
    severity: str = "felony"
    notes: str = ""

    @property
    def cache_key(self) -> str:
        """Generate deterministic cache key from topic."""
        return f"{self.category}.{self.topic.lower().replace(' ', '_')}"

    @property
    def content_hash(self) -> str:
        """SHA-256 hash of the doctrine content for determinism checks."""
        content = json.dumps({
            "topic": self.topic,
            "summary": self.summary,
            "key_statutes": self.key_statutes,
            "elements": self.elements,
            "defenses": self.defenses,
            "remedies": self.remedies,
            "leading_cases": self.leading_cases,
        }, sort_keys=True)
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    @property
    def searchable_text(self) -> str:
        """Flattened text for search indexing."""
        parts = [
            self.topic,
            self.summary,
            " ".join(self.key_statutes),
            " ".join(self.elements),
            " ".join(self.defenses),
            " ".join(self.remedies),
            " ".join(self.leading_cases),
            self.notes,
        ]
        return " ".join(parts)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "topic": self.topic,
            "summary": self.summary,
            "key_statutes": self.key_statutes,
            "elements": self.elements,
            "defenses": self.defenses,
            "remedies": self.remedies,
            "leading_cases": self.leading_cases,
            "jurisdiction": self.jurisdiction,
            "category": self.category,
            "severity": self.severity,
            "notes": self.notes,
            "cache_key": self.cache_key,
            "content_hash": self.content_hash,
        }


# =============================================================================
# ELEMENTS OF CRIME DOCTRINES
# =============================================================================

ELEMENTS_OF_CRIME_DOCTRINES: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Actus Reus",
        summary=(
            "Actus reus is the physical element of a crime, requiring a voluntary act or "
            "an unlawful omission when there is a legal duty to act. The act must be conscious "
            "and volitional; reflexive or unconscious movements do not satisfy the requirement. "
            "Under MPC Section 2.01, a bodily movement that is not a product of the effort or "
            "determination of the actor is not a voluntary act. Omissions qualify only where a "
            "duty arises by statute, contract, relationship, voluntary assumption of care, or "
            "creation of peril."
        ),
        key_statutes=["MPC Section 2.01", "Texas Penal Code Section 6.01", "18 USC General Principles"],
        elements=[
            "Voluntary bodily movement or conscious act",
            "Omission where legal duty to act exists",
            "Act must be product of conscious effort or determination",
            "Mere status or condition is insufficient (Robinson v California)",
            "Possession counts if aware of possession for sufficient period",
        ],
        defenses=[
            "Involuntary act (seizure, reflex, unconsciousness)",
            "Automatism (sleepwalking, hypnotic state)",
            "No legal duty to act (for omission-based charges)",
            "Duress negating voluntariness",
        ],
        remedies=[
            "Acquittal if actus reus not proven beyond reasonable doubt",
            "Directed verdict of acquittal",
            "Reduction of charge if lesser act proven",
        ],
        leading_cases=[
            "Robinson v California (1962) — Status crimes unconstitutional",
            "Martin v State (1944) — Involuntary public appearance",
            "People v Newton (1970) — Unconscious act not voluntary",
            "Jones v United States (1962) — Legal duty for omissions",
            "Pope v State (1979) — Limits of omission liability",
        ],
        jurisdiction="federal",
        category="elements_of_crime",
        severity="general",
        notes="Foundation element required for all criminal offenses. Prosecution must prove voluntary act.",
    ),
    DoctrineBlock(
        topic="Mens Rea",
        summary=(
            "Mens rea is the mental element of a crime — the guilty mind. The MPC recognizes four "
            "levels of culpability in descending order: purposely (conscious object to engage in "
            "conduct or cause result), knowingly (awareness that conduct is of a particular nature "
            "or that a circumstance exists), recklessly (conscious disregard of a substantial and "
            "unjustifiable risk), and negligently (should be aware of a substantial and unjustifiable "
            "risk). Common law distinguished between specific intent and general intent crimes. "
            "Strict liability offenses require no mens rea for at least one element."
        ),
        key_statutes=[
            "MPC Section 2.02", "Texas Penal Code Section 6.02", "Texas Penal Code Section 6.03",
            "Morissette v United States (1952) — Presumption of mens rea",
        ],
        elements=[
            "Purposely: conscious object to engage in conduct or cause result",
            "Knowingly: aware conduct is of particular nature or circumstance exists",
            "Recklessly: conscious disregard of substantial and unjustifiable risk",
            "Negligently: should be aware of substantial and unjustifiable risk",
            "Transferred intent: intent transfers to unintended victim",
            "Willful blindness: deliberate avoidance of knowledge equals knowledge",
        ],
        defenses=[
            "Mistake of fact negating required mental state",
            "Involuntary intoxication negating mens rea",
            "Diminished capacity (where recognized)",
            "Insanity (complete defense to mens rea)",
        ],
        remedies=[
            "Acquittal if prosecution fails to prove required mental state",
            "Reduction to lesser included offense with lower mens rea",
            "Jury instruction on lesser mental state",
        ],
        leading_cases=[
            "Morissette v United States (1952) — Presumption of mens rea requirement",
            "Staples v United States (1994) — Mens rea for regulatory offenses",
            "Elonis v United States (2015) — Subjective intent for true threats",
            "Global-Tech Appliances v SEB SA (2011) — Willful blindness standard",
            "Carter v United States (2000) — Mens rea default under federal law",
        ],
        jurisdiction="federal",
        category="elements_of_crime",
        severity="general",
        notes="Every element of an offense must have a corresponding culpability level unless strict liability applies.",
    ),
    DoctrineBlock(
        topic="Concurrence",
        summary=(
            "The concurrence requirement demands that the mens rea and actus reus coincide in "
            "time. The defendant must possess the required mental state at the time of the "
            "criminal act. A later-formed intent does not satisfy this element. The doctrine of "
            "continuing trespass or continuing act may extend the temporal window in some "
            "jurisdictions to cover situations where mens rea forms during an ongoing act."
        ),
        key_statutes=["MPC Section 2.02(1)", "Common Law Principle"],
        elements=[
            "Mental state must exist at time of physical act",
            "Temporal overlap between mens rea and actus reus",
            "Continuing act doctrine may extend the temporal window",
            "Motivation is distinct from intent — motive alone insufficient",
        ],
        defenses=[
            "Afterthought defense — intent formed after act completed",
            "Temporal disconnect between mental state and act",
        ],
        remedies=[
            "Acquittal if concurrence not proven",
            "Reduction to attempt if act preceded intent formation",
        ],
        leading_cases=[
            "People v Henson (1957) — Temporal concurrence required",
            "Fagan v Metropolitan Police (1969) — Continuing act doctrine",
            "Thabo Meli v R (1954) — Transaction theory of concurrence",
            "State v Rose (1973) — Continuing omission satisfies concurrence",
        ],
        jurisdiction="federal",
        category="elements_of_crime",
        severity="general",
    ),
    DoctrineBlock(
        topic="Causation",
        summary=(
            "Causation connects the defendant's act to the criminal result. Two types must be "
            "proven: actual cause (but-for causation) and proximate cause (legal causation). "
            "But-for: the result would not have occurred but for the defendant's act. Proximate "
            "cause limits liability to foreseeable consequences and considers whether intervening "
            "causes break the causal chain. Under MPC Section 2.03, the result must not be too "
            "remote or accidental to have a just bearing on the actor's liability."
        ),
        key_statutes=["MPC Section 2.03", "Common Law Proximate Cause Doctrine"],
        elements=[
            "But-for causation: result would not have occurred absent defendant's act",
            "Proximate cause: result is a natural and probable consequence of the act",
            "Substantial factor test for concurrent causes",
            "Intervening cause analysis (dependent vs independent)",
            "Superseding cause breaks the causal chain if unforeseeable",
        ],
        defenses=[
            "Intervening superseding cause (unforeseeable third-party act)",
            "Pre-existing condition as sole cause",
            "Victim's own conduct as superseding cause",
            "Act of God or natural disaster",
        ],
        remedies=[
            "Acquittal if causation chain broken",
            "Reduction to lesser offense (e.g., assault instead of murder)",
        ],
        leading_cases=[
            "People v Acosta (1991) — Foreseeability in proximate cause",
            "People v Arzon (1978) — Concurrent causation with fire",
            "People v Warner-Lambert Co (1980) — Foreseeability limits",
            "Velazquez v State (1990) — Victim conduct as intervening cause",
            "State v Preslar (1856) — Victim's voluntary act as superseding",
        ],
        jurisdiction="federal",
        category="elements_of_crime",
        severity="general",
    ),
    DoctrineBlock(
        topic="Strict Liability",
        summary=(
            "Strict liability offenses require no mens rea for one or more elements. The prosecution "
            "need only prove the actus reus. These typically involve regulatory or public welfare "
            "offenses where the social harm justifies eliminating the mental state requirement. "
            "Statutory rape is the classic example in traditional criminal law. The Supreme Court "
            "has held that strict liability is disfavored for serious offenses and courts should "
            "presume a mens rea requirement unless Congress clearly intended otherwise."
        ),
        key_statutes=[
            "MPC Section 2.05", "United States v Balint (1922)",
            "Morissette v United States (1952)", "Staples v United States (1994)",
        ],
        elements=[
            "No mental state required for at least one element",
            "Typically applies to public welfare and regulatory offenses",
            "Prosecution must still prove actus reus beyond reasonable doubt",
            "Mistake of fact is generally not a defense",
        ],
        defenses=[
            "Constitutional challenge (due process for serious penalties)",
            "Legislative intent argument (statute intended mens rea)",
            "Impossibility of compliance",
        ],
        remedies=[
            "Challenge classification as strict liability",
            "Argue statute requires implicit mens rea per Morissette",
        ],
        leading_cases=[
            "United States v Balint (1922) — Public welfare offense doctrine",
            "Morissette v United States (1952) — Presumption against strict liability",
            "Staples v United States (1994) — Firearms require knowledge",
            "United States v Dotterweich (1943) — Corporate strict liability",
            "Garnett v State (1993) — Statutory rape as strict liability",
        ],
        jurisdiction="federal",
        category="elements_of_crime",
        severity="general",
    ),
]


# =============================================================================
# HOMICIDE DOCTRINES
# =============================================================================

HOMICIDE_DOCTRINES: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Capital Murder",
        summary=(
            "Capital murder is the most serious homicide offense, eligible for the death penalty "
            "or life without parole. Under Texas Penal Code Section 19.03, capital murder includes "
            "murder of a peace officer or firefighter, murder during commission of enumerated "
            "felonies (kidnapping, burglary, robbery, aggravated sexual assault, arson, obstruction "
            "or retaliation, terroristic threat), murder for hire, murder while incarcerated for "
            "murder or capital murder, murder of a child under 10, and multiple murders in a "
            "single transaction. Federal capital offenses include treason, espionage, and certain "
            "drug-related killings under 18 USC 3591."
        ),
        key_statutes=[
            "Texas Penal Code Section 19.03", "18 USC 3591 (Federal Death Penalty Act)",
            "18 USC 1111 (Federal Murder)", "21 USC 848(e) (Drug Kingpin Act)",
        ],
        elements=[
            "Intentional or knowing killing (base murder element)",
            "Plus one or more statutory aggravating factors",
            "Specific enumerated victims (peace officer, child under 10, judge)",
            "Murder during commission of enumerated felony",
            "Murder for remuneration or promise of remuneration",
            "Multiple murders in single criminal transaction",
        ],
        defenses=[
            "Lack of intent or knowledge (negating mens rea)",
            "Alibi or misidentification",
            "Mitigation evidence (for sentencing phase, not guilt)",
            "Intellectual disability (Atkins v Virginia bars execution)",
            "Age under 18 at time of offense (Roper v Simmons bars execution)",
        ],
        remedies=[
            "Death penalty (after bifurcated trial with penalty phase)",
            "Life without parole (Texas: automatic if death not imposed)",
            "Appeal to Court of Criminal Appeals (direct appeal)",
            "Federal habeas corpus under 28 USC 2254",
        ],
        leading_cases=[
            "Furman v Georgia (1972) — Arbitrary death penalty unconstitutional",
            "Gregg v Georgia (1976) — Guided discretion death penalty constitutional",
            "Atkins v Virginia (2002) — Cannot execute intellectually disabled",
            "Roper v Simmons (2005) — Cannot execute juveniles",
            "Kennedy v Louisiana (2008) — Death penalty limited to homicide offenses",
            "Penry v Lynaugh (1989) — Mitigating evidence in capital cases",
        ],
        jurisdiction="texas",
        category="homicide",
        severity="capital_felony",
    ),
    DoctrineBlock(
        topic="First Degree Murder",
        summary=(
            "First degree murder requires premeditation and deliberation in addition to the intent "
            "to kill. The defendant must have formed the intent to kill before the act and had "
            "time to reflect on the decision, however brief. Under federal law (18 USC 1111), "
            "murder is killing with malice aforethought; first degree encompasses premeditated "
            "killing, felony murder, and killing by poison, lying in wait, or other willful and "
            "deliberate means. Texas does not use the 'degrees' system — instead, murder is "
            "codified under TPC Section 19.02 with capital murder as the highest category."
        ),
        key_statutes=[
            "18 USC 1111", "MPC Section 210.2", "Texas Penal Code Section 19.02",
        ],
        elements=[
            "Intent to kill (express malice)",
            "Premeditation: formation of intent before the act",
            "Deliberation: cool reflection on the decision to kill",
            "No specific time period required — can be instantaneous in some jurisdictions",
            "Malice aforethought (express or implied)",
        ],
        defenses=[
            "Lack of premeditation (reduction to second degree or manslaughter)",
            "Heat of passion (reduction to voluntary manslaughter)",
            "Self-defense or defense of others",
            "Insanity defense",
            "Diminished capacity (where recognized)",
            "Intoxication negating specific intent (voluntary in some jurisdictions)",
        ],
        remedies=[
            "Life imprisonment or life without parole",
            "Mandatory minimum sentencing in many jurisdictions",
            "Federal sentencing guidelines Chapter 2A1.1",
        ],
        leading_cases=[
            "People v Anderson (1968) — Three factors for premeditation",
            "Midgett v State (1987) — Premeditation requires cool reflection",
            "State v Guthrie (1995) — Some prior calculation and design",
            "United States v Watson (1979) — Federal first degree murder elements",
        ],
        jurisdiction="federal",
        category="homicide",
        severity="first_degree_felony",
    ),
    DoctrineBlock(
        topic="Second Degree Murder",
        summary=(
            "Second degree murder is an intentional killing without premeditation and deliberation, "
            "or a killing resulting from conduct demonstrating a depraved indifference to human "
            "life (depraved heart murder). It encompasses situations where the defendant intended "
            "to cause serious bodily harm that resulted in death, or acted with extreme recklessness "
            "creating a grave risk of death. Under MPC Section 210.2(1)(b), murder committed "
            "recklessly under circumstances manifesting extreme indifference to human life."
        ),
        key_statutes=["18 USC 1111", "MPC Section 210.2(1)(b)"],
        elements=[
            "Intent to kill without premeditation, OR",
            "Intent to cause serious bodily harm resulting in death, OR",
            "Depraved heart: extreme recklessness showing disregard for human life",
            "Implied malice aforethought",
            "No cooling-off or deliberation element",
        ],
        defenses=[
            "Heat of passion (reduce to voluntary manslaughter)",
            "Self-defense",
            "Lack of implied malice",
            "Intoxication negating awareness",
            "Accident or misadventure",
        ],
        remedies=[
            "Substantial prison term (typically 15 years to life)",
            "Federal sentencing guidelines apply",
        ],
        leading_cases=[
            "People v Knoller (2007) — Depraved heart dog mauling case",
            "Berry v Superior Court (1989) — Implied malice standard",
            "State v Davidson (1999) — Reckless murder elements",
            "United States v Fleming (1984) — Drunk driving as depraved heart",
        ],
        jurisdiction="federal",
        category="homicide",
        severity="second_degree_felony",
    ),
    DoctrineBlock(
        topic="Voluntary Manslaughter",
        summary=(
            "Voluntary manslaughter is an intentional killing committed in the heat of passion "
            "upon adequate provocation. The provocation must be such that a reasonable person "
            "would lose self-control, and the defendant must not have had sufficient time to "
            "cool off. Under Texas law (TPC 19.02(d)), a murder charge may be reduced to a "
            "second degree felony if the defendant acted under the immediate influence of "
            "sudden passion arising from an adequate cause. The defendant bears the burden "
            "of proving sudden passion by a preponderance at sentencing."
        ),
        key_statutes=[
            "MPC Section 210.3", "Texas Penal Code Section 19.02(d)",
            "18 USC 1112 (Federal Manslaughter)",
        ],
        elements=[
            "Intentional killing (would otherwise be murder)",
            "Adequate provocation by the victim",
            "Actual heat of passion in the defendant",
            "No reasonable cooling-off period elapsed",
            "Causal connection between provocation and killing",
        ],
        defenses=[
            "Complete self-defense (acquittal rather than reduction)",
            "Lack of intent (reduction to involuntary manslaughter)",
            "Provocation was inadequate as a matter of law",
        ],
        remedies=[
            "Second degree felony in Texas (2-20 years)",
            "Federal: up to 15 years under 18 USC 1112",
            "Significantly reduced from murder sentencing range",
        ],
        leading_cases=[
            "Girouard v State (1991) — Words alone insufficient provocation",
            "People v Berry (1976) — Long-simmering provocation theory",
            "Maher v People (1862) — Classic provocation analysis",
            "People v Casassa (1980) — MPC extreme emotional disturbance",
        ],
        jurisdiction="federal",
        category="homicide",
        severity="second_degree_felony",
    ),
    DoctrineBlock(
        topic="Involuntary Manslaughter",
        summary=(
            "Involuntary manslaughter is an unintentional killing resulting from criminal "
            "negligence or during the commission of an unlawful act not amounting to a felony "
            "(misdemeanor manslaughter). The defendant's conduct must represent a gross deviation "
            "from the standard of care that a reasonable person would exercise. Under Texas law, "
            "criminally negligent homicide (TPC 19.05) is a state jail felony involving a death "
            "caused by criminal negligence."
        ),
        key_statutes=[
            "18 USC 1112", "MPC Section 210.4", "Texas Penal Code Section 19.04",
            "Texas Penal Code Section 19.05",
        ],
        elements=[
            "Unintentional killing",
            "Criminal negligence: gross deviation from reasonable standard of care",
            "Or recklessness: conscious disregard of substantial risk (TPC 19.04)",
            "Causal connection between negligent/reckless act and death",
            "Misdemeanor manslaughter: death during unlawful act not a felony",
        ],
        defenses=[
            "Ordinary negligence (civil, not criminal)",
            "Unforeseeable intervening cause",
            "Contributory negligence of victim (limited applicability)",
            "Accident without criminal negligence",
        ],
        remedies=[
            "Federal: up to 8 years (18 USC 1112)",
            "Texas manslaughter (TPC 19.04): second degree felony (2-20 years)",
            "Texas criminally negligent homicide (TPC 19.05): state jail felony (180 days-2 years)",
        ],
        leading_cases=[
            "Commonwealth v Welansky (1944) — Gross negligence standard",
            "State v Williams (1971) — Parental duty and negligent homicide",
            "People v Datema (1995) — Reckless vs negligent distinction",
            "United States v Walker (2005) — Federal involuntary manslaughter",
        ],
        jurisdiction="federal",
        category="homicide",
        severity="felony",
    ),
    DoctrineBlock(
        topic="Felony Murder",
        summary=(
            "The felony murder rule imputes malice aforethought to a killing that occurs during "
            "the commission or attempted commission of a dangerous felony, regardless of the "
            "defendant's intent to kill. The underlying felony must be independent of the killing "
            "(merger doctrine). Most jurisdictions limit the rule to inherently dangerous felonies "
            "enumerated by statute. Co-felons may be liable for killings committed by accomplices "
            "during the felony under the agency theory or proximate cause theory. In Texas, "
            "capital murder includes murder committed during kidnapping, burglary, robbery, "
            "aggravated sexual assault, arson, obstruction, or terroristic threat."
        ),
        key_statutes=[
            "18 USC 1111", "Texas Penal Code Section 19.02(b)(3)",
            "Texas Penal Code Section 19.03(a)(2)", "MPC Section 210.2(1)(b)",
        ],
        elements=[
            "Commission or attempted commission of an enumerated felony",
            "Death occurs during the felony or immediate flight therefrom",
            "Causal connection between felony and death",
            "Merger doctrine: underlying felony must be independent of homicide",
            "Res gestae temporal requirement: death during the felony transaction",
        ],
        defenses=[
            "Felony was not inherently dangerous",
            "Merger doctrine (assault-based felony merges with homicide)",
            "Death occurred after felony was clearly completed",
            "Not a participant in the underlying felony",
            "Howard limitation: not a foreseeable consequence",
        ],
        remedies=[
            "First degree murder sentencing (life imprisonment)",
            "Capital murder if enumerated under TPC 19.03 (Texas)",
            "Co-felon liability extends to all participants",
        ],
        leading_cases=[
            "People v Stamp (1969) — Heart attack during robbery counted",
            "People v Burton (1971) — Merger doctrine articulated",
            "State v Sophophone (2001) — Agency vs proximate cause theory",
            "Tison v Arizona (1987) — Felony murder and death penalty",
            "Enmund v Florida (1982) — Minor participant and death penalty",
        ],
        jurisdiction="federal",
        category="homicide",
        severity="first_degree_felony",
    ),
]


# =============================================================================
# ASSAULT AND BATTERY DOCTRINES
# =============================================================================

ASSAULT_BATTERY_DOCTRINES: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Simple Assault",
        summary=(
            "Simple assault involves intentionally, knowingly, or recklessly causing bodily "
            "injury to another person, or threatening another with imminent bodily injury, or "
            "causing physical contact that the actor knows or should reasonably believe the "
            "victim will regard as offensive or provocative. Under Texas Penal Code Section "
            "22.01, simple assault is generally a Class A misdemeanor but may be enhanced "
            "based on victim status or defendant history."
        ),
        key_statutes=[
            "Texas Penal Code Section 22.01", "18 USC 113 (Federal Assault)",
            "MPC Section 211.1",
        ],
        elements=[
            "Intentionally, knowingly, or recklessly causing bodily injury, OR",
            "Intentionally or knowingly threatening imminent bodily injury, OR",
            "Intentionally or knowingly causing offensive physical contact",
            "Bodily injury: physical pain, illness, or any impairment of physical condition",
        ],
        defenses=[
            "Self-defense or defense of third person",
            "Consent (in limited circumstances, e.g., sports)",
            "Defense of property",
            "Accident without criminal negligence",
            "Lack of required mental state",
        ],
        remedies=[
            "Class A misdemeanor: up to 1 year jail, $4,000 fine (Texas)",
            "Class C misdemeanor if threat only or offensive contact (Texas)",
            "Enhanced to third degree felony for family violence with prior",
        ],
        leading_cases=[
            "Lane v State (2003) — Bodily injury definition in Texas",
            "United States v Juvenile Male (2010) — Federal assault elements",
            "Johnson v State (1997) — Offensive contact standard",
        ],
        jurisdiction="texas",
        category="assault_battery",
        severity="misdemeanor",
    ),
    DoctrineBlock(
        topic="Aggravated Assault",
        summary=(
            "Aggravated assault occurs when the defendant causes serious bodily injury to another "
            "or uses or exhibits a deadly weapon during an assault. Under Texas Penal Code Section "
            "22.02, aggravated assault is a second degree felony, enhanced to first degree when "
            "committed against a public servant, security officer, witness, informant, or in "
            "retaliation, or involving serious bodily injury in domestic violence context. "
            "Serious bodily injury means injury creating a substantial risk of death, serious "
            "permanent disfigurement, or protracted loss of function of any organ or body member."
        ),
        key_statutes=[
            "Texas Penal Code Section 22.02", "18 USC 113(a)(3) (Federal Aggravated Assault)",
            "Texas Penal Code Section 1.07(a)(46) (Serious Bodily Injury definition)",
        ],
        elements=[
            "Commission of an assault (TPC 22.01 elements), AND",
            "Causes serious bodily injury to another, OR",
            "Uses or exhibits a deadly weapon during the assault",
            "Deadly weapon: anything designed, made, or adapted to cause death or serious bodily injury",
            "Hands/feet can be deadly weapons depending on manner of use",
        ],
        defenses=[
            "Self-defense with proportional force",
            "Defense of third person",
            "Lack of serious bodily injury",
            "Object used was not a deadly weapon in context",
            "Mutual combat (limited defense, may reduce charge)",
        ],
        remedies=[
            "Second degree felony: 2-20 years, up to $10,000 fine (Texas)",
            "First degree felony if against public servant or with domestic violence SBI",
            "Deadly weapon finding affects parole eligibility",
        ],
        leading_cases=[
            "McCain v State (1986) — Hands as deadly weapons",
            "Turner v State (2003) — Deadly weapon finding and parole",
            "Laster v State (2009) — Serious bodily injury vs bodily injury",
            "Tucker v State (2006) — Exhibit vs use of deadly weapon",
        ],
        jurisdiction="texas",
        category="assault_battery",
        severity="second_degree_felony",
    ),
    DoctrineBlock(
        topic="Domestic Violence Assault",
        summary=(
            "Domestic violence assault involves an assault committed against a family member, "
            "household member, or someone with whom the defendant has or had a dating relationship. "
            "Texas takes family violence extremely seriously with progressive enhancement: a "
            "second family violence assault is a third degree felony, continuous family violence "
            "(two or more assaults in 12 months) under TPC 25.11 is a third degree felony, and "
            "strangulation or suffocation in family violence context is enhanced. Federal law "
            "prohibits firearm possession by persons convicted of misdemeanor domestic violence "
            "under 18 USC 922(g)(9)."
        ),
        key_statutes=[
            "Texas Penal Code Section 22.01(b)", "Texas Penal Code Section 25.11",
            "18 USC 922(g)(9) (Lautenberg Amendment)", "Violence Against Women Act (VAWA)",
        ],
        elements=[
            "All elements of assault (TPC 22.01)",
            "Victim is family member, household member, or dating partner",
            "Family member: related by blood, marriage, adoption, or foster",
            "Household member: living together currently or previously",
            "Dating relationship: continuing romantic or intimate relationship",
        ],
        defenses=[
            "Self-defense",
            "No family/dating relationship exists",
            "Injuries were accidental",
            "False accusation (common in custody disputes)",
            "Recanting witness (does not automatically defeat charge)",
        ],
        remedies=[
            "Class A misdemeanor for first offense (Texas)",
            "Third degree felony for second family violence conviction",
            "Third degree felony for continuous violence against family",
            "Federal firearms prohibition under Lautenberg Amendment",
            "Protective order and bond conditions",
        ],
        leading_cases=[
            "United States v Castleman (2014) — Misdemeanor crime of domestic violence",
            "Voisine v United States (2016) — Reckless domestic assault counts",
            "Ybarra v State (2011) — Dating relationship definition",
            "Hernandez v State (2014) — Continuous family violence elements",
        ],
        jurisdiction="texas",
        category="assault_battery",
        severity="misdemeanor_to_felony",
    ),
]


# =============================================================================
# PROPERTY CRIME DOCTRINES
# =============================================================================

PROPERTY_CRIME_DOCTRINES: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Theft",
        summary=(
            "Theft is the unlawful appropriation of property with intent to deprive the owner. "
            "Under Texas Penal Code Section 31.03, a person commits theft if they unlawfully "
            "appropriate property with intent to deprive the owner of the property. Appropriation "
            "is unlawful if without the owner's effective consent, or the property is stolen and "
            "the actor knows it was stolen. Severity ranges from Class C misdemeanor (under $100) "
            "to first degree felony ($300,000 or more). Federal theft includes interstate "
            "transportation of stolen property (18 USC 2314)."
        ),
        key_statutes=[
            "Texas Penal Code Section 31.03", "18 USC 2314 (Interstate Stolen Property)",
            "18 USC 641 (Theft of Government Property)",
        ],
        elements=[
            "Unlawful appropriation of property",
            "Intent to deprive the owner of the property",
            "Without effective consent of the owner",
            "Property includes real, personal, and intangible property",
            "Value determines offense level in Texas",
        ],
        defenses=[
            "Consent of the owner",
            "Claim of right (good faith belief of ownership)",
            "Lack of intent to permanently deprive",
            "Mistaken identity",
            "Value dispute (affects punishment level)",
        ],
        remedies=[
            "Class C misdemeanor: under $100 (Texas)",
            "Class B misdemeanor: $100-$750",
            "Class A misdemeanor: $750-$2,500",
            "State jail felony: $2,500-$30,000",
            "Third degree felony: $30,000-$150,000",
            "Second degree felony: $150,000-$300,000",
            "First degree felony: $300,000 or more",
            "Restitution to victim",
        ],
        leading_cases=[
            "McGee v State (2003) — Appropriation and intent elements",
            "Brooks v State (1990) — Effective consent doctrine",
            "Pratt v State (2011) — Aggregation of theft amounts",
            "United States v Morissette (1952) — Intent for theft offenses",
        ],
        jurisdiction="texas",
        category="property_crimes",
        severity="varies",
    ),
    DoctrineBlock(
        topic="Burglary",
        summary=(
            "Burglary involves entering a building or habitation without consent with the intent "
            "to commit a felony, theft, or assault inside. Under Texas Penal Code Section 30.02, "
            "burglary of a habitation is a second degree felony, enhanced to first degree if the "
            "defendant intended or committed another felony other than theft. Burglary of a building "
            "is a state jail felony. The entry need not be forced; entering through an open door "
            "without consent is sufficient. Common law burglary required breaking and entering of "
            "a dwelling at night, but modern statutes have largely eliminated these requirements."
        ),
        key_statutes=[
            "Texas Penal Code Section 30.02", "18 USC 2113 (Federal Bank Robbery/Burglary)",
            "MPC Section 221.1",
        ],
        elements=[
            "Entry into a building or habitation (or remaining concealed therein)",
            "Without effective consent of the owner",
            "With intent to commit a felony, theft, or assault therein",
            "Habitation: structure adapted for overnight accommodation",
            "Building: enclosed structure intended for business use",
            "Entry includes any part of the body crossing the threshold",
        ],
        defenses=[
            "Consent to enter",
            "No intent at time of entry (intent formed after lawful entry)",
            "Mistaken belief of consent",
            "Claim of right to be in premises",
        ],
        remedies=[
            "Burglary of habitation: second degree felony (2-20 years) Texas",
            "First degree if intent to commit felony other than theft (5-99 years)",
            "Burglary of building: state jail felony (180 days-2 years)",
            "Burglary of vehicle: Class A misdemeanor",
        ],
        leading_cases=[
            "Garcia v State (2004) — Entry element and partial intrusion",
            "Faulkner v State (2002) — Remaining concealed theory",
            "Miles v State (2015) — Intent at time of entry requirement",
            "People v Davis (1998) — Habitation vs building distinction",
        ],
        jurisdiction="texas",
        category="property_crimes",
        severity="second_degree_felony",
    ),
    DoctrineBlock(
        topic="Robbery and Aggravated Robbery",
        summary=(
            "Robbery is theft plus the use or threat of force against the victim. Under Texas "
            "Penal Code Section 29.02, robbery occurs when in the course of committing theft, "
            "the defendant intentionally, knowingly, or recklessly causes bodily injury or "
            "threatens or places another in fear of imminent bodily injury or death. Aggravated "
            "robbery (TPC 29.03) adds serious bodily injury, use or exhibition of a deadly "
            "weapon, or the victim being disabled or 65+. Aggravated robbery is a first degree "
            "felony punishable by 5-99 years or life."
        ),
        key_statutes=[
            "Texas Penal Code Section 29.02", "Texas Penal Code Section 29.03",
            "18 USC 1951 (Hobbs Act Robbery)", "18 USC 2113 (Bank Robbery)",
        ],
        elements=[
            "Commission of theft (TPC 31.03 elements)",
            "In the course of committing theft (during, attempt, or immediate flight)",
            "Intentionally, knowingly, or recklessly causes bodily injury, OR",
            "Threatens or places another in fear of imminent bodily injury or death",
            "Aggravated: plus SBI, deadly weapon, or vulnerable victim",
        ],
        defenses=[
            "No theft occurred (taking was lawful)",
            "No force or threat of force used",
            "Misidentification defense",
            "Duress (forced to participate)",
            "Intoxication negating specific intent",
        ],
        remedies=[
            "Robbery: second degree felony (2-20 years) Texas",
            "Aggravated robbery: first degree felony (5-99 years or life) Texas",
            "Federal bank robbery: up to 20 years (18 USC 2113)",
            "Hobbs Act: up to 20 years (18 USC 1951)",
        ],
        leading_cases=[
            "McGee v State (2009) — 'In the course of committing theft' timing",
            "Wolfe v State (2007) — Fear of imminent bodily injury standard",
            "Devoe v State (2012) — Deadly weapon in aggravated robbery",
            "United States v Taylor (2022) — Attempted Hobbs Act robbery",
        ],
        jurisdiction="texas",
        category="property_crimes",
        severity="first_degree_felony",
    ),
    DoctrineBlock(
        topic="Arson",
        summary=(
            "Arson is the intentional or knowing starting of a fire or causing an explosion with "
            "intent to destroy or damage property. Under Texas Penal Code Section 28.02, arson "
            "is a second degree felony, enhanced to first degree if bodily injury or death results, "
            "the property is a habitation or place of worship, or the fire is set with intent to "
            "collect insurance. Federal arson (18 USC 844) covers arson affecting interstate "
            "commerce. Reckless burning that endangers life is also criminal."
        ),
        key_statutes=[
            "Texas Penal Code Section 28.02", "18 USC 844(i) (Federal Arson)",
            "MPC Section 220.1",
        ],
        elements=[
            "Starting a fire or causing an explosion",
            "Intentionally or knowingly",
            "Damage or destruction of any building, habitation, or vehicle",
            "Or recklessly starting fire or explosion that endangers life/property",
            "Intent to destroy, damage, or collect insurance",
        ],
        defenses=[
            "Accidental fire (no criminal intent)",
            "Consent of property owner (limited — insurance fraud still applies)",
            "Arson investigator error in origin/cause determination",
            "Alibi",
        ],
        remedies=[
            "Second degree felony (2-20 years) Texas",
            "First degree felony if habitation, worship, or bodily injury",
            "Federal: 5-20 years, mandatory minimum if property used in interstate commerce",
            "Restitution for damage",
        ],
        leading_cases=[
            "Russell v United States (2005) — Owner-occupied arson",
            "Jones v United States (2000) — Federal arson jurisdiction limits",
            "Combs v State (2008) — Reckless arson elements in Texas",
        ],
        jurisdiction="texas",
        category="property_crimes",
        severity="second_degree_felony",
    ),
    DoctrineBlock(
        topic="Fraud General",
        summary=(
            "Fraud involves obtaining property, money, or services through intentional "
            "misrepresentation or deception. Federal fraud statutes are broadly applied: wire "
            "fraud (18 USC 1343) and mail fraud (18 USC 1341) require a scheme to defraud using "
            "wire communications or mail. Bank fraud (18 USC 1344) targets schemes to defraud "
            "financial institutions. Each carries up to 20 years (30 years if financial institution). "
            "Texas fraud offenses include securing execution of document by deception (TPC 32.46), "
            "insurance fraud (TPC 35.02), and Medicaid fraud."
        ),
        key_statutes=[
            "18 USC 1341 (Mail Fraud)", "18 USC 1343 (Wire Fraud)",
            "18 USC 1344 (Bank Fraud)", "Texas Penal Code Section 32.46",
        ],
        elements=[
            "Scheme or artifice to defraud",
            "Material misrepresentation or omission",
            "Intent to defraud",
            "Use of mail or wire communications (federal)",
            "Victim reliance on the misrepresentation",
            "Resulting loss to victim or gain to defendant",
        ],
        defenses=[
            "Good faith belief in truthfulness of statements",
            "No material misrepresentation",
            "Puffery or opinion vs factual misrepresentation",
            "Lack of intent to defraud",
            "Statute of limitations (5 years federal)",
        ],
        remedies=[
            "Federal: up to 20 years per count (30 years if financial institution victim)",
            "Fines up to $250,000 or $1,000,000 for organizations",
            "Mandatory restitution under 18 USC 3663A",
            "Forfeiture of proceeds",
        ],
        leading_cases=[
            "McNally v United States (1987) — Fraud limited to property rights",
            "Skilling v United States (2010) — Honest services fraud narrowed",
            "Neder v United States (1999) — Materiality element required",
            "Kelly v United States (2020) — Property fraud requires property",
            "Ciminelli v United States (2023) — Right-to-control theory rejected",
        ],
        jurisdiction="federal",
        category="property_crimes",
        severity="felony",
    ),
]


# =============================================================================
# DRUG OFFENSE DOCTRINES
# =============================================================================

DRUG_OFFENSE_DOCTRINES: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Controlled Substance Scheduling",
        summary=(
            "The Controlled Substances Act (21 USC 801 et seq.) classifies drugs into five "
            "schedules based on accepted medical use, potential for abuse, and dependence "
            "liability. Schedule I (highest restriction): no accepted medical use, high abuse "
            "potential (heroin, LSD, marijuana federally, peyote, MDMA). Schedule II: accepted "
            "medical use, high abuse potential (cocaine, methamphetamine, oxycodone, fentanyl). "
            "Schedule III: moderate abuse potential (anabolic steroids, ketamine). Schedule IV: "
            "low abuse potential (benzodiazepines, tramadol). Schedule V: lowest potential "
            "(cough medicines with codeine). Texas uses Penalty Groups 1-4 plus marijuana."
        ),
        key_statutes=[
            "21 USC 812 (Federal Scheduling)", "Texas Health and Safety Code Chapter 481",
            "21 CFR 1308 (Drug Scheduling Regulations)",
        ],
        elements=[
            "Schedule I: high abuse potential, no accepted medical use, unsafe even under supervision",
            "Schedule II: high abuse potential, accepted medical use, severe dependence risk",
            "Schedule III: moderate abuse potential, accepted medical use, moderate dependence",
            "Schedule IV: low abuse potential, accepted medical use, limited dependence",
            "Schedule V: lowest abuse potential, accepted medical use, limited dependence",
            "Texas Penalty Group 1 = most dangerous (heroin, cocaine, meth, fentanyl, oxycodone)",
            "Texas Penalty Group 2 = hallucinogens, THC concentrates, MDMA, PCP, amphetamines",
        ],
        defenses=[
            "Substance is not actually a controlled substance",
            "Scheduling challenge (constitutional or administrative law)",
            "Medical use authorization (prescription defense)",
            "Lab analysis error in identifying substance",
        ],
        remedies=[
            "Penalties vary dramatically based on schedule and quantity",
            "Schedule I/II carry heaviest penalties",
            "Mandatory minimums apply for trafficking quantities",
            "Scheduling affects both state and federal prosecution",
        ],
        leading_cases=[
            "Gonzales v Raich (2005) — Federal scheduling power over state laws",
            "Touby v United States (1991) — Emergency scheduling constitutional",
            "McFadden v United States (2015) — Knowledge requirement for analogue act",
        ],
        jurisdiction="federal",
        category="drug_offenses",
        severity="varies",
    ),
    DoctrineBlock(
        topic="Drug Possession",
        summary=(
            "Possession of a controlled substance requires proof that the defendant knowingly "
            "and intentionally possessed the substance. Possession can be actual (on person) "
            "or constructive (not on person but accessible with knowledge and control). Texas "
            "Health and Safety Code Section 481.115-481.121 grades possession by penalty group "
            "and quantity. The defendant must know the substance is contraband, though specific "
            "knowledge of the exact drug is not always required."
        ),
        key_statutes=[
            "21 USC 844 (Federal Simple Possession)", "Texas Health and Safety Code Section 481.115",
            "Texas Health and Safety Code Section 481.116-121",
        ],
        elements=[
            "The defendant exercised care, custody, control, or management over the substance",
            "The defendant knew the substance was contraband",
            "Actual possession (on person) or constructive possession (accessible with knowledge/control)",
            "Affirmative links connecting defendant to the substance (for constructive possession)",
            "Identity of substance as controlled substance (lab analysis typically required)",
        ],
        defenses=[
            "Lack of knowledge that substance was contraband",
            "No affirmative links to substance (constructive possession)",
            "Illegal search and seizure (suppression of evidence)",
            "Prescription defense (valid prescription for the substance)",
            "Entrapment",
            "Lab analysis challenge",
        ],
        remedies=[
            "Texas PG1 less than 1 gram: state jail felony (180 days-2 years)",
            "Texas PG1 1-4 grams: third degree felony (2-10 years)",
            "Texas PG1 4-200 grams: second degree felony (2-20 years)",
            "Texas PG1 200-400 grams: first degree felony (5-99 years)",
            "Federal simple possession first offense: up to 1 year",
            "Diversion programs may be available for first offenders",
        ],
        leading_cases=[
            "Poindexter v State (2006) — Affirmative links for constructive possession",
            "Evans v State (2001) — Knowledge of contraband nature required",
            "United States v Bailey (2020) — Constructive possession standard",
            "Dubry v State (2019) — Usable quantity requirement in Texas",
        ],
        jurisdiction="texas",
        category="drug_offenses",
        severity="varies",
    ),
    DoctrineBlock(
        topic="Drug Distribution and Trafficking",
        summary=(
            "Drug distribution involves the delivery, sale, or transfer of controlled substances. "
            "Trafficking adds quantity thresholds triggering enhanced penalties and mandatory "
            "minimums. Under 21 USC 841, it is unlawful to manufacture, distribute, or dispense "
            "a controlled substance. Texas Health and Safety Code Section 481.112 grades delivery "
            "of PG1 substances from state jail felony (under 1g) to life imprisonment (400g+). "
            "Federal mandatory minimums: 5 years for 5g crack or 500g powder cocaine, 10 years "
            "for 50g crack or 5kg powder cocaine."
        ),
        key_statutes=[
            "21 USC 841 (Federal Distribution)", "21 USC 846 (Federal Conspiracy)",
            "Texas Health and Safety Code Section 481.112",
            "Fair Sentencing Act of 2010", "First Step Act of 2018",
        ],
        elements=[
            "Knowing and intentional delivery, distribution, or dispensing",
            "Of a controlled substance",
            "Delivery includes actual transfer, constructive transfer, or offer to sell",
            "Trafficking: distribution plus quantity meeting statutory threshold",
            "Federal conspiracy: agreement plus overt act",
            "Drug quantity determines mandatory minimum exposure",
        ],
        defenses=[
            "Lack of knowledge of substance identity",
            "Mere presence at scene of drug transaction",
            "Buyer-seller relationship (may negate conspiracy)",
            "Entrapment (government inducement)",
            "Sentencing safety valve (10 USC 3553(f)) for minimal participants",
        ],
        remedies=[
            "Federal: 5-year mandatory minimum for lower quantity threshold",
            "Federal: 10-year mandatory minimum for higher quantity threshold",
            "Federal: life maximum for large quantities",
            "Texas delivery PG1 400g+: 10-99 years or life, $100,000 fine",
            "Drug-free zone enhancement adds additional penalties",
            "Asset forfeiture under 21 USC 853",
        ],
        leading_cases=[
            "Apprendi v New Jersey (2000) — Drug quantity must be found by jury",
            "Alleyne v United States (2013) — Mandatory minimum facts to jury",
            "United States v Booker (2005) — Advisory guidelines",
            "Dorsey v United States (2012) — Fair Sentencing Act retroactivity",
            "Terry v United States (2021) — First Step Act crack cocaine",
        ],
        jurisdiction="federal",
        category="drug_offenses",
        severity="felony",
    ),
]


# =============================================================================
# WHITE COLLAR CRIME DOCTRINES
# =============================================================================

WHITE_COLLAR_DOCTRINES: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Embezzlement",
        summary=(
            "Embezzlement is the fraudulent conversion of property by a person who was entrusted "
            "with that property. Unlike theft, the initial possession is lawful — the crime occurs "
            "when the entrusted person converts the property to their own use. Under federal law, "
            "bank employee embezzlement is covered by 18 USC 656 (up to 30 years), government "
            "embezzlement by 18 USC 641 (up to 10 years). Texas prosecutes under general theft "
            "statute TPC 31.03 with fiduciary relationship as an aggravating factor."
        ),
        key_statutes=[
            "18 USC 656 (Bank Embezzlement)", "18 USC 641 (Government Property)",
            "18 USC 666 (Federal Program Fraud)", "Texas Penal Code Section 31.03",
        ],
        elements=[
            "Lawful possession or custody of property belonging to another",
            "Fiduciary, employment, or entrustment relationship",
            "Fraudulent conversion or appropriation to personal use",
            "Intent to deprive the rightful owner",
        ],
        defenses=[
            "Claim of right (good faith belief property belonged to defendant)",
            "Authorization for the expenditure",
            "Intent to return (sometimes reduces culpability)",
            "Statute of limitations",
        ],
        remedies=[
            "Federal bank embezzlement: up to 30 years, $1M fine",
            "Federal government property: up to 10 years",
            "Texas: punishment based on value under theft statute",
            "Mandatory restitution",
            "Professional license revocation",
        ],
        leading_cases=[
            "United States v Rybicki (2002) — Bank embezzlement intent",
            "Morissette v United States (1952) — Conversion requires intent",
            "United States v Sabri (2004) — Federal program fraud scope",
        ],
        jurisdiction="federal",
        category="fraud_white_collar",
        severity="felony",
    ),
    DoctrineBlock(
        topic="Money Laundering",
        summary=(
            "Money laundering involves conducting financial transactions with proceeds known to "
            "be derived from unlawful activity with the intent to promote the unlawful activity, "
            "conceal the nature or source of the proceeds, or avoid reporting requirements. "
            "18 USC 1956 criminalizes transaction laundering (up to 20 years), while 18 USC 1957 "
            "criminalizes spending over $10,000 of criminal proceeds (up to 10 years). The Bank "
            "Secrecy Act (31 USC 5324) separately criminalizes structuring transactions to avoid "
            "reporting thresholds."
        ),
        key_statutes=[
            "18 USC 1956 (Transaction Laundering)", "18 USC 1957 (Spending Criminal Proceeds)",
            "31 USC 5324 (Structuring)", "31 USC 5322 (BSA Penalties)",
        ],
        elements=[
            "Financial transaction involving proceeds of specified unlawful activity",
            "Knowledge that proceeds are from unlawful activity",
            "Intent to promote SUA, conceal nature/source, or avoid reporting (1956)",
            "Or knowingly engaging in transaction over $10,000 from criminal proceeds (1957)",
            "Structuring: breaking transactions to stay under $10,000 CTR threshold",
        ],
        defenses=[
            "Legitimate source of funds",
            "No knowledge funds were criminally derived",
            "Government sting (proceeds not actually criminal — circuit split)",
            "Merger with underlying crime (some circuits)",
            "Statute of limitations (5 years)",
        ],
        remedies=[
            "18 USC 1956: up to 20 years per count",
            "18 USC 1957: up to 10 years per count",
            "Fine up to $500,000 or twice the amount laundered",
            "Asset forfeiture of all property involved in or traceable to offense",
            "Structuring: up to 5 years plus forfeiture of structured funds",
        ],
        leading_cases=[
            "United States v Santos (2008) — 'Proceeds' means profits, not gross receipts",
            "Cuellar v United States (2008) — Concealment purpose requirement",
            "Ratzlaf v United States (1994) — Structuring requires willfulness",
            "United States v Halk (2016) — Knowledge standard for laundering",
        ],
        jurisdiction="federal",
        category="fraud_white_collar",
        severity="felony",
    ),
    DoctrineBlock(
        topic="RICO",
        summary=(
            "The Racketeer Influenced and Corrupt Organizations Act (18 USC 1961-1968) targets "
            "patterns of racketeering activity connected to enterprises. RICO requires proof that "
            "the defendant conducted or participated in the affairs of an enterprise through a "
            "pattern of racketeering activity (at least two predicate acts within 10 years that "
            "are related and constitute a continuing threat). Predicate acts include murder, "
            "robbery, extortion, drug trafficking, fraud, gambling, bribery, and many other "
            "offenses. RICO conspiracy (1962(d)) does not require completion of predicate acts."
        ),
        key_statutes=[
            "18 USC 1961 (Definitions)", "18 USC 1962 (Prohibited Activities)",
            "18 USC 1963 (Criminal Penalties)", "18 USC 1964 (Civil Remedies)",
        ],
        elements=[
            "Existence of an enterprise (association-in-fact or legal entity)",
            "Defendant's association with or conduct of enterprise affairs",
            "Pattern of racketeering activity (2+ predicate acts in 10 years)",
            "Predicate acts must be related and pose continuing threat",
            "Nexus between enterprise and racketeering pattern",
        ],
        defenses=[
            "No enterprise exists",
            "Predicate acts are unrelated (no pattern)",
            "No continuing threat of racketeering (closed-ended)",
            "Withdrawal from conspiracy before limitations period",
            "RICO does not apply to the particular conduct",
        ],
        remedies=[
            "Up to 20 years per count (life if predicate carries life)",
            "Mandatory forfeiture of interest in enterprise and proceeds",
            "Treble damages in civil RICO (18 USC 1964(c))",
            "Pretrial restraining order on assets",
        ],
        leading_cases=[
            "Boyle v United States (2009) — Association-in-fact enterprise",
            "Reves v Ernst & Young (1993) — Conduct or participate in operations",
            "H.J. Inc v Northwestern Bell (1989) — Pattern of racketeering",
            "Sedima v Imrex (1985) — Civil RICO standing",
            "Turkette v United States (1981) — Enterprise includes illegal organizations",
        ],
        jurisdiction="federal",
        category="fraud_white_collar",
        severity="felony",
    ),
    DoctrineBlock(
        topic="Securities Fraud and Insider Trading",
        summary=(
            "Securities fraud encompasses schemes to defraud investors through material "
            "misrepresentations or omissions in connection with the purchase or sale of securities. "
            "Insider trading is buying or selling securities based on material nonpublic information "
            "in breach of a duty of trust or confidence. Under the classical theory, corporate "
            "insiders breach their fiduciary duty to shareholders. Under the misappropriation "
            "theory, outsiders breach a duty owed to the source of information. SEC Rule 10b-5 "
            "is the primary enforcement vehicle."
        ),
        key_statutes=[
            "15 USC 78j(b) (Securities Exchange Act Section 10(b))",
            "17 CFR 240.10b-5 (Rule 10b-5)",
            "18 USC 1348 (Securities Fraud)", "15 USC 78ff (Criminal Penalties)",
        ],
        elements=[
            "Material misrepresentation or omission (fraud), OR",
            "Trading on material nonpublic information (insider trading)",
            "In connection with purchase or sale of securities",
            "Scienter (intent to deceive, manipulate, or defraud)",
            "Breach of fiduciary duty or duty of trust and confidence (insider trading)",
            "Materiality: reasonable investor would consider important",
        ],
        defenses=[
            "No material misrepresentation",
            "Information was public at time of trade",
            "No duty of trust or confidence (outsider with no relationship)",
            "10b5-1 trading plan (affirmative defense for insider trading)",
            "Good faith reliance on counsel",
            "Lack of scienter",
        ],
        remedies=[
            "Criminal: up to 20 years under 18 USC 1348",
            "SEC civil penalties up to three times profit gained or loss avoided",
            "Disgorgement of profits",
            "Industry bars and officer/director bars",
            "Private securities fraud class actions",
        ],
        leading_cases=[
            "SEC v Texas Gulf Sulphur (1968) — Classical insider trading theory",
            "Chiarella v United States (1980) — Duty requirement",
            "Dirks v SEC (1983) — Tipper-tippee liability",
            "United States v O'Hagan (1997) — Misappropriation theory",
            "Salman v United States (2016) — Personal benefit for tippers",
            "United States v Martoma (2018) — Insider trading in hedge funds",
        ],
        jurisdiction="federal",
        category="fraud_white_collar",
        severity="felony",
    ),
]


# =============================================================================
# CONSTITUTIONAL RIGHTS DOCTRINES
# =============================================================================

CONSTITUTIONAL_DOCTRINES: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Fourth Amendment Search and Seizure",
        summary=(
            "The Fourth Amendment protects against unreasonable searches and seizures and requires "
            "warrants be issued upon probable cause, supported by oath, particularly describing "
            "the place to be searched and persons or things to be seized. A search occurs when the "
            "government violates a person's reasonable expectation of privacy (Katz test) or "
            "physically trespasses on a constitutionally protected area (Jones). The warrant "
            "requirement is the default, with recognized exceptions including consent, search "
            "incident to arrest, automobile, plain view, exigent circumstances, inventory, and "
            "Terry stop and frisk."
        ),
        key_statutes=[
            "U.S. Constitution, Fourth Amendment",
            "Federal Rules of Criminal Procedure Rule 41",
            "Texas Constitution Article I, Section 9",
            "Texas Code of Criminal Procedure Chapter 18",
        ],
        elements=[
            "Government action (state actor requirement)",
            "Search: violation of reasonable expectation of privacy or physical trespass",
            "Seizure of person: reasonable person would not feel free to leave",
            "Seizure of property: meaningful interference with possessory interest",
            "Warrant: probable cause, particularity, neutral magistrate, oath",
        ],
        defenses=[
            "Evidence obtained in violation of Fourth Amendment excluded (exclusionary rule)",
            "Fruit of the poisonous tree doctrine",
            "Standing requirement (defendant's own rights must be violated)",
        ],
        remedies=[
            "Exclusionary rule: illegally obtained evidence suppressed",
            "Fruit of the poisonous tree: derivative evidence also suppressed",
            "42 USC 1983 civil suit for damages against officers",
            "Bivens action against federal officers",
        ],
        leading_cases=[
            "Katz v United States (1967) — Reasonable expectation of privacy test",
            "United States v Jones (2012) — Physical trespass theory revived",
            "Mapp v Ohio (1961) — Exclusionary rule applies to states",
            "Carpenter v United States (2018) — Cell phone location data",
            "Riley v California (2014) — Cell phone search requires warrant",
            "Terry v Ohio (1968) — Stop and frisk on reasonable suspicion",
        ],
        jurisdiction="federal",
        category="constitutional_rights",
        severity="constitutional",
    ),
    DoctrineBlock(
        topic="Fifth Amendment Self-Incrimination and Miranda",
        summary=(
            "The Fifth Amendment protects against compelled self-incrimination. Miranda v Arizona "
            "(1966) requires that before custodial interrogation, officers must inform suspects of "
            "their rights: right to remain silent, anything said can be used against them, right "
            "to an attorney, and right to appointed counsel if unable to afford one. Custody means "
            "a reasonable person would not feel free to leave. Interrogation means express "
            "questioning or functional equivalent. Miranda rights may be waived if the waiver "
            "is knowing, voluntary, and intelligent."
        ),
        key_statutes=[
            "U.S. Constitution, Fifth Amendment",
            "Miranda v Arizona (1966)", "18 USC 3501",
            "Texas Code of Criminal Procedure Article 38.22",
        ],
        elements=[
            "Custodial interrogation (custody + interrogation)",
            "Custody: reasonable person in suspect's position would not feel free to terminate and leave",
            "Interrogation: express questioning or functional equivalent (likely to elicit response)",
            "Failure to give warnings renders statements inadmissible",
            "Waiver must be knowing, voluntary, and intelligent",
            "Invocation of right to silence or counsel must be unambiguous (Berghuis v Thompkins)",
        ],
        defenses=[
            "Statement obtained in violation of Miranda: suppression",
            "Involuntary confession (due process violation independent of Miranda)",
            "Right to counsel invoked: all interrogation must cease (Edwards v Arizona)",
        ],
        remedies=[
            "Suppression of statements obtained in Miranda violation",
            "Suppression of fruits derived from Miranda violation",
            "Exception: impeachment use of Miranda-violating statements (Harris v New York)",
            "Exception: public safety exception (New York v Quarles)",
        ],
        leading_cases=[
            "Miranda v Arizona (1966) — Custodial interrogation warnings required",
            "Berghuis v Thompkins (2010) — Unambiguous invocation required",
            "Edwards v Arizona (1981) — Right to counsel invoked: questioning must stop",
            "New York v Quarles (1984) — Public safety exception",
            "Missouri v Seibert (2004) — Deliberate two-step interrogation prohibited",
            "Dickerson v United States (2000) — Miranda is constitutional rule",
            "Vega v Tekoh (2022) — No Section 1983 action for Miranda violations",
        ],
        jurisdiction="federal",
        category="constitutional_rights",
        severity="constitutional",
    ),
    DoctrineBlock(
        topic="Sixth Amendment Right to Counsel",
        summary=(
            "The Sixth Amendment guarantees the right to assistance of counsel in all criminal "
            "prosecutions. Under Gideon v Wainwright, this right applies to felony cases. Under "
            "Argersinger v Hamlin, it extends to any case resulting in actual imprisonment. "
            "The right attaches at the initiation of formal adversarial proceedings (indictment, "
            "information, arraignment, preliminary hearing). Ineffective assistance of counsel "
            "claims require showing that counsel's performance was deficient and that the "
            "deficiency prejudiced the defense (Strickland two-prong test)."
        ),
        key_statutes=[
            "U.S. Constitution, Sixth Amendment",
            "18 USC 3006A (Criminal Justice Act)", "Gideon v Wainwright (1963)",
        ],
        elements=[
            "Right to counsel attaches at initiation of adversarial judicial proceedings",
            "Right to appointed counsel if indigent (Gideon, Argersinger)",
            "Right to counsel of choice if not indigent (United States v Gonzalez-Lopez)",
            "Right to effective assistance (Strickland v Washington two-prong test)",
            "Right to self-representation (Faretta v California)",
            "Conflict-free representation (Cuyler v Sullivan)",
        ],
        defenses=[
            "Ineffective assistance of counsel (Strickland)",
            "Denial of counsel of choice (automatic reversal)",
            "Conflict of interest affecting representation",
        ],
        remedies=[
            "Reversal of conviction for denial of counsel",
            "New trial for ineffective assistance if prejudice shown",
            "Automatic reversal for complete denial of counsel",
            "Habeas corpus relief under 28 USC 2254",
        ],
        leading_cases=[
            "Gideon v Wainwright (1963) — Right to appointed counsel for felonies",
            "Argersinger v Hamlin (1972) — Extends to misdemeanors with imprisonment",
            "Strickland v Washington (1984) — Ineffective assistance two-prong test",
            "United States v Gonzalez-Lopez (2006) — Right to counsel of choice",
            "Faretta v California (1975) — Right to self-representation",
            "Padilla v Kentucky (2010) — Duty to advise on immigration consequences",
            "Lafler v Cooper (2012) — IAC during plea bargaining",
        ],
        jurisdiction="federal",
        category="constitutional_rights",
        severity="constitutional",
    ),
    DoctrineBlock(
        topic="Eighth Amendment Punishment",
        summary=(
            "The Eighth Amendment prohibits excessive bail, excessive fines, and cruel and unusual "
            "punishment. Cruel and unusual punishment analysis considers evolving standards of "
            "decency (Trop v Dulles). The death penalty has specific limitations: cannot be imposed "
            "for non-homicide offenses against individuals (Kennedy v Louisiana), on juveniles "
            "(Roper v Simmons), or on intellectually disabled persons (Atkins v Virginia). "
            "Mandatory life without parole for juveniles is unconstitutional (Miller v Alabama). "
            "The proportionality principle requires that punishment not be grossly disproportionate "
            "to the offense."
        ),
        key_statutes=[
            "U.S. Constitution, Eighth Amendment",
            "Texas Constitution Article I, Section 13",
            "18 USC 3553(a) (Federal Sentencing Factors)",
        ],
        elements=[
            "Excessive bail: bail set higher than necessary to ensure appearance",
            "Excessive fines: fine grossly disproportionate to offense (Timbs v Indiana)",
            "Cruel and unusual: punishment shocks conscience or violates evolving standards",
            "Proportionality: sentence not grossly disproportionate to offense",
            "Conditions of confinement: prison conditions violating Eighth Amendment",
        ],
        defenses=[
            "Eighth Amendment challenge to sentence as disproportionate",
            "Challenge mandatory minimum as cruel and unusual",
            "Juvenile defendant protections (Miller, Montgomery)",
            "Intellectual disability claim (Atkins)",
        ],
        remedies=[
            "Resentencing if sentence found unconstitutional",
            "Bail reduction if excessive",
            "Fine reduction if grossly disproportionate",
            "Injunctive relief for conditions of confinement",
            "Habeas corpus for unconstitutional sentence",
        ],
        leading_cases=[
            "Trop v Dulles (1958) — Evolving standards of decency",
            "Solem v Helm (1983) — Proportionality for prison sentences",
            "Harmelin v Michigan (1991) — Narrow proportionality review",
            "Graham v Florida (2010) — No LWOP for juvenile non-homicide",
            "Miller v Alabama (2012) — No mandatory LWOP for juveniles",
            "Montgomery v Louisiana (2016) — Miller retroactive",
            "Timbs v Indiana (2019) — Excessive fines applies to states",
        ],
        jurisdiction="federal",
        category="constitutional_rights",
        severity="constitutional",
    ),
    DoctrineBlock(
        topic="Exclusionary Rule and Exceptions",
        summary=(
            "The exclusionary rule, established in Weeks v United States (1914) for federal courts "
            "and extended to states in Mapp v Ohio (1961), prohibits use of evidence obtained in "
            "violation of the Fourth Amendment. Derivative evidence is also excluded under the "
            "fruit of the poisonous tree doctrine (Wong Sun v United States). Major exceptions: "
            "independent source (evidence obtained through lawful independent means), inevitable "
            "discovery (evidence would have been lawfully discovered anyway), attenuation "
            "(connection between illegality and evidence sufficiently attenuated), and good faith "
            "reliance on a warrant later found defective (United States v Leon)."
        ),
        key_statutes=[
            "U.S. Constitution, Fourth Amendment",
            "Mapp v Ohio (1961)", "United States v Leon (1984)",
            "Texas Code of Criminal Procedure Article 38.23",
        ],
        elements=[
            "Government obtained evidence through unconstitutional search or seizure",
            "Defendant has standing (own rights violated)",
            "Evidence is fruit of the illegal action (causal connection)",
            "No exception to exclusionary rule applies",
        ],
        defenses=[
            "Motion to suppress evidence under Fourth Amendment",
            "Fruit of the poisonous tree argument for derivative evidence",
            "Standing challenge if evidence found in third-party premises",
        ],
        remedies=[
            "Suppression of primary evidence",
            "Suppression of derivative evidence (fruit of poisonous tree)",
            "May result in dismissal if key evidence suppressed",
        ],
        leading_cases=[
            "Weeks v United States (1914) — Exclusionary rule in federal courts",
            "Mapp v Ohio (1961) — Exclusionary rule applies to states",
            "Wong Sun v United States (1963) — Fruit of poisonous tree",
            "United States v Leon (1984) — Good faith exception",
            "Nix v Williams (1984) — Inevitable discovery exception",
            "Murray v United States (1988) — Independent source doctrine",
            "Utah v Strieff (2016) — Attenuation by intervening warrant",
            "Davis v United States (2011) — Good faith reliance on binding precedent",
        ],
        jurisdiction="federal",
        category="constitutional_rights",
        severity="constitutional",
    ),
]


# =============================================================================
# DEFENSE DOCTRINES
# =============================================================================

DEFENSE_DOCTRINES: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Self-Defense",
        summary=(
            "Self-defense justifies the use of force when a person reasonably believes force "
            "is immediately necessary to protect against another's use or attempted use of "
            "unlawful force. Under Texas Penal Code Section 9.31, a person is justified in using "
            "force when and to the degree they reasonably believe it is immediately necessary to "
            "protect against another's use or attempted use of unlawful force. Deadly force is "
            "justified under TPC 9.32 when the actor reasonably believes it is immediately "
            "necessary to protect against deadly force, kidnapping, murder, sexual assault, "
            "aggravated sexual assault, robbery, or aggravated robbery. Texas has no duty to "
            "retreat (stand your ground) if lawfully present."
        ),
        key_statutes=[
            "Texas Penal Code Section 9.31", "Texas Penal Code Section 9.32",
            "Texas Penal Code Section 9.33 (Defense of Third Person)",
            "MPC Section 3.04",
        ],
        elements=[
            "Reasonable belief that force is immediately necessary",
            "Against another's use or attempted use of unlawful force",
            "Force used must be proportional (non-deadly vs deadly)",
            "Deadly force: only against deadly force, kidnapping, murder, sexual assault, robbery",
            "No duty to retreat in Texas (stand your ground)",
            "Castle doctrine: presumption of reasonableness in home (TPC 9.31(a))",
            "Actor must not have provoked the encounter",
        ],
        defenses=[
            "Self-defense is itself a defense — this is the justification",
            "Imperfect self-defense may reduce murder to manslaughter",
            "Initial aggressor may regain self-defense right through withdrawal",
        ],
        remedies=[
            "Complete acquittal if self-defense proven",
            "Imperfect self-defense: reduction to manslaughter",
            "Castle doctrine: presumption shifts burden to prosecution",
            "Civil immunity under Texas Civil Practice and Remedies Code 83.001",
        ],
        leading_cases=[
            "People v Goetz (1986) — Reasonable belief standard in self-defense",
            "State v Norman (1989) — Battered woman syndrome and imminence",
            "United States v Peterson (1973) — Initial aggressor and withdrawal",
            "Morales v State (2006) — Texas castle doctrine",
            "Smith v State (2011) — Stand your ground application in Texas",
        ],
        jurisdiction="texas",
        category="defenses",
        severity="justification",
    ),
    DoctrineBlock(
        topic="Insanity Defense",
        summary=(
            "The insanity defense excuses criminal conduct when the defendant, due to a severe "
            "mental disease or defect, was unable to appreciate the nature and quality of their "
            "act or was unable to distinguish right from wrong at the time of the offense. Texas "
            "follows a modified M'Naghten standard under TPC Section 8.01: it is an affirmative "
            "defense that at the time of the conduct, the actor, as a result of severe mental "
            "disease or defect, did not know that the conduct was wrong. The federal standard "
            "under 18 USC 17 requires proof by clear and convincing evidence that the defendant "
            "was unable to appreciate the nature and quality or wrongfulness of their acts."
        ),
        key_statutes=[
            "Texas Penal Code Section 8.01", "18 USC 17 (Federal Insanity Defense)",
            "Insanity Defense Reform Act of 1984",
        ],
        elements=[
            "Severe mental disease or defect at time of offense",
            "Unable to appreciate nature and quality of the act (cognitive prong)",
            "OR unable to distinguish right from wrong (moral prong)",
            "Texas: defendant bears burden by preponderance of evidence",
            "Federal: defendant bears burden by clear and convincing evidence",
            "Evaluating mental state at time of offense, not at trial",
        ],
        defenses=[
            "Insanity defense itself is the affirmative defense",
            "Diminished capacity (where recognized — not in Texas)",
            "Guilty but mentally ill (alternative verdict in some states)",
        ],
        remedies=[
            "Not guilty by reason of insanity (NGRI)",
            "Commitment to mental institution (may exceed prison term)",
            "Conditional release with supervision",
            "Federal: automatic commitment for evaluation under 18 USC 4243",
        ],
        leading_cases=[
            "M'Naghten's Case (1843) — Original right/wrong test",
            "Durham v United States (1954) — Product test (since abandoned)",
            "United States v Hinckley (1982) — Led to Insanity Defense Reform Act",
            "Clark v Arizona (2006) — States may limit insanity defense",
            "Kahler v Kansas (2020) — States may abolish insanity as affirmative defense",
        ],
        jurisdiction="texas",
        category="defenses",
        severity="affirmative_defense",
    ),
    DoctrineBlock(
        topic="Duress",
        summary=(
            "Duress excuses criminal conduct when the defendant was compelled to act by the threat "
            "of imminent death or serious bodily injury. The threat must be of such a nature that "
            "a person of reasonable firmness in the defendant's situation would have been unable "
            "to resist. Under Texas Penal Code Section 8.05, duress is an affirmative defense "
            "except for murder and certain serious offenses. The threat must come from another "
            "person, not from natural circumstances (which falls under necessity). Under MPC "
            "Section 2.09, duress is available for any crime including homicide if the threat "
            "is of unlawful force against the person or another."
        ),
        key_statutes=[
            "Texas Penal Code Section 8.05", "MPC Section 2.09",
            "18 USC Federal Common Law Duress",
        ],
        elements=[
            "Threat of imminent death or serious bodily injury",
            "Threat from another person (not natural circumstances)",
            "Person of reasonable firmness would have been unable to resist",
            "No reasonable escape or alternative available",
            "Defendant did not recklessly place themselves in the situation",
        ],
        defenses=[
            "Duress is the defense — this is the excuse",
            "Not available for intentional murder in most jurisdictions",
            "Texas: not available if defendant intentionally, knowingly, or recklessly placed self in situation",
        ],
        remedies=[
            "Complete acquittal if duress established",
            "Texas: affirmative defense with preponderance burden on defendant",
            "May reduce culpability for sentencing even if not complete defense",
        ],
        leading_cases=[
            "United States v Dixon (2008) — Federal duress elements",
            "People v Anderson (2002) — Imminence requirement",
            "State v Toscano (1977) — MPC broad duress defense",
            "United States v Fleming (2000) — Duress and drug offenses",
        ],
        jurisdiction="texas",
        category="defenses",
        severity="affirmative_defense",
    ),
    DoctrineBlock(
        topic="Entrapment",
        summary=(
            "Entrapment occurs when government agents induce a person to commit a crime that the "
            "person was not otherwise predisposed to commit. The subjective test (federal/majority) "
            "focuses on the defendant's predisposition. The objective test (MPC/minority) focuses "
            "on whether the government conduct would induce a law-abiding person to commit the "
            "crime. Under Texas Penal Code Section 8.06, entrapment is an affirmative defense "
            "where the defendant was induced by a law enforcement agent using persuasion or other "
            "means likely to cause persons to commit the offense."
        ),
        key_statutes=[
            "Texas Penal Code Section 8.06", "MPC Section 2.13",
            "Jacobson v United States (1992)",
        ],
        elements=[
            "Government agent or informant involvement",
            "Inducement to commit the crime (beyond merely providing opportunity)",
            "Subjective test: defendant was not predisposed to commit the crime",
            "Objective test: conduct would induce a normally law-abiding person",
            "Government must initiate or induce, not merely facilitate",
        ],
        defenses=[
            "Entrapment is the defense",
            "Subjective focus: defendant's lack of predisposition",
            "Objective focus: government overreach regardless of predisposition",
        ],
        remedies=[
            "Complete acquittal",
            "Dismissal of charges",
            "Due process defense for outrageous government conduct (rare)",
        ],
        leading_cases=[
            "Sorrells v United States (1932) — Entrapment defense established",
            "Sherman v United States (1958) — Predisposition focus affirmed",
            "Jacobson v United States (1992) — Government created predisposition",
            "Mathews v United States (1988) — Inconsistent defenses allowed",
            "United States v Russell (1973) — Outrageous government conduct",
            "Bush v State (1999) — Texas entrapment standard",
        ],
        jurisdiction="federal",
        category="defenses",
        severity="affirmative_defense",
    ),
    DoctrineBlock(
        topic="Necessity Defense",
        summary=(
            "The necessity defense (choice of evils) justifies criminal conduct when the defendant "
            "reasonably believed the conduct was immediately necessary to avoid imminent harm, and "
            "the harm avoided was greater than the harm caused by the criminal conduct. Unlike "
            "duress, the threat comes from natural forces or circumstances rather than another "
            "person. Texas Penal Code Section 9.22 codifies necessity: conduct is justified if "
            "the actor reasonably believes the conduct is immediately necessary to avoid imminent "
            "harm, the desirability and urgency of avoiding the harm clearly outweigh the harm "
            "sought to be prevented by the law, and a legislative purpose to exclude the "
            "justification is not plainly apparent."
        ),
        key_statutes=[
            "Texas Penal Code Section 9.22", "MPC Section 3.02",
        ],
        elements=[
            "Imminent harm from natural forces or circumstances",
            "Reasonable belief that conduct is immediately necessary",
            "Harm avoided clearly outweighs harm caused by criminal conduct",
            "No reasonable legal alternative available",
            "Legislative purpose does not plainly exclude the defense",
            "Defendant did not substantially contribute to creating the emergency",
        ],
        defenses=["Necessity is itself the justification defense."],
        remedies=[
            "Complete acquittal",
            "Jury instruction on necessity when evidence raises the issue",
        ],
        leading_cases=[
            "United States v Bailey (1980) — Necessity requires imminence",
            "United States v Schoon (1992) — Indirect civil disobedience not necessity",
            "People v Unger (1977) — Prison escape and necessity",
            "Bragg v State (2006) — Necessity in Texas driving cases",
        ],
        jurisdiction="texas",
        category="defenses",
        severity="justification",
    ),
]


# =============================================================================
# SENTENCING DOCTRINES
# =============================================================================

SENTENCING_DOCTRINES: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Federal Sentencing Guidelines",
        summary=(
            "The United States Sentencing Guidelines (USSG) provide a framework for sentencing "
            "in federal courts. After United States v Booker (2005), the guidelines are advisory "
            "rather than mandatory but remain the starting point for sentencing. The guidelines "
            "use a grid system with offense level (1-43) on the vertical axis and criminal history "
            "category (I-VI) on the horizontal axis to determine a sentencing range. Judges must "
            "calculate the guidelines range, consider Section 3553(a) factors, and may vary from "
            "the range with adequate explanation. Departures and variances must be procedurally "
            "and substantively reasonable."
        ),
        key_statutes=[
            "18 USC 3553(a) (Sentencing Factors)", "28 USC 991-998 (Sentencing Commission)",
            "USSG Manual", "18 USC 3553(f) (Safety Valve)",
        ],
        elements=[
            "Calculate base offense level from relevant guideline section",
            "Apply specific offense characteristics (adjustments)",
            "Apply Chapter 3 adjustments (role, obstruction, acceptance)",
            "Determine criminal history category (I-VI)",
            "Find guideline range on sentencing table",
            "Consider 18 USC 3553(a) factors for variance",
            "Mandatory minimums override guidelines if higher",
        ],
        defenses=[
            "Downward departure for substantial assistance (USSG 5K1.1)",
            "Safety valve for minimal drug participants (18 USC 3553(f))",
            "Variance based on 3553(a) factors (history, characteristics, deterrence)",
            "Challenge to criminal history overrepresentation",
            "First Step Act provisions for recalculation",
        ],
        remedies=[
            "Sentencing within or below guidelines range",
            "Downward departure or variance with adequate explanation",
            "Appeal for procedural or substantive unreasonableness",
            "First Step Act compassionate release (18 USC 3582(c)(1)(A))",
        ],
        leading_cases=[
            "United States v Booker (2005) — Guidelines made advisory",
            "Gall v United States (2007) — Abuse of discretion review standard",
            "Rita v United States (2007) — Within-guidelines presumption reasonable",
            "Kimbrough v United States (2007) — Judge may disagree with guidelines policy",
            "Pepper v United States (2011) — Post-sentencing rehabilitation relevant",
        ],
        jurisdiction="federal",
        category="sentencing",
        severity="guidelines",
    ),
    DoctrineBlock(
        topic="Texas Sentencing Framework",
        summary=(
            "Texas sentencing is structured around offense classifications. Capital felony: death "
            "or life without parole. First degree felony: 5-99 years or life, up to $10,000 fine. "
            "Second degree felony: 2-20 years, up to $10,000 fine. Third degree felony: 2-10 "
            "years, up to $10,000 fine. State jail felony: 180 days-2 years in state jail, up to "
            "$10,000 fine. Class A misdemeanor: up to 1 year jail, $4,000 fine. Class B: up to "
            "180 days, $2,000 fine. Class C: fine only up to $500. Enhancement provisions can "
            "increase punishment range. Habitual offender statutes under TPC 12.42 can enhance "
            "up to 25-99 years or life."
        ),
        key_statutes=[
            "Texas Penal Code Chapter 12 (Punishments)",
            "Texas Penal Code Section 12.42 (Enhancement)",
            "Texas Code of Criminal Procedure Article 42A (Community Supervision)",
        ],
        elements=[
            "Offense classification determines punishment range",
            "Enhancement based on prior convictions (TPC 12.42)",
            "Deadly weapon finding affects parole eligibility",
            "Jury or judge sentencing (defendant's choice in Texas)",
            "Probation/community supervision eligibility varies by offense",
            "Good conduct time: day-for-day credit for most offenses",
            "3g offenses require minimum 50% flat time before parole eligibility",
        ],
        defenses=[
            "Challenge prior convictions used for enhancement",
            "Argue for minimum sentence within range",
            "Present mitigation evidence",
            "Seek probation where eligible",
            "Deferred adjudication (no final conviction if completed)",
        ],
        remedies=[
            "Prison sentence within statutory range",
            "Probation/community supervision",
            "Deferred adjudication (eligible offenses)",
            "State jail with possible probation",
            "Fine with or without confinement",
        ],
        leading_cases=[
            "Ex parte Pue (2009) — Enhancement requirements in Texas",
            "Stringer v State (2013) — Deadly weapon finding and parole",
            "Rickels v State (2000) — Deferred adjudication scope",
            "Jordan v State (2004) — Jury sentencing discretion",
        ],
        jurisdiction="texas",
        category="sentencing",
        severity="framework",
    ),
]


# =============================================================================
# JUVENILE JUSTICE DOCTRINES
# =============================================================================

JUVENILE_JUSTICE_DOCTRINES: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Juvenile Jurisdiction and Transfer",
        summary=(
            "Juvenile courts have original jurisdiction over persons under 17 (Texas) or 18 "
            "(federal/most states) who commit delinquent conduct (would be a crime if committed "
            "by an adult) or status offenses (truancy, curfew, runaway). Transfer to adult court "
            "(certification) may occur for serious offenses. Texas Family Code Section 54.02 "
            "allows discretionary transfer for children 14+ accused of a felony if the court "
            "finds probable cause, the child is not amenable to rehabilitation, and the welfare "
            "of the community requires it. Determinate sentencing (blended) allows juvenile "
            "courts to sentence up to 40 years for enumerated offenses."
        ),
        key_statutes=[
            "Texas Family Code Section 51.02-51.04 (Jurisdiction)",
            "Texas Family Code Section 54.02 (Transfer/Certification)",
            "18 USC 5031-5042 (Federal Juvenile Delinquency Act)",
        ],
        elements=[
            "Juvenile jurisdiction: under 17 in Texas (10 minimum age)",
            "Delinquent conduct: act that would be criminal if by adult",
            "Status offense: conduct only criminal because of age",
            "Transfer hearing: probable cause, non-amenability, community welfare",
            "Kent factors for transfer decision (Kent v United States)",
            "Determinate sentencing for capital murder, first degree felony, aggravated controlled substance",
        ],
        defenses=[
            "Amenability to juvenile rehabilitation (oppose transfer)",
            "Age at time of offense (under minimum transfer age)",
            "Mitigating factors: mental health, maturity, family circumstances",
            "Due process protections (In re Gault)",
        ],
        remedies=[
            "Juvenile disposition: probation, placement, commitment to TJJD",
            "Determinate sentence: up to 40 years with transfer to adult prison at 19",
            "Sealing of juvenile records",
            "Diversion programs",
            "Restitution and community service",
        ],
        leading_cases=[
            "Kent v United States (1966) — Due process required for transfer",
            "In re Gault (1967) — Due process rights for juveniles",
            "In re Winship (1970) — Beyond reasonable doubt standard applies",
            "McKeiver v Pennsylvania (1971) — No jury trial right in juvenile court",
            "Roper v Simmons (2005) — No death penalty for juveniles",
            "Graham v Florida (2010) — No LWOP for non-homicide juveniles",
            "Miller v Alabama (2012) — No mandatory LWOP for juveniles",
        ],
        jurisdiction="texas",
        category="juvenile_justice",
        severity="juvenile",
    ),
]


# =============================================================================
# INCHOATE OFFENSE DOCTRINES
# =============================================================================

INCHOATE_DOCTRINES: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Criminal Attempt",
        summary=(
            "Criminal attempt occurs when a person, with the specific intent to commit an offense, "
            "does an act amounting to more than mere preparation that tends but fails to effect "
            "the commission of the offense. Under Texas Penal Code Section 15.01, attempt is "
            "punished one category below the target offense (e.g., attempt of first degree felony "
            "is second degree felony). The substantial step test (MPC) asks whether the defendant "
            "took a substantial step strongly corroborative of criminal purpose. Impossibility: "
            "factual impossibility is not a defense, legal impossibility may be."
        ),
        key_statutes=[
            "Texas Penal Code Section 15.01", "MPC Section 5.01",
            "18 USC 1113 (Attempted Murder)", "General federal attempt principles",
        ],
        elements=[
            "Specific intent to commit the target offense",
            "Act beyond mere preparation (substantial step)",
            "Substantial step must be strongly corroborative of criminal purpose",
            "Failure to complete the offense (or completed but result not achieved)",
            "Factual impossibility is no defense",
        ],
        defenses=[
            "Abandonment/renunciation: voluntary and complete (MPC/Texas TPC 15.04)",
            "Legal impossibility (limited recognition)",
            "Mere preparation (not a substantial step)",
            "Lack of specific intent",
        ],
        remedies=[
            "Texas: one category below completed offense",
            "Federal: varies by statute (some have specific attempt provisions)",
            "Cannot receive more punishment than for completed offense",
        ],
        leading_cases=[
            "People v Rizzo (1927) — Dangerous proximity test",
            "United States v Jackson (1977) — Substantial step standard",
            "People v Dlugash (1977) — Impossibility doctrine",
            "Ross v State (2013) — Texas attempt elements",
        ],
        jurisdiction="texas",
        category="inchoate_crimes",
        severity="varies",
    ),
    DoctrineBlock(
        topic="Criminal Conspiracy",
        summary=(
            "Criminal conspiracy is an agreement between two or more persons to commit a crime, "
            "accompanied by an overt act in furtherance (required under federal law and Texas "
            "law). Under Texas Penal Code Section 15.02, conspiracy is one category below the "
            "target offense. Federal conspiracy under 18 USC 371 carries up to 5 years. "
            "Drug conspiracy under 21 USC 846 carries the same penalties as the underlying "
            "offense. Pinkerton liability holds conspirators responsible for foreseeable crimes "
            "committed by co-conspirators in furtherance of the conspiracy."
        ),
        key_statutes=[
            "Texas Penal Code Section 15.02", "18 USC 371 (General Federal Conspiracy)",
            "21 USC 846 (Drug Conspiracy)", "MPC Section 5.03",
        ],
        elements=[
            "Agreement between two or more persons",
            "To commit a criminal offense",
            "Intent to agree and intent to commit the underlying offense",
            "Overt act in furtherance of the conspiracy (federal and Texas)",
            "Pinkerton liability: co-conspirator liable for foreseeable acts of others",
        ],
        defenses=[
            "No agreement existed (mere knowledge insufficient)",
            "Withdrawal: affirmative and communicated to co-conspirators",
            "Single conspiracy vs multiple conspiracies (variance defense)",
            "Wharton's Rule: crime requiring two parties cannot be conspiracy",
            "Buyer-seller rule: simple buyer-seller relationship may not be conspiracy",
        ],
        remedies=[
            "Texas: one category below target offense",
            "Federal 18 USC 371: up to 5 years",
            "Federal drug conspiracy: same as underlying offense penalties",
            "RICO conspiracy 18 USC 1962(d): up to 20 years",
        ],
        leading_cases=[
            "Pinkerton v United States (1946) — Co-conspirator liability",
            "Kotteakos v United States (1946) — Single vs multiple conspiracies",
            "United States v Jimenez Recio (2003) — Conspiracy continues after impossibility",
            "Ocasio v United States (2016) — Conspiracy to commit extortion",
        ],
        jurisdiction="federal",
        category="inchoate_crimes",
        severity="varies",
    ),
]


# =============================================================================
# TITLE 18 USC FEDERAL CRIMES DOCTRINES
# =============================================================================

FEDERAL_CRIMES_DOCTRINES: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Federal Firearms Offenses",
        summary=(
            "Federal firearms law centers on 18 USC 922 which prohibits certain persons from "
            "possessing firearms: convicted felons (922(g)(1)), fugitives (922(g)(2)), unlawful "
            "users of controlled substances (922(g)(3)), persons committed to mental institutions "
            "(922(g)(4)), illegal aliens (922(g)(5)), dishonorably discharged (922(g)(6)), "
            "persons under domestic violence restraining orders (922(g)(8)), and persons convicted "
            "of misdemeanor domestic violence (922(g)(9)). Using or carrying a firearm during a "
            "crime of violence or drug trafficking offense under 18 USC 924(c) carries mandatory "
            "consecutive sentences: 5 years for possession, 7 for brandishing, 10 for discharge."
        ),
        key_statutes=[
            "18 USC 922(g) (Prohibited Persons)", "18 USC 924(c) (Use During Crime)",
            "18 USC 921 (Definitions)", "National Firearms Act (26 USC 5801-5872)",
        ],
        elements=[
            "Defendant falls within prohibited category (18 USC 922(g))",
            "Knowing possession of firearm or ammunition",
            "Firearm traveled in or affects interstate commerce (jurisdictional element)",
            "924(c): use, carry, or possess firearm during and in relation to crime of violence or drug crime",
            "NFA: registration and tax requirements for certain weapons (short-barrel, suppressors, machine guns)",
        ],
        defenses=[
            "Not a prohibited person (challenge prior conviction validity)",
            "No knowing possession",
            "Justification (possessing firearm in emergency)",
            "Second Amendment challenge (after Bruen)",
            "Commerce clause challenge to jurisdictional element",
        ],
        remedies=[
            "922(g): up to 15 years (enhanced if 3+ prior violent/drug convictions under ACCA)",
            "924(c): 5/7/10 year mandatory consecutive terms",
            "Second or subsequent 924(c): 25 years mandatory consecutive",
            "NFA violations: up to 10 years",
        ],
        leading_cases=[
            "District of Columbia v Heller (2008) — Individual right to bear arms",
            "New York State Rifle & Pistol Assn v Bruen (2022) — Text, history, tradition test",
            "Rehaif v United States (2019) — Knowledge of prohibited status required",
            "United States v Rahimi (2024) — Domestic violence disarmament survives Bruen",
            "United States v Taylor (2022) — Hobbs Act robbery not 924(c) crime of violence",
        ],
        jurisdiction="federal",
        category="federal_crimes",
        severity="felony",
    ),
    DoctrineBlock(
        topic="Federal Habeas Corpus",
        summary=(
            "Federal habeas corpus under 28 USC 2254 allows state prisoners to challenge their "
            "convictions in federal court on constitutional grounds. The Anti-Terrorism and "
            "Effective Death Penalty Act (AEDPA) of 1996 significantly restricted federal habeas "
            "review. Under AEDPA, federal courts may grant relief only if the state court decision "
            "was contrary to clearly established Supreme Court precedent (de novo) or involved an "
            "unreasonable application of clearly established law (deferential). Petitioners must "
            "exhaust state remedies and file within one year of conviction becoming final. "
            "Procedural default bars claims not properly raised in state court."
        ),
        key_statutes=[
            "28 USC 2254 (State Prisoner Habeas)", "28 USC 2255 (Federal Prisoner Motion)",
            "AEDPA (1996)", "28 USC 2244(d) (Statute of Limitations)",
        ],
        elements=[
            "Petitioner is in custody pursuant to state court judgment",
            "Claim raises federal constitutional violation",
            "State remedies exhausted or futile",
            "Filed within one-year limitations period",
            "Not procedurally defaulted (or cause and prejudice shown)",
            "AEDPA deference: state court decision contrary to or unreasonable application of SCOTUS precedent",
        ],
        defenses=[
            "Actual innocence gateway (Schlup v Delo)",
            "Cause and prejudice to overcome procedural default",
            "Equitable tolling of limitations period",
            "Ineffective assistance of post-conviction counsel (Martinez v Ryan)",
        ],
        remedies=[
            "Grant of writ: new trial or resentencing",
            "Conditional writ: state must retry within specified period",
            "Stay of execution in capital cases",
            "Certificate of appealability required for appeal",
        ],
        leading_cases=[
            "Williams v Taylor (2000) — AEDPA standard explained",
            "Harrington v Richter (2011) — Strong AEDPA deference",
            "Martinez v Ryan (2012) — Ineffective PCR counsel excuses default",
            "Schlup v Delo (1995) — Actual innocence gateway",
            "McQuiggin v Perkins (2013) — Actual innocence overcomes limitations",
            "Cullen v Pinholster (2011) — Review limited to state court record",
        ],
        jurisdiction="federal",
        category="federal_procedure",
        severity="post_conviction",
    ),
]


# =============================================================================
# PLEA BARGAINING AND PROCEDURE DOCTRINES
# =============================================================================

PLEA_PROCEDURE_DOCTRINES: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Plea Bargaining",
        summary=(
            "Plea bargaining resolves approximately 95% of federal and state criminal cases. "
            "Charge bargaining involves dismissing some charges or reducing to lesser offense. "
            "Sentence bargaining involves agreement on sentencing recommendation. Under Federal "
            "Rule 11, the court must address the defendant personally, determine the plea is "
            "voluntary, ensure a factual basis exists, and advise of rights being waived. In "
            "Texas, a plea agreement is not binding on the court — the judge may reject it. "
            "Defendants have a Sixth Amendment right to effective assistance during plea negotiations."
        ),
        key_statutes=[
            "Federal Rules of Criminal Procedure Rule 11",
            "Texas Code of Criminal Procedure Article 26.13",
            "Brady v United States (1970)",
        ],
        elements=[
            "Voluntary, knowing, and intelligent plea",
            "Understanding of charges and potential penalties",
            "Factual basis for the plea",
            "Waiver of trial rights (jury, confrontation, self-incrimination)",
            "Understanding of mandatory minimums if applicable",
            "Immigration consequences advisement (Padilla v Kentucky)",
        ],
        defenses=[
            "Involuntary plea (coercion, threats, misinformation)",
            "Ineffective assistance during plea process (Lafler v Cooper)",
            "Breach of plea agreement by government",
            "Failure to advise of immigration consequences",
        ],
        remedies=[
            "Withdrawal of plea before sentencing (fair and just reason)",
            "Withdrawal after sentencing (manifest injustice or IAC)",
            "Specific performance of breached agreement",
            "Resentencing before different judge",
        ],
        leading_cases=[
            "Brady v United States (1970) — Plea bargaining constitutional",
            "Boykin v Alabama (1969) — Record must show knowing waiver",
            "Padilla v Kentucky (2010) — Immigration consequence advisement",
            "Lafler v Cooper (2012) — IAC in plea process",
            "Missouri v Frye (2012) — IAC for failure to communicate offer",
            "Class v United States (2018) — Conditional plea preserves claims",
        ],
        jurisdiction="federal",
        category="procedural",
        severity="procedural",
    ),
]


# =============================================================================
# SEARCH AND SEIZURE DETAIL DOCTRINES
# =============================================================================

SEARCH_SEIZURE_DOCTRINES: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Warrant Exceptions Comprehensive",
        summary=(
            "While the Fourth Amendment generally requires a warrant, the Supreme Court has "
            "recognized numerous exceptions. Consent search: voluntary consent from person with "
            "authority (Schneckloth v Bustamonte). Search incident to arrest: area within "
            "immediate control (Chimel v California), including vehicle passenger compartment "
            "(New York v Belton, limited by Arizona v Gant). Automobile exception: probable "
            "cause to search vehicle (Carroll v United States). Plain view: officer lawfully "
            "present, evidence in plain view, incriminating nature immediately apparent (Horton "
            "v California). Exigent circumstances: imminent destruction of evidence, hot pursuit, "
            "risk of harm. Inventory search: standardized procedures for impounded property. "
            "Terry stop and frisk: reasonable suspicion of criminal activity (pat-down for weapons)."
        ),
        key_statutes=[
            "U.S. Constitution, Fourth Amendment",
            "Terry v Ohio (1968)", "Chimel v California (1969)",
            "Carroll v United States (1925)",
        ],
        elements=[
            "Consent: voluntary, from person with actual or apparent authority",
            "Search incident to arrest: contemporaneous, within wingspan/lunge area",
            "Vehicle: probable cause that vehicle contains evidence or contraband",
            "Plain view: lawful position, immediately apparent incriminating nature",
            "Exigent: imminent destruction of evidence, hot pursuit, emergency",
            "Inventory: pursuant to standardized department procedures",
            "Terry: reasonable suspicion of criminal activity, pat-down for weapons only",
            "Border search: routine search at international border without warrant or suspicion",
        ],
        defenses=[
            "No valid exception applies — evidence should be suppressed",
            "Consent was coerced or involuntary",
            "Scope of search exceeded exception boundaries",
            "Pretext stop challenge (Whren limits this)",
        ],
        remedies=[
            "Suppression of evidence obtained outside valid exception",
            "Suppression of derivative evidence (fruit of poisonous tree)",
        ],
        leading_cases=[
            "Schneckloth v Bustamonte (1973) — Voluntary consent standard",
            "Arizona v Gant (2009) — Search incident to arrest in vehicles limited",
            "Carroll v United States (1925) — Automobile exception",
            "Horton v California (1990) — Plain view doctrine",
            "Kentucky v King (2011) — Police-created exigency",
            "Florida v Jardines (2013) — Dog sniff at front door is search",
            "South Dakota v Opperman (1976) — Inventory search of vehicle",
            "Birchfield v North Dakota (2016) — Blood test requires warrant in DWI",
        ],
        jurisdiction="federal",
        category="search_seizure",
        severity="constitutional",
    ),
]


# =============================================================================
# ALL DOCTRINES REGISTRY
# =============================================================================

ALL_DOCTRINE_LISTS: Dict[str, List[DoctrineBlock]] = {
    "elements_of_crime": ELEMENTS_OF_CRIME_DOCTRINES,
    "homicide": HOMICIDE_DOCTRINES,
    "assault_battery": ASSAULT_BATTERY_DOCTRINES,
    "property_crimes": PROPERTY_CRIME_DOCTRINES,
    "drug_offenses": DRUG_OFFENSE_DOCTRINES,
    "fraud_white_collar": WHITE_COLLAR_DOCTRINES,
    "constitutional_rights": CONSTITUTIONAL_DOCTRINES,
    "defenses": DEFENSE_DOCTRINES,
    "sentencing": SENTENCING_DOCTRINES,
    "juvenile_justice": JUVENILE_JUSTICE_DOCTRINES,
    "inchoate_crimes": INCHOATE_DOCTRINES,
    "federal_crimes": FEDERAL_CRIMES_DOCTRINES,
    "plea_procedure": PLEA_PROCEDURE_DOCTRINES,
    "search_seizure": SEARCH_SEIZURE_DOCTRINES,
}


# =============================================================================
# DOCTRINE CACHE
# =============================================================================

class DoctrineCacheManager:
    """
    Thread-safe doctrine cache manager.

    Provides fast O(1) lookup by cache_key with optional category and
    jurisdiction filtering. Supports bulk loading, individual inserts,
    and content hash verification for determinism.
    """

    def __init__(self) -> None:
        self._cache: Dict[str, DoctrineBlock] = {}
        self._by_category: Dict[str, List[str]] = {}
        self._by_jurisdiction: Dict[str, List[str]] = {}
        self._lock = threading.Lock()
        self._loaded_at: Optional[float] = None
        self._load_count: int = 0

    def load_all_doctrines(self) -> int:
        """Load all pre-defined doctrine blocks into the cache."""
        count = 0
        for category, doctrine_list in ALL_DOCTRINE_LISTS.items():
            for doctrine in doctrine_list:
                self.add(doctrine)
                count += 1
        self._loaded_at = time.time()
        self._load_count = count
        logger.info(
            f"Doctrine cache loaded: {count} blocks across "
            f"{len(ALL_DOCTRINE_LISTS)} categories"
        )
        return count

    def add(self, doctrine: DoctrineBlock) -> str:
        """Add a doctrine block to the cache. Returns cache_key."""
        key = doctrine.cache_key
        with self._lock:
            self._cache[key] = doctrine
            cat = doctrine.category
            if cat not in self._by_category:
                self._by_category[cat] = []
            if key not in self._by_category[cat]:
                self._by_category[cat].append(key)
            jur = doctrine.jurisdiction
            if jur not in self._by_jurisdiction:
                self._by_jurisdiction[jur] = []
            if key not in self._by_jurisdiction[jur]:
                self._by_jurisdiction[jur].append(key)
        return key

    def get(self, cache_key: str) -> Optional[DoctrineBlock]:
        """Retrieve a doctrine block by cache key."""
        with self._lock:
            return self._cache.get(cache_key)

    def search(self, query: str, max_results: int = 10) -> List[DoctrineBlock]:
        """Simple text search across doctrine topics and summaries."""
        query_lower = query.lower()
        results: List[Tuple[float, DoctrineBlock]] = []
        with self._lock:
            for doctrine in self._cache.values():
                score = 0.0
                if query_lower in doctrine.topic.lower():
                    score += 2.0
                if query_lower in doctrine.summary.lower():
                    score += 1.0
                searchable = doctrine.searchable_text.lower()
                occurrences = searchable.count(query_lower)
                score += min(occurrences * 0.1, 1.0)
                if score > 0:
                    results.append((score, doctrine))
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:max_results]]

    def get_by_category(self, category: str) -> List[DoctrineBlock]:
        """Get all doctrines in a category."""
        with self._lock:
            keys = self._by_category.get(category, [])
            return [self._cache[k] for k in keys if k in self._cache]

    def get_by_jurisdiction(self, jurisdiction: str) -> List[DoctrineBlock]:
        """Get all doctrines for a jurisdiction."""
        with self._lock:
            keys = self._by_jurisdiction.get(jurisdiction, [])
            return [self._cache[k] for k in keys if k in self._cache]

    def get_all_keys(self) -> List[str]:
        """Return all cache keys."""
        with self._lock:
            return list(self._cache.keys())

    def get_all_categories(self) -> List[str]:
        """Return all category names."""
        with self._lock:
            return list(self._by_category.keys())

    def get_all_jurisdictions(self) -> List[str]:
        """Return all jurisdiction names."""
        with self._lock:
            return list(self._by_jurisdiction.keys())

    @property
    def size(self) -> int:
        """Number of doctrine blocks in cache."""
        with self._lock:
            return len(self._cache)

    def verify_hash(self, cache_key: str, expected_hash: str) -> bool:
        """Verify doctrine content hash for determinism checks."""
        doctrine = self.get(cache_key)
        if doctrine is None:
            return False
        return doctrine.content_hash == expected_hash

    def export_hashes(self) -> Dict[str, str]:
        """Export all cache_key -> content_hash mappings for determinism verification."""
        with self._lock:
            return {key: d.content_hash for key, d in self._cache.items()}

    def get_stats(self) -> Dict[str, Any]:
        """Return cache statistics."""
        with self._lock:
            cat_counts = {cat: len(keys) for cat, keys in self._by_category.items()}
            jur_counts = {jur: len(keys) for jur, keys in self._by_jurisdiction.items()}
        return {
            "total_blocks": self.size,
            "categories": cat_counts,
            "jurisdictions": jur_counts,
            "loaded_at": (
                datetime.fromtimestamp(self._loaded_at, tz=timezone.utc).isoformat()
                if self._loaded_at else None
            ),
            "load_count": self._load_count,
        }

    def health_check(self) -> Dict[str, Any]:
        """Check doctrine cache health."""
        status = "healthy"
        issues: List[str] = []
        if self.size == 0:
            status = "degraded"
            issues.append("Doctrine cache is empty")
        if self._loaded_at is None:
            status = "degraded"
            issues.append("Doctrine cache never loaded")
        return {
            "component": "doctrine_cache",
            "status": status,
            "block_count": self.size,
            "category_count": len(self._by_category),
            "issues": issues,
        }

    def to_search_entries(self) -> List[Dict[str, Any]]:
        """Convert all doctrines to search index entries."""
        entries: List[Dict[str, Any]] = []
        with self._lock:
            for key, doctrine in self._cache.items():
                entries.append({
                    "doctrine_key": key,
                    "text": doctrine.searchable_text,
                    "metadata": {
                        "topic": doctrine.topic,
                        "category": doctrine.category,
                        "jurisdiction": doctrine.jurisdiction,
                        "severity": doctrine.severity,
                        "content_hash": doctrine.content_hash,
                    },
                })
        return entries


# =============================================================================
# MODULE-LEVEL SINGLETON
# =============================================================================

_doctrine_cache: Optional[DoctrineCacheManager] = None
_cache_lock = threading.Lock()


def get_doctrine_cache() -> DoctrineCacheManager:
    """Get or create the singleton doctrine cache, pre-loaded with all doctrines."""
    global _doctrine_cache
    if _doctrine_cache is None:
        with _cache_lock:
            if _doctrine_cache is None:
                _doctrine_cache = DoctrineCacheManager()
                _doctrine_cache.load_all_doctrines()
    return _doctrine_cache


def get_doctrine(cache_key: str) -> Optional[DoctrineBlock]:
    """Convenience: look up a doctrine by cache key."""
    return get_doctrine_cache().get(cache_key)


def search_doctrines(query: str, max_results: int = 10) -> List[DoctrineBlock]:
    """Convenience: search doctrines by text query."""
    return get_doctrine_cache().search(query, max_results)


def get_doctrine_stats() -> Dict[str, Any]:
    """Convenience: get doctrine cache statistics."""
    return get_doctrine_cache().get_stats()
