"""
LM04 Mineral Interest Tracker - Doctrine Cache
================================================

Comprehensive mineral interest doctrines covering:
- Mineral vs royalty distinction
- Executive rights doctrine
- Bonus, delay rental, development rights
- Non-participating royalty interests (NPRI)
- Term mineral interests
- Life estate minerals
- Fee simple determinable minerals
- Possibility of reverter
- Mineral servitude (Louisiana comparison)
- Dormant mineral acts
- Pooling effects on mineral interests
- Fractional interest calculations
- Undivided interests and partition
- Texas-specific mineral law

Engine: LM04 | Version: 1.0.0
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from loguru import logger


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class DoctrineCategory(str, Enum):
    """Categories of mineral interest doctrines."""
    OWNERSHIP = "ownership"
    CONVEYANCE = "conveyance"
    RIGHTS_BUNDLE = "rights_bundle"
    INTEREST_TYPES = "interest_types"
    TEMPORAL = "temporal"
    FRACTIONAL = "fractional"
    POOLING = "pooling"
    PROBATE = "probate"
    CONFLICT = "conflict"
    LOUISIANA_COMPARE = "louisiana_compare"
    DORMANT_MINERAL = "dormant_mineral"
    PARTITION = "partition"
    EXECUTIVE_RIGHTS = "executive_rights"
    SURFACE_MINERAL = "surface_mineral"
    LEASING = "leasing"
    TEXAS_SPECIFIC = "texas_specific"


class DoctrineAuthority(str, Enum):
    """Authority level of a doctrine."""
    CONSTITUTIONAL = "constitutional"
    STATUTORY = "statutory"
    CASE_LAW_SUPREME = "case_law_supreme"
    CASE_LAW_APPELLATE = "case_law_appellate"
    REGULATORY = "regulatory"
    TREATISE = "treatise"
    PRACTICE_GUIDE = "practice_guide"
    INDUSTRY_STANDARD = "industry_standard"


class Jurisdiction(str, Enum):
    """Jurisdictions covered."""
    TEXAS = "texas"
    LOUISIANA = "louisiana"
    NEW_MEXICO = "new_mexico"
    OKLAHOMA = "oklahoma"
    FEDERAL = "federal"
    MULTI_STATE = "multi_state"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class DoctrineBlock:
    """Single doctrine knowledge block."""
    block_id: str
    title: str
    category: DoctrineCategory
    authority: DoctrineAuthority
    jurisdiction: Jurisdiction
    content: str
    legal_citations: list[str] = field(default_factory=list)
    key_principles: list[str] = field(default_factory=list)
    practical_notes: list[str] = field(default_factory=list)
    related_blocks: list[str] = field(default_factory=list)
    effective_date: str = ""
    last_updated: str = ""
    hash_digest: str = ""

    def __post_init__(self) -> None:
        if not self.last_updated:
            self.last_updated = datetime.now(timezone.utc).isoformat()
        if not self.hash_digest:
            self.hash_digest = self._compute_hash()

    def _compute_hash(self) -> str:
        payload = f"{self.block_id}|{self.title}|{self.content}"
        return hashlib.sha256(payload.encode()).hexdigest()[:16]

    def to_dict(self) -> dict[str, Any]:
        return {
            "block_id": self.block_id,
            "title": self.title,
            "category": self.category.value,
            "authority": self.authority.value,
            "jurisdiction": self.jurisdiction.value,
            "content": self.content,
            "legal_citations": self.legal_citations,
            "key_principles": self.key_principles,
            "practical_notes": self.practical_notes,
            "related_blocks": self.related_blocks,
            "effective_date": self.effective_date,
            "last_updated": self.last_updated,
            "hash_digest": self.hash_digest,
        }


# ---------------------------------------------------------------------------
# Doctrine Cache
# ---------------------------------------------------------------------------

class MineralInterestDoctrineCache:
    """Full doctrine cache for LM04 Mineral Interest Tracker."""

    def __init__(self) -> None:
        self._blocks: dict[str, DoctrineBlock] = {}
        self._category_index: dict[str, list[str]] = {}
        self._keyword_index: dict[str, list[str]] = {}
        self._load_all_doctrines()
        logger.info(
            "LM04 DoctrineCache loaded: {} blocks across {} categories",
            len(self._blocks),
            len(self._category_index),
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_block(self, block_id: str) -> DoctrineBlock | None:
        """Retrieve a single doctrine block by ID."""
        return self._blocks.get(block_id)

    def get_by_category(self, category: DoctrineCategory) -> list[DoctrineBlock]:
        """Retrieve all blocks in a category."""
        ids = self._category_index.get(category.value, [])
        return [self._blocks[bid] for bid in ids if bid in self._blocks]

    def search(self, keyword: str) -> list[DoctrineBlock]:
        """Search doctrines by keyword."""
        keyword_lower = keyword.lower()
        results: list[DoctrineBlock] = []
        seen: set[str] = set()
        # Check keyword index first
        for term, block_ids in self._keyword_index.items():
            if keyword_lower in term:
                for bid in block_ids:
                    if bid not in seen and bid in self._blocks:
                        results.append(self._blocks[bid])
                        seen.add(bid)
        # Fallback to content search
        for bid, block in self._blocks.items():
            if bid not in seen and keyword_lower in block.content.lower():
                results.append(block)
                seen.add(bid)
        return results

    def get_all_blocks(self) -> list[DoctrineBlock]:
        """Return all doctrine blocks."""
        return list(self._blocks.values())

    def get_related(self, block_id: str) -> list[DoctrineBlock]:
        """Get blocks related to the given block."""
        block = self._blocks.get(block_id)
        if not block:
            return []
        return [
            self._blocks[rid]
            for rid in block.related_blocks
            if rid in self._blocks
        ]

    def export_json(self) -> str:
        """Export entire cache as JSON."""
        return json.dumps(
            [b.to_dict() for b in self._blocks.values()],
            indent=2,
        )

    @property
    def block_count(self) -> int:
        return len(self._blocks)

    @property
    def category_counts(self) -> dict[str, int]:
        return {k: len(v) for k, v in self._category_index.items()}

    # ------------------------------------------------------------------
    # Internal indexing
    # ------------------------------------------------------------------

    def _register(self, block: DoctrineBlock) -> None:
        self._blocks[block.block_id] = block
        cat = block.category.value
        self._category_index.setdefault(cat, []).append(block.block_id)
        # Build keyword index from title and key_principles
        words = block.title.lower().split()
        for w in words:
            cleaned = w.strip("(),.:;-\"'")
            if len(cleaned) > 2:
                self._keyword_index.setdefault(cleaned, []).append(block.block_id)
        for principle in block.key_principles:
            for w in principle.lower().split():
                cleaned = w.strip("(),.:;-\"'")
                if len(cleaned) > 3:
                    self._keyword_index.setdefault(cleaned, []).append(block.block_id)

    # ------------------------------------------------------------------
    # Doctrine definitions
    # ------------------------------------------------------------------

    def _load_all_doctrines(self) -> None:
        self._load_ownership_doctrines()
        self._load_mineral_royalty_distinction()
        self._load_executive_rights_doctrines()
        self._load_interest_type_doctrines()
        self._load_temporal_interest_doctrines()
        self._load_fractional_calculation_doctrines()
        self._load_pooling_doctrines()
        self._load_probate_doctrines()
        self._load_conveyance_doctrines()
        self._load_conflict_doctrines()
        self._load_louisiana_comparison()
        self._load_dormant_mineral_doctrines()
        self._load_partition_doctrines()
        self._load_surface_mineral_doctrines()
        self._load_leasing_doctrines()
        self._load_texas_specific_doctrines()

    # === OWNERSHIP =====================================================

    def _load_ownership_doctrines(self) -> None:
        self._register(DoctrineBlock(
            block_id="LM04-OWN-001",
            title="Fee Simple Absolute Mineral Ownership",
            category=DoctrineCategory.OWNERSHIP,
            authority=DoctrineAuthority.CASE_LAW_SUPREME,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "Fee simple absolute mineral ownership is the most complete form of mineral "
                "estate ownership. The owner holds all rights in the mineral estate without "
                "limitation of time or condition. This includes the full bundle of rights: "
                "the right to develop (ingress and egress), the right to lease (executive right), "
                "the right to receive bonus, the right to receive delay rentals, the right to "
                "receive royalties, and the right to receive shut-in payments. In Texas, minerals "
                "are treated as real property and can be severed from the surface estate by "
                "express grant or reservation. Once severed, the mineral estate is dominant and "
                "carries with it the implied right to use so much of the surface as is reasonably "
                "necessary for mineral exploration and production. The fee simple absolute mineral "
                "owner may convey any or all of these rights separately, creating a fragmented "
                "ownership structure that requires careful tracking."
            ),
            legal_citations=[
                "Stephens County v. Mid-Kansas Oil & Gas Co., 113 Tex. 160 (1923)",
                "Tex. Nat. Res. Code Ann. \u00a791.001 et seq.",
                "French v. Chevron U.S.A., Inc., 896 S.W.2d 795 (Tex. 1995)",
            ],
            key_principles=[
                "Fee simple absolute is the highest form of mineral ownership",
                "Minerals are real property in Texas, severable from surface",
                "Mineral estate is dominant over surface estate",
                "Full bundle of rights can be subdivided and separately conveyed",
                "No time limitation or defeasance condition",
            ],
            practical_notes=[
                "Verify chain of title back to sovereign to confirm fee simple",
                "Check for any prior reservations or exceptions in the chain",
                "Confirm no outstanding term interests or life estates",
                "Review all conveyances for fractional interest language",
            ],
            related_blocks=["LM04-OWN-002", "LM04-OWN-003", "LM04-EXEC-001"],
        ))

        self._register(DoctrineBlock(
            block_id="LM04-OWN-002",
            title="Severed Mineral Estate",
            category=DoctrineCategory.OWNERSHIP,
            authority=DoctrineAuthority.CASE_LAW_SUPREME,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "When the mineral estate is severed from the surface estate, it becomes "
                "a separate estate in land. Severance can occur by express grant of minerals "
                "to another party, or by reservation of minerals when the surface is conveyed. "
                "Once severed, the two estates are independently alienable and inheritable. "
                "The mineral estate owner retains the implied easement to use the surface for "
                "mineral operations, subject to the accommodation doctrine established in "
                "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971). The severed mineral "
                "estate includes all five constituent rights unless the severance instrument "
                "specifies otherwise. Critically, severance language must be examined carefully: "
                "'minerals' may or may not include all substances depending on the instrument's "
                "date and the Moser v. U.S. Steel analysis framework. After the Texas Supreme "
                "Court's decision in Texas v. TXO Production Corp., the definition of 'minerals' "
                "follows the ordinary-and-natural-meaning test for instruments executed after 1983."
            ),
            legal_citations=[
                "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)",
                "Moser v. U.S. Steel Corp., 676 S.W.2d 99 (Tex. 1984)",
                "Humphreys-Mexia Co. v. Gammon, 113 Tex. 247 (1924)",
                "Reed v. Wylie, 597 S.W.2d 743 (Tex. 1980)",
            ],
            key_principles=[
                "Severance creates two separate estates in land",
                "Either express grant or reservation effects severance",
                "Implied easement for surface use accompanies mineral estate",
                "Definition of 'minerals' depends on instrument date and language",
                "Accommodation doctrine limits surface use rights",
            ],
            practical_notes=[
                "Identify the severance instrument and date precisely",
                "Analyze whether 'minerals' includes all hydrocarbons per Moser framework",
                "Check for surface use restrictions or limitations in the severance deed",
                "Track both mineral and surface chains separately after severance",
            ],
            related_blocks=["LM04-OWN-001", "LM04-SURF-001", "LM04-SURF-002"],
        ))

        self._register(DoctrineBlock(
            block_id="LM04-OWN-003",
            title="Undivided Mineral Interest",
            category=DoctrineCategory.OWNERSHIP,
            authority=DoctrineAuthority.CASE_LAW_SUPREME,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "An undivided mineral interest is a fractional ownership in the entire mineral "
                "estate of a tract, not a specific portion of the land. Each co-owner of an "
                "undivided mineral interest holds a proportionate share in every molecule of "
                "mineral beneath the entire tract. This is the standard form of concurrent "
                "mineral ownership. An owner of an undivided 1/4 mineral interest does not own "
                "the minerals beneath 1/4 of the land; rather, they own 1/4 of the minerals "
                "beneath all of the land. This distinction is critical for pooling, leasing, "
                "and royalty calculations. Each co-owner has the right to develop independently "
                "(subject to accounting obligations to other co-owners), and each co-owner may "
                "independently lease their undivided interest. The rule in Texas is that one "
                "co-tenant may develop without the consent of other co-tenants but must account "
                "for their proportionate share of production."
            ),
            legal_citations=[
                "Cox v. Davison, 397 S.W.2d 200 (Tex. 1965)",
                "Burnham v. Hardy Oil Co., 108 S.W. 960 (Tex. Civ. App. 1908)",
                "Japhet v. McRae, 276 S.W. 669 (Tex. Comm'n App. 1925)",
            ],
            key_principles=[
                "Undivided interest = proportionate share of whole, not a geographic portion",
                "Co-tenants may develop independently with accounting duty",
                "Each co-owner may independently lease their share",
                "Fractional interests are in the whole mineral estate, not a sub-tract",
                "Co-tenant's share of production must be accounted for",
            ],
            practical_notes=[
                "Always express mineral interests as undivided fractions unless partition occurred",
                "Track each co-owner's fractional share through all conveyances",
                "Verify denominator consistency across the chain of title",
                "Check for partition actions that may have divided the mineral estate",
            ],
            related_blocks=["LM04-OWN-001", "LM04-FRAC-001", "LM04-PART-001"],
        ))

        self._register(DoctrineBlock(
            block_id="LM04-OWN-004",
            title="Community Property and Mineral Interests",
            category=DoctrineCategory.OWNERSHIP,
            authority=DoctrineAuthority.STATUTORY,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "Texas is a community property state. Minerals acquired during marriage are "
                "presumed community property unless proven separate. Separate property minerals "
                "are those owned before marriage, acquired by gift, devise, or descent during "
                "marriage, or acquired with separate property funds with clear tracing. Income "
                "from separate property minerals (royalties, bonuses, delay rentals) is community "
                "property. Both spouses must join in conveying community property minerals. A "
                "conveyance by one spouse alone of community minerals is voidable at the election "
                "of the non-joining spouse. Upon death of a spouse, the surviving spouse retains "
                "their 1/2 community interest, and the decedent's 1/2 passes under their will "
                "or intestacy. Upon divorce, the court divides community property (including "
                "minerals) in a just and right manner, which is not always equal. Mineral "
                "interests acquired by either spouse during marriage using community funds are "
                "community property even if titled in only one spouse's name."
            ),
            legal_citations=[
                "Tex. Fam. Code Ann. \u00a73.002 (community property presumption)",
                "Tex. Fam. Code Ann. \u00a73.003 (separate property definition)",
                "Arnold v. Leonard, 114 Tex. 535 (1925)",
                "Hilley v. Hilley, 342 S.W.2d 565 (Tex. 1961)",
            ],
            key_principles=[
                "Minerals acquired during marriage are presumptively community property",
                "Both spouses must join in conveying community minerals",
                "Income from separate property minerals is community property",
                "Tracing required to prove separate property character",
                "Divorce courts divide community minerals just and right, not necessarily equal",
            ],
            practical_notes=[
                "Check marital status at time of each mineral acquisition",
                "Verify both spouses signed mineral conveyances during marriage",
                "Review divorce decrees for mineral property division language",
                "Trace funds used to acquire minerals to determine community vs separate",
            ],
            related_blocks=["LM04-OWN-001", "LM04-PROB-001", "LM04-CONV-001"],
        ))

        self._register(DoctrineBlock(
            block_id="LM04-OWN-005",
            title="Rule Against Perpetuities and Mineral Interests",
            category=DoctrineCategory.OWNERSHIP,
            authority=DoctrineAuthority.STATUTORY,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "The Rule Against Perpetuities (RAP) limits future interests in mineral estates. "
                "Under Texas law (Tex. Prop. Code \u00a7112.036), a nonvested property interest is "
                "invalid unless it must vest, if at all, within 21 years after some life in being "
                "at the creation of the interest. Texas adopted the Uniform Statutory Rule Against "
                "Perpetuities in 1991, providing a 300-year alternative vesting period for interests "
                "created after September 1, 1991. For mineral interests, RAP commonly applies to "
                "options to purchase mineral interests, executory interests following fee simple "
                "determinable mineral grants, and contingent remainder interests in mineral estates. "
                "Importantly, RAP does not apply to: (1) possibilities of reverter and rights of "
                "entry (reentry) following determinable or conditional mineral grants, (2) vested "
                "remainder interests, or (3) interests created by the exercise of a presently "
                "exercisable general power of appointment. The Texas Supreme Court in Peveto v. "
                "Starkey confirmed that RAP applies to executive rights if they are contingent."
            ),
            legal_citations=[
                "Tex. Prop. Code Ann. \u00a7112.036",
                "Peveto v. Starkey, 645 S.W.2d 770 (Tex. 1982)",
                "Hamman v. Ritchey, 598 S.W.2d 879 (Tex. Civ. App. 1980)",
                "Tex. Prop. Code Ann. \u00a75.043 (USRAP)",
            ],
            key_principles=[
                "RAP limits nonvested future interests in mineral estates",
                "300-year alternative period for interests created after Sept 1 1991",
                "Possibilities of reverter and rights of entry are exempt from RAP",
                "Contingent executive rights may be subject to RAP",
                "Vested remainder interests are not subject to RAP",
            ],
            practical_notes=[
                "Identify all future interests in mineral conveyances and test against RAP",
                "Check instrument date to determine whether USRAP 300-year period applies",
                "Distinguish vested vs contingent interests for RAP analysis",
                "Flag any contingent executive right grants for RAP review",
            ],
            related_blocks=["LM04-TEMP-001", "LM04-TEMP-002", "LM04-FSD-001"],
        ))

    # === MINERAL/ROYALTY DISTINCTION ===================================

    def _load_mineral_royalty_distinction(self) -> None:
        self._register(DoctrineBlock(
            block_id="LM04-MRD-001",
            title="Mineral Interest vs Royalty Interest - The Fundamental Distinction",
            category=DoctrineCategory.INTEREST_TYPES,
            authority=DoctrineAuthority.CASE_LAW_SUPREME,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "The distinction between a mineral interest and a royalty interest is the most "
                "fundamental classification in Texas mineral law. A mineral interest carries the "
                "full bundle of rights: (1) the right to develop, (2) the executive right to "
                "lease, (3) the right to receive bonus, (4) the right to receive delay rentals, "
                "and (5) the right to receive royalties. A royalty interest, by contrast, is only "
                "the right to receive a share of production (or proceeds) free of production costs. "
                "The Texas Supreme Court established the definitive test in Altman v. Blake: "
                "'the fundamental distinction between a royalty interest and a mineral interest "
                "is that a mineral interest carries with it executive rights, while a royalty "
                "interest does not.' This distinction has enormous practical consequences: a "
                "mineral interest owner can execute leases, receive bonus payments, and negotiate "
                "lease terms, while a royalty interest owner can only receive their share of "
                "production. A mineral deed conveys a mineral interest; a royalty deed conveys "
                "only a royalty interest. The language of the instrument controls, but Texas "
                "courts apply the four-corners rule and the harmonization principle from Luckel "
                "v. White to determine intent."
            ),
            legal_citations=[
                "Altman v. Blake, 712 S.W.2d 117 (Tex. 1986)",
                "French v. Chevron U.S.A., Inc., 896 S.W.2d 795 (Tex. 1995)",
                "Luckel v. White, 819 S.W.2d 459 (Tex. 1991)",
                "Temple-Inland, Inc. v. Henderson Family Partnership, Ltd., 958 S.W.2d 183 (Tex. App. 1997)",
            ],
            key_principles=[
                "Mineral interest = full bundle of rights including executive rights",
                "Royalty interest = right to share of production only, no executive rights",
                "Language of the instrument controls classification",
                "Four-corners rule and harmonization principle apply",
                "Mineral deed vs royalty deed distinction is critical",
            ],
            practical_notes=[
                "Read every conveyance instrument carefully for mineral vs royalty language",
                "The word 'royalty' in a deed does not automatically make it a royalty deed",
                "Check for granting vs reserving clause language differences",
                "Apply the Altman v. Blake test to ambiguous instruments",
            ],
            related_blocks=["LM04-MRD-002", "LM04-EXEC-001", "LM04-INT-001"],
        ))

        self._register(DoctrineBlock(
            block_id="LM04-MRD-002",
            title="The Two-Grant Doctrine and Double Fraction Problem",
            category=DoctrineCategory.INTEREST_TYPES,
            authority=DoctrineAuthority.CASE_LAW_SUPREME,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "The two-grant doctrine (or estate-misconception doctrine) arises when a "
                "conveyance uses fractional language that could describe either a mineral interest "
                "or a royalty interest, resulting in two different quantities depending on "
                "classification. For example, 'an undivided one-half (1/2) of the royalties' "
                "could mean: (A) 1/2 of the lessor's royalty (e.g., 1/2 of 1/8 = 1/16 of "
                "production), or (B) 1/2 of total production as a royalty. The Texas Supreme "
                "Court in Hysaw v. Dawkins adopted the 'estate/royalty' distinction: if the "
                "grant is of a fraction of 'royalty,' it is a fraction of the landowner's royalty "
                "under existing leases. If the grant is of a fraction of 'minerals' or uses "
                "language suggesting a mineral fee, the grantee receives a mineral interest "
                "that entitles them to the stated fraction of all production regardless of "
                "lease terms. The double fraction problem is especially acute when the original "
                "lease royalty changes (e.g., from 1/8 to 1/4): a 1/2 royalty interest under "
                "a 1/8 royalty lease is 1/16, but under a 1/4 royalty lease becomes 1/8. "
                "A 1/2 mineral interest always yields 1/2 of production."
            ),
            legal_citations=[
                "Hysaw v. Dawkins, 483 S.W.3d 1 (Tex. 2016)",
                "Garrett v. Dils Co., 157 Tex. 92, 299 S.W.2d 904 (1957)",
                "Watkins v. Slaughter, 144 Tex. 179, 189 S.W.2d 481 (1945)",
                "Jupiter Oil Co. v. Snow, 819 S.W.2d 466 (Tex. 1991)",
            ],
            key_principles=[
                "Two-grant doctrine applies to ambiguous fractional mineral/royalty language",
                "Fraction of 'royalty' = fraction of landowner's royalty under the lease",
                "Fraction of 'minerals' = fraction of all production regardless of lease",
                "Double fraction problem arises when lease royalty rate changes",
                "Instrument language and four-corners analysis control interpretation",
            ],
            practical_notes=[
                "When fractional language is ambiguous, apply Hysaw analysis",
                "Track the lease royalty rate applicable at time of each conveyance",
                "Calculate both possible interpretations and flag for review",
                "Document the basis for choosing mineral vs royalty interpretation",
            ],
            related_blocks=["LM04-MRD-001", "LM04-FRAC-001", "LM04-FRAC-002"],
        ))

        self._register(DoctrineBlock(
            block_id="LM04-MRD-003",
            title="Fixed Royalty vs Floating Royalty",
            category=DoctrineCategory.INTEREST_TYPES,
            authority=DoctrineAuthority.CASE_LAW_SUPREME,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "A fixed royalty is a specific fraction of production that does not change "
                "regardless of the lease royalty rate: for example, a grant of '1/16 of all "
                "oil and gas produced.' A floating royalty is a fraction of the lessor's "
                "royalty that changes as the lease royalty rate changes: for example, '1/2 of "
                "whatever royalty is provided in any lease.' Under a fixed royalty, if the lease "
                "provides a 1/4 royalty, the fixed 1/16 royalty holder still receives 1/16, not "
                "1/8. Under a floating royalty, the holder would receive 1/2 of 1/4 = 1/8. "
                "The distinction matters enormously for net mineral acre calculations and "
                "division order preparation. Texas courts look at the entirety of the instrument "
                "to determine whether the royalty was intended to be fixed or floating. Key "
                "language indicators: 'a 1/16 royalty' (fixed) vs 'a 1/2 interest in and to "
                "all royalties' (floating). The Garrett v. Dils line of cases provides the "
                "primary analytical framework."
            ),
            legal_citations=[
                "Garrett v. Dils Co., 157 Tex. 92 (1957)",
                "Pich v. Lankford, 302 S.W.2d 645 (Tex. 1957)",
                "Graham v. Prochaska, 429 S.W.2d 508 (Tex. Civ. App. 1968)",
            ],
            key_principles=[
                "Fixed royalty = specific fraction of production, unaffected by lease terms",
                "Floating royalty = fraction of lessor's royalty, changes with lease terms",
                "Language of the instrument determines fixed vs floating",
                "Distinction critical for NMA calculations and division orders",
                "Garrett v. Dils framework applies to ambiguous instruments",
            ],
            practical_notes=[
                "Classify every royalty interest as fixed or floating in the tracker",
                "Model NMA calculations under both current and potential future lease rates",
                "Flag instruments with ambiguous fixed/floating language for attorney review",
                "Record the basis for classification in the interest record",
            ],
            related_blocks=["LM04-MRD-001", "LM04-MRD-002", "LM04-FRAC-001"],
        ))

    # === EXECUTIVE RIGHTS ==============================================

    def _load_executive_rights_doctrines(self) -> None:
        self._register(DoctrineBlock(
            block_id="LM04-EXEC-001",
            title="Executive Rights Doctrine",
            category=DoctrineCategory.EXECUTIVE_RIGHTS,
            authority=DoctrineAuthority.CASE_LAW_SUPREME,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "The executive right is the right to execute oil and gas leases on the mineral "
                "estate. It is one of the five constituent rights of the mineral estate and may "
                "be severed and held separately. When executive rights are separated from the "
                "other mineral rights, the executive right holder owes a fiduciary-like duty "
                "to the non-executive mineral interest holders. This duty, established in "
                "Manges v. Guerra, requires the executive to exercise the right with due regard "
                "for the interests of the non-executive owners. The executive may not engage "
                "in self-dealing or obtain lease terms that unfairly benefit themselves at the "
                "expense of non-executive owners. However, the duty is not a full fiduciary "
                "duty; the Texas Supreme Court in Lesley v. Veterans Land Board clarified that "
                "the standard is 'utmost fair dealing' rather than strict fiduciary obligation. "
                "The executive must make reasonable efforts to lease on fair terms and must not "
                "unreasonably refuse to lease. An executive who refuses to lease when it would "
                "be economically beneficial to non-executives may breach this duty."
            ),
            legal_citations=[
                "Manges v. Guerra, 673 S.W.2d 180 (Tex. 1984)",
                "Lesley v. Veterans Land Board, 352 S.W.3d 479 (Tex. 2011)",
                "Hlavinka v. Hancock, 116 S.W.3d 412 (Tex. App. 2003)",
                "KCM Financial LLC v. Bradshaw, 457 S.W.3d 70 (Tex. 2015)",
            ],
            key_principles=[
                "Executive right can be severed from other mineral rights",
                "Executive owes duty of utmost fair dealing to non-executives",
                "Not a full fiduciary duty but more than arm's length dealing",
                "Executive may not self-deal or obtain unfairly favorable terms",
                "Unreasonable refusal to lease may breach executive duty",
            ],
            practical_notes=[
                "Track executive right ownership separately from other mineral rights",
                "Identify any separation of executive rights in the chain of title",
                "Note when NPRI holders may have claims against executive right holders",
                "Review lease terms for potential self-dealing by executive",
            ],
            related_blocks=["LM04-MRD-001", "LM04-INT-003", "LM04-INT-004"],
        ))

        self._register(DoctrineBlock(
            block_id="LM04-EXEC-002",
            title="Separation of Executive Rights from Mineral Estate",
            category=DoctrineCategory.EXECUTIVE_RIGHTS,
            authority=DoctrineAuthority.CASE_LAW_SUPREME,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "Executive rights may be separated from the mineral estate through several "
                "mechanisms: (1) express reservation in a mineral deed, (2) grant of executive "
                "rights alone, (3) creation of a non-participating royalty interest (which by "
                "definition excludes executive rights), or (4) creation of a non-executive "
                "mineral interest. When mineral interests are conveyed 'without executive rights,' "
                "the grantor retains the executive right. The separation creates significant "
                "practical issues: the executive right holder controls leasing but may have "
                "little or no financial interest in production. This creates potential conflicts "
                "of interest, especially when the executive holder leases to themselves or to "
                "entities in which they have an interest. Texas courts have imposed the duty "
                "of utmost fair dealing precisely because of this inherent conflict. For "
                "tracking purposes, executive rights must be treated as a separate trackable "
                "interest that can be held by a different party than the royalty or mineral "
                "interest holder."
            ),
            legal_citations=[
                "Day & Co. v. Texland Petroleum, Inc., 786 S.W.2d 667 (Tex. 1990)",
                "Manges v. Guerra, 673 S.W.2d 180 (Tex. 1984)",
                "In re Bass, 113 S.W.3d 735 (Tex. 2003)",
            ],
            key_principles=[
                "Executive rights can be held separately from mineral interest",
                "Multiple mechanisms for separation exist",
                "Separation creates inherent conflict-of-interest potential",
                "Must track executive rights as separate interest line",
                "Duty of utmost fair dealing applies when separated",
            ],
            practical_notes=[
                "Create separate ownership line for executive rights in tracker",
                "Link executive right holder to the mineral/royalty interests they control",
                "Flag any leases executed by the executive for conflict review",
                "Track bonus and delay rental allocation when executive rights are separated",
            ],
            related_blocks=["LM04-EXEC-001", "LM04-INT-003", "LM04-OWN-001"],
        ))

    # === INTEREST TYPE DOCTRINES =======================================

    def _load_interest_type_doctrines(self) -> None:
        self._register(DoctrineBlock(
            block_id="LM04-INT-001",
            title="Working Interest (WI)",
            category=DoctrineCategory.INTEREST_TYPES,
            authority=DoctrineAuthority.INDUSTRY_STANDARD,
            jurisdiction=Jurisdiction.MULTI_STATE,
            content=(
                "A working interest (WI) is the operating interest in an oil and gas lease that "
                "bears the costs of exploration, development, and production. The WI owner has "
                "the right to drill, produce, and market oil and gas from the leased premises. "
                "The WI is created by the oil and gas lease: the lessee receives a working "
                "interest in exchange for the obligations to develop, pay royalties, and comply "
                "with lease terms. The WI bears 100% of costs and receives 100% of revenue, "
                "less burdens (royalty, ORRI, etc.). The net revenue interest (NRI) to the WI "
                "owner equals the WI minus all burdens. For example, if a lessee holds 100% WI "
                "and the lease has a 1/4 royalty plus a 5% ORRI, the lessee's NRI is 100% - 25% "
                "- 5% = 70%. WI can be assigned in whole or in part. WI terminates when the "
                "lease terminates. WI owners are jointly and severally liable for surface damage "
                "and other lease obligations. The WI is the only interest type that bears costs."
            ),
            legal_citations=[
                "Williams & Meyers, Oil and Gas Law \u00a7503",
                "8 Tex. Jur. 3d, Oil and Gas \u00a7\u00a7180-195",
            ],
            key_principles=[
                "Working interest bears costs and receives revenue less burdens",
                "Created by oil and gas lease, terminates with lease",
                "NRI = WI minus all burdens",
                "Only interest type that bears costs of development",
                "Assignable in whole or in part",
            ],
            practical_notes=[
                "Always track WI as lease-dependent interest",
                "Calculate NRI by subtracting all burdens from WI",
                "Track WI assignments and partial assignments through the lease term",
                "Note that WI terminates on lease expiration or release",
            ],
            related_blocks=["LM04-INT-002", "LM04-INT-005", "LM04-LEASE-001"],
        ))

        self._register(DoctrineBlock(
            block_id="LM04-INT-002",
            title="Overriding Royalty Interest (ORRI)",
            category=DoctrineCategory.INTEREST_TYPES,
            authority=DoctrineAuthority.CASE_LAW_APPELLATE,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "An overriding royalty interest (ORRI) is a non-possessory interest carved from "
                "the working interest that entitles the holder to a share of production free of "
                "costs. Unlike a landowner's royalty, an ORRI is created by the lease or by "
                "assignment from the working interest holder and terminates when the underlying "
                "lease terminates. ORRIs are commonly used to compensate landmen, geologists, "
                "brokers, and other industry participants. The ORRI does not carry executive "
                "rights, does not participate in bonus or delay rentals, and has no obligation "
                "to develop. ORRIs are burdens on the working interest and reduce the WI holder's "
                "NRI. ORRIs may be retained on assignment of the lease (carved-out ORRI) or "
                "granted separately. Multiple ORRIs may burden the same lease. The total of all "
                "burdens (royalty + all ORRIs) cannot exceed the working interest; if they do, "
                "this creates a 'washout' situation where the WI holder has no economic incentive "
                "to produce."
            ),
            legal_citations=[
                "In re Haut, 76 B.R. 379 (Bankr. W.D. Tex. 1987)",
                "Pich v. Lankford, 302 S.W.2d 645 (Tex. 1957)",
                "Williams & Meyers, Oil and Gas Law \u00a7418",
            ],
            key_principles=[
                "ORRI carved from working interest, terminates with lease",
                "No cost bearing, no executive rights, no bonus/rental participation",
                "Burden on WI reduces lessee NRI",
                "Multiple ORRIs may burden same lease",
                "Washout occurs if total burdens exceed WI",
            ],
            practical_notes=[
                "Track ORRI as lease-dependent, separate from mineral/royalty interests",
                "Sum all ORRIs with royalty to compute total burden on WI",
                "Flag washout situations where burdens exceed practical WI threshold",
                "Verify ORRI holder has no cost-bearing obligation",
            ],
            related_blocks=["LM04-INT-001", "LM04-INT-003", "LM04-FRAC-003"],
        ))

        self._register(DoctrineBlock(
            block_id="LM04-INT-003",
            title="Non-Participating Royalty Interest (NPRI)",
            category=DoctrineCategory.INTEREST_TYPES,
            authority=DoctrineAuthority.CASE_LAW_SUPREME,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "A non-participating royalty interest (NPRI) is a share of production (or its "
                "value) free of costs, carved from the mineral estate, that does not carry "
                "executive rights and does not participate in bonus payments or delay rentals. "
                "Unlike an ORRI, an NPRI survives lease termination because it is carved from "
                "the mineral fee, not from the working interest. The NPRI holder has no right "
                "to lease, no right to bonus, no right to delay rental, and no right to "
                "participate in pooling decisions. However, the NPRI holder does receive their "
                "share of production (royalties) from any lease executed by the executive right "
                "holder. The NPRI is calculated as a fraction of the mineral estate, not a "
                "fraction of the lease royalty, unless the instrument specifies otherwise. "
                "Under the French v. Chevron analysis, an NPRI of '1/16 of production' means "
                "the holder receives 1/16 of all oil and gas produced, regardless of the lease "
                "royalty rate. This makes NPRIs fixed interests unless the creating instrument "
                "specifies a floating fraction."
            ),
            legal_citations=[
                "French v. Chevron U.S.A., Inc., 896 S.W.2d 795 (Tex. 1995)",
                "Nortex Mineral Co. v. R.A. Scott Pet. Corp., 803 S.W.2d 474 (Tex. App. 1991)",
                "Altman v. Blake, 712 S.W.2d 117 (Tex. 1986)",
                "Bagby v. Bredthauer, 627 S.W.2d 190 (Tex. App. 1981)",
            ],
            key_principles=[
                "NPRI carved from mineral fee, survives lease termination",
                "No executive rights, no bonus, no delay rental participation",
                "Typically fixed fraction of production unless instrument says otherwise",
                "Not lease-dependent unlike ORRI",
                "Executive right holder owes duty to NPRI holder",
            ],
            practical_notes=[
                "Track NPRI separately from ORRI and mineral interest",
                "Determine if NPRI is fixed or floating per instrument language",
                "Calculate NPRI burden on the mineral interest, not the lease",
                "NPRI reduces the mineral interest holder's effective royalty",
            ],
            related_blocks=["LM04-INT-002", "LM04-EXEC-001", "LM04-MRD-001"],
        ))

        self._register(DoctrineBlock(
            block_id="LM04-INT-004",
            title="Non-Executive Mineral Interest (NEMI)",
            category=DoctrineCategory.INTEREST_TYPES,
            authority=DoctrineAuthority.CASE_LAW_SUPREME,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "A non-executive mineral interest (NEMI) is a mineral interest from which the "
                "executive right has been severed. The NEMI holder retains all rights of a "
                "mineral interest owner except the right to execute leases. They are entitled "
                "to bonus, delay rentals, and royalties from any lease executed by the holder "
                "of the executive right. This distinguishes a NEMI from an NPRI: the NPRI "
                "holder receives only royalties, while the NEMI holder receives bonus, delay "
                "rentals, and royalties. The executive right holder owes the same duty of "
                "utmost fair dealing to NEMI holders as to NPRI holders. A NEMI is created "
                "when minerals are conveyed with a reservation of executive rights, or when "
                "executive rights are separately granted to a third party. The NEMI is a "
                "mineral fee interest and survives lease termination."
            ),
            legal_citations=[
                "Day & Co. v. Texland Petroleum, Inc., 786 S.W.2d 667 (Tex. 1990)",
                "Lesley v. Veterans Land Board, 352 S.W.3d 479 (Tex. 2011)",
                "Hlavinka v. Hancock, 116 S.W.3d 412 (Tex. App. 2003)",
            ],
            key_principles=[
                "NEMI = mineral interest minus executive rights",
                "NEMI holder receives bonus, delay rental, AND royalty",
                "Distinguishable from NPRI which receives only royalty",
                "Executive right holder owes duty of utmost fair dealing",
                "Survives lease termination as mineral fee interest",
            ],
            practical_notes=[
                "Distinguish NEMI from NPRI by checking bonus/rental entitlement",
                "Track executive right separation as separate interest line",
                "Allocate bonus and delay rentals to NEMI holders proportionally",
                "NEMI computation differs from NPRI in NMA calculations",
            ],
            related_blocks=["LM04-INT-003", "LM04-EXEC-001", "LM04-EXEC-002"],
        ))

        self._register(DoctrineBlock(
            block_id="LM04-INT-005",
            title="Net Revenue Interest (NRI) Calculation",
            category=DoctrineCategory.INTEREST_TYPES,
            authority=DoctrineAuthority.INDUSTRY_STANDARD,
            jurisdiction=Jurisdiction.MULTI_STATE,
            content=(
                "Net Revenue Interest (NRI) is the share of production revenue an interest "
                "holder actually receives after deducting all burdens. For a working interest "
                "holder: NRI = WI - royalty burden - ORRI burden - any other production payment "
                "burdens. For a mineral interest holder who has leased: the NRI under the lease "
                "equals the mineral interest fraction multiplied by the lease royalty rate, "
                "minus any outstanding NPRIs or other burdens on the mineral interest. "
                "NRI is always expressed as a decimal fraction of total production. Example: "
                "Owner has 1/2 mineral interest, leases at 1/4 royalty. NRI = 0.5 * 0.25 = "
                "0.125 (12.5% of production). If there is a 1/16 NPRI outstanding, the mineral "
                "owner's NRI is reduced: (0.5 * 0.25) - 0.0625 = 0.0625 (6.25%). The NPRI "
                "holder's NRI is 0.0625 (6.25%). Total royalty burden: 12.5%. NRI calculations "
                "are the foundation of division order preparation and revenue distribution."
            ),
            legal_citations=[
                "Williams & Meyers, Oil and Gas Law \u00a7\u00a7503, 504",
                "3 Kuntz, Law of Oil and Gas \u00a739.3",
            ],
            key_principles=[
                "NRI = share of production actually received by interest holder",
                "WI NRI = WI minus all burdens (royalty + ORRI + production payments)",
                "Mineral owner NRI = mineral fraction x lease royalty - NPRI burdens",
                "NRI expressed as decimal fraction of total production",
                "Foundation for division order preparation",
            ],
            practical_notes=[
                "Calculate NRI for every interest holder in the tract",
                "Verify all NRIs sum to 1.0 (100% of production accounted for)",
                "Separate pre-lease and post-lease NRI calculations",
                "Track NRI changes when lease royalty rate changes",
            ],
            related_blocks=["LM04-INT-001", "LM04-INT-002", "LM04-INT-003", "LM04-FRAC-001"],
        ))

    # === TEMPORAL INTERESTS ============================================

    def _load_temporal_interest_doctrines(self) -> None:
        self._register(DoctrineBlock(
            block_id="LM04-TEMP-001",
            title="Term Mineral Interest",
            category=DoctrineCategory.TEMPORAL,
            authority=DoctrineAuthority.CASE_LAW_SUPREME,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "A term mineral interest is a mineral interest limited to a specific duration "
                "of time, after which it reverts to the grantor or their successors. Common "
                "forms include: (1) fixed term ('for a period of 20 years'), (2) term plus "
                "production ('for 20 years and so long thereafter as oil or gas is produced'), "
                "and (3) defeasible term ('for 20 years, provided that...'). The Texas Supreme "
                "Court in Hamman v. Ritchey established that a term mineral interest is a "
                "determinable fee that automatically reverts upon expiration of the term. The "
                "holder of the possibility of reverter (the grantor) does not need to take any "
                "action to reclaim the minerals; reverter is automatic. Term mineral interests "
                "must be carefully tracked because they create a future interest (the possibility "
                "of reverter) that vests automatically. The commencement date, duration, and "
                "any saving clauses must be precisely identified and calendared."
            ),
            legal_citations=[
                "Hamman v. Ritchey, 598 S.W.2d 879 (Tex. Civ. App. 1980)",
                "Bagby v. Bredthauer, 627 S.W.2d 190 (Tex. App. 1981)",
                "Jupiter Oil Co. v. Snow, 819 S.W.2d 466 (Tex. 1991)",
            ],
            key_principles=[
                "Term mineral interest limited by time, reverts automatically on expiration",
                "Three forms: fixed term, term plus production, defeasible term",
                "Possibility of reverter is automatic, no action needed",
                "Must track commencement date, duration, and saving clauses",
                "Term plus production saves the interest if production exists at term end",
            ],
            practical_notes=[
                "Calendar all term expirations for proactive monitoring",
                "Check for production saving clauses before declaring term expired",
                "Track the holder of the possibility of reverter",
                "Verify whether any lease activity saves the term interest",
            ],
            related_blocks=["LM04-TEMP-002", "LM04-OWN-005", "LM04-FSD-001"],
        ))

        self._register(DoctrineBlock(
            block_id="LM04-TEMP-002",
            title="Life Estate Mineral Interest",
            category=DoctrineCategory.TEMPORAL,
            authority=DoctrineAuthority.CASE_LAW_SUPREME,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "A life estate in minerals grants the holder mineral rights for the duration "
                "of a specified person's life (the measuring life). Upon the death of the "
                "measuring life, the minerals pass to the remainderman. The life tenant has the "
                "right to use and enjoy the minerals during their lifetime, including the right "
                "to lease and receive bonus, delay rentals, and royalties. However, the life "
                "tenant must not commit waste: they may not deplete the minerals beyond what "
                "a reasonably prudent operator would extract. Under the open mine doctrine "
                "recognized in Texas, if mineral development was occurring at the time the "
                "life estate was created, the life tenant may continue development of existing "
                "wells but generally may not open new wells on unleased portions without the "
                "remainderman's consent. The life tenant's right to lease may be limited by "
                "the remainder interest. A lease granted by the life tenant alone generally "
                "terminates upon the death of the measuring life unless the remainderman "
                "ratifies or the lease contains savings language."
            ),
            legal_citations=[
                "Evans v. Templeton, 69 S.W.2d 1098 (Tex. 1934)",
                "Williams & Meyers, Oil and Gas Law \u00a7\u00a7326-329",
                "3 Kuntz, Law of Oil and Gas \u00a730.3",
            ],
            key_principles=[
                "Life estate limited to measuring life duration",
                "Life tenant may lease and receive income during measuring life",
                "Open mine doctrine governs existing vs new development",
                "Life tenant must not commit waste",
                "Lease by life tenant alone terminates at measuring life's death",
            ],
            practical_notes=[
                "Track measuring life identity and vital status",
                "Calendar life estate for monitoring (death triggers remainder)",
                "Check if existing development saves the open mine doctrine",
                "Verify remainderman identity and track their interest separately",
            ],
            related_blocks=["LM04-TEMP-001", "LM04-PROB-001", "LM04-OWN-001"],
        ))

        self._register(DoctrineBlock(
            block_id="LM04-FSD-001",
            title="Fee Simple Determinable Minerals and Possibility of Reverter",
            category=DoctrineCategory.TEMPORAL,
            authority=DoctrineAuthority.CASE_LAW_SUPREME,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "A fee simple determinable mineral interest is an interest that automatically "
                "terminates upon the occurrence of a stated event. Unlike a fee simple subject "
                "to condition subsequent (which requires the grantor to exercise a right of "
                "reentry), a fee simple determinable ends automatically. The grantor retains "
                "a possibility of reverter, which is a future interest that becomes possessory "
                "automatically upon the occurrence of the determinable event. Common determinable "
                "events for mineral interests include: cessation of production, failure to develop "
                "within a specified period, change of use, or abandonment. The language creating "
                "a determinable fee typically uses words like 'so long as,' 'during,' 'while,' "
                "or 'until.' Language such as 'on condition that,' 'provided that,' or 'but if' "
                "typically creates a fee simple subject to condition subsequent with a right of "
                "reentry, which does not terminate automatically. The distinction is critical "
                "because the possibility of reverter is not subject to the Rule Against "
                "Perpetuities, while the right of reentry/power of termination in some "
                "jurisdictions may be."
            ),
            legal_citations=[
                "Tex. Prop. Code Ann. \u00a75.042",
                "Hamman v. Ritchey, 598 S.W.2d 879 (Tex. Civ. App. 1980)",
                "Williams & Meyers, Oil and Gas Law \u00a7320",
            ],
            key_principles=[
                "FSD terminates automatically on occurrence of stated event",
                "Grantor retains possibility of reverter (automatic)",
                "Distinguish from FSSCS which requires reentry action",
                "Key language: 'so long as' vs 'on condition that'",
                "Possibility of reverter exempt from Rule Against Perpetuities",
            ],
            practical_notes=[
                "Parse determinable language carefully in all mineral deeds",
                "Calendar determinable events for monitoring",
                "Track the possibility of reverter as a separate future interest",
                "Flag FSD minerals in conflict reports as potentially reverting",
            ],
            related_blocks=["LM04-TEMP-001", "LM04-OWN-005", "LM04-CONF-001"],
        ))

    # === FRACTIONAL CALCULATIONS =======================================

    def _load_fractional_calculation_doctrines(self) -> None:
        self._register(DoctrineBlock(
            block_id="LM04-FRAC-001",
            title="Net Mineral Acre (NMA) Calculation",
            category=DoctrineCategory.FRACTIONAL,
            authority=DoctrineAuthority.INDUSTRY_STANDARD,
            jurisdiction=Jurisdiction.MULTI_STATE,
            content=(
                "Net Mineral Acres (NMA) is the standard unit of measure for mineral ownership. "
                "NMA = gross acres x mineral interest fraction. For example, a 1/4 mineral "
                "interest in a 640-acre section = 160 NMA. NMA calculations must account for: "
                "(1) the original survey acreage, (2) all fractional conveyances in the chain, "
                "(3) any fractional interests created by probate/heirship, (4) any pooling "
                "effects on the interest, and (5) any outstanding burdens (NPRI, ORRI). "
                "NMA is calculated at the mineral interest level, not the royalty level. "
                "To compute royalty NMA (the NMA equivalent for royalty purposes), multiply "
                "NMA x lease royalty rate. The industry standard for NMA calculation follows "
                "a multiplicative chain: if A owns 1/2 minerals, conveys 1/4 of her interest "
                "to B, B owns 1/8 NMA (assuming 1 NMA total). Each successive conveyance "
                "fractions off the grantor's remaining interest. Careful tracking of the "
                "denominator at each step is essential to avoid compounding errors."
            ),
            legal_citations=[
                "Williams & Meyers, Oil and Gas Law \u00a7502",
                "AAPL Form 610 (Division Order)",
            ],
            key_principles=[
                "NMA = gross acres x mineral interest fraction",
                "Multiplicative chain through all conveyances",
                "Must track denominator at each conveyance step",
                "Distinguish mineral NMA from royalty NMA",
                "Account for probate, heirship, and pooling effects",
            ],
            practical_notes=[
                "Always start NMA calculation from the original patent/survey acreage",
                "Build the fractional chain step by step through each conveyance",
                "Verify that all mineral interests in a tract sum to total NMA",
                "Flag any tract where interests sum to more or less than total NMA",
            ],
            related_blocks=["LM04-FRAC-002", "LM04-FRAC-003", "LM04-INT-005"],
        ))

        self._register(DoctrineBlock(
            block_id="LM04-FRAC-002",
            title="Fractional Interest Chain Computation",
            category=DoctrineCategory.FRACTIONAL,
            authority=DoctrineAuthority.PRACTICE_GUIDE,
            jurisdiction=Jurisdiction.MULTI_STATE,
            content=(
                "Computing fractional mineral interests through a chain of title requires "
                "precise arithmetic at each step. The fundamental rule is: each conveyance "
                "operates on the grantor's then-existing interest. If A owns 1/2 and conveys "
                "'an undivided 1/4 of my mineral interest,' B receives 1/2 x 1/4 = 1/8. "
                "If A then conveys 'an undivided 1/4 mineral interest,' ambiguity arises: "
                "does this mean 1/4 of A's remaining interest (1/4 x 3/8 = 3/32) or 1/4 of "
                "the whole mineral estate (1/4)? If A only owns 3/8, A cannot convey more than "
                "3/8 without the conveyance being partially ineffective. Texas follows the "
                "Duhig rule for warranty deeds: if the grantor warrants title but has previously "
                "reserved minerals, the warranty may estop the grantor from claiming the reserved "
                "minerals. The Duhig rule can alter fractional calculations by estopping a grantor "
                "from claiming a prior reservation. Each step must be documented with: (1) the "
                "grantor's interest before conveyance, (2) the fraction conveyed, (3) whether "
                "the fraction is of the grantor's interest or the whole estate, (4) the grantor's "
                "remaining interest after conveyance, and (5) the grantee's resulting interest."
            ),
            legal_citations=[
                "Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503 (1940)",
                "Benge v. Scharbauer, 152 Tex. 447 (1953)",
                "Harris v. Currie, 142 Tex. 93 (1944)",
            ],
            key_principles=[
                "Each conveyance operates on grantor's then-existing interest",
                "Ambiguity: fraction of grantor's interest vs fraction of whole estate",
                "Duhig rule may estop grantor from claiming prior reservation",
                "Cannot convey more than you own (partial ineffectiveness)",
                "Five elements must be documented at each chain step",
            ],
            practical_notes=[
                "Build chain step-by-step, never skip intermediate conveyances",
                "Check for Duhig rule applicability on every warranty deed",
                "Resolve 'of my interest' vs 'of the whole' ambiguity explicitly",
                "Carry forward the exact remaining fraction at each step",
            ],
            related_blocks=["LM04-FRAC-001", "LM04-CONV-001", "LM04-CONF-001"],
        ))

        self._register(DoctrineBlock(
            block_id="LM04-FRAC-003",
            title="Burden Stacking and Total Burden Computation",
            category=DoctrineCategory.FRACTIONAL,
            authority=DoctrineAuthority.PRACTICE_GUIDE,
            jurisdiction=Jurisdiction.MULTI_STATE,
            content=(
                "Burden stacking refers to the accumulation of non-cost-bearing interests "
                "(royalty, NPRI, ORRI) on a mineral tract. The total burden on a working interest "
                "is the sum of all royalty interests, NPRIs, and ORRIs. This total burden "
                "determines the working interest holder's net revenue interest (NRI). When "
                "burdens are stacked, there is a risk of overburdening: if the total burdens "
                "exceed the working interest, no rational operator would develop the tract "
                "(a 'washout'). Burden stacking calculations must account for: (1) the lease "
                "royalty rate, (2) all outstanding NPRIs as a fraction of production, (3) all "
                "outstanding ORRIs, (4) any production payment obligations, and (5) any carried "
                "interest arrangements. The total burden should never exceed 100% of production. "
                "If it does, there is an error in the chain or a conflict that must be resolved. "
                "In practice, many operators require a minimum NRI (commonly 75-80% for oil, "
                "80-85% for gas) before committing to development."
            ),
            legal_citations=[
                "Williams & Meyers, Oil and Gas Law \u00a7\u00a7424.1-424.3",
                "3 Kuntz, Law of Oil and Gas \u00a742.3",
            ],
            key_principles=[
                "Total burden = royalty + NPRI + ORRI + production payments",
                "WI NRI = 100% minus total burden",
                "Washout occurs when burdens exceed practical development threshold",
                "Burdens cannot exceed 100% of production",
                "Minimum NRI thresholds govern operator development decisions",
            ],
            practical_notes=[
                "Calculate total burden for every tract and flag if > 25%",
                "Detect washout conditions where NRI falls below operator minimums",
                "Layer burdens in order: lease royalty first, then NPRI, then ORRI",
                "Report total burden alongside NMA and NRI for each interest",
            ],
            related_blocks=["LM04-FRAC-001", "LM04-INT-001", "LM04-INT-002", "LM04-INT-005"],
        ))

    # === POOLING ======================================================

    def _load_pooling_doctrines(self) -> None:
        self._register(DoctrineBlock(
            block_id="LM04-POOL-001",
            title="Pooling Effects on Mineral Interests",
            category=DoctrineCategory.POOLING,
            authority=DoctrineAuthority.STATUTORY,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "Pooling combines two or more tracts or mineral interests into a single unit "
                "for drilling and production purposes. In Texas, pooling may be voluntary "
                "(by agreement of all interest owners), compulsory (by Railroad Commission "
                "order under Tex. Nat. Res. Code \u00a7102.011 et seq.), or pursuant to lease "
                "pooling clauses. When a tract is pooled, the mineral interest owner's share "
                "of production from the unit is proportional to their acreage contribution "
                "to the unit. NMA in a pooled unit is calculated as: NMA x (tract acres / "
                "total unit acres). For example, if an owner has 80 NMA in a 160-acre tract "
                "that is pooled into a 640-acre unit, their unit NMA = 80 x (160/640) = 20 "
                "NMA equivalent. Pooling affects NRI calculations because the interest is "
                "diluted by the ratio of tract acreage to total unit acreage. The pooling "
                "clause in the lease is critical: some clauses limit pooling to specific "
                "acreage maximums, some require consent, and some permit the lessee to pool "
                "at their sole discretion. Force pooling under Texas law requires a showing "
                "of waste prevention or fair and equitable treatment of all interest owners."
            ),
            legal_citations=[
                "Tex. Nat. Res. Code Ann. \u00a7102.011 et seq.",
                "Jones v. Killingsworth, 403 S.W.2d 325 (Tex. 1966)",
                "Railroad Commission of Texas Statewide Rule 37",
            ],
            key_principles=[
                "Pooling combines tracts into single production unit",
                "Proportional share based on acreage contribution to unit",
                "Unit NMA = tract NMA x (tract acres / unit acres)",
                "Three types: voluntary, compulsory, lease-clause",
                "Lease pooling clause terms control voluntary pooling scope",
            ],
            practical_notes=[
                "Track pooling declarations and unit designations for each tract",
                "Recalculate NMA and NRI after pooling using acreage ratio",
                "Review lease pooling clauses for maximum acreage and consent requirements",
                "Monitor Railroad Commission pooling orders affecting tracked tracts",
            ],
            related_blocks=["LM04-POOL-002", "LM04-FRAC-001", "LM04-LEASE-001"],
        ))

        self._register(DoctrineBlock(
            block_id="LM04-POOL-002",
            title="Pugh Clause and Anti-Pooling Protections",
            category=DoctrineCategory.POOLING,
            authority=DoctrineAuthority.CASE_LAW_APPELLATE,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "The Pugh clause (named after Lawrence G. Pugh) is a lease provision that "
                "severs the pooled portions of a lease from the unpooled portions, so that "
                "production from a pooled unit does not hold the entire lease beyond the "
                "primary term. Without a Pugh clause, production from any part of a pooled "
                "unit holds the entire lease in force. With a Pugh clause, only the pooled "
                "acreage is held by production from the unit; the remaining unpooled acreage "
                "must be independently maintained by production, drilling, or payment. There "
                "are two types: horizontal Pugh clauses (severing by depth) and vertical Pugh "
                "clauses (severing by areal extent). A depth severance clause releases all "
                "depths below the deepest producing formation. These clauses significantly "
                "affect mineral interest tracking because they create potentially different "
                "lease statuses for different portions of the same tract."
            ),
            legal_citations=[
                "Pugh v. Curecare, Inc., 158 F. Supp. 2d 659 (W.D. La. 2001)",
                "Williams & Meyers, Oil and Gas Law \u00a7669",
                "8 Tex. Jur. 3d, Oil and Gas \u00a7\u00a7270-275",
            ],
            key_principles=[
                "Pugh clause severs pooled from unpooled acreage for lease maintenance",
                "Without Pugh clause, unit production holds entire lease",
                "Horizontal Pugh severs by depth, vertical Pugh severs by area",
                "Depth severance releases formations below deepest producing zone",
                "Creates multiple lease statuses within same tract",
            ],
            practical_notes=[
                "Check every lease for Pugh clause presence and type",
                "Track pooled vs unpooled acreage separately after Pugh clause activation",
                "Monitor for partial lease expiration on unpooled portions",
                "Calculate NMA separately for pooled and unpooled portions",
            ],
            related_blocks=["LM04-POOL-001", "LM04-LEASE-001", "LM04-FRAC-001"],
        ))

    # === PROBATE =======================================================

    def _load_probate_doctrines(self) -> None:
        self._register(DoctrineBlock(
            block_id="LM04-PROB-001",
            title="Probate and Intestate Succession of Mineral Interests",
            category=DoctrineCategory.PROBATE,
            authority=DoctrineAuthority.STATUTORY,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "When a mineral interest owner dies, their mineral interests pass either by "
                "will (testate) or under the Texas Estates Code (intestate). Under intestate "
                "succession for separate property (including minerals acquired before marriage "
                "or by gift/inheritance), the distribution depends on survivors: if survived "
                "by spouse and children, the spouse receives 1/3 of personal property and a "
                "life estate in 1/3 of real property (including minerals), with the remainder "
                "to children. If survived by spouse only with no children, spouse receives all "
                "personal property and 1/2 of real property. For community property minerals: "
                "the surviving spouse already owns 1/2. The decedent's 1/2 passes: to children "
                "if any (equally, per stirpes), or to the surviving spouse if no children. "
                "Each probate event creates fractional interests that must be tracked. Heirship "
                "affidavits (Tex. Est. Code \u00a7203.001) are commonly used to establish mineral "
                "inheritance without full probate, but they are not conclusive evidence of "
                "heirship. A Determination of Heirship proceeding under Tex. Est. Code \u00a7202 "
                "provides stronger evidence."
            ),
            legal_citations=[
                "Tex. Est. Code Ann. \u00a7\u00a7201.001-201.003",
                "Tex. Est. Code Ann. \u00a7\u00a7202.001 et seq.",
                "Tex. Est. Code Ann. \u00a7\u00a7203.001 et seq.",
                "Tex. Prop. Code Ann. \u00a7\u00a72.101-2.103",
            ],
            key_principles=[
                "Minerals pass by will or intestate succession",
                "Community property: surviving spouse already owns 1/2",
                "Separate property succession depends on family survivors",
                "Each probate event fractions the mineral interest",
                "Heirship affidavits vs Determination of Heirship have different weight",
            ],
            practical_notes=[
                "Track death dates and probate proceedings for all mineral owners",
                "Apply correct intestacy rules based on date of death and family situation",
                "Calculate each heir's fractional interest after probate",
                "Distinguish community vs separate property minerals in probate analysis",
            ],
            related_blocks=["LM04-PROB-002", "LM04-OWN-004", "LM04-FRAC-002"],
        ))

        self._register(DoctrineBlock(
            block_id="LM04-PROB-002",
            title="Heirship Affidavit Practice and Weight",
            category=DoctrineCategory.PROBATE,
            authority=DoctrineAuthority.STATUTORY,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "An affidavit of heirship is a sworn statement recorded in the county deed "
                "records identifying the heirs of a deceased person. Under Tex. Est. Code "
                "\u00a7203.001, an affidavit of heirship may be filed in the deed records of any "
                "county where the decedent owned real property. The affidavit becomes prima "
                "facie evidence of the facts stated therein after being of record for five "
                "years. However, it is not conclusive and may be contradicted by other evidence. "
                "For mineral interest tracking, heirship affidavits are critical because many "
                "mineral interests pass by descent without formal probate. The affidavit must "
                "identify: the decedent, date and place of death, marital history, all children "
                "and their issue, and the nature and extent of the estate. Best practice requires "
                "corroboration with obituaries, family records, and other documentary evidence. "
                "A Determination of Heirship under \u00a7202 is a judicial proceeding that provides "
                "stronger and often conclusive evidence, but is more expensive and time-consuming."
            ),
            legal_citations=[
                "Tex. Est. Code Ann. \u00a7\u00a7203.001-203.002",
                "Tex. Est. Code Ann. \u00a7\u00a7202.001 et seq.",
                "Tex. Prop. Code Ann. \u00a75.013",
            ],
            key_principles=[
                "Heirship affidavit is prima facie evidence after 5 years of record",
                "Not conclusive - can be contradicted by other evidence",
                "Must identify decedent, heirs, marital history, and estate",
                "Judicial Determination of Heirship provides stronger evidence",
                "Many mineral interests pass by descent without formal probate",
            ],
            practical_notes=[
                "Accept heirship affidavits with caution, verify facts independently",
                "Check how long the affidavit has been of record (5-year threshold)",
                "Cross-reference affidavit facts with other title documents",
                "Flag interests relying solely on unrecorded heirship claims",
            ],
            related_blocks=["LM04-PROB-001", "LM04-CONV-001", "LM04-CONF-001"],
        ))

    # === CONVEYANCE ===================================================

    def _load_conveyance_doctrines(self) -> None:
        self._register(DoctrineBlock(
            block_id="LM04-CONV-001",
            title="Mineral Deed Construction and Interpretation",
            category=DoctrineCategory.CONVEYANCE,
            authority=DoctrineAuthority.CASE_LAW_SUPREME,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "Texas courts construe mineral deeds under the four-corners rule: the intent "
                "of the parties is determined from the instrument as a whole, not from isolated "
                "clauses. When the granting clause and the habendum clause conflict, the granting "
                "clause generally prevails. The Texas Supreme Court in Luckel v. White established "
                "the harmonization approach: courts should attempt to harmonize all parts of "
                "the instrument before giving one clause priority over another. Key construction "
                "issues in mineral deeds include: (1) whether the deed conveys minerals or "
                "royalties, (2) whether the fraction applies to the grantor's interest or the "
                "whole estate, (3) whether the interest is fixed or floating, (4) whether "
                "executive rights are included, and (5) whether the deed includes a Mother "
                "Hubbard clause covering after-acquired interests. For mineral deeds executed "
                "after 1983, the Moser ordinary-and-natural-meaning test applies to determine "
                "what substances are included in 'minerals.' The Duhig rule applies to warranty "
                "deeds that convey minerals while the grantor has previously reserved minerals."
            ),
            legal_citations=[
                "Luckel v. White, 819 S.W.2d 459 (Tex. 1991)",
                "Altman v. Blake, 712 S.W.2d 117 (Tex. 1986)",
                "Moser v. U.S. Steel Corp., 676 S.W.2d 99 (Tex. 1984)",
                "Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503 (1940)",
            ],
            key_principles=[
                "Four-corners rule: intent from whole instrument",
                "Granting clause prevails over habendum if in conflict",
                "Harmonization approach before giving clause priority",
                "Moser test for 'minerals' definition post-1983",
                "Duhig rule for warranty deeds with prior mineral reservations",
            ],
            practical_notes=[
                "Read entire deed, not just granting clause, for interpretation",
                "Identify and flag any internal conflicts between deed clauses",
                "Check deed date for applicable interpretive framework",
                "Apply Duhig analysis to every warranty deed in the chain",
            ],
            related_blocks=["LM04-MRD-001", "LM04-MRD-002", "LM04-FRAC-002"],
        ))

        self._register(DoctrineBlock(
            block_id="LM04-CONV-002",
            title="Reservation vs Exception in Mineral Conveyances",
            category=DoctrineCategory.CONVEYANCE,
            authority=DoctrineAuthority.CASE_LAW_SUPREME,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "In mineral conveyances, a reservation creates a new interest in the grantor, "
                "while an exception withholds an existing interest from the conveyance. "
                "Historically, this distinction mattered because at common law a reservation "
                "could only be in favor of the grantor, while an exception could withhold "
                "interests for third parties. Texas largely eliminated this distinction by "
                "statute and case law, but the language still matters for interpretation. "
                "A deed that says 'reserving unto grantor 1/2 of the mineral estate' creates "
                "a new interest in the grantor (the 1/2 mineral interest). A deed that says "
                "'excepting the 1/2 mineral interest previously conveyed to X' withholds an "
                "already-existing interest. For tracking purposes, reservations by the grantor "
                "create fractional interests that remain with the grantor, while exceptions "
                "recognize interests already held by third parties. Both reduce the interest "
                "conveyed to the grantee."
            ),
            legal_citations=[
                "Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503 (1940)",
                "Benge v. Scharbauer, 152 Tex. 447 (1953)",
                "Williams & Meyers, Oil and Gas Law \u00a7\u00a7304-306",
            ],
            key_principles=[
                "Reservation creates new interest in grantor",
                "Exception withholds existing interest from conveyance",
                "Texas has largely merged the doctrines",
                "Both reduce the interest conveyed to grantee",
                "Language and context determine which applies",
            ],
            practical_notes=[
                "Identify every reservation and exception in each deed",
                "Track reserved interests as remaining with grantor's chain",
                "Track excepted interests as belonging to the identified third party",
                "Calculate net interest conveyed = total interest - reservations - exceptions",
            ],
            related_blocks=["LM04-CONV-001", "LM04-FRAC-002", "LM04-OWN-002"],
        ))

    # === CONFLICT DOCTRINES ===========================================

    def _load_conflict_doctrines(self) -> None:
        self._register(DoctrineBlock(
            block_id="LM04-CONF-001",
            title="Over-Conveyance and Interest Summation Conflicts",
            category=DoctrineCategory.CONFLICT,
            authority=DoctrineAuthority.CASE_LAW_SUPREME,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "An over-conveyance occurs when the total mineral interests conveyed from a "
                "common source exceed 100% of the mineral estate. This can happen through: "
                "(1) mathematical error in fractional computations, (2) overlapping grants, "
                "(3) failure to account for prior reservations, (4) Duhig rule complications, "
                "or (5) ambiguous deed language interpreted differently by different parties. "
                "When interests sum to more than 100%, several resolution approaches exist: "
                "first-in-time priority (earlier conveyance has priority), proportional "
                "reduction (all interests reduced pro rata to sum to 100%), or estoppel "
                "(warranty deed grantor estopped from claiming against their warranty). "
                "Texas generally follows first-in-time priority for recorded instruments under "
                "the recording act: the first recorded deed has priority over later-recorded "
                "deeds from the same grantor. However, a bona fide purchaser for value without "
                "notice may take free of a prior unrecorded instrument."
            ),
            legal_citations=[
                "Tex. Prop. Code Ann. \u00a713.001 (recording statute)",
                "Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503 (1940)",
                "Benge v. Scharbauer, 152 Tex. 447 (1953)",
                "Madison v. Gordon, 39 S.W.3d 604 (Tex. 2001)",
            ],
            key_principles=[
                "Over-conveyance = total interests exceed 100%",
                "First-in-time priority under recording act",
                "BFP without notice may prevail over prior unrecorded deed",
                "Duhig rule may estop grantor from over-conveyance claim",
                "Proportional reduction may apply in some circumstances",
            ],
            practical_notes=[
                "Run summation check on every tract: all interests must sum to 100%",
                "Flag any tract where interests exceed 100% as CONFLICT",
                "Identify the source of over-conveyance in the chain",
                "Document resolution approach and legal basis",
            ],
            related_blocks=["LM04-CONF-002", "LM04-FRAC-002", "LM04-CONV-001"],
        ))

        self._register(DoctrineBlock(
            block_id="LM04-CONF-002",
            title="Gap Detection and Missing Interest Identification",
            category=DoctrineCategory.CONFLICT,
            authority=DoctrineAuthority.PRACTICE_GUIDE,
            jurisdiction=Jurisdiction.MULTI_STATE,
            content=(
                "A gap in mineral interest occurs when the total interests in a tract sum to "
                "less than 100%. Gaps indicate one or more of: (1) unrecorded conveyances, "
                "(2) missing probate records, (3) overlooked reservations, (4) dormant mineral "
                "interests that may have reverted, or (5) interests held by unknown or unfound "
                "heirs. Gap detection is essential for accurate division order preparation and "
                "for identifying curative requirements. The gap analysis should be performed "
                "at every stage of the mineral interest computation. When a gap is detected, "
                "the landman must investigate: check for unrecorded deeds, search for additional "
                "probate records, review county tax records for unlisted owners, and examine "
                "Railroad Commission production records for interest holders not appearing in "
                "the title chain. A gap may also indicate a title defect requiring curative "
                "action (corrective deed, quiet title suit, or missing heir proceeding)."
            ),
            legal_citations=[
                "Williams & Meyers, Oil and Gas Law \u00a7\u00a7502-504",
                "AAPL Title Examination Standards",
            ],
            key_principles=[
                "Gap = total interests sum to less than 100%",
                "Indicates missing conveyances, probate, or reservations",
                "May require curative action to resolve",
                "Check tax records and RRC records for hidden owners",
                "Gaps block clean division order preparation",
            ],
            practical_notes=[
                "Run gap check on every tract alongside summation check",
                "Flag any tract where interests sum to less than 99.9%",
                "Investigate tax roll, RRC, and county records for missing interests",
                "Document gap source and recommended curative action",
            ],
            related_blocks=["LM04-CONF-001", "LM04-FRAC-001", "LM04-CONV-001"],
        ))

    # === LOUISIANA COMPARISON ==========================================

    def _load_louisiana_comparison(self) -> None:
        self._register(DoctrineBlock(
            block_id="LM04-LA-001",
            title="Mineral Servitude - Louisiana Civil Law Comparison",
            category=DoctrineCategory.LOUISIANA_COMPARE,
            authority=DoctrineAuthority.STATUTORY,
            jurisdiction=Jurisdiction.LOUISIANA,
            content=(
                "Louisiana, as a civil law state, uses the mineral servitude concept instead of "
                "the common law severed mineral estate. Under La. R.S. 31:16 et seq. (the "
                "Mineral Code), a mineral servitude is a real right to explore, develop, and "
                "produce minerals from another's land. Unlike Texas's permanent mineral severance, "
                "a Louisiana mineral servitude prescribes (extinguishes) after 10 years of "
                "non-use (no drilling, production, or good faith operations). This prescription "
                "period is critical for border county analysis: mineral interests near the "
                "Texas-Louisiana border may be governed by Louisiana law if the minerals are "
                "located in Louisiana. The key differences from Texas: (1) mineral servitude "
                "prescribes after 10 years of non-use, (2) no severance of executive rights "
                "concept, (3) mineral royalties are separate concept under La. R.S. 31:80, "
                "(4) forced unitization governed by Commissioner of Conservation, and (5) no "
                "Duhig rule equivalent. For Permian Basin operations, this is primarily relevant "
                "for border county due diligence when checking interests that may have Louisiana "
                "components or when dealing with parties who hold interests in both states."
            ),
            legal_citations=[
                "La. R.S. 31:16 et seq. (Mineral Code)",
                "La. R.S. 31:27 (prescription of mineral servitude)",
                "La. R.S. 31:80 (mineral royalties)",
                "La. Civ. Code Art. 3546 (choice of law for immovables)",
            ],
            key_principles=[
                "Mineral servitude prescribes after 10 years of non-use",
                "No permanent mineral estate severance in Louisiana",
                "No separation of executive rights concept",
                "Different unitization/pooling regime",
                "Choice of law follows situs of the minerals",
            ],
            practical_notes=[
                "Check situs of minerals for cross-border tracts",
                "Apply Louisiana law to minerals located in Louisiana",
                "Monitor 10-year prescription period for Louisiana mineral servitudes",
                "Different analysis framework than Texas common law minerals",
            ],
            related_blocks=["LM04-DORM-001", "LM04-OWN-002", "LM04-OWN-001"],
        ))

    # === DORMANT MINERAL ACTS =========================================

    def _load_dormant_mineral_doctrines(self) -> None:
        self._register(DoctrineBlock(
            block_id="LM04-DORM-001",
            title="Texas Dormant Mineral Act",
            category=DoctrineCategory.DORMANT_MINERAL,
            authority=DoctrineAuthority.STATUTORY,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "Texas does not have a traditional dormant mineral act that extinguishes unused "
                "mineral interests. However, several mechanisms can affect stale mineral interests: "
                "(1) the Mineral Interest Pooling Act (Tex. Nat. Res. Code \u00a7102.001 et seq.) "
                "provides for compulsory pooling, (2) adverse possession may apply to mineral "
                "interests in limited circumstances (Tex. Civ. Prac. & Rem. Code \u00a716.025 requires "
                "actual possession and production for 10 years), (3) marketable title acts in "
                "other states may affect interests of Texas-based owners in those states, and "
                "(4) the Texas Tax Code provides for tax foreclosure of mineral interests with "
                "delinquent taxes. While Texas does not have a dormant mineral act like Ohio "
                "(O.R.C. \u00a75301.56), Indiana (IC 32-23-10), or West Virginia (W. Va. Code "
                "\u00a736-4-9a), the practical effect of long dormancy is that interests become "
                "difficult to trace and may require curative action. The title examiner should "
                "flag any mineral interest that has not been the subject of a recorded instrument "
                "or tax payment for more than 20 years."
            ),
            legal_citations=[
                "Tex. Nat. Res. Code Ann. \u00a7102.001 et seq.",
                "Tex. Civ. Prac. & Rem. Code Ann. \u00a716.025",
                "Tex. Tax Code Ann. \u00a733.01 et seq.",
                "Compare O.R.C. \u00a75301.56 (Ohio Dormant Mineral Act)",
            ],
            key_principles=[
                "Texas has NO traditional dormant mineral act",
                "Adverse possession requires 10 years actual possession/production",
                "Tax foreclosure may extinguish delinquent mineral interests",
                "Compulsory pooling available under MIPA",
                "Long dormancy creates practical tracing difficulties",
            ],
            practical_notes=[
                "Flag interests inactive > 20 years for investigation",
                "Check tax payment history for dormant mineral interests",
                "Verify no adverse possession claims against dormant interests",
                "Compare with other state dormant mineral acts for multi-state interests",
            ],
            related_blocks=["LM04-LA-001", "LM04-CONF-002", "LM04-OWN-001"],
        ))

    # === PARTITION =====================================================

    def _load_partition_doctrines(self) -> None:
        self._register(DoctrineBlock(
            block_id="LM04-PART-001",
            title="Partition of Mineral Estates",
            category=DoctrineCategory.PARTITION,
            authority=DoctrineAuthority.STATUTORY,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "Partition is the division of co-owned property into separately owned portions. "
                "Under Tex. Prop. Code \u00a723.001 et seq., any co-owner of mineral interests may "
                "seek partition. There are two types: partition in kind (physical division of "
                "the mineral estate by geographic area) and partition by sale (forced sale of "
                "the entire mineral interest with proceeds divided). Courts prefer partition "
                "in kind when practicable. For mineral estates, partition in kind converts "
                "undivided interests into divided (geographically specific) interests. After "
                "partition in kind, each former co-owner holds 100% of the minerals beneath "
                "their partitioned portion, rather than an undivided fraction of the whole. "
                "Partition fundamentally changes NMA calculations: before partition, an owner "
                "of 1/4 undivided interest in 640 acres has 160 NMA across the entire tract. "
                "After partition in kind, the same owner might hold 100% of minerals beneath "
                "160 specific acres. This is the same NMA numerically but a very different "
                "interest geographically."
            ),
            legal_citations=[
                "Tex. Prop. Code Ann. \u00a723.001 et seq.",
                "Yturria v. Kimbro, 921 S.W.2d 338 (Tex. App. 1996)",
                "Williams & Meyers, Oil and Gas Law \u00a7\u00a7515-517",
            ],
            key_principles=[
                "Any co-owner may seek partition of mineral interests",
                "Partition in kind preferred over partition by sale",
                "Partition in kind converts undivided to divided interests",
                "NMA unchanged numerically but geographically different",
                "After partition, each owner holds 100% of their portion",
            ],
            practical_notes=[
                "Check for recorded partition deeds or court orders",
                "After partition, track interests geographically, not fractionally",
                "Update NMA calculations to reflect partitioned ownership",
                "Note that partition by sale extinguishes the mineral interest entirely",
            ],
            related_blocks=["LM04-OWN-003", "LM04-FRAC-001", "LM04-CONF-001"],
        ))

    # === SURFACE-MINERAL =============================================

    def _load_surface_mineral_doctrines(self) -> None:
        self._register(DoctrineBlock(
            block_id="LM04-SURF-001",
            title="Accommodation Doctrine",
            category=DoctrineCategory.SURFACE_MINERAL,
            authority=DoctrineAuthority.CASE_LAW_SUPREME,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "The accommodation doctrine, established in Getty Oil Co. v. Jones, 470 S.W.2d "
                "618 (Tex. 1971), requires the mineral estate owner (dominant estate) to "
                "accommodate existing surface uses when reasonable alternatives exist for "
                "mineral operations. The mineral estate remains dominant, but the mineral "
                "owner must use the surface with due regard for the surface owner's rights. "
                "The doctrine applies when: (1) the surface owner has an existing use that "
                "would be substantially impaired by the mineral operations, (2) the mineral "
                "owner has reasonable alternative methods of conducting operations that would "
                "not impair the surface use, and (3) the alternative methods are available and "
                "practicable. The doctrine does not require the mineral owner to forego "
                "development entirely, only to use reasonable alternatives when available."
            ),
            legal_citations=[
                "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)",
                "Tex. Nat. Res. Code Ann. \u00a791.402 (Surface Damage Act)",
                "Merriman v. XTO Energy, Inc., 407 S.W.3d 244 (Tex. 2013)",
            ],
            key_principles=[
                "Mineral estate is dominant but must accommodate existing surface uses",
                "Three-part test: existing surface use, impairment, reasonable alternatives",
                "Does not prevent development, only requires reasonable accommodation",
                "Surface Damage Act provides additional compensation requirements",
                "Applies to severed mineral estate operations",
            ],
            practical_notes=[
                "Note existing surface uses when examining mineral tract",
                "Factor accommodation requirements into development planning",
                "Not directly relevant to ownership tracking but affects value",
                "Surface damage payments may be required even without accommodation issues",
            ],
            related_blocks=["LM04-SURF-002", "LM04-OWN-002"],
        ))

        self._register(DoctrineBlock(
            block_id="LM04-SURF-002",
            title="Surface Destruction Test and Mineral Definition",
            category=DoctrineCategory.SURFACE_MINERAL,
            authority=DoctrineAuthority.CASE_LAW_SUPREME,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "The surface destruction test, developed in Acker v. Guinn, 464 S.W.2d 348 "
                "(Tex. 1971) and refined in Moser v. U.S. Steel Corp., 676 S.W.2d 99 (Tex. "
                "1984), determines what substances are included in a 'mineral' severance. "
                "Under Acker, if extraction of a substance would consume or destroy the surface, "
                "it is not included in a pre-1983 general mineral reservation. After Moser, "
                "for instruments dated 1983 or later, courts apply the ordinary-and-natural-"
                "meaning test: 'minerals' includes substances that a reasonable person would "
                "understand as minerals (primarily oil, gas, and their constituents). This "
                "affects tracking because the definition of what minerals are included in an "
                "interest varies by instrument date and language. Common disputes involve: "
                "limestone, caliche, sand, gravel, uranium, lignite, and geothermal resources."
            ),
            legal_citations=[
                "Acker v. Guinn, 464 S.W.2d 348 (Tex. 1971)",
                "Moser v. U.S. Steel Corp., 676 S.W.2d 99 (Tex. 1984)",
                "Friedman v. Texaco, Inc., 691 F.2d 241 (5th Cir. 1982)",
                "Schwarz v. State, 703 S.W.2d 187 (Tex. 1986)",
            ],
            key_principles=[
                "Pre-1983 instruments: surface destruction test (Acker)",
                "Post-1983 instruments: ordinary-and-natural-meaning test (Moser)",
                "Oil and gas always included in 'minerals'",
                "Near-surface substances may or may not be included",
                "Instrument language and date control the analysis",
            ],
            practical_notes=[
                "Check instrument date to determine applicable test",
                "For pre-1983 instruments, evaluate surface destruction potential",
                "For post-1983 instruments, apply ordinary meaning of 'minerals'",
                "Document which substances are included/excluded in each interest",
            ],
            related_blocks=["LM04-SURF-001", "LM04-OWN-002", "LM04-CONV-001"],
        ))

    # === LEASING ======================================================

    def _load_leasing_doctrines(self) -> None:
        self._register(DoctrineBlock(
            block_id="LM04-LEASE-001",
            title="Oil and Gas Lease Impact on Mineral Interests",
            category=DoctrineCategory.LEASING,
            authority=DoctrineAuthority.CASE_LAW_SUPREME,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "An oil and gas lease creates a determinable fee in the lessee (the working "
                "interest) and converts the lessor's mineral interest into a royalty interest "
                "for the duration of the lease. The lessor retains the executive right for "
                "future leases (after lease termination), the right to bonus, delay rentals, "
                "and the royalty interest specified in the lease. The lease has a primary term "
                "(typically 3-5 years) and continues into a secondary term 'and so long "
                "thereafter as oil or gas is produced' (the habendum clause). During the lease "
                "term, the mineral interest is said to be 'leased' and the mineral owner's "
                "practical rights are limited to receiving royalty payments. Upon lease "
                "termination, all rights revert to the mineral owner (or their successors). "
                "For tracking purposes, the existence and status of any lease is critical: "
                "it determines whether the mineral interest is currently generating royalty "
                "income and whether the executive right is currently exercisable."
            ),
            legal_citations=[
                "Stephens County v. Mid-Kansas Oil & Gas Co., 113 Tex. 160 (1923)",
                "Texas Co. v. Davis, 113 Tex. 321, 254 S.W. 304 (1923)",
                "Natural Gas Pipeline Co. of Am. v. Pool, 124 Tex. 257 (1934)",
            ],
            key_principles=[
                "Lease creates determinable fee in lessee (working interest)",
                "Lessor's mineral interest converts to royalty during lease term",
                "Primary term + secondary term (production) habendum structure",
                "All rights revert on lease termination",
                "Lease status is critical for interest tracking",
            ],
            practical_notes=[
                "Track lease status (active/expired/released) for every tract",
                "Record lease royalty rate for NRI calculations",
                "Monitor primary term expiration dates",
                "Note that leased vs unleased status affects executive right tracking",
            ],
            related_blocks=["LM04-INT-001", "LM04-INT-005", "LM04-POOL-001"],
        ))

    # === TEXAS-SPECIFIC ===============================================

    def _load_texas_specific_doctrines(self) -> None:
        self._register(DoctrineBlock(
            block_id="LM04-TX-001",
            title="Texas Recording Act and Mineral Interest Priority",
            category=DoctrineCategory.TEXAS_SPECIFIC,
            authority=DoctrineAuthority.STATUTORY,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "Texas has a notice recording statute (Tex. Prop. Code \u00a713.001): a conveyance "
                "of real property (including mineral interests) is void as to a subsequent "
                "purchaser for valuable consideration without notice unless the conveyance "
                "has been duly recorded. This means: (1) an unrecorded mineral deed is valid "
                "between the parties but may be defeated by a bona fide purchaser (BFP) for "
                "value without notice, (2) constructive notice is provided by recording in "
                "the county where the property is located, (3) actual notice of an unrecorded "
                "deed prevents a subsequent purchaser from qualifying as a BFP. For mineral "
                "interest tracking, the recording act creates priority rules: the first properly "
                "recorded deed generally has priority, except that an earlier unrecorded deed "
                "prevails if the subsequent purchaser had actual notice. Title examiners must "
                "check recording dates, not just execution dates, to establish priority."
            ),
            legal_citations=[
                "Tex. Prop. Code Ann. \u00a713.001",
                "Madison v. Gordon, 39 S.W.3d 604 (Tex. 2001)",
                "Lutken v. Allen, 595 S.W.2d 120 (Tex. Civ. App. 1980)",
            ],
            key_principles=[
                "Texas notice recording statute: unrecorded deed void vs BFP",
                "Recording provides constructive notice",
                "Actual notice defeats BFP status",
                "Priority based on recording date, not execution date",
                "Valid between parties even if unrecorded",
            ],
            practical_notes=[
                "Track both execution and recording dates for every instrument",
                "Establish priority based on recording sequence",
                "Investigate any gaps in the recording chain for unrecorded instruments",
                "Note that actual notice can create priority outside recording order",
            ],
            related_blocks=["LM04-CONV-001", "LM04-CONF-001", "LM04-OWN-001"],
        ))

        self._register(DoctrineBlock(
            block_id="LM04-TX-002",
            title="Texas Relinquishment Act and State Mineral Ownership",
            category=DoctrineCategory.TEXAS_SPECIFIC,
            authority=DoctrineAuthority.STATUTORY,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "Under the Texas Relinquishment Act (Tex. Nat. Res. Code \u00a752.171 et seq.), "
                "the State of Texas relinquishes its mineral interest in certain lands to the "
                "surface owner, subject to specific conditions. The Act applies to 'free royalty' "
                "lands — lands sold by the State with a reservation of minerals. The State "
                "relinquishes its mineral interest to the surface owner (or their successors) "
                "for leasing purposes, retaining a royalty interest (typically 1/16). The "
                "surface owner may execute leases as the State's agent and receives the "
                "remainder of the royalty above the State's retained interest. This creates a "
                "unique ownership structure: the State owns the minerals but the surface owner "
                "has the exclusive right to lease. For tracts with State mineral ownership, "
                "the Relinquishment Act must be analyzed to determine: (1) whether the Act "
                "applies to the specific land, (2) the State's retained royalty fraction, "
                "(3) the surface owner's leasing authority, and (4) any specific terms imposed "
                "by the General Land Office."
            ),
            legal_citations=[
                "Tex. Nat. Res. Code Ann. \u00a752.171 et seq.",
                "Greene v. Robison, 117 Tex. 516, 8 S.W.2d 655 (1928)",
                "Magnolia Petroleum Co. v. Railroad Comm'n, 141 Tex. 96 (1943)",
            ],
            key_principles=[
                "Relinquishment Act transfers leasing authority to surface owner",
                "State retains mineral ownership but relinquishes executive right",
                "State retains royalty interest (typically 1/16)",
                "Surface owner acts as State's agent for leasing",
                "Applies to specific 'free royalty' lands sold by State",
            ],
            practical_notes=[
                "Check land patent for State mineral reservation language",
                "Determine if Relinquishment Act applies to the specific tract",
                "Contact GLO for confirmation of State mineral ownership status",
                "Track State's retained royalty as a burden on the mineral estate",
            ],
            related_blocks=["LM04-TX-001", "LM04-OWN-001", "LM04-LEASE-001"],
        ))

        self._register(DoctrineBlock(
            block_id="LM04-TX-003",
            title="Railroad Commission and Mineral Interest Regulation",
            category=DoctrineCategory.TEXAS_SPECIFIC,
            authority=DoctrineAuthority.REGULATORY,
            jurisdiction=Jurisdiction.TEXAS,
            content=(
                "The Railroad Commission of Texas (RRC) regulates oil and gas production in "
                "Texas and its regulatory actions directly affect mineral interests. Key RRC "
                "functions impacting mineral interest tracking: (1) spacing rules determine "
                "minimum well density, affecting which tracts can be developed, (2) pooling "
                "and unitization orders combine interests for regulatory purposes, (3) "
                "production allowables limit how much each well can produce, affecting revenue, "
                "(4) well permits (Form W-1) identify operators and working interest owners, "
                "(5) production reports (Form P-1) provide monthly production data for royalty "
                "verification, and (6) plugging reports (Form W-3A) document well abandonment. "
                "The RRC's online system (RRC GIS Viewer and PDQI) provides public access to "
                "well data, permit information, and production records. For mineral interest "
                "tracking, RRC records serve as an independent verification source for lease "
                "status, operator identity, production volumes, and unit declarations."
            ),
            legal_citations=[
                "Tex. Nat. Res. Code Ann. \u00a785.001 et seq. (RRC jurisdiction)",
                "Tex. Nat. Res. Code Ann. \u00a786.011 et seq. (well spacing)",
                "16 Tex. Admin. Code \u00a73.37 et seq. (Statewide Rules)",
            ],
            key_principles=[
                "RRC regulates production but does not determine ownership",
                "Spacing rules affect development potential of mineral interests",
                "Pooling/unitization orders combine interests for regulatory purposes",
                "Production reports verify royalty calculations",
                "RRC records are independent verification for interest tracking",
            ],
            practical_notes=[
                "Cross-reference RRC records with title chain for verification",
                "Check RRC for active permits and production on tracked tracts",
                "Monitor RRC pooling/unitization orders affecting tracked interests",
                "Use RRC production data to verify royalty payment accuracy",
            ],
            related_blocks=["LM04-POOL-001", "LM04-LEASE-001", "LM04-INT-001"],
        ))


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

_doctrine_cache: MineralInterestDoctrineCache | None = None


def get_doctrine_cache() -> MineralInterestDoctrineCache:
    """Get or create the singleton doctrine cache instance."""
    global _doctrine_cache
    if _doctrine_cache is None:
        _doctrine_cache = MineralInterestDoctrineCache()
    return _doctrine_cache


def search_doctrines(keyword: str) -> list[dict[str, Any]]:
    """Search doctrines by keyword, returning dict representations."""
    cache = get_doctrine_cache()
    blocks = cache.search(keyword)
    return [b.to_dict() for b in blocks]


def get_doctrine_by_id(block_id: str) -> dict[str, Any] | None:
    """Get a single doctrine block by ID."""
    cache = get_doctrine_cache()
    block = cache.get_block(block_id)
    return block.to_dict() if block else None


def get_doctrines_by_category(category: str) -> list[dict[str, Any]]:
    """Get all doctrines in a category."""
    cache = get_doctrine_cache()
    try:
        cat = DoctrineCategory(category)
    except ValueError:
        return []
    blocks = cache.get_by_category(cat)
    return [b.to_dict() for b in blocks]


def get_doctrine_stats() -> dict[str, Any]:
    """Get statistics about the doctrine cache."""
    cache = get_doctrine_cache()
    return {
        "total_blocks": cache.block_count,
        "categories": cache.category_counts,
        "engine": "LM04",
        "version": "1.0.0",
    }
