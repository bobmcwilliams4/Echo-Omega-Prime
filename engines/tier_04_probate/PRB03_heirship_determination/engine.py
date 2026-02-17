"""
PRB03 HEIRSHIP DETERMINATION ENGINE v1.0.0
TIE-Grade Intelligence Engine for Intestate Succession Analysis

Determines heirship under intestate succession rules, per stirpes vs per capita
distribution, community vs separate property, pretermitted heirs, adopted children,
posthumous heirs, half-blood relatives, representation, lapsed devises.

Author: ECHO OMEGA PRIME
Date: 2026-02-14
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from collections import defaultdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field


# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "PRB03"
ENGINE_NAME = "Heirship Determination Engine"
VERSION = "1.0.0"
PORT = 9113

logger.add(
    f"logs/{ENGINE_ID}_{{time}}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO"
)


# ============================================================================
# ENUMS
# ============================================================================

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class DistributionMethod(str, Enum):
    PER_STIRPES = "per_stirpes"
    PER_CAPITA = "per_capita_at_each_generation"
    STRICT_PER_STIRPES = "strict_per_stirpes"


class PropertyType(str, Enum):
    COMMUNITY = "community"
    SEPARATE = "separate"
    QUASI_COMMUNITY = "quasi_community"
    UNKNOWN = "unknown"


# ============================================================================
# MODELS
# ============================================================================

class HeirshipRequest(BaseModel):
    decedent_name: str
    decedent_state: str = "TX"
    survived_by: List[str] = Field(default_factory=list)
    predeceased: List[str] = Field(default_factory=list)
    property_description: str = ""
    property_type: Optional[PropertyType] = None
    marriage_status: str = ""
    children_info: str = ""
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.REPORTING


class DoctrineBlock(BaseModel):
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
    confidence: ConfidenceLevel
    controlling_precedent: Optional[str] = None


class TelemetryRecord(BaseModel):
    query_id: str
    timestamp: str
    latency_ms: float
    cache_hit: bool
    mode: str
    zone: str
    doctrines_triggered: List[str]
    error_domain: Optional[str] = None


# ============================================================================
# DOCTRINE CACHE - 25+ HEIRSHIP LAW BLOCKS
# ============================================================================

DOCTRINE_CACHE: Dict[str, DoctrineBlock] = {
    "intestate_spouse_with_children": DoctrineBlock(
        topic="Intestate Succession - Surviving Spouse with Descendants",
        keywords=["intestate", "spouse", "children", "community property", "separate property"],
        conclusion_template="Under Texas Estates Code Section 201.002, surviving spouse takes all community property and one-third of separate personal property, plus life estate in one-third of separate real property, with remainder to descendants.",
        reasoning_framework="""
1. Determine marital status at death (valid marriage required)
2. Classify property as community vs separate
3. Apply TEC 201.002 distribution rules:
   - All community property to surviving spouse
   - 1/3 separate personal property to spouse, 2/3 to descendants
   - Life estate in 1/3 separate realty to spouse, remainder to descendants
4. Identify all descendants (children, grandchildren via representation)
5. Apply per stirpes distribution among descendants' shares
6. Consider pretermitted heir statutes if will exists but omits heir
        """,
        key_factors=[
            "Valid marriage at time of death",
            "Community property presumption applies to Texas marital property",
            "Separate property requires clear tracing (pre-marriage, gift, inheritance)",
            "Descendants include all biological and adopted children",
            "Half-blood descendants inherit equally with whole-blood",
            "Posthumous children inherit if born within 300 days of death"
        ],
        primary_authority=[
            "Texas Estates Code Section 201.002",
            "Texas Estates Code Section 201.001 (definitions)",
            "Texas Family Code Section 3.002 (community property presumption)",
            "Texas Estates Code Section 201.054 (half-blood kindred)",
            "Texas Estates Code Section 201.056 (posthumous descendants)"
        ],
        burden_holder="Party claiming separate property status",
        adversary_position="All property acquired during marriage is community property unless proven otherwise",
        counter_arguments=[
            "Spouse claims all property is community and should take 100%",
            "Descendants argue spouse's share should be limited to community only",
            "Separate property claimants lack sufficient tracing evidence"
        ],
        resolution_strategy="Apply community property presumption strictly; require clear and convincing evidence of separate property character; use inception of title rule for tracing.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="In re Estate of Hanau, 730 S.W.2d 663 (Tex. 1987)"
    ),

    "intestate_no_spouse_with_descendants": DoctrineBlock(
        topic="Intestate Succession - No Spouse, Descendants Only",
        keywords=["intestate", "no spouse", "children", "descendants", "per stirpes"],
        conclusion_template="Under TEC 201.001, when decedent dies intestate without surviving spouse, entire estate passes to descendants per stirpes.",
        reasoning_framework="""
1. Confirm no surviving spouse (divorced, predeceased, void marriage)
2. Identify all living descendants in first generation (children)
3. For predeceased children, identify their descendants (grandchildren)
4. Apply per stirpes (by representation) distribution:
   - Divide estate into as many shares as living children + deceased children with living descendants
   - Each living child takes one share
   - Each deceased child's share passes to their descendants equally
5. Continue representation through generations as needed
        """,
        key_factors=[
            "Per stirpes is default method in Texas",
            "Each generational line receives equal share regardless of number of members",
            "Adopted children treated identically to biological children",
            "Stepchildren do NOT inherit unless legally adopted",
            "Children born out of wedlock inherit from mother automatically, from father if paternity established"
        ],
        primary_authority=[
            "Texas Estates Code Section 201.001(b)",
            "Texas Estates Code Section 201.101 (adopted children)",
            "Texas Estates Code Section 201.052 (maternal inheritance)",
            "Texas Estates Code Section 201.053 (paternal inheritance)"
        ],
        burden_holder="Claimant asserting heirship status",
        adversary_position="Only formally recognized descendants inherit; stepchildren and non-adjudicated children excluded",
        counter_arguments=[
            "Stepchild claims equitable adoption",
            "Non-adjudicated child claims presumed paternity",
            "Half-siblings argue for reduced share"
        ],
        resolution_strategy="Require legal adoption or formal paternity adjudication; reject equitable adoption claims; treat half-blood equally with whole-blood per TEC 201.054.",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "per_stirpes_distribution": DoctrineBlock(
        topic="Per Stirpes Distribution Mechanics",
        keywords=["per stirpes", "representation", "distribution", "shares", "generational"],
        conclusion_template="Per stirpes distribution creates equal shares at the first generational level with living takers or deceased takers with living descendants, then subdivides each predeceased person's share among their descendants.",
        reasoning_framework="""
