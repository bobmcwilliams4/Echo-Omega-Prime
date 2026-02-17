#!/usr/bin/env python
"""PRB07 Estate Tax Planning Engine v1.0.0 - TIE-Grade Intelligence

Federal estate/gift/GST tax planning with IRC §2001-2664 coverage.
Port 9117. Full TIE-20 architecture.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# ==================== CONFIGURATION ====================
ENGINE_ID = "PRB07"
ENGINE_NAME = "Estate Tax Planning Engine"
VERSION = "1.0.0"
PORT = 9117

logger.add(
    Path(__file__).parent / "logs" / "prb07_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO"
)

# ==================== DATA MODELS ====================
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

class AuthorityLevel(str, Enum):
    STATUTE = "STATUTE"
    REGULATION = "REGULATION"
    REVENUE_RULING = "REVENUE_RULING"
    CASE_LAW = "CASE_LAW"
    PLR = "PLR"

@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    zone: AnalysisZone
    authority_level: AuthorityLevel
    adversary_position: str = ""
    counter_arguments: List[str] = field(default_factory=list)
    entity_scope: str = "ALL"
    controlling_precedent: str = ""

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5)
    mode: ResponseMode = ResponseMode.FAST
    context: Dict[str, Any] = Field(default_factory=dict)
    zone: AnalysisZone = AnalysisZone.PLANNING

class QueryResponse(BaseModel):
    answer: str
    mode: ResponseMode
    confidence: ConfidenceLevel
    sources: List[str]
    reasoning_chain: List[str]
    determinism_hash: str
    response_time_ms: float
    doctrines_triggered: List[str]
    epistemic_warnings: List[str] = Field(default_factory=list)

# ==================== DOCTRINE CACHE ====================
ESTATE_TAX_DOCTRINES = [
    DoctrineBlock(
        topic="gross_estate_inclusion",
        keywords=["gross estate", "IRC 2031", "valuation", "fair market value", "inclusion"],
        conclusion_template="Gross estate under IRC §2031 includes all property interests owned at death valued at FMV. Date-of-death valuation is mandatory unless alternate valuation elected under §2032.",
        reasoning_framework="""
IRC §2031(a): Gross estate = value of all property (real, personal, tangible, intangible) to extent of decedent's interest.
FMV = price willing buyer pays willing seller, neither under compulsion, both with reasonable knowledge.
Valuation date: Date of death, unless §2032 alternate valuation elected (6 months later OR earlier disposition).
Alternate valuation reduces estate tax if both estate value AND tax decline.
Include: real estate, stocks, bonds, business interests, collectibles, retirement accounts, life insurance (if incidents of ownership).
Exclude: Property passing to surviving spouse (marital deduction §2056), qualified charities (§2055), property decedent never owned.
Partial interests valued separately: life estate, remainder, usufruct rights.
Community property states: 50% of community property in each spouse's gross estate.
""",
        key_factors=["date of death FMV", "alternate valuation availability", "ownership interests", "valuation discounts", "appraisal support"],
        primary_authority=["IRC §2031(a)", "IRC §2032", "Treas. Reg. §20.2031-1", "Estate of Bright v. US (658 F.2d 999)"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.STATUTE,
        adversary_position="IRS may challenge low valuations with higher appraisals, assert FMV understated.",
        counter_arguments=["Independent appraisal supports FMV", "Comparable sales data", "Alternate valuation election if estate value declined"],
        controlling_precedent="Estate of Bright: FMV determined by hypothetical willing buyer/seller standard."
    ),

    DoctrineBlock(
        topic="unified_credit_lifetime_exemption",
        keywords=["unified credit", "basic exclusion amount", "lifetime exemption", "IRC 2010", "exemption portability"],
        conclusion_template="IRC §2010 unified credit shelters estates up to basic exclusion amount (BEA). 2024 BEA: $13.61M per person, indexed for inflation. Portable between spouses if DSUE elected on timely 706.",
        reasoning_framework="""
IRC §2010(c): Unified credit = tentative tax on basic exclusion amount.
BEA inflation-adjusted annually. 2024: $13,610,000. 2025: $13,990,000 (projected).
TCJA 2017: Doubled BEA through 2025; reverts to ~$7M (indexed) in 2026 unless extended.
Portability §2010(c)(4): Surviving spouse may elect deceased spouse unused exclusion (DSUE).
DSUE election: File Form 706 for deceased spouse within 9 months + extensions, even if no estate tax due.
Portability allows surviving spouse BEA = own BEA + DSUE from predeceased spouse.
Lifetime gifts reduce available exemption: adjusted taxable gifts under §2001(b) consume BEA.
Clawback protection: If BEA declines before death, gifts made under higher BEA protected (Treas. Reg. §20.2010-1(c)).
Credit computed: tentative tax on taxable estate + adjusted taxable gifts, minus gift tax paid on post-1976 gifts.
""",
        key_factors=["current BEA amount", "DSUE portability election", "lifetime gift history", "sunset risk 2026", "clawback protection"],
        primary_authority=["IRC §2010(c)", "IRC §2505 (gift tax unified credit)", "Treas. Reg. §20.2010-1", "Rev. Proc. 2022-32 (inflation adjustments)"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.STATUTE,
        adversary_position="IRS may challenge DSUE election if Form 706 filing incomplete or untimely.",
        counter_arguments=["Timely filed complete Form 706", "Valid portability election on return", "BEA sunset planning with 2025 gifts"],
        controlling_precedent="Treas. Reg. §20.2010-2: DSUE computed on estate tax return, portable to surviving spouse."
    ),

    DoctrineBlock(
        topic="annual_gift_exclusion",
        keywords=["annual exclusion", "IRC 2503", "present interest", "Crummey", "future interest"],
        conclusion_template="IRC §2503(b) annual exclusion: $18,000 per donee (2024), indexed. Applies only to present interest gifts. Future interests ineligible unless Crummey withdrawal rights granted.",
        reasoning_framework="""
IRC §2503(b): First $18,000 (2024) of gifts per donee per year excluded from taxable gifts.
Indexed for inflation in $1,000 increments.
Present interest: Donee has immediate right to use/enjoyment/income.
Future interest: Possession/enjoyment postponed (e.g., remainder interest, trust without withdrawal rights).
Crummey power: Beneficiary given temporary withdrawal right (30-60 days) converts future interest to present.
Withdrawal notice required: beneficiary must receive actual notice of contribution and withdrawal right.
Lapse of Crummey power: If withdrawal right lapses, treated as gift IF lapse exceeds greater of $5,000 or 5% of trust corpus.
Married couple: Can split gifts (IRC §2513) to double annual exclusion ($36,000/donee if both spouses consent).
Educational/medical exclusion (IRC §2503(e)): Unlimited exclusion if paid directly to institution/provider.
Gifts to minors: UTMA/UGMA accounts qualify if minor has present access at 18/21.
""",
        key_factors=["present vs future interest", "Crummey withdrawal notice", "lapse limits", "gift splitting", "direct education/medical payments"],
        primary_authority=["IRC §2503(b)", "IRC §2503(e)", "Crummey v. Comm'r (397 F.2d 82)", "Rev. Rul. 81-7"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.STATUTE,
        adversary_position="IRS may disallow annual exclusion for trusts lacking valid Crummey withdrawal rights or adequate notice.",
        counter_arguments=["Documented Crummey notices to beneficiaries", "Withdrawal window 30+ days", "Lapse within 5/5 safe harbor"],
        controlling_precedent="Crummey v. Comm'r: Withdrawal right creates present interest eligible for annual exclusion."
    ),

    DoctrineBlock(
        topic="marital_deduction",
        keywords=["marital deduction", "IRC 2056", "QTIP", "unlimited marital deduction", "terminable interest"],
        conclusion_template="IRC §2056 unlimited marital deduction for property passing to surviving spouse. QTIP trust (IRC §2056(b)(7)) qualifies if spouse receives all income annually and QTIP election made on 706.",
        reasoning_framework="""
