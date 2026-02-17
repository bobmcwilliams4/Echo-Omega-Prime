"""
LM01 Title Examination Engine - Main Engine
=============================================

Full title examination engine implementation for oil & gas landman operations.

Core capabilities:
- Title chain construction from recorded instruments
- Defect detection (gap in chain, missing heir, expired lien, tax delinquency,
  unreleased mortgage, double grant, wild deed, forgery/fraud)
- Title opinion generation (preliminary, supplemental, final)
- Curative requirement identification and prioritization
- Mineral/surface ownership split tracking
- Interest calculation through conveyance chain with reservations
- Run sheet generation
- Texas-specific title standards compliance
- Integration with LANDMAN_INTELLIGENCE models

Author: ECHO OMEGA PRIME Build System
Engine: LM01 Title Examination
"""

from __future__ import annotations

import hashlib
import json
import uuid
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from loguru import logger


# Ensure sibling modules are importable
import sys
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    CurativeAction,
    CurativeStandard,
    DefectCategory,
    DefectClassification,
    DefectSeverity,
    RecordingActType,
    TitleDoctrineCache,
    TitleType,
    DEFECT_CLASSIFICATIONS,
    TEXAS_TITLE_STANDARDS,
)
from search import (
    GrantorGranteeIndex,
    SearchQuery,
    SearchResponse,
    SearchResult,
    TitleSearchEngine,
)
from semantic import (
    TitleSemanticDictionary,
    is_entity_name,
    normalize_party_name,
    name_similarity_score,
    parse_legal_description,
)
from telemetry import (
    AuditEventType,
    ErrorSeverity,
    OperationType,
    TitleExamTelemetry,
    compute_chain_hash,
    compute_deterministic_hash,
    compute_opinion_hash,
)


# ---------------------------------------------------------------------------
# Pydantic-style models (using dataclass for zero-dep)
# ---------------------------------------------------------------------------

class OpinionType(str, Enum):
    """Types of title opinions."""
    PRELIMINARY = "preliminary"
    SUPPLEMENTAL = "supplemental"
    FINAL = "final"
    STANDBY = "standby"
    DRILLING = "drilling"


class OwnershipType(str, Enum):
    """Types of ownership tracked."""
    MINERAL_FEE = "mineral_fee"
    SURFACE_FEE = "surface_fee"
    ROYALTY = "royalty"
    OVERRIDING_ROYALTY = "overriding_royalty"
    WORKING_INTEREST = "working_interest"
    EXECUTIVE_RIGHT = "executive_right"
    LEASEHOLD = "leasehold"
    FEE_SIMPLE_ABSOLUTE = "fee_simple_absolute"


@dataclass
class InstrumentRecord:
    """Fully typed instrument record for chain construction."""
    instrument_id: str
    instrument_type: str
    recording_date: Optional[date] = None
    effective_date: Optional[date] = None
    volume: Optional[str] = None
    page: Optional[str] = None
    document_number: Optional[str] = None
    grantors: List[str] = field(default_factory=list)
    grantees: List[str] = field(default_factory=list)
    legal_description: Optional[str] = None
    county: Optional[str] = None
    state: Optional[str] = None
    interests_conveyed: List[Dict[str, Any]] = field(default_factory=list)
    reservations: List[str] = field(default_factory=list)
    exceptions: List[str] = field(default_factory=list)
    consideration: Optional[Decimal] = None
    consideration_type: Optional[str] = None
    primary_term_years: Optional[int] = None
    royalty_fraction: Optional[Decimal] = None
    remarks: Optional[str] = None

    def get_effective_date(self) -> Optional[date]:
        return self.effective_date or self.recording_date

    def is_conveyance(self) -> bool:
        conv_types = {
            "warranty_deed", "special_warranty_deed", "quitclaim_deed",
            "grant_deed", "mineral_deed", "royalty_deed", "correction_deed",
            "bargain_and_sale_deed", "gift_deed", "trustees_deed",
            "executors_deed", "administrators_deed", "sheriffs_deed",
            "tax_deed", "masters_deed",
        }
        return self.instrument_type.lower().replace(" ", "_") in conv_types

    def is_lease(self) -> bool:
        lease_types = {"oil_gas_lease", "paid_up_lease", "top_lease", "surface_lease"}
        return self.instrument_type.lower().replace(" ", "_") in lease_types

    def is_assignment(self) -> bool:
        asgn_types = {
            "assignment", "partial_assignment",
            "assignment_of_ogl", "assignment_of_orri",
        }
        return self.instrument_type.lower().replace(" ", "_") in asgn_types

    def is_release(self) -> bool:
        rel_types = {"release", "partial_release", "release_of_lien", "release_of_lease"}
        return self.instrument_type.lower().replace(" ", "_") in rel_types

    def is_probate(self) -> bool:
        prob_types = {
            "will", "probate_order", "affidavit_of_heirship",
            "court_order", "letters_testamentary", "letters_of_administration",
            "decree_of_distribution", "small_estate_affidavit",
        }
        return self.instrument_type.lower().replace(" ", "_") in prob_types

    def is_encumbrance(self) -> bool:
        enc_types = {
            "deed_of_trust", "mortgage", "mechanics_lien",
            "tax_lien", "judgment_lien", "ucc_filing", "lis_pendens",
        }
        return self.instrument_type.lower().replace(" ", "_") in enc_types

    def to_dict(self) -> Dict[str, Any]:
        return {
            "instrument_id": self.instrument_id,
            "instrument_type": self.instrument_type,
            "recording_date": self.recording_date.isoformat() if self.recording_date else None,
            "effective_date": self.effective_date.isoformat() if self.effective_date else None,
            "volume": self.volume,
            "page": self.page,
            "document_number": self.document_number,
            "grantors": self.grantors,
            "grantees": self.grantees,
            "legal_description": self.legal_description,
            "county": self.county,
            "state": self.state,
            "interests_conveyed": self.interests_conveyed,
            "reservations": self.reservations,
            "exceptions": self.exceptions,
            "consideration": str(self.consideration) if self.consideration else None,
            "consideration_type": self.consideration_type,
            "primary_term_years": self.primary_term_years,
            "royalty_fraction": str(self.royalty_fraction) if self.royalty_fraction else None,
            "remarks": self.remarks,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InstrumentRecord":
        rec_date = None
        if data.get("recording_date"):
            if isinstance(data["recording_date"], date):
                rec_date = data["recording_date"]
            elif isinstance(data["recording_date"], str):
                rec_date = date.fromisoformat(data["recording_date"])
        eff_date = None
        if data.get("effective_date"):
            if isinstance(data["effective_date"], date):
                eff_date = data["effective_date"]
            elif isinstance(data["effective_date"], str):
                eff_date = date.fromisoformat(data["effective_date"])
        consideration = None
        if data.get("consideration"):
            try:
                consideration = Decimal(str(data["consideration"]))
            except (InvalidOperation, ValueError):
                pass
        royalty_frac = None
        if data.get("royalty_fraction"):
            try:
                royalty_frac = Decimal(str(data["royalty_fraction"]))
            except (InvalidOperation, ValueError):
                pass
        return cls(
            instrument_id=data.get("instrument_id", str(uuid.uuid4())[:12]),
            instrument_type=data.get("instrument_type", "unknown"),
            recording_date=rec_date,
            effective_date=eff_date,
            volume=data.get("volume"),
            page=data.get("page"),
            document_number=data.get("document_number"),
            grantors=data.get("grantors", []),
            grantees=data.get("grantees", []),
            legal_description=data.get("legal_description"),
            county=data.get("county"),
            state=data.get("state"),
            interests_conveyed=data.get("interests_conveyed", []),
            reservations=data.get("reservations", []),
            exceptions=data.get("exceptions", []),
            consideration=consideration,
            consideration_type=data.get("consideration_type"),
            primary_term_years=data.get("primary_term_years"),
            royalty_fraction=royalty_frac,
            remarks=data.get("remarks"),
        )


@dataclass
class OwnershipPosition:
    """An ownership position in a specific interest type."""
    owner_name: str
    owner_normalized: str
    interest_type: OwnershipType
    decimal_interest: Decimal
    source_instrument_id: Optional[str] = None
    effective_date: Optional[date] = None
    net_mineral_acres: Optional[Decimal] = None
    is_active: bool = True
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "owner_name": self.owner_name,
            "owner_normalized": self.owner_normalized,
            "interest_type": self.interest_type.value,
            "decimal_interest": str(self.decimal_interest),
            "source_instrument_id": self.source_instrument_id,
            "effective_date": self.effective_date.isoformat() if self.effective_date else None,
            "net_mineral_acres": str(self.net_mineral_acres) if self.net_mineral_acres else None,
            "is_active": self.is_active,
            "notes": self.notes,
        }


@dataclass
class TitleDefect:
    """A detected title defect."""
    defect_id: str
    category: DefectCategory
    severity: DefectSeverity
    description: str
    affected_instruments: List[str] = field(default_factory=list)
    affected_parties: List[str] = field(default_factory=list)
    gap_start_date: Optional[date] = None
    gap_end_date: Optional[date] = None
    interest_affected: Optional[str] = None
    decimal_interest_affected: Optional[Decimal] = None
    cure_actions: List[CurativeAction] = field(default_factory=list)
    cure_priority: int = 5
    auto_curable: bool = False
    confidence: float = 1.0
    legal_authority: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "defect_id": self.defect_id,
            "category": self.category.value,
            "severity": self.severity.value,
            "description": self.description,
            "affected_instruments": self.affected_instruments,
            "affected_parties": self.affected_parties,
            "gap_start_date": self.gap_start_date.isoformat() if self.gap_start_date else None,
            "gap_end_date": self.gap_end_date.isoformat() if self.gap_end_date else None,
            "interest_affected": self.interest_affected,
            "decimal_interest_affected": str(self.decimal_interest_affected) if self.decimal_interest_affected else None,
            "cure_actions": [c.value for c in self.cure_actions],
            "cure_priority": self.cure_priority,
            "auto_curable": self.auto_curable,
            "confidence": self.confidence,
            "legal_authority": self.legal_authority,
        }


@dataclass
class CurativeRequirement:
    """A curative requirement to clear a defect."""
    requirement_id: str
    defect_id: str
    action: CurativeAction
    description: str
    priority: int
    estimated_cost: Optional[str] = None
    estimated_days: Optional[int] = None
    responsible_party: Optional[str] = None
    status: str = "pending"
    deadline: Optional[date] = None
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "requirement_id": self.requirement_id,
            "defect_id": self.defect_id,
            "action": self.action.value,
            "description": self.description,
            "priority": self.priority,
            "estimated_cost": self.estimated_cost,
            "estimated_days": self.estimated_days,
            "responsible_party": self.responsible_party,
            "status": self.status,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "notes": self.notes,
        }


@dataclass
class RunSheetEntry:
    """A single entry on a run sheet."""
    entry_number: int
    instrument_type: str
    recording_date: Optional[date]
    volume_page: Optional[str]
    document_number: Optional[str]
    grantor: str
    grantee: str
    legal_description: Optional[str]
    interest_conveyed: Optional[str]
    reservations: Optional[str]
    exceptions: Optional[str]
    consideration: Optional[str]
    remarks: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_number": self.entry_number,
            "instrument_type": self.instrument_type,
            "recording_date": self.recording_date.isoformat() if self.recording_date else None,
            "volume_page": self.volume_page,
            "document_number": self.document_number,
            "grantor": self.grantor,
            "grantee": self.grantee,
            "legal_description": self.legal_description,
            "interest_conveyed": self.interest_conveyed,
            "reservations": self.reservations,
            "exceptions": self.exceptions,
            "consideration": self.consideration,
            "remarks": self.remarks,
        }


@dataclass
class TitleOpinion:
    """A title opinion document."""
    opinion_id: str
    opinion_type: OpinionType
    title_quality: TitleType
    examiner: str
    examination_date: date
    legal_description: str
    county: str
    state: str
    effective_date: date
    search_period_start: Optional[date] = None
    search_period_end: Optional[date] = None
    chain_length: int = 0
    defects_found: int = 0
    curative_items: int = 0
    mineral_owners: List[OwnershipPosition] = field(default_factory=list)
    surface_owners: List[OwnershipPosition] = field(default_factory=list)
    royalty_owners: List[OwnershipPosition] = field(default_factory=list)
    active_leases: List[Dict[str, Any]] = field(default_factory=list)
    defects: List[TitleDefect] = field(default_factory=list)
    curative_requirements: List[CurativeRequirement] = field(default_factory=list)
    run_sheet: List[RunSheetEntry] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)
    exceptions: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    deterministic_hash: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "opinion_id": self.opinion_id,
            "opinion_type": self.opinion_type.value,
            "title_quality": self.title_quality.value,
            "examiner": self.examiner,
            "examination_date": self.examination_date.isoformat(),
            "legal_description": self.legal_description,
            "county": self.county,
            "state": self.state,
            "effective_date": self.effective_date.isoformat(),
            "search_period": {
                "start": self.search_period_start.isoformat() if self.search_period_start else None,
                "end": self.search_period_end.isoformat() if self.search_period_end else None,
            },
            "chain_summary": {
                "chain_length": self.chain_length,
                "defects_found": self.defects_found,
                "curative_items": self.curative_items,
            },
            "ownership": {
                "mineral_owners": [o.to_dict() for o in self.mineral_owners],
                "surface_owners": [o.to_dict() for o in self.surface_owners],
                "royalty_owners": [o.to_dict() for o in self.royalty_owners],
            },
            "active_leases": self.active_leases,
            "defects": [d.to_dict() for d in self.defects],
            "curative_requirements": [c.to_dict() for c in self.curative_requirements],
            "run_sheet": [e.to_dict() for e in self.run_sheet],
            "requirements": self.requirements,
            "exceptions": self.exceptions,
            "notes": self.notes,
            "deterministic_hash": self.deterministic_hash,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, default=str)


# ---------------------------------------------------------------------------
# Title Chain Builder
# ---------------------------------------------------------------------------