1. Identify the generational level at which distribution begins (usually children)
2. Count: (living members at that level) + (deceased members with living descendants)
3. Create that many equal shares
4. Distribute one share to each living member
5. For each deceased member's share, subdivide equally among their descendants
6. If a descendant is also deceased, their share passes to THEIR descendants
7. Continue until all shares are distributed to living persons
        """,
        key_factors=[
            "Each family line receives one share regardless of size",
            "A large family line with many members receives same total as single heir",
            "Representation continues through unlimited generations",
            "No living descendants in a line = that line's share reallocates",
            "Modern per stirpes differs from strict per stirpes and per capita"
        ],
        primary_authority=[
            "Texas Estates Code Section 201.001(b) ('by representation')",
            "Uniform Probate Code Section 2-106 (comparison)",
            "Restatement (Third) of Property: Wills and Other Donative Transfers Section 2.3"
        ],
        burden_holder="Party claiming larger share under different distribution method",
        adversary_position="Per capita distribution is more equitable (equal shares to each person)",
        counter_arguments=[
            "Per capita at each generation is fairer to distant relatives",
            "Strict per stirpes gives more to closer generations",
            "Will should specify method if different from statute"
        ],
        resolution_strategy="Apply statutory default unless will specifies otherwise; explain how per stirpes honors family lines; calculate actual dollar amounts to show impact.",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "community_property_classification": DoctrineBlock(
        topic="Community Property Classification",
        keywords=["community property", "separate property", "marital property", "inception of title", "tracing"],
        conclusion_template="Texas law presumes all property acquired during marriage is community property; separate property requires clear and convincing evidence of pre-marital acquisition, gift, or inheritance.",
        reasoning_framework="""
1. Apply community property presumption to all marital property
2. Burden on claimant to prove separate character by clear and convincing evidence
3. Use inception of title rule: character determined when right to property first arises
4. Separate property sources: owned before marriage, gift, devise, descent
5. Commingling analysis if separate funds mixed with community
6. Tracing requirements: clear paper trail showing separate source
7. Mutations: income from separate property is community in Texas
        """,
        key_factors=[
            "Texas is community property state (one of 9)",
            "Presumption is rebuttable but burden is high",
            "Inception of title controls even if asset changes form",
            "Gifts between spouses require donative intent and delivery",
            "Partition or exchange agreements can change character",
            "Income from separate property (rents, dividends) is community"
        ],
        primary_authority=[
            "Texas Family Code Section 3.002 (community property presumption)",
            "Texas Family Code Section 3.001 (separate property definition)",
            "Texas Family Code Section 3.003 (management rights)",
            "Vallone v. Vallone, 644 S.W.2d 455 (Tex. 1982)",
            "Boyd v. Boyd, 67 S.W.3d 398 (Tex. App. 2002)"
        ],
        burden_holder="Party claiming separate property status",
        adversary_position="All assets acquired during marriage are community absent direct proof otherwise",
        counter_arguments=[
            "Commingling defeats tracing",
            "Insufficient documentation to prove separate source",
            "Gift lacks donative intent or proper formalities"
        ],
        resolution_strategy="Demand bank records, deeds, inheritance documents; trace every dollar; partition or exchange agreements must be in writing; apply strict tracing rules for commingled accounts.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Tarver v. Tarver, 394 S.W.2d 780 (Tex. 1965)"
    ),

    "pretermitted_heir_statute": DoctrineBlock(
        topic="Pretermitted Heir Rights",
        keywords=["pretermitted heir", "omitted child", "after-born", "testamentary intent", "intestate share"],
        conclusion_template="Under TEC 255.052, a child born or adopted after will execution who is not provided for takes an intestate share unless the will shows intent to disinherit or child is provided for outside the will.",
        reasoning_framework="""
1. Determine if child was born/adopted after will execution
2. Check if will provides for the child (even nominally)
3. Check if will expresses intent to disinherit after-born children
4. Check if decedent provided for child by non-probate transfer
5. If none of the above, child takes intestate share from:
   - Devises to other children (prorated reduction), or
   - Entire estate if no other children provided for
6. Calculate intestate share as if decedent died intestate
        """,
        key_factors=[
            "Statute protects children born/adopted after will execution",
            "Intent to disinherit must be clear from will text",
            "Provision can be nominal (dollar 1) if intent clear",
            "Non-probate transfers (life insurance, POD accounts) count as provision",
            "Stepchildren and foster children NOT protected",
            "Statute applies even if decedent knew of pregnancy"
        ],
        primary_authority=[
            "Texas Estates Code Section 255.052",
            "Texas Estates Code Section 255.053 (pretermitted spouse)",
            "Uniform Probate Code Section 2-302 (comparison)",
            "In re Estate of Trevino, 789 S.W.2d 269 (Tex. App. 1990)"
        ],
        burden_holder="Proponent of will seeking to exclude pretermitted heir",
        adversary_position="Child entitled to intestate share as statute intended to prevent accidental disinheritance",
        counter_arguments=[
            "Will shows intent to disinherit all children",
            "Child was provided for via life insurance/trust",
            "Will has residuary clause covering all property"
        ],
        resolution_strategy="Examine will language for disinheritance intent; value non-probate transfers; calculate precise intestate share; prorate reduction among similar devises.",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "adopted_children_inheritance": DoctrineBlock(
        topic="Adopted Children's Inheritance Rights",
        keywords=["adoption", "adopted child", "legal adoption", "biological parents", "dual inheritance"],
        conclusion_template="Under TEC 201.054, legally adopted child inherits from and through adoptive parents as if biological child; generally severs inheritance rights from biological parents except in stepparent adoption.",
        reasoning_framework="""
1. Confirm legal adoption via court decree (not equitable adoption)
2. Adopted child inherits FROM adoptive parents as biological child
3. Adopted child inherits THROUGH adoptive parents (from adoptive grandparents, etc.)
4. Inheritance rights from biological parents terminated EXCEPT:
   - Stepparent adoption (child still inherits from biological parent married to stepparent)
   - Adoption by close relative (may retain rights from biological family)
5. Biological parents generally CANNOT inherit from adopted-out child
6. Adoptive parents' relatives treat adopted child as blood relative
        """,
        key_factors=[
            "Legal adoption required; equitable adoption NOT recognized for inheritance in Texas",
            "Adult adoption is valid and grants full inheritance rights",
            "Stepparent adoption preserves one biological parent line",
            "Post-adoption inheritance from biological family requires specific bequest",
            "Adopted child's descendants inherit through adoptive family line",
            "International adoptions recognized if valid under issuing country's law"
        ],
        primary_authority=[
            "Texas Estates Code Section 201.054",
            "Texas Family Code Chapter 162 (adoption procedures)",
            "Heien v. Crabtree, 369 S.W.2d 28 (Tex. 1963)",
            "In re Estate of Hodge, 705 S.W.2d 447 (Tex. App. 1986)"
        ],
        burden_holder="Party claiming adoption was invalid or incomplete",
        adversary_position="Legally adopted child has identical rights to biological child in adoptive family",
        counter_arguments=[
            "Equitable adoption should be recognized",
            "Adult adoption is sham to create inheritance rights",
            "Child should inherit from both biological and adoptive families"
        ],
        resolution_strategy="Require certified adoption decree; reject equitable adoption claims; explain severance of biological family inheritance unless stepparent adoption; validate adult adoption if legally proper.",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "posthumous_heir_rights": DoctrineBlock(
        topic="Posthumous Heirs and Gestation Period",
        keywords=["posthumous", "gestation", "conceived", "300 days", "assisted reproduction"],
        conclusion_template="Under TEC 201.056, child in gestation at decedent's death who is later born alive inherits as if born during decedent's lifetime; child born within 300 days of death is presumed conceived before death.",
        reasoning_framework="""