IRC §2056(a): Deduction for value of property passing from decedent to surviving spouse.
Unlimited amount: no cap on marital deduction.
Terminable interest rule §2056(b): Disallows deduction if interest terminates (e.g., life estate) UNLESS QTIP exception applies.
QTIP (Qualified Terminable Interest Property) §2056(b)(7):
  - Surviving spouse entitled to all income annually for life.
  - No person may appoint principal to non-spouse during spouse's life.
  - Executor elects QTIP treatment on Form 706.
QTIP inclusion in survivor's estate: QTIP assets included in surviving spouse's gross estate under IRC §2044.
Portability vs QTIP: QTIP defers estate tax to survivor's death; portability allows DSUE without QTIP trust.
Credit shelter trust (bypass trust): Uses decedent's BEA, avoids marital deduction, not in survivor's estate.
Same-sex spouses: Full marital deduction post-Obergefell (2015) and Rev. Rul. 2013-17.
Non-citizen spouse: Marital deduction disallowed unless QDOT (Qualified Domestic Trust) used (IRC §2056A).
""",
        key_factors=["spouse citizenship", "QTIP election", "income distribution requirement", "terminable interest analysis", "QDOT for non-citizens"],
        primary_authority=["IRC §2056", "IRC §2056(b)(7) (QTIP)", "IRC §2056A (QDOT)", "IRC §2044 (QTIP inclusion)", "Rev. Rul. 2013-17"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.STATUTE,
        adversary_position="IRS may disallow marital deduction if QTIP income not distributed annually or non-citizen spouse lacks QDOT.",
        counter_arguments=["QTIP trust terms require annual income distribution", "Timely QTIP election on 706", "QDOT established for non-citizen"],
        controlling_precedent="IRC §2056(b)(7): QTIP exception to terminable interest rule if income/election requirements met."
    ),

    DoctrineBlock(
        topic="charitable_deduction",
        keywords=["charitable deduction", "IRC 2055", "qualified charity", "IRC 170(c)", "charitable remainder trust"],
        conclusion_template="IRC §2055 allows estate tax deduction for bequests to qualified IRC §170(c) charities. Unlimited deduction. Charitable remainder trusts (CRT) qualify if meet IRC §664 requirements.",
        reasoning_framework="""
IRC §2055(a): Deduction for transfers to qualified charitable organizations.
Qualified charities (IRC §170(c)): 501(c)(3) public charities, private foundations, government entities for public purposes.
Unlimited deduction: no cap on charitable deduction amount.
CRT (Charitable Remainder Trust) IRC §664:
  - Pays annuity (CRAT) or unitrust (CRUT) to non-charitable beneficiary for term of years/life.
  - Remainder to charity.
  - Deduction = present value of remainder interest (IRS §7520 rate discount).
CLT (Charitable Lead Trust) IRC §2522: Charity receives income stream, remainder to heirs. Estate deduction for PV of lead interest.
Split-interest trusts: Must comply with IRC §664 (CRT) or §2522 (CLT) to avoid partial disallowance.
Private foundation CRT: Payout rate min 5%, max 50%. Term max 20 years or life.
Substantiation: Appraisal required for non-cash assets >$5,000.
""",
        key_factors=["qualified charity status", "CRT/CLT compliance", "valuation of remainder interest", "§7520 discount rate", "substantiation requirements"],
        primary_authority=["IRC §2055", "IRC §664 (CRT)", "IRC §2522 (CLT)", "IRC §7520 (actuarial tables)", "Treas. Reg. §20.2055-2"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.STATUTE,
        adversary_position="IRS may challenge CRT deduction if payout rate exceeds limits or trust violates §664 requirements.",
        counter_arguments=["CRT drafted per §664 safe harbor", "Qualified appraisal for non-cash assets", "Charity has valid 501(c)(3) status"],
        controlling_precedent="IRC §664: CRT qualifies for charitable deduction if annuity/unitrust requirements met."
    ),

    DoctrineBlock(
        topic="life_insurance_inclusion",
        keywords=["life insurance", "IRC 2042", "incidents of ownership", "ILIT", "three-year rule"],
        conclusion_template="IRC §2042 includes life insurance in gross estate if decedent possessed incidents of ownership OR proceeds payable to estate. ILIT (Irrevocable Life Insurance Trust) avoids inclusion if no retained incidents and survives three-year lookback (IRC §2035).",
        reasoning_framework="""
IRC §2042(1): Proceeds includible if payable to estate or executor.
IRC §2042(2): Proceeds includible if decedent possessed incidents of ownership at death.
Incidents of ownership: Right to change beneficiary, borrow against cash value, surrender policy, assign policy.
ILIT strategy: Transfer policy to irrevocable trust, relinquish all incidents, trust owns policy.
Three-year rule §2035(a): If policy transferred within 3 years of death, proceeds included in gross estate.
Gift tax on transfer: Transfer of policy to ILIT is completed gift; value = replacement cost or cash surrender value.
Premium payments: Annual premiums paid by grantor to trust are gifts; use Crummey powers for annual exclusion.
Community property: In community property states, each spouse owns 50% of policy on other spouse's life.
Group term life: Employer-provided group term over $50,000 includible if employee had incidents.
""",
        key_factors=["incidents of ownership", "ILIT transfer timing", "three-year lookback", "Crummey withdrawal rights", "premium gift strategy"],
        primary_authority=["IRC §2042", "IRC §2035(a)", "Treas. Reg. §20.2042-1", "Estate of Noel v. Comm'r (380 US 678)"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.STATUTE,
        adversary_position="IRS may assert incidents of ownership if grantor retains indirect control or pays premiums without Crummey notices.",
        counter_arguments=["ILIT drafted to prohibit grantor control", "Transfer >3 years before death", "Crummey notices for premium gifts"],
        controlling_precedent="Estate of Noel: Incidents of ownership include any economic benefit or control over policy."
    ),

    DoctrineBlock(
        topic="retained_life_estate_2036",
        keywords=["IRC 2036", "retained life estate", "retained income", "retained use", "estate inclusion"],
        conclusion_template="IRC §2036(a) includes in gross estate property transferred during life if decedent retained: (1) possession/enjoyment, OR (2) right to income. QPRT, GRAT avoid §2036 if comply with IRC §2702.",
        reasoning_framework="""
IRC §2036(a)(1): Inclusion if retained possession, enjoyment, or right to income for life/period not ascertainable without reference to death.
IRC §2036(a)(2): Inclusion if retained right to designate who possesses/enjoys property or income.
§2036 applies to transfers for less than full consideration.
Common triggers: Retained right to live in residence, retained income from trust, informal arrangement to receive benefits.
Bona fide sale exception: If full FMV paid, §2036 does not apply.
QPRT (Qualified Personal Residence Trust) IRC §2702(a)(3)(A)(ii): Grantor retains residence for term of years, remainder to beneficiaries. If grantor survives term, residence excluded from estate.
GRAT (Grantor Retained Annuity Trust) IRC §2702(b): Grantor receives annuity for term, remainder to beneficiaries. FMV paid via annuity; appreciation passes gift-tax-free if grantor survives.
Informal retained benefits: Continued use of gifted property without paying rent triggers §2036.
""",
        key_factors=["retained rights at transfer", "bona fide sale consideration", "QPRT/GRAT compliance", "informal arrangements", "survival of term"],
        primary_authority=["IRC §2036", "IRC §2702 (QPRT/GRAT)", "Treas. Reg. §20.2036-1", "Estate of Maxwell v. Comm'r (3 F.3d 591)"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.STATUTE,
        adversary_position="IRS may assert §2036 inclusion if informal agreement or continued use without rent after transfer.",
        counter_arguments=["QPRT/GRAT comply with §2702", "No retained rights in transfer documents", "Arms-length rent paid if residence used post-transfer"],
        controlling_precedent="Estate of Maxwell: Informal understanding to retain benefits triggers §2036 even without written agreement."
    ),

    DoctrineBlock(
        topic="revocable_transfers_2038",
        keywords=["IRC 2038", "revocable transfer", "power to alter", "retained control", "trustee powers"],
        conclusion_template="IRC §2038 includes transferred property in gross estate if decedent retained power to alter, amend, revoke, or terminate. Revocable trust assets fully includible. Irrevocable trust safe if no retained powers.",
        reasoning_framework="""
