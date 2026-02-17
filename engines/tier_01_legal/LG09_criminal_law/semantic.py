"""
LG09 Criminal Law Engine - Semantic Normalization Dictionary
=============================================================
Deterministic term normalization for criminal law queries.

This module standardizes user input into canonical legal terms before
doctrine lookup. It is strictly deterministic: no ML, no embeddings,
no probabilistic models. Pure dictionary + regex + rule-based mapping.

Coverage:
    - Crime classifications and elements
    - Homicide terminology
    - Property crime terms
    - Drug offense vocabulary
    - White collar crime terms
    - Constitutional rights terminology
    - Procedural terms
    - Sentencing and corrections vocabulary
    - Defense terminology
    - Texas Penal Code specific terms
    - Federal criminal law terms

Author: ECHO OMEGA PRIME
Engine: LG09 Criminal Law
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from loguru import logger


# =============================================================================
# NORMALIZATION RESULT
# =============================================================================

@dataclass
class NormalizationResult:
    """Result of semantic normalization on a query."""
    original_text: str
    normalized_text: str
    mappings_applied: List[Dict[str, str]] = field(default_factory=list)
    canonical_terms: List[str] = field(default_factory=list)
    jurisdiction_hints: List[str] = field(default_factory=list)
    crime_categories: List[str] = field(default_factory=list)
    confidence: float = 1.0
    warnings: List[str] = field(default_factory=list)

    @property
    def was_normalized(self) -> bool:
        return len(self.mappings_applied) > 0

    @property
    def mapping_count(self) -> int:
        return len(self.mappings_applied)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_text": self.original_text,
            "normalized_text": self.normalized_text,
            "was_normalized": self.was_normalized,
            "mapping_count": self.mapping_count,
            "mappings_applied": self.mappings_applied,
            "canonical_terms": self.canonical_terms,
            "jurisdiction_hints": self.jurisdiction_hints,
            "crime_categories": self.crime_categories,
            "confidence": round(self.confidence, 4),
            "warnings": self.warnings,
        }


# =============================================================================
# CRIME CATEGORY ENUM
# =============================================================================

class CrimeCategory(str, Enum):
    HOMICIDE = "homicide"
    ASSAULT = "assault"
    PROPERTY = "property"
    DRUG = "drug"
    WHITE_COLLAR = "white_collar"
    SEX_OFFENSE = "sex_offense"
    DWI = "dwi"
    WEAPONS = "weapons"
    INCHOATE = "inchoate"
    JUVENILE = "juvenile"
    CONSTITUTIONAL = "constitutional"
    PROCEDURAL = "procedural"
    SENTENCING = "sentencing"
    DEFENSE = "defense"
    FEDERAL = "federal"
    TRAFFIC = "traffic"
    CYBER = "cyber"
    DOMESTIC = "domestic"
    PUBLIC_ORDER = "public_order"
    IMMIGRATION = "immigration"


# =============================================================================
# CANONICAL TERM MAPPINGS
# =============================================================================

# Each mapping: { "pattern": regex, "canonical": replacement, "category": CrimeCategory }

HOMICIDE_MAPPINGS: Dict[str, str] = {
    "murder one": "first degree murder",
    "murder 1": "first degree murder",
    "murder 1st": "first degree murder",
    "1st degree murder": "first degree murder",
    "first-degree murder": "first degree murder",
    "murder two": "second degree murder",
    "murder 2": "second degree murder",
    "murder 2nd": "second degree murder",
    "2nd degree murder": "second degree murder",
    "second-degree murder": "second degree murder",
    "murder in the first": "first degree murder",
    "murder in the second": "second degree murder",
    "capital murder charge": "capital murder",
    "death penalty murder": "capital murder",
    "voluntary manslaughter": "voluntary manslaughter",
    "heat of passion killing": "voluntary manslaughter",
    "heat-of-passion": "voluntary manslaughter",
    "passion killing": "voluntary manslaughter",
    "adequate provocation": "voluntary manslaughter",
    "involuntary manslaughter": "involuntary manslaughter",
    "accidental killing": "involuntary manslaughter",
    "unintentional killing": "involuntary manslaughter",
    "reckless homicide": "criminally negligent homicide",
    "negligent homicide": "criminally negligent homicide",
    "vehicular homicide": "vehicular manslaughter",
    "vehicular manslaughter": "vehicular manslaughter",
    "car accident death": "vehicular manslaughter",
    "felony murder rule": "felony murder",
    "felony murder doctrine": "felony murder",
    "killing during felony": "felony murder",
    "death during robbery": "felony murder",
    "depraved heart murder": "depraved heart murder",
    "depraved indifference murder": "depraved heart murder",
    "extreme indifference": "depraved heart murder",
    "premeditated murder": "first degree murder",
    "premeditated killing": "first degree murder",
    "deliberate murder": "first degree murder",
    "willful murder": "first degree murder",
    "cold blooded killing": "first degree murder",
    "assassination": "first degree murder",
    "hired killing": "murder for hire",
    "contract killing": "murder for hire",
    "murder for hire": "murder for hire",
    "serial killing": "serial murder",
    "serial murder": "serial murder",
    "mass murder": "mass murder",
    "mass shooting": "mass murder",
}

ASSAULT_BATTERY_MAPPINGS: Dict[str, str] = {
    "simple assault": "simple assault",
    "misdemeanor assault": "simple assault",
    "assault charge": "assault",
    "agg assault": "aggravated assault",
    "aggravated assault": "aggravated assault",
    "assault with a deadly weapon": "aggravated assault",
    "assault with deadly weapon": "aggravated assault",
    "assault with a weapon": "aggravated assault",
    "awdw": "aggravated assault",
    "assault causing bodily injury": "assault causing bodily injury",
    "assault bodily injury": "assault causing bodily injury",
    "simple battery": "battery",
    "battery charge": "battery",
    "aggravated battery": "aggravated battery",
    "assault on a police officer": "assault on a public servant",
    "assault on cop": "assault on a public servant",
    "assault on officer": "assault on a public servant",
    "assault public servant": "assault on a public servant",
    "domestic assault": "domestic violence assault",
    "domestic battery": "domestic violence assault",
    "dv assault": "domestic violence assault",
    "family violence": "domestic violence assault",
    "family violence assault": "domestic violence assault",
    "strangulation": "assault by strangulation",
    "choking assault": "assault by strangulation",
    "terroristic threat": "terroristic threat",
    "threat of violence": "terroristic threat",
    "menacing": "menacing",
    "stalking": "stalking",
    "harassment": "harassment",
    "criminal threatening": "terroristic threat",
    "intimidation": "intimidation",
    "hate crime assault": "hate crime enhancement",
    "bias-motivated assault": "hate crime enhancement",
}

PROPERTY_CRIME_MAPPINGS: Dict[str, str] = {
    "theft": "theft",
    "stealing": "theft",
    "larceny": "theft",
    "petty theft": "petty theft",
    "petty larceny": "petty theft",
    "shoplifting": "theft shoplifting",
    "shoplifter": "theft shoplifting",
    "grand theft": "grand theft",
    "grand larceny": "grand theft",
    "felony theft": "grand theft",
    "auto theft": "theft of motor vehicle",
    "car theft": "theft of motor vehicle",
    "vehicle theft": "theft of motor vehicle",
    "carjacking": "carjacking",
    "burglary": "burglary",
    "breaking and entering": "burglary",
    "b and e": "burglary",
    "b&e": "burglary",
    "home invasion": "burglary of habitation",
    "burglary of habitation": "burglary of habitation",
    "burglary of building": "burglary of building",
    "commercial burglary": "burglary of building",
    "robbery": "robbery",
    "armed robbery": "aggravated robbery",
    "aggravated robbery": "aggravated robbery",
    "mugging": "robbery",
    "stickup": "robbery",
    "holdup": "robbery",
    "arson": "arson",
    "fire setting": "arson",
    "setting fire": "arson",
    "criminal mischief": "criminal mischief",
    "vandalism": "criminal mischief",
    "property damage": "criminal mischief",
    "criminal trespass": "criminal trespass",
    "trespassing": "criminal trespass",
    "receiving stolen property": "receiving stolen property",
    "possession of stolen goods": "receiving stolen property",
    "fencing stolen goods": "receiving stolen property",
    "embezzlement": "embezzlement",
    "employee theft": "embezzlement",
    "conversion": "embezzlement",
    "identity theft": "identity theft",
    "id theft": "identity theft",
    "identity fraud": "identity theft",
    "credit card fraud": "credit card abuse",
    "cc fraud": "credit card abuse",
    "forgery": "forgery",
    "check fraud": "forgery",
    "counterfeiting": "counterfeiting",
    "fake money": "counterfeiting",
    "extortion": "extortion",
    "blackmail": "extortion",
}

DRUG_OFFENSE_MAPPINGS: Dict[str, str] = {
    "drug possession": "possession of controlled substance",
    "pos controlled substance": "possession of controlled substance",
    "pcs": "possession of controlled substance",
    "possession of drugs": "possession of controlled substance",
    "drug charge": "controlled substance offense",
    "narcotic possession": "possession of controlled substance",
    "narcotics": "controlled substance",
    "controlled substance": "controlled substance",
    "drug distribution": "distribution of controlled substance",
    "drug dealing": "distribution of controlled substance",
    "dealing drugs": "distribution of controlled substance",
    "drug sale": "distribution of controlled substance",
    "selling drugs": "distribution of controlled substance",
    "drug trafficking": "drug trafficking",
    "trafficking": "drug trafficking",
    "drug manufacturing": "manufacture of controlled substance",
    "drug lab": "manufacture of controlled substance",
    "meth lab": "manufacture of controlled substance methamphetamine",
    "cooking meth": "manufacture of controlled substance methamphetamine",
    "marijuana possession": "possession of marijuana",
    "pot possession": "possession of marijuana",
    "weed possession": "possession of marijuana",
    "cannabis possession": "possession of marijuana",
    "marijuana distribution": "distribution of marijuana",
    "cocaine possession": "possession of controlled substance cocaine",
    "crack cocaine": "possession of controlled substance crack cocaine",
    "heroin possession": "possession of controlled substance heroin",
    "fentanyl": "controlled substance fentanyl",
    "meth possession": "possession of controlled substance methamphetamine",
    "methamphetamine": "controlled substance methamphetamine",
    "ecstasy": "controlled substance MDMA",
    "mdma": "controlled substance MDMA",
    "lsd": "controlled substance LSD",
    "prescription fraud": "prescription fraud",
    "doctor shopping": "prescription fraud",
    "drug paraphernalia": "drug paraphernalia",
    "schedule i": "schedule I controlled substance",
    "schedule ii": "schedule II controlled substance",
    "schedule iii": "schedule III controlled substance",
    "schedule iv": "schedule IV controlled substance",
    "schedule v": "schedule V controlled substance",
    "penalty group 1": "Texas penalty group 1",
    "penalty group 2": "Texas penalty group 2",
    "penalty group 3": "Texas penalty group 3",
    "penalty group 4": "Texas penalty group 4",
    "drug free zone": "drug free zone enhancement",
    "school zone": "drug free zone enhancement",
    "intent to distribute": "possession with intent to distribute",
    "pwid": "possession with intent to distribute",
    "constructive possession": "constructive possession",
}

WHITE_COLLAR_MAPPINGS: Dict[str, str] = {
    "wire fraud": "wire fraud 18 USC 1343",
    "mail fraud": "mail fraud 18 USC 1341",
    "bank fraud": "bank fraud 18 USC 1344",
    "securities fraud": "securities fraud",
    "stock fraud": "securities fraud",
    "insider trading": "insider trading",
    "insider trade": "insider trading",
    "money laundering": "money laundering 18 USC 1956",
    "laundering money": "money laundering 18 USC 1956",
    "structuring": "structuring financial transactions",
    "smurfing": "structuring financial transactions",
    "rico": "RICO 18 USC 1961-1968",
    "racketeering": "RICO 18 USC 1961-1968",
    "racketeer influenced": "RICO 18 USC 1961-1968",
    "organized crime": "RICO 18 USC 1961-1968",
    "tax evasion": "tax evasion 26 USC 7201",
    "tax fraud": "tax fraud",
    "tax cheat": "tax evasion 26 USC 7201",
    "bribery": "bribery",
    "public corruption": "public corruption",
    "kickback": "illegal kickback",
    "ponzi scheme": "investment fraud ponzi scheme",
    "pyramid scheme": "investment fraud pyramid scheme",
    "mortgage fraud": "mortgage fraud",
    "healthcare fraud": "healthcare fraud",
    "insurance fraud": "insurance fraud",
    "accounting fraud": "accounting fraud",
    "corporate fraud": "corporate fraud",
    "antitrust": "antitrust violation",
    "price fixing": "antitrust price fixing",
    "bid rigging": "antitrust bid rigging",
    "computer fraud": "computer fraud 18 USC 1030",
    "hacking": "computer fraud 18 USC 1030",
    "cyber crime": "computer fraud 18 USC 1030",
    "conspiracy to defraud": "conspiracy to defraud the United States",
}

DWI_MAPPINGS: Dict[str, str] = {
    "dwi": "driving while intoxicated",
    "dui": "driving under the influence",
    "drunk driving": "driving while intoxicated",
    "driving drunk": "driving while intoxicated",
    "impaired driving": "driving while intoxicated",
    "driving while intoxicated": "driving while intoxicated",
    "driving under influence": "driving under the influence",
    "owi": "operating while intoxicated",
    "oui": "operating under the influence",
    "bac": "blood alcohol concentration",
    "blood alcohol": "blood alcohol concentration",
    "breathalyzer": "chemical breath test",
    "breath test": "chemical breath test",
    "field sobriety": "standardized field sobriety test",
    "field sobriety test": "standardized field sobriety test",
    "sfst": "standardized field sobriety test",
    "walk and turn": "standardized field sobriety test walk and turn",
    "one leg stand": "standardized field sobriety test one leg stand",
    "hgn": "horizontal gaze nystagmus test",
    "nystagmus": "horizontal gaze nystagmus test",
    "implied consent": "implied consent law",
    "refusal to blow": "breath test refusal",
    "license suspension": "administrative license revocation",
    "alr": "administrative license revocation",
    "intoxication assault": "intoxication assault",
    "intoxication manslaughter": "intoxication manslaughter",
    "open container": "open container violation",
    "minor in possession": "minor in possession of alcohol",
    "mip": "minor in possession of alcohol",
    "ignition interlock": "ignition interlock device",
    "iid": "ignition interlock device",
    "repeat dwi": "felony DWI repeat offender",
    "felony dwi": "felony DWI",
    "dwi 3rd": "felony DWI third offense",
    "dwi with child": "DWI with child passenger",
}

CONSTITUTIONAL_MAPPINGS: Dict[str, str] = {
    "fourth amendment": "Fourth Amendment search and seizure",
    "4th amendment": "Fourth Amendment search and seizure",
    "search and seizure": "Fourth Amendment search and seizure",
    "unreasonable search": "Fourth Amendment unreasonable search",
    "illegal search": "Fourth Amendment unreasonable search",
    "warrant requirement": "Fourth Amendment warrant requirement",
    "search warrant": "Fourth Amendment search warrant",
    "warrantless search": "warrantless search exception",
    "probable cause": "probable cause",
    "reasonable suspicion": "reasonable suspicion",
    "terry stop": "Terry stop Terry v Ohio",
    "stop and frisk": "Terry stop Terry v Ohio",
    "terry frisk": "Terry stop Terry v Ohio",
    "plain view doctrine": "plain view doctrine",
    "exigent circumstances": "exigent circumstances exception",
    "hot pursuit": "exigent circumstances hot pursuit",
    "consent search": "consent search exception",
    "automobile exception": "automobile exception",
    "vehicle search": "automobile exception",
    "car search": "automobile exception",
    "inventory search": "inventory search exception",
    "search incident to arrest": "search incident to arrest",
    "exclusionary rule": "exclusionary rule Mapp v Ohio",
    "fruit of poisonous tree": "fruit of the poisonous tree Wong Sun",
    "good faith exception": "good faith exception Leon",
    "inevitable discovery": "inevitable discovery exception",
    "independent source": "independent source doctrine",
    "fifth amendment": "Fifth Amendment self-incrimination",
    "5th amendment": "Fifth Amendment self-incrimination",
    "self incrimination": "Fifth Amendment self-incrimination",
    "right to remain silent": "Fifth Amendment right to silence",
    "right to silence": "Fifth Amendment right to silence",
    "miranda": "Miranda rights Miranda v Arizona",
    "miranda rights": "Miranda rights Miranda v Arizona",
    "miranda warning": "Miranda warnings",
    "miranda waiver": "Miranda waiver",
    "custodial interrogation": "custodial interrogation",
    "in custody": "custody determination Miranda",
    "double jeopardy": "Fifth Amendment double jeopardy",
    "grand jury": "Fifth Amendment grand jury",
    "due process": "Fifth Amendment due process",
    "sixth amendment": "Sixth Amendment right to counsel",
    "6th amendment": "Sixth Amendment right to counsel",
    "right to counsel": "Sixth Amendment right to counsel",
    "right to attorney": "Sixth Amendment right to counsel",
    "right to lawyer": "Sixth Amendment right to counsel",
    "gideon": "Sixth Amendment right to counsel Gideon v Wainwright",
    "public defender": "Sixth Amendment appointed counsel",
    "ineffective assistance": "ineffective assistance of counsel Strickland",
    "iac": "ineffective assistance of counsel Strickland",
    "speedy trial": "Sixth Amendment speedy trial",
    "confrontation clause": "Sixth Amendment confrontation clause",
    "right to confront witnesses": "Sixth Amendment confrontation clause",
    "cross examination": "Sixth Amendment confrontation clause",
    "jury trial": "Sixth Amendment jury trial right",
    "right to jury": "Sixth Amendment jury trial right",
    "eighth amendment": "Eighth Amendment cruel and unusual",
    "8th amendment": "Eighth Amendment cruel and unusual",
    "cruel and unusual": "Eighth Amendment cruel and unusual punishment",
    "excessive bail": "Eighth Amendment excessive bail",
    "excessive fines": "Eighth Amendment excessive fines",
    "proportionality": "Eighth Amendment proportionality",
    "equal protection": "Fourteenth Amendment equal protection",
    "14th amendment": "Fourteenth Amendment due process equal protection",
}

DEFENSE_MAPPINGS: Dict[str, str] = {
    "self defense": "self-defense",
    "self-defense": "self-defense",
    "defense of others": "defense of third persons",
    "defending someone": "defense of third persons",
    "castle doctrine": "castle doctrine",
    "home defense": "castle doctrine",
    "stand your ground": "stand your ground",
    "no duty to retreat": "stand your ground",
    "duty to retreat": "duty to retreat",
    "insanity defense": "insanity defense",
    "insanity plea": "insanity defense",
    "not guilty by reason of insanity": "NGRI insanity defense",
    "ngri": "NGRI insanity defense",
    "m'naghten": "M'Naghten insanity test",
    "mcnaghten": "M'Naghten insanity test",
    "irresistible impulse": "irresistible impulse insanity test",
    "diminished capacity": "diminished capacity defense",
    "guilty but mentally ill": "guilty but mentally ill",
    "gbmi": "guilty but mentally ill",
    "duress": "duress defense",
    "coercion defense": "duress defense",
    "under duress": "duress defense",
    "necessity": "necessity defense",
    "choice of evils": "necessity defense choice of evils",
    "entrapment": "entrapment defense",
    "police entrapment": "entrapment defense",
    "sting operation": "entrapment defense",
    "intoxication defense": "intoxication defense",
    "voluntary intoxication": "voluntary intoxication defense",
    "involuntary intoxication": "involuntary intoxication defense",
    "mistake of fact": "mistake of fact defense",
    "mistake of law": "mistake of law defense",
    "statute of limitations": "statute of limitations defense",
    "sol": "statute of limitations defense",
    "time barred": "statute of limitations defense",
    "alibi": "alibi defense",
    "alibi defense": "alibi defense",
    "consent defense": "consent defense",
    "age defense": "infancy defense",
    "infancy defense": "infancy defense",
    "too young to charge": "infancy defense",
    "diplomatic immunity": "diplomatic immunity defense",
    "immunity": "immunity",
    "prosecutorial immunity": "prosecutorial immunity",
    "qualified immunity": "qualified immunity",
    "sovereign immunity": "sovereign immunity",
    "justification": "justification defense",
    "excuse": "excuse defense",
    "affirmative defense": "affirmative defense",
    "automatism": "automatism defense",
    "sleepwalking defense": "automatism defense",
}

SENTENCING_MAPPINGS: Dict[str, str] = {
    "sentencing guidelines": "sentencing guidelines",
    "federal sentencing": "federal sentencing guidelines USSG",
    "ussg": "federal sentencing guidelines USSG",
    "mandatory minimum": "mandatory minimum sentence",
    "mandatory sentence": "mandatory minimum sentence",
    "three strikes": "three strikes habitual offender",
    "habitual offender": "habitual offender enhancement",
    "repeat offender": "habitual offender enhancement",
    "career criminal": "career offender USSG",
    "career offender": "career offender USSG",
    "death penalty": "capital punishment death penalty",
    "capital punishment": "capital punishment death penalty",
    "execution": "capital punishment death penalty",
    "lethal injection": "capital punishment method lethal injection",
    "life sentence": "life imprisonment",
    "life without parole": "life without parole LWOP",
    "lwop": "life without parole LWOP",
    "concurrent sentence": "concurrent sentencing",
    "consecutive sentence": "consecutive sentencing",
    "stacking sentences": "consecutive sentencing",
    "enhancement": "sentencing enhancement",
    "sentence enhancement": "sentencing enhancement",
    "downward departure": "downward departure from guidelines",
    "substantial assistance": "substantial assistance departure",
    "cooperation agreement": "substantial assistance departure",
    "restitution": "restitution order",
    "fine": "criminal fine",
    "community service": "community service sentence",
    "probation": "probation",
    "deferred adjudication": "deferred adjudication",
    "community supervision": "community supervision probation",
    "parole": "parole",
    "early release": "parole early release",
    "good time": "good time credit",
    "time served": "credit for time served",
    "jail credit": "credit for time served",
    "expungement": "expungement of criminal record",
    "expunge record": "expungement of criminal record",
    "record sealing": "record sealing nondisclosure",
    "nondisclosure": "order of nondisclosure",
    "record clearing": "expungement of criminal record",
    "clean record": "expungement of criminal record",
    "sex offender registration": "sex offender registration SORNA",
    "sorna": "sex offender registration SORNA",
    "megan's law": "sex offender registration notification",
    "registry": "sex offender registration",
}

PROCEDURAL_MAPPINGS: Dict[str, str] = {
    "arraignment": "arraignment initial appearance",
    "initial appearance": "arraignment initial appearance",
    "bail": "bail bond",
    "bail bond": "bail bond",
    "bond hearing": "bail bond hearing",
    "pretrial detention": "pretrial detention",
    "no bond": "pretrial detention denial of bail",
    "preliminary hearing": "preliminary hearing probable cause",
    "indictment": "grand jury indictment",
    "information": "criminal information charging document",
    "complaint": "criminal complaint",
    "plea deal": "plea bargain agreement",
    "plea bargain": "plea bargain agreement",
    "plea agreement": "plea bargain agreement",
    "guilty plea": "guilty plea",
    "not guilty plea": "not guilty plea",
    "nolo contendere": "nolo contendere no contest plea",
    "no contest": "nolo contendere no contest plea",
    "alford plea": "Alford plea North Carolina v Alford",
    "trial": "criminal trial",
    "jury trial right": "Sixth Amendment jury trial right",
    "bench trial": "bench trial judge trial",
    "voir dire": "voir dire jury selection",
    "jury selection": "voir dire jury selection",
    "peremptory challenge": "peremptory challenge Batson",
    "batson challenge": "Batson challenge racial jury selection",
    "opening statement": "opening statement trial procedure",
    "closing argument": "closing argument trial procedure",
    "burden of proof": "burden of proof beyond reasonable doubt",
    "beyond reasonable doubt": "beyond reasonable doubt standard",
    "brd": "beyond reasonable doubt standard",
    "preponderance": "preponderance of evidence standard",
    "clear and convincing": "clear and convincing evidence standard",
    "directed verdict": "motion for directed verdict acquittal",
    "acquittal": "acquittal not guilty verdict",
    "conviction": "conviction guilty verdict",
    "mistrial": "mistrial declaration",
    "hung jury": "hung jury mistrial",
    "appeal": "criminal appeal",
    "appellate": "criminal appeal appellate review",
    "habeas corpus": "habeas corpus 28 USC 2254",
    "habeas": "habeas corpus 28 USC 2254",
    "writ of habeas": "habeas corpus 28 USC 2254",
    "post conviction": "post-conviction relief",
    "pcr": "post-conviction relief",
    "discovery": "criminal discovery Brady",
    "brady material": "Brady disclosure Brady v Maryland",
    "brady violation": "Brady violation suppression of evidence",
    "giglio": "Giglio impeachment evidence",
    "jencks": "Jencks Act witness statements",
    "speedy trial act": "Speedy Trial Act 18 USC 3161",
    "continuance": "continuance delay of trial",
    "change of venue": "change of venue motion",
    "suppression motion": "motion to suppress evidence",
    "motion to suppress": "motion to suppress evidence",
    "motion in limine": "motion in limine exclude evidence",
    "severance": "severance of defendants or charges",
}

JUVENILE_MAPPINGS: Dict[str, str] = {
    "juvenile": "juvenile justice",
    "minor": "juvenile offender",
    "juvenile delinquent": "juvenile delinquent conduct",
    "delinquent conduct": "juvenile delinquent conduct",
    "status offense": "juvenile status offense",
    "truancy": "juvenile status offense truancy",
    "curfew violation": "juvenile status offense curfew",
    "runaway": "juvenile status offense runaway",
    "certification as adult": "juvenile certification transfer to adult court",
    "transfer to adult court": "juvenile certification transfer to adult court",
    "waiver to adult court": "juvenile certification transfer to adult court",
    "juvenile detention": "juvenile detention facility",
    "juvenile probation": "juvenile probation supervision",
    "juvenile record": "juvenile record confidentiality",
    "sealing juvenile record": "juvenile record sealing",
    "youthful offender": "youthful offender program",
    "juvenile diversion": "juvenile diversion program",
    "disposition hearing": "juvenile disposition hearing",
    "adjudication hearing": "juvenile adjudication hearing",
    "tjjd": "Texas Juvenile Justice Department",
}

INCHOATE_MAPPINGS: Dict[str, str] = {
    "attempt": "criminal attempt",
    "attempted murder": "attempted murder",
    "attempted robbery": "attempted robbery",
    "conspiracy": "criminal conspiracy",
    "conspiracy charge": "criminal conspiracy",
    "drug conspiracy": "drug conspiracy",
    "rico conspiracy": "RICO conspiracy 18 USC 1962",
    "solicitation": "criminal solicitation",
    "solicitation of murder": "solicitation of capital murder",
    "aiding and abetting": "aiding and abetting complicity",
    "accomplice": "accomplice liability",
    "accessory": "accessory to crime",
    "accessory after the fact": "accessory after the fact",
    "accessory before the fact": "accessory before the fact",
    "getaway driver": "accomplice liability aiding and abetting",
    "lookout": "accomplice liability aiding and abetting",
}

TEXAS_SPECIFIC_MAPPINGS: Dict[str, str] = {
    "texas penal code": "Texas Penal Code",
    "tpc": "Texas Penal Code",
    "code of criminal procedure": "Texas Code of Criminal Procedure",
    "tccp": "Texas Code of Criminal Procedure",
    "state jail felony": "Texas state jail felony",
    "sjf": "Texas state jail felony",
    "third degree felony": "Texas third degree felony",
    "second degree felony": "Texas second degree felony",
    "first degree felony": "Texas first degree felony",
    "class a misdemeanor": "Texas Class A misdemeanor",
    "class b misdemeanor": "Texas Class B misdemeanor",
    "class c misdemeanor": "Texas Class C misdemeanor",
    "texas rangers": "Texas Rangers law enforcement",
    "tdcj": "Texas Department of Criminal Justice",
    "texas prison": "Texas Department of Criminal Justice",
    "texas parole": "Texas Board of Pardons and Paroles",
    "deadly conduct": "Texas deadly conduct TPC 22.05",
    "evading arrest": "Texas evading arrest TPC 38.04",
    "unauthorized use of vehicle": "Texas UUMV TPC 31.07",
    "uumv": "Texas UUMV TPC 31.07",
    "criminal nonsupport": "Texas criminal nonsupport TPC 25.05",
    "organized criminal activity": "Texas engaging in organized criminal activity TPC 71.02",
    "engaging in organized crime": "Texas engaging in organized criminal activity TPC 71.02",
    "protective order violation": "Texas protective order violation TPC 25.07",
    "continuous violence against family": "Texas continuous violence against family TPC 25.11",
    "online solicitation of minor": "Texas online solicitation of minor TPC 33.021",
    "improper relationship": "Texas improper relationship educator student TPC 21.12",
    "continuous sexual abuse": "Texas continuous sexual abuse of child TPC 21.02",
    "intoxication assault texas": "Texas intoxication assault TPC 49.07",
    "intoxication manslaughter texas": "Texas intoxication manslaughter TPC 49.08",
    "credit card abuse": "Texas credit card or debit card abuse TPC 32.31",
    "theft of service": "Texas theft of service TPC 31.04",
    "hindering apprehension": "Texas hindering apprehension TPC 38.05",
    "tampering with evidence": "Texas tampering with evidence TPC 37.09",
    "tampering with witness": "Texas tampering with witness TPC 36.05",
    "perjury": "perjury TPC 37.02",
    "false report to police": "Texas false report to peace officer TPC 37.08",
    "failure to identify": "Texas failure to identify TPC 38.02",
    "resisting arrest": "Texas resisting arrest TPC 38.03",
    "escape": "Texas escape TPC 38.06",
    "bail jumping": "Texas bail jumping failure to appear TPC 38.10",
    "retaliation": "Texas retaliation TPC 36.06",
    "obstruction": "Texas obstruction or retaliation TPC 36.06",
}


# =============================================================================
# ALL MAPPINGS COMBINED
# =============================================================================

ALL_MAPPINGS: Dict[str, str] = {}
ALL_MAPPINGS.update(HOMICIDE_MAPPINGS)
ALL_MAPPINGS.update(ASSAULT_BATTERY_MAPPINGS)
ALL_MAPPINGS.update(PROPERTY_CRIME_MAPPINGS)
ALL_MAPPINGS.update(DRUG_OFFENSE_MAPPINGS)
ALL_MAPPINGS.update(WHITE_COLLAR_MAPPINGS)
ALL_MAPPINGS.update(DWI_MAPPINGS)
ALL_MAPPINGS.update(CONSTITUTIONAL_MAPPINGS)
ALL_MAPPINGS.update(DEFENSE_MAPPINGS)
ALL_MAPPINGS.update(SENTENCING_MAPPINGS)
ALL_MAPPINGS.update(PROCEDURAL_MAPPINGS)
ALL_MAPPINGS.update(JUVENILE_MAPPINGS)
ALL_MAPPINGS.update(INCHOATE_MAPPINGS)
ALL_MAPPINGS.update(TEXAS_SPECIFIC_MAPPINGS)


# =============================================================================
# CATEGORY DETECTION PATTERNS
# =============================================================================

CATEGORY_PATTERNS: Dict[CrimeCategory, List[str]] = {
    CrimeCategory.HOMICIDE: [
        r"\bmurder\b", r"\bhomicide\b", r"\bmanslaughter\b", r"\bkilling\b",
        r"\bdepraved heart\b", r"\bfelony murder\b", r"\bcapital murder\b",
    ],
    CrimeCategory.ASSAULT: [
        r"\bassault\b", r"\bbattery\b", r"\bstrangulation\b", r"\bstalking\b",
        r"\bmenacing\b", r"\bharassment\b", r"\bintimidation\b", r"\bthreat\b",
    ],
    CrimeCategory.PROPERTY: [
        r"\btheft\b", r"\bburglary\b", r"\brobbery\b", r"\barson\b", r"\bvandalism\b",
        r"\btrespass\b", r"\bshoplifting\b", r"\blarceny\b", r"\bstolen\b",
        r"\bforgery\b", r"\bcounterfeit\b", r"\bextortion\b",
    ],
    CrimeCategory.DRUG: [
        r"\bdrug\b", r"\bnarcotics?\b", r"\bcontrolled substance\b", r"\bmarijuana\b",
        r"\bcocaine\b", r"\bheroin\b", r"\bmeth\b", r"\bfentanyl\b", r"\bpcs\b",
        r"\bpossession\b.*\b(drug|substance|marijuana)\b", r"\btrafficking\b",
        r"\bschedule [iv]+\b", r"\bpenalty group\b",
    ],
    CrimeCategory.WHITE_COLLAR: [
        r"\bfraud\b", r"\bembezzlement\b", r"\bmoney laundering\b", r"\brico\b",
        r"\bracketeering\b", r"\binsider trading\b", r"\bbribery\b", r"\bcorruption\b",
        r"\bponzi\b", r"\bscheme\b", r"\bantitrust\b",
    ],
    CrimeCategory.SEX_OFFENSE: [
        r"\bsexual assault\b", r"\brape\b", r"\bindecency\b", r"\bsex offend\b",
        r"\bchild exploitation\b", r"\bsolicitation of minor\b",
        r"\bcontinuous sexual abuse\b", r"\bregistration\b.*\bsex\b",
    ],
    CrimeCategory.DWI: [
        r"\bdwi\b", r"\bdui\b", r"\bdrunk driv\b", r"\bimpaired driv\b",
        r"\bblood alcohol\b", r"\bbac\b", r"\bbreathalyzer\b", r"\bfield sobriety\b",
        r"\bintoxication\b", r"\bignition interlock\b",
    ],
    CrimeCategory.WEAPONS: [
        r"\bweapon\b", r"\bfirearm\b", r"\bgun\b", r"\bpistol\b", r"\brifle\b",
        r"\bshotgun\b", r"\bconcealed carry\b", r"\bfelon.*possession\b",
        r"\bprohibited weapon\b",
    ],
    CrimeCategory.INCHOATE: [
        r"\battempt\b", r"\bconspiracy\b", r"\bsolicitation\b",
        r"\baiding and abetting\b", r"\baccomplice\b", r"\baccessory\b",
    ],
    CrimeCategory.JUVENILE: [
        r"\bjuvenile\b", r"\bminor\b.*\boffend\b", r"\bdelinquent\b",
        r"\bstatus offense\b", r"\bcertification.*adult\b", r"\btjjd\b",
    ],
    CrimeCategory.CONSTITUTIONAL: [
        r"\bamendment\b", r"\bconstitutional\b", r"\bsearch and seizure\b",
        r"\bmiranda\b", r"\bdue process\b", r"\bequal protection\b",
        r"\bexclusionary rule\b", r"\bwarrant\b", r"\bprobable cause\b",
    ],
    CrimeCategory.PROCEDURAL: [
        r"\barraignment\b", r"\bbail\b", r"\bindictment\b", r"\bplea\b",
        r"\btrial\b", r"\bjury\b", r"\bappeal\b", r"\bhabeas\b",
        r"\bbrady\b", r"\bdiscovery\b", r"\bsuppress\b", r"\bmotion\b",
    ],
    CrimeCategory.SENTENCING: [
        r"\bsentencing\b", r"\bmandatory minimum\b", r"\bthree strikes\b",
        r"\bdeath penalty\b", r"\bprobation\b", r"\bparole\b",
        r"\bexpungement\b", r"\bnondisclosure\b", r"\brestitution\b",
    ],
    CrimeCategory.DEFENSE: [
        r"\bself[- ]defense\b", r"\binsanity\b", r"\bduress\b",
        r"\bnecessity\b", r"\bentrapment\b", r"\bcastle doctrine\b",
        r"\bstand your ground\b", r"\baffirmative defense\b",
        r"\bdiminished capacity\b",
    ],
    CrimeCategory.DOMESTIC: [
        r"\bdomestic violence\b", r"\bfamily violence\b", r"\bprotective order\b",
        r"\brestraining order\b", r"\bdomestic assault\b",
    ],
    CrimeCategory.CYBER: [
        r"\bcyber\b", r"\bhacking\b", r"\bcomputer fraud\b", r"\bidentity theft\b",
        r"\bphishing\b", r"\bransomware\b",
    ],
}

# =============================================================================
# JURISDICTION DETECTION PATTERNS
# =============================================================================

JURISDICTION_PATTERNS: Dict[str, List[str]] = {
    "federal": [
        r"\bfederal\b", r"\busc\b", r"\bunited states code\b",
        r"\bcircuit court\b", r"\bdistrict court\b", r"\bfbi\b",
        r"\bdea\b", r"\batf\b", r"\bussg\b", r"\bsentencing guideline\b",
        r"\bsupreme court\b", r"\b18 usc\b", r"\b21 usc\b",
        r"\btitle 18\b", r"\btitle 21\b",
    ],
    "texas": [
        r"\btexas\b", r"\btpc\b", r"\btccp\b", r"\btx\b",
        r"\bstate jail felony\b", r"\btdcj\b", r"\btexas ranger\b",
        r"\btexas penal\b", r"\bpenalty group\b",
        r"\bclass [abc] misdemeanor\b",
    ],
    "model_penal_code": [
        r"\bmodel penal code\b", r"\bmpc\b", r"\bali\b",
    ],
}


# =============================================================================
# NORMALIZATION ENGINE
# =============================================================================

class SemanticNormalizer:
    """
    Deterministic semantic normalizer for criminal law queries.

    Rules:
    1. Case-insensitive matching
    2. Longest match first (greedy)
    3. No probabilistic inference
    4. No ML models
    5. Pure dictionary + regex
    """

    def __init__(self):
        # Sort mappings by key length (longest first) for greedy matching
        self._sorted_mappings: List[Tuple[str, str]] = sorted(
            ALL_MAPPINGS.items(),
            key=lambda x: len(x[0]),
            reverse=True,
        )
        # Compile category patterns
        self._category_patterns: Dict[CrimeCategory, List[re.Pattern]] = {}
        for cat, patterns in CATEGORY_PATTERNS.items():
            self._category_patterns[cat] = [re.compile(p, re.IGNORECASE) for p in patterns]

        # Compile jurisdiction patterns
        self._jurisdiction_patterns: Dict[str, List[re.Pattern]] = {}
        for jur, patterns in JURISDICTION_PATTERNS.items():
            self._jurisdiction_patterns[jur] = [re.compile(p, re.IGNORECASE) for p in patterns]

        logger.info(
            f"SemanticNormalizer initialized: {len(ALL_MAPPINGS)} mappings, "
            f"{len(CATEGORY_PATTERNS)} categories, {len(JURISDICTION_PATTERNS)} jurisdictions"
        )

    def normalize(self, text: str) -> NormalizationResult:
        """
        Normalize a query string using criminal law semantic mappings.

        Args:
            text: Raw user query text

        Returns:
            NormalizationResult with normalized text and metadata
        """
        if not text or not text.strip():
            return NormalizationResult(
                original_text=text,
                normalized_text=text,
                warnings=["Empty input text"],
            )

        original = text.strip()
        working = original.lower()
        mappings_applied: List[Dict[str, str]] = []
        canonical_terms: Set[str] = set()

        # Apply mappings (longest first)
        for key, canonical in self._sorted_mappings:
            pattern = re.compile(r"\b" + re.escape(key) + r"\b", re.IGNORECASE)
            if pattern.search(working):
                working = pattern.sub(canonical, working)
                mappings_applied.append({"from": key, "to": canonical})
                canonical_terms.add(canonical)

        # Detect crime categories
        categories = self._detect_categories(original)

        # Detect jurisdictions
        jurisdictions = self._detect_jurisdictions(original)

        # Build result
        result = NormalizationResult(
            original_text=original,
            normalized_text=working,
            mappings_applied=mappings_applied,
            canonical_terms=sorted(canonical_terms),
            jurisdiction_hints=jurisdictions,
            crime_categories=[c.value for c in categories],
            confidence=self._calculate_confidence(mappings_applied, categories),
        )

        if not mappings_applied and not categories:
            result.warnings.append("No criminal law terms detected in query")

        logger.debug(
            f"Normalized: '{original[:80]}' -> {len(mappings_applied)} mappings, "
            f"{len(categories)} categories, {len(jurisdictions)} jurisdictions"
        )

        return result

    def _detect_categories(self, text: str) -> List[CrimeCategory]:
        """Detect crime categories present in the text."""
        detected: List[CrimeCategory] = []
        for cat, patterns in self._category_patterns.items():
            for pattern in patterns:
                if pattern.search(text):
                    detected.append(cat)
                    break
        return detected

    def _detect_jurisdictions(self, text: str) -> List[str]:
        """Detect jurisdictional hints in the text."""
        detected: List[str] = []
        for jur, patterns in self._jurisdiction_patterns.items():
            for pattern in patterns:
                if pattern.search(text):
                    detected.append(jur)
                    break
        return detected

    def _calculate_confidence(
        self,
        mappings: List[Dict[str, str]],
        categories: List[CrimeCategory],
    ) -> float:
        """Calculate normalization confidence score."""
        if not mappings and not categories:
            return 0.3
        score = 0.5
        if mappings:
            score += min(0.3, len(mappings) * 0.05)
        if categories:
            score += min(0.2, len(categories) * 0.05)
        return min(1.0, score)

    def get_mapping_count(self) -> int:
        """Return total number of semantic mappings."""
        return len(ALL_MAPPINGS)

    def get_categories(self) -> List[str]:
        """Return all crime category names."""
        return [c.value for c in CrimeCategory]

    def search_mappings(self, term: str) -> List[Dict[str, str]]:
        """Search for mappings containing a term."""
        term_lower = term.lower()
        results = []
        for key, canonical in ALL_MAPPINGS.items():
            if term_lower in key.lower() or term_lower in canonical.lower():
                results.append({"term": key, "canonical": canonical})
        return results

    def get_stats(self) -> Dict[str, Any]:
        """Return normalizer statistics."""
        category_counts = {cat.value: len(patterns) for cat, patterns in CATEGORY_PATTERNS.items()}
        return {
            "total_mappings": len(ALL_MAPPINGS),
            "mapping_groups": {
                "homicide": len(HOMICIDE_MAPPINGS),
                "assault_battery": len(ASSAULT_BATTERY_MAPPINGS),
                "property_crimes": len(PROPERTY_CRIME_MAPPINGS),
                "drug_offenses": len(DRUG_OFFENSE_MAPPINGS),
                "white_collar": len(WHITE_COLLAR_MAPPINGS),
                "dwi": len(DWI_MAPPINGS),
                "constitutional": len(CONSTITUTIONAL_MAPPINGS),
                "defense": len(DEFENSE_MAPPINGS),
                "sentencing": len(SENTENCING_MAPPINGS),
                "procedural": len(PROCEDURAL_MAPPINGS),
                "juvenile": len(JUVENILE_MAPPINGS),
                "inchoate": len(INCHOATE_MAPPINGS),
                "texas_specific": len(TEXAS_SPECIFIC_MAPPINGS),
            },
            "categories": len(CrimeCategory),
            "category_patterns": category_counts,
            "jurisdictions": list(JURISDICTION_PATTERNS.keys()),
        }


# =============================================================================
# MODULE-LEVEL CONVENIENCE
# =============================================================================

_normalizer: Optional[SemanticNormalizer] = None


def get_normalizer() -> SemanticNormalizer:
    """Get or create the singleton normalizer."""
    global _normalizer
    if _normalizer is None:
        _normalizer = SemanticNormalizer()
    return _normalizer


def normalize_semantics(text: str) -> NormalizationResult:
    """Convenience function: normalize text using the singleton normalizer."""
    return get_normalizer().normalize(text)