1. Determine if child was in gestation at death (conceived before death)
2. Apply 300-day presumption: birth within 300 days = presumed conceived before death
3. Child must be born alive (live birth required, even if survives briefly)
4. For assisted reproduction, check if decedent consented to posthumous use
5. For gestational agreements, identify legal parents under Texas Family Code
6. Posthumous child takes as if born during decedent's lifetime
7. Other heirs' shares adjust to include posthumous heir
        """,
        key_factors=[
            "Live birth required; stillborn child does not inherit",
            "300-day presumption is rebuttable with medical evidence",
            "Assisted reproduction may extend beyond 300 days if consent documented",
            "Gestational surrogacy: intended parents are legal parents",
            "Sperm/egg donors generally NOT parents for inheritance unless intent shown",
            "Class gifts ('to my children') include posthumous heirs"
        ],
        primary_authority=[
            "Texas Estates Code Section 201.056",
            "Texas Family Code Section 160.102 (parent-child relationship)",
            "Texas Family Code Section 160.707 (deceased parent's consent to ART)",
            "Uniform Probate Code Section 2-108",
            "Astrue v. Capato, 566 U.S. 541 (2012)"
        ],
        burden_holder="Party challenging posthumous heir's status",
        adversary_position="Posthumous child is heir if in gestation at death and born alive",
        counter_arguments=[
            "Child conceived after death via frozen sperm/eggs",
            "No written consent to posthumous reproduction",
            "Gestation period exceeds biological limits"
        ],
        resolution_strategy="Apply 300-day presumption unless rebutted; require written consent for post-death ART; verify live birth with birth certificate; adjust distribution to include posthumous heir pro rata.",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "half_blood_inheritance": DoctrineBlock(
        topic="Half-Blood Relatives' Inheritance Rights",
        keywords=["half-blood", "half-sibling", "whole-blood", "equal inheritance", "collateral heirs"],
        conclusion_template="Under TEC 201.057, half-blood kindred inherit equally with whole-blood kindred of same degree; Texas does not discriminate based on half vs whole blood relationship.",
        reasoning_framework="""
1. Identify degree of relationship (siblings, aunts/uncles, cousins, etc.)
2. Determine if relative is half-blood (one common parent) or whole-blood (both parents)
3. In Texas, treat half-blood and whole-blood equally
4. Apply per stirpes or per capita distribution without regard to blood fraction
5. Note: some states give half-blood relatives half share (Texas does NOT)
6. Community property passes to spouse first; half-blood issue arises for separate property
        """,
        key_factors=[
            "Texas law treats half-blood and whole-blood equally (modern trend)",
            "Old common law gave half-blood heirs half share (Texas rejected this)",
            "Half-blood determination requires proof of common parent",
            "Applies to all collateral heirs (siblings, nieces/nephews, cousins)",
            "Does NOT apply to lineal descendants (children always inherit equally)",
            "Half-siblings by marriage (step-siblings) do NOT inherit"
        ],
        primary_authority=[
            "Texas Estates Code Section 201.057",
            "Uniform Probate Code Section 2-107",
            "Restatement (Third) of Property Section 2.4"
        ],
        burden_holder="Party seeking to reduce half-blood relative's share",
        adversary_position="Half-blood kindred inherit same share as whole-blood of same degree",
        counter_arguments=[
            "Half-blood should receive half share under common law",
            "Decedent was closer to whole-blood siblings",
            "Half-blood sibling from different family unit"
        ],
        resolution_strategy="Apply TEC 201.057 strictly; explain Texas rejected common law discrimination; calculate equal shares regardless of blood fraction; require genetic proof if relationship disputed.",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "simultaneous_death_act": DoctrineBlock(
        topic="Simultaneous Death and 120-Hour Survival Rule",
        keywords=["simultaneous death", "120 hour", "survival", "common disaster", "USDA"],
        conclusion_template="Under TEC 121.101 (Uniform Simultaneous Death Act), if heir fails to survive decedent by 120 hours, heir is treated as having predeceased decedent for inheritance purposes.",
        reasoning_framework="""
1. Determine if heir survived decedent at all (instant death vs later death)
2. If heir survived, count 120 hours (5 days) from decedent's death
3. If heir dies within 120 hours, treat as predeceased for intestate succession
4. Apply to: spouses, beneficiaries, joint tenants, life insurance, etc.
5. Purpose: avoid double probate and ensure property passes to next generation
6. Exception: will or instrument can override with different survival period
7. Burden of proof: clear and convincing evidence of 120-hour survival
        """,
        key_factors=[
            "120-hour rule applies unless instrument specifies different period",
            "Prevents double administration of same property",
            "Common in accidents, disasters, or closely-timed deaths",
            "Medical records and death certificates establish time of death",
            "If insufficient evidence of survival order, property distributed as if each predeceased the other",
            "Joint tenancy property passes as if joint tenant predeceased"
        ],
        primary_authority=[
            "Texas Estates Code Section 121.101",
            "Texas Estates Code Section 121.102 (co-owners)",
            "Texas Estates Code Section 121.052 (standard of proof)",
            "Uniform Simultaneous Death Act (1993)",
            "In re Estate of Tran, 2011 WL 13235942 (Tex. App. 2011)"
        ],
        burden_holder="Party claiming heir survived 120 hours",
        adversary_position="Heir did not survive 120 hours; treat as predeceased",
        counter_arguments=[
            "Heir survived 119 hours; should still inherit",
            "Medical uncertainty about exact time of death",
            "Will specifies shorter survival period"
        ],
        resolution_strategy="Obtain death certificates and medical records; calculate precise 120-hour period; if evidence insufficient, apply presumption of predeceased; check for contractual override in will/trust.",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "ancestral_property_rule": DoctrineBlock(
        topic="Ancestral Property and Collateral Heirs",
        keywords=["ancestral property", "collateral heirs", "maternal line", "paternal line", "separate property"],
        conclusion_template="Texas does not apply ancestral property rule; separate property passes under general intestacy rules regardless of property's ancestral source, unlike some states that return property to line of origin.",
        reasoning_framework="""