IRC §2038(a)(1): Inclusion if decedent could alter, amend, revoke, or terminate enjoyment of property.
Revocable trust: Grantor retains power to revoke → entire trust in gross estate.
Irrevocable trust: Generally excluded UNLESS grantor retained power to alter beneficiaries or distributions.
Power exercisable with consent: §2038 applies even if power requires consent of adverse party.
Trustee powers: If grantor serves as trustee with discretion over distributions, §2038 may apply.
Independent trustee safe harbor: If only independent trustee has discretion (no grantor/family), §2038 does not apply.
Power relinquished before death: If power released >3 years before death, property excluded (but see §2035 three-year rule).
Ascertainable standard exception: Power limited by ascertainable standard (health, education, support, maintenance) may avoid §2038.
""",
        key_factors=["revocability of transfer", "retained powers over distributions", "trustee independence", "ascertainable standards", "timing of power release"],
        primary_authority=["IRC §2038", "IRC §2041 (general power of appointment)", "Treas. Reg. §20.2038-1", "Old Colony Trust v. US (423 F.2d 601)"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.STATUTE,
        adversary_position="IRS may assert §2038 if grantor retained any control as trustee or co-trustee with discretionary powers.",
        counter_arguments=["Irrevocable trust with independent trustee", "No grantor powers to alter/amend", "Distributions governed by ascertainable standard"],
        controlling_precedent="Old Colony Trust: §2038 applies if decedent could alter enjoyment, even indirectly."
    ),

    DoctrineBlock(
        topic="generation_skipping_transfer_tax",
        keywords=["GST tax", "IRC 2601", "skip person", "GSTT exemption", "dynasty trust"],
        conclusion_template="IRC §2601-2664 imposes GST tax on transfers to skip persons (grandchildren, >37.5 years younger). GSTT rate = 40% (top estate tax rate). $13.61M exemption (2024). Allocate exemption to dynasty trusts for multi-generational wealth transfer.",
        reasoning_framework="""
IRC §2611: GST = transfer to skip person (person 2+ generations below transferor or >37.5 years younger if not relative).
Three GST types:
  1. Direct skip: Outright transfer to skip person (e.g., gift to grandchild).
  2. Taxable termination: Trust interest terminates, skip person receives property.
  3. Taxable distribution: Distribution from trust to skip person.
GSTT exemption §2631: $13.61M (2024), same as BEA. Indexed for inflation.
Exemption allocation: Grantor allocates exemption to transfers on Form 709 (gifts) or Form 706 (estate).
Automatic allocation rules: Exemption auto-allocated to direct skips and indirect skips unless grantor opts out.
Inclusion ratio: (1 - exemption allocated / value) = portion subject to GST tax.
Dynasty trust: Irrevocable trust with GSTT exemption allocated; can last for perpetuities period (some states allow perpetual).
Annual exclusion GST: Direct skip gifts qualifying for annual exclusion also exempt from GST if under $18,000.
""",
        key_factors=["skip person definition", "GSTT exemption allocation", "inclusion ratio", "dynasty trust perpetuities", "automatic allocation rules"],
        primary_authority=["IRC §2601", "IRC §2611 (skip person)", "IRC §2631 (exemption)", "IRC §2642 (inclusion ratio)", "Treas. Reg. §26.2632-1"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.STATUTE,
        adversary_position="IRS may challenge late or improper GSTT exemption allocation, resulting in 40% tax on distributions to skip persons.",
        counter_arguments=["Timely exemption allocation on 709/706", "Automatic allocation not opted out", "Dynasty trust in perpetual jurisdiction"],
        controlling_precedent="IRC §2642: Inclusion ratio determines GST tax; zero ratio if full exemption allocated."
    ),

    DoctrineBlock(
        topic="special_use_valuation_2032A",
        keywords=["IRC 2032A", "special use valuation", "farm valuation", "real property", "qualified use"],
        conclusion_template="IRC §2032A allows estates to value qualified real property (farm/ranch/business) at actual use value rather than highest-and-best-use FMV. Max reduction: $1.39M (2024). Requires family operation and continuity.",
        reasoning_framework="""
IRC §2032A: Estate may elect to value qualified real property based on actual use (farming, ranching, trade/business) rather than development value.
Maximum reduction: $1,390,000 (2024), indexed.
Qualification requirements:
  - Real property located in US.
  - Property used for farming, ranching, or trade/business at decedent's death.
  - Decedent or family member materially participated in operation for 5 of 8 years before death.
  - Adjusted value of real/personal property used in business >= 50% of adjusted gross estate.
  - Qualified real property >= 25% of adjusted gross estate.
Material participation: Grantor must participate in management decisions, not just passive ownership.
Recapture: If heir ceases qualified use or disposes of property within 10 years of death, recapture tax imposed.
Recapture amount: Lesser of (1) appreciation since death, or (2) §2032A reduction.
Family member: Ancestor, spouse, lineal descendant, spouse of descendant.
""",
        key_factors=["qualified use at death", "material participation history", "50%/25% gross estate tests", "10-year holding period", "recapture risk"],
        primary_authority=["IRC §2032A", "Treas. Reg. §20.2032A-3 (material participation)", "Treas. Reg. §20.2032A-8 (election)", "Rev. Rul. 2006-66"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.STATUTE,
        adversary_position="IRS may disallow §2032A election if material participation not proven or gross estate tests fail.",
        counter_arguments=["Activity logs proving material participation", "Appraisal showing 50%/25% tests met", "Heirs commit to 10-year holding"],
        controlling_precedent="Rev. Rul. 2006-66: Material participation requires regular/continuous involvement in management."
    ),

    DoctrineBlock(
        topic="QPRT_qualified_personal_residence_trust",
        keywords=["QPRT", "IRC 2702", "personal residence", "term of years", "gift tax", "remainder interest"],
        conclusion_template="QPRT (IRC §2702(a)(3)(A)(ii)) allows grantor to transfer residence to trust, retain right to live there for term of years, remainder to beneficiaries. Gift tax = remainder interest PV. If grantor survives term, residence excluded from estate.",
        reasoning_framework="""
IRC §2702(a)(3)(A)(ii): QPRT exception to §2702 zero-valuation rule for retained interests.
Structure: Grantor transfers residence to irrevocable trust, retains rent-free use for term (e.g., 10-15 years), remainder to children.
Gift tax at creation: Taxable gift = FMV of remainder interest (residence value - PV of retained term, using §7520 rate).
Longer term = lower gift: Longer retained term reduces gift value but increases mortality risk.
Mortality risk: If grantor dies during term, residence included in gross estate under §2036 (retained life estate).
Post-term rent: If grantor survives term and wants to stay, must pay fair market rent to remainder beneficiaries.
One residence or two: QPRT may hold one principal residence and one vacation home; separate QPRTs for each.
Sale during term: If residence sold during term, proceeds held in trust; replacement residence purchased or term ends.
Basis step-up: If included in estate (grantor dies during term), heirs receive step-up in basis.
""",
        key_factors=["term length selection", "grantor survival probability", "§7520 discount rate", "post-term rent arrangement", "mortality risk"],
        primary_authority=["IRC §2702(a)(3)(A)(ii)", "Treas. Reg. §25.2702-5 (QPRT requirements)", "IRC §7520", "Rev. Rul. 2003-72"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.STATUTE,
        adversary_position="IRS may include residence in estate if grantor dies during term or continues to use without paying rent post-term.",
        counter_arguments=["QPRT complies with Treas. Reg. §25.2702-5", "Grantor survives term", "Fair market rent paid post-term if occupancy continues"],
        controlling_precedent="Treas. Reg. §25.2702-5: QPRT must meet strict requirements or retained interest valued at zero."
    ),

    DoctrineBlock(
        topic="GRAT_grantor_retained_annuity_trust",
        keywords=["GRAT", "IRC 2702", "annuity", "zeroed-out GRAT", "appreciation", "remainder interest"],
        conclusion_template="GRAT (IRC §2702(b)) allows grantor to transfer assets to trust, receive fixed annuity for term, remainder to beneficiaries. Zeroed-out GRAT: annuity = FMV, taxable gift near zero. If assets appreciate above §7520 rate, excess passes gift-tax-free.",
        reasoning_framework="""
