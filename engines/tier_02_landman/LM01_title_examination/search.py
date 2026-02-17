"""
LM01 Title Examination Engine - Search Module
===============================================

Search functionality for title examination records.

Supports:
- Grantor/grantee name search with fuzzy matching
- Legal description search
- Date range filtering
- Instrument type filtering
- Volume/page and document number lookup
- Relevance scoring
- Grantor-grantee index construction
- Chain of title traversal search
- Wildcard and phonetic matching

Author: ECHO OMEGA PRIME Build System
Engine: LM01 Title Examination
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from loguru import logger

from semantic import (
    TitleSemanticDictionary,
    normalize_party_name,
    name_similarity_score,
    is_entity_name,
    parse_legal_description,
)


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class SearchField(str, Enum):
    """Fields that can be searched."""
    GRANTOR = "grantor"
    GRANTEE = "grantee"
    LEGAL_DESCRIPTION = "legal_description"
    INSTRUMENT_TYPE = "instrument_type"
    RECORDING_DATE = "recording_date"
    VOLUME_PAGE = "volume_page"
    DOCUMENT_NUMBER = "document_number"
    CONSIDERATION = "consideration"
    FULL_TEXT = "full_text"


class SortOrder(str, Enum):
    """Sort order for search results."""
    RELEVANCE_DESC = "relevance_desc"
    DATE_ASC = "date_asc"
    DATE_DESC = "date_desc"
    GRANTOR_ASC = "grantor_asc"
    GRANTEE_ASC = "grantee_asc"
    VOLUME_PAGE_ASC = "volume_page_asc"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class SearchQuery:
    """A structured search query for title records."""
    query_id: str = ""
    grantor_name: Optional[str] = None
    grantee_name: Optional[str] = None
    legal_description: Optional[str] = None
    instrument_types: List[str] = field(default_factory=list)
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    volume: Optional[str] = None
    page: Optional[str] = None
    document_number: Optional[str] = None
    county: Optional[str] = None
    state: Optional[str] = None
    full_text: Optional[str] = None
    fuzzy_matching: bool = True
    fuzzy_threshold: float = 0.80
    max_results: int = 50
    offset: int = 0
    sort_order: SortOrder = SortOrder.RELEVANCE_DESC
    include_related: bool = False

    def __post_init__(self) -> None:
        if not self.query_id:
            self.query_id = self._generate_id()

    def _generate_id(self) -> str:
        components = [
            self.grantor_name or "",
            self.grantee_name or "",
            self.legal_description or "",
            ",".join(self.instrument_types),
            str(self.date_from) if self.date_from else "",
            str(self.date_to) if self.date_to else "",
            self.document_number or "",
        ]
        hash_input = "query:" + "|".join(components)
        return hashlib.sha256(hash_input.encode()).hexdigest()[:12]

    def has_criteria(self) -> bool:
        """Check if query has any search criteria."""
        return any([
            self.grantor_name,
            self.grantee_name,
            self.legal_description,
            self.instrument_types,
            self.date_from,
            self.date_to,
            self.volume,
            self.page,
            self.document_number,
            self.full_text,
        ])

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query_id": self.query_id,
            "grantor_name": self.grantor_name,
            "grantee_name": self.grantee_name,
            "legal_description": self.legal_description,
            "instrument_types": self.instrument_types,
            "date_from": self.date_from.isoformat() if self.date_from else None,
            "date_to": self.date_to.isoformat() if self.date_to else None,
            "volume": self.volume,
            "page": self.page,
            "document_number": self.document_number,
            "county": self.county,
            "state": self.state,
            "full_text": self.full_text,
            "fuzzy_matching": self.fuzzy_matching,
            "fuzzy_threshold": self.fuzzy_threshold,
            "max_results": self.max_results,
            "offset": self.offset,
            "sort_order": self.sort_order.value,
            "include_related": self.include_related,
        }


@dataclass
class SearchResult:
    """A single search result with relevance scoring."""
    instrument_id: str
    instrument_type: str
    recording_date: Optional[date]
    volume: Optional[str]
    page: Optional[str]
    document_number: Optional[str]
    grantors: List[str]
    grantees: List[str]
    legal_description: Optional[str]
    county: Optional[str]
    state: Optional[str]
    relevance_score: float = 0.0
    match_fields: List[str] = field(default_factory=list)
    match_details: Dict[str, Any] = field(default_factory=dict)
    interests_conveyed: List[Dict[str, Any]] = field(default_factory=list)
    reservations: List[str] = field(default_factory=list)
    consideration: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "instrument_id": self.instrument_id,
            "instrument_type": self.instrument_type,
            "recording_date": self.recording_date.isoformat() if self.recording_date else None,
            "volume": self.volume,
            "page": self.page,
            "document_number": self.document_number,
            "grantors": self.grantors,
            "grantees": self.grantees,
            "legal_description": self.legal_description,
            "county": self.county,
            "state": self.state,
            "relevance_score": round(self.relevance_score, 4),
            "match_fields": self.match_fields,
            "match_details": self.match_details,
            "interests_conveyed": self.interests_conveyed,
            "reservations": self.reservations,
            "consideration": self.consideration,
        }


@dataclass
class SearchResponse:
    """Complete search response with metadata."""
    query: SearchQuery
    results: List[SearchResult]
    total_matches: int
    returned_count: int
    search_time_ms: float
    index_stats: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query.to_dict(),
            "results": [r.to_dict() for r in self.results],
            "total_matches": self.total_matches,
            "returned_count": self.returned_count,
            "search_time_ms": round(self.search_time_ms, 2),
            "index_stats": self.index_stats,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, default=str)


# ---------------------------------------------------------------------------
# Index Structures
# ---------------------------------------------------------------------------

@dataclass
class IndexEntry:
    """An entry in a search index."""
    instrument_id: str
    value: str
    normalized_value: str
    field_name: str
    recording_date: Optional[date] = None
    score_boost: float = 1.0


class GrantorGranteeIndex:
    """
    Inverted index for grantor and grantee name lookups.
    Supports exact match, prefix match, fuzzy match, and phonetic match.
    """

    def __init__(self) -> None:
        self._grantor_index: Dict[str, List[IndexEntry]] = defaultdict(list)
        self._grantee_index: Dict[str, List[IndexEntry]] = defaultdict(list)
        self._grantor_by_instrument: Dict[str, List[str]] = defaultdict(list)
        self._grantee_by_instrument: Dict[str, List[str]] = defaultdict(list)
        self._all_names: Set[str] = set()
        self._name_to_instruments: Dict[str, Set[str]] = defaultdict(set)
        self._entry_count: int = 0

    def add_grantor(
        self,
        instrument_id: str,
        name: str,
        recording_date: Optional[date] = None,
    ) -> None:
        """Add a grantor name to the index."""
        normalized = normalize_party_name(name)
        if not normalized:
            return

        entry = IndexEntry(
            instrument_id=instrument_id,
            value=name,
            normalized_value=normalized,
            field_name="grantor",
            recording_date=recording_date,
        )

        self._grantor_index[normalized].append(entry)
        self._grantor_by_instrument[instrument_id].append(normalized)
        self._all_names.add(normalized)
        self._name_to_instruments[normalized].add(instrument_id)
        self._entry_count += 1

        tokens = normalized.split()
        for token in tokens:
            if len(token) >= 3:
                self._grantor_index[token].append(entry)

    def add_grantee(
        self,
        instrument_id: str,
        name: str,
        recording_date: Optional[date] = None,
    ) -> None:
        """Add a grantee name to the index."""
        normalized = normalize_party_name(name)
        if not normalized:
            return

        entry = IndexEntry(
            instrument_id=instrument_id,
            value=name,
            normalized_value=normalized,
            field_name="grantee",
            recording_date=recording_date,
        )

        self._grantee_index[normalized].append(entry)
        self._grantee_by_instrument[instrument_id].append(normalized)
        self._all_names.add(normalized)
        self._name_to_instruments[normalized].add(instrument_id)
        self._entry_count += 1

        tokens = normalized.split()
        for token in tokens:
            if len(token) >= 3:
                self._grantee_index[token].append(entry)

    def search_grantor(
        self,
        name: str,
        fuzzy: bool = True,
        threshold: float = 0.80,
    ) -> List[Tuple[IndexEntry, float]]:
        """
        Search the grantor index.
        Returns list of (entry, similarity_score) tuples sorted by score.
        """
        return self._search_index(self._grantor_index, name, fuzzy, threshold)

    def search_grantee(
        self,
        name: str,
        fuzzy: bool = True,
        threshold: float = 0.80,
    ) -> List[Tuple[IndexEntry, float]]:
        """
        Search the grantee index.
        Returns list of (entry, similarity_score) tuples sorted by score.
        """
        return self._search_index(self._grantee_index, name, fuzzy, threshold)

    def _search_index(
        self,
        index: Dict[str, List[IndexEntry]],
        name: str,
        fuzzy: bool,
        threshold: float,
    ) -> List[Tuple[IndexEntry, float]]:
        """Internal search against an index."""
        normalized = normalize_party_name(name)
        results: List[Tuple[IndexEntry, float]] = []
        seen_instruments: Set[str] = set()

        if normalized in index:
            for entry in index[normalized]:
                if entry.instrument_id not in seen_instruments:
                    results.append((entry, 1.0))
                    seen_instruments.add(entry.instrument_id)

        if fuzzy and len(results) < 50:
            for indexed_name, entries in index.items():
                if indexed_name == normalized:
                    continue
                similarity = name_similarity_score(normalized, indexed_name)
                if similarity >= threshold:
                    for entry in entries:
                        if entry.instrument_id not in seen_instruments:
                            results.append((entry, similarity))
                            seen_instruments.add(entry.instrument_id)

        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def get_grantors_for_instrument(self, instrument_id: str) -> List[str]:
        """Get all grantor names for an instrument."""
        return list(self._grantor_by_instrument.get(instrument_id, []))

    def get_grantees_for_instrument(self, instrument_id: str) -> List[str]:
        """Get all grantee names for an instrument."""
        return list(self._grantee_by_instrument.get(instrument_id, []))

    def get_instruments_for_name(self, name: str) -> Set[str]:
        """Get all instrument IDs involving a name (as grantor or grantee)."""
        normalized = normalize_party_name(name)
        return self._name_to_instruments.get(normalized, set())

    def trace_chain_forward(
        self,
        start_name: str,
        max_depth: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Trace chain of title forward from a grantor.
        Follows grantee -> grantor links through the index.
        """
        normalized = normalize_party_name(start_name)
        chain: List[Dict[str, Any]] = []
        visited: Set[str] = set()
        current_names: Set[str] = {normalized}

        for depth in range(max_depth):
            if not current_names:
                break

            next_names: Set[str] = set()

            for name in current_names:
                if name in visited:
                    continue
                visited.add(name)

                entries_as_grantor = self._grantor_index.get(name, [])
                for entry in entries_as_grantor:
                    grantees = self._grantee_by_instrument.get(entry.instrument_id, [])
                    chain.append({
                        "depth": depth,
                        "instrument_id": entry.instrument_id,
                        "grantor": name,
                        "grantees": grantees,
                        "recording_date": entry.recording_date.isoformat() if entry.recording_date else None,
                    })
                    for grantee_name in grantees:
                        if grantee_name not in visited:
                            next_names.add(grantee_name)

            current_names = next_names

        return chain

    def trace_chain_backward(
        self,
        start_name: str,
        max_depth: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Trace chain of title backward from a grantee.
        Follows grantor -> grantee links backwards through the index.
        """
        normalized = normalize_party_name(start_name)
        chain: List[Dict[str, Any]] = []
        visited: Set[str] = set()
        current_names: Set[str] = {normalized}

        for depth in range(max_depth):
            if not current_names:
                break

            next_names: Set[str] = set()

            for name in current_names:
                if name in visited:
                    continue
                visited.add(name)

                entries_as_grantee = self._grantee_index.get(name, [])
                for entry in entries_as_grantee:
                    grantors = self._grantor_by_instrument.get(entry.instrument_id, [])
                    chain.append({
                        "depth": depth,
                        "instrument_id": entry.instrument_id,
                        "grantee": name,
                        "grantors": grantors,
                        "recording_date": entry.recording_date.isoformat() if entry.recording_date else None,
                    })
                    for grantor_name in grantors:
                        if grantor_name not in visited:
                            next_names.add(grantor_name)

            current_names = next_names

        chain.reverse()
        return chain

    def stats(self) -> Dict[str, int]:
        """Return index statistics."""
        return {
            "total_entries": self._entry_count,
            "unique_grantor_keys": len(self._grantor_index),
            "unique_grantee_keys": len(self._grantee_index),
            "unique_names": len(self._all_names),
            "instruments_indexed": len(
                set(self._grantor_by_instrument.keys()) |
                set(self._grantee_by_instrument.keys())
            ),
        }


# ---------------------------------------------------------------------------
# Legal Description Index
# ---------------------------------------------------------------------------

class LegalDescriptionIndex:
    """
    Index for legal description lookups.
    Supports section/block, abstract, lot/block, and text search.
    """

    def __init__(self) -> None:
        self._by_section_block: Dict[str, List[IndexEntry]] = defaultdict(list)
        self._by_abstract: Dict[str, List[IndexEntry]] = defaultdict(list)
        self._by_lot_block: Dict[str, List[IndexEntry]] = defaultdict(list)
        self._by_county: Dict[str, List[IndexEntry]] = defaultdict(list)
        self._full_text: Dict[str, IndexEntry] = {}
        self._entry_count: int = 0

    def add(
        self,
        instrument_id: str,
        legal_text: str,
        county: Optional[str] = None,
        recording_date: Optional[date] = None,
    ) -> None:
        """Index a legal description."""
        parsed = parse_legal_description(legal_text)
        entry = IndexEntry(
            instrument_id=instrument_id,
            value=legal_text,
            normalized_value=legal_text.upper().strip(),
            field_name="legal_description",
            recording_date=recording_date,
        )

        if parsed.get("section") and parsed.get("block"):
            key = f"S{parsed['section']}_B{parsed['block']}"
            self._by_section_block[key].append(entry)

        if parsed.get("abstract_number"):
            key = f"A{parsed['abstract_number']}"
            self._by_abstract[key].append(entry)

        if parsed.get("lot") and parsed.get("block"):
            key = f"L{parsed['lot']}_B{parsed['block']}"
            self._by_lot_block[key].append(entry)

        county_key = (county or parsed.get("county") or "UNKNOWN").upper()
        self._by_county[county_key].append(entry)

        self._full_text[instrument_id] = entry
        self._entry_count += 1

    def search(
        self,
        query_text: str,
        county: Optional[str] = None,
    ) -> List[Tuple[IndexEntry, float]]:
        """Search legal descriptions by text, returning (entry, score) tuples."""
        parsed = parse_legal_description(query_text)
        results: Dict[str, Tuple[IndexEntry, float]] = {}

        if parsed.get("section") and parsed.get("block"):
            key = f"S{parsed['section']}_B{parsed['block']}"
            for entry in self._by_section_block.get(key, []):
                results[entry.instrument_id] = (entry, 0.95)

        if parsed.get("abstract_number"):
            key = f"A{parsed['abstract_number']}"
            for entry in self._by_abstract.get(key, []):
                if entry.instrument_id in results:
                    old_score = results[entry.instrument_id][1]
                    results[entry.instrument_id] = (entry, min(old_score + 0.05, 1.0))
                else:
                    results[entry.instrument_id] = (entry, 0.90)

        if parsed.get("lot"):
            block = parsed.get("block", "")
            key = f"L{parsed['lot']}_B{block}"
            for entry in self._by_lot_block.get(key, []):
                if entry.instrument_id not in results:
                    results[entry.instrument_id] = (entry, 0.90)

        if county:
            county_upper = county.upper()
            county_entries = {e.instrument_id for e in self._by_county.get(county_upper, [])}
            filtered = {
                k: v for k, v in results.items()
                if k in county_entries
            }
            if filtered:
                results = filtered

        if not results:
            query_upper = query_text.upper().strip()
            for inst_id, entry in self._full_text.items():
                if query_upper in entry.normalized_value:
                    score = len(query_upper) / max(len(entry.normalized_value), 1)
                    results[inst_id] = (entry, min(score, 0.80))

        result_list = list(results.values())
        result_list.sort(key=lambda x: x[1], reverse=True)
        return result_list

    def search_by_section_block(
        self,
        section: str,
        block: str,
    ) -> List[IndexEntry]:
        """Direct lookup by section and block."""
        key = f"S{section}_B{block}"
        return self._by_section_block.get(key, [])

    def search_by_abstract(self, abstract_number: str) -> List[IndexEntry]:
        """Direct lookup by abstract number."""
        key = f"A{abstract_number}"
        return self._by_abstract.get(key, [])

    def stats(self) -> Dict[str, int]:
        return {
            "total_entries": self._entry_count,
            "section_block_keys": len(self._by_section_block),
            "abstract_keys": len(self._by_abstract),
            "lot_block_keys": len(self._by_lot_block),
            "county_keys": len(self._by_county),
        }


# ---------------------------------------------------------------------------
# Instrument Type Index
# ---------------------------------------------------------------------------

class InstrumentTypeIndex:
    """Index for instrument type filtering."""

    def __init__(self) -> None:
        self._by_type: Dict[str, Set[str]] = defaultdict(set)
        self._by_date: Dict[str, List[Tuple[str, date]]] = defaultdict(list)

    def add(
        self,
        instrument_id: str,
        instrument_type: str,
        recording_date: Optional[date] = None,
    ) -> None:
        type_upper = instrument_type.upper().replace(" ", "_")
        self._by_type[type_upper].add(instrument_id)
        if recording_date:
            self._by_date[type_upper].append((instrument_id, recording_date))

    def get_by_type(self, instrument_type: str) -> Set[str]:
        type_upper = instrument_type.upper().replace(" ", "_")
        return self._by_type.get(type_upper, set())

    def get_by_type_and_date(
        self,
        instrument_type: str,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ) -> List[str]:
        type_upper = instrument_type.upper().replace(" ", "_")
        entries = self._by_date.get(type_upper, [])
        results: List[str] = []
        for inst_id, rec_date in entries:
            if date_from and rec_date < date_from:
                continue
            if date_to and rec_date > date_to:
                continue
            results.append(inst_id)
        return results

    def stats(self) -> Dict[str, int]:
        return {
            "types_indexed": len(self._by_type),
            "total_instruments": sum(len(ids) for ids in self._by_type.values()),
        }


# ---------------------------------------------------------------------------
# Date Range Index
# ---------------------------------------------------------------------------

class DateRangeIndex:
    """Index for date range queries."""

    def __init__(self) -> None:
        self._by_year: Dict[int, List[Tuple[str, date]]] = defaultdict(list)
        self._by_month: Dict[str, List[Tuple[str, date]]] = defaultdict(list)
        self._all_dates: List[Tuple[str, date]] = []

    def add(self, instrument_id: str, recording_date: date) -> None:
        self._by_year[recording_date.year].append((instrument_id, recording_date))
        month_key = f"{recording_date.year:04d}-{recording_date.month:02d}"
        self._by_month[month_key].append((instrument_id, recording_date))
        self._all_dates.append((instrument_id, recording_date))

    def search(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ) -> List[str]:
        """Search for instruments within a date range."""
        results: List[str] = []

        if date_from and date_to:
            start_year = date_from.year
            end_year = date_to.year
            for year in range(start_year, end_year + 1):
                for inst_id, rec_date in self._by_year.get(year, []):
                    if date_from <= rec_date <= date_to:
                        results.append(inst_id)
        elif date_from:
            for inst_id, rec_date in self._all_dates:
                if rec_date >= date_from:
                    results.append(inst_id)
        elif date_to:
            for inst_id, rec_date in self._all_dates:
                if rec_date <= date_to:
                    results.append(inst_id)
        else:
            results = [inst_id for inst_id, _ in self._all_dates]

        return results

    def stats(self) -> Dict[str, int]:
        return {
            "total_dated_instruments": len(self._all_dates),
            "year_range": f"{min(self._by_year.keys(), default=0)}-{max(self._by_year.keys(), default=0)}",
            "years_indexed": len(self._by_year),
        }


# ---------------------------------------------------------------------------
# Volume/Page and Document Number Index
# ---------------------------------------------------------------------------

class VolumePageIndex:
    """Index for volume/page and document number lookups."""

    def __init__(self) -> None:
        self._by_vol_page: Dict[str, str] = {}
        self._by_doc_number: Dict[str, str] = {}

    def add(
        self,
        instrument_id: str,
        volume: Optional[str] = None,
        page: Optional[str] = None,
        document_number: Optional[str] = None,
    ) -> None:
        if volume and page:
            key = f"V{volume}_P{page}"
            self._by_vol_page[key] = instrument_id
        if document_number:
            self._by_doc_number[document_number.strip().upper()] = instrument_id

    def lookup_volume_page(self, volume: str, page: str) -> Optional[str]:
        key = f"V{volume}_P{page}"
        return self._by_vol_page.get(key)

    def lookup_document_number(self, doc_number: str) -> Optional[str]:
        return self._by_doc_number.get(doc_number.strip().upper())

    def stats(self) -> Dict[str, int]:
        return {
            "volume_page_entries": len(self._by_vol_page),
            "document_number_entries": len(self._by_doc_number),
        }


# ---------------------------------------------------------------------------
# Main Search Engine
# ---------------------------------------------------------------------------

class TitleSearchEngine:
    """
    Main search engine for title examination records.
    Provides multi-field search with relevance scoring across
    all index types.
    """

    def __init__(self, semantic_dict: Optional[TitleSemanticDictionary] = None) -> None:
        self._gg_index = GrantorGranteeIndex()
        self._legal_index = LegalDescriptionIndex()
        self._type_index = InstrumentTypeIndex()
        self._date_index = DateRangeIndex()
        self._vp_index = VolumePageIndex()
        self._instruments: Dict[str, Dict[str, Any]] = {}
        self._semantic_dict = semantic_dict
        self._total_indexed: int = 0

    def index_instrument(self, instrument: Dict[str, Any]) -> None:
        """
        Index a single instrument record.

        Expected keys:
          instrument_id, instrument_type, recording_date,
          volume, page, document_number,
          grantors (list of names), grantees (list of names),
          legal_description, county, state,
          interests_conveyed, reservations, consideration
        """
        inst_id = instrument.get("instrument_id", "")
        if not inst_id:
            logger.warning("Instrument missing instrument_id, skipping")
            return

        self._instruments[inst_id] = instrument

        rec_date_str = instrument.get("recording_date")
        rec_date: Optional[date] = None
        if rec_date_str:
            if isinstance(rec_date_str, date):
                rec_date = rec_date_str
            elif isinstance(rec_date_str, str):
                try:
                    rec_date = date.fromisoformat(rec_date_str)
                except ValueError:
                    pass

        for grantor_name in instrument.get("grantors", []):
            self._gg_index.add_grantor(inst_id, grantor_name, rec_date)

        for grantee_name in instrument.get("grantees", []):
            self._gg_index.add_grantee(inst_id, grantee_name, rec_date)

        legal = instrument.get("legal_description", "")
        if legal:
            self._legal_index.add(
                inst_id, legal,
                county=instrument.get("county"),
                recording_date=rec_date,
            )

        inst_type = instrument.get("instrument_type", "")
        if inst_type:
            self._type_index.add(inst_id, inst_type, rec_date)

        if rec_date:
            self._date_index.add(inst_id, rec_date)

        self._vp_index.add(
            inst_id,
            volume=instrument.get("volume"),
            page=instrument.get("page"),
            document_number=instrument.get("document_number"),
        )

        self._total_indexed += 1

    def index_instruments(self, instruments: List[Dict[str, Any]]) -> int:
        """Index multiple instruments. Returns count indexed."""
        count = 0
        for inst in instruments:
            self.index_instrument(inst)
            count += 1
        logger.info(f"Indexed {count} instruments")
        return count

    def search(self, query: SearchQuery) -> SearchResponse:
        """
        Execute a search query against all indexes.
        Returns scored, sorted results.
        """
        start_time = time.time()

        if not query.has_criteria():
            elapsed = (time.time() - start_time) * 1000
            return SearchResponse(
                query=query,
                results=[],
                total_matches=0,
                returned_count=0,
                search_time_ms=elapsed,
                index_stats=self.stats(),
            )

        candidate_scores: Dict[str, float] = defaultdict(float)
        candidate_fields: Dict[str, List[str]] = defaultdict(list)
        candidate_details: Dict[str, Dict[str, Any]] = defaultdict(dict)

        if query.grantor_name:
            matches = self._gg_index.search_grantor(
                query.grantor_name,
                fuzzy=query.fuzzy_matching,
                threshold=query.fuzzy_threshold,
            )
            for entry, score in matches:
                candidate_scores[entry.instrument_id] += score * 0.35
                candidate_fields[entry.instrument_id].append("grantor")
                candidate_details[entry.instrument_id]["grantor_match"] = {
                    "query": query.grantor_name,
                    "matched": entry.value,
                    "score": score,
                }

        if query.grantee_name:
            matches = self._gg_index.search_grantee(
                query.grantee_name,
                fuzzy=query.fuzzy_matching,
                threshold=query.fuzzy_threshold,
            )
            for entry, score in matches:
                candidate_scores[entry.instrument_id] += score * 0.35
                candidate_fields[entry.instrument_id].append("grantee")
                candidate_details[entry.instrument_id]["grantee_match"] = {
                    "query": query.grantee_name,
                    "matched": entry.value,
                    "score": score,
                }

        if query.legal_description:
            matches = self._legal_index.search(query.legal_description, query.county)
            for entry, score in matches:
                candidate_scores[entry.instrument_id] += score * 0.30
                candidate_fields[entry.instrument_id].append("legal_description")

        if query.document_number:
            inst_id = self._vp_index.lookup_document_number(query.document_number)
            if inst_id:
                candidate_scores[inst_id] += 1.0
                candidate_fields[inst_id].append("document_number")

        if query.volume and query.page:
            inst_id = self._vp_index.lookup_volume_page(query.volume, query.page)
            if inst_id:
                candidate_scores[inst_id] += 1.0
                candidate_fields[inst_id].append("volume_page")

        if query.instrument_types:
            type_instruments: Set[str] = set()
            for inst_type in query.instrument_types:
                type_instruments |= self._type_index.get_by_type(inst_type)

            if candidate_scores:
                to_remove = [
                    inst_id for inst_id in candidate_scores
                    if inst_id not in type_instruments
                ]
                for inst_id in to_remove:
                    del candidate_scores[inst_id]
            else:
                for inst_id in type_instruments:
                    candidate_scores[inst_id] += 0.10
                    candidate_fields[inst_id].append("instrument_type")

        if query.date_from or query.date_to:
            date_instruments = set(
                self._date_index.search(query.date_from, query.date_to)
            )
            if candidate_scores:
                to_remove = [
                    inst_id for inst_id in candidate_scores
                    if inst_id not in date_instruments
                ]
                for inst_id in to_remove:
                    del candidate_scores[inst_id]
            else:
                for inst_id in date_instruments:
                    candidate_scores[inst_id] += 0.05
                    candidate_fields[inst_id].append("recording_date")

        if query.county:
            county_upper = query.county.upper()
            if candidate_scores:
                to_remove = []
                for inst_id in candidate_scores:
                    inst = self._instruments.get(inst_id, {})
                    if inst.get("county", "").upper() != county_upper:
                        to_remove.append(inst_id)
                for inst_id in to_remove:
                    del candidate_scores[inst_id]

        total_matches = len(candidate_scores)

        sorted_candidates = sorted(
            candidate_scores.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        if query.sort_order == SortOrder.DATE_ASC:
            sorted_candidates = sorted(
                sorted_candidates,
                key=lambda x: self._instruments.get(x[0], {}).get("recording_date", "9999"),
            )
        elif query.sort_order == SortOrder.DATE_DESC:
            sorted_candidates = sorted(
                sorted_candidates,
                key=lambda x: self._instruments.get(x[0], {}).get("recording_date", "0000"),
                reverse=True,
            )

        page = sorted_candidates[query.offset:query.offset + query.max_results]

        results: List[SearchResult] = []
        for inst_id, score in page:
            inst = self._instruments.get(inst_id, {})
            rec_date_val = inst.get("recording_date")
            if isinstance(rec_date_val, str):
                try:
                    rec_date_val = date.fromisoformat(rec_date_val)
                except ValueError:
                    rec_date_val = None

            result = SearchResult(
                instrument_id=inst_id,
                instrument_type=inst.get("instrument_type", ""),
                recording_date=rec_date_val,
                volume=inst.get("volume"),
                page=inst.get("page"),
                document_number=inst.get("document_number"),
                grantors=inst.get("grantors", []),
                grantees=inst.get("grantees", []),
                legal_description=inst.get("legal_description"),
                county=inst.get("county"),
                state=inst.get("state"),
                relevance_score=score,
                match_fields=candidate_fields.get(inst_id, []),
                match_details=candidate_details.get(inst_id, {}),
                interests_conveyed=inst.get("interests_conveyed", []),
                reservations=inst.get("reservations", []),
                consideration=str(inst.get("consideration")) if inst.get("consideration") else None,
            )
            results.append(result)

        elapsed = (time.time() - start_time) * 1000

        return SearchResponse(
            query=query,
            results=results,
            total_matches=total_matches,
            returned_count=len(results),
            search_time_ms=elapsed,
            index_stats=self.stats(),
        )

    def search_chain_forward(self, name: str, max_depth: int = 20) -> List[Dict[str, Any]]:
        """Trace chain of title forward from a grantor name."""
        return self._gg_index.trace_chain_forward(name, max_depth)

    def search_chain_backward(self, name: str, max_depth: int = 20) -> List[Dict[str, Any]]:
        """Trace chain of title backward from a grantee name."""
        return self._gg_index.trace_chain_backward(name, max_depth)

    def get_instrument(self, instrument_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific instrument by ID."""
        return self._instruments.get(instrument_id)

    def stats(self) -> Dict[str, int]:
        """Return search engine statistics."""
        return {
            "total_indexed": self._total_indexed,
            "grantor_grantee": self._gg_index.stats(),
            "legal_description": self._legal_index.stats(),
            "instrument_type": self._type_index.stats(),
            "date_range": self._date_index.stats(),
            "volume_page": self._vp_index.stats(),
        }

    def health_check(self) -> Dict[str, Any]:
        """Return health status."""
        return {
            "status": "healthy" if self._total_indexed > 0 else "empty",
            "total_indexed": self._total_indexed,
            "stats": self.stats(),
        }