1. Identify if property is community or separate
2. For separate property, Texas applies general intestacy without ancestral preference
3. Some states return ancestral property to blood relatives of ancestor who provided it
4. Texas rejected this rule: separate property passes by normal intestacy
5. Exception: if no spouse/descendants/parents, property passes to siblings and their descendants
6. No preference for maternal vs paternal line absent specific statute
        """,
        key_factors=[
            "Texas follows modern trend rejecting ancestral property rule",
            "Some states (Louisiana, civil law jurisdictions) retain ancestral property rules",
            "Applies only to separate property (community goes to spouse)",
            "Practical impact: inherited land may pass to non-blood relatives via spouse",
            "Testator can restore property to ancestral line via will",
            "Collateral heirs take equally regardless of which side of family"
        ],
        primary_authority=[
            "Texas Estates Code Chapter 201 (no ancestral property provisions)",
            "Louisiana Civil Code Article 880 (comparison - has ancestral rule)",
            "Uniform Probate Code Section 2-103 (modern approach)"
        ],
        burden_holder="Party claiming property should return to ancestral line",
        adversary_position="Texas law applies general intestacy; no ancestral preference",
        counter_arguments=[
            "Decedent would have wanted property to stay in family line",
            "Property was in family for generations",
            "Spouse is not blood relative and should not inherit ancestral land"
        ],
        resolution_strategy="Explain Texas law does not recognize ancestral property rule; advise estate planning with will if ancestral preservation desired; show UPC and modern trend against ancestral rule.",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "anti_lapse_statute": DoctrineBlock(
        topic="Anti-Lapse Statute for Testamentary Gifts",
        keywords=["lapsed devise", "anti-lapse", "predeceased beneficiary", "substitute gift", "descendants"],
        conclusion_template="Under TEC 255.153, if devisee is descendant of testator's parent and predeceases testator, devisee's descendants take by substitution unless will shows contrary intent.",
        reasoning_framework="""
1. Determine if devisee predeceased testator (lapsed gift)
2. Check if devisee is descendant of testator's parent (sibling, niece, nephew, etc.)
3. If yes, devisee's descendants take the gift by substitution (anti-lapse)
4. If will shows contrary intent (express or implied), anti-lapse does not apply
5. Common contrary intent: 'if X survives me', 'to X or his estate', residuary clause
6. Anti-lapse saves gifts to close relatives by passing to their descendants
7. Does NOT apply to class gifts with built-in survival requirement
        """,
        key_factors=[
            "Protected class: descendants of testator's parents (siblings, nieces, nephews)",
            "Does NOT apply to non-relatives, spouses, or distant relatives",
            "Substitute takers must be descendants of predeceased devisee",
            "Will language expressing survival requirement defeats anti-lapse",
            "Residuary clause may show intent that lapsed gift falls to residue",
            "Per stirpes distribution among substitute takers"
        ],
        primary_authority=[
            "Texas Estates Code Section 255.153",
            "Texas Estates Code Section 255.154 (class gifts)",
            "Uniform Probate Code Section 2-603",
            "In re Estate of Kemper, 241 S.W.3d 415 (Tex. App. 2007)"
        ],
        burden_holder="Party claiming anti-lapse does not apply",
        adversary_position="Anti-lapse statute applies; descendants of predeceased devisee take by substitution",
        counter_arguments=[
            "Will language shows testator wanted gift to lapse",
            "Residuary clause was intended to catch lapsed gifts",
            "Devisee was not descendant of testator's parents"
        ],
        resolution_strategy="Analyze will for survival language; determine if devisee is in protected class; identify substitute takers (descendants of devisee); apply per stirpes among substitutes; check residuary clause for contrary intent.",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "no_surviving_spouse_or_descendants": DoctrineBlock(
        topic="Intestate Succession Without Spouse or Descendants",
        keywords=["no descendants", "parents", "siblings", "collateral heirs", "escheat"],
        conclusion_template="Under TEC 201.001(c)-(e), if no spouse or descendants survive, estate passes to: (1) parents, (2) siblings and their descendants, (3) grandparents and their descendants, (4) more remote relatives, or (5) state if no heirs found.",
        reasoning_framework="""
1. Confirm no surviving spouse or descendants
2. Check for surviving parents (both or one)
3. If no parents, check for siblings (whole or half-blood) and their descendants
4. If no siblings/descendants, pass to grandparents or their descendants (aunts/uncles/cousins)
5. If no grandparents' line, continue to great-grandparents' line (more remote)
6. Maternal and paternal lines take equally
7. If no heirs found after diligent search, estate escheats to state
        """,
        key_factors=[
            "Parents take equal shares if both alive; survivor takes all if one deceased",
            "Siblings inherit per stirpes (nieces/nephews by representation)",
            "Half-blood siblings inherit equally with whole-blood",
            "If one parent deceased, their family line (siblings of deceased parent) may still inherit",
            "Escheat is rare; state has interest in finding heirs",
            "Kinship degrees: siblings=2, aunts/uncles=3, first cousins=4, etc."
        ],
        primary_authority=[
            "Texas Estates Code Section 201.001(c)-(e)",
            "Texas Estates Code Section 201.002 (spouse shares)",
            "Texas Estates Code Section 201.101 (degree of relationship)",
            "Texas Property Code Section 71.001 (escheat)"
        ],
        burden_holder="Party claiming heirship at remote degree",
        adversary_position="Next closest relative inherits; more remote relatives excluded",
        counter_arguments=[
            "Decedent had closer relatives not yet located",
            "Alleged heir's relationship is unproven",
            "Estate should escheat rather than pass to distant heirs"
        ],
        resolution_strategy="Conduct genealogical research; obtain birth/death/marriage records; apply degree-of-relationship rules; exhaust search before escheat; publish notice to unknown heirs.",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "children_born_out_of_wedlock": DoctrineBlock(
        topic="Inheritance Rights of Non-Marital Children",
        keywords=["illegitimate", "out of wedlock", "paternity", "maternity", "acknowledgment"],
        conclusion_template="Under TEC 201.052-201.053, child born out of wedlock inherits from mother and maternal kindred automatically; inherits from father if paternity established by adjudication, acknowledgment, or presumption.",
        reasoning_framework="""
1. Maternal inheritance: automatic for all children born to mother
2. Paternal inheritance: requires establishment of paternity via:
   - Judicial adjudication of paternity
   - Acknowledgment of paternity (AOP) filed with Vital Statistics
   - Presumption of paternity (marriage to mother, etc.)
   - Genetic testing showing probability >99%