IRC §2702(b): GRAT exception to zero-valuation rule; retained annuity valued actuarially.
Structure: Grantor transfers assets to trust, receives annual annuity (fixed dollar amount or fixed % of initial FMV) for term, remainder to beneficiaries.
Taxable gift = FMV of transferred assets - PV of annuity payments (using §7520 rate).
Zeroed-out GRAT: Set annuity so PV = FMV of assets; taxable gift = $0 or minimal.
Appreciation capture: If trust assets grow faster than §7520 rate, excess appreciation passes to remaindermen gift-tax-free.
Mortality risk: If grantor dies during term, pro-rata portion of trust included in gross estate under §2036.
Short terms reduce mortality risk: 2-year rolling GRATs common to minimize death-during-term risk.
Annuity funding: Trust must distribute annuity even if income insufficient; may distribute in kind.
No substitution: Assets may not be substituted post-transfer (unlike grantor trust §675(4)(C) power).
Clawback protection: GRAT gifts made under higher BEA protected if BEA declines before death.
""",
        key_factors=["§7520 rate at creation", "asset appreciation potential", "term length vs mortality risk", "zeroed-out vs taxable gift", "clawback protection"],
        primary_authority=["IRC §2702(b)", "Treas. Reg. §25.2702-3 (GRAT requirements)", "IRC §7520", "Walton v. Comm'r (115 TC 589)"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.STATUTE,
        adversary_position="IRS may include trust assets in estate if grantor dies during term or annuity undervalued.",
        counter_arguments=["GRAT complies with Treas. Reg. §25.2702-3", "Annuity properly calculated using §7520", "Short 2-year term minimizes mortality risk"],
        controlling_precedent="Walton v. Comm'r: GRAT remainder interest valued using §7520 rate; actual appreciation irrelevant to gift tax."
    ),

    DoctrineBlock(
        topic="family_limited_partnership_valuation_discounts",
        keywords=["FLP", "family limited partnership", "valuation discount", "lack of control", "lack of marketability", "IRC 2703", "IRC 2704"],
        conclusion_template="FLP allows fractional gifting of business interests with valuation discounts for lack of control (20-30%) and lack of marketability (20-35%). IRC §2703/§2704 restrict discounts if arrangement lacks business purpose or family controls restrictions.",
        reasoning_framework="""
FLP structure: Family business assets transferred to partnership; parents retain general partner (GP) interest (1-2%), children receive limited partner (LP) interests as gifts.
Valuation discounts:
  - Lack of control (minority discount): LP has no control over management, distributions, sale. 20-30% discount.
  - Lack of marketability: LP interests not publicly traded, restricted transfer. 20-35% discount.
  - Combined discounts: Often 40-50% total discount from pro-rata NAV.
IRC §2703(a): Buy-sell agreements and restrictions on transfer disregarded for estate/gift tax UNLESS:
  - Bona fide business arrangement,
  - Not device to transfer to family for less than full consideration,
  - Terms comparable to arms-length deals.
IRC §2704(b): Lapsing liquidation rights treated as transfer if family controls entity and restriction more stringent than state law.
Business purpose: Must demonstrate non-tax reasons (asset protection, centralized management, succession planning).
Adequate capitalization: Partnership should not be shell; must hold operating business or investment assets.
Avoid retained control: If parents gift LP interests but retain ability to liquidate partnership, §2036 may apply.
""",
        key_factors=["business purpose justification", "arms-length terms", "independent appraisal", "avoid §2703/§2704 disallowance", "operating business vs passive assets"],
        primary_authority=["IRC §2703", "IRC §2704", "Treas. Reg. §25.2703-1", "Estate of Jones v. Comm'r (116 TC 121)", "Holman v. Comm'r (601 F.3d 763)"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.STATUTE,
        adversary_position="IRS may disallow discounts if FLP lacks business purpose, parents retain control, or §2704 restrictions apply.",
        counter_arguments=["Non-tax business purposes documented", "Independent appraisal supporting discounts", "Operating business with active management"],
        controlling_precedent="Estate of Jones: Discounts allowed if FLP has bona fide business purpose and arms-length terms."
    ),

    DoctrineBlock(
        topic="portability_election_DSUE",
        keywords=["portability", "DSUE", "deceased spousal unused exclusion", "IRC 2010(c)(4)", "Form 706 election"],
        conclusion_template="IRC §2010(c)(4) portability allows surviving spouse to add deceased spouse's unused exclusion (DSUE) to own BEA. Requires timely complete Form 706 for deceased spouse, even if no estate tax due.",
        reasoning_framework="""
IRC §2010(c)(4): Surviving spouse's applicable exclusion = own BEA + DSUE of last deceased spouse.
DSUE (Deceased Spousal Unused Exclusion) = deceased spouse's BEA minus taxable estate and adjusted taxable gifts.
Portability election: File complete Form 706 for deceased spouse within 9 months of death + 6-month automatic extension.
Must file even if estate below BEA: DSUE only available if Form 706 filed (Rev. Proc. 2017-34 simplified filing for small estates).
Last deceased spouse rule: DSUE from most recent deceased spouse only; prior DSUE lost on remarriage and new spouse's death.
DSUE not indexed: DSUE amount fixed at first spouse's death; does not increase with inflation.
Planning consideration: Portability vs credit shelter trust (CST).
  - Portability: Simpler, no trust admin, all assets get basis step-up at survivor's death.
  - CST: Appreciating assets grow outside survivor's estate, state estate tax benefits, asset protection.
DSUE + CST hybrid: Use deceased's BEA for CST, port remaining DSUE to survivor.
""",
        key_factors=["timely Form 706 filing", "DSUE calculation accuracy", "last deceased spouse rule", "portability vs CST comparison", "state estate tax impact"],
        primary_authority=["IRC §2010(c)(4)", "IRC §2010(c)(5) (DSUE computation)", "Treas. Reg. §20.2010-2", "Rev. Proc. 2017-34"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.STATUTE,
        adversary_position="IRS may deny DSUE if Form 706 filed late or incomplete.",
        counter_arguments=["Timely complete Form 706 within 9 months + extension", "DSUE computed per §2010(c)(5)", "Rev. Proc. 2017-34 simplified filing for estates under BEA"],
        controlling_precedent="Treas. Reg. §20.2010-2: DSUE computed on properly filed estate tax return."
    ),

    DoctrineBlock(
        topic="stepped_up_basis_IRC_1014",
        keywords=["stepped-up basis", "IRC 1014", "FMV at death", "basis adjustment", "capital gains", "community property"],
        conclusion_template="IRC §1014 gives heirs stepped-up basis = FMV at decedent's death for inherited property. Eliminates capital gains on pre-death appreciation. Community property gets 100% step-up for both spouses' interests.",
        reasoning_framework="""
IRC §1014(a): Basis of property acquired from decedent = FMV at date of death (or alternate valuation date if elected).
Eliminates built-in gain: Pre-death appreciation escapes capital gains tax.
Example: Decedent bought stock for $10K, worth $1M at death. Heirs' basis = $1M; can sell immediately with zero gain.
Community property step-up IRC §1014(b)(6): In community property states, 100% of community property gets step-up, not just decedent's 50%.
  - Huge benefit: Surviving spouse's 50% also stepped up to FMV.