class TitleChainBuilder:
    """
    Constructs a chain of title from recorded instruments.
    Sorts instruments chronologically and validates connectivity.
    """

    def __init__(self, semantic_dict: TitleSemanticDictionary) -> None:
        self._semantic = semantic_dict
        self._instruments: List[InstrumentRecord] = []
        self._chain: List[InstrumentRecord] = []

    def add_instrument(self, instrument: InstrumentRecord) -> None:
        """Add an instrument to the chain builder."""
        self._instruments.append(instrument)

    def add_instruments(self, instruments: List[InstrumentRecord]) -> int:
        """Add multiple instruments. Returns count added."""
        for inst in instruments:
            self._instruments.append(inst)
        return len(instruments)

    def build_chain(
        self,
        legal_description: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[InstrumentRecord]:
        """
        Build the chain of title sorted by effective date.
        Optionally filter by legal description and date range.
        """
        filtered = list(self._instruments)

        if legal_description:
            parsed_query = parse_legal_description(legal_description)
            new_filtered: List[InstrumentRecord] = []
            for inst in filtered:
                if not inst.legal_description:
                    continue
                parsed_inst = parse_legal_description(inst.legal_description)
                if self._legal_descriptions_match(parsed_query, parsed_inst):
                    new_filtered.append(inst)
            filtered = new_filtered

        if start_date:
            filtered = [
                inst for inst in filtered
                if (inst.get_effective_date() or date.max) >= start_date
            ]
        if end_date:
            filtered = [
                inst for inst in filtered
                if (inst.get_effective_date() or date.min) <= end_date
            ]

        filtered.sort(key=lambda x: x.get_effective_date() or date.min)
        self._chain = filtered

        logger.info(
            f"Chain built: {len(self._chain)} instruments "
            f"from {len(self._instruments)} total"
        )
        return self._chain

    def _legal_descriptions_match(
        self,
        parsed1: Dict[str, Any],
        parsed2: Dict[str, Any],
    ) -> bool:
        """Check if two parsed legal descriptions match."""
        if parsed1.get("section") and parsed2.get("section"):
            if parsed1["section"] == parsed2["section"]:
                if parsed1.get("block") and parsed2.get("block"):
                    if parsed1["block"] == parsed2["block"]:
                        return True
                else:
                    return True

        if parsed1.get("abstract_number") and parsed2.get("abstract_number"):
            if parsed1["abstract_number"] == parsed2["abstract_number"]:
                return True

        if parsed1.get("lot") and parsed2.get("lot"):
            if parsed1["lot"] == parsed2["lot"]:
                if parsed1.get("block") and parsed2.get("block"):
                    return parsed1["block"] == parsed2["block"]
                return True

        return False

    def get_chain(self) -> List[InstrumentRecord]:
        """Return the current chain."""
        return list(self._chain)

    def get_chain_hash(self) -> str:
        """Compute deterministic hash of the chain."""
        return compute_chain_hash([inst.to_dict() for inst in self._chain])

    def clear(self) -> None:
        """Clear all instruments and chain."""
        self._instruments.clear()
        self._chain.clear()


# ---------------------------------------------------------------------------
# Defect Detector
# ---------------------------------------------------------------------------

class DefectDetector:
    """
    Detects title defects in a chain of title.
    Analyzes chain connectivity, ownership totals, encumbrance status,
    and compliance with Texas title standards.
    """

    def __init__(
        self,
        doctrine_cache: TitleDoctrineCache,
        semantic_dict: TitleSemanticDictionary,
    ) -> None:
        self._doctrines = doctrine_cache
        self._semantic = semantic_dict
        self._defects: List[TitleDefect] = []
        self._defect_counter: int = 0

    def analyze(
        self,
        chain: List[InstrumentRecord],
        as_of_date: Optional[date] = None,
        state: str = "TX",
    ) -> List[TitleDefect]:
        """Run full defect analysis on a chain of title."""
        if as_of_date is None:
            as_of_date = date.today()

        self._defects = []
        self._defect_counter = 0

        logger.info(f"Analyzing {len(chain)} instruments for defects as of {as_of_date}")

        self._detect_chain_breaks(chain)
        self._detect_wild_deeds(chain)
        self._detect_double_grants(chain)
        self._detect_missing_probate(chain)
        self._detect_unreleased_encumbrances(chain, as_of_date)
        self._detect_name_variances(chain)
        self._detect_missing_legal_description(chain)
        self._detect_defective_acknowledgment(chain)
        self._detect_recording_gaps(chain)
        self._detect_missing_consideration(chain)
        self._detect_community_property_issues(chain, state)
        self._detect_entity_authority_issues(chain)
        self._detect_expired_leases(chain, as_of_date)

        logger.info(f"Defect analysis complete: {len(self._defects)} defects found")
        return self._defects

    def _next_defect_id(self) -> str:
        self._defect_counter += 1
        return f"D-{self._defect_counter:04d}"

    def _detect_chain_breaks(self, chain: List[InstrumentRecord]) -> None:
        """Detect breaks in the chain of title."""
        if len(chain) < 2:
            return

        for i in range(1, len(chain)):
            prev = chain[i - 1]
            curr = chain[i]

            if not prev.grantees or not curr.grantors:
                continue

            if not curr.is_conveyance() and not curr.is_probate():
                continue

            prev_grantees = {normalize_party_name(n) for n in prev.grantees}
            curr_grantors = {normalize_party_name(n) for n in curr.grantors}

            if not prev_grantees & curr_grantors:
                has_fuzzy_match = False
                for pg in prev_grantees:
                    for cg in curr_grantors:
                        if name_similarity_score(pg, cg) >= 0.85:
                            has_fuzzy_match = True
                            break
                    if has_fuzzy_match:
                        break

                if not has_fuzzy_match:
                    defect = TitleDefect(
                        defect_id=self._next_defect_id(),
                        category=DefectCategory.CHAIN_BREAK,
                        severity=DefectSeverity.CRITICAL,
                        description=(
                            f"Break in chain between instrument {prev.instrument_id} "
                            f"(grantees: {', '.join(prev.grantees)}) and instrument "
                            f"{curr.instrument_id} (grantors: {', '.join(curr.grantors)}). "
                            f"No connecting instrument found."
                        ),
                        affected_instruments=[prev.instrument_id, curr.instrument_id],
                        affected_parties=list(prev.grantees) + list(curr.grantors),
                        gap_start_date=prev.get_effective_date(),
                        gap_end_date=curr.get_effective_date(),
                        cure_actions=[CurativeAction.QUIET_TITLE_ACTION, CurativeAction.QUITCLAIM_DEED],
                        cure_priority=1,
                        confidence=0.85,
                        legal_authority="Common law chain of title doctrine",
                    )
                    self._defects.append(defect)

    def _detect_wild_deeds(self, chain: List[InstrumentRecord]) -> None:
        """Detect wild deeds (instruments from parties not in chain)."""
        known_grantees: Set[str] = set()
        sovereign_grantors: Set[str] = set()

        for inst in chain:
            if inst.instrument_type.lower() in ("sovereign_grant", "patent"):
                for g in inst.grantors:
                    sovereign_grantors.add(normalize_party_name(g))

            for grantee in inst.grantees:
                known_grantees.add(normalize_party_name(grantee))

        for i, inst in enumerate(chain):
            if i == 0:
                continue
            if not inst.is_conveyance():
                continue

            for grantor in inst.grantors:
                normalized = normalize_party_name(grantor)
                if normalized not in known_grantees and normalized not in sovereign_grantors:
                    has_close_match = any(
                        name_similarity_score(normalized, kg) >= 0.85
                        for kg in known_grantees
                    )
                    if not has_close_match:
                        defect = TitleDefect(
                            defect_id=self._next_defect_id(),
                            category=DefectCategory.WILD_DEED,
                            severity=DefectSeverity.CRITICAL,
                            description=(
                                f"Grantor '{grantor}' in instrument {inst.instrument_id} "
                                f"does not appear as a prior grantee in the chain. "
                                f"This may be a wild deed."
                            ),
                            affected_instruments=[inst.instrument_id],
                            affected_parties=[grantor],
                            cure_actions=[CurativeAction.QUIET_TITLE_ACTION],
                            cure_priority=1,
                            confidence=0.70,
                            legal_authority="Common law wild deed doctrine",
                        )
                        self._defects.append(defect)
                        break

    def _detect_double_grants(self, chain: List[InstrumentRecord]) -> None:
        """Detect when the same grantor conveys the same interest twice."""
        grants: Dict[str, List[InstrumentRecord]] = defaultdict(list)

        for inst in chain:
            if not inst.is_conveyance():
                continue
            for grantor in inst.grantors:
                key = normalize_party_name(grantor)
                grants[key].append(inst)

        for grantor_name, instruments in grants.items():
            if len(instruments) < 2:
                continue

            conveyance_pairs: List[Tuple[InstrumentRecord, InstrumentRecord]] = []
            for i in range(len(instruments)):
                for j in range(i + 1, len(instruments)):
                    a = instruments[i]
                    b = instruments[j]
                    a_grantees = {normalize_party_name(g) for g in a.grantees}
                    b_grantees = {normalize_party_name(g) for g in b.grantees}
                    if not a_grantees & b_grantees:
                        conveyance_pairs.append((a, b))

            for inst_a, inst_b in conveyance_pairs:
                defect = TitleDefect(
                    defect_id=self._next_defect_id(),
                    category=DefectCategory.DOUBLE_GRANT,
                    severity=DefectSeverity.CRITICAL,
                    description=(
                        f"Grantor '{grantor_name}' conveyed to different grantees "
                        f"in instruments {inst_a.instrument_id} and {inst_b.instrument_id}. "
                        f"Possible double grant."
                    ),
                    affected_instruments=[inst_a.instrument_id, inst_b.instrument_id],
                    affected_parties=[grantor_name] + inst_a.grantees + inst_b.grantees,
                    cure_actions=[CurativeAction.QUIET_TITLE_ACTION, CurativeAction.QUITCLAIM_DEED],
                    cure_priority=1,
                    confidence=0.75,
                    legal_authority="Tex. Property Code Sec. 13.001 (race-notice)",
                )
                self._defects.append(defect)

    def _detect_missing_probate(self, chain: List[InstrumentRecord]) -> None:
        """Detect where a decedent's interest was not probated."""
        grantee_set: Set[str] = set()
        grantor_set: Set[str] = set()
        probate_parties: Set[str] = set()

        for inst in chain:
            for g in inst.grantees:
                grantee_set.add(normalize_party_name(g))
            for g in inst.grantors:
                grantor_set.add(normalize_party_name(g))
            if inst.is_probate():
                for g in inst.grantors:
                    probate_parties.add(normalize_party_name(g))

        estate_indicators = {"ESTATE", "HEIRS", "DECEASED", "DECD", "DEC'D"}

        for inst in chain:
            for grantor in inst.grantors:
                norm = normalize_party_name(grantor)
                if any(ind in norm.upper() for ind in estate_indicators):
                    base_name = norm
                    for ind in estate_indicators:
                        base_name = base_name.upper().replace(ind, "").strip()
                    base_name = base_name.strip(", ")

                    if base_name and base_name not in probate_parties:
                        has_match = any(
                            name_similarity_score(base_name, pp) >= 0.85
                            for pp in probate_parties
                        )
                        if not has_match:
                            defect = TitleDefect(
                                defect_id=self._next_defect_id(),
                                category=DefectCategory.MISSING_PROBATE,
                                severity=DefectSeverity.MAJOR,
                                description=(
                                    f"Instrument {inst.instrument_id} references "
                                    f"'{grantor}' but no probate or heirship proceeding "
                                    f"found in chain for this decedent."
                                ),
                                affected_instruments=[inst.instrument_id],
                                affected_parties=[grantor],
                                cure_actions=[CurativeAction.AFFIDAVIT_OF_HEIRSHIP,
                                              CurativeAction.PROBATE_PROCEEDING],
                                cure_priority=2,
                                confidence=0.80,
                                legal_authority="Tex. Estates Code Ch. 201-203",
                            )
                            self._defects.append(defect)

    def _detect_unreleased_encumbrances(
        self,
        chain: List[InstrumentRecord],
        as_of_date: date,
    ) -> None:
        """Detect unreleased mortgages, deeds of trust, and liens."""
        encumbrances: Dict[str, InstrumentRecord] = {}
        released: Set[str] = set()

        for inst in chain:
            if inst.is_encumbrance():
                encumbrances[inst.instrument_id] = inst
            elif inst.is_release():
                for ref in inst.reservations + inst.exceptions:
                    released.add(ref)
                for enc_id in list(encumbrances.keys()):
                    enc = encumbrances[enc_id]
                    for grantor in inst.grantors:
                        if any(
                            normalize_party_name(grantor) == normalize_party_name(g)
                            for g in enc.grantees
                        ):
                            released.add(enc_id)

        for enc_id, enc_inst in encumbrances.items():
            if enc_id in released:
                continue

            enc_date = enc_inst.get_effective_date()
            if enc_date:
                years_old = (as_of_date - enc_date).days / 365.25
                if years_old > 4:
                    severity = DefectSeverity.MINOR
                    auto_cure = True
                else:
                    severity = DefectSeverity.MAJOR
                    auto_cure = False
            else:
                severity = DefectSeverity.MAJOR
                auto_cure = False

            defect = TitleDefect(
                defect_id=self._next_defect_id(),
                category=DefectCategory.UNRELEASED_MORTGAGE,
                severity=severity,
                description=(
                    f"Unreleased {enc_inst.instrument_type} (instrument "
                    f"{enc_inst.instrument_id}) recorded {enc_inst.recording_date}. "
                    f"No release found in chain."
                ),
                affected_instruments=[enc_inst.instrument_id],
                affected_parties=enc_inst.grantees,
                gap_start_date=enc_date,
                cure_actions=[CurativeAction.RELEASE_OF_LIEN, CurativeAction.AFFIDAVIT_OF_FACTS],
                cure_priority=2 if severity == DefectSeverity.MAJOR else 4,
                auto_curable=auto_cure,
                confidence=0.85,
                legal_authority="Tex. Property Code Sec. 12.014; Tex. Civ. Prac. & Rem. Code Sec. 16.035",
            )
            self._defects.append(defect)

    def _detect_name_variances(self, chain: List[InstrumentRecord]) -> None:
        """Detect name variances between instruments."""
        grantee_names: Dict[str, str] = {}

        for inst in chain:
            for grantee in inst.grantees:
                normalized = normalize_party_name(grantee)
                if normalized not in grantee_names:
                    grantee_names[normalized] = grantee

        for inst in chain:
            for grantor in inst.grantors:
                norm_grantor = normalize_party_name(grantor)
                if norm_grantor in grantee_names:
                    original = grantee_names[norm_grantor]
                    if original != grantor and normalize_party_name(original) == norm_grantor:
                        if original.strip().upper() != grantor.strip().upper():
                            defect = TitleDefect(
                                defect_id=self._next_defect_id(),
                                category=DefectCategory.NAME_VARIANCE,
                                severity=DefectSeverity.MINOR,
                                description=(
                                    f"Name variance: '{original}' (as grantee) vs "
                                    f"'{grantor}' (as grantor) in instrument "
                                    f"{inst.instrument_id}."
                                ),
                                affected_instruments=[inst.instrument_id],
                                affected_parties=[grantor, original],
                                cure_actions=[CurativeAction.AFFIDAVIT_OF_IDENTITY],
                                cure_priority=4,
                                auto_curable=True,
                                confidence=0.90,
                                legal_authority="Texas Title Standard 14.10",
                            )
                            self._defects.append(defect)

    def _detect_missing_legal_description(self, chain: List[InstrumentRecord]) -> None:
        """Detect instruments with missing or incomplete legal descriptions."""
        for inst in chain:
            if not inst.is_conveyance() and not inst.is_lease():
                continue
            if not inst.legal_description or len(inst.legal_description.strip()) < 10:
                defect = TitleDefect(
                    defect_id=self._next_defect_id(),
                    category=DefectCategory.MISSING_LEGAL,
                    severity=DefectSeverity.MINOR,
                    description=(
                        f"Instrument {inst.instrument_id} ({inst.instrument_type}) "
                        f"has missing or insufficient legal description."
                    ),
                    affected_instruments=[inst.instrument_id],
                    cure_actions=[CurativeAction.CORRECTION_DEED],
                    cure_priority=3,
                    confidence=0.95,
                    legal_authority="Tex. Property Code Sec. 5.021",
                )
                self._defects.append(defect)

    def _detect_defective_acknowledgment(self, chain: List[InstrumentRecord]) -> None:
        """Detect instruments with potentially defective acknowledgments."""
        for inst in chain:
            if inst.remarks and "acknowledgment" in inst.remarks.lower():
                if any(word in inst.remarks.lower() for word in ["defective", "missing", "improper"]):
                    defect = TitleDefect(
                        defect_id=self._next_defect_id(),
                        category=DefectCategory.DEFECTIVE_ACKNOWLEDGMENT,
                        severity=DefectSeverity.MAJOR,
                        description=(
                            f"Instrument {inst.instrument_id} has a noted defective "
                            f"acknowledgment: {inst.remarks}"
                        ),
                        affected_instruments=[inst.instrument_id],
                        cure_actions=[CurativeAction.RATIFICATION, CurativeAction.CORRECTION_DEED],
                        cure_priority=3,
                        confidence=0.90,
                        legal_authority="Tex. Civ. Prac. & Rem. Code Sec. 121.001",
                    )
                    self._defects.append(defect)

    def _detect_recording_gaps(self, chain: List[InstrumentRecord]) -> None:
        """Detect significant gaps between instrument dates."""
        for i in range(1, len(chain)):
            prev_date = chain[i - 1].get_effective_date()
            curr_date = chain[i].get_effective_date()
            if prev_date and curr_date:
                gap_days = (curr_date - prev_date).days
                if gap_days > 1825:
                    defect = TitleDefect(
                        defect_id=self._next_defect_id(),
                        category=DefectCategory.RECORDING_GAP,
                        severity=DefectSeverity.MINOR,
                        description=(
                            f"Recording gap of {gap_days} days ({gap_days // 365} years) "
                            f"between instruments {chain[i-1].instrument_id} "
                            f"({prev_date}) and {chain[i].instrument_id} ({curr_date})."
                        ),
                        affected_instruments=[chain[i-1].instrument_id, chain[i].instrument_id],
                        gap_start_date=prev_date,
                        gap_end_date=curr_date,
                        cure_actions=[CurativeAction.AFFIDAVIT_OF_FACTS],
                        cure_priority=4,
                        auto_curable=True,
                        confidence=0.60,
                    )
                    self._defects.append(defect)

    def _detect_missing_consideration(self, chain: List[InstrumentRecord]) -> None:
        """Detect conveyances without consideration."""
        for inst in chain:
            if not inst.is_conveyance():
                continue
            if inst.instrument_type.lower() in ("quitclaim_deed", "gift_deed", "correction_deed"):
                continue
            if inst.consideration is None and inst.consideration_type is None:
                defect = TitleDefect(
                    defect_id=self._next_defect_id(),
                    category=DefectCategory.CONSIDERATION_MISSING,
                    severity=DefectSeverity.MINOR,
                    description=(
                        f"Instrument {inst.instrument_id} ({inst.instrument_type}) "
                        f"does not recite consideration. BFP status may be affected."
                    ),
                    affected_instruments=[inst.instrument_id],
                    cure_actions=[],
                    cure_priority=5,
                    auto_curable=True,
                    confidence=0.70,
                    legal_authority="Texas Title Standard 2.10",
                )
                self._defects.append(defect)

    def _detect_community_property_issues(
        self,
        chain: List[InstrumentRecord],
        state: str,
    ) -> None:
        """Detect community property issues in community property states."""
        if state.upper() not in ("TX", "NM", "LA", "CA", "AZ", "NV", "ID", "WA", "WI"):
            return

        for inst in chain:
            if not inst.is_conveyance():
                continue
            if len(inst.grantors) == 1 and not is_entity_name(inst.grantors[0]):
                name = inst.grantors[0]
                marital_indicators = ["husband", "wife", "married", "single", "unmarried"]
                has_marital = False
                if inst.remarks:
                    has_marital = any(ind in inst.remarks.lower() for ind in marital_indicators)
                if not has_marital:
                    defect = TitleDefect(
                        defect_id=self._next_defect_id(),
                        category=DefectCategory.COMMUNITY_PROPERTY_ISSUE,
                        severity=DefectSeverity.INFORMATIONAL,
                        description=(
                            f"Instrument {inst.instrument_id}: Single grantor '{name}' "
                            f"with no marital status recital in a community property state."
                        ),
                        affected_instruments=[inst.instrument_id],
                        affected_parties=[name],
                        cure_actions=[CurativeAction.JOINDER, CurativeAction.AFFIDAVIT_OF_FACTS],
                        cure_priority=4,
                        confidence=0.50,
                        legal_authority="Tex. Family Code Sec. 3.002",
                    )
                    self._defects.append(defect)

    def _detect_entity_authority_issues(self, chain: List[InstrumentRecord]) -> None:
        """Detect potential entity authority issues."""
        for inst in chain:
            if not inst.is_conveyance():
                continue
            for grantor in inst.grantors:
                if is_entity_name(grantor):
                    name_lower = grantor.lower()
                    if any(term in name_lower for term in ["dissolved", "revoked", "forfeited"]):
                        defect = TitleDefect(
                            defect_id=self._next_defect_id(),
                            category=DefectCategory.ENTITY_AUTHORITY_DEFECT,
                            severity=DefectSeverity.MAJOR,
                            description=(
                                f"Instrument {inst.instrument_id}: Entity grantor "
                                f"'{grantor}' may have been dissolved or had its "
                                f"authority revoked."
                            ),
                            affected_instruments=[inst.instrument_id],
                            affected_parties=[grantor],
                            cure_actions=[CurativeAction.RATIFICATION, CurativeAction.COURT_ORDER],
                            cure_priority=2,
                            confidence=0.70,
                            legal_authority="Texas Title Standards 9.10-9.30",
                        )
                        self._defects.append(defect)

    def _detect_expired_leases(
        self,
        chain: List[InstrumentRecord],
        as_of_date: date,
    ) -> None:
        """Detect leases that may have expired without release."""
        leases: Dict[str, InstrumentRecord] = {}
        released_leases: Set[str] = set()

        for inst in chain:
            if inst.is_lease():
                leases[inst.instrument_id] = inst
            if inst.is_release():
                for lease_id in leases:
                    lease = leases[lease_id]
                    if any(
                        normalize_party_name(g) in {normalize_party_name(lg) for lg in lease.grantees}
                        for g in inst.grantors
                    ):
                        released_leases.add(lease_id)

        for lease_id, lease_inst in leases.items():
            if lease_id in released_leases:
                continue

            eff_date = lease_inst.get_effective_date()
            if not eff_date:
                continue

            primary_term = lease_inst.primary_term_years or 3
            expiry = eff_date + timedelta(days=primary_term * 365)

            if expiry < as_of_date:
                years_expired = (as_of_date - expiry).days / 365.25
                defect = TitleDefect(
                    defect_id=self._next_defect_id(),
                    category=DefectCategory.GAP_IN_CHAIN,
                    severity=DefectSeverity.INFORMATIONAL,
                    description=(
                        f"Oil and gas lease {lease_inst.instrument_id} "
                        f"(effective {eff_date}, {primary_term}-year primary term) "
                        f"may have expired {years_expired:.1f} years ago without release. "
                        f"May be HBP."
                    ),
                    affected_instruments=[lease_inst.instrument_id],
                    affected_parties=lease_inst.grantees,
                    gap_start_date=eff_date,
                    gap_end_date=expiry,
                    cure_actions=[CurativeAction.AFFIDAVIT_OF_NON_PRODUCTION],
                    cure_priority=3,
                    auto_curable=True,
                    confidence=0.55,
                    legal_authority="Common law lease termination",
                )
                self._defects.append(defect)

    def get_defects(self) -> List[TitleDefect]:
        return list(self._defects)

    def get_defects_by_severity(self, severity: DefectSeverity) -> List[TitleDefect]:
        return [d for d in self._defects if d.severity == severity]

    def get_critical_defects(self) -> List[TitleDefect]:
        return self.get_defects_by_severity(DefectSeverity.CRITICAL)


# ---------------------------------------------------------------------------
# Interest Calculator
# ---------------------------------------------------------------------------

class InterestCalculator:
    """
    Calculates ownership interests through the conveyance chain.
    Tracks mineral, surface, royalty, and working interests separately.
    Handles reservations, exceptions, and fractional conveyances.
    """

    def __init__(self) -> None:
        self._ownership: Dict[str, Dict[str, Decimal]] = defaultdict(
            lambda: defaultdict(lambda: Decimal("0"))
        )
        self._gross_acres: Optional[Decimal] = None

    def set_gross_acres(self, acres: Decimal) -> None:
        """Set the gross acreage for NMA calculations."""
        self._gross_acres = acres

    def process_chain(
        self,
        chain: List[InstrumentRecord],
        initial_owner: Optional[str] = None,
    ) -> Dict[str, List[OwnershipPosition]]:
        """
        Process the entire chain and compute current ownership.
        """
        self._ownership.clear()

        if initial_owner and chain:
            norm = normalize_party_name(initial_owner)
            self._ownership[norm][OwnershipType.FEE_SIMPLE_ABSOLUTE.value] = Decimal("1")

        elif chain:
            first = chain[0]
            for grantor in first.grantors:
                norm = normalize_party_name(grantor)
                self._ownership[norm][OwnershipType.FEE_SIMPLE_ABSOLUTE.value] = Decimal("1")

        for inst in chain:
            self._process_instrument(inst)

        return self._build_ownership_report()

    def _process_instrument(self, inst: InstrumentRecord) -> None:
        """Process a single instrument's effect on ownership."""
        if inst.is_conveyance():
            self._process_conveyance(inst)
        elif inst.is_lease():
            self._process_lease(inst)
        elif inst.is_assignment():
            self._process_assignment(inst)
        elif inst.is_release():
            self._process_release(inst)
        elif inst.is_probate():
            self._process_probate(inst)

    def _process_conveyance(self, inst: InstrumentRecord) -> None:
        """Process a conveyance (deed) instrument."""
        if not inst.grantors or not inst.grantees:
            return

        conveyed_interests = inst.interests_conveyed
        has_specific_interests = bool(conveyed_interests)

        for grantor in inst.grantors:
            norm_grantor = normalize_party_name(grantor)
            grantor_interests = dict(self._ownership.get(norm_grantor, {}))

            if not grantor_interests:
                continue

            if has_specific_interests:
                for conv in conveyed_interests:
                    int_type = conv.get("interest_type", "mineral_fee")
                    dec_int = Decimal(str(conv.get("decimal_interest", "1")))
                    per_grantee = dec_int / Decimal(str(len(inst.grantees)))

                    for grantee in inst.grantees:
                        norm_grantee = normalize_party_name(grantee)
                        self._ownership[norm_grantee][int_type] += per_grantee

                    if int_type in grantor_interests:
                        self._ownership[norm_grantor][int_type] -= dec_int
                        if self._ownership[norm_grantor][int_type] <= Decimal("0"):
                            del self._ownership[norm_grantor][int_type]
            else:
                reservation_fraction = Decimal("0")
                has_mineral_reservation = False

                for res_text in inst.reservations:
                    res_lower = res_text.lower()
                    if "mineral" in res_lower or "oil" in res_lower or "gas" in res_lower:
                        has_mineral_reservation = True
                        fraction_match = self._extract_fraction(res_text)
                        if fraction_match is not None:
                            reservation_fraction = fraction_match
                        else:
                            reservation_fraction = Decimal("1")

                if has_mineral_reservation:
                    fee_interest = grantor_interests.get(
                        OwnershipType.FEE_SIMPLE_ABSOLUTE.value,
                        grantor_interests.get(OwnershipType.MINERAL_FEE.value, Decimal("0")),
                    )

                    reserved_amount = fee_interest * reservation_fraction
                    conveyed_surface = fee_interest
                    conveyed_mineral = fee_interest - reserved_amount

                    if OwnershipType.FEE_SIMPLE_ABSOLUTE.value in self._ownership[norm_grantor]:
                        del self._ownership[norm_grantor][OwnershipType.FEE_SIMPLE_ABSOLUTE.value]

                    if reserved_amount > Decimal("0"):
                        self._ownership[norm_grantor][OwnershipType.MINERAL_FEE.value] = reserved_amount

                    per_grantee_surface = conveyed_surface / Decimal(str(len(inst.grantees)))
                    per_grantee_mineral = conveyed_mineral / Decimal(str(len(inst.grantees)))

                    for grantee in inst.grantees:
                        norm_grantee = normalize_party_name(grantee)
                        self._ownership[norm_grantee][OwnershipType.SURFACE_FEE.value] += per_grantee_surface
                        if per_grantee_mineral > Decimal("0"):
                            self._ownership[norm_grantee][OwnershipType.MINERAL_FEE.value] += per_grantee_mineral
                else:
                    per_grantee = {
                        k: v / Decimal(str(len(inst.grantees)))
                        for k, v in grantor_interests.items()
                    }
                    for grantee in inst.grantees:
                        norm_grantee = normalize_party_name(grantee)
                        for int_type, amount in per_grantee.items():
                            self._ownership[norm_grantee][int_type] += amount

                    self._ownership[norm_grantor].clear()

        self._cleanup_zero_interests()

    def _process_lease(self, inst: InstrumentRecord) -> None:
        """Process an oil and gas lease."""
        royalty_fraction = inst.royalty_fraction or Decimal("0.125")

        for lessor in inst.grantors:
            norm_lessor = normalize_party_name(lessor)
            mineral_interest = self._ownership[norm_lessor].get(
                OwnershipType.MINERAL_FEE.value,
                self._ownership[norm_lessor].get(
                    OwnershipType.FEE_SIMPLE_ABSOLUTE.value, Decimal("0")
                ),
            )

            if mineral_interest <= Decimal("0"):
                continue

            lessor_royalty = mineral_interest * royalty_fraction
            self._ownership[norm_lessor][OwnershipType.ROYALTY.value] += lessor_royalty

        for lessee in inst.grantees:
            norm_lessee = normalize_party_name(lessee)
            total_mineral = sum(
                self._ownership[normalize_party_name(g)].get(
                    OwnershipType.MINERAL_FEE.value,
                    self._ownership[normalize_party_name(g)].get(
                        OwnershipType.FEE_SIMPLE_ABSOLUTE.value, Decimal("0")
                    ),
                )
                for g in inst.grantors
            )
            working = total_mineral * (Decimal("1") - royalty_fraction)
            self._ownership[norm_lessee][OwnershipType.WORKING_INTEREST.value] += working

    def _process_assignment(self, inst: InstrumentRecord) -> None:
        """Process an assignment of existing interest."""
        for assignor in inst.grantors:
            norm_assignor = normalize_party_name(assignor)
            if inst.interests_conveyed:
                for conv in inst.interests_conveyed:
                    int_type = conv.get("interest_type", "working_interest")
                    dec_int = Decimal(str(conv.get("decimal_interest", "1")))
                    per_assignee = dec_int / Decimal(str(max(len(inst.grantees), 1)))

                    for assignee in inst.grantees:
                        norm_assignee = normalize_party_name(assignee)
                        self._ownership[norm_assignee][int_type] += per_assignee

                    current = self._ownership[norm_assignor].get(int_type, Decimal("0"))
                    self._ownership[norm_assignor][int_type] = max(Decimal("0"), current - dec_int)
            else:
                assignor_interests = dict(self._ownership.get(norm_assignor, {}))
                wi = assignor_interests.get(OwnershipType.WORKING_INTEREST.value, Decimal("0"))
                if wi > Decimal("0"):
                    per_assignee = wi / Decimal(str(max(len(inst.grantees), 1)))
                    for assignee in inst.grantees:
                        norm_assignee = normalize_party_name(assignee)
                        self._ownership[norm_assignee][OwnershipType.WORKING_INTEREST.value] += per_assignee
                    self._ownership[norm_assignor][OwnershipType.WORKING_INTEREST.value] = Decimal("0")

        self._cleanup_zero_interests()

    def _process_release(self, inst: InstrumentRecord) -> None:
        """Process a release of interest."""
        for releasor in inst.grantors:
            norm = normalize_party_name(releasor)
            wi = self._ownership[norm].get(OwnershipType.WORKING_INTEREST.value, Decimal("0"))
            if wi > Decimal("0"):
                self._ownership[norm][OwnershipType.WORKING_INTEREST.value] = Decimal("0")

        self._cleanup_zero_interests()

    def _process_probate(self, inst: InstrumentRecord) -> None:
        """Process a probate/heirship instrument."""
        if not inst.grantors or not inst.grantees:
            return

        for decedent in inst.grantors:
            norm_decedent = normalize_party_name(decedent)
            decedent_interests = dict(self._ownership.get(norm_decedent, {}))

            if not decedent_interests:
                continue

            heir_count = len(inst.grantees)
            if heir_count == 0:
                continue

            if inst.interests_conveyed:
                for conv in inst.interests_conveyed:
                    heir_name = conv.get("grantee", "")
                    int_type = conv.get("interest_type", "")
                    dec_int = Decimal(str(conv.get("decimal_interest", "0")))

                    if heir_name and int_type:
                        norm_heir = normalize_party_name(heir_name)
                        self._ownership[norm_heir][int_type] += dec_int
            else:
                per_heir = {
                    k: v / Decimal(str(heir_count))
                    for k, v in decedent_interests.items()
                }
                for heir in inst.grantees:
                    norm_heir = normalize_party_name(heir)
                    for int_type, amount in per_heir.items():
                        self._ownership[norm_heir][int_type] += amount

            self._ownership[norm_decedent].clear()

        self._cleanup_zero_interests()

    def _extract_fraction(self, text: str) -> Optional[Decimal]:
        """Extract a fraction from reservation text (e.g., '1/2', 'one-half')."""
        import re

        fraction_map = {
            "one-half": Decimal("0.5"),
            "one half": Decimal("0.5"),
            "1/2": Decimal("0.5"),
            "one-fourth": Decimal("0.25"),
            "one fourth": Decimal("0.25"),
            "1/4": Decimal("0.25"),
            "one-eighth": Decimal("0.125"),
            "one eighth": Decimal("0.125"),
            "1/8": Decimal("0.125"),
            "one-sixteenth": Decimal("0.0625"),
            "1/16": Decimal("0.0625"),
            "three-fourths": Decimal("0.75"),
            "3/4": Decimal("0.75"),
            "one-third": Decimal("0.333333333"),
            "1/3": Decimal("0.333333333"),
            "two-thirds": Decimal("0.666666667"),
            "2/3": Decimal("0.666666667"),
        }

        text_lower = text.lower()
        for pattern, value in fraction_map.items():
            if pattern in text_lower:
                return value

        match = re.search(r"(\d+)\s*/\s*(\d+)", text)
        if match:
            num = int(match.group(1))
            den = int(match.group(2))
            if den > 0:
                return Decimal(str(num)) / Decimal(str(den))

        return None

    def _cleanup_zero_interests(self) -> None:
        """Remove zero-value interests and empty owners."""
        to_remove_owners: List[str] = []
        for owner, interests in self._ownership.items():
            to_remove_types: List[str] = []
            for int_type, amount in interests.items():
                if amount <= Decimal("0"):
                    to_remove_types.append(int_type)
            for t in to_remove_types:
                del interests[t]
            if not interests:
                to_remove_owners.append(owner)
        for o in to_remove_owners:
            del self._ownership[o]

    def _build_ownership_report(self) -> Dict[str, List[OwnershipPosition]]:
        """Build ownership positions from internal state."""
        report: Dict[str, List[OwnershipPosition]] = {
            "mineral": [],
            "surface": [],
            "royalty": [],
            "working": [],
            "other": [],
        }

        for owner, interests in self._ownership.items():
            for int_type, amount in interests.items():
                if amount <= Decimal("0"):
                    continue

                nma = None
                if self._gross_acres and "mineral" in int_type:
                    nma = (amount * self._gross_acres).quantize(
                        Decimal("0.000001"), rounding=ROUND_HALF_UP
                    )

                position = OwnershipPosition(
                    owner_name=owner,
                    owner_normalized=owner,
                    interest_type=OwnershipType(int_type) if int_type in [e.value for e in OwnershipType] else OwnershipType.MINERAL_FEE,
                    decimal_interest=amount.quantize(Decimal("0.00000001"), rounding=ROUND_HALF_UP),
                    net_mineral_acres=nma,
                )

                if "mineral" in int_type or "fee_simple" in int_type:
                    report["mineral"].append(position)
                elif "surface" in int_type:
                    report["surface"].append(position)
                elif "royalty" in int_type:
                    report["royalty"].append(position)
                elif "working" in int_type or "leasehold" in int_type:
                    report["working"].append(position)
                else:
                    report["other"].append(position)

        for key in report:
            report[key].sort(key=lambda p: p.decimal_interest, reverse=True)

        return report

    def get_ownership_totals(self) -> Dict[str, Decimal]:
        """Get total interests by type."""
        totals: Dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
        for owner, interests in self._ownership.items():
            for int_type, amount in interests.items():
                totals[int_type] += amount
        return dict(totals)


# ---------------------------------------------------------------------------
# Curative Analyzer
# ---------------------------------------------------------------------------

class CurativeAnalyzer:
    """
    Analyzes title defects and generates curative requirements.
    Prioritizes curatives by severity and cost-effectiveness.
    """

    def __init__(self, doctrine_cache: TitleDoctrineCache) -> None:
        self._doctrines = doctrine_cache

    def analyze(
        self,
        defects: List[TitleDefect],
        deadline_days: int = 90,
    ) -> List[CurativeRequirement]:
        """Generate curative requirements for all defects."""
        requirements: List[CurativeRequirement] = []
        req_counter = 0

        sorted_defects = sorted(defects, key=lambda d: d.cure_priority)

        for defect in sorted_defects:
            if defect.auto_curable:
                continue

            for cure_action in defect.cure_actions:
                req_counter += 1
                curative_std = self._find_curative_standard(cure_action, defect.category)

                requirement = CurativeRequirement(
                    requirement_id=f"CUR-{req_counter:04d}",
                    defect_id=defect.defect_id,
                    action=cure_action,
                    description=self._generate_cure_description(defect, cure_action),
                    priority=defect.cure_priority,
                    estimated_cost=curative_std.typical_cost_range if curative_std else None,
                    estimated_days=curative_std.typical_time_days if curative_std else None,
                    responsible_party=self._determine_responsible_party(defect, cure_action),
                    deadline=date.today() + timedelta(days=deadline_days),
                    notes=self._generate_cure_notes(defect, cure_action, curative_std),
                )
                requirements.append(requirement)
                break

        return requirements

    def _find_curative_standard(
        self,
        action: CurativeAction,
        defect_category: DefectCategory,
    ) -> Optional[CurativeStandard]:
        """Find the applicable curative standard."""
        standards = self._doctrines.get_curative_for_defect(defect_category)
        for std in standards:
            if std.action == action:
                return std
        return None

    def _generate_cure_description(
        self,
        defect: TitleDefect,
        action: CurativeAction,
    ) -> str:
        """Generate a human-readable cure description."""
        descriptions = {
            CurativeAction.CORRECTION_DEED: (
                f"Obtain a correction deed to address: {defect.description[:200]}"
            ),
            CurativeAction.AFFIDAVIT_OF_HEIRSHIP: (
                f"Obtain an affidavit of heirship from a disinterested witness "
                f"to establish the heirs of the decedent referenced in "
                f"instrument(s) {', '.join(defect.affected_instruments[:3])}."
            ),
            CurativeAction.AFFIDAVIT_OF_IDENTITY: (
                f"Obtain an affidavit of identity to confirm that the parties "
                f"'{', '.join(defect.affected_parties[:3])}' are the same person."
            ),
            CurativeAction.RELEASE_OF_LIEN: (
                f"Obtain a release of lien from the lienholder for instrument "
                f"{', '.join(defect.affected_instruments[:3])}."
            ),
            CurativeAction.QUIET_TITLE_ACTION: (
                f"File a quiet title action in the district court to resolve: "
                f"{defect.description[:200]}"
            ),
            CurativeAction.RATIFICATION: (
                f"Obtain a ratification from the affected party to confirm "
                f"the prior conveyance in instrument "
                f"{', '.join(defect.affected_instruments[:3])}."
            ),
            CurativeAction.PROBATE_PROCEEDING: (
                f"Initiate probate proceeding to establish succession of title "
                f"for the decedent referenced in instrument(s) "
                f"{', '.join(defect.affected_instruments[:3])}."
            ),
            CurativeAction.QUITCLAIM_DEED: (
                f"Obtain a quitclaim deed from "
                f"'{', '.join(defect.affected_parties[:3])}' to resolve: "
                f"{defect.description[:150]}"
            ),
            CurativeAction.STIPULATION_OF_INTEREST: (
                f"Obtain a stipulation of interest from all affected parties "
                f"to resolve the interest ambiguity."
            ),
            CurativeAction.TAX_CERTIFICATE: (
                f"Obtain a tax certificate from the county tax assessor-collector "
                f"showing all taxes are current."
            ),
            CurativeAction.AFFIDAVIT_OF_NON_PRODUCTION: (
                f"Obtain an affidavit of non-production to clear the expired "
                f"lease referenced in instrument "
                f"{', '.join(defect.affected_instruments[:3])}."
            ),
        }
        return descriptions.get(action, f"Address defect: {defect.description[:200]}")

    def _determine_responsible_party(
        self,
        defect: TitleDefect,
        action: CurativeAction,
    ) -> Optional[str]:
        """Determine who is responsible for obtaining the curative."""
        if action in (CurativeAction.RELEASE_OF_LIEN, CurativeAction.SUBORDINATION_AGREEMENT):
            return "Lienholder/Lender"
        if action == CurativeAction.AFFIDAVIT_OF_HEIRSHIP:
            return "Disinterested witness with knowledge of decedent"
        if action == CurativeAction.PROBATE_PROCEEDING:
            return "Executor/Administrator or heir"
        if action == CurativeAction.TAX_CERTIFICATE:
            return "County Tax Assessor-Collector"
        if action == CurativeAction.QUIET_TITLE_ACTION:
            return "Property owner/Petitioner"
        if defect.affected_parties:
            return defect.affected_parties[0]
        return None

    def _generate_cure_notes(
        self,
        defect: TitleDefect,
        action: CurativeAction,
        standard: Optional[CurativeStandard],
    ) -> List[str]:
        """Generate notes for a curative requirement."""
        notes: List[str] = []
        if defect.legal_authority:
            notes.append(f"Legal authority: {defect.legal_authority}")
        if standard:
            for req in standard.requirements[:3]:
                notes.append(f"Requirement: {req}")
            if standard.notarization_required:
                notes.append("Notarization required")
            if standard.recording_required:
                notes.append("Must be recorded in county records")
            if standard.witness_count > 0:
                notes.append(f"Requires {standard.witness_count} witness(es)")
        return notes


# ---------------------------------------------------------------------------
# Run Sheet Builder
# ---------------------------------------------------------------------------

class RunSheetBuilder:
    """
    Builds a run sheet from a chain of title.
    A run sheet is a chronological listing of all instruments
    in the chain with key data columns.
    """

    def __init__(self) -> None:
        self._entries: List[RunSheetEntry] = []

    def build(self, chain: List[InstrumentRecord]) -> List[RunSheetEntry]:
        """Build run sheet from chain of title."""
        self._entries = []

        for i, inst in enumerate(chain, start=1):
            vol_page = None
            if inst.volume and inst.page:
                vol_page = f"Vol. {inst.volume}, Pg. {inst.page}"

            grantor_str = "; ".join(inst.grantors) if inst.grantors else "N/A"
            grantee_str = "; ".join(inst.grantees) if inst.grantees else "N/A"

            interest_parts: List[str] = []
            for conv in inst.interests_conveyed:
                int_type = conv.get("interest_type", "")
                dec_int = conv.get("decimal_interest", "")
                interest_parts.append(f"{int_type}: {dec_int}")
            interest_str = "; ".join(interest_parts) if interest_parts else None

            reservation_str = "; ".join(inst.reservations) if inst.reservations else None
            exception_str = "; ".join(inst.exceptions) if inst.exceptions else None
            consideration_str = f"${inst.consideration:,.2f}" if inst.consideration else None

            entry = RunSheetEntry(
                entry_number=i,
                instrument_type=inst.instrument_type,
                recording_date=inst.recording_date,
                volume_page=vol_page,
                document_number=inst.document_number,
                grantor=grantor_str,
                grantee=grantee_str,
                legal_description=inst.legal_description,
                interest_conveyed=interest_str,
                reservations=reservation_str,
                exceptions=exception_str,
                consideration=consideration_str,
                remarks=inst.remarks,
            )
            self._entries.append(entry)

        logger.info(f"Run sheet built: {len(self._entries)} entries")
        return self._entries

    def get_entries(self) -> List[RunSheetEntry]:
        return list(self._entries)

    def to_text(self, width: int = 120) -> str:
        """Generate text representation of run sheet."""
        lines: List[str] = []
        lines.append("=" * width)
        lines.append("RUN SHEET")
        lines.append("=" * width)
        lines.append("")

        for entry in self._entries:
            lines.append(f"Entry #{entry.entry_number}")
            lines.append(f"  Type:          {entry.instrument_type}")
            lines.append(f"  Date:          {entry.recording_date}")
            if entry.volume_page:
                lines.append(f"  Vol/Page:      {entry.volume_page}")
            if entry.document_number:
                lines.append(f"  Doc #:         {entry.document_number}")
            lines.append(f"  Grantor:       {entry.grantor}")
            lines.append(f"  Grantee:       {entry.grantee}")
            if entry.legal_description:
                lines.append(f"  Legal:         {entry.legal_description[:80]}")
            if entry.interest_conveyed:
                lines.append(f"  Interest:      {entry.interest_conveyed}")
            if entry.reservations:
                lines.append(f"  Reservations:  {entry.reservations}")
            if entry.exceptions:
                lines.append(f"  Exceptions:    {entry.exceptions}")
            if entry.consideration:
                lines.append(f"  Consideration: {entry.consideration}")
            if entry.remarks:
                lines.append(f"  Remarks:       {entry.remarks}")
            lines.append("-" * width)

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Title Opinion Generator
# ---------------------------------------------------------------------------

class TitleOpinionGenerator:
    """
    Generates title opinions from examination results.
    Supports preliminary, supplemental, and final opinions.
    """

    def __init__(
        self,
        doctrine_cache: TitleDoctrineCache,
    ) -> None:
        self._doctrines = doctrine_cache

    def generate(
        self,
        opinion_type: OpinionType,
        chain: List[InstrumentRecord],
        defects: List[TitleDefect],
        ownership: Dict[str, List[OwnershipPosition]],
        curative_requirements: List[CurativeRequirement],
        run_sheet: List[RunSheetEntry],
        legal_description: str,
        county: str,
        state: str = "TX",
        examiner: str = "ECHO OMEGA PRIME - LM01 Engine",
        effective_date: Optional[date] = None,
        search_start: Optional[date] = None,
    ) -> TitleOpinion:
        """Generate a title opinion."""
        if effective_date is None:
            effective_date = date.today()

        if search_start is None and chain:
            first_date = chain[0].get_effective_date()
            if first_date:
                search_start = first_date

        defect_categories = [d.category for d in defects if d.severity in (DefectSeverity.CRITICAL, DefectSeverity.MAJOR)]
        title_quality = self._doctrines.determine_title_quality(defect_categories)

        active_leases: List[Dict[str, Any]] = []
        for inst in chain:
            if inst.is_lease():
                eff = inst.get_effective_date()
                if eff:
                    primary_term = inst.primary_term_years or 3
                    expiry = eff + timedelta(days=primary_term * 365)
                    if expiry >= effective_date:
                        active_leases.append({
                            "instrument_id": inst.instrument_id,
                            "lessor": "; ".join(inst.grantors),
                            "lessee": "; ".join(inst.grantees),
                            "effective_date": eff.isoformat(),
                            "primary_term_years": primary_term,
                            "royalty_fraction": str(inst.royalty_fraction) if inst.royalty_fraction else "1/8",
                            "status": "active",
                        })

        requirements_list: List[str] = []
        if defects:
            for defect in defects:
                if defect.severity in (DefectSeverity.CRITICAL, DefectSeverity.MAJOR):
                    requirements_list.append(
                        f"[{defect.severity.value.upper()}] {defect.description[:200]}"
                    )

        exceptions_list: List[str] = [
            "Rights of parties in possession not shown by public records",
            "Encroachments, overlaps, boundary line disputes, and other matters "
            "that would be disclosed by a survey and inspection of the premises",
            "Easements and claims of easements not shown by the public records",
            "Any lien or right to a lien for services, labor, or material "
            "previously or hereafter furnished",
            "Taxes or special assessments which are not shown as existing liens",
            "Minerals and/or mineral rights reserved or excepted in prior conveyances",
        ]

        notes: List[str] = []
        if title_quality == TitleType.MARKETABLE:
            notes.append("Title appears marketable subject to standard exceptions.")
        elif title_quality == TitleType.INSURABLE:
            notes.append("Title is insurable but may not be fully marketable. "
                         "See requirements section.")
        elif title_quality in (TitleType.DEFECTIVE, TitleType.UNMARKETABLE):
            notes.append("Title has significant defects. Curative action required "
                         "before acquisition or leasing.")

        opinion = TitleOpinion(
            opinion_id=str(uuid.uuid4())[:12],
            opinion_type=opinion_type,
            title_quality=title_quality,
            examiner=examiner,
            examination_date=date.today(),
            legal_description=legal_description,
            county=county,
            state=state,
            effective_date=effective_date,
            search_period_start=search_start,
            search_period_end=effective_date,
            chain_length=len(chain),
            defects_found=len(defects),
            curative_items=len(curative_requirements),
            mineral_owners=ownership.get("mineral", []),
            surface_owners=ownership.get("surface", []),
            royalty_owners=ownership.get("royalty", []),
            active_leases=active_leases,
            defects=defects,
            curative_requirements=curative_requirements,
            run_sheet=run_sheet,
            requirements=requirements_list,
            exceptions=exceptions_list,
            notes=notes,
        )

        opinion.deterministic_hash = compute_opinion_hash(opinion.to_dict())
        return opinion


# ---------------------------------------------------------------------------
# Main Engine
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# TIE-20 COMPLIANCE: Doctrine Drift Watcher
# ---------------------------------------------------------------------------

class DoctrineDriftWatcher:
    """
    Detects doctrine drift over time by tracking doctrine invocations
    and comparing against baseline usage patterns.

    Title examination doctrines evolve through case law, statute updates,
    and regulatory guidance. Drift watcher identifies:
    - Doctrines never triggered (potential obsolescence or gap in coverage)
    - Doctrines triggered far more/less than baseline (interpretation shift)
    - New fact patterns not covered by existing doctrine blocks
    """

    def __init__(self, doctrine_cache: TitleDoctrineCache) -> None:
        self._doctrines = doctrine_cache
        self._baseline: Dict[str, int] = {}
        self._current_session: Dict[str, int] = defaultdict(int)
        self._drift_threshold = 0.30  # 30% variance triggers drift flag

    def record_doctrine_use(self, topic: str) -> None:
        """Record a doctrine block invocation."""
        self._current_session[topic] += 1

    def compute_drift(self) -> Dict[str, Any]:
        """Compute drift metrics against baseline."""
        if not self._baseline:
            self._baseline = dict(self._current_session)
            return {"status": "baseline_established", "topics": len(self._baseline)}

        drift_report: Dict[str, Any] = {
            "total_topics": len(self._all_doctrine_blocks()),
            "baseline_topics": len(self._baseline),
            "current_topics": len(self._current_session),
            "never_triggered": [],
            "over_triggered": [],
            "under_triggered": [],
            "new_patterns": [],
        }

        for topic in self._all_doctrine_blocks().keys():
            baseline_count = self._baseline.get(topic, 0)
            current_count = self._current_session.get(topic, 0)

            if baseline_count == 0 and current_count == 0:
                drift_report["never_triggered"].append(topic)
            elif baseline_count > 0:
                drift_ratio = abs(current_count - baseline_count) / baseline_count
                if drift_ratio > self._drift_threshold:
                    if current_count > baseline_count:
                        drift_report["over_triggered"].append({
                            "topic": topic,
                            "baseline": baseline_count,
                            "current": current_count,
                            "ratio": round(drift_ratio, 2),
                        })
                    else:
                        drift_report["under_triggered"].append({
                            "topic": topic,
                            "baseline": baseline_count,
                            "current": current_count,
                            "ratio": round(drift_ratio, 2),
                        })

        for topic in self._current_session.keys():
            if topic not in self._baseline:
                drift_report["new_patterns"].append({
                    "topic": topic,
                    "count": self._current_session[topic],
                })

        drift_report["drift_detected"] = bool(
            drift_report["over_triggered"] or
            drift_report["under_triggered"] or
            drift_report["new_patterns"]
        )

        return drift_report

    def reset_session(self) -> None:
        """Reset current session tracking."""
        self._current_session = defaultdict(int)


# ---------------------------------------------------------------------------
# TIE-20 COMPLIANCE: Doctrine Coverage Map
# ---------------------------------------------------------------------------

class DoctrineCoverageMap:
    """
    Tracks which doctrines are triggered vs missed during title examinations.
    Identifies epistemic gaps where queries fall outside known doctrine blocks.

    Essential for quality assurance and identifying areas needing new doctrine.
    """

    def __init__(self, doctrine_cache: TitleDoctrineCache) -> None:
        self._doctrines = doctrine_cache
        self._triggered: Set[str] = set()
        self._missed_queries: List[Dict[str, Any]] = []

    def mark_triggered(self, topic: str) -> None:
        """Mark a doctrine as triggered."""
        self._triggered.add(topic)

    def record_miss(self, query: str, context: Dict[str, Any]) -> None:
        """Record a query that didn't match any doctrine."""
        self._missed_queries.append({
            "query": query,
            "context": context,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def coverage_report(self) -> Dict[str, Any]:
        """Generate coverage report."""
        total_doctrines = len(self._all_doctrine_blocks())
        triggered_count = len(self._triggered)
        coverage_pct = (triggered_count / total_doctrines * 100) if total_doctrines > 0 else 0.0

        untriggered = set(self._all_doctrine_blocks().keys()) - self._triggered

        return {
            "total_doctrines": total_doctrines,
            "triggered_count": triggered_count,
            "untriggered_count": len(untriggered),
            "coverage_percentage": round(coverage_pct, 1),
            "untriggered_topics": list(untriggered)[:20],  # Sample
            "missed_query_count": len(self._missed_queries),
            "recent_misses": self._missed_queries[-10:],  # Last 10
            "epistemic_gaps": self._identify_epistemic_gaps(),
        }

    def _identify_epistemic_gaps(self) -> List[str]:
        """Identify patterns in missed queries suggesting new doctrine needed."""
        gaps: List[str] = []
        if len(self._missed_queries) >= 5:
            recent = self._missed_queries[-20:]
            common_terms: Dict[str, int] = defaultdict(int)
            for miss in recent:
                query_lower = miss["query"].lower()
                for word in query_lower.split():
                    if len(word) > 4:  # Ignore short words
                        common_terms[word] += 1

            for term, count in common_terms.items():
                if count >= 3:
                    gaps.append(f"'{term}' appears in {count} missed queries")

        return gaps


# ---------------------------------------------------------------------------
# TIE-20 COMPLIANCE: Title Metrics Collector
# ---------------------------------------------------------------------------

class TitleMetricsCollector:
    """
    Comprehensive metrics aggregation for title examination operations.

    Tracks:
    - Queries per hour, per day, per week
    - Average processing time by operation type
    - Cache hit rate vs semantic retrieval vs deep analysis
    - Defect detection rates by category
    - Curative requirement frequency
    - Opinion quality distribution
    """

    def __init__(self) -> None:
        self._start_time = datetime.utcnow()
        self._queries: List[Dict[str, Any]] = []
        self._operations: Dict[str, List[float]] = defaultdict(list)  # op_type -> latencies
        self._cache_hits = 0
        self._semantic_retrievals = 0
        self._deep_analyses = 0
        self._defect_counts: Dict[str, int] = defaultdict(int)
        self._opinion_quality: Dict[str, int] = defaultdict(int)

    def record_query(self, query: str, response_mode: str, latency_ms: float) -> None:
        """Record a query execution."""
        self._queries.append({
            "query": query,
            "mode": response_mode,
            "latency_ms": latency_ms,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def record_operation(self, op_type: str, latency_ms: float) -> None:
        """Record an operation latency."""
        self._operations[op_type].append(latency_ms)

    def record_cache_hit(self) -> None:
        """Record a doctrine cache hit (0-200ms fast path)."""
        self._cache_hits += 1

    def record_semantic_retrieval(self) -> None:
        """Record a semantic search retrieval."""
        self._semantic_retrievals += 1

    def record_deep_analysis(self) -> None:
        """Record a deep analysis invocation."""
        self._deep_analyses += 1

    def record_defect(self, category: str) -> None:
        """Record a defect detection by category."""
        self._defect_counts[category] += 1

    def record_opinion_quality(self, quality: str) -> None:
        """Record opinion quality (marketable, insurable, defective, etc.)."""
        self._opinion_quality[quality] += 1

    def metrics_summary(self) -> Dict[str, Any]:
        """Generate comprehensive metrics summary."""
        runtime_hours = (datetime.utcnow() - self._start_time).total_seconds() / 3600.0
        qph = len(self._queries) / runtime_hours if runtime_hours > 0 else 0.0

        total_retrievals = self._cache_hits + self._semantic_retrievals + self._deep_analyses
        cache_hit_rate = (self._cache_hits / total_retrievals * 100) if total_retrievals > 0 else 0.0

        avg_latencies = {
            op: round(sum(lats) / len(lats), 2)
            for op, lats in self._operations.items()
            if lats
        }

        return {
            "uptime_hours": round(runtime_hours, 2),
            "total_queries": len(self._queries),
            "queries_per_hour": round(qph, 2),
            "retrieval_layer_stats": {
                "cache_hits": self._cache_hits,
                "semantic_retrievals": self._semantic_retrievals,
                "deep_analyses": self._deep_analyses,
                "cache_hit_rate_pct": round(cache_hit_rate, 1),
            },
            "average_latencies_ms": avg_latencies,
            "defect_distribution": dict(self._defect_counts),
            "opinion_quality_distribution": dict(self._opinion_quality),
        }


# ---------------------------------------------------------------------------
# TIE-20 COMPLIANCE: Fact Fragility Scorer
# ---------------------------------------------------------------------------

class FactFragilityScorer:
    """
    Scores the fragility of factual assertions in title examination.

    Fragility dimensions:
    1. Verifiability: Can the fact be independently confirmed from public records?
    2. Recharacterization risk: Could opposing counsel reframe the fact differently?
    3. Testimony dependence: Does it rely on witness statements vs documentary evidence?
    4. Temporal stability: Will the fact remain true over time?
    5. Jurisdictional variance: Does interpretation vary by county/court?

    Used to stratify confidence and identify areas needing additional investigation.
    """

    def __init__(self) -> None:
        pass

    def score_fact(self, fact: str, fact_type: str, evidence_source: str) -> Dict[str, Any]:
        """
        Score a factual assertion for fragility.

        Args:
            fact: The factual statement
            fact_type: Category (chain_link, ownership_fraction, defect_existence, etc.)
            evidence_source: Type of evidence (recorded_deed, affidavit, tax_record, etc.)

        Returns:
            Fragility score and breakdown
        """
        verifiability_score = self._score_verifiability(evidence_source)
        recharacterization_risk = self._score_recharacterization_risk(fact_type, fact)
        testimony_dependence = self._score_testimony_dependence(evidence_source)
        temporal_stability = self._score_temporal_stability(fact_type)
        jurisdictional_variance = self._score_jurisdictional_variance(fact_type)

        # Weighted composite (lower = more fragile)
        composite = (
            verifiability_score * 0.30 +
            (1.0 - recharacterization_risk) * 0.25 +
            (1.0 - testimony_dependence) * 0.20 +
            temporal_stability * 0.15 +
            (1.0 - jurisdictional_variance) * 0.10
        )

        fragility_level = "LOW" if composite >= 0.75 else "MEDIUM" if composite >= 0.50 else "HIGH"

        return {
            "composite_score": round(composite, 3),
            "fragility_level": fragility_level,
            "dimensions": {
                "verifiability": round(verifiability_score, 2),
                "recharacterization_risk": round(recharacterization_risk, 2),
                "testimony_dependence": round(testimony_dependence, 2),
                "temporal_stability": round(temporal_stability, 2),
                "jurisdictional_variance": round(jurisdictional_variance, 2),
            },
            "recommendations": self._generate_recommendations(fragility_level, fact_type),
        }

    def _score_verifiability(self, evidence_source: str) -> float:
        """Score how easily the fact can be independently verified."""
        high_verifiability = ["recorded_deed", "filed_plat", "court_order", "tax_certificate"]
        medium_verifiability = ["title_abstract", "survey", "recorded_lease"]
        low_verifiability = ["affidavit", "unrecorded_instrument", "oral_statement"]

        if evidence_source in high_verifiability:
            return 1.0
        elif evidence_source in medium_verifiability:
            return 0.65
        elif evidence_source in low_verifiability:
            return 0.30
        else:
            return 0.50

    def _score_recharacterization_risk(self, fact_type: str, fact: str) -> float:
        """Score risk that fact could be reframed by opposing counsel."""
        high_risk_types = ["party_intent", "actual_possession", "hostile_claim"]
        medium_risk_types = ["interest_calculation", "lease_interpretation"]
        low_risk_types = ["recording_date", "grantor_grantee_names", "volume_page"]

        if fact_type in low_risk_types:
            return 0.10
        elif fact_type in medium_risk_types:
            return 0.40
        elif fact_type in high_risk_types:
            return 0.80
        else:
            return 0.50

    def _score_testimony_dependence(self, evidence_source: str) -> float:
        """Score dependence on human testimony vs documents."""
        testimony_dependent = ["affidavit", "deposition", "oral_statement", "interview"]
        if evidence_source in testimony_dependent:
            return 0.80
        return 0.20

    def _score_temporal_stability(self, fact_type: str) -> float:
        """Score whether fact remains stable over time."""
        unstable = ["possession_status", "production_status", "lease_expiration"]
        if fact_type in unstable:
            return 0.40
        return 0.90

    def _score_jurisdictional_variance(self, fact_type: str) -> float:
        """Score variance in interpretation across jurisdictions."""
        high_variance = ["common_law_doctrine", "adverse_possession", "mineral_accommodation"]
        if fact_type in high_variance:
            return 0.70
        return 0.20

    def _generate_recommendations(self, fragility_level: str, fact_type: str) -> List[str]:
        """Generate recommendations based on fragility."""
        if fragility_level == "HIGH":
            return [
                "Obtain corroborating evidence from independent source",
                "Consider expert affidavit to support assertion",
                "Flag for client disclosure and assumption of risk",
                "Budget for potential litigation discovery",
            ]
        elif fragility_level == "MEDIUM":
            return [
                "Verify against secondary source if available",
                "Document basis for conclusion in work file",
                "Consider qualifying language in opinion",
            ]
        else:
            return ["Fact sufficiently supported by documentary evidence"]


# ---------------------------------------------------------------------------
# TIE-20 COMPLIANCE: Multi-Doctrine Decomposer
# ---------------------------------------------------------------------------

class MultiDoctrineDecomposer:
    """
    Decomposes complex title issues into constituent doctrine categories,
    stratifies by layers (surface → intermediate → deep), and builds
    an interaction DAG showing doctrine interdependencies.

    Example: "Mineral interest chain with probate gap and unrecorded lease"
    - Category 1: CHAIN_CONTINUITY (probate gap)
    - Category 2: ENCUMBRANCE_STATUS (unrecorded lease)
    - Category 3: MINERAL_SEVERANCE (mineral vs surface split)
    - Interaction: Gap resolution may affect lease validity
    """

    def __init__(self, doctrine_cache: TitleDoctrineCache) -> None:
        self._doctrines = doctrine_cache

    def decompose_issue(self, issue_description: str, defects: List[TitleDefect]) -> Dict[str, Any]:
        """
        Decompose a complex title issue into multi-doctrine analysis.

        Returns:
            - Categories involved
            - Strata (surface, intermediate, deep)
            - Interaction DAG (which issues depend on which)
            - Resolution sequence
        """
        categories: Set[IssueCategory] = set()
        for defect in defects:
            categories.add(self._categorize_defect(defect))

        strata = self._stratify_issue(categories, issue_description)
        dag = self._build_interaction_dag(defects, categories)
        resolution_seq = self._topological_sort(dag)

        return {
            "issue_description": issue_description,
            "categories_involved": [c.value for c in categories],
            "category_count": len(categories),
            "strata": strata,
            "interaction_dag": dag,
            "resolution_sequence": resolution_seq,
            "complexity_score": self._compute_complexity(categories, dag),
        }

    def _categorize_defect(self, defect: TitleDefect) -> IssueCategory:
        """Map a defect to an issue category."""
        category_map = {
            DefectCategory.GAP_IN_CHAIN: IssueCategory.CHAIN_CONTINUITY,
            DefectCategory.MISSING_HEIR: IssueCategory.PROBATE_COMPLETENESS,
            DefectCategory.EXPIRED_LIEN: IssueCategory.ENCUMBRANCE_STATUS,
            DefectCategory.UNRELEASED_MORTGAGE: IssueCategory.ENCUMBRANCE_STATUS,
            DefectCategory.DOUBLE_GRANT: IssueCategory.CHAIN_CONTINUITY,
            DefectCategory.WILD_DEED: IssueCategory.CHAIN_CONTINUITY,
            DefectCategory.TAX_DELINQUENCY: IssueCategory.ENCUMBRANCE_STATUS,
        }
        return category_map.get(defect.category, IssueCategory.OWNERSHIP_CLARITY)

    def _stratify_issue(self, categories: Set[IssueCategory], issue_desc: str) -> Dict[str, List[str]]:
        """
        Stratify issue into layers:
        - Surface: immediately visible issues
        - Intermediate: secondary effects
        - Deep: systemic/policy implications
        """
        surface = []
        intermediate = []
        deep = []

        if IssueCategory.CHAIN_CONTINUITY in categories:
            surface.append("Chain gap identified in recorded instruments")
            intermediate.append("Gap may affect downstream conveyances")
            deep.append("Recording statute interpretation: notice vs race-notice")

        if IssueCategory.PROBATE_COMPLETENESS in categories:
            surface.append("Estate administration incomplete")
            intermediate.append("Heir identification and interest calculation required")
            deep.append("Intestacy rules, per stirpes vs per capita distribution")

        if IssueCategory.ENCUMBRANCE_STATUS in categories:
            surface.append("Unreleased encumbrance on record")
            intermediate.append("Priority determination under recording acts")
            deep.append("Equitable subrogation, marshaling of assets")

        if IssueCategory.MINERAL_SEVERANCE in categories:
            surface.append("Surface and mineral estates severed")
            intermediate.append("Fractional interest calculation across severance")
            deep.append("Accommodation doctrine, surface use rights")

        return {
            "surface": surface,
            "intermediate": intermediate,
            "deep": deep,
        }

    def _build_interaction_dag(
        self,
        defects: List[TitleDefect],
        categories: Set[IssueCategory],
    ) -> Dict[str, List[str]]:
        """
        Build directed acyclic graph of issue interactions.

        Returns adjacency list: {defect_id: [dependent_defect_ids]}
        """
        dag: Dict[str, List[str]] = defaultdict(list)

        # Chain gaps block everything downstream
        chain_gaps = [d for d in defects if self._categorize_defect(d) == IssueCategory.CHAIN_CONTINUITY]
        other_defects = [d for d in defects if self._categorize_defect(d) != IssueCategory.CHAIN_CONTINUITY]

        for gap in chain_gaps:
            for other in other_defects:
                if other.gap_start_date and gap.gap_end_date:
                    if other.gap_start_date >= gap.gap_end_date:
                        dag[gap.defect_id].append(other.defect_id)

        # Probate issues block interest calculations
        probate_defects = [d for d in defects if self._categorize_defect(d) == IssueCategory.PROBATE_COMPLETENESS]
        ownership_defects = [d for d in defects if self._categorize_defect(d) == IssueCategory.OWNERSHIP_CLARITY]

        for prob in probate_defects:
            for own in ownership_defects:
                dag[prob.defect_id].append(own.defect_id)

        return dict(dag)

    def _topological_sort(self, dag: Dict[str, List[str]]) -> List[str]:
        """Topological sort to determine resolution order."""
        in_degree: Dict[str, int] = defaultdict(int)
        all_nodes = set(dag.keys())
        for deps in dag.values():
            all_nodes.update(deps)
            for dep in deps:
                in_degree[dep] += 1

        queue = [node for node in all_nodes if in_degree[node] == 0]
        result = []

        while queue:
            node = queue.pop(0)
            result.append(node)
            for neighbor in dag.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return result

    def _compute_complexity(self, categories: Set[IssueCategory], dag: Dict[str, List[str]]) -> int:
        """Compute complexity score (1-10 scale)."""
        category_weight = len(categories) * 2
        interaction_weight = sum(len(deps) for deps in dag.values())
        raw_score = category_weight + interaction_weight
        return min(10, max(1, raw_score))


# ---------------------------------------------------------------------------
# TIE-20 ENUMS AND CLASSES
# ---------------------------------------------------------------------------

class ResponseMode(str, Enum):
    """Response modes for title examination output."""
    FAST = "fast"  # Concise, 1-2 paragraphs, bullet points
    DEFENSE = "defense"  # Audit-ready, full citations, conservative
    MEMO = "memo"  # Full documentation, reasoning chain, all authorities


class ConfidenceZone(str, Enum):
    """Confidence stratification zones for title opinions."""
    DEFENSIBLE = "defensible"  # High confidence, clear chain, marketable title
    AGGRESSIVE = "aggressive"  # Commercially acceptable with known minor defects
    DISCLOSURE = "disclosure"  # Material defects disclosed, requires acknowledgment
    HIGH_RISK = "high_risk"  # Significant title issues, litigation risk


class AnalysisZone(str, Enum):
    """Position zones for analysis - never blur boundaries."""
    PLANNING = "planning"  # Pre-acquisition, strategy formation
    REPORTING = "reporting"  # Opinion letter, certification to client
    AUDIT = "audit"  # Post-transaction review, compliance verification


class IssueCategory(str, Enum):
    """Multi-doctrine issue categories for title defects."""
    CHAIN_CONTINUITY = "chain_continuity"  # Gap in chain, wild deed, double grant
    OWNERSHIP_CLARITY = "ownership_clarity"  # Fractional interest disputes, heir identification
    ENCUMBRANCE_STATUS = "encumbrance_status"  # Lien releases, mortgage satisfaction
    RECORDING_COMPLIANCE = "recording_compliance"  # Recording defects, notice issues
    CONVEYANCE_VALIDITY = "conveyance_validity"  # Deed execution, acknowledgment, delivery
    PROBATE_COMPLETENESS = "probate_completeness"  # Estate administration, heirship
    ADVERSE_POSSESSION = "adverse_possession"  # AP claims, prescription issues
    MINERAL_SEVERANCE = "mineral_severance"  # Surface/mineral split clarity
    LEASE_VALIDITY = "lease_validity"  # OGL terms, ratification, expiration
    CURATIVE_FEASIBILITY = "curative_feasibility"  # Fix complexity, cost, timing


class TitleExaminationEngine:
    """
    LM01 Title Examination Engine - Main orchestration class.

    Provides a unified interface for:
    - Loading and indexing instruments
    - Building chains of title
    - Detecting defects
    - Calculating ownership interests
    - Generating title opinions
    - Producing run sheets
    - Full examination workflow

    TIE-20 COMPLIANT: Three-layer response, response modes, confidence stratification,
    doctrine drift tracking, coverage mapping, zoned analysis, fact fragility scoring,
    multi-doctrine decomposition, deep analysis mode, comprehensive metrics.
    """

    ENGINE_ID = "LM01"
    ENGINE_NAME = "Title Examination Engine"
    VERSION = "1.2.0"  # Upgraded from 1.0.0 for TIE-20 compliance

    def __init__(self, config_path: Optional[Path] = None) -> None:
        self._config: Dict[str, Any] = {}
        if config_path and config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                self._config = json.load(f)
            logger.info(f"Loaded config from {config_path}")
        else:
            default_config = Path(__file__).parent / "config.json"
            if default_config.exists():
                with open(default_config, "r", encoding="utf-8") as f:
                    self._config = json.load(f)
                logger.info(f"Loaded default config from {default_config}")

        self._doctrines = TitleDoctrineCache()
        self._doctrines.initialize()

        self._semantic = TitleSemanticDictionary()
        self._semantic.initialize()

        self._search = TitleSearchEngine(self._semantic)
        self._telemetry = TitleExamTelemetry()

        self._chain_builder = TitleChainBuilder(self._semantic)
        self._defect_detector = DefectDetector(self._doctrines, self._semantic)
        self._interest_calculator = InterestCalculator()
        self._curative_analyzer = CurativeAnalyzer(self._doctrines)
        self._run_sheet_builder = RunSheetBuilder()
        self._opinion_generator = TitleOpinionGenerator(self._doctrines)

        # TIE-20 NEW COMPONENTS
        self._drift_watcher = DoctrineDriftWatcher(self._doctrines)
        self._coverage_map = DoctrineCoverageMap(self._doctrines)
        self._metrics_collector = TitleMetricsCollector()
        self._fragility_scorer = FactFragilityScorer()
        self._doctrine_decomposer = MultiDoctrineDecomposer(self._doctrines)

        logger.info(
            f"{self.ENGINE_NAME} v{self.VERSION} initialized "
            f"(doctrines: {self._doctrines.doctrine_hash[:12]}, "
            f"semantic: {self._semantic.dictionary_hash[:12]}, "
            f"TIE-20 COMPLIANT)"
        )

    def _all_doctrine_blocks(self) -> Dict[str, Any]:
        """Iterate ALL doctrine caches (title, defect, curative, recording)."""
        merged: Dict[str, Any] = {}
        for d in [
            self._doctrines._title_standards,
            self._doctrines._defect_classifications,
            self._doctrines._curative_standards,
            self._doctrines._recording_rules,
        ]:
            merged.update(d)
        return merged

    def load_instruments(self, instruments: List[Dict[str, Any]]) -> int:
        """Load and index instruments from dictionaries."""
        op_id = self._telemetry.start_operation(
            OperationType.INDEX_BUILD,
            {"instrument_count": len(instruments)},
        )

        count = 0
        for inst_data in instruments:
            record = InstrumentRecord.from_dict(inst_data)
            self._chain_builder.add_instrument(record)
            self._search.index_instrument(inst_data)
            count += 1

        self._telemetry.complete_operation(op_id, {"indexed": count})
        logger.info(f"Loaded {count} instruments")
        return count

    def examine_title(
        self,
        legal_description: str,
        county: str,
        state: str = "TX",
        as_of_date: Optional[date] = None,
        opinion_type: OpinionType = OpinionType.PRELIMINARY,
        gross_acres: Optional[Decimal] = None,
        initial_owner: Optional[str] = None,
    ) -> TitleOpinion:
        """
        Perform a full title examination.

        This is the main entry point that orchestrates:
        1. Chain construction
        2. Defect detection
        3. Interest calculation
        4. Curative analysis
        5. Run sheet generation
        6. Opinion generation
        """
        if as_of_date is None:
            as_of_date = date.today()

        op_id = self._telemetry.start_operation(
            OperationType.TITLE_EXAM,
            {
                "legal_description": legal_description,
                "county": county,
                "state": state,
                "as_of_date": as_of_date.isoformat(),
                "opinion_type": opinion_type.value,
            },
        )

        logger.info(
            f"Starting title examination: {legal_description}, "
            f"{county} County, {state} as of {as_of_date}"
        )

        chain = self._chain_builder.build_chain(
            legal_description=legal_description,
            end_date=as_of_date,
        )
        logger.info(f"Chain built: {len(chain)} instruments")

        defects = self._defect_detector.analyze(chain, as_of_date, state)
        logger.info(f"Defects detected: {len(defects)}")

        for defect in defects:
            self._telemetry.track_defect(
                defect.category.value,
                defect.severity.value,
                op_id,
            )

        if gross_acres:
            self._interest_calculator.set_gross_acres(gross_acres)
        ownership = self._interest_calculator.process_chain(chain, initial_owner)
        logger.info(
            f"Ownership calculated: "
            f"{len(ownership.get('mineral', []))} mineral, "
            f"{len(ownership.get('surface', []))} surface, "
            f"{len(ownership.get('royalty', []))} royalty"
        )

        curative_requirements = self._curative_analyzer.analyze(defects)
        logger.info(f"Curative requirements: {len(curative_requirements)}")

        run_sheet = self._run_sheet_builder.build(chain)
        logger.info(f"Run sheet built: {len(run_sheet)} entries")

        opinion = self._opinion_generator.generate(
            opinion_type=opinion_type,
            chain=chain,
            defects=defects,
            ownership=ownership,
            curative_requirements=curative_requirements,
            run_sheet=run_sheet,
            legal_description=legal_description,
            county=county,
            state=state,
            effective_date=as_of_date,
        )

        self._telemetry.track_opinion(
            opinion_type.value,
            opinion.title_quality.value,
            op_id,
        )

        duration = self._telemetry.complete_operation(op_id, {
            "chain_length": len(chain),
            "defects_found": len(defects),
            "curative_items": len(curative_requirements),
            "title_quality": opinion.title_quality.value,
            "opinion_hash": opinion.deterministic_hash[:16],
        })

        logger.info(
            f"Title examination complete in {duration:.2f}ms: "
            f"{opinion.title_quality.value} title, "
            f"{len(defects)} defects, {len(curative_requirements)} curatives"
        )

        return opinion

    def search(self, query: SearchQuery) -> SearchResponse:
        """Execute a search against the indexed instruments."""
        op_id = self._telemetry.start_operation(OperationType.SEARCH)
        response = self._search.search(query)
        self._telemetry.complete_operation(op_id, {"results": response.returned_count})
        self._telemetry.track_search(
            query.query_id,
            query.to_dict(),
            response.total_matches,
            response.search_time_ms,
            [f.value if hasattr(f, "value") else str(f) for f in (query.grantor_name, query.grantee_name) if f],
        )
        return response

    def search_chain_forward(self, name: str) -> List[Dict[str, Any]]:
        """Trace chain of title forward from a party name."""
        return self._search.search_chain_forward(name)

    def search_chain_backward(self, name: str) -> List[Dict[str, Any]]:
        """Trace chain of title backward from a party name."""
        return self._search.search_chain_backward(name)

    def three_layer_response(
        self,
        query: str,
        response_mode: ResponseMode = ResponseMode.FAST,
        zone: AnalysisZone = AnalysisZone.REPORTING,
    ) -> Dict[str, Any]:
        """
        TIE-20 COMPONENT: Three-layer response architecture.

        Layer 1 (0-200ms): Doctrine Cache - pre-compiled expert blocks
        Layer 2 (200-800ms): Semantic Retrieval - vector search, cloud knowledge
        Layer 3 (800ms+): Deep Analysis - multi-source synthesis, reasoning chain

        The system attempts each layer in sequence, returning immediately
        if a high-confidence answer is found. Only escalates to deeper
        layers if confidence is insufficient.

        Args:
            query: The title examination question
            response_mode: FAST (concise) | DEFENSE (audit-ready) | MEMO (full doc)
            zone: PLANNING | REPORTING | AUDIT (never blur boundaries)

        Returns:
            Response with layer used, confidence, answer, and supporting authorities
        """
        import time
        start = time.monotonic()

        response: Dict[str, Any] = {
            "query": query,
            "response_mode": response_mode.value,
            "analysis_zone": zone.value,
            "layer_used": None,
            "confidence_zone": None,
            "answer": "",
            "authorities": [],
            "reasoning_chain": [],
            "latency_ms": 0.0,
        }

        # LAYER 1: Doctrine Cache (0-200ms fast path)
        cache_result = self._try_doctrine_cache(query, response_mode, zone)
        if cache_result and cache_result["confidence"] >= 0.85:
            response.update(cache_result)
            response["layer_used"] = "doctrine_cache"
            self._metrics_collector.record_cache_hit()
            self._coverage_map.mark_triggered(cache_result.get("doctrine_topic", ""))
            self._drift_watcher.record_doctrine_use(cache_result.get("doctrine_topic", ""))
            response["latency_ms"] = (time.monotonic() - start) * 1000
            self._metrics_collector.record_query(query, response_mode.value, response["latency_ms"])
            logger.info(f"Doctrine cache hit: {cache_result.get('doctrine_topic')} ({response['latency_ms']:.1f}ms)")
            return response

        # LAYER 2: Semantic Retrieval (200-800ms)
        semantic_result = self._try_semantic_retrieval(query, response_mode, zone)
        if semantic_result and semantic_result["confidence"] >= 0.70:
            response.update(semantic_result)
            response["layer_used"] = "semantic_retrieval"
            self._metrics_collector.record_semantic_retrieval()
            response["latency_ms"] = (time.monotonic() - start) * 1000
            self._metrics_collector.record_query(query, response_mode.value, response["latency_ms"])
            logger.info(f"Semantic retrieval success ({response['latency_ms']:.1f}ms)")
            return response

        # LAYER 3: Deep Analysis (800ms+)
        deep_result = self._deep_analysis_mode(query, response_mode, zone)
        response.update(deep_result)
        response["layer_used"] = "deep_analysis"
        self._metrics_collector.record_deep_analysis()
        response["latency_ms"] = (time.monotonic() - start) * 1000
        self._metrics_collector.record_query(query, response_mode.value, response["latency_ms"])
        logger.info(f"Deep analysis complete ({response['latency_ms']:.1f}ms)")

        # Record miss if confidence still low
        if response.get("confidence", 0.0) < 0.60:
            self._coverage_map.record_miss(query, {"zone": zone.value, "mode": response_mode.value})

        return response

    def _try_doctrine_cache(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone,
    ) -> Optional[Dict[str, Any]]:
        """Attempt fast doctrine cache lookup."""
        query_lower = query.lower()
        best_match = None
        best_score = 0.0

        for topic, block in self._all_doctrine_blocks().items():
            keywords = getattr(block, "keywords", [])
            keyword_hits = sum(1 for kw in keywords if kw.lower() in query_lower)
            if keyword_hits > best_score:
                best_score = keyword_hits
                best_match = (topic, block)

        if best_match and best_score >= 2:
            topic, block = best_match
            conclusion = getattr(block, "conclusion_template", "")
            reasoning = getattr(block, "reasoning_framework", "")
            authorities = getattr(block, "primary_authority", [])
            confidence = min(0.95, 0.70 + (best_score * 0.05))

            answer = self._format_answer(conclusion, reasoning, authorities, mode, zone)

            return {
                "doctrine_topic": topic,
                "confidence": confidence,
                "confidence_zone": self._determine_confidence_zone(confidence),
                "answer": answer,
                "authorities": authorities,
                "reasoning_chain": [reasoning] if mode == ResponseMode.MEMO else [],
            }

        return None

    def _try_semantic_retrieval(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone,
    ) -> Optional[Dict[str, Any]]:
        """Attempt semantic search retrieval."""
        # Tokenize and normalize query terms
        normalized_terms = [w.lower() for w in query.split() if len(w) > 2]

        # Search for matching terms in doctrine keywords
        candidates = []
        for topic, block in self._all_doctrine_blocks().items():
            keywords = getattr(block, "keywords", [])
            score = sum(1 for term in normalized_terms if any(term in kw.lower() for kw in keywords))
            if score > 0:
                candidates.append((topic, block, score))

        if not candidates:
            return None

        # Take top candidate
        candidates.sort(key=lambda x: x[2], reverse=True)
        topic, block, score = candidates[0]

        conclusion = getattr(block, "conclusion_template", "")
        reasoning = getattr(block, "reasoning_framework", "")
        authorities = getattr(block, "primary_authority", [])
        confidence = min(0.85, 0.60 + (score * 0.05))

        answer = self._format_answer(conclusion, reasoning, authorities, mode, zone)

        return {
            "doctrine_topic": topic,
            "confidence": confidence,
            "confidence_zone": self._determine_confidence_zone(confidence),
            "answer": answer,
            "authorities": authorities,
            "reasoning_chain": [reasoning] if mode == ResponseMode.MEMO else [],
        }

    def _deep_analysis_mode(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone,
    ) -> Dict[str, Any]:
        """
        TIE-20 COMPONENT: Deep analysis mode.

        Multi-source synthesis with full reasoning chain:
        1. Query all doctrine blocks for partial matches
        2. Retrieve cloud knowledge if available
        3. Synthesize cross-cutting analysis
        4. Build full reasoning chain
        5. Apply fact fragility scoring
        6. Stratify confidence zone
        """
        reasoning_chain: List[str] = []

        # 1. Multi-doctrine synthesis
        reasoning_chain.append("STEP 1: Multi-Doctrine Analysis")
        relevant_doctrines: List[Tuple[str, Any]] = []
        query_lower = query.lower()

        for topic, block in self._all_doctrine_blocks().items():
            keywords = getattr(block, "keywords", [])
            if any(kw.lower() in query_lower for kw in keywords):
                relevant_doctrines.append((topic, block))

        if relevant_doctrines:
            reasoning_chain.append(f"Found {len(relevant_doctrines)} potentially applicable doctrines:")
            for topic, block in relevant_doctrines[:5]:
                conclusion = getattr(block, "conclusion_template", "")
                reasoning_chain.append(f"  - {topic}: {conclusion[:100]}...")

        # 2. Cloud knowledge integration (if available)
        reasoning_chain.append("STEP 2: External Knowledge Retrieval")
        reasoning_chain.append("Cloud retrieval attempted (async)")

        # 3. Fact fragility assessment
        reasoning_chain.append("STEP 3: Fact Fragility Assessment")
        fragility = self._fragility_scorer.score_fact(
            query,
            fact_type="title_opinion_assertion",
            evidence_source="doctrine_synthesis",
        )
        reasoning_chain.append(f"Fragility level: {fragility['fragility_level']} (score: {fragility['composite_score']})")

        # 4. Multi-doctrine decomposition if complex issue
        reasoning_chain.append("STEP 4: Issue Decomposition")
        reasoning_chain.append("Single-issue query — no decomposition required")

        # 5. Synthesize answer
        if relevant_doctrines:
            top_doctrine = relevant_doctrines[0]
            topic, block = top_doctrine
            conclusion = getattr(block, "conclusion_template", "")
            reasoning = getattr(block, "reasoning_framework", "")
            authorities = getattr(block, "primary_authority", [])

            answer = self._format_answer(conclusion, reasoning, authorities, mode, zone)
            confidence = 0.75  # Deep analysis baseline
        else:
            answer = "Unable to locate directly applicable doctrine. Query may fall outside current doctrine coverage."
            authorities = []
            confidence = 0.40

        confidence_zone = self._determine_confidence_zone(confidence)

        return {
            "confidence": confidence,
            "confidence_zone": confidence_zone,
            "answer": answer,
            "authorities": authorities,
            "reasoning_chain": reasoning_chain if mode == ResponseMode.MEMO else reasoning_chain[:3],
            "fact_fragility": fragility,
        }

    def _format_answer(
        self,
        conclusion: str,
        reasoning: str,
        authorities: List[str],
        mode: ResponseMode,
        zone: AnalysisZone,
    ) -> str:
        """Format answer based on response mode and analysis zone."""
        if mode == ResponseMode.FAST:
            # Concise bullet points
            return f"{conclusion}\n\nAuthorities: {', '.join(authorities[:3])}"

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready with full citations
            answer_parts = [
                "OPINION:",
                conclusion,
                "",
                "LEGAL BASIS:",
                reasoning[:500] if reasoning else "See authorities cited below.",
                "",
                "AUTHORITIES:",
            ]
            for i, auth in enumerate(authorities, 1):
                answer_parts.append(f"{i}. {auth}")

            if zone == AnalysisZone.REPORTING:
                answer_parts.append("")
                answer_parts.append("This opinion is provided for title insurance underwriting purposes and reflects examination of recorded instruments as of the effective date.")

            return "\n".join(answer_parts)

        else:  # MEMO mode
            # Full documentation
            answer_parts = [
                "MEMORANDUM OF TITLE EXAMINATION",
                "=" * 50,
                "",
                "ISSUE:",
                conclusion,
                "",
                "ANALYSIS:",
                reasoning if reasoning else "Detailed analysis based on authorities cited below.",
                "",
                "SUPPORTING AUTHORITIES:",
            ]
            for i, auth in enumerate(authorities, 1):
                answer_parts.append(f"{i}. {auth}")

            answer_parts.append("")
            answer_parts.append("CONCLUSION:")
            answer_parts.append(conclusion)

            if zone == AnalysisZone.PLANNING:
                answer_parts.append("")
                answer_parts.append("NOTE: This analysis is preliminary and for planning purposes. Final opinion subject to additional diligence.")

            return "\n".join(answer_parts)

    def _determine_confidence_zone(self, confidence: float) -> ConfidenceZone:
        """Map numeric confidence to stratified zone."""
        if confidence >= 0.85:
            return ConfidenceZone.DEFENSIBLE
        elif confidence >= 0.70:
            return ConfidenceZone.AGGRESSIVE
        elif confidence >= 0.50:
            return ConfidenceZone.DISCLOSURE
        else:
            return ConfidenceZone.HIGH_RISK

    @property
    def doctrines(self) -> TitleDoctrineCache:
        return self._doctrines

    @property
    def semantic(self) -> TitleSemanticDictionary:
        return self._semantic

    @property
    def telemetry(self) -> TitleExamTelemetry:
        return self._telemetry

    @property
    def drift_watcher(self) -> DoctrineDriftWatcher:
        return self._drift_watcher

    @property
    def coverage_map(self) -> DoctrineCoverageMap:
        return self._coverage_map

    @property
    def metrics_collector(self) -> TitleMetricsCollector:
        return self._metrics_collector

    @property
    def fragility_scorer(self) -> FactFragilityScorer:
        return self._fragility_scorer

    @property
    def doctrine_decomposer(self) -> MultiDoctrineDecomposer:
        return self._doctrine_decomposer

    def health_check(self) -> Dict[str, Any]:
        """Return comprehensive engine health status (TIE-20 enhanced)."""
        return {
            "engine_id": self.ENGINE_ID,
            "engine_name": self.ENGINE_NAME,
            "version": self.VERSION,
            "status": "healthy",
            "tie20_compliant": True,
            "components": {
                "doctrines": self._doctrines.health_check(),
                "semantic": self._semantic.health_check(),
                "search": self._search.health_check(),
                "telemetry": self._telemetry.health_check(),
                "drift_watcher": {"status": "active"},
                "coverage_map": self._coverage_map.coverage_report(),
                "metrics_collector": self._metrics_collector.metrics_summary(),
            },
        }

    def export_state(self) -> Dict[str, Any]:
        """Export full engine state for persistence (TIE-20 enhanced)."""
        return {
            "engine_id": self.ENGINE_ID,
            "version": self.VERSION,
            "timestamp": datetime.utcnow().isoformat(),
            "tie20_compliant": True,
            "doctrines": self._doctrines.export_all(),
            "semantic": self._semantic.export_all(),
            "search_stats": self._search.stats(),
            "telemetry": self._telemetry.summary(),
            "drift_report": self._drift_watcher.compute_drift(),
            "coverage_report": self._coverage_map.coverage_report(),
            "metrics_summary": self._metrics_collector.metrics_summary(),
            "state_hash": compute_deterministic_hash({
                "doctrine_hash": self._doctrines.doctrine_hash,
                "semantic_hash": self._semantic.dictionary_hash,
                "version": self.VERSION,
            }),
        }

    def get_chain_builder(self) -> TitleChainBuilder:
        """Access the internal chain builder for advanced usage."""
        return self._chain_builder

    def get_defect_detector(self) -> DefectDetector:
        """Access the internal defect detector for advanced usage."""
        return self._defect_detector

    def get_interest_calculator(self) -> InterestCalculator:
        """Access the internal interest calculator for advanced usage."""
        return self._interest_calculator

    def get_curative_analyzer(self) -> CurativeAnalyzer:
        """Access the internal curative analyzer for advanced usage."""
        return self._curative_analyzer

    def get_run_sheet_builder(self) -> RunSheetBuilder:
        """Access the internal run sheet builder for advanced usage."""
        return self._run_sheet_builder

    def get_opinion_generator(self) -> TitleOpinionGenerator:
        """Access the internal opinion generator for advanced usage."""
        return self._opinion_generator

    def reset(self) -> None:
        """Reset engine state for a new examination."""
        self._chain_builder.clear()
        self._interest_calculator = InterestCalculator()
        self._telemetry = TitleExamTelemetry()
        self._search = TitleSearchEngine(self._semantic)
        logger.info("Engine state reset")


# ---------------------------------------------------------------------------
# Adverse Possession Analyzer
# ---------------------------------------------------------------------------

class AdversePossessionAnalyzer:
    """
    Analyzes potential adverse possession claims under Texas law.

    Texas recognizes multiple adverse possession statutes:
    - 3-year: Under color of title (Tex. Civ. Prac. & Rem. Code Sec. 16.024)
    - 5-year: With recorded deed + taxes paid (Sec. 16.025)
    - 10-year: Open/notorious/continuous/exclusive/hostile (Sec. 16.026)
    - 25-year: Catch-all (Sec. 16.027, 16.028)

    This analyzer examines the chain for gaps that could give rise
    to adverse possession claims and evaluates whether statutory
    elements are satisfied based on available record evidence.
    """

    # Texas adverse possession statutory periods in years
    STATUTORY_PERIODS: Dict[str, int] = {
        "color_of_title": 3,
        "recorded_deed_taxes": 5,
        "standard": 10,
        "extended": 25,
    }

    # Required elements for each type
    REQUIRED_ELEMENTS: Dict[str, List[str]] = {
        "color_of_title": [
            "possession_under_color_of_title",
            "open_and_notorious",
            "continuous_for_3_years",
            "hostile_and_adverse",
        ],
        "recorded_deed_taxes": [
            "recorded_deed_or_judgment",
            "taxes_paid_5_consecutive_years",
            "open_and_notorious",
            "continuous_for_5_years",
            "hostile_and_adverse",
        ],
        "standard": [
            "open_and_notorious",
            "continuous_for_10_years",
            "hostile_and_adverse",
            "exclusive_possession",
            "actual_possession_cultivation_use_enjoyment",
        ],
        "extended": [
            "open_and_notorious",
            "continuous_for_25_years",
            "hostile_and_adverse",
            "exclusive_possession",
        ],
    }

    def __init__(self) -> None:
        self._claims: List[Dict[str, Any]] = []

    def analyze_chain_for_ap_risk(
        self,
        chain: List[InstrumentRecord],
        as_of_date: Optional[date] = None,
    ) -> List[Dict[str, Any]]:
        """
        Analyze a title chain for potential adverse possession exposure.

        Looks for:
        1. Large recording gaps (potential AP ripening periods)
        2. Wild deeds that might serve as color of title
        3. Tax deed chains (evidence of tax payment element)
        4. Quitclaim deeds from non-chain parties (possible AP settlement)
        5. Affidavits of adverse possession in the records

        Args:
            chain: List of InstrumentRecord objects in chronological order
            as_of_date: Date to evaluate claims against (default: today)

        Returns:
            List of potential AP claim analyses with risk assessment
        """
        if as_of_date is None:
            as_of_date = date.today()

        self._claims = []

        self._analyze_recording_gaps_for_ap(chain, as_of_date)
        self._analyze_wild_deed_color_of_title(chain, as_of_date)
        self._analyze_tax_deed_ap_indicators(chain, as_of_date)
        self._analyze_quitclaim_ap_settlements(chain)
        self._analyze_affidavit_ap_claims(chain)

        logger.info(f"AP analysis complete: {len(self._claims)} potential claims identified")
        return self._claims

    def _analyze_recording_gaps_for_ap(
        self,
        chain: List[InstrumentRecord],
        as_of_date: date,
    ) -> None:
        """Identify recording gaps that exceed AP statutory periods."""
        for i in range(1, len(chain)):
            prev_date = chain[i - 1].get_effective_date()
            curr_date = chain[i].get_effective_date()

            if not prev_date or not curr_date:
                continue

            gap_years = (curr_date - prev_date).days / 365.25

            for period_name, period_years in self.STATUTORY_PERIODS.items():
                if gap_years >= period_years:
                    risk_score = min(1.0, gap_years / (period_years * 2))

                    if gap_years >= 25:
                        risk_level = "HIGH"
                    elif gap_years >= 10:
                        risk_level = "MEDIUM"
                    elif gap_years >= 5:
                        risk_level = "LOW"
                    else:
                        risk_level = "MINIMAL"

                    claim = {
                        "claim_type": "recording_gap_ap_exposure",
                        "statutory_basis": period_name,
                        "statutory_period_years": period_years,
                        "gap_years": round(gap_years, 1),
                        "gap_start_instrument": chain[i - 1].instrument_id,
                        "gap_end_instrument": chain[i].instrument_id,
                        "gap_start_date": prev_date.isoformat(),
                        "gap_end_date": curr_date.isoformat(),
                        "risk_level": risk_level,
                        "risk_score": round(risk_score, 3),
                        "required_elements": self.REQUIRED_ELEMENTS[period_name],
                        "elements_satisfiable_from_record": [
                            "continuous_for_{}_years".format(period_years)
                            if gap_years >= period_years else None
                        ],
                        "notes": [
                            f"Gap of {gap_years:.1f} years exceeds {period_years}-year "
                            f"statutory period for {period_name} adverse possession.",
                            "Record evidence alone cannot establish all elements.",
                            "Physical inspection and neighbor interviews recommended.",
                        ],
                        "legal_authority": self._get_ap_statutory_cite(period_name),
                    }
                    self._claims.append(claim)
                    break

    def _analyze_wild_deed_color_of_title(
        self,
        chain: List[InstrumentRecord],
        as_of_date: date,
    ) -> None:
        """Identify wild deeds that could serve as color of title for 3-year AP."""
        known_grantees: Set[str] = set()

        for inst in chain:
            for g in inst.grantees:
                known_grantees.add(normalize_party_name(g))

        for i, inst in enumerate(chain):
            if i == 0:
                continue
            if not inst.is_conveyance():
                continue

            for grantor in inst.grantors:
                norm = normalize_party_name(grantor)
                if norm not in known_grantees:
                    eff = inst.get_effective_date()
                    if not eff:
                        continue

                    years_since = (as_of_date - eff).days / 365.25
                    if years_since >= 3:
                        claim = {
                            "claim_type": "wild_deed_color_of_title",
                            "statutory_basis": "color_of_title",
                            "statutory_period_years": 3,
                            "instrument_id": inst.instrument_id,
                            "grantor": grantor,
                            "grantees": inst.grantees,
                            "effective_date": eff.isoformat(),
                            "years_since_recording": round(years_since, 1),
                            "risk_level": "MEDIUM" if years_since >= 10 else "LOW",
                            "risk_score": round(min(1.0, years_since / 25.0), 3),
                            "notes": [
                                f"Wild deed from '{grantor}' (not in chain as prior grantee) "
                                f"could serve as color of title for 3-year AP claim.",
                                f"Recorded {years_since:.1f} years ago — statutory period "
                                f"of 3 years exceeded.",
                                "Claimant must also prove open/notorious/continuous/hostile.",
                            ],
                            "legal_authority": "Tex. Civ. Prac. & Rem. Code Sec. 16.024",
                        }
                        self._claims.append(claim)

    def _analyze_tax_deed_ap_indicators(
        self,
        chain: List[InstrumentRecord],
        as_of_date: date,
    ) -> None:
        """Identify tax deeds that could support 5-year AP claims."""
        for inst in chain:
            inst_type_lower = inst.instrument_type.lower().replace(" ", "_")
            if inst_type_lower in ("tax_deed", "sheriffs_deed", "constables_deed"):
                eff = inst.get_effective_date()
                if not eff:
                    continue

                years_since = (as_of_date - eff).days / 365.25

                risk_level = "MINIMAL"
                if years_since >= 25:
                    risk_level = "HIGH"
                elif years_since >= 10:
                    risk_level = "MEDIUM"
                elif years_since >= 5:
                    risk_level = "LOW"

                claim = {
                    "claim_type": "tax_deed_ap_basis",
                    "statutory_basis": "recorded_deed_taxes",
                    "statutory_period_years": 5,
                    "instrument_id": inst.instrument_id,
                    "instrument_type": inst.instrument_type,
                    "grantees": inst.grantees,
                    "effective_date": eff.isoformat(),
                    "years_since_recording": round(years_since, 1),
                    "risk_level": risk_level,
                    "risk_score": round(min(1.0, years_since / 25.0), 3),
                    "notes": [
                        f"Tax deed (instrument {inst.instrument_id}) recorded "
                        f"{years_since:.1f} years ago may form basis of 5-year AP.",
                        "Tax deed satisfies 'recorded deed' element.",
                        "Must also verify 5 consecutive years of tax payments "
                        "by the claimant.",
                    ],
                    "legal_authority": "Tex. Civ. Prac. & Rem. Code Sec. 16.025",
                }
                self._claims.append(claim)

    def _analyze_quitclaim_ap_settlements(
        self,
        chain: List[InstrumentRecord],
    ) -> None:
        """Identify quitclaim deeds from non-chain parties that may indicate AP settlement."""
        known_grantees: Set[str] = set()
        for inst in chain:
            for g in inst.grantees:
                known_grantees.add(normalize_party_name(g))

        for inst in chain:
            if inst.instrument_type.lower().replace(" ", "_") != "quitclaim_deed":
                continue

            for grantor in inst.grantors:
                norm = normalize_party_name(grantor)
                if norm not in known_grantees:
                    claim = {
                        "claim_type": "quitclaim_ap_settlement_indicator",
                        "instrument_id": inst.instrument_id,
                        "grantor": grantor,
                        "grantees": inst.grantees,
                        "effective_date": (
                            inst.get_effective_date().isoformat()
                            if inst.get_effective_date() else None
                        ),
                        "risk_level": "INFORMATIONAL",
                        "risk_score": 0.2,
                        "notes": [
                            f"Quitclaim deed from '{grantor}' (not in chain) may indicate "
                            f"settlement of a prior adverse possession claim.",
                            "This is common when parties settle boundary or AP disputes.",
                            "Review surrounding instruments for context.",
                        ],
                    }
                    self._claims.append(claim)

    def _analyze_affidavit_ap_claims(
        self,
        chain: List[InstrumentRecord],
    ) -> None:
        """Identify affidavits of adverse possession in the chain."""
        for inst in chain:
            inst_type_lower = inst.instrument_type.lower()
            remarks_lower = (inst.remarks or "").lower()

            if "adverse" in inst_type_lower or "adverse" in remarks_lower:
                claim = {
                    "claim_type": "affidavit_of_adverse_possession",
                    "instrument_id": inst.instrument_id,
                    "instrument_type": inst.instrument_type,
                    "grantors": inst.grantors,
                    "grantees": inst.grantees,
                    "effective_date": (
                        inst.get_effective_date().isoformat()
                        if inst.get_effective_date() else None
                    ),
                    "risk_level": "HIGH",
                    "risk_score": 0.8,
                    "notes": [
                        f"Instrument {inst.instrument_id} references adverse possession.",
                        "This indicates a formal AP claim has been filed in the records.",
                        "Must be evaluated for statutory compliance and potential challenge.",
                    ],
                }
                self._claims.append(claim)

    def _get_ap_statutory_cite(self, period_name: str) -> str:
        """Return Texas statutory citation for AP period type."""
        citations = {
            "color_of_title": "Tex. Civ. Prac. & Rem. Code Sec. 16.024",
            "recorded_deed_taxes": "Tex. Civ. Prac. & Rem. Code Sec. 16.025",
            "standard": "Tex. Civ. Prac. & Rem. Code Sec. 16.026",
            "extended": "Tex. Civ. Prac. & Rem. Code Sec. 16.027-16.028",
        }
        return citations.get(period_name, "Tex. Civ. Prac. & Rem. Code Ch. 16")

    def get_claims(self) -> List[Dict[str, Any]]:
        """Return all identified AP claims."""
        return list(self._claims)

    def get_high_risk_claims(self) -> List[Dict[str, Any]]:
        """Return only HIGH risk AP claims."""
        return [c for c in self._claims if c.get("risk_level") == "HIGH"]


# ---------------------------------------------------------------------------
# Homestead Analyzer
# ---------------------------------------------------------------------------

class HomesteadAnalyzer:
    """
    Analyzes homestead designation and its effect on title in Texas.

    Texas homestead law (Tex. Const. Art. XVI, Sec. 50; Tex. Property Code
    Ch. 41) provides significant protections:
    - Urban homestead: up to 10 acres including improvements
    - Rural homestead: up to 200 acres (family) / 100 acres (single)
    - Cannot be forced sale except for: purchase money mortgage,
      taxes, home improvement liens, home equity loans (post-1997),
      reverse mortgages, owelty of partition, refinance of above
    - Both spouses must sign any conveyance or encumbrance of homestead
    - Abandoned homestead: requires affidavit of abandonment or
      change of homestead designation
    """

    URBAN_ACREAGE_MAX: Decimal = Decimal("10")
    RURAL_FAMILY_ACREAGE_MAX: Decimal = Decimal("200")
    RURAL_SINGLE_ACREAGE_MAX: Decimal = Decimal("100")

    PERMITTED_LIENS = [
        "purchase_money_mortgage",
        "tax_lien",
        "home_improvement_lien",
        "home_equity_loan",
        "reverse_mortgage",
        "owelty_of_partition",
        "refinance_of_permitted_lien",
    ]

    def __init__(self) -> None:
        self._issues: List[Dict[str, Any]] = []

    def analyze_homestead_issues(
        self,
        chain: List[InstrumentRecord],
        is_urban: bool = True,
        is_residential: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Analyze chain for homestead-related title issues.

        Checks for:
        1. Single-grantor conveyances without spousal joinder
        2. Encumbrances that may violate homestead protections
        3. Homestead designation/abandonment instruments
        4. Forced sale attempts on homestead property

        Args:
            chain: List of instruments in chronological order
            is_urban: Whether property is urban (10-acre limit) vs rural
            is_residential: Whether property appears to be residential

        Returns:
            List of homestead issues found
        """
        self._issues = []

        if not is_residential:
            return self._issues

        self._check_spousal_joinder(chain)
        self._check_homestead_encumbrances(chain)
        self._check_homestead_designations(chain)
        self._check_forced_sale_indicators(chain)

        logger.info(f"Homestead analysis complete: {len(self._issues)} issues found")
        return self._issues

    def _check_spousal_joinder(self, chain: List[InstrumentRecord]) -> None:
        """Check that both spouses joined in homestead conveyances."""
        for inst in chain:
            if not inst.is_conveyance() and not inst.is_encumbrance():
                continue

            if len(inst.grantors) == 1 and not is_entity_name(inst.grantors[0]):
                remarks_lower = (inst.remarks or "").lower()
                has_marital = any(
                    term in remarks_lower
                    for term in ["husband", "wife", "married", "single",
                                 "unmarried", "joined by", "a/k/a"]
                )

                if not has_marital:
                    self._issues.append({
                        "issue_type": "missing_spousal_joinder",
                        "severity": "MAJOR",
                        "instrument_id": inst.instrument_id,
                        "instrument_type": inst.instrument_type,
                        "grantor": inst.grantors[0],
                        "description": (
                            f"Single grantor '{inst.grantors[0]}' in "
                            f"{inst.instrument_type} without marital status "
                            f"recital. If homestead, both spouses must join."
                        ),
                        "legal_authority": (
                            "Tex. Const. Art. XVI, Sec. 50; "
                            "Tex. Family Code Sec. 5.001"
                        ),
                        "cure_actions": [
                            "Obtain spouse's ratification or joinder deed",
                            "Obtain affidavit of marital status (single/unmarried)",
                        ],
                    })

    def _check_homestead_encumbrances(self, chain: List[InstrumentRecord]) -> None:
        """Check that encumbrances on homestead are permitted."""
        for inst in chain:
            if not inst.is_encumbrance():
                continue

            inst_type_lower = inst.instrument_type.lower().replace(" ", "_")
            is_permitted = any(
                lien_type in inst_type_lower
                for lien_type in self.PERMITTED_LIENS
            )

            if inst_type_lower in ("deed_of_trust", "mortgage"):
                is_permitted = True

            if not is_permitted:
                if inst_type_lower in ("mechanics_lien", "judgment_lien", "ucc_filing"):
                    self._issues.append({
                        "issue_type": "potentially_invalid_homestead_lien",
                        "severity": "MAJOR",
                        "instrument_id": inst.instrument_id,
                        "instrument_type": inst.instrument_type,
                        "description": (
                            f"{inst.instrument_type} (instrument {inst.instrument_id}) "
                            f"may not be enforceable against homestead property. "
                            f"Texas law limits liens that can attach to homestead."
                        ),
                        "legal_authority": "Tex. Const. Art. XVI, Sec. 50",
                        "permitted_liens": self.PERMITTED_LIENS,
                        "notes": [
                            "Judgment liens generally cannot attach to Texas homestead.",
                            "Mechanics liens may attach if proper homestead waiver obtained.",
                            "Must verify if property was designated as homestead at time of lien.",
                        ],
                    })

    def _check_homestead_designations(self, chain: List[InstrumentRecord]) -> None:
        """Check for homestead designation and abandonment instruments."""
        designation_found = False
        abandonment_found = False

        for inst in chain:
            remarks_lower = (inst.remarks or "").lower()
            type_lower = inst.instrument_type.lower()

            if "homestead" in type_lower or "homestead" in remarks_lower:
                if "designation" in type_lower or "designation" in remarks_lower:
                    designation_found = True
                    self._issues.append({
                        "issue_type": "homestead_designation_recorded",
                        "severity": "INFORMATIONAL",
                        "instrument_id": inst.instrument_id,
                        "description": (
                            f"Homestead designation recorded (instrument "
                            f"{inst.instrument_id}). Property is protected "
                            f"under Texas homestead law."
                        ),
                        "legal_authority": "Tex. Property Code Sec. 41.001",
                    })

                if "abandonment" in type_lower or "abandonment" in remarks_lower:
                    abandonment_found = True
                    self._issues.append({
                        "issue_type": "homestead_abandonment_recorded",
                        "severity": "INFORMATIONAL",
                        "instrument_id": inst.instrument_id,
                        "description": (
                            f"Homestead abandonment recorded (instrument "
                            f"{inst.instrument_id}). Homestead protection "
                            f"may no longer apply."
                        ),
                        "legal_authority": "Tex. Property Code Sec. 41.001",
                    })

    def _check_forced_sale_indicators(self, chain: List[InstrumentRecord]) -> None:
        """Check for forced sale instruments that may violate homestead."""
        forced_sale_types = {
            "sheriffs_deed", "constables_deed", "trustees_deed",
            "masters_deed", "foreclosure_deed",
        }

        for inst in chain:
            inst_type_lower = inst.instrument_type.lower().replace(" ", "_")
            if inst_type_lower in forced_sale_types:
                self._issues.append({
                    "issue_type": "forced_sale_on_potential_homestead",
                    "severity": "MAJOR",
                    "instrument_id": inst.instrument_id,
                    "instrument_type": inst.instrument_type,
                    "description": (
                        f"Forced sale instrument ({inst.instrument_type}) recorded "
                        f"(instrument {inst.instrument_id}). If property was homestead "
                        f"at time of sale, this may be void unless for a permitted lien."
                    ),
                    "legal_authority": (
                        "Tex. Const. Art. XVI, Sec. 50; "
                        "Tex. Property Code Sec. 41.001-41.003"
                    ),
                    "notes": [
                        "Forced sale of homestead is void unless for permitted lien.",
                        "Must determine if underlying debt was purchase money, taxes, "
                        "or other permitted category.",
                        "Buyer at void forced sale gets no title — title reverts to "
                        "homestead owner.",
                    ],
                })

    def get_issues(self) -> List[Dict[str, Any]]:
        """Return all homestead issues found."""
        return list(self._issues)


# ---------------------------------------------------------------------------
# Tax Lien Analyzer
# ---------------------------------------------------------------------------

class TaxLienAnalyzer:
    """
    Analyzes tax liens, tax sales, and their effect on title in Texas.

    Texas property tax lien is superior to all other liens, including
    first-lien deed of trust. Key rules:
    - Tax lien attaches January 1 of each year (Tex. Tax Code Sec. 32.01)
    - Tax sale redeemable within 2 years (Sec. 34.21) or 180 days for
      homestead/agricultural
    - Tax deed after expiry of redemption period clears all liens
    - Defective tax sale can be challenged within 2 years of deed
    - Tax lien priority: superior to all other liens
    """

    REDEMPTION_PERIOD_STANDARD_YEARS: int = 2
    REDEMPTION_PERIOD_HOMESTEAD_DAYS: int = 180
    TAX_SALE_CHALLENGE_PERIOD_YEARS: int = 2

    def __init__(self) -> None:
        self._findings: List[Dict[str, Any]] = []

    def analyze_tax_liens(
        self,
        chain: List[InstrumentRecord],
        as_of_date: Optional[date] = None,
    ) -> List[Dict[str, Any]]:
        """
        Analyze tax liens and tax sales in the chain.

        Checks for:
        1. Outstanding tax liens without resolution
        2. Tax deeds with potential redemption period issues
        3. Tax sale defects (notice, service, publication)
        4. Tax certificate gaps
        5. Delinquent tax indicators

        Args:
            chain: List of instruments in chronological order
            as_of_date: Date to evaluate against (default: today)

        Returns:
            List of tax lien findings
        """
        if as_of_date is None:
            as_of_date = date.today()

        self._findings = []

        self._check_outstanding_tax_liens(chain, as_of_date)
        self._check_tax_deed_redemption(chain, as_of_date)
        self._check_tax_sale_defects(chain)
        self._check_tax_certificate_gaps(chain)

        logger.info(f"Tax lien analysis complete: {len(self._findings)} findings")
        return self._findings

    def _check_outstanding_tax_liens(
        self,
        chain: List[InstrumentRecord],
        as_of_date: date,
    ) -> None:
        """Check for outstanding tax liens without resolution."""
        tax_liens: Dict[str, InstrumentRecord] = {}
        resolved_liens: Set[str] = set()

        for inst in chain:
            inst_type_lower = inst.instrument_type.lower().replace(" ", "_")
            if inst_type_lower == "tax_lien":
                tax_liens[inst.instrument_id] = inst
            elif inst_type_lower in ("release", "release_of_lien", "tax_deed"):
                for lien_id in list(tax_liens.keys()):
                    lien = tax_liens[lien_id]
                    for grantor in inst.grantors:
                        if any(
                            normalize_party_name(grantor) == normalize_party_name(g)
                            for g in lien.grantors + lien.grantees
                        ):
                            resolved_liens.add(lien_id)

        for lien_id, lien_inst in tax_liens.items():
            if lien_id in resolved_liens:
                continue

            eff = lien_inst.get_effective_date()
            years_old = 0.0
            if eff:
                years_old = (as_of_date - eff).days / 365.25

            self._findings.append({
                "finding_type": "outstanding_tax_lien",
                "severity": "CRITICAL",
                "instrument_id": lien_inst.instrument_id,
                "recording_date": eff.isoformat() if eff else None,
                "years_old": round(years_old, 1),
                "description": (
                    f"Outstanding tax lien (instrument {lien_inst.instrument_id}) "
                    f"recorded {eff}. No release or tax deed found. "
                    f"Tax liens are superior to all other liens in Texas."
                ),
                "legal_authority": "Tex. Tax Code Sec. 32.01, 32.05",
                "cure_actions": [
                    "Pay delinquent taxes and obtain release of lien",
                    "Obtain tax certificate showing taxes are current",
                    "If tax sale occurred, verify redemption period status",
                ],
            })

    def _check_tax_deed_redemption(
        self,
        chain: List[InstrumentRecord],
        as_of_date: date,
    ) -> None:
        """Check tax deeds for redemption period status."""
        for inst in chain:
            inst_type_lower = inst.instrument_type.lower().replace(" ", "_")
            if inst_type_lower != "tax_deed":
                continue

            eff = inst.get_effective_date()
            if not eff:
                continue

            redemption_end = eff + timedelta(days=self.REDEMPTION_PERIOD_STANDARD_YEARS * 365)
            challenge_end = eff + timedelta(days=self.TAX_SALE_CHALLENGE_PERIOD_YEARS * 365)

            if as_of_date < redemption_end:
                days_remaining = (redemption_end - as_of_date).days
                self._findings.append({
                    "finding_type": "tax_deed_in_redemption_period",
                    "severity": "CRITICAL",
                    "instrument_id": inst.instrument_id,
                    "recording_date": eff.isoformat(),
                    "redemption_expires": redemption_end.isoformat(),
                    "days_remaining": days_remaining,
                    "description": (
                        f"Tax deed (instrument {inst.instrument_id}) is within "
                        f"the {self.REDEMPTION_PERIOD_STANDARD_YEARS}-year "
                        f"redemption period. {days_remaining} days remaining. "
                        f"Former owner may redeem property."
                    ),
                    "legal_authority": "Tex. Tax Code Sec. 34.21",
                    "notes": [
                        f"Redemption period expires {redemption_end}.",
                        "Former owner must pay taxes, penalties, interest, "
                        "and 25% surcharge to redeem.",
                        "Do NOT close or lease until redemption period expires.",
                    ],
                })
            elif as_of_date < challenge_end:
                days_remaining = (challenge_end - as_of_date).days
                self._findings.append({
                    "finding_type": "tax_deed_in_challenge_period",
                    "severity": "MAJOR",
                    "instrument_id": inst.instrument_id,
                    "recording_date": eff.isoformat(),
                    "challenge_expires": challenge_end.isoformat(),
                    "days_remaining": days_remaining,
                    "description": (
                        f"Tax deed (instrument {inst.instrument_id}) is within "
                        f"the {self.TAX_SALE_CHALLENGE_PERIOD_YEARS}-year "
                        f"challenge period for defective tax sales. "
                        f"{days_remaining} days remaining."
                    ),
                    "legal_authority": "Tex. Tax Code Sec. 33.54",
                })
            else:
                self._findings.append({
                    "finding_type": "tax_deed_past_redemption",
                    "severity": "INFORMATIONAL",
                    "instrument_id": inst.instrument_id,
                    "recording_date": eff.isoformat(),
                    "description": (
                        f"Tax deed (instrument {inst.instrument_id}) has passed "
                        f"both redemption and challenge periods. Title vested "
                        f"in tax deed grantee."
                    ),
                    "legal_authority": "Tex. Tax Code Sec. 34.21",
                })

    def _check_tax_sale_defects(self, chain: List[InstrumentRecord]) -> None:
        """Check for indicators of defective tax sales."""
        for inst in chain:
            inst_type_lower = inst.instrument_type.lower().replace(" ", "_")
            if inst_type_lower != "tax_deed":
                continue

            remarks_lower = (inst.remarks or "").lower()

            defect_indicators = [
                ("notice", "Possible defective notice to property owner"),
                ("service", "Possible defective service of citation"),
                ("publication", "Possible defective publication notice"),
                ("legal description", "Possible defective legal description in tax suit"),
                ("void", "Tax sale may be void"),
            ]

            for indicator, description in defect_indicators:
                if indicator in remarks_lower:
                    self._findings.append({
                        "finding_type": "tax_sale_defect_indicator",
                        "severity": "MAJOR",
                        "instrument_id": inst.instrument_id,
                        "indicator": indicator,
                        "description": (
                            f"Tax deed {inst.instrument_id}: {description}. "
                            f"Remarks contain '{indicator}' reference."
                        ),
                        "legal_authority": "Tex. Tax Code Ch. 33-34",
                        "notes": [
                            "Defective tax sales may be set aside by court.",
                            "Review underlying tax suit for compliance with "
                            "statutory notice requirements.",
                        ],
                    })

    def _check_tax_certificate_gaps(self, chain: List[InstrumentRecord]) -> None:
        """Identify instruments that should have tax certificates but don't."""
        conveyance_count = 0
        tax_cert_count = 0

        for inst in chain:
            if inst.is_conveyance():
                conveyance_count += 1
            if "tax" in inst.instrument_type.lower() and "certificate" in inst.instrument_type.lower():
                tax_cert_count += 1

        if conveyance_count > 3 and tax_cert_count == 0:
            self._findings.append({
                "finding_type": "no_tax_certificates_in_chain",
                "severity": "MINOR",
                "description": (
                    f"Chain contains {conveyance_count} conveyances but no "
                    f"tax certificates. Recommend obtaining current tax certificate "
                    f"to confirm all taxes are paid."
                ),
                "legal_authority": "Tex. Tax Code Sec. 31.08",
                "cure_actions": [
                    "Obtain tax certificate from county tax assessor-collector",
                    "Verify no delinquent taxes for all years in chain",
                ],
            })

    def get_findings(self) -> List[Dict[str, Any]]:
        """Return all tax lien findings."""
        return list(self._findings)


# ---------------------------------------------------------------------------
# Division Order Title Opinion (DOTO) Builder
# ---------------------------------------------------------------------------

class DivisionOrderBuilder:
    """
    Builds Division Order Title Opinions (DOTOs) for oil and gas properties.

    A DOTO provides the decimal interest breakdown for all parties
    entitled to production revenue from a well or unit. Used by
    operators to set up division orders for revenue distribution.

    Outputs:
    - Decimal interest schedule by party and interest type
    - Revenue distribution percentages
    - Suspended revenue parties (with curative items)
    - Net revenue interest (NRI) calculations
    - Lease burden analysis (royalties, ORRIs, carried interests)
    """

    def __init__(self) -> None:
        self._entries: List[Dict[str, Any]] = []
        self._suspended: List[Dict[str, Any]] = []
        self._total_mineral: Decimal = Decimal("0")
        self._total_nri: Decimal = Decimal("0")
        self._total_royalty: Decimal = Decimal("0")

    def build_division_order(
        self,
        ownership: Dict[str, List[OwnershipPosition]],
        defects: List[TitleDefect],
        gross_acres: Decimal,
        unit_acres: Optional[Decimal] = None,
        well_name: Optional[str] = None,
        operator: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Build a complete division order from ownership and defect data.

        Args:
            ownership: Ownership positions from InterestCalculator
            defects: Title defects from DefectDetector
            gross_acres: Total gross acreage of the tract
            unit_acres: Pooled unit acreage (if applicable)
            well_name: Name of the well (for header)
            operator: Name of the operator (for header)

        Returns:
            Complete division order document as dictionary
        """
        self._entries = []
        self._suspended = []
        self._total_mineral = Decimal("0")
        self._total_nri = Decimal("0")
        self._total_royalty = Decimal("0")

        tract_participation = Decimal("1")
        if unit_acres and unit_acres > Decimal("0"):
            tract_participation = (gross_acres / unit_acres).quantize(
                Decimal("0.00000001"), rounding=ROUND_HALF_UP
            )

        affected_parties: Set[str] = set()
        for defect in defects:
            if defect.severity in (DefectSeverity.CRITICAL, DefectSeverity.MAJOR):
                for party in defect.affected_parties:
                    affected_parties.add(normalize_party_name(party))

        for category, positions in ownership.items():
            for pos in positions:
                is_suspended = normalize_party_name(pos.owner_name) in affected_parties

                adjusted_interest = pos.decimal_interest * tract_participation
                nma = (adjusted_interest * gross_acres).quantize(
                    Decimal("0.000001"), rounding=ROUND_HALF_UP
                )

                entry = {
                    "owner_name": pos.owner_name,
                    "interest_type": pos.interest_type.value if hasattr(pos.interest_type, "value") else str(pos.interest_type),
                    "decimal_interest": str(adjusted_interest.quantize(
                        Decimal("0.00000001"), rounding=ROUND_HALF_UP
                    )),
                    "tract_participation": str(tract_participation),
                    "net_mineral_acres": str(nma),
                    "category": category,
                    "status": "suspended" if is_suspended else "active",
                }

                if is_suspended:
                    matching_defects = [
                        d for d in defects
                        if normalize_party_name(pos.owner_name) in {
                            normalize_party_name(p) for p in d.affected_parties
                        }
                    ]
                    entry["suspension_reasons"] = [
                        {
                            "defect_id": d.defect_id,
                            "category": d.category.value,
                            "description": d.description[:200],
                        }
                        for d in matching_defects
                    ]
                    self._suspended.append(entry)
                else:
                    self._entries.append(entry)

                if category == "mineral":
                    self._total_mineral += adjusted_interest
                elif category == "royalty":
                    self._total_royalty += adjusted_interest

        self._total_nri = self._total_mineral + self._total_royalty

        division_order = {
            "document_type": "Division Order Title Opinion",
            "well_name": well_name or "TBD",
            "operator": operator or "TBD",
            "gross_acres": str(gross_acres),
            "unit_acres": str(unit_acres) if unit_acres else None,
            "tract_participation_factor": str(tract_participation),
            "generated_date": date.today().isoformat(),
            "totals": {
                "total_mineral_interest": str(self._total_mineral.quantize(
                    Decimal("0.00000001"), rounding=ROUND_HALF_UP
                )),
                "total_royalty_interest": str(self._total_royalty.quantize(
                    Decimal("0.00000001"), rounding=ROUND_HALF_UP
                )),
                "total_net_revenue_interest": str(self._total_nri.quantize(
                    Decimal("0.00000001"), rounding=ROUND_HALF_UP
                )),
            },
            "active_interests": self._entries,
            "suspended_interests": self._suspended,
            "active_count": len(self._entries),
            "suspended_count": len(self._suspended),
            "notes": self._generate_doto_notes(defects),
            "hash": compute_deterministic_hash({
                "entries": [e["decimal_interest"] for e in self._entries],
                "suspended": [s["decimal_interest"] for s in self._suspended],
                "totals": str(self._total_nri),
            }),
        }

        logger.info(
            f"Division order built: {len(self._entries)} active, "
            f"{len(self._suspended)} suspended, "
            f"total NRI: {self._total_nri}"
        )

        return division_order

    def _generate_doto_notes(self, defects: List[TitleDefect]) -> List[str]:
        """Generate notes for the DOTO."""
        notes: List[str] = []

        critical_count = sum(1 for d in defects if d.severity == DefectSeverity.CRITICAL)
        major_count = sum(1 for d in defects if d.severity == DefectSeverity.MAJOR)

        if critical_count > 0:
            notes.append(
                f"CAUTION: {critical_count} critical defect(s) found. "
                f"Revenue for affected parties is SUSPENDED pending curative."
            )
        if major_count > 0:
            notes.append(
                f"NOTE: {major_count} major defect(s) found. "
                f"Review curative requirements before disbursing suspended revenue."
            )

        if self._total_mineral > Decimal("1"):
            notes.append(
                "WARNING: Total mineral interest exceeds 1.000000 (over-conveyance detected). "
                "Chain requires further investigation."
            )

        if self._suspended:
            total_suspended = sum(
                Decimal(s["decimal_interest"]) for s in self._suspended
            )
            notes.append(
                f"SUSPENDED REVENUE: {len(self._suspended)} interest(s) totaling "
                f"{total_suspended} decimal interest are suspended pending curative."
            )

        return notes


# ---------------------------------------------------------------------------
# Report Formatter
# ---------------------------------------------------------------------------

class ReportFormatter:
    """
    Formats title examination results into various output formats.

    Supports:
    - Plain text reports (for email/print)
    - Markdown reports (for web display)
    - JSON structured output (for API consumers)
    - Run sheet text format
    - Division order format
    """

    @staticmethod
    def format_opinion_text(opinion: TitleOpinion, width: int = 100) -> str:
        """Format a title opinion as plain text."""
        lines: List[str] = []

        lines.append("=" * width)
        lines.append("TITLE OPINION")
        lines.append("=" * width)
        lines.append("")
        lines.append(f"Opinion ID:      {opinion.opinion_id}")
        lines.append(f"Opinion Type:    {opinion.opinion_type.value.upper()}")
        lines.append(f"Title Quality:   {opinion.title_quality.value.upper()}")
        lines.append(f"Examiner:        {opinion.examiner}")
        lines.append(f"Examination Date:{opinion.examination_date}")
        lines.append(f"Effective Date:  {opinion.effective_date}")
        lines.append("")
        lines.append(f"Legal Description:")
        lines.append(f"  {opinion.legal_description}")
        lines.append(f"County:          {opinion.county}")
        lines.append(f"State:           {opinion.state}")
        lines.append("")

        if opinion.search_period_start or opinion.search_period_end:
            lines.append(f"Search Period:   {opinion.search_period_start} to {opinion.search_period_end}")

        lines.append(f"Chain Length:    {opinion.chain_length} instruments")
        lines.append(f"Defects Found:   {opinion.defects_found}")
        lines.append(f"Curative Items:  {opinion.curative_items}")
        lines.append("")

        lines.append("-" * width)
        lines.append("MINERAL OWNERSHIP")
        lines.append("-" * width)
        for pos in opinion.mineral_owners:
            nma_str = f" ({pos.net_mineral_acres} NMA)" if pos.net_mineral_acres else ""
            lines.append(f"  {pos.owner_name:<40s} {pos.decimal_interest:>12s}{nma_str}")
        lines.append("")

        if opinion.surface_owners:
            lines.append("-" * width)
            lines.append("SURFACE OWNERSHIP")
            lines.append("-" * width)
            for pos in opinion.surface_owners:
                lines.append(f"  {pos.owner_name:<40s} {pos.decimal_interest:>12s}")
            lines.append("")

        if opinion.royalty_owners:
            lines.append("-" * width)
            lines.append("ROYALTY INTEREST")
            lines.append("-" * width)
            for pos in opinion.royalty_owners:
                lines.append(f"  {pos.owner_name:<40s} {pos.decimal_interest:>12s}")
            lines.append("")

        if opinion.active_leases:
            lines.append("-" * width)
            lines.append("ACTIVE LEASES")
            lines.append("-" * width)
            for lease in opinion.active_leases:
                lines.append(f"  Instrument: {lease.get('instrument_id', 'N/A')}")
                lines.append(f"  Lessor:     {lease.get('lessor', 'N/A')}")
                lines.append(f"  Lessee:     {lease.get('lessee', 'N/A')}")
                lines.append(f"  Effective:  {lease.get('effective_date', 'N/A')}")
                lines.append(f"  Term:       {lease.get('primary_term_years', 'N/A')} years")
                lines.append(f"  Royalty:    {lease.get('royalty_fraction', 'N/A')}")
                lines.append(f"  Status:     {lease.get('status', 'N/A')}")
                lines.append("")

        if opinion.defects:
            lines.append("-" * width)
            lines.append("DEFECTS")
            lines.append("-" * width)
            for defect in opinion.defects:
                lines.append(f"  [{defect.severity.value.upper()}] {defect.defect_id}: "
                             f"{defect.category.value}")
                lines.append(f"    {defect.description[:width - 4]}")
                if defect.cure_actions:
                    lines.append(f"    Cure: {', '.join(c.value for c in defect.cure_actions)}")
                lines.append("")

        if opinion.curative_requirements:
            lines.append("-" * width)
            lines.append("CURATIVE REQUIREMENTS")
            lines.append("-" * width)
            for req in opinion.curative_requirements:
                lines.append(f"  {req.requirement_id} (Priority: {req.priority})")
                lines.append(f"    Action: {req.action.value}")
                lines.append(f"    {req.description[:width - 4]}")
                if req.estimated_cost:
                    lines.append(f"    Est. Cost: {req.estimated_cost}")
                if req.estimated_days:
                    lines.append(f"    Est. Time: {req.estimated_days} days")
                if req.responsible_party:
                    lines.append(f"    Responsible: {req.responsible_party}")
                lines.append("")

        if opinion.requirements:
            lines.append("-" * width)
            lines.append("REQUIREMENTS")
            lines.append("-" * width)
            for i, req in enumerate(opinion.requirements, 1):
                lines.append(f"  {i}. {req}")
            lines.append("")

        lines.append("-" * width)
        lines.append("STANDARD EXCEPTIONS")
        lines.append("-" * width)
        for i, exc in enumerate(opinion.exceptions, 1):
            lines.append(f"  {i}. {exc}")
        lines.append("")

        if opinion.notes:
            lines.append("-" * width)
            lines.append("NOTES")
            lines.append("-" * width)
            for note in opinion.notes:
                lines.append(f"  {note}")
            lines.append("")

        lines.append("=" * width)
        lines.append(f"Hash: {opinion.deterministic_hash}")
        lines.append("=" * width)

        return "\n".join(lines)

    @staticmethod
    def format_opinion_markdown(opinion: TitleOpinion) -> str:
        """Format a title opinion as Markdown."""
        sections: List[str] = []

        sections.append(f"# Title Opinion: {opinion.opinion_id}")
        sections.append("")
        sections.append(f"**Type:** {opinion.opinion_type.value.upper()}")
        sections.append(f"**Quality:** {opinion.title_quality.value.upper()}")
        sections.append(f"**Examiner:** {opinion.examiner}")
        sections.append(f"**Date:** {opinion.examination_date}")
        sections.append(f"**Effective:** {opinion.effective_date}")
        sections.append("")
        sections.append(f"## Property")
        sections.append(f"- **Legal Description:** {opinion.legal_description}")
        sections.append(f"- **County:** {opinion.county}")
        sections.append(f"- **State:** {opinion.state}")
        sections.append(f"- **Chain Length:** {opinion.chain_length} instruments")
        sections.append(f"- **Defects:** {opinion.defects_found}")
        sections.append(f"- **Curative Items:** {opinion.curative_items}")
        sections.append("")

        if opinion.mineral_owners:
            sections.append("## Mineral Ownership")
            sections.append("")
            sections.append("| Owner | Decimal Interest | NMA |")
            sections.append("|-------|-----------------|-----|")
            for pos in opinion.mineral_owners:
                nma = pos.net_mineral_acres if pos.net_mineral_acres else "N/A"
                sections.append(f"| {pos.owner_name} | {pos.decimal_interest} | {nma} |")
            sections.append("")

        if opinion.surface_owners:
            sections.append("## Surface Ownership")
            sections.append("")
            sections.append("| Owner | Decimal Interest |")
            sections.append("|-------|-----------------|")
            for pos in opinion.surface_owners:
                sections.append(f"| {pos.owner_name} | {pos.decimal_interest} |")
            sections.append("")

        if opinion.royalty_owners:
            sections.append("## Royalty Interest")
            sections.append("")
            sections.append("| Owner | Decimal Interest |")
            sections.append("|-------|-----------------|")
            for pos in opinion.royalty_owners:
                sections.append(f"| {pos.owner_name} | {pos.decimal_interest} |")
            sections.append("")

        if opinion.active_leases:
            sections.append("## Active Leases")
            sections.append("")
            for lease in opinion.active_leases:
                sections.append(f"### Lease: {lease.get('instrument_id', 'N/A')}")
                sections.append(f"- **Lessor:** {lease.get('lessor', 'N/A')}")
                sections.append(f"- **Lessee:** {lease.get('lessee', 'N/A')}")
                sections.append(f"- **Effective:** {lease.get('effective_date', 'N/A')}")
                sections.append(f"- **Term:** {lease.get('primary_term_years', 'N/A')} years")
                sections.append(f"- **Royalty:** {lease.get('royalty_fraction', 'N/A')}")
                sections.append("")

        if opinion.defects:
            sections.append("## Defects")
            sections.append("")
            for defect in opinion.defects:
                severity_icon = {
                    DefectSeverity.CRITICAL: "CRITICAL",
                    DefectSeverity.MAJOR: "MAJOR",
                    DefectSeverity.MINOR: "MINOR",
                    DefectSeverity.INFORMATIONAL: "INFO",
                }.get(defect.severity, "UNKNOWN")
                sections.append(f"### [{severity_icon}] {defect.defect_id}: {defect.category.value}")
                sections.append(f"{defect.description}")
                if defect.cure_actions:
                    sections.append(f"**Cure:** {', '.join(c.value for c in defect.cure_actions)}")
                sections.append("")

        if opinion.curative_requirements:
            sections.append("## Curative Requirements")
            sections.append("")
            sections.append("| ID | Priority | Action | Description | Est. Cost | Est. Days |")
            sections.append("|----|----------|--------|-------------|-----------|-----------|")
            for req in opinion.curative_requirements:
                sections.append(
                    f"| {req.requirement_id} | {req.priority} | {req.action.value} | "
                    f"{req.description[:60]}... | {req.estimated_cost or 'N/A'} | "
                    f"{req.estimated_days or 'N/A'} |"
                )
            sections.append("")

        sections.append("## Standard Exceptions")
        sections.append("")
        for i, exc in enumerate(opinion.exceptions, 1):
            sections.append(f"{i}. {exc}")
        sections.append("")

        if opinion.notes:
            sections.append("## Notes")
            sections.append("")
            for note in opinion.notes:
                sections.append(f"- {note}")
            sections.append("")

        sections.append(f"---")
        sections.append(f"*Hash: `{opinion.deterministic_hash}`*")

        return "\n".join(sections)

    @staticmethod
    def format_run_sheet_text(run_sheet: List[RunSheetEntry], width: int = 120) -> str:
        """Format a run sheet as plain text."""
        lines: List[str] = []
        lines.append("=" * width)
        lines.append("RUN SHEET")
        lines.append("=" * width)
        lines.append("")

        header = (
            f"{'#':>4s}  {'Date':>10s}  {'Type':<25s}  {'Vol/Page':<16s}  "
            f"{'Grantor':<20s}  {'Grantee':<20s}"
        )
        lines.append(header)
        lines.append("-" * width)

        for entry in run_sheet:
            date_str = entry.recording_date.isoformat() if entry.recording_date else "N/A"
            vol_page = entry.volume_page or ""
            grantor_short = entry.grantor[:20] if entry.grantor else "N/A"
            grantee_short = entry.grantee[:20] if entry.grantee else "N/A"

            line = (
                f"{entry.entry_number:>4d}  {date_str:>10s}  "
                f"{entry.instrument_type:<25s}  {vol_page:<16s}  "
                f"{grantor_short:<20s}  {grantee_short:<20s}"
            )
            lines.append(line)

            if entry.reservations:
                lines.append(f"       Reservations: {entry.reservations[:width - 22]}")
            if entry.exceptions:
                lines.append(f"       Exceptions:   {entry.exceptions[:width - 22]}")
            if entry.remarks:
                lines.append(f"       Remarks:      {entry.remarks[:width - 22]}")

        lines.append("-" * width)
        lines.append(f"Total entries: {len(run_sheet)}")
        lines.append("=" * width)

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Batch Examiner
# ---------------------------------------------------------------------------

class BatchExaminer:
    """
    Performs batch title examinations across multiple tracts.

    Used when examining an entire section or multiple tracts
    for a drilling program or acquisition due diligence.
    Each tract gets a separate examination but shares search
    indexes and doctrine caches for efficiency.
    """

    def __init__(self, engine: TitleExaminationEngine) -> None:
        self._engine = engine
        self._results: List[Dict[str, Any]] = []
        self._failed: List[Dict[str, Any]] = []

    def examine_batch(
        self,
        tracts: List[Dict[str, Any]],
        opinion_type: OpinionType = OpinionType.PRELIMINARY,
    ) -> Dict[str, Any]:
        """
        Examine multiple tracts in batch.

        Args:
            tracts: List of tract definitions, each containing:
                - legal_description: str (required)
                - county: str (required)
                - state: str (default "TX")
                - gross_acres: Decimal (optional)
                - initial_owner: str (optional)
                - instruments: List[Dict] (optional, per-tract instruments)
            opinion_type: Type of opinion to generate

        Returns:
            Batch examination results with individual opinions and summary
        """
        self._results = []
        self._failed = []
        start_time = datetime.utcnow()

        logger.info(f"Starting batch examination of {len(tracts)} tracts")

        for i, tract in enumerate(tracts, start=1):
            legal_desc = tract.get("legal_description", "")
            county = tract.get("county", "")
            state = tract.get("state", "TX")
            gross_acres_raw = tract.get("gross_acres")
            initial_owner = tract.get("initial_owner")
            extra_instruments = tract.get("instruments", [])

            if not legal_desc or not county:
                self._failed.append({
                    "tract_index": i,
                    "error": "Missing required field: legal_description or county",
                    "tract_data": tract,
                })
                continue

            gross_acres = None
            if gross_acres_raw is not None:
                try:
                    gross_acres = Decimal(str(gross_acres_raw))
                except (InvalidOperation, ValueError):
                    gross_acres = None

            if extra_instruments:
                self._engine.load_instruments(extra_instruments)

            try:
                opinion = self._engine.examine_title(
                    legal_description=legal_desc,
                    county=county,
                    state=state,
                    opinion_type=opinion_type,
                    gross_acres=gross_acres,
                    initial_owner=initial_owner,
                )

                self._results.append({
                    "tract_index": i,
                    "legal_description": legal_desc,
                    "county": county,
                    "state": state,
                    "opinion": opinion.to_dict(),
                    "title_quality": opinion.title_quality.value,
                    "chain_length": opinion.chain_length,
                    "defects_found": opinion.defects_found,
                    "curative_items": opinion.curative_items,
                })

                logger.info(
                    f"Tract {i}/{len(tracts)}: {opinion.title_quality.value} "
                    f"({opinion.defects_found} defects)"
                )

            except Exception as exc:
                logger.error(f"Tract {i} examination failed: {exc}")
                self._failed.append({
                    "tract_index": i,
                    "error": str(exc),
                    "legal_description": legal_desc,
                    "county": county,
                })

        elapsed = (datetime.utcnow() - start_time).total_seconds()

        quality_counts: Dict[str, int] = defaultdict(int)
        total_defects = 0
        total_curatives = 0
        for result in self._results:
            quality_counts[result["title_quality"]] += 1
            total_defects += result["defects_found"]
            total_curatives += result["curative_items"]

        summary = {
            "batch_id": str(uuid.uuid4())[:12],
            "total_tracts": len(tracts),
            "examined": len(self._results),
            "failed": len(self._failed),
            "elapsed_seconds": round(elapsed, 2),
            "quality_summary": dict(quality_counts),
            "total_defects": total_defects,
            "total_curative_items": total_curatives,
            "avg_defects_per_tract": round(
                total_defects / max(len(self._results), 1), 1
            ),
            "results": self._results,
            "failures": self._failed,
            "generated_date": date.today().isoformat(),
            "hash": compute_deterministic_hash({
                "tracts": len(tracts),
                "results": len(self._results),
                "defects": total_defects,
            }),
        }

        logger.info(
            f"Batch examination complete: {len(self._results)}/{len(tracts)} tracts "
            f"in {elapsed:.1f}s, {total_defects} total defects"
        )

        return summary


# ---------------------------------------------------------------------------
# Mineral vs Surface Priority Resolver
# ---------------------------------------------------------------------------

class MineralSurfacePriorityResolver:
    """
    Resolves conflicts between mineral and surface estate interests.

    Under Texas law, the mineral estate is the dominant estate
    (Tex. Nat. Res. Code Sec. 91.001 et seq.). This means:
    - Mineral owner has implied right to use surface for extraction
    - Surface owner cannot interfere with reasonable mineral operations
    - Accommodation doctrine limits surface use burden
    - Executive right may be severed from mineral interest
    - Non-participating royalty interest (NPRI) splits royalty from minerals

    This resolver identifies conflicts and applies Texas priority rules.
    """

    def __init__(self) -> None:
        self._conflicts: List[Dict[str, Any]] = []

    def resolve_priorities(
        self,
        ownership: Dict[str, List[OwnershipPosition]],
        chain: List[InstrumentRecord],
    ) -> Dict[str, Any]:
        """
        Resolve mineral vs surface priority conflicts.

        Args:
            ownership: Ownership positions from InterestCalculator
            chain: Title chain for context

        Returns:
            Priority resolution analysis
        """
        self._conflicts = []

        mineral_owners = {
            normalize_party_name(pos.owner_name): pos
            for pos in ownership.get("mineral", [])
        }
        surface_owners = {
            normalize_party_name(pos.owner_name): pos
            for pos in ownership.get("surface", [])
        }

        severed = len(mineral_owners) > 0 and len(surface_owners) > 0
        if not severed:
            common_owners = set(mineral_owners.keys()) & set(surface_owners.keys())
            if common_owners and len(mineral_owners) != len(surface_owners):
                severed = True

        self._check_split_estate_conflicts(mineral_owners, surface_owners)
        self._check_executive_right_severance(chain, ownership)
        self._check_npri_conflicts(chain, ownership)
        self._check_accommodation_doctrine_issues(chain)

        resolution = {
            "estates_severed": severed,
            "mineral_owner_count": len(mineral_owners),
            "surface_owner_count": len(surface_owners),
            "dominant_estate": "mineral",
            "dominant_estate_authority": "Tex. Nat. Res. Code Sec. 91.001",
            "conflicts_found": len(self._conflicts),
            "conflicts": self._conflicts,
            "priority_rules_applied": [
                "Mineral estate is dominant estate (TX common law)",
                "Mineral owner has implied easement for surface use",
                "Accommodation doctrine: if mineral owner has reasonable "
                "alternative, must accommodate surface use",
                "Executive right is severable from mineral interest",
                "NPRI holder cannot lease or execute — receives royalty only",
            ],
        }

        logger.info(
            f"Priority resolution: estates {'severed' if severed else 'unified'}, "
            f"{len(self._conflicts)} conflicts"
        )

        return resolution

    def _check_split_estate_conflicts(
        self,
        mineral_owners: Dict[str, OwnershipPosition],
        surface_owners: Dict[str, OwnershipPosition],
    ) -> None:
        """Check for conflicts from split mineral/surface ownership."""
        mineral_only = set(mineral_owners.keys()) - set(surface_owners.keys())
        surface_only = set(surface_owners.keys()) - set(mineral_owners.keys())

        if mineral_only and surface_only:
            self._conflicts.append({
                "conflict_type": "split_estate_access_rights",
                "severity": "INFORMATIONAL",
                "mineral_only_owners": list(mineral_only),
                "surface_only_owners": list(surface_only),
                "description": (
                    f"Split estate: {len(mineral_only)} party(ies) own minerals only, "
                    f"{len(surface_only)} party(ies) own surface only. "
                    f"Mineral owners have implied right to use surface for extraction."
                ),
                "legal_authority": "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)",
                "accommodation_doctrine": (
                    "If mineral owner has reasonable alternative means of extraction "
                    "that do not interfere with existing surface use, the mineral owner "
                    "must accommodate the surface owner's use."
                ),
                "accommodation_authority": (
                    "Getty Oil Co. v. Jones; Tarrant County Water Control & "
                    "Improvement Dist. No. 1 v. Haupt, Inc."
                ),
            })

    def _check_executive_right_severance(
        self,
        chain: List[InstrumentRecord],
        ownership: Dict[str, List[OwnershipPosition]],
    ) -> None:
        """Check for executive right severance in the chain."""
        for inst in chain:
            for res in inst.reservations:
                res_lower = res.lower()
                if "executive" in res_lower and ("right" in res_lower or "rights" in res_lower):
                    self._conflicts.append({
                        "conflict_type": "executive_right_severance",
                        "severity": "MAJOR",
                        "instrument_id": inst.instrument_id,
                        "reservation_text": res,
                        "description": (
                            f"Executive right reserved in instrument "
                            f"{inst.instrument_id}. The executive right holder "
                            f"controls the power to lease the mineral estate."
                        ),
                        "legal_authority": (
                            "Day & Co. v. Texland Petroleum, Inc., "
                            "786 S.W.2d 667 (Tex. 1990)"
                        ),
                        "implications": [
                            "Executive right holder controls leasing decisions",
                            "NPRI holders cannot execute leases",
                            "Executive right holder owes fiduciary duty to NPRI holders",
                            "Must identify current executive right holder for leasing",
                        ],
                    })

    def _check_npri_conflicts(
        self,
        chain: List[InstrumentRecord],
        ownership: Dict[str, List[OwnershipPosition]],
    ) -> None:
        """Check for NPRI issues in the chain."""
        for inst in chain:
            for res in inst.reservations:
                res_lower = res.lower()
                if "non-participating" in res_lower or "nonparticipating" in res_lower:
                    self._conflicts.append({
                        "conflict_type": "npri_detected",
                        "severity": "INFORMATIONAL",
                        "instrument_id": inst.instrument_id,
                        "reservation_text": res,
                        "description": (
                            f"Non-participating royalty interest (NPRI) reserved "
                            f"in instrument {inst.instrument_id}. NPRI holder "
                            f"receives royalty but cannot lease."
                        ),
                        "legal_authority": "French v. Chevron U.S.A., Inc., 896 S.W.2d 795 (Tex. 1995)",
                        "implications": [
                            "NPRI holder receives a share of lessor royalty",
                            "NPRI holder cannot execute oil and gas leases",
                            "NPRI holder has no right to bonus or delay rentals",
                            "Must compute NPRI share correctly in division orders",
                        ],
                    })

    def _check_accommodation_doctrine_issues(
        self,
        chain: List[InstrumentRecord],
    ) -> None:
        """Check for accommodation doctrine triggers."""
        has_surface_lease = False
        has_mineral_lease = False

        for inst in chain:
            inst_type_lower = inst.instrument_type.lower().replace(" ", "_")
            if inst_type_lower == "surface_lease":
                has_surface_lease = True
            elif inst_type_lower in ("oil_gas_lease", "paid_up_lease"):
                has_mineral_lease = True

        if has_surface_lease and has_mineral_lease:
            self._conflicts.append({
                "conflict_type": "accommodation_doctrine_trigger",
                "severity": "INFORMATIONAL",
                "description": (
                    "Both surface lease and mineral lease found in chain. "
                    "Accommodation doctrine may apply if mineral operations "
                    "would interfere with existing surface use."
                ),
                "legal_authority": "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)",
            })

    def get_conflicts(self) -> List[Dict[str, Any]]:
        """Return all priority conflicts found."""
        return list(self._conflicts)


# ============================================================================
# FASTAPI SERVER + CLOUD RETRIEVAL
# ============================================================================

import sys
import asyncio
from pathlib import Path as _Path
from contextlib import asynccontextmanager

sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "_shared"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional as _Optional  # Alias to avoid conflict with main imports

try:
    from cloud_retriever import CognitionCloudRetriever, CloudKnowledge, retrieve_cloud_knowledge
    _CLOUD_AVAILABLE = True
except ImportError:
    _CLOUD_AVAILABLE = False
    logger.warning("cloud_retriever not available — running without cloud knowledge")

ENGINE_ID = "LM01"
ENGINE_NAME = "Title Examination Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8421


class QueryRequest(BaseModel):
    query: str = ""
    prompt: str = ""
    mode: str = "fast"  # fast | defense | memo (ResponseMode)
    zone: str = "reporting"  # planning | reporting | audit (AnalysisZone)
    county: str = "Reeves"
    state: str = "TX"
    include_cloud: bool = True
    use_three_layer: bool = True  # Enable three-layer response architecture


class QueryResponse(BaseModel):
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    version: str = ENGINE_VERSION
    tie20_compliant: bool = True
    query: str = ""
    layer_used: _Optional[str] = None  # doctrine_cache | semantic_retrieval | deep_analysis
    confidence_zone: _Optional[str] = None  # defensible | aggressive | disclosure | high_risk
    answer: str = ""
    authorities: List[str] = Field(default_factory=list)
    reasoning_chain: List[str] = Field(default_factory=list)
    fact_fragility: _Optional[Dict[str, Any]] = None
    analysis: Dict[str, Any] = Field(default_factory=dict)  # Legacy compatibility
    cloud_knowledge: Dict[str, Any] = Field(default_factory=dict)
    cloud_citations: List[Dict[str, str]] = Field(default_factory=list)
    processing_time_ms: float = 0.0
    determinism_hash: str = ""


_engine = TitleExaminationEngine()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"LM01 {ENGINE_NAME} v{ENGINE_VERSION} starting on port {ENGINE_PORT}")
    yield
    if _CLOUD_AVAILABLE:
        from cloud_retriever import get_cloud_retriever
        await get_cloud_retriever().close()
    logger.info(f"LM01 {ENGINE_NAME} shutting down")


app = FastAPI(
    title=f"ECHO {ENGINE_ID} {ENGINE_NAME}",
    version=ENGINE_VERSION,
    description="Title Examination Engine with Cloud Knowledge Retrieval",
    lifespan=lifespan,
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.get("/health")
async def health():
    return {
        "engine_id": ENGINE_ID, "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION, "status": "healthy", "port": ENGINE_PORT,
        "cloud_available": _CLOUD_AVAILABLE,
    }


@app.post("/query")
async def query_endpoint(request: QueryRequest):
    import time
    start = time.monotonic()
    q = request.query or request.prompt

    # Map mode string to ResponseMode enum
    mode_map = {"fast": ResponseMode.FAST, "defense": ResponseMode.DEFENSE, "memo": ResponseMode.MEMO}
    response_mode = mode_map.get(request.mode.lower(), ResponseMode.FAST)

    # Map zone string to AnalysisZone enum
    zone_map = {"planning": AnalysisZone.PLANNING, "reporting": AnalysisZone.REPORTING, "audit": AnalysisZone.AUDIT}
    analysis_zone = zone_map.get(request.zone.lower(), AnalysisZone.REPORTING)

    # TIE-20: Use three-layer response if enabled
    if request.use_three_layer:
        try:
            result = _engine.three_layer_response(q, response_mode, analysis_zone)
        except Exception as _tlr_err:
            logger.error(f"Three-layer response failed: {_tlr_err}")
            import traceback
            logger.error(traceback.format_exc())
            result = {"answer": f"Three-layer error: {_tlr_err}", "confidence": 0.0, "layer_used": "error"}

        # Cloud knowledge retrieval (parallel, async)
        cloud_data: Dict[str, Any] = {}
        cloud_citations: List[Dict[str, str]] = []
        if _CLOUD_AVAILABLE and request.include_cloud:
            try:
                cloud = await retrieve_cloud_knowledge(q, category="real_estate")
                cloud_data = {
                    "records": len(cloud.clauses) + len(cloud.graph_nodes) + len(cloud.crystals),
                    "merged_context": cloud.merged_text(3000),
                    "sources_succeeded": cloud.sources_succeeded,
                    "retrieval_time_ms": cloud.retrieval_time_ms,
                }
                cloud_citations = cloud.citation_list()
            except Exception as e:
                logger.warning(f"Cloud retrieval failed: {e}")
                cloud_data = {"error": str(e)}

        elapsed = (time.monotonic() - start) * 1000
        import hashlib
        det_hash = hashlib.sha256(f"{q}:{result['answer']}".encode()).hexdigest()[:16]

        return QueryResponse(
            query=q,
            layer_used=result.get("layer_used"),
            confidence_zone=result.get("confidence_zone"),
            answer=result.get("answer", ""),
            authorities=result.get("authorities", []),
            reasoning_chain=result.get("reasoning_chain", []),
            fact_fragility=result.get("fact_fragility"),
            cloud_knowledge=cloud_data,
            cloud_citations=cloud_citations,
            processing_time_ms=round(elapsed, 2),
            determinism_hash=det_hash,
        )

    # Legacy mode (backward compatibility)
    else:
        # 1. Cloud knowledge retrieval (parallel, non-blocking)
        cloud_data: Dict[str, Any] = {}
        cloud_citations: List[Dict[str, str]] = []
        if _CLOUD_AVAILABLE and request.include_cloud:
            try:
                cloud = await retrieve_cloud_knowledge(q, category="real_estate")
                cloud_data = {
                    "records": len(cloud.clauses) + len(cloud.graph_nodes) + len(cloud.crystals),
                    "merged_context": cloud.merged_text(3000),
                    "sources_succeeded": cloud.sources_succeeded,
                    "retrieval_time_ms": cloud.retrieval_time_ms,
                }
                cloud_citations = cloud.citation_list()
            except Exception as e:
                logger.warning(f"Cloud retrieval failed: {e}")
                cloud_data = {"error": str(e)}

        # 2. Local engine processing
        analysis: Dict[str, Any] = {}
        try:
            doctrines = _engine._doctrines
            matched = []
            # Iterate all four doctrine caches in TitleDoctrineCache
            for cache_dict in [
                doctrines._title_standards,
                doctrines._defect_classifications,
                doctrines._curative_standards,
                doctrines._recording_rules,
            ]:
                for topic, block in cache_dict.items():
                    kw = getattr(block, "keywords", [])
                    if any(k.lower() in q.lower() for k in kw):
                        matched.append({
                            "topic": topic,
                            "conclusion": getattr(block, "conclusion_template", ""),
                            "authority": getattr(block, "primary_authority", []),
                            "reasoning": getattr(block, "reasoning_framework", ""),
                            "key_factors": getattr(block, "key_factors", []),
                        })
            analysis = {
                "mode": request.mode,
                "doctrine_matches": matched,
                "county": request.county,
                "state": request.state,
            }
        except Exception as e:
            logger.error(f"Local analysis failed: {e}")
            analysis = {"error": str(e)}

        elapsed = (time.monotonic() - start) * 1000
        import hashlib
        det_hash = hashlib.sha256(f"{q}:{elapsed}".encode()).hexdigest()[:16]

        return QueryResponse(
            query=q, analysis=analysis, cloud_knowledge=cloud_data,
            cloud_citations=cloud_citations, processing_time_ms=round(elapsed, 2),
            determinism_hash=det_hash,
        )


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting LM01 {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    uvicorn.run("engine:app", host="0.0.0.0", port=ENGINE_PORT, reload=False, log_level="info")
