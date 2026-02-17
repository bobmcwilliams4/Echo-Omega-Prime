"""
LM14 Easement Analyzer Engine - Doctrine Cache Module
========================================================
Pre-compiled easement doctrine blocks for instant retrieval on common
rights-of-way, surface use, pipeline corridor, accommodation doctrine,
eminent domain, and Texas-specific easement queries.

Each doctrine block contains:
    - topic: Canonical topic identifier
    - summary: Executive-level overview of the doctrine
    - key_statutes: Controlling statutory references
    - elements: Legal elements or requirements
    - defenses: Common defenses or exceptions
    - remedies: Available remedies or relief
    - leading_cases: Landmark case citations

Components:
    - DOCTRINE_BLOCKS: List of pre-compiled doctrine cache entries
    - DoctrineCacheBlock: Structured doctrine entry model
    - DoctrineCacheIndex: Fast O(1) lookup by topic/category
    - build_doctrine_cache(): Build the complete cache from blocks
    - get_doctrine_block(): Retrieve a single block by topic
    - search_doctrines(): Free-text search over doctrine blocks
    - get_coverage_map(): Map of all topics with staleness data
    - get_all_doctrine_topics(): List every registered topic
    - get_all_doctrine_categories(): List every registered category

Version: 1.0.0
Engine: LM14 Easement Analyzer
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from typing import Any, ClassVar, Dict, List, Optional, Set

from loguru import logger


# ============================================================================
# DOCTRINE CACHE BLOCK MODEL
# ============================================================================

@dataclass
class DoctrineCacheBlock:
    """A single pre-compiled easement doctrine cache entry."""

    topic: str
    summary: str
    key_statutes: List[str]
    elements: List[str]
    defenses: List[str]
    remedies: List[str]
    leading_cases: List[str]
    category: str
    subcategory: str = ""
    jurisdiction: str = "texas"
    authority_score: float = 0.80
    last_updated: str = ""
    tags: List[str] = dc_field(default_factory=list)
    cross_references: List[str] = dc_field(default_factory=list)
    notes: str = ""
    _access_count: int = dc_field(default=0, repr=False)
    _last_accessed: float = dc_field(default=0.0, repr=False)

    # Class-level constants
    STALENESS_THRESHOLD_DAYS: ClassVar[int] = 180
    MIN_AUTHORITY_SCORE: ClassVar[float] = 0.50

    def __post_init__(self) -> None:
        if not self.last_updated:
            self.last_updated = datetime.now(timezone.utc).isoformat()
        if not self.tags:
            self.tags = [self.category.lower().replace(" ", "_")]

    def record_access(self) -> None:
        """Track access for LRU and popularity metrics."""
        self._access_count += 1
        self._last_accessed = time.time()

    def is_stale(self) -> bool:
        """Return True if the block was last updated beyond the staleness threshold."""
        try:
            updated_dt = datetime.fromisoformat(self.last_updated)
            if updated_dt.tzinfo is None:
                updated_dt = updated_dt.replace(tzinfo=timezone.utc)
            age_days = (datetime.now(timezone.utc) - updated_dt).days
            return age_days > self.STALENESS_THRESHOLD_DAYS
        except (ValueError, TypeError):
            return True

    def content_hash(self) -> str:
        """SHA-256 hash of the block content for determinism verification."""
        payload = json.dumps(
            {
                "topic": self.topic,
                "summary": self.summary,
                "key_statutes": self.key_statutes,
                "elements": self.elements,
                "defenses": self.defenses,
                "remedies": self.remedies,
                "leading_cases": self.leading_cases,
                "category": self.category,
                "subcategory": self.subcategory,
            },
            sort_keys=True,
        )
        return hashlib.sha256(payload.encode()).hexdigest()

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
            "category": self.category,
            "subcategory": self.subcategory,
            "jurisdiction": self.jurisdiction,
            "authority_score": self.authority_score,
            "last_updated": self.last_updated,
            "tags": self.tags,
            "cross_references": self.cross_references,
            "notes": self.notes,
            "content_hash": self.content_hash(),
            "access_count": self._access_count,
        }

    def matches_query(self, query: str) -> float:
        """Return a relevance score (0.0-1.0) for a free-text query."""
        query_lower = query.lower()
        tokens = query_lower.split()
        searchable = (
            f"{self.topic} {self.summary} {self.category} {self.subcategory} "
            f"{' '.join(self.key_statutes)} {' '.join(self.elements)} "
            f"{' '.join(self.tags)} {' '.join(self.leading_cases)} {self.notes}"
        ).lower()

        if not tokens:
            return 0.0

        matched_count = sum(1 for t in tokens if t in searchable)
        base_score = matched_count / len(tokens)

        # Boost for exact topic match
        if query_lower in self.topic.lower():
            base_score = min(1.0, base_score + 0.3)

        # Boost for category match
        if query_lower in self.category.lower():
            base_score = min(1.0, base_score + 0.15)

        return round(base_score, 4)


# ============================================================================
# DOCTRINE CACHE INDEX
# ============================================================================

class DoctrineCacheIndex:
    """Fast O(1) lookup by topic, category, and tag with LRU tracking."""

    def __init__(self) -> None:
        self._by_topic: Dict[str, DoctrineCacheBlock] = {}
        self._by_category: Dict[str, List[DoctrineCacheBlock]] = {}
        self._by_tag: Dict[str, List[DoctrineCacheBlock]] = {}
        self._all_blocks: List[DoctrineCacheBlock] = []
        self._build_time: float = 0.0

    @property
    def size(self) -> int:
        return len(self._all_blocks)

    @property
    def categories(self) -> List[str]:
        return sorted(self._by_category.keys())

    @property
    def topics(self) -> List[str]:
        return sorted(self._by_topic.keys())

    def build(self, blocks: List[DoctrineCacheBlock]) -> None:
        """Build the index from a list of doctrine blocks."""
        start = time.time()
        self._by_topic.clear()
        self._by_category.clear()
        self._by_tag.clear()
        self._all_blocks = list(blocks)

        for block in blocks:
            # Index by topic (case-insensitive key)
            topic_key = block.topic.lower().strip()
            if topic_key in self._by_topic:
                logger.warning(f"Duplicate doctrine topic: {block.topic}")
            self._by_topic[topic_key] = block

            # Index by category
            cat_key = block.category.lower().strip()
            if cat_key not in self._by_category:
                self._by_category[cat_key] = []
            self._by_category[cat_key].append(block)

            # Index by tags
            for tag in block.tags:
                tag_key = tag.lower().strip()
                if tag_key not in self._by_tag:
                    self._by_tag[tag_key] = []
                self._by_tag[tag_key].append(block)

        self._build_time = time.time() - start
        logger.info(
            f"Doctrine cache index built: {len(blocks)} blocks, "
            f"{len(self._by_category)} categories, "
            f"{len(self._by_tag)} tags in {self._build_time:.3f}s"
        )

    def get_by_topic(self, topic: str) -> Optional[DoctrineCacheBlock]:
        """Retrieve a block by exact topic match (case-insensitive)."""
        block = self._by_topic.get(topic.lower().strip())
        if block:
            block.record_access()
        return block

    def get_by_category(self, category: str) -> List[DoctrineCacheBlock]:
        """Retrieve all blocks in a category."""
        blocks = self._by_category.get(category.lower().strip(), [])
        for b in blocks:
            b.record_access()
        return blocks

    def get_by_tag(self, tag: str) -> List[DoctrineCacheBlock]:
        """Retrieve all blocks with a given tag."""
        blocks = self._by_tag.get(tag.lower().strip(), [])
        for b in blocks:
            b.record_access()
        return blocks

    def search(self, query: str, top_k: int = 10) -> List[DoctrineCacheBlock]:
        """Free-text search over all blocks. Returns top_k by relevance."""
        scored = []
        for block in self._all_blocks:
            score = block.matches_query(query)
            if score > 0.0:
                scored.append((score, block))
        scored.sort(key=lambda x: x[0], reverse=True)
        results = [b for _, b in scored[:top_k]]
        for b in results:
            b.record_access()
        return results

    def get_stale_blocks(self) -> List[DoctrineCacheBlock]:
        """Return blocks that are past their staleness threshold."""
        return [b for b in self._all_blocks if b.is_stale()]

    def coverage_map(self) -> Dict[str, Any]:
        """Return coverage statistics per category."""
        coverage: Dict[str, Any] = {}
        for cat, blocks in self._by_category.items():
            stale_count = sum(1 for b in blocks if b.is_stale())
            avg_authority = sum(b.authority_score for b in blocks) / max(len(blocks), 1)
            coverage[cat] = {
                "total_blocks": len(blocks),
                "stale_blocks": stale_count,
                "average_authority": round(avg_authority, 3),
                "topics": [b.topic for b in blocks],
            }
        return coverage

    def export_all(self) -> List[Dict[str, Any]]:
        """Export all blocks as serializable dicts."""
        return [b.to_dict() for b in self._all_blocks]


# ============================================================================
# DOCTRINE BLOCKS - THE KNOWLEDGE BASE
# ============================================================================

DOCTRINE_BLOCKS: List[DoctrineCacheBlock] = [
    # ------------------------------------------------------------------
    # CATEGORY: Express Easements
    # ------------------------------------------------------------------
    DoctrineCacheBlock(
        topic="express_easement_creation",
        summary=(
            "An express easement is created by a written instrument, typically a deed "
            "or grant, that explicitly conveys the right to use another's property for "
            "a specified purpose. In Texas, the Statute of Frauds (Tex. Bus. & Com. Code "
            "\xA726.01) requires that all conveyances of interests in real property, "
            "including easements, be in writing and signed by the grantor. The grant must "
            "identify the dominant and servient estates (if appurtenant), describe the "
            "purpose of the easement, and ideally specify width, location, and duration."
        ),
        key_statutes=[
            "Tex. Bus. & Com. Code \xA726.01 (Statute of Frauds)",
            "Tex. Prop. Code \xA75.021 (Requirements for Conveyance)",
            "Tex. Prop. Code \xA713.001 (Recording Requirements)",
        ],
        elements=[
            "Written instrument signed by grantor (or authorized agent)",
            "Sufficient description of the easement location and purpose",
            "Identification of dominant and servient estates (if appurtenant)",
            "Consideration (though nominal consideration is sufficient)",
            "Delivery and acceptance of the instrument",
            "Recording in county deed records (not required for validity but protects against BFP)",
        ],
        defenses=[
            "Failure to satisfy Statute of Frauds",
            "Ambiguity in grant language rendering easement unenforceable",
            "Lack of grantor authority (e.g., co-owner did not join)",
            "Fraud, duress, or undue influence in procuring the grant",
            "Easement outside chain of title (wild deed)",
        ],
        remedies=[
            "Injunctive relief to enforce easement rights",
            "Declaratory judgment confirming easement existence and scope",
            "Damages for interference with easement use",
            "Reformation of instrument if mutual mistake in description",
            "Quiet title action to establish easement against challengers",
        ],
        leading_cases=[
            "Marcus Cable Assocs. v. Krohn, 90 S.W.3d 697 (Tex. 2002)",
            "Drye v. Eagle Rock Ranch, Inc., 364 S.W.2d 196 (Tex. 1963)",
            "DeWitt County Elec. Coop. v. Parks, 1 S.W.3d 96 (Tex. 1999)",
            "Hlavinka v. Hancock, 116 S.W.3d 412 (Tex. App.—Corpus Christi 2003)",
        ],
        category="Express Easements",
        subcategory="Creation",
        tags=["express", "creation", "statute_of_frauds", "conveyance", "deed"],
        cross_references=["express_easement_scope", "easement_recording"],
    ),
    DoctrineCacheBlock(
        topic="express_easement_scope",
        summary=(
            "The scope of an express easement is determined by the language of the "
            "grant instrument, interpreted in light of the parties' intent at the time "
            "of conveyance. Texas courts apply the four corners rule to construe the "
            "grant, looking first to the plain language of the instrument. Where the "
            "grant is ambiguous, courts may consider surrounding circumstances including "
            "the physical condition of the property, the purpose for which the easement "
            "was granted, and the parties' course of conduct. The scope encompasses the "
            "uses that are reasonably necessary to effectuate the purpose of the grant."
        ),
        key_statutes=[
            "Tex. Prop. Code \xA75.001 (Construction of Instruments)",
            "Tex. Prop. Code \xA75.021 (Deed Requirements)",
        ],
        elements=[
            "Language of the grant instrument controls scope",
            "Purpose stated in the grant defines permissible uses",
            "Width, depth, and location as specified or reasonably implied",
            "Duration (perpetual unless expressly limited to term of years)",
            "Ancillary rights reasonably necessary for primary use (e.g., maintenance access)",
            "Changes in use must be within the reasonable contemplation of the parties at grant",
        ],
        defenses=[
            "Use exceeds scope defined in grant instrument (overburdening)",
            "Unilateral relocation by dominant estate without consent or authority",
            "Changed use incompatible with original purpose",
            "Grant language ambiguous and extrinsic evidence supports narrow reading",
        ],
        remedies=[
            "Injunction to confine use within granted scope",
            "Damages for overburdening or excessive use",
            "Declaratory judgment defining scope boundaries",
            "Reformation if mutual mistake about scope",
        ],
        leading_cases=[
            "Marcus Cable Assocs. v. Krohn, 90 S.W.3d 697 (Tex. 2002) (scope limited to grant terms)",
            "Coleman v. Forister, 514 S.W.2d 899 (Tex. 1974) (changed use analysis)",
            "Severance v. Patterson, 370 S.W.3d 705 (Tex. 2012) (rolling easements)",
        ],
        category="Express Easements",
        subcategory="Scope",
        tags=["express", "scope", "overburdening", "width", "purpose"],
        cross_references=["overburdening_doctrine", "easement_modification"],
    ),
    DoctrineCacheBlock(
        topic="express_easement_recording",
        summary=(
            "Recording an easement instrument in the county deed records provides "
            "constructive notice to subsequent purchasers and protects the easement "
            "holder against bona fide purchaser claims. Texas follows a notice "
            "recording statute: an unrecorded instrument is void against subsequent "
            "BFP without notice. The instrument must comply with Tex. Prop. Code "
            "\xA712.001 et seq. to be eligible for recording."
        ),
        key_statutes=[
            "Tex. Prop. Code \xA713.001 (Recording Requirements)",
            "Tex. Prop. Code \xA712.001 (Instruments Eligible for Recording)",
            "Tex. Prop. Code \xA713.002 (Effect of Recording - Constructive Notice)",
        ],
        elements=[
            "Instrument must be acknowledged or proved per recording requirements",
            "Filed in county where servient estate is located",
            "Provides constructive notice from date of recording",
            "Unrecorded easement valid between original parties",
            "Recording protects against subsequent BFP without actual or constructive notice",
        ],
        defenses=[
            "Bona fide purchaser without notice takes free of unrecorded easement",
            "Recording defect (improper acknowledgment, wrong county) may negate constructive notice",
            "Inquiry notice from visible easement use may defeat BFP defense",
        ],
        remedies=[
            "Recording of easement instrument to cure constructive notice gap",
            "Suit to quiet title and establish easement priority",
            "Damages against grantor for failure to disclose known unrecorded easement",
        ],
        leading_cases=[
            "Cosgrove v. Cade, 468 S.W.3d 32 (Tex. 2015)",
            "Madison v. Gordon, 39 S.W.3d 604 (Tex. 2001)",
        ],
        category="Express Easements",
        subcategory="Recording",
        tags=["express", "recording", "constructive_notice", "bfp"],
        cross_references=["express_easement_creation"],
    ),

    # ------------------------------------------------------------------
    # CATEGORY: Implied Easements
    # ------------------------------------------------------------------
    DoctrineCacheBlock(
        topic="implied_easement_prior_use",
        summary=(
            "An implied easement by prior use arises when a landowner conveys part of "
            "a tract, and at the time of severance, one portion was being used for the "
            "benefit of the other in a manner that was apparent, continuous, and "
            "reasonably necessary. The use must have existed at the time of the "
            "severance, and both the grantor and grantee are presumed to have intended "
            "the use to continue. Texas courts require the use to be reasonably "
            "necessary (not strictly necessary) for the enjoyment of the dominant estate."
        ),
        key_statutes=[
            "No specific Texas statute - common law doctrine",
            "Restatement (Third) of Property: Servitudes \xA72.12 (persuasive)",
        ],
        elements=[
            "Common ownership of dominant and servient parcels prior to severance",
            "Use of one part for benefit of the other existed before severance",
            "The use was apparent (or discoverable upon reasonable inspection)",
            "The use was continuous (not sporadic or temporary)",
            "The use is reasonably necessary for enjoyment of the dominant estate",
            "The parties intended the use to continue after severance",
        ],
        defenses=[
            "Use was not apparent or discoverable at time of severance",
            "Use was merely convenient, not reasonably necessary",
            "Express language in the deed negates implied easement",
            "Use was permissive and not under claim of right",
            "No common ownership prior to severance",
        ],
        remedies=[
            "Declaratory judgment establishing implied easement",
            "Injunctive relief against interference",
            "Damages for interference with implied easement rights",
        ],
        leading_cases=[
            "Bains v. Parker, 143 Tex. 57, 182 S.W.2d 397 (1944)",
            "Othen v. Rosier, 148 Tex. 485, 226 S.W.2d 622 (1950)",
            "Drye v. Eagle Rock Ranch, Inc., 364 S.W.2d 196 (Tex. 1963)",
            "Roberts v. Friendswood Dev. Co., 886 S.W.2d 363 (Tex. App.—Houston [1st Dist.] 1994)",
        ],
        category="Implied Easements",
        subcategory="Prior Use",
        tags=["implied", "prior_use", "severance", "apparent", "continuous"],
        cross_references=["implied_easement_necessity", "express_easement_creation"],
    ),
    DoctrineCacheBlock(
        topic="implied_easement_necessity",
        summary=(
            "An easement by necessity arises when a conveyance renders a parcel "
            "landlocked with no access to a public road. The doctrine is grounded in "
            "the presumption that the parties did not intend the conveyance to deprive "
            "the grantee of access. In Texas, strict necessity is required -- "
            "convenience or preference for a particular route is insufficient. The "
            "easement lasts only as long as the necessity exists, and it terminates "
            "if alternative access becomes available."
        ),
        key_statutes=[
            "No specific Texas statute - common law doctrine",
            "Tex. Transp. Code \xA7311.001 (Public Road Access - related context)",
        ],
        elements=[
            "Common ownership of the dominant and servient tracts at some prior point",
            "Severance of the common ownership by conveyance",
            "Strict necessity: no alternative access to a public road exists",
            "The necessity arose from the severance (not from grantee's own acts)",
        ],
        defenses=[
            "Alternative access exists (even if inconvenient or expensive)",
            "No common ownership between dominant and servient tracts historically",
            "Necessity is self-created (e.g., grantee conveyed away access route)",
            "Public road frontage exists on another side of the parcel",
            "Statutory alternative (e.g., Tex. Transp. Code road petition) available",
        ],
        remedies=[
            "Declaratory judgment establishing easement by necessity",
            "Court-ordered access route across servient estate",
            "Injunction against blocking access on established route",
            "Compensation to servient owner if ordered by court",
        ],
        leading_cases=[
            "Othen v. Rosier, 148 Tex. 485, 226 S.W.2d 622 (1950)",
            "Bains v. Parker, 143 Tex. 57, 182 S.W.2d 397 (1944)",
            "Koonce v. Brite Estate, 663 S.W.2d 451 (Tex. 1984)",
        ],
        category="Implied Easements",
        subcategory="Necessity",
        tags=["implied", "necessity", "landlocked", "access", "strict_necessity"],
        cross_references=["implied_easement_prior_use", "road_easements"],
    ),

    # ------------------------------------------------------------------
    # CATEGORY: Prescriptive Easements
    # ------------------------------------------------------------------
    DoctrineCacheBlock(
        topic="prescriptive_easement",
        summary=(
            "A prescriptive easement is acquired through adverse use of another's "
            "property for the statutory limitations period. In Texas, the claimant must "
            "show use that is open, notorious, hostile, adverse, uninterrupted, "
            "continuous, and exclusive for at least 10 years under the general "
            "limitations statute. Unlike adverse possession, a prescriptive easement "
            "grants only a right to use, not fee ownership. Texas courts are cautious "
            "about prescriptive easement claims because they operate as a taking "
            "without compensation."
        ),
        key_statutes=[
            "Tex. Civ. Prac. & Rem. Code \xA716.026 (10-year Statute of Limitations)",
            "Tex. Civ. Prac. & Rem. Code \xA716.030 (25-year Adverse Possession)",
        ],
        elements=[
            "Open and notorious use (visible to the servient owner or the public)",
            "Hostile and adverse (without permission; inconsistent with owner's rights)",
            "Continuous and uninterrupted for the full statutory period (10 years in Texas)",
            "Exclusive (not shared with the general public as a public way)",
            "Use must be of a definite and specific route or area",
        ],
        defenses=[
            "Use was permissive (express or implied permission given)",
            "Statutory period not met (interruption or discontinuity)",
            "Government property (prescriptive easements generally cannot be acquired against government land)",
            "Written lease or license agreement governed the use",
            "Owner took affirmative steps to prevent use within limitations period",
            "Use was by general public (creates public road claim, not private prescriptive easement)",
        ],
        remedies=[
            "Declaratory judgment establishing prescriptive easement",
            "Injunctive relief to continue access",
            "Quiet title to confirm easement against servient estate",
        ],
        leading_cases=[
            "Brooks v. Jones, 578 S.W.2d 669 (Tex. 1979)",
            "Othen v. Rosier, 148 Tex. 485, 226 S.W.2d 622 (1950)",
            "Melvin v. Cochran, 362 S.W.2d 104 (Tex. 1962)",
            "Mack v. Landry, 22 S.W.3d 524 (Tex. App.—Houston [14th Dist.] 2000)",
        ],
        category="Prescriptive Easements",
        subcategory="Acquisition",
        tags=["prescriptive", "adverse_use", "limitations", "hostile", "continuous"],
        cross_references=["express_easement_creation", "abandonment_extinguishment"],
    ),

    # ------------------------------------------------------------------
    # CATEGORY: Appurtenant vs In Gross
    # ------------------------------------------------------------------
    DoctrineCacheBlock(
        topic="easement_appurtenant",
        summary=(
            "An easement appurtenant benefits a specific parcel of land (the dominant "
            "estate) and burdens another parcel (the servient estate). It runs with the "
            "land and transfers automatically with conveyance of the dominant estate, "
            "even if not expressly mentioned in the deed. Texas law presumes an easement "
            "is appurtenant if it benefits identifiable land, absent clear language "
            "making it personal. The burden also runs with the servient estate, binding "
            "subsequent purchasers with notice."
        ),
        key_statutes=[
            "Tex. Prop. Code \xA75.001 (Instruments Interpreted to Include All Parts)",
            "Restatement (Third) of Property: Servitudes \xA74.5",
        ],
        elements=[
            "Two distinct parcels: dominant estate (benefited) and servient estate (burdened)",
            "Easement must benefit the dominant estate in its use and enjoyment",
            "Benefit is connected to the land, not merely personal to the holder",
            "Runs with the land upon conveyance of either estate",
            "Binding on successors with constructive or actual notice",
        ],
        defenses=[
            "Easement language shows intent to create personal (in gross) right",
            "No identifiable dominant estate exists",
            "Benefit is purely personal to the named grantee",
            "Easement was abandoned by dominant estate owner",
        ],
        remedies=[
            "Declaratory judgment confirming appurtenant nature and running with the land",
            "Injunction against interference by servient estate successor",
            "Damages for interference with appurtenant easement rights",
        ],
        leading_cases=[
            "DeWitt County Elec. Coop. v. Parks, 1 S.W.3d 96 (Tex. 1999)",
            "Drye v. Eagle Rock Ranch, Inc., 364 S.W.2d 196 (Tex. 1963)",
            "Coleman v. Forister, 514 S.W.2d 899 (Tex. 1974)",
        ],
        category="Appurtenant vs In Gross",
        subcategory="Appurtenant",
        tags=["appurtenant", "runs_with_land", "dominant_estate", "servient_estate"],
        cross_references=["easement_in_gross", "express_easement_scope"],
    ),
    DoctrineCacheBlock(
        topic="easement_in_gross",
        summary=(
            "An easement in gross benefits a particular person or entity rather than "
            "a specific parcel of land. There is no dominant estate. Common examples "
            "include pipeline rights-of-way, utility easements, and railroad easements "
            "where the beneficiary is a company, not a landowner. In Texas, commercial "
            "easements in gross are generally assignable and transferable. Personal "
            "easements in gross (e.g., a right to fish) are generally not assignable "
            "and terminate on the death of the holder."
        ),
        key_statutes=[
            "No specific Texas statute - common law doctrine",
            "Restatement (Third) of Property: Servitudes \xA74.6",
        ],
        elements=[
            "Benefits a person or entity, not a specific parcel of land",
            "No dominant estate required",
            "Commercial easements in gross (pipeline, utility) are transferable",
            "Personal easements in gross are non-transferable",
            "Burden runs with servient estate, binding successors with notice",
        ],
        defenses=[
            "Attempted assignment of personal (non-commercial) easement in gross",
            "Overburdening by assignee exceeding original scope",
            "Easement holder no longer exists (corporate dissolution without successor)",
        ],
        remedies=[
            "Declaratory judgment confirming in gross nature and transferability",
            "Injunction against unauthorized assignment of personal easement in gross",
            "Damages for overburdening by assignee",
        ],
        leading_cases=[
            "Marcus Cable Assocs. v. Krohn, 90 S.W.3d 697 (Tex. 2002)",
            "Southwestern Bell Tel. Co. v. Webb, 393 S.W.2d 832 (Tex. Civ. App.—Austin 1965)",
        ],
        category="Appurtenant vs In Gross",
        subcategory="In Gross",
        tags=["in_gross", "commercial", "pipeline", "utility", "transferable"],
        cross_references=["easement_appurtenant", "pipeline_row_agreements"],
    ),

    # ------------------------------------------------------------------
    # CATEGORY: Pipeline ROW Agreements
    # ------------------------------------------------------------------
    DoctrineCacheBlock(
        topic="pipeline_row_agreements",
        summary=(
            "Pipeline right-of-way agreements are negotiated contracts between a "
            "pipeline operator and a surface landowner (or mineral lessee) granting the "
            "right to install, operate, and maintain one or more pipelines across the "
            "landowner's property. Key terms include the width of the permanent easement, "
            "temporary workspace during construction, depth of cover, cathodic protection, "
            "restoration obligations, annual rental or one-time payment, and additional "
            "line provisions. Texas RRC T-4 permits are required for intrastate pipelines."
        ),
        key_statutes=[
            "Tex. Nat. Res. Code \xA7111.001 et seq. (Pipeline Companies)",
            "Tex. Util. Code \xA7121.001 (Common Carrier Pipelines)",
            "16 TAC \xA73.70 (RRC Pipeline Safety Rules)",
            "49 CFR Parts 192, 195 (Federal Pipeline Safety - PHMSA)",
        ],
        elements=[
            "Written grant of easement for pipeline installation, operation, maintenance",
            "Defined permanent ROW width (typically 30-75 ft depending on pipe diameter)",
            "Temporary workspace for construction (additional 25-50 ft)",
            "Depth of cover specifications (min 36 inches, more at crossings)",
            "Right to install additional lines (often limited or requiring additional payment)",
            "Restoration obligation after construction (grading, topsoil replacement, reseeding)",
            "Term: perpetual or for duration of pipeline operation",
            "Consideration: one-time payment and/or annual rental per rod or per acre",
            "Cathodic protection and leak monitoring obligations",
            "Indemnification and liability provisions",
        ],
        defenses=[
            "ROW agreement expired by its own terms",
            "Pipeline abandoned (not in use for stated period)",
            "Operator exceeded scope (additional lines without authorization)",
            "Failure to maintain or restore as required",
            "Fraud or misrepresentation in procuring agreement",
        ],
        remedies=[
            "Injunctive relief to enforce or prevent ROW violations",
            "Damages for surface damage beyond agreed scope",
            "Declaratory judgment on scope of additional line rights",
            "Forfeiture for material breach of restoration obligations",
            "Condemnation proceedings if landowner refuses to negotiate (common carriers)",
        ],
        leading_cases=[
            "Texas Eastern Transmission Corp. v. Wildlife Preserves, Inc., 48 N.J. 261 (1966)",
            "Enbridge Pipelines (East Texas) LP v. Avinger Timber, LLC, 386 S.W.3d 256 (Tex. 2012)",
            "El Paso Natural Gas Co. v. Berryman, 858 S.W.2d 362 (Tex. 1993)",
        ],
        category="Pipeline ROW",
        subcategory="Agreements",
        tags=["pipeline", "row", "right_of_way", "surface", "construction", "t4_permit"],
        cross_references=["pipeline_condemnation", "surface_use_agreements", "rrc_pipeline_requirements"],
    ),
    DoctrineCacheBlock(
        topic="pipeline_row_width_standards",
        summary=(
            "Pipeline ROW widths vary by pipe diameter, product type, and operating "
            "pressure. Gathering lines (2-12 inch) typically require 30 ft permanent "
            "ROW. Transmission lines (6-42 inch) require 50 ft or more. Major trunk "
            "lines may require 75 ft or wider. Temporary workspace during construction "
            "adds 25-50 ft. Road crossings, waterway crossings, and HDD operations "
            "require additional workspace. Minimum depth of cover under 49 CFR Part 192 "
            "is 36 inches for normal soil, 48 inches under roads, and 60 inches under "
            "navigable waterways."
        ),
        key_statutes=[
            "49 CFR \xA7192.327 (Depth of Cover - Gas)",
            "49 CFR \xA7195.248 (Depth of Cover - Liquids)",
            "16 TAC \xA73.70 (RRC Pipeline Safety)",
            "TxDOT TAC Title 43, Part 1, Ch. 21 (Utility Accommodation)",
        ],
        elements=[
            "Permanent ROW width based on pipe diameter and product",
            "Temporary construction workspace (typically equal to permanent width)",
            "Depth of cover: 36 in standard, 48 in roads, 60 in waterways",
            "Additional workspace at HDD entry/exit points",
            "Road and railroad crossing permits (TxDOT Form 1082)",
            "Marker requirements: at crossings, fences, every 660 ft minimum",
            "Class location determines wall thickness and safety design factor",
        ],
        defenses=[
            "Operator using less than required depth of cover violates federal rules",
            "Temporary workspace exceeds what was granted in ROW agreement",
            "Pipeline installed outside described ROW corridor",
        ],
        remedies=[
            "PHMSA enforcement action for depth/safety violations",
            "Trespass action for pipeline outside granted ROW",
            "Damages for use of surface beyond temporary workspace provision",
        ],
        leading_cases=[
            "Enterprise Products Partners LP v. Energy Transfer Partners LP, 593 S.W.3d 732 (Tex. 2020)",
            "Denbury Green Pipeline-Texas LLC v. Texas Rice Land Partners Ltd., 510 S.W.3d 909 (Tex. 2017)",
        ],
        category="Pipeline ROW",
        subcategory="Width Standards",
        tags=["pipeline", "width", "depth_of_cover", "construction", "hdd"],
        cross_references=["pipeline_row_agreements", "txdot_crossing_permits"],
    ),
    DoctrineCacheBlock(
        topic="rrc_pipeline_requirements",
        summary=(
            "The Texas Railroad Commission regulates intrastate pipeline operations "
            "under Tex. Nat. Res. Code and 16 TAC. Pipeline operators must obtain a "
            "T-4 permit before constructing a new pipeline. Gathering systems must be "
            "registered with Form H-7. Operators must maintain cathodic protection, "
            "conduct annual leak surveys (biannual for gathering lines), perform "
            "inspections every 5 years, and follow specific abandonment procedures "
            "including purging, filling, capping, marking, and filing Form W-1X."
        ),
        key_statutes=[
            "Tex. Nat. Res. Code Ch. 111 (Pipeline Common Carriers)",
            "Tex. Nat. Res. Code Ch. 117 (Pipeline Safety)",
            "16 TAC \xA73.70 (Pipeline Safety Regulations)",
            "16 TAC \xA73.65 (Pipeline Permits and Reports)",
        ],
        elements=[
            "T-4 permit required before pipeline construction",
            "H-7 form for gathering system registration",
            "Annual cathodic protection monitoring",
            "Annual leak survey (transmission), biannual (gathering)",
            "5-year inspection interval for pipeline segments",
            "Abandonment: purge, fill with inert material, cap, mark, file W-1X",
            "Pipeline markers at crossings, fences, every 660 ft minimum",
            "Emergency response plan on file with RRC",
        ],
        defenses=[
            "Operator holds valid T-4 permit with proper route description",
            "Pipeline meets or exceeds all depth and safety requirements",
            "Cathodic protection records demonstrate compliance",
        ],
        remedies=[
            "RRC enforcement action for permit violations",
            "Civil penalties for safety regulation violations",
            "Injunction requiring proper abandonment procedures",
            "Environmental remediation orders for pipeline leaks",
        ],
        leading_cases=[
            "Railroad Commission of Texas v. Texas Citizens for a Safe Future, 336 S.W.3d 619 (Tex. 2011)",
        ],
        category="Pipeline ROW",
        subcategory="RRC Requirements",
        tags=["rrc", "pipeline", "t4_permit", "safety", "cathodic_protection", "abandonment"],
        cross_references=["pipeline_row_agreements", "pipeline_condemnation"],
    ),

    # ------------------------------------------------------------------
    # CATEGORY: Surface Use Agreements
    # ------------------------------------------------------------------
    DoctrineCacheBlock(
        topic="surface_use_agreements",
        summary=(
            "Surface use agreements (SUAs) are negotiated contracts between a mineral "
            "lessee/operator and the surface owner governing the operator's use of the "
            "surface estate for oil and gas operations. Texas follows the dominant "
            "mineral estate doctrine, granting the mineral owner/lessee implied rights "
            "to use the surface as reasonably necessary. However, the accommodation "
            "doctrine (Getty Oil v. Jones) limits this right where alternative methods "
            "exist. SUAs provide certainty by specifying permitted locations, access "
            "roads, water sources, restoration obligations, and compensation."
        ),
        key_statutes=[
            "Tex. Nat. Res. Code Ch. 52 (Surface Damage Act)",
            "Tex. Nat. Res. Code \xA791.001 et seq. (Mineral Interest Pooling Act)",
        ],
        elements=[
            "Identification of operator, surface owner, and mineral lease",
            "Permitted surface activities (pad sites, roads, tanks, pits, flowlines)",
            "Location restrictions (setbacks from homes, wells, stock tanks)",
            "Water source access rights and limitations",
            "Road construction and maintenance specifications",
            "Damage payment schedule (per acre, per well, per disturbance)",
            "Restoration and reclamation timeline and standards",
            "Insurance and indemnification requirements",
            "Environmental compliance obligations",
            "Term: duration of mineral lease operations",
        ],
        defenses=[
            "SUA not required where mineral and surface owned by same entity",
            "Operator exceeded scope of permitted activities under SUA",
            "SUA terminated upon completion of operations and restoration",
            "Force majeure relieving restoration timeline obligations",
        ],
        remedies=[
            "Damages for breach of SUA terms",
            "Specific performance of restoration obligations",
            "Injunctive relief to prevent unauthorized surface use",
            "Termination of SUA for material breach",
            "Surface damage payments under Tex. Nat. Res. Code Ch. 52",
        ],
        leading_cases=[
            "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)",
            "Merriman v. XTO Energy, Inc., 407 S.W.3d 244 (Tex. 2013)",
            "Coyote Lake Ranch, LLC v. City of Lubbock, 498 S.W.3d 53 (Tex. 2016)",
        ],
        category="Surface Use Agreements",
        subcategory="General",
        tags=["surface_use", "sua", "operator", "surface_owner", "restoration", "damage_payment"],
        cross_references=["accommodation_doctrine", "surface_damage_act", "dominant_mineral_estate"],
    ),
    DoctrineCacheBlock(
        topic="surface_damage_act",
        summary=(
            "The Texas Surface Damage Act (Tex. Nat. Res. Code Ch. 52) requires "
            "mineral lessees and operators to provide written notice to surface owners "
            "at least 30 days before commencing operations and to negotiate in good "
            "faith for surface damage compensation. If no agreement is reached, either "
            "party may file suit. Damages include actual loss to land and improvements, "
            "lost income, and restoration costs. The Act applies only when the mineral "
            "and surface estates are separately owned and the operator does not have a "
            "surface lease or other written agreement."
        ),
        key_statutes=[
            "Tex. Nat. Res. Code \xA752.001 (Definitions)",
            "Tex. Nat. Res. Code \xA752.002 (Written Notice Required)",
            "Tex. Nat. Res. Code \xA752.003 (Good Faith Negotiation)",
            "Tex. Nat. Res. Code \xA752.004 (Damages)",
            "Tex. Nat. Res. Code \xA752.0025 (Bond or Letter of Credit)",
        ],
        elements=[
            "Mineral and surface estates are separately owned",
            "Operator provides written notice 30 days before operations commence",
            "Good faith negotiation for surface damage compensation",
            "If no agreement, either party may sue in county where land is located",
            "Damages: actual loss to land, improvements, lost income, restoration costs",
            "Operator may be required to post bond or letter of credit",
            "Act does not apply where operator owns the surface or has written SUA",
        ],
        defenses=[
            "Surface and mineral owned by same entity (Act does not apply)",
            "Written surface use agreement exists (Act does not apply)",
            "Operator complied with all notice and negotiation requirements",
            "Surface owner refused good faith negotiations",
        ],
        remedies=[
            "Court-determined surface damage payment",
            "Injunction prohibiting operations until notice and negotiation complete",
            "Bond or letter of credit requirement before operations commence",
            "Attorney fees to prevailing party",
        ],
        leading_cases=[
            "FPL Farming Ltd. v. Environmental Processing Systems, L.C., 457 S.W.3d 414 (Tex. 2015)",
        ],
        category="Surface Use Agreements",
        subcategory="Surface Damage Act",
        tags=["surface_damage", "chapter_52", "notice", "good_faith", "compensation"],
        cross_references=["surface_use_agreements", "accommodation_doctrine"],
    ),

    # ------------------------------------------------------------------
    # CATEGORY: Accommodation Doctrine
    # ------------------------------------------------------------------
    DoctrineCacheBlock(
        topic="accommodation_doctrine",
        summary=(
            "The Texas accommodation doctrine, established in Getty Oil Co. v. Jones "
            "(1971), requires a mineral lessee to accommodate existing surface uses when "
            "alternative methods of mineral extraction are available and industry-standard. "
            "The doctrine balances the dominant mineral estate's implied right to use the "
            "surface against the surface owner's right to continue existing uses. The "
            "surface owner bears the burden of proof to show (1) an existing surface use, "
            "(2) the mineral operations substantially impair that use, (3) alternative "
            "methods exist that are reasonable, customary in the industry, and would "
            "permit coexistence, and (4) the alternatives would not unreasonably "
            "increase the mineral owner's costs."
        ),
        key_statutes=[
            "No specific statute - common law doctrine (judicially created)",
            "Tex. Nat. Res. Code Ch. 52 (Surface Damage Act - related but distinct)",
        ],
        elements=[
            "Existing surface use at time mineral operations commence",
            "Mineral operations substantially impair the existing surface use",
            "Alternative methods of mineral extraction exist that are industry-standard",
            "Alternatives are reasonable and would not substantially increase cost to mineral owner",
            "Alternatives would permit coexistence of both surface and mineral uses",
            "Burden of proof on the surface owner",
        ],
        defenses=[
            "No existing surface use was impaired (surface was unused or idle)",
            "No reasonable alternative methods exist for mineral extraction",
            "Alternative methods would unreasonably increase cost to mineral owner",
            "Surface use commenced after mineral operations began",
            "Surface owner consented to the mineral operations as conducted",
        ],
        remedies=[
            "Injunctive relief requiring mineral owner to use alternative methods",
            "Damages for impairment of surface use where injunction is impractical",
            "Court-ordered modifications to mineral operations plan",
        ],
        leading_cases=[
            "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971) (seminal case)",
            "Merriman v. XTO Energy, Inc., 407 S.W.3d 244 (Tex. 2013) (expansion to groundwater)",
            "Coyote Lake Ranch, LLC v. City of Lubbock, 498 S.W.3d 53 (Tex. 2016) (surface vs groundwater)",
            "Sun Oil Co. v. Whitaker, 424 S.W.2d 216 (Tex. 1968)",
        ],
        category="Accommodation Doctrine",
        subcategory="General",
        tags=["accommodation", "getty_oil", "surface_use", "mineral_estate", "alternative_methods"],
        cross_references=["dominant_mineral_estate", "surface_use_agreements", "surface_damage_act"],
    ),

    # ------------------------------------------------------------------
    # CATEGORY: Dominant/Servient Estate
    # ------------------------------------------------------------------
    DoctrineCacheBlock(
        topic="dominant_mineral_estate",
        summary=(
            "Under Texas law, the mineral estate is the dominant estate and carries "
            "an implied easement to use the surface as reasonably necessary to develop "
            "the mineral estate. This implied right includes access roads, drill sites, "
            "storage tanks, flowlines, and other facilities. However, the dominant estate "
            "right is not absolute -- it is limited to what is reasonably necessary and "
            "subject to the accommodation doctrine. The mineral owner cannot use more "
            "surface than is reasonably necessary and must exercise the right with due "
            "regard for the surface owner's rights."
        ),
        key_statutes=[
            "Common law doctrine - no specific statute",
            "Tex. Nat. Res. Code \xA752.001 et seq. (Surface Damage Act - modifications)",
        ],
        elements=[
            "Mineral estate is dominant; surface estate is servient",
            "Implied right to use surface as reasonably necessary for mineral development",
            "Includes access roads, drill pads, tank batteries, flowlines, water sources",
            "Limited to reasonable use -- cannot destroy surface or use more than necessary",
            "Subject to accommodation doctrine when alternative methods exist",
            "Does not include right to use surface for development of other tracts",
        ],
        defenses=[
            "Surface owner waived objection by written agreement or course of conduct",
            "Mineral owner's use is within scope of what is reasonably necessary",
            "No alternative method available that is industry-standard and economically viable",
        ],
        remedies=[
            "Injunction against excessive or unreasonable surface use",
            "Damages for use exceeding what is reasonably necessary",
            "Accommodation doctrine relief (alternative methods required)",
            "Surface damage payments under Ch. 52",
        ],
        leading_cases=[
            "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)",
            "Harris v. Currie, 142 Tex. 93, 176 S.W.2d 170 (1943)",
            "Warren Petroleum Corp. v. Martin, 153 Tex. 465, 271 S.W.2d 410 (1954)",
        ],
        category="Dominant/Servient Estate",
        subcategory="Mineral Dominance",
        tags=["dominant_estate", "mineral_estate", "implied_easement", "reasonable_use"],
        cross_references=["accommodation_doctrine", "surface_use_agreements"],
    ),

    # ------------------------------------------------------------------
    # CATEGORY: Road Easements
    # ------------------------------------------------------------------
    DoctrineCacheBlock(
        topic="road_easements",
        summary=(
            "Road easements in Texas oil and gas operations provide access to well "
            "sites, tank batteries, and pipeline facilities. Access roads may be "
            "established by express grant, implied easement, or prescriptive use. "
            "Oilfield roads are typically 20-40 ft wide and must accommodate heavy "
            "equipment including drilling rigs, frac trucks, and tanker vehicles. "
            "County road dedication, abandonment, and maintenance are governed by "
            "Tex. Transp. Code. Private road petitions under Ch. 311 provide a "
            "statutory alternative when access is denied."
        ),
        key_statutes=[
            "Tex. Transp. Code \xA7311.001 et seq. (Private Roads)",
            "Tex. Transp. Code \xA7251.001 et seq. (County Roads)",
            "Tex. Loc. Gov't Code \xA7240.901 (County Road Standards)",
        ],
        elements=[
            "Express grant specifying road width, route, and maintenance responsibility",
            "Implied right of access to mineral estate as reasonably necessary",
            "County road dedication or prescriptive public road establishment",
            "Width sufficient for intended traffic (20 ft minimum for oilfield access)",
            "Maintenance obligations (typically on easement holder for private roads)",
            "Gate and cattle guard provisions in agricultural areas",
        ],
        defenses=[
            "Alternative access route available (negates necessity claim)",
            "Road use exceeds scope of granted easement (heavier traffic than contemplated)",
            "Road location conflicts with surface improvements",
            "County road was properly abandoned under statutory procedure",
        ],
        remedies=[
            "Private road petition under Tex. Transp. Code Ch. 311 (with compensation)",
            "Injunction against blocking access road",
            "Damages for road damage beyond normal wear",
            "Court-ordered road relocation or upgrade",
        ],
        leading_cases=[
            "Othen v. Rosier, 148 Tex. 485, 226 S.W.2d 622 (1950)",
            "Gutierrez v. County of Zapata, 951 S.W.2d 831 (Tex. App.—San Antonio 1997)",
        ],
        category="Road Easements",
        subcategory="General",
        tags=["road", "access", "oilfield", "county_road", "private_road", "ch_311"],
        cross_references=["implied_easement_necessity", "dominant_mineral_estate"],
    ),

    # ------------------------------------------------------------------
    # CATEGORY: Utility Easements
    # ------------------------------------------------------------------
    DoctrineCacheBlock(
        topic="utility_easements",
        summary=(
            "Utility easements grant electric, water, sewer, telephone, and "
            "communication companies the right to install, operate, and maintain "
            "utility infrastructure across private property. Most utility easements "
            "are easements in gross, running to the utility company rather than a "
            "dominant estate. In Texas, utility companies with certificates of "
            "convenience and necessity have eminent domain authority under Tex. Util. "
            "Code Ch. 21. Electric cooperatives have condemnation authority under "
            "Tex. Util. Code Ch. 161."
        ),
        key_statutes=[
            "Tex. Util. Code \xA7181.001 et seq. (Electric Utility Regulation)",
            "Tex. Util. Code Ch. 21 (Condemnation Authority)",
            "Tex. Util. Code \xA7161.001 (Electric Cooperatives)",
            "Tex. Water Code \xA749.221 (Water District Eminent Domain)",
        ],
        elements=[
            "Grant of right to install, operate, and maintain utility infrastructure",
            "Typically easement in gross (benefits utility company, not specific land)",
            "Width varies by utility type (10-30 ft typical)",
            "Includes right of access for maintenance and emergency repair",
            "Often includes right to trim vegetation interfering with lines",
            "Term usually perpetual or for duration of utility service",
        ],
        defenses=[
            "Utility use exceeds scope of granted easement (e.g., adding cell tower to power easement)",
            "Utility company abandoned the easement by non-use",
            "Easement conflicts with prior recorded interest",
        ],
        remedies=[
            "Condemnation proceedings (if utility has eminent domain authority)",
            "Injunction against unauthorized expansion of utility use",
            "Damages for interference with surface use by utility operations",
            "Declaratory judgment on scope of utility easement",
        ],
        leading_cases=[
            "Marcus Cable Assocs. v. Krohn, 90 S.W.3d 697 (Tex. 2002) (cable on electric easement = overburdening)",
            "DeWitt County Elec. Coop. v. Parks, 1 S.W.3d 96 (Tex. 1999)",
        ],
        category="Utility Easements",
        subcategory="General",
        tags=["utility", "electric", "water", "sewer", "telephone", "in_gross", "condemnation"],
        cross_references=["easement_in_gross", "pipeline_condemnation"],
    ),

    # ------------------------------------------------------------------
    # CATEGORY: Pipeline Condemnation / Eminent Domain
    # ------------------------------------------------------------------
    DoctrineCacheBlock(
        topic="pipeline_condemnation",
        summary=(
            "In Texas, pipeline companies operating as common carriers have eminent "
            "domain authority to condemn private property for pipeline rights-of-way "
            "under Tex. Nat. Res. Code Ch. 111. The condemning entity must show it is "
            "a common carrier, the property is necessary for the public use, and it "
            "attempted good faith negotiation before filing. After the Denbury decision "
            "(2011/2017), a pipeline company must demonstrate it will actually serve the "
            "public and not merely transport its own product. Just compensation includes "
            "fair market value of the easement, severance damages to the remainder, "
            "and cost to cure."
        ),
        key_statutes=[
            "Tex. Nat. Res. Code \xA7111.001 et seq. (Pipeline Common Carriers)",
            "Tex. Prop. Code Ch. 21 (Eminent Domain Procedures)",
            "Tex. Gov't Code Ch. 2206 (Private Property Protection - post-Kelo reforms)",
            "U.S. Const. Amend. V (Just Compensation Clause)",
            "Tex. Const. Art. I, \xA717 (Takings Clause)",
        ],
        elements=[
            "Pipeline company is a common carrier under Tex. Nat. Res. Code \xA7111.002",
            "Property is necessary for the common carrier pipeline purpose",
            "Good faith offer to purchase (bona fide offer requirement)",
            "Landowner refused to sell or parties could not agree on terms",
            "Filing of condemnation petition in county where land is located",
            "Appointment of special commissioners to assess just compensation",
            "Just compensation: FMV of easement + severance damages + cost to cure",
            "Condemner must prove public use (Denbury test)",
        ],
        defenses=[
            "Pipeline company is not a bona fide common carrier (Denbury test)",
            "No public use demonstrated (purely private pipeline)",
            "Condemner failed to make good faith offer before filing",
            "Property not necessary for stated pipeline purpose",
            "Alternative routes available that avoid the property",
            "Condemnation would result in unreasonable burden on remainder",
        ],
        remedies=[
            "Just compensation award by special commissioners (or jury on appeal)",
            "Dismissal of condemnation if common carrier status disproved",
            "Attorney fees and costs to landowner if condemnation dismissed",
            "Damages for temporary construction damages",
        ],
        leading_cases=[
            "Denbury Green Pipeline-Texas LLC v. Texas Rice Land Partners Ltd., 510 S.W.3d 909 (Tex. 2017)",
            "Texas Rice Land Partners, Ltd. v. Denbury Green Pipeline-Texas, LLC, 363 S.W.3d 192 (Tex. 2012)",
            "Hubenak v. San Jacinto Gas Transmission Co., 141 S.W.3d 172 (Tex. 2004)",
            "City of Keller v. Wilson, 168 S.W.3d 802 (Tex. 2005)",
        ],
        category="Eminent Domain",
        subcategory="Pipeline Condemnation",
        tags=["condemnation", "eminent_domain", "common_carrier", "just_compensation", "denbury"],
        cross_references=["pipeline_row_agreements", "rrc_pipeline_requirements"],
    ),

    # ------------------------------------------------------------------
    # CATEGORY: Abandonment / Extinguishment
    # ------------------------------------------------------------------
    DoctrineCacheBlock(
        topic="abandonment_extinguishment",
        summary=(
            "An easement can be terminated through abandonment, merger, release, "
            "estoppel, condemnation, expiration of term, or destruction of purpose. "
            "In Texas, abandonment requires both (1) intent to abandon and (2) "
            "affirmative acts or conduct inconsistent with future use. Mere non-use, "
            "no matter how long, is insufficient to establish abandonment in Texas. "
            "Merger occurs when the dominant and servient estates come into common "
            "ownership. Extinguishment by agreement requires a written release."
        ),
        key_statutes=[
            "No specific Texas statute for easement abandonment - common law",
            "Tex. Prop. Code \xA75.021 (Written release for express easement extinguishment)",
        ],
        elements=[
            "Abandonment: intent to abandon + acts inconsistent with continued use",
            "Mere non-use alone is insufficient in Texas (no matter how long)",
            "Merger: dominant and servient estates come under common ownership",
            "Release: written instrument releasing the easement (must satisfy Statute of Frauds)",
            "Expiration: easement granted for a term of years expires by its own terms",
            "Estoppel: servient owner relies on abandonment representations to their detriment",
            "Destruction of purpose: the purpose for which easement was granted no longer exists",
            "Condemnation: government takes the easement for public use",
        ],
        defenses=[
            "Non-use alone does not constitute abandonment under Texas law",
            "Intent to abandon was equivocal or unclear",
            "Servient owner did not detrimentally rely (estoppel defense fails)",
            "Merger did not occur (e.g., equitable interest only, not fee simple)",
            "Release was not in writing (fails Statute of Frauds)",
        ],
        remedies=[
            "Declaratory judgment that easement has been abandoned/extinguished",
            "Quiet title action to clear extinguished easement from records",
            "Damages for interference if easement still valid and enforced",
            "Recording release or quit claim to remove cloud on title",
        ],
        leading_cases=[
            "Nat'l Resort Communities, Inc. v. Cain, 526 S.W.2d 510 (Tex. 1975)",
            "Humphrey-Trott Land Co. v. Andrews County, 733 S.W.2d 649 (Tex. App.—El Paso 1987)",
            "Roberts v. Friendswood Dev. Co., 886 S.W.2d 363 (Tex. App.—Houston [1st Dist.] 1994)",
        ],
        category="Abandonment/Extinguishment",
        subcategory="General",
        tags=["abandonment", "extinguishment", "merger", "release", "non_use", "intent"],
        cross_references=["express_easement_creation", "prescriptive_easement"],
    ),

    # ------------------------------------------------------------------
    # CATEGORY: Overburdening
    # ------------------------------------------------------------------
    DoctrineCacheBlock(
        topic="overburdening_doctrine",
        summary=(
            "Overburdening occurs when a dominant estate owner uses an easement in a "
            "manner that exceeds the scope of the original grant, imposing a greater "
            "burden on the servient estate than was contemplated. In Marcus Cable v. "
            "Krohn, the Texas Supreme Court held that stringing cable television lines "
            "on poles within an electric power easement constituted overburdening because "
            "cable TV was not within the scope of the original electric easement grant. "
            "The test is whether the use falls within the reasonable contemplation of "
            "the parties at the time of the grant."
        ),
        key_statutes=[
            "No specific statute - common law doctrine",
            "Restatement (Third) of Property: Servitudes \xA74.10 (persuasive)",
        ],
        elements=[
            "Easement use exceeds scope defined in the grant instrument",
            "Additional burden on servient estate beyond what was contemplated",
            "Use for benefit of non-dominant parcel (misuse by dominant owner)",
            "Unauthorized third-party use piggybacking on existing easement",
            "Physical expansion beyond granted width or location",
            "Change in character of use (e.g., foot path to vehicle road)",
        ],
        defenses=[
            "Use falls within reasonable scope of original grant language",
            "Technology evolution clause in grant permits updated methods",
            "Servient owner acquiesced to expanded use for prescriptive period",
            "Additional use is de minimis and does not increase burden",
        ],
        remedies=[
            "Injunction requiring removal of unauthorized improvements",
            "Damages for additional burden on servient estate",
            "Declaratory judgment limiting easement to original scope",
            "Negotiated amendment to expand easement scope with additional compensation",
        ],
        leading_cases=[
            "Marcus Cable Assocs. v. Krohn, 90 S.W.3d 697 (Tex. 2002) (seminal overburdening case)",
            "Coleman v. Forister, 514 S.W.2d 899 (Tex. 1974)",
            "City of Tyler v. Likes, 962 S.W.2d 489 (Tex. 1997)",
        ],
        category="Overburdening",
        subcategory="General",
        tags=["overburdening", "scope", "excess_use", "marcus_cable", "unauthorized"],
        cross_references=["express_easement_scope", "easement_in_gross"],
    ),

    # ------------------------------------------------------------------
    # CATEGORY: Scope Limitations (Vertical & Horizontal)
    # ------------------------------------------------------------------
    DoctrineCacheBlock(
        topic="vertical_horizontal_limits",
        summary=(
            "Easement scope includes both horizontal limits (the surface area or "
            "corridor width) and vertical limits (above and below the surface). A "
            "pipeline easement includes rights to a specified depth (typically 36-60 "
            "inches below surface) and may not restrict surface use above the pipeline "
            "beyond what is necessary for safety. An overhead power line easement "
            "includes vertical clearance above but the surface owner retains farming "
            "and other compatible uses below. The grant instrument should specify "
            "both horizontal and vertical parameters to avoid disputes."
        ),
        key_statutes=[
            "49 CFR \xA7192.327 (Gas Pipeline Depth of Cover)",
            "49 CFR \xA7195.248 (Liquid Pipeline Depth of Cover)",
            "NESC C2-2023 (National Electrical Safety Code - clearances)",
        ],
        elements=[
            "Horizontal limits defined by ROW width in grant instrument",
            "Vertical limits defined by depth of cover (subsurface) or clearance (overhead)",
            "Surface use above buried pipeline may be restricted for safety",
            "Subsurface use below overhead lines may be restricted for clearance",
            "Mineral rights below pipeline depth are not affected by pipeline easement",
            "Vertical drilling through pipeline easement requires coordination",
        ],
        defenses=[
            "Use does not physically conflict with the vertical or horizontal easement zone",
            "Grant instrument does not restrict use outside the defined zone",
            "Safety regulations do not prohibit the proposed use adjacent to easement",
        ],
        remedies=[
            "Injunction against encroachment into easement zone",
            "Mandatory excavation and pipeline relocation (rarely granted, very expensive)",
            "Damages for interference with pipeline or utility operations",
            "Declaratory judgment defining exact 3D limits of easement",
        ],
        leading_cases=[
            "El Paso Natural Gas Co. v. Berryman, 858 S.W.2d 362 (Tex. 1993)",
        ],
        category="Scope Limitations",
        subcategory="Vertical and Horizontal",
        tags=["vertical", "horizontal", "depth", "clearance", "3d_limits", "pipeline_depth"],
        cross_references=["pipeline_row_width_standards", "overburdening_doctrine"],
    ),

    # ------------------------------------------------------------------
    # CATEGORY: Texas Natural Resources Code Surface Provisions
    # ------------------------------------------------------------------
    DoctrineCacheBlock(
        topic="tnrc_surface_provisions",
        summary=(
            "The Texas Natural Resources Code contains several provisions governing "
            "surface use in the context of oil and gas operations. Chapter 52 (Surface "
            "Damage Act) addresses compensation to surface owners. Chapter 91 "
            "(Well Plugging and Surface Restoration) requires operators to plug wells "
            "and restore the surface upon cessation of operations. Chapter 111 "
            "(Pipeline Common Carriers) governs pipeline condemnation. Chapter 85 "
            "(Spacing and Proration) indirectly affects surface use by dictating well "
            "spacing requirements. The RRC enforces surface restoration under Statewide "
            "Rule 8 (16 TAC \xA73.8)."
        ),
        key_statutes=[
            "Tex. Nat. Res. Code Ch. 52 (Surface Damage Act)",
            "Tex. Nat. Res. Code Ch. 91 (Well Plugging and Surface Restoration)",
            "Tex. Nat. Res. Code Ch. 111 (Pipeline Common Carriers)",
            "Tex. Nat. Res. Code Ch. 85 (Spacing and Proration)",
            "16 TAC \xA73.8 (Statewide Rule 8 - Water Protection)",
            "16 TAC \xA73.14 (Statewide Rule 14 - Surface Restoration)",
        ],
        elements=[
            "Surface damage notice and compensation (Ch. 52)",
            "Well plugging obligation upon cessation of production (Ch. 91)",
            "Surface restoration to as near original condition as practicable",
            "Pipeline condemnation procedures (Ch. 111)",
            "Well spacing requirements that affect pad site locations (Ch. 85)",
            "Water protection and spill prevention (Rule 8)",
            "Financial assurance for plugging and restoration (Form P-12)",
        ],
        defenses=[
            "Operator complied with all statutory surface use requirements",
            "Surface owner consented to operations as conducted",
            "Force majeure delayed restoration within reasonable time",
        ],
        remedies=[
            "RRC enforcement action for failure to plug or restore",
            "Civil penalties for Statewide Rule violations",
            "Surface owner damages under Ch. 52",
            "State plugging fund used if operator is insolvent",
        ],
        leading_cases=[
            "FPL Farming Ltd. v. Environmental Processing Systems, L.C., 457 S.W.3d 414 (Tex. 2015)",
            "Railroad Commission of Texas v. Texas Citizens for a Safe Future, 336 S.W.3d 619 (Tex. 2011)",
        ],
        category="Texas Natural Resources Code",
        subcategory="Surface Provisions",
        tags=["tnrc", "surface", "plugging", "restoration", "rule_8", "rule_14", "ch_91"],
        cross_references=["surface_damage_act", "accommodation_doctrine", "pipeline_condemnation"],
    ),

    # ------------------------------------------------------------------
    # CATEGORY: Reasonable Use Doctrine
    # ------------------------------------------------------------------
    DoctrineCacheBlock(
        topic="reasonable_use_doctrine",
        summary=(
            "The reasonable use doctrine in Texas surface/mineral law provides that "
            "while the mineral estate is dominant and has an implied easement to use "
            "the surface, that use must be exercised with due regard for the surface "
            "owner's rights and must not exceed what is reasonably necessary. This "
            "doctrine was the predecessor to the accommodation doctrine and still "
            "provides the baseline standard for evaluating surface use disputes. "
            "Reasonableness is assessed under the totality of circumstances, including "
            "industry practices, alternative methods, and the extent of surface "
            "impairment."
        ),
        key_statutes=[
            "Common law doctrine",
        ],
        elements=[
            "Mineral owner has implied right to use surface only as reasonably necessary",
            "Must exercise with due regard for surface owner rights",
            "Cannot use more surface than reasonably necessary for operations",
            "Industry practices and customs inform the reasonableness standard",
            "Totality of circumstances evaluation",
        ],
        defenses=[
            "Mineral owner's use is within industry standards and reasonably necessary",
            "No alternative method available that would reduce surface impact",
            "Surface owner's use commenced after mineral operations began",
        ],
        remedies=[
            "Injunction against unreasonable surface use",
            "Damages for surface impairment exceeding reasonable necessity",
        ],
        leading_cases=[
            "Harris v. Currie, 142 Tex. 93, 176 S.W.2d 170 (1943)",
            "Warren Petroleum Corp. v. Martin, 153 Tex. 465, 271 S.W.2d 410 (1954)",
            "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971) (evolved into accommodation doctrine)",
        ],
        category="Reasonable Use",
        subcategory="General",
        tags=["reasonable_use", "surface", "mineral", "implied_easement", "due_regard"],
        cross_references=["accommodation_doctrine", "dominant_mineral_estate"],
    ),

    # ------------------------------------------------------------------
    # CATEGORY: Conservation Easements
    # ------------------------------------------------------------------
    DoctrineCacheBlock(
        topic="conservation_easement",
        summary=(
            "Conservation easements restrict development and use of land to protect "
            "natural, scenic, or agricultural values. In Texas, conservation easements "
            "are authorized under Tex. Nat. Res. Code Ch. 183. They must be held by a "
            "qualified organization (land trust, government agency) and are typically "
            "perpetual. Donors may receive federal income tax deductions under IRC "
            "\xA7170(h) and reduced property tax assessments. In oil and gas contexts, "
            "conservation easements may conflict with mineral development rights."
        ),
        key_statutes=[
            "Tex. Nat. Res. Code \xA7183.001 et seq. (Conservation Easement Act)",
            "IRC \xA7170(h) (Federal Tax Deduction for Conservation Easements)",
            "Tex. Tax Code \xA723.51 et seq. (Agricultural Appraisal - related)",
        ],
        elements=[
            "Written instrument creating perpetual restriction on land use",
            "Held by qualified conservation organization or government",
            "Protects natural, scenic, open space, or agricultural values",
            "Must serve a valid conservation purpose under IRC \xA7170(h)",
            "Runs with the land and binds successors",
            "May or may not reserve mineral development rights",
        ],
        defenses=[
            "Conservation easement was not properly executed or recorded",
            "Mineral rights were reserved and conservation easement cannot prohibit development",
            "Conservation purpose is no longer served (changed circumstances)",
            "Qualified organization ceased to exist without successor",
        ],
        remedies=[
            "Injunctive relief to enforce conservation restrictions",
            "Cy pres modification if original purpose cannot be achieved",
            "Tax recapture if easement violates IRC \xA7170(h) requirements",
        ],
        leading_cases=[
            "Lingle v. Chevron U.S.A. Inc., 544 U.S. 528 (2005) (regulatory taking context)",
        ],
        category="Conservation Easements",
        subcategory="General",
        tags=["conservation", "land_trust", "irc_170h", "perpetual", "restriction"],
        cross_references=["dominant_mineral_estate", "accommodation_doctrine"],
    ),

    # ------------------------------------------------------------------
    # CATEGORY: Flowage / Drainage Easements
    # ------------------------------------------------------------------
    DoctrineCacheBlock(
        topic="flowage_drainage_easement",
        summary=(
            "Flowage and drainage easements grant the right to direct or allow water "
            "to flow across another's property. In oil and gas operations, these "
            "easements are relevant for produced water disposal, stormwater management "
            "around well pads, and reservoir operations. Texas follows a modified "
            "civil law rule for surface water drainage: a landowner may not collect "
            "and channel water in a manner that damages a downstream property beyond "
            "the natural flow. Flowage easements may be express, implied, or "
            "prescriptive."
        ),
        key_statutes=[
            "Tex. Water Code \xA711.086 (Diversion of Water)",
            "Tex. Water Code \xA711.021 (State Water Rights)",
            "40 CFR \xA7122 (NPDES Permit Requirements - stormwater)",
        ],
        elements=[
            "Right to direct or allow water flow across servient property",
            "Must not exceed natural drainage patterns without easement",
            "Express flowage easement specifies volume, rate, and point of discharge",
            "Stormwater management around well pads and facility sites",
            "Produced water disposal requires separate permits (UIC, TRD)",
        ],
        defenses=[
            "Drainage follows natural flow patterns (no easement needed)",
            "Flowage easement was not recorded and holder is not in privity",
            "Water exceeds permitted volume or contains unauthorized constituents",
        ],
        remedies=[
            "Injunction against unauthorized diversion or discharge",
            "Damages for flooding or contamination of servient property",
            "Regulatory enforcement for permit violations",
        ],
        leading_cases=[
            "Kraft v. Langford, 565 S.W.2d 223 (Tex. 1978)",
        ],
        category="Flowage/Drainage",
        subcategory="General",
        tags=["flowage", "drainage", "water", "stormwater", "produced_water"],
        cross_references=["surface_use_agreements", "tnrc_surface_provisions"],
    ),

    # ------------------------------------------------------------------
    # CATEGORY: Easement Relocation
    # ------------------------------------------------------------------
    DoctrineCacheBlock(
        topic="easement_relocation",
        summary=(
            "Under traditional Texas common law, neither the dominant nor the servient "
            "estate owner may unilaterally relocate an easement without the other's "
            "consent. However, modern courts have recognized exceptions, particularly "
            "under the Restatement (Third) of Property: Servitudes \xA74.8, which "
            "allows the servient owner to relocate if (1) the relocation does not "
            "significantly lessen the utility of the easement, (2) does not increase "
            "the burdens on the dominant owner, and (3) the servient owner bears the "
            "cost. Texas has not fully adopted \xA74.8 but has moved in that direction "
            "in some contexts."
        ),
        key_statutes=[
            "Restatement (Third) of Property: Servitudes \xA74.8 (persuasive, not binding in TX)",
        ],
        elements=[
            "Traditional rule: no unilateral relocation by either party",
            "Modern trend: servient owner may relocate under narrow conditions",
            "Relocation must not significantly lessen utility to dominant estate",
            "Must not increase burdens on dominant estate",
            "Servient owner bears all costs of relocation",
            "Consent of both parties is safest approach",
        ],
        defenses=[
            "Relocation would significantly impair dominant estate's access or use",
            "Increased cost or inconvenience to dominant estate",
            "Grant instrument prohibits relocation by express terms",
        ],
        remedies=[
            "Injunction requiring restoration to original location",
            "Damages for increased cost to dominant estate from unauthorized relocation",
            "Court-ordered relocation with conditions and cost allocation",
        ],
        leading_cases=[
            "Drye v. Eagle Rock Ranch, Inc., 364 S.W.2d 196 (Tex. 1963)",
        ],
        category="Easement Relocation",
        subcategory="General",
        tags=["relocation", "unilateral", "restatement_4.8", "consent", "servient_owner"],
        cross_references=["express_easement_scope", "overburdening_doctrine"],
    ),

    # ------------------------------------------------------------------
    # CATEGORY: TxDOT Crossing Permits
    # ------------------------------------------------------------------
    DoctrineCacheBlock(
        topic="txdot_crossing_permits",
        summary=(
            "Pipeline and utility crossings of TxDOT-maintained highways require a "
            "permit under the Utility Accommodation Policy (TAC Title 43, Part 1, "
            "Chapter 21). TxDOT Form 1082 must be filed for each crossing. Minimum "
            "depth under highways is 48 inches; under railroads, 60 inches. Casing "
            "(steel or concrete) is required under highways. Horizontal directional "
            "drilling (HDD) is preferred; open-cut requires special approval for "
            "low-traffic roads. Processing takes approximately 30 days."
        ),
        key_statutes=[
            "TAC Title 43, Part 1, Ch. 21 (Utility Accommodation Policy)",
            "Tex. Transp. Code \xA7203.092 (Highway Permits)",
        ],
        elements=[
            "TxDOT Form 1082 required for each highway crossing",
            "Minimum 48 inches depth under highway surface",
            "Minimum 60 inches depth under railroad crossings",
            "Casing required (steel or concrete) under highways",
            "HDD preferred method; open-cut requires special approval",
            "15-ft encroachment setback from ROW edge",
            "Processing time approximately 30 days",
            "Annual permit renewal may be required for recurring maintenance access",
        ],
        defenses=[
            "Valid TxDOT crossing permit on file",
            "Depth and casing comply with or exceed minimums",
            "HDD method used, minimizing surface disturbance",
        ],
        remedies=[
            "TxDOT enforcement for unpermitted crossings",
            "Removal order for non-compliant installations",
            "Fines for violation of Utility Accommodation Policy",
        ],
        leading_cases=[],
        category="TxDOT Crossings",
        subcategory="Permits",
        tags=["txdot", "crossing", "form_1082", "hdd", "casing", "highway"],
        cross_references=["pipeline_row_width_standards", "rrc_pipeline_requirements"],
    ),

    # ------------------------------------------------------------------
    # CATEGORY: Easement Conflicts and Dispute Resolution
    # ------------------------------------------------------------------
    DoctrineCacheBlock(
        topic="easement_conflict_detection",
        summary=(
            "Easement conflicts arise when multiple easements burden the same property "
            "with incompatible uses, or when a proposed easement interferes with an "
            "existing one. Common conflicts include pipeline ROW crossing an existing "
            "utility easement, new road easement conflicting with conservation "
            "restriction, and multiple pipeline easements competing for limited corridor "
            "space. Resolution follows priority rules (first in time, first in right), "
            "with recorded easements taking priority over unrecorded ones among BFPs. "
            "Practical resolution often involves negotiated crossing agreements."
        ),
        key_statutes=[
            "Tex. Prop. Code \xA713.001 (Recording Priority)",
            "Tex. Prop. Code \xA713.002 (Constructive Notice)",
        ],
        elements=[
            "Identify all easements burdening the property from deed records",
            "Map easement corridors with width, depth, and use restrictions",
            "Check for physical overlap or proximity conflicts",
            "Evaluate whether uses are compatible or mutually exclusive",
            "Priority: recorded first in time has priority over later recorded",
            "Unrecorded easement loses to BFP without notice",
            "Crossing agreements between easement holders for shared corridors",
        ],
        defenses=[
            "Later easement holder had actual or constructive notice of prior easement",
            "Easements are physically compatible (different depths, non-interfering uses)",
            "Crossing agreement governs the relationship between conflicting easements",
        ],
        remedies=[
            "Declaratory judgment on priority and scope of competing easements",
            "Injunction against interference with prior easement",
            "Court-ordered crossing agreement or relocation",
            "Damages for interference with established easement rights",
        ],
        leading_cases=[
            "Cosgrove v. Cade, 468 S.W.3d 32 (Tex. 2015)",
        ],
        category="Easement Conflicts",
        subcategory="Detection and Resolution",
        tags=["conflict", "priority", "crossing_agreement", "overlap", "recording"],
        cross_references=["express_easement_recording", "pipeline_row_agreements"],
    ),

    # ------------------------------------------------------------------
    # CATEGORY: Eminent Domain Valuation
    # ------------------------------------------------------------------
    DoctrineCacheBlock(
        topic="eminent_domain_valuation",
        summary=(
            "Just compensation in eminent domain proceedings for pipeline ROW and "
            "utility easements requires payment of fair market value of the property "
            "taken, plus severance damages to the remainder. Texas uses the before "
            "and after method: the difference in market value of the whole tract "
            "immediately before and after the taking. Special commissioners make the "
            "initial award; either party may appeal to the county court for a jury "
            "trial. Cost to cure (measures the owner can take to reduce severance "
            "damages) may offset severance damages."
        ),
        key_statutes=[
            "Tex. Prop. Code \xA721.042 (Just Compensation)",
            "Tex. Prop. Code \xA721.012 (Special Commissioners)",
            "Tex. Prop. Code \xA721.018 (Objections and Trial)",
            "U.S. Const. Amend. V",
            "Tex. Const. Art. I, \xA717",
        ],
        elements=[
            "Fair market value of the easement strip taken",
            "Severance damages to the remainder of the tract",
            "Cost to cure (if it reduces severance damages below its cost)",
            "Special benefits may offset severance damages (not value of land taken)",
            "Temporary construction damages (separate from permanent taking)",
            "Before and after method is the standard in Texas",
            "Highest and best use of the property is considered",
        ],
        defenses=[
            "Condemner's appraised value is supported by comparable sales",
            "Special benefits to remainder offset claimed severance damages",
            "Cost to cure is less than severance damages and should be deducted",
        ],
        remedies=[
            "Special commissioners' award (initial determination)",
            "Jury trial on appeal to county court",
            "Expert testimony on valuation (appraiser, engineer, economist)",
            "Attorney fees to landowner if final award exceeds initial offer by threshold",
        ],
        leading_cases=[
            "State v. Heal, 917 S.W.2d 6 (Tex. 1996)",
            "City of Keller v. Wilson, 168 S.W.3d 802 (Tex. 2005)",
            "Hubenak v. San Jacinto Gas Transmission Co., 141 S.W.3d 172 (Tex. 2004)",
        ],
        category="Eminent Domain",
        subcategory="Valuation",
        tags=["valuation", "just_compensation", "severance_damages", "cost_to_cure", "before_after"],
        cross_references=["pipeline_condemnation"],
    ),

    # ------------------------------------------------------------------
    # CATEGORY: Easement Assignments and Successors
    # ------------------------------------------------------------------
    DoctrineCacheBlock(
        topic="easement_assignment",
        summary=(
            "The assignability of an easement depends on its type. Appurtenant "
            "easements transfer automatically with the dominant estate. Commercial "
            "easements in gross (pipeline, utility) are generally assignable. "
            "Personal easements in gross are not assignable and terminate with the "
            "holder. Assignments of pipeline ROW are common in the oil and gas "
            "industry when pipelines change operators. The assignment should be "
            "recorded and the servient owner notified, though notification is "
            "generally not a condition of validity."
        ),
        key_statutes=[
            "Tex. Prop. Code \xA75.001 (Conveyance Includes All Parts)",
            "Restatement (Third) of Property: Servitudes \xA74.6 (persuasive)",
        ],
        elements=[
            "Appurtenant easements transfer automatically with dominant estate deed",
            "Commercial easements in gross are assignable by written instrument",
            "Personal easements in gross are non-assignable and non-inheritable",
            "Assignment should be recorded in county deed records",
            "Assignee takes subject to the same scope and limitations as assignor",
            "Anti-assignment clause in grant instrument may restrict transfer",
        ],
        defenses=[
            "Attempted assignment of personal (non-commercial) easement in gross",
            "Anti-assignment clause in original grant prohibits transfer",
            "Assignee attempts to expand scope beyond original grant",
        ],
        remedies=[
            "Declaratory judgment confirming validity of assignment",
            "Injunction against assignee exceeding original easement scope",
            "Quiet title to clear invalid assignment from records",
        ],
        leading_cases=[
            "Marcus Cable Assocs. v. Krohn, 90 S.W.3d 697 (Tex. 2002)",
        ],
        category="Easement Assignments",
        subcategory="Successors",
        tags=["assignment", "transfer", "successor", "appurtenant", "in_gross"],
        cross_references=["easement_appurtenant", "easement_in_gross"],
    ),
]


# ============================================================================
# MODULE-LEVEL FUNCTIONS
# ============================================================================

_CACHE_INDEX: Optional[DoctrineCacheIndex] = None


def build_doctrine_cache() -> DoctrineCacheIndex:
    """Build and return the global doctrine cache index."""
    global _CACHE_INDEX
    _CACHE_INDEX = DoctrineCacheIndex()
    _CACHE_INDEX.build(DOCTRINE_BLOCKS)
    logger.info(f"LM14 doctrine cache built: {_CACHE_INDEX.size} blocks")
    return _CACHE_INDEX


def get_cache_index() -> DoctrineCacheIndex:
    """Return the global cache index, building it if necessary."""
    global _CACHE_INDEX
    if _CACHE_INDEX is None:
        return build_doctrine_cache()
    return _CACHE_INDEX


def get_doctrine_block(topic: str) -> Optional[DoctrineCacheBlock]:
    """Retrieve a single doctrine block by topic name."""
    return get_cache_index().get_by_topic(topic)


def search_doctrines(query: str, top_k: int = 10) -> List[DoctrineCacheBlock]:
    """Free-text search over all doctrine blocks."""
    return get_cache_index().search(query, top_k)


def get_all_doctrine_topics() -> List[str]:
    """Return a sorted list of all doctrine topic names."""
    return get_cache_index().topics


def get_all_doctrine_categories() -> List[str]:
    """Return a sorted list of all doctrine category names."""
    return get_cache_index().categories


def get_coverage_map() -> Dict[str, Any]:
    """Return coverage statistics per doctrine category."""
    return get_cache_index().coverage_map()


def get_blocks_by_category(category: str) -> List[DoctrineCacheBlock]:
    """Retrieve all doctrine blocks in a given category."""
    return get_cache_index().get_by_category(category)


def get_blocks_by_tag(tag: str) -> List[DoctrineCacheBlock]:
    """Retrieve all doctrine blocks with a given tag."""
    return get_cache_index().get_by_tag(tag)


def export_all_doctrines() -> List[Dict[str, Any]]:
    """Export all doctrine blocks as serializable dictionaries."""
    return get_cache_index().export_all()


def doctrine_cache_health() -> Dict[str, Any]:
    """Return health metrics for the doctrine cache."""
    idx = get_cache_index()
    stale = idx.get_stale_blocks()
    return {
        "total_blocks": idx.size,
        "total_categories": len(idx.categories),
        "total_topics": len(idx.topics),
        "stale_blocks": len(stale),
        "stale_topics": [b.topic for b in stale],
        "build_time_sec": round(idx._build_time, 4),
        "coverage": idx.coverage_map(),
    }