Separate property: Only decedent's interest gets step-up.
Joint tenancy: Only decedent's fractional interest steps up (usually 50% for spouses).
Property subject to IRC §2032A special use valuation: Basis = special use value, not FMV.
Carryover basis gifts: Lifetime gifts do NOT get step-up; donee takes donor's basis.
Planning: Hold appreciated assets until death for step-up vs gifting (carryover basis + gift tax).
§1022 carryover basis repealed: 2010 EGTRRA sunset would have imposed carryover basis; repealed by TCJA.
""",
        key_factors=["FMV at death", "community vs separate property", "joint tenancy titling", "lifetime gift vs testamentary bequest", "capital gain elimination"],
        primary_authority=["IRC §1014(a)", "IRC §1014(b)(6) (community property)", "IRC §1015 (carryover basis for gifts)", "Rev. Rul. 87-98"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.STATUTE,
        adversary_position="IRS may challenge FMV if appraisal unreasonably high; basis limited to estate tax value reported.",
        counter_arguments=["Independent appraisal at date of death", "Basis = FMV reported on Form 706", "Community property 100% step-up documented"],
        controlling_precedent="IRC §1014(a): Basis = FMV at death; no built-in gain carried over."
    ),

    DoctrineBlock(
        topic="disclaimers_IRC_2518",
        keywords=["qualified disclaimer", "IRC 2518", "9-month deadline", "irrevocable refusal", "redirect inheritance"],
        conclusion_template="IRC §2518 qualified disclaimer allows beneficiary to irrevocably refuse inheritance within 9 months of death. Disclaimed property passes as if beneficiary predeceased; no gift tax. Enables post-death tax planning.",
        reasoning_framework="""
IRC §2518: Qualified disclaimer treated as if disclaimant never received property; no gift tax on disclaimed property passing to next beneficiary.
Requirements for qualified disclaimer:
  1. Irrevocable written refusal.
  2. Received within 9 months of decedent's death (or turning 21 for minors).
  3. Disclaimant has not accepted property or benefits.
  4. Property passes to someone other than disclaimant without direction by disclaimant.
  5. Disclaimer complies with state law.
No direction: Disclaimant may not direct who receives property; must pass under will or state intestacy law.
Use cases: Surviving spouse disclaims to utilize deceased's BEA (CST), reduce survivor's estate, equalize distributions, qualification for benefits.
Partial disclaimer allowed: Can disclaim portion (e.g., amount exceeding BEA).
Retirement accounts: 9-month deadline applies from date of death, not date beneficiary learns of inheritance.
Estate reduction: Disclaimer by wealthier beneficiary shifts assets to lower-bracket heirs.
""",
        key_factors=["9-month deadline", "no acceptance of benefits", "irrevocable refusal", "state law compliance", "passage without direction"],
        primary_authority=["IRC §2518", "Treas. Reg. §25.2518-1", "Treas. Reg. §25.2518-2 (requirements)", "Walshire v. US (288 F.3d 342)"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.STATUTE,
        adversary_position="IRS may disqualify disclaimer if filed late, disclaimant accepted benefits, or directed property's passage.",
        counter_arguments=["Written disclaimer within 9 months", "No benefits accepted", "Property passes per will/intestacy without disclaimant control"],
        controlling_precedent="Treas. Reg. §25.2518-2: Qualified disclaimer must meet all five requirements."
    ),

    DoctrineBlock(
        topic="inadequate_consideration_2043",
        keywords=["IRC 2043", "partial consideration", "bargain sale", "gift element", "estate inclusion"],
        conclusion_template="IRC §2043 applies when decedent transferred property for partial consideration less than FMV. Estate includes excess of FMV over consideration. Common in installment sales to family, SCINs, private annuities.",
        reasoning_framework="""
IRC §2043(a): If property transferred for partial consideration, gross estate includes excess of FMV over consideration received.
Example: Decedent sold $1M property to child for $600K. At death, $400K included in gross estate.
Adequate and full consideration: If FMV paid, no estate inclusion.
Bargain sale to family: If sale below FMV, gift element ($400K in example) may trigger gift tax and §2043 inclusion.
SCIN (Self-Canceling Installment Note): Note cancels at death; if premium paid, bona fide sale. If inadequate premium, §2043 inclusion.
Private annuity: Transfer for promise to pay annuity for life. If actuarially sound, no §2043 inclusion; if undervalued, inclusion.
Bona fide sale safe harbor: If transaction at arms-length with unrelated party for FMV, no inclusion (even if paid in installments).
Family sale scrutiny: IRS challenges installment sales to family; require appraisal, adequate interest rate (AFR), note security.
""",
        key_factors=["FMV vs consideration paid", "arms-length terms", "adequate interest rate", "bona fide sale elements", "appraisal support"],
        primary_authority=["IRC §2043", "Treas. Reg. §20.2043-1", "Estate of Frane v. Comm'r (98 TC 341)", "Rev. Rul. 77-193 (SCIN)"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.STATUTE,
        adversary_position="IRS may assert §2043 inclusion if sale to family member undervalued or lacks arms-length terms.",
        counter_arguments=["Independent appraisal at FMV", "Adequate interest (AFR or higher)", "Note secured by property", "Bona fide sale intent documented"],
        controlling_precedent="Estate of Frane: Partial consideration transactions scrutinized; must prove FMV paid."
    ),

    DoctrineBlock(
        topic="powers_of_appointment_IRC_2041",
        keywords=["general power of appointment", "IRC 2041", "5-and-5 power", "limited power", "estate inclusion"],
        conclusion_template="IRC §2041 includes in gross estate property over which decedent held general power of appointment (power to appoint to self, estate, creditors). Limited power (to others only) excluded. 5-and-5 power safe harbor.",
        reasoning_framework="""
IRC §2041(a)(2): General power of appointment = power to appoint property to decedent, estate, creditors, or creditors of estate.
Estate inclusion: Property subject to general power included in gross estate, even if power unexercised.
Limited power (special power): Power to appoint only to specific class (e.g., children) is not general power; no inclusion.
5-and-5 power IRC §2041(b)(2): Power to withdraw greater of $5,000 or 5% of trust corpus is NOT general power.
  - Lapse of power: If withdrawal right lapses, excess over 5-and-5 is gift.
  - Crummey power lapses: Use 5-and-5 safe harbor to avoid taxable lapse.
Testamentary power: Power exercisable only at death; if general, property included in estate.
Lifetime release: If general power released >3 years before death, no inclusion (unless §2035 applies).
Ascertainable standard exception: Power limited to health, education, support, maintenance (HEMS) is not general power.
Trustee powers: Grantor as trustee with discretion over distributions = general power if no ascertainable standard.
""",
        key_factors=["general vs limited power", "5-and-5 safe harbor", "ascertainable standard", "timing of release", "trustee discretion limits"],
        primary_authority=["IRC §2041", "IRC §2041(b)(2) (5-and-5)", "Treas. Reg. §20.2041-1", "Estate of Vissering v. Comm'r (990 F.2d 578)"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.STATUTE,
        adversary_position="IRS may assert general power if discretion lacks ascertainable standard or lapse exceeds 5-and-5.",
        counter_arguments=["Power limited to HEMS standard", "Withdrawal rights within 5-and-5 safe harbor", "Independent trustee holds discretion"],
        controlling_precedent="Estate of Vissering: Power limited to ascertainable standard not general power."
    ),

    DoctrineBlock(
        topic="deathbed_transfers_IRC_2035",
        keywords=["IRC 2035", "three-year rule", "gifts within three years", "life insurance", "gross-up"],
        conclusion_template="IRC §2035(a) includes in gross estate certain transfers made within 3 years of death: life insurance, retained interests under §2036/2037/2038, gift tax paid on gifts within 3 years (gross-up). Other gifts excluded.",
        reasoning_framework="""