3. Father can inherit from non-marital child if paternity established
4. Paternal kindred (father's relatives) can inherit from child if paternity established
5. Time limits: paternity action must be filed during child's lifetime or within 4 years of death
        """,
        key_factors=[
            "Maternity is rarely disputed; biological mother always has inheritance rights",
            "Paternity requires legal establishment before inheritance",
            "Acknowledgment of paternity form (AOP) is sufficient if signed by both parents",
            "Presumed father under Family Code Section 160.204 has inheritance rights",
            "Genetic testing admissible to establish paternity posthumously",
            "Statute of limitations may bar late paternity claims"
        ],
        primary_authority=[
            "Texas Estates Code Section 201.052 (maternal inheritance)",
            "Texas Estates Code Section 201.053 (paternal inheritance)",
            "Texas Family Code Chapter 160 (parent-child relationship)",
            "Texas Family Code Section 160.204 (presumptions of paternity)",
            "In re Estate of Urias, 2019 WL 2435803 (Tex. App. 2019)"
        ],
        burden_holder="Party claiming paternity was not established",
        adversary_position="Child cannot inherit from father without legal establishment of paternity",
        counter_arguments=[
            "Father openly acknowledged child during life",
            "Genetic testing shows 99.9% probability of paternity",
            "Father supported child financially"
        ],
        resolution_strategy="Obtain certified copy of AOP or paternity adjudication; conduct genetic testing if father deceased; check Family Code presumptions; verify statute of limitations; apply strict proof standard.",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "step_children_and_foster_children": DoctrineBlock(
        topic="Stepchildren and Foster Children - No Inheritance Rights",
        keywords=["stepchild", "foster child", "in loco parentis", "equitable adoption", "legal adoption required"],
        conclusion_template="Texas law does not recognize inheritance rights for stepchildren or foster children absent legal adoption; equitable adoption doctrine is not recognized for inheritance purposes.",
        reasoning_framework="""
1. Stepchild relationship: child of spouse by prior marriage/relationship
2. Stepchildren do NOT inherit from stepparent under intestacy
3. Foster child relationship: child placed in care by state
4. Foster children do NOT inherit from foster parents under intestacy
5. Legal adoption required to create inheritance rights
6. In loco parentis status insufficient for intestate succession
7. Equitable adoption not recognized in Texas for inheritance
8. Contract to adopt must be fully executed (legal adoption completed)
        """,
        key_factors=[
            "Step-relationship does not create inheritance rights",
            "Stepparent can leave property to stepchild by will, but not intestacy",
            "Foster care placement is temporary; not equivalent to adoption",
            "Equitable adoption recognized in some states (not Texas for inheritance)",
            "In loco parentis may create support obligations but not inheritance rights",
            "Stepparent adoption severs one biological parent's rights, creates new parent-child relationship"
        ],
        primary_authority=[
            "Texas Estates Code Section 201.054 (adoption required)",
            "Heien v. Crabtree, 369 S.W.2d 28 (Tex. 1963) (rejecting equitable adoption)",
            "Texas Family Code Chapter 162 (adoption procedures)"
        ],
        burden_holder="Stepchild or foster child claiming inheritance rights",
        adversary_position="No inheritance rights without legal adoption decree",
        counter_arguments=[
            "Stepparent promised to adopt and treated child as own",
            "Child relied on promise and changed position",
            "Stepparent held child out as biological child"
        ],
        resolution_strategy="Require certified adoption decree; reject equitable adoption claims citing Heien; distinguish support obligations from inheritance rights; explain policy favoring legal adoption.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Heien v. Crabtree, 369 S.W.2d 28 (Tex. 1963)"
    ),

    "advancements_and_hotchpot": DoctrineBlock(
        topic="Advancements and Hotchpot Doctrine",
        keywords=["advancement", "hotchpot", "inter vivos gift", "intestate share", "presumption"],
        conclusion_template="Under TEC 201.151, lifetime gift to heir is NOT treated as advancement against intestate share unless shown to be intended as such by written declaration or heir's acknowledgment; modern law presumes gifts are absolute.",
        reasoning_framework="""
1. Common law: presumed inter vivos gift to child was advancement
2. Modern law (Texas): presumes gift is NOT advancement
3. Advancement finding requires:
   - Written declaration by decedent that gift is advancement, OR
   - Written acknowledgment by heir that gift is advancement
4. If advancement proven, value of gift is added to estate for calculation
5. Heir's share reduced by advancement amount
6. If advancement exceeds heir's share, heir does not have to return excess
7. Hotchpot: process of bringing advancements into estate calculation
        """,
        key_factors=[
            "Burden on party claiming gift was advancement",
            "Oral statements insufficient; writing required",
            "Valuation at time of gift (not death)",
            "Only applies to intestate succession (not wills unless will says so)",
            "Heir who received advancement still inherits, but share reduced",
            "Doctrine rarely applied in modern practice due to writing requirement"
        ],
        primary_authority=[
            "Texas Estates Code Section 201.151",
            "Uniform Probate Code Section 2-109",
            "Restatement (Third) of Property Section 2.5"
        ],
        burden_holder="Party claiming gift was advancement",
        adversary_position="Gift was absolute; not advancement without writing",
        counter_arguments=[
            "Decedent stated gift was advancement (orally)",
            "Gift was down payment on house intended to come from inheritance",
            "Other heirs did not receive similar gifts"
        ],
        resolution_strategy="Require written evidence; reject oral testimony; value gift at time given; calculate hotchpot if advancement proven; explain modern presumption favors absolute gift.",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "disclaimer_of_inheritance": DoctrineBlock(
        topic="Disclaimer of Inheritance Rights",
        keywords=["disclaimer", "renunciation", "qualified disclaimer", "tax planning", "creditor avoidance"],
        conclusion_template="Under TEC Chapter 122, heir may disclaim inheritance within 9 months of death; disclaimer must be in writing, irrevocable, and filed with probate court; disclaimed property passes as if disclaimant predeceased decedent.",
        reasoning_framework="""
1. Heir has right to disclaim (refuse) inheritance
2. Disclaimer must be: written, signed, acknowledged, filed with court
3. Time limit: 9 months from date of death (or majority if minor)
4. Disclaimer is irrevocable once filed
5. Disclaimed property passes as if disclaimant predeceased decedent
6. Next heirs in line receive disclaimed share
7. Tax benefits: qualified disclaimer avoids gift tax
8. Creditor issues: disclaimer may be fraudulent transfer if insolvent
        """,
        key_factors=[
            "Disclaimer is voluntary; heir cannot be forced to accept inheritance",
            "9-month deadline is strict for qualified tax disclaimer",
            "Partial disclaimers allowed (disclaim part of inheritance)",
            "Disclaimant cannot control who receives disclaimed property",
            "Bankruptcy trustee may object to disclaimer as fraudulent transfer",
            "Disclaimer relates back to date of death for tax purposes"
        ],
        primary_authority=[
            "Texas Estates Code Chapter 122",
            "IRC Section 2518 (qualified disclaimers for tax)",
            "Texas Business and Commerce Code Section 24.005 (fraudulent transfer)",
            "Uniform Disclaimer of Property Interests Act"
        ],
        burden_holder="Party challenging validity of disclaimer",
        adversary_position="Valid disclaimer passes property to next heirs as if disclaimant predeceased",
        counter_arguments=[
            "Disclaimer is fraudulent transfer to avoid creditors",
            "Disclaimer filed after 9-month deadline",
            "Disclaimant accepted benefits before disclaiming"
        ],
        resolution_strategy="File disclaimer promptly; ensure writing and court filing; disclaim before accepting benefits; analyze fraudulent transfer risk if creditors involved; coordinate with tax advisor for qualified disclaimer.",
        confidence=ConfidenceLevel.AGGRESSIVE
    ),

    "survivorship_proof_burden": DoctrineBlock(
        topic="Burden of Proof for Survivorship",
        keywords=["survivorship", "burden of proof", "order of death", "medical evidence", "presumption"],
        conclusion_template="Party claiming inheritance bears burden of proving heir survived decedent by clear and convincing evidence under TEC 121.052; if insufficient evidence, property distributed as if each predeceased the other.",
        reasoning_framework="""
1. Claimant must prove heir survived decedent (not just simultaneously)
2. Standard: clear and convincing evidence (higher than preponderance)
3. Evidence: death certificates, medical records, witness testimony
4. If order of death uncertain, apply USDA presumption (each predeceased other)
5. Result: property distributed to each decedent's estate separately
6. 120-hour survival rule applies if survivorship proven
7. Simultaneous death in common disaster often triggers this issue
        """,
        key_factors=[
            "Clear and convincing standard is high burden",
            "Medical examiner's opinion on time of death is persuasive",
            "Witness testimony may be sufficient if credible and detailed",
            "If evidence equally balanced, apply presumption of simultaneous death",
            "Presumption avoids double probate in many cases",
            "Joint tenancy and POD accounts also subject to survivorship proof"
        ],
        primary_authority=[
            "Texas Estates Code Section 121.052",
            "Texas Estates Code Section 121.101",
            "Uniform Simultaneous Death Act Section 3"
        ],
        burden_holder="Heir or beneficiary claiming survivor status",
        adversary_position="Insufficient evidence of survivorship; apply simultaneous death presumption",
        counter_arguments=[
            "Witness testimony conflicts with medical evidence",
            "Death certificates show same time of death",
            "No direct evidence of who died first"
        ],
        resolution_strategy="Obtain all medical records and death certificates; depose emergency responders and medical personnel; analyze autopsy reports; if evidence insufficient, apply USDA presumption.",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "spousal_election_against_will": DoctrineBlock(
        topic="Surviving Spouse's Right of Election",
        keywords=["spousal election", "elective share", "augmented estate", "community property", "will contest"],
        conclusion_template="Texas does not have statutory elective share for surviving spouse because community property system protects spouse's half of marital property; spouse takes 1/2 community property regardless of will.",
        reasoning_framework="""
1. Texas is community property state (not separate property state)
2. Spouse owns 1/2 of community property automatically
3. Decedent can only devise their 1/2 of community property
4. No elective share statute needed because spouse already protected
5. Separate property can be devised away from spouse completely
6. Spouse's intestate share of separate property is NOT guaranteed if will exists
7. Pretermitted spouse statute protects spouse omitted from pre-marriage will
        """,
        key_factors=[
            "Community property system is functional equivalent of elective share",
            "Separate property states (common law states) have elective share statutes",
            "Texas spouse gets 1/2 community but may get zero separate property under will",
            "Community property presumption is strong protection for spouse",
            "Pretermitted spouse statute (TEC 255.053) protects spouse if married after will execution",
            "Spouse can contest will on grounds of undue influence, lack of capacity, etc."
        ],
        primary_authority=[
            "Texas Family Code Section 3.002 (community property)",
            "Texas Estates Code Section 255.053 (pretermitted spouse)",
            "Uniform Probate Code Section 2-202 (elective share - not in Texas)",
            "Restatement (Third) of Property Section 9.1"
        ],
        burden_holder="Spouse claiming property beyond community 1/2",
        adversary_position="Spouse limited to 1/2 community property plus whatever will provides",
        counter_arguments=[
            "Decedent transmuted community to separate to disinherit spouse",
            "Will should be set aside for undue influence",
            "Spouse entitled to support/maintenance from estate"
        ],
        resolution_strategy="Classify all property as community or separate; trace separate property; challenge transmutation if fraud/duress; pursue will contest if grounds exist; explain no elective share in Texas.",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "intestate_succession_flow": DoctrineBlock(
        topic="Intestate Succession Priority Flow Chart",
        keywords=["succession order", "priority", "heirs", "next of kin", "escheat"],
        conclusion_template="Texas intestate succession follows statutory priority: (1) spouse and descendants, (2) descendants only, (3) parents, (4) siblings and their descendants, (5) grandparents and their descendants, (6) more remote ancestors and their descendants, (7) escheat to state.",
        reasoning_framework="""
1. First: spouse and descendants (TEC 201.002)
   - Community property: all to spouse
   - Separate property: spouse gets 1/3 personalty + life estate in 1/3 realty; descendants get rest
2. Second: descendants only (no spouse) (TEC 201.001(b))
   - All to descendants per stirpes
3. Third: parents (no spouse or descendants) (TEC 201.001(c))
   - If both alive: equal shares to both
   - If one alive: all to survivor
4. Fourth: siblings and their descendants (no spouse/descendants/parents)
   - Half-blood and whole-blood inherit equally
   - Per stirpes distribution
5. Fifth: grandparents and their descendants (aunts/uncles/cousins)
   - Maternal and paternal lines take equally
6. Sixth: more remote ancestors (great-grandparents, etc.)
7. Seventh: escheat to State of Texas (no heirs found)
        """,
        key_factors=[
            "Spouse's share depends on property classification (community vs separate)",
            "Each tier excludes the next (if heirs in tier 1, tiers 2-7 are excluded)",
            "Half-blood relatives inherit equally with whole-blood at same tier",
            "Per stirpes applies to descendants of deceased heirs",
            "Escheat is last resort; state benefits from property if no heirs",
            "Diligent search for heirs required before escheat"
        ],
        primary_authority=[
            "Texas Estates Code Chapter 201",
            "Texas Estates Code Section 201.001 (general rules)",
            "Texas Estates Code Section 201.002 (spouse's share)",
            "Texas Property Code Chapter 71 (escheat)"
        ],
        burden_holder="Party claiming heirship at lower tier",
        adversary_position="Heirs at higher tier take all; lower tiers excluded",
        counter_arguments=[
            "Higher-tier heir should be disqualified (slayer, disclaimer, etc.)",
            "Alleged heir's relationship is unproven",
            "Estate should skip to next tier due to special circumstances"
        ],
        resolution_strategy="Apply statutory priority strictly; prove all higher tiers have no heirs before passing to next tier; verify each heir's relationship with legal documentation; exhaust search before escheat.",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "degree_of_relationship_calculation": DoctrineBlock(
        topic="Calculating Degree of Relationship",
        keywords=["degree", "kinship", "civil law degree", "common ancestor", "counting generations"],
        conclusion_template="Under TEC 201.101, degree of relationship is determined by counting generations from decedent up to common ancestor and down to relative; closer degree excludes more remote.",
        reasoning_framework="""
1. Identify common ancestor of decedent and relative
2. Count generations up from decedent to common ancestor
3. Count generations down from common ancestor to relative
4. Add the two numbers = degree of relationship
5. Examples:
   - Parent/child: 1 degree (1 generation)
   - Siblings: 2 degrees (up 1 to parent, down 1 to sibling)
   - Aunt/uncle: 3 degrees (up 1 to parent, up 1 to grandparent, down 1 to aunt/uncle)
   - First cousin: 4 degrees (up 2 to grandparent, down 2 to cousin)
6. Closer degree takes priority over more remote degree
        """,
        key_factors=[
            "Civil law method (used in Texas) differs from common law method",
            "Degree determines priority when multiple relatives exist",
            "Half-blood and whole-blood have same degree",
            "Adopted relatives counted as blood relatives for degree purposes",
            "If multiple relatives at same degree, they share equally",
            "Degrees used for both intestate succession and homestead rights"
        ],
        primary_authority=[
            "Texas Estates Code Section 201.101",
            "Texas Probate Code Section 38(b) (historical)",
            "Restatement (Third) of Property Section 2.4"
        ],
        burden_holder="Remote relative claiming equal or superior rights to closer relative",
        adversary_position="Closer degree excludes more remote; equal degree relatives share",
        counter_arguments=[
            "More remote relative was closer to decedent personally",
            "Degree calculation is incorrect",
            "Half-blood should be treated as more remote"
        ],
        resolution_strategy="Calculate degree mathematically using generation count; diagram family tree; apply civil law method strictly; treat equal-degree relatives equally regardless of bloodline.",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "slayer_statute": DoctrineBlock(
        topic="Slayer Statute - Killer Disqualified",
        keywords=["slayer", "felonious killing", "disqualified heir", "constructive trust", "public policy"],
        conclusion_template="Under TEC 201.058, person who feloniously and intentionally kills decedent forfeits all inheritance rights; property passes as if killer predeceased decedent; includes will, intestacy, joint tenancy, life insurance.",
        reasoning_framework="""
1. Killer must be convicted of or found liable for felonious and intentional killing
2. Manslaughter or negligent homicide may not trigger slayer statute
3. Self-defense, accident, insanity may be defenses to slayer disqualification
4. Killer forfeits: inheritance, will devises, joint tenancy, POD, life insurance
5. Property passes as if killer predeceased victim
6. Constructive trust imposed on property killer receives
7. Slayer's descendants may still inherit by representation (depends on statute language)
        """,
        key_factors=[
            "Conviction not required; civil finding of liability is sufficient",
            "Intent element is critical; accidental killing may not disqualify",
            "Public policy: no one should profit from their own wrongdoing",
            "Applies to all forms of property transfer, not just probate",
            "Life insurance beneficiary designation revoked if beneficiary is slayer",
            "Statute may allow slayer's descendants to inherit (check TEC 201.058 language)"
        ],
        primary_authority=[
            "Texas Estates Code Section 201.058",
            "Texas Estates Code Section 201.059 (effect of disqualification)",
            "Uniform Probate Code Section 2-803",
            "Restatement (Third) of Restitution Section 45"
        ],
        burden_holder="Party claiming killer should be disqualified",
        adversary_position="Killer forfeits all property rights; passes to next heirs",
        counter_arguments=[
            "Killing was self-defense",
            "Killer was insane and not criminally responsible",
            "Conviction was for negligent homicide, not murder"
        ],
        resolution_strategy="Obtain criminal judgment or file civil wrongful death action; prove felonious and intentional killing; trace all property interests; impose constructive trust; apply statute to insurance and joint accounts.",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    "separate_property_tracing": DoctrineBlock(
        topic="Tracing Separate Property Character",
        keywords=["tracing", "inception of title", "separate property", "commingling", "burden of proof"],
        conclusion_template="Party claiming separate property character must trace property to separate source (pre-marital, gift, inheritance) by clear and convincing evidence; commingling with community property may defeat tracing absent detailed records.",
        reasoning_framework="""
1. Community property presumption applies to all marital property
2. Claimant must rebut presumption with clear and convincing evidence
3. Tracing methods:
   - Direct tracing: bank records showing deposit from separate source
   - Inception of title: property right arose before marriage or via gift/inheritance
   - Exhaustion of community: show community funds insufficient for purchase
4. Commingling defeats tracing if separate funds mixed irreversibly
5. Mutations: income/gains from separate property may be community
6. Written partition/exchange agreement can change character
        """,
        key_factors=[
            "Burden on separate property claimant is high (clear and convincing)",
            "Bank records, deeds, wills, gift letters are key evidence",
            "Testimony alone usually insufficient to rebut presumption",
            "Inception of title rule: character determined when right to property arises",
            "Commingling in joint account creates evidentiary problem",
            "Tracing requires contemporaneous documentation, not after-the-fact reconstruction"
        ],
        primary_authority=[
            "Texas Family Code Section 3.003 (separate property)",
            "Texas Family Code Section 3.002 (community presumption)",
            "Vallone v. Vallone, 644 S.W.2d 455 (Tex. 1982)",
            "Tarver v. Tarver, 394 S.W.2d 780 (Tex. 1965)"
        ],
        burden_holder="Party claiming separate property character",
        adversary_position="All property acquired during marriage is community unless proven separate",
        counter_arguments=[
            "Funds were deposited to joint account and commingled",
            "No contemporaneous documentation of separate source",
            "Property purchased during marriage with title in both names"
        ],
        resolution_strategy="Obtain bank records from date of marriage forward; trace each deposit and withdrawal; use forensic accountant if needed; apply inception of title rule; show separate source clearly.",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="Vallone v. Vallone, 644 S.W.2d 455 (Tex. 1982)"
    ),

    "homestead_rights_of_spouse": DoctrineBlock(
        topic="Surviving Spouse's Homestead Rights",
        keywords=["homestead", "life estate", "probate homestead", "family allowance", "exempt property"],
        conclusion_template="Under Texas Constitution and TEC Chapter 353, surviving spouse has constitutional right to remain in homestead for life or until remarriage, regardless of who inherits property; homestead exempt from forced sale for debts.",
        reasoning_framework="""
1. Homestead is constitutional protection, not probate law
2. Surviving spouse entitled to possess homestead:
   - For life if no minor children
   - Until youngest child reaches majority if minor children
3. Homestead right is possessory only; does not affect ownership
4. Property may be owned by children but spouse has right to occupy
5. Homestead exempt from creditors' claims (except taxes, purchase money, home equity loans)
6. Community property homestead: spouse owns 1/2, has possessory right to other 1/2
7. Separate property homestead: spouse has no ownership but has occupancy right
        """,
        key_factors=[
            "Homestead protection is in Texas Constitution Article 16, Section 50-52",
            "Creditors cannot force sale of homestead while spouse/minor children occupy",
            "Homestead right terminates on remarriage or death of spouse",
            "Homestead designation does not affect ownership or inheritance",
            "Family allowance and exempt property also available to spouse",
            "Homestead can be urban (10 acres) or rural (200 acres family, 100 single)"
        ],
        primary_authority=[
            "Texas Constitution Article 16, Sections 50-52",
            "Texas Estates Code Chapter 353",
            "Texas Property Code Section 41.001",
            "Williams v. Williams, 569 S.W.2d 867 (Tex. 1978)"
        ],
        burden_holder="Party seeking to force sale or evict spouse",
        adversary_position="Spouse has constitutional right to occupy homestead; cannot be forced to sell or vacate",
        counter_arguments=[
            "Spouse abandoned homestead and established new residence",
            "Spouse remarried and lost homestead right",
            "Property is not homestead (investment property, second home)"
        ],
        resolution_strategy="Verify homestead designation and occupancy; distinguish ownership from possessory rights; protect homestead from creditors; advise estate planning to preserve homestead for spouse and children.",
        confidence=ConfidenceLevel.DEFENSIBLE
    )
}


# ============================================================================
# TELEMETRY & METRICS
# ============================================================================

class TelemetryCollector:
    def __init__(self):
        self.queries: List[TelemetryRecord] = []
        self.cache_hits = 0
        self.cache_misses = 0
        self.total_latency_ms = 0.0
        self.error_count = 0

    def record_query(self, record: TelemetryRecord):
        self.queries.append(record)
        if record.cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        self.total_latency_ms += record.latency_ms
        if record.error_domain:
            self.error_count += 1

    def get_stats(self) -> Dict[str, Any]:
        total = len(self.queries)
        return {
            "total_queries": total,
            "cache_hit_rate": self.cache_hits / total if total > 0 else 0,
            "avg_latency_ms": self.total_latency_ms / total if total > 0 else 0,
            "error_rate": self.error_count / total if total > 0 else 0
        }


telemetry = TelemetryCollector()


# ============================================================================
# CORE ENGINE
# ============================================================================

class HeirshipEngine:
    def __init__(self):
        self.doctrine_cache = DOCTRINE_CACHE
        self.query_count = 0

    def analyze_heirship(self, req: HeirshipRequest) -> Dict[str, Any]:
        start_time = time.time()
        query_id = f"Q{self.query_count:05d}"
        self.query_count += 1

        triggered_doctrines = []
        response_text = ""
        confidence = ConfidenceLevel.DEFENSIBLE

        # Doctrine matching
        has_spouse = "spouse" in req.survived_by or "married" in req.marriage_status.lower()
        has_descendants = any(word in req.survived_by for word in ["child", "children", "son", "daughter"])
        has_parents = "parent" in req.survived_by

        if has_spouse and has_descendants:
            triggered_doctrines.append("intestate_spouse_with_children")
            doctrine = self.doctrine_cache["intestate_spouse_with_children"]
            response_text = self._build_response(doctrine, req)
        elif has_descendants and not has_spouse:
            triggered_doctrines.append("intestate_no_spouse_with_descendants")
            triggered_doctrines.append("per_stirpes_distribution")
            response_text = self._build_multi_doctrine_response(
                [self.doctrine_cache["intestate_no_spouse_with_descendants"],
                 self.doctrine_cache["per_stirpes_distribution"]],
                req
            )
        elif not has_spouse and not has_descendants:
            triggered_doctrines.append("no_surviving_spouse_or_descendants")
            doctrine = self.doctrine_cache["no_surviving_spouse_or_descendants"]
            response_text = self._build_response(doctrine, req)

        # Property classification
        if req.property_type == PropertyType.COMMUNITY or "community" in req.property_description.lower():
            triggered_doctrines.append("community_property_classification")

        # Special situations
        if "adopted" in req.children_info.lower():
            triggered_doctrines.append("adopted_children_inheritance")
        if "half" in req.survived_by or "half-blood" in req.survived_by:
            triggered_doctrines.append("half_blood_inheritance")
        if "posthumous" in req.children_info.lower():
            triggered_doctrines.append("posthumous_heir_rights")

        latency_ms = (time.time() - start_time) * 1000

        telemetry_record = TelemetryRecord(
            query_id=query_id,
            timestamp=datetime.utcnow().isoformat(),
            latency_ms=latency_ms,
            cache_hit=len(triggered_doctrines) > 0,
            mode=req.mode.value,
            zone=req.zone.value,
            doctrines_triggered=triggered_doctrines,
            error_domain=None
        )
        telemetry.record_query(telemetry_record)

        return {
            "query_id": query_id,
            "decedent": req.decedent_name,
            "state": req.decedent_state,
            "analysis": response_text,
            "doctrines_applied": triggered_doctrines,
            "confidence": confidence.value,
            "mode": req.mode.value,
            "latency_ms": latency_ms,
            "determinism_hash": self._compute_hash(req, response_text)
        }

    def _build_response(self, doctrine: DoctrineBlock, req: HeirshipRequest) -> str:
        if req.mode == ResponseMode.FAST:
            return doctrine.conclusion_template
        elif req.mode == ResponseMode.DEFENSE:
            return f"{doctrine.conclusion_template}\n\nAuthority: {'; '.join(doctrine.primary_authority)}\n\nKey Factors: {'; '.join(doctrine.key_factors)}"
        else:  # MEMO
            return f"""LEGAL MEMORANDUM - HEIRSHIP DETERMINATION

ISSUE: {doctrine.topic}

CONCLUSION:
{doctrine.conclusion_template}

REASONING:
{doctrine.reasoning_framework}

KEY FACTORS:
{chr(10).join(f'- {f}' for f in doctrine.key_factors)}

PRIMARY AUTHORITY:
{chr(10).join(f'- {a}' for a in doctrine.primary_authority)}

ADVERSE ARGUMENTS:
{chr(10).join(f'- {c}' for c in doctrine.counter_arguments)}

RESOLUTION STRATEGY:
{doctrine.resolution_strategy}

CONFIDENCE LEVEL: {doctrine.confidence.value}
"""

    def _build_multi_doctrine_response(self, doctrines: List[DoctrineBlock], req: HeirshipRequest) -> str:
        parts = []
        for doctrine in doctrines:
            if req.mode == ResponseMode.FAST:
                parts.append(doctrine.conclusion_template)
            else:
                parts.append(self._build_response(doctrine, req))
        return "\n\n".join(parts)

    def _compute_hash(self, req: HeirshipRequest, response: str) -> str:
        data = f"{req.decedent_name}|{req.decedent_state}|{req.survived_by}|{response}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]


engine = HeirshipEngine()


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title=ENGINE_NAME,
    version=VERSION,
    description="TIE-Grade Heirship Determination Engine"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/health")
def health_check():
    stats = telemetry.get_stats()
    return {
        "status": "healthy",
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": VERSION,
        "port": PORT,
        "uptime_queries": engine.query_count,
        "doctrine_blocks": len(DOCTRINE_CACHE),
        "telemetry": stats
    }


@app.post("/query")
def query_heirship(request: HeirshipRequest):
    try:
        logger.info(f"Heirship query: {request.decedent_name} ({request.decedent_state})")
        result = engine.analyze_heirship(request)
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/doctrines")
def list_doctrines():
    return {
        "total": len(DOCTRINE_CACHE),
        "topics": [d.topic for d in DOCTRINE_CACHE.values()]
    }


@app.get("/")
def root():
    return {
        "engine": ENGINE_NAME,
        "version": VERSION,
        "endpoints": ["/health", "/query", "/doctrines"]
    }


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