IRC §2035(a): Property transferred within 3 years of death included in gross estate IF:
  1. Transfer was of interest that would have been included under §2036 (retained life estate), §2037 (reversionary interest), §2038 (revocable transfer), or §2042 (life insurance).
  2. Gift tax paid on transfers within 3 years (gross-up rule §2035(b)).
Life insurance 3-year rule: If policy transferred within 3 years of death, proceeds included in gross estate under §2035(a)(2) + §2042.
Gift tax gross-up §2035(b): Gift tax paid on gifts made within 3 years of death added to gross estate (prevents deathbed gift tax removal).
Gifts NOT included: Outright gifts made >3 years before death excluded (even if taxable gifts).
GRAT/QPRT 3-year rule: If grantor dies during term, assets included under §2036 (retained interest), NOT §2035.
Contemplation of death: Pre-1981, subjective test; repealed by ERTA; now bright-line 3-year rule.
Planning: Transfer life insurance >3 years before anticipated death to avoid inclusion.
""",
        key_factors=["3-year lookback", "life insurance transfers", "gift tax gross-up", "§2036/2038 transfers", "outright gifts excluded"],
        primary_authority=["IRC §2035(a)", "IRC §2035(b) (gross-up)", "IRC §2042", "Treas. Reg. §20.2035-1", "Rev. Rul. 84-179"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.STATUTE,
        adversary_position="IRS includes transferred life insurance if decedent dies within 3 years, even if all incidents relinquished.",
        counter_arguments=["Transfer >3 years before death", "No retained interests under §2036-2038", "Gift tax gross-up properly computed"],
        controlling_precedent="IRC §2035(a): 3-year bright-line rule for life insurance and retained interest transfers."
    ),

    DoctrineBlock(
        topic="alternate_valuation_IRC_2032",
        keywords=["alternate valuation", "IRC 2032", "6-month valuation", "estate tax reduction", "disposition date"],
        conclusion_template="IRC §2032 allows estate to elect alternate valuation date (6 months after death or earlier disposition) instead of date-of-death FMV. Reduces estate tax if both estate value AND tax liability decline.",
        reasoning_framework="""
IRC §2032(a): Estate may elect to value all property at alternate valuation date = 6 months after death, EXCEPT property disposed/distributed before then valued at disposition date.
Requirements to elect:
  1. Alternate valuation reduces total gross estate value, AND
  2. Alternate valuation reduces estate tax liability (after credits).
Both conditions mandatory: Cannot elect if reduces value but not tax (e.g., if estate below BEA).
Disposition before 6 months: Property sold/distributed before 6-month date valued at disposition date, not 6 months.
All-or-nothing election: Must apply to entire estate; cannot cherry-pick assets.
Interest/rent accruals: Post-death income excluded from alternate value; only property value counted.
Marketable securities: Valued at 6-month date or sale date if earlier.
No alternate for income in respect of decedent (IRD): IRD items (e.g., unpaid salary, retirement distributions) valued at date-of-death rights.
Planning use: Volatile markets, declining property values, estate just above BEA.
""",
        key_factors=["6-month date or earlier disposition", "must reduce value AND tax", "all-or-nothing election", "exclusion of post-death income", "marketable securities volatility"],
        primary_authority=["IRC §2032(a)", "IRC §2032(c) (election requirements)", "Treas. Reg. §20.2032-1", "Rev. Rul. 83-30"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.STATUTE,
        adversary_position="IRS may deny election if requirements not met (e.g., tax liability does not decline).",
        counter_arguments=["Both gross estate and tax reduced", "Timely election on Form 706", "Proper valuation at 6-month date or disposition"],
        controlling_precedent="IRC §2032(c): Must reduce BOTH value and tax; cannot elect if only value declines."
    ),

    DoctrineBlock(
        topic="charitable_lead_trust_IRC_2522",
        keywords=["CLT", "charitable lead trust", "IRC 2522", "lead interest", "remainder to heirs", "annuity trust"],
        conclusion_template="Charitable Lead Trust (CLT) pays income to charity for term of years, remainder to heirs. IRC §2522 estate deduction = present value of lead interest. Reduces estate tax, shifts appreciation to heirs.",
        reasoning_framework="""
CLT structure: Trust pays annuity or unitrust to charity for term (e.g., 20 years), remainder to family.
Estate tax deduction IRC §2522: PV of charitable lead interest using §7520 rate.
CLAT (Charitable Lead Annuity Trust): Fixed dollar annuity to charity.
CLUT (Charitable Lead Unitrust): Fixed % of annually-revalued trust assets to charity.
Gift/estate tax on remainder: Remainder to heirs is taxable gift/estate transfer; value = FMV - PV of lead interest.
Zeroed-out CLT: Set lead interest PV = FMV of assets; remainder gift = zero. Appreciation passes to heirs gift-tax-free.
Grantor CLT: If grantor trust, grantor gets income tax deduction for PV of lead interest but pays income tax on trust income (even though charity receives it).
Non-grantor CLT: Trust pays income tax on income not distributed to charity; no upfront income tax deduction.
High §7520 rate favors CLT: Higher discount rate = higher PV of lead interest = larger deduction.
Use case: Testamentary CLT in will/revocable trust at death; reduces estate tax via charitable deduction.
""",
        key_factors=["§7520 discount rate", "lead term length", "grantor vs non-grantor", "zeroed-out remainder", "income tax treatment"],
        primary_authority=["IRC §2522", "IRC §664 (CLAT/CLUT)", "IRC §7520", "Treas. Reg. §20.2055-2 (split-interest)", "Rev. Rul. 77-374"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.STATUTE,
        adversary_position="IRS may challenge CLT deduction if trust violates split-interest rules or lead interest undervalued.",
        counter_arguments=["CLT complies with IRC §664 or Treas. Reg. §20.2055-2", "Lead interest PV computed per §7520", "Qualified charity beneficiary"],
        controlling_precedent="IRC §2522: Estate deduction for PV of income interest passing to charity."
    ),

    DoctrineBlock(
        topic="minority_discount_valuation",
        keywords=["minority discount", "lack of control", "FLP", "closely-held business", "valuation", "IRC 2031"],
        conclusion_template="Minority discount reduces FMV of non-controlling interests in closely-held entities (FLP, LLC, corp). Typical range: 20-40%. Based on lack of control over management, distributions, liquidation. Must prove via appraisal and comparable sales.",
        reasoning_framework="""
IRC §2031 FMV standard: Price willing buyer pays willing seller, both with reasonable knowledge, neither under compulsion.
Minority interest: <50% ownership; lacks control over entity decisions.
Lack of control factors:
  - Cannot elect directors/managers.
  - Cannot force distributions.
  - Cannot compel sale/liquidation.
  - Cannot set compensation.
Discount range: 20-40% typical for minority interests.
Appraisal methods: Comparable sales of minority interests, income approach, market approach.
Built-in gains discount: If entity holds appreciated assets, discount for built-in capital gains tax liability.
Revenue Ruling 59-60: Factors for valuing closely-held stock (nature of business, economic outlook, financial condition, earning capacity, dividend capacity, goodwill, sales of stock, comparable public companies).
Marketability discount separate: Often combined with minority discount; total 40-60%.
IRS scrutiny: Family-controlled entities with discounts trigger audits; need strong appraisal.
""",
        key_factors=["<50% ownership", "lack of control documented", "independent appraisal", "comparable sales data", "built-in gains"],
        primary_authority=["IRC §2031", "Rev. Rul. 59-60", "Estate of Watts v. Comm'r (823 F.2d 483)", "Propstra v. US (680 F.2d 1248)"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.REGULATION,
        adversary_position="IRS may challenge minority discount if family controls entity or restrictions manufactured to reduce value.",
        counter_arguments=["Qualified independent appraisal", "Comparable minority sales data", "Bona fide business purpose for entity"],
        controlling_precedent="Estate of Watts: Minority discount allowed if lack of control genuine and supported by appraisal."
    ),

    DoctrineBlock(
        topic="marketability_discount_valuation",
        keywords=["marketability discount", "lack of marketability", "illiquid asset", "transfer restrictions", "FLP", "closely-held stock"],
        conclusion_template="Marketability discount reduces FMV of interests lacking ready market due to illiquidity, transfer restrictions, or private nature. Typical range: 20-40%. Applies to FLP units, closely-held stock, restricted securities.",
        reasoning_framework="""
Lack of marketability: No public market, difficult to sell quickly, transfer restrictions.
Factors supporting discount:
  - No public trading.
  - Buy-sell agreement restrictions.
  - Right of first refusal.
  - Required consents for transfer.
  - Small pool of potential buyers (family members).
  - Illiquid underlying assets (real estate, operating business).
Typical discount range: 20-40%; combined with minority discount can reach 50-60%.
Studies: Restricted stock studies, pre-IPO studies show 20-45% discounts for illiquidity.
Appraisal requirement: Qualified appraiser must analyze entity, restrictions, comparable restricted sales.
IRC §2703 limitation: Transfer restrictions disregarded if not bona fide business arrangement or comparables to arms-length.
FLP marketability: LP units typically have higher marketability discount than GP interests (less control, more restrictions).
""",
        key_factors=["transfer restrictions", "lack of public market", "appraisal support", "comparable restricted sales", "§2703 compliance"],
        primary_authority=["IRC §2031", "IRC §2703", "Rev. Rul. 59-60", "Estate of Newhouse v. Comm'r (94 TC 193)", "Mandelbaum v. Comm'r (TCM 1995-255)"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.CASE_LAW,
        adversary_position="IRS may disallow marketability discount if restrictions lack business purpose or are testamentary.",
        counter_arguments=["Independent appraisal", "Bona fide business purpose for restrictions", "Comparable restricted stock sales data"],
        controlling_precedent="Mandelbaum: Marketability discount allowed based on 10-factor analysis (put rights, dividends, restrictions, etc.)."
    ),

    DoctrineBlock(
        topic="defined_value_formula_clause",
        keywords=["defined value clause", "formula clause", "valuation adjustment", "Wandry", "price adjustment", "gift tax"],
        conclusion_template="Defined value formula clause transfers fixed dollar amount or formula-based value to donees, with excess reverting to grantor or charity. Wandry formula upheld: transfer units worth $X million, excess to charity. Protects against IRS valuation adjustments.",
        reasoning_framework="""
Formula clause: Gift defined by value, not units. E.g., 'Transfer FLP units worth $10M to children, remainder to charity.'
Valuation protection: If IRS revalues units higher, excess goes to charity, not treated as additional gift to children.
Wandry v. Comm'r (103 AFTR 2d 2009-1956): Tax Court upheld defined value formula clause; IRS revaluation did not create additional gift.
Conditions for validity:
  - Formula clearly defines value transferred.
  - Excess passes to qualified charity or reverts to grantor.
  - No risk of violating savings clause (McCord issue resolved by charity recipient).
Price adjustment clause vs formula clause:
  - Price adjustment: 'If IRS determines higher value, children return excess.' INVALID (Procter, McCord).
  - Defined value: 'Transfer value of $X, determined by later appraisal/IRS.' VALID (Wandry).
Charity backstop: Excess passes to charity if IRS values higher; avoids gift tax on revaluation.
Savings clause risk: If excess reverts to grantor, may be void as against public policy (older cases); charity safer.
""",
        key_factors=["formula defines value not units", "charity recipient for excess", "appraisal process", "avoidance of price adjustment clause", "Wandry precedent"],
        primary_authority=["Wandry v. Comm'r (103 AFTR 2d 2009-1956)", "Estate of Christiansen v. Comm'r (586 F.3d 1061)", "Procter v. Comm'r (142 F.2d 824)", "McCord v. Comm'r (461 F.3d 614)"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.CASE_LAW,
        adversary_position="IRS may challenge defined value clause if not clearly drafted or if savings clause violates public policy.",
        counter_arguments=["Wandry formula upheld by Tax Court", "Excess passes to qualified charity", "Independent appraisal establishes initial value"],
        controlling_precedent="Wandry: Defined value formula valid if excess passes to charity, not back to donor."
    ),

    DoctrineBlock(
        topic="estate_freeze_IRC_2701",
        keywords=["IRC 2701", "estate freeze", "preferred stock recapitalization", "junior equity", "senior equity", "valuation"],
        conclusion_template="IRC §2701 prevents estate freeze via preferred stock recapitalization by zeroing out senior retained interests unless meet strict requirements (qualified payments). Transfers junior equity to family at low gift tax by retaining 'valueless' preferred.",
        reasoning_framework="""
IRC §2701 purpose: Prevent undervaluation of gifts when senior family members retain preferred interests and transfer common to juniors.
Estate freeze structure (pre-2701): Parent holds common stock, recapitalizes into preferred (parent) + common (children). Common valued low; preferred retains value.
§2701 zero-valuation rule: Retained preferred interest valued at ZERO for gift tax unless:
  - Qualified payment right (fixed cumulative dividend), OR
  - Market quotation available, OR
  - Same class as transferred interest.
Qualified payment: Cumulative dividend at fixed rate payable at fixed intervals.
Non-qualified payment: Discretionary dividends, liquidation preferences → valued at zero.
Subtraction method: Gift = FMV of entity - value of retained interest. If retained interest = zero, gift = full FMV.
Applicable family member: Spouse, ancestor, lineal descendant → §2701 applies.
Minimum value rule: Transferred interest valued at least 10% of entity FMV + value of senior equity.
Planning post-2701: Use GRAT/QPRT (IRC §2702 exceptions) instead of preferred recaps.
""",
        key_factors=["qualified vs non-qualified payments", "subtraction method", "minimum value rule", "applicable family member", "post-2701 alternatives"],
        primary_authority=["IRC §2701", "IRC §2701(a)(3) (qualified payment)", "Treas. Reg. §25.2701-1", "Treas. Reg. §25.2701-2 (subtraction method)"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.STATUTE,
        adversary_position="IRS applies §2701 zero-valuation if retained preferred lacks qualified payment rights.",
        counter_arguments=["Preferred has qualified cumulative dividend", "Same class transfer avoids §2701", "Use GRAT/QPRT instead of preferred recap"],
        controlling_precedent="IRC §2701: Retained interests valued at zero unless qualified payment or same class."
    ),

    DoctrineBlock(
        topic="installment_sale_to_grantor_trust",
        keywords=["installment sale", "grantor trust", "IDGT", "intentionally defective", "sale to trust", "note"],
        conclusion_template="Installment sale to intentionally defective grantor trust (IDGT): Grantor sells assets to trust for promissory note. No capital gain (grantor trust rules ignore sale). Trust appreciation passes to beneficiaries outside estate. Note in estate = sale price.",
        reasoning_framework="""
IDGT structure: Irrevocable trust is grantor trust for income tax (IRC §671-679) but NOT for estate/gift tax.
Grantor trust income tax: Grantor pays income tax on all trust income; trust distributions tax-free.
Intentionally defective: Include grantor trust trigger (e.g., power to substitute assets §675(4)(C), spousal distribution §677).
Installment sale: Grantor sells appreciated assets to IDGT for promissory note (face value = FMV).
No capital gain: Rev. Rul. 85-13: Sale to grantor trust ignored for income tax; no gain recognized.
Estate planning benefit: Trust assets appreciate outside grantor's estate; promissory note frozen in estate at sale price.
Note terms: Adequate interest (AFR), balloon payment or amortizing, secured or unsecured.
Seed capital: Trust must have 10% equity (cash or prior gifts) to avoid sale treated as disguised gift.
Grantor death: Note included in estate at face value; trust appreciation excluded.
Income tax at death: Trust becomes non-grantor trust; distributions taxable to beneficiaries going forward.
""",
        key_factors=["grantor trust status", "10% seed capital", "adequate interest rate (AFR)", "note in estate at face value", "trust appreciation excluded"],
        primary_authority=["IRC §671-679 (grantor trust)", "Rev. Rul. 85-13 (no gain on sale to grantor trust)", "IRC §1274 (AFR)", "IRC §7872 (below-market loans)"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        zone=AnalysisZone.PLANNING,
        authority_level=AuthorityLevel.REVENUE_RULING,
        adversary_position="IRS may recharacterize sale as gift if inadequate consideration, no seed capital, or below-AFR interest.",
        counter_arguments=["Rev. Rul. 85-13 supports no-gain treatment", "10% seed capital funded with prior gifts", "Note at AFR or higher"],
        controlling_precedent="Rev. Rul. 85-13: Sale to grantor trust not recognized for income tax; no capital gain."
    )
]

# ==================== THREE-LAYER RESPONSE ENGINE ====================
class EstateTaxEngine:
    def __init__(self):
        self.doctrines = ESTATE_TAX_DOCTRINES
        self.doctrine_index = self._build_index()
        self.query_log = []
        self.metrics = defaultdict(int)
        self.drift_observations = []

    def _build_index(self) -> Dict[str, List[DoctrineBlock]]:
        index = defaultdict(list)
        for doctrine in self.doctrines:
            for keyword in doctrine.keywords:
                index[keyword.lower()].append(doctrine)
            index[doctrine.topic].append(doctrine)
        return index

    def analyze(self, question: str, mode: ResponseMode, zone: AnalysisZone, context: Dict[str, Any]) -> QueryResponse:
        start_time = time.time()

        # Layer 1: Doctrine Cache (0-200ms)
        triggered_doctrines = self._match_doctrines(question)

        if triggered_doctrines and mode == ResponseMode.FAST:
            answer = self._fast_response(triggered_doctrines, question)
            confidence = triggered_doctrines[0].confidence
        elif triggered_doctrines:
            answer = self._defense_response(triggered_doctrines, question, zone, context)
            confidence = ConfidenceLevel.DEFENSIBLE
        else:
            answer = self._deep_analysis(question, context)
            confidence = ConfidenceLevel.DISCLOSURE

        sources = [auth for d in triggered_doctrines[:3] for auth in d.primary_authority]
        reasoning_chain = [d.reasoning_framework[:200] + "..." for d in triggered_doctrines[:2]]

        response_time = (time.time() - start_time) * 1000
        determinism_hash = hashlib.sha256(
            f"{question}:{mode}:{zone}:{','.join([d.topic for d in triggered_doctrines])}".encode()
        ).hexdigest()[:16]

        self._record_query(question, mode, triggered_doctrines, response_time)

        return QueryResponse(
            answer=answer,
            mode=mode,
            confidence=confidence,
            sources=sources[:5],
            reasoning_chain=reasoning_chain,
            determinism_hash=determinism_hash,
            response_time_ms=round(response_time, 2),
            doctrines_triggered=[d.topic for d in triggered_doctrines],
            epistemic_warnings=self._epistemic_check(answer)
        )

    def _match_doctrines(self, question: str) -> List[DoctrineBlock]:
        question_lower = question.lower()
        scores = defaultdict(float)

        for doctrine in self.doctrines:
            score = 0.0
            for keyword in doctrine.keywords:
                if keyword.lower() in question_lower:
                    score += 2.0
            if doctrine.topic.replace("_", " ") in question_lower:
                score += 3.0

            if score > 0:
                scores[doctrine] = score

        return sorted(scores.keys(), key=lambda d: scores[d], reverse=True)[:5]

    def _fast_response(self, doctrines: List[DoctrineBlock], question: str) -> str:
        primary = doctrines[0]
        return f"{primary.conclusion_template}\n\nKey factors: {', '.join(primary.key_factors[:3])}. Primary authority: {primary.primary_authority[0]}."

    def _defense_response(self, doctrines: List[DoctrineBlock], question: str, zone: AnalysisZone, context: Dict[str, Any]) -> str:
        primary = doctrines[0]
        answer = f"ANALYSIS ({zone.value}):\n\n{primary.conclusion_template}\n\n"
        answer += f"REASONING:\n{primary.reasoning_framework[:500]}...\n\n"
        answer += f"KEY FACTORS:\n" + "\n".join([f"- {factor}" for factor in primary.key_factors[:5]]) + "\n\n"
        answer += f"AUTHORITY:\n" + "\n".join([f"- {auth}" for auth in primary.primary_authority[:3]]) + "\n\n"

        if primary.adversary_position:
            answer += f"ADVERSARY POSITION: {primary.adversary_position}\n\n"
            answer += f"COUNTER-ARGUMENTS:\n" + "\n".join([f"- {arg}" for arg in primary.counter_arguments[:3]])

        return answer

    def _deep_analysis(self, question: str, context: Dict[str, Any]) -> str:
        return f"DEEP ANALYSIS REQUIRED:\n\nThe question '{question}' involves estate tax issues requiring multi-source synthesis beyond cached doctrines. Recommend consulting IRC provisions, Treasury Regulations, and case law for: gross estate inclusion analysis, valuation methodology, deduction availability, and filing requirements.\n\nConsider context: {list(context.keys())} provided."

    def _epistemic_check(self, answer: str) -> List[str]:
        warnings = []
        banned_phrases = ["always", "never", "guaranteed", "certainly", "definitely will"]
        for phrase in banned_phrases:
            if phrase in answer.lower():
                warnings.append(f"Epistemic overreach: '{phrase}' may overstate certainty.")
        return warnings

    def _record_query(self, question: str, mode: ResponseMode, doctrines: List[DoctrineBlock], response_time: float):
        self.query_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "question": question,
            "mode": mode.value,
            "doctrines_triggered": [d.topic for d in doctrines],
            "response_time_ms": response_time
        })
        self.metrics["total_queries"] += 1
        self.metrics[f"mode_{mode.value}"] += 1

    def get_health(self) -> Dict[str, Any]:
        return {
            "engine_id": ENGINE_ID,
            "engine_name": ENGINE_NAME,
            "version": VERSION,
            "status": "healthy",
            "doctrines_loaded": len(self.doctrines),
            "queries_processed": self.metrics["total_queries"],
            "avg_response_time_ms": round(
                sum([q["response_time_ms"] for q in self.query_log[-100:]]) / max(len(self.query_log[-100:]), 1), 2
            ) if self.query_log else 0,
            "mode_distribution": {
                "FAST": self.metrics["mode_FAST"],
                "DEFENSE": self.metrics["mode_DEFENSE"],
                "MEMO": self.metrics["mode_MEMO"]
            }
        }

# ==================== FASTAPI APPLICATION ====================
engine = EstateTaxEngine()

app = FastAPI(
    title=ENGINE_NAME,
    version=VERSION,
    description="Estate and gift tax planning intelligence with IRC §2001-2664 coverage"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def startup_event():
    logger.info(f"{ENGINE_NAME} v{VERSION} starting on port {PORT}")
    logger.info(f"Loaded {len(engine.doctrines)} estate tax doctrine blocks")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"{ENGINE_NAME} shutting down. Processed {engine.metrics['total_queries']} queries.")

@app.get("/health")
async def health_check():
    return engine.get_health()

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    try:
        response = engine.analyze(
            question=request.question,
            mode=request.mode,
            zone=request.zone,
            context=request.context
        )
        return response
    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/doctrines")
async def list_doctrines():
    return {
        "total": len(engine.doctrines),
        "topics": [d.topic for d in engine.doctrines],
        "by_zone": {
            zone.value: len([d for d in engine.doctrines if d.zone == zone])
            for zone in AnalysisZone
        }
    }

@app.get("/metrics")
async def get_metrics():
    return {
        "total_queries": engine.metrics["total_queries"],
        "mode_breakdown": {
            "FAST": engine.metrics["mode_FAST"],
            "DEFENSE": engine.metrics["mode_DEFENSE"],
            "MEMO": engine.metrics["mode_MEMO"]
        },
        "recent_queries": engine.query_log[-10:]
    }

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=PORT,
        log_level="info"
    )
