"""
LM02 Lease Analysis Engine - Search Module
Oil and Gas Lease Search, Filtering, and Retrieval

Provides comprehensive search capabilities for lease records including:
    - Lessor/lessee name search with fuzzy matching
    - Legal description matching (section, block, survey, abstract)
    - Date range filtering (execution, recording, expiration)
    - Expiration status filtering (active, expired, expiring soon)
    - Royalty rate filtering and comparison
    - Operator search with alias normalization
    - County and RRC district filtering
    - Lease term and clause type search
    - Multi-field compound queries
    - Pagination, sorting, and result aggregation

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
Version: 1.0.0
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

from loguru import logger
from pydantic import BaseModel, Field

# ============================================================================
# SEARCH ENUMERATIONS
# ============================================================================


class LeaseStatus(str, Enum):
    """Current status of a lease."""
    ACTIVE_PRIMARY = "active_primary"
    ACTIVE_SECONDARY = "active_secondary"
    HELD_BY_PRODUCTION = "held_by_production"
    SHUT_IN = "shut_in"
    CONTINUOUS_OPERATIONS = "continuous_operations"
    FORCE_MAJEURE = "force_majeure"
    EXPIRED = "expired"
    TERMINATED = "terminated"
    SURRENDERED = "surrendered"
    RELEASED = "released"
    PENDING_EXPIRATION = "pending_expiration"
    UNKNOWN = "unknown"


class SortField(str, Enum):
    """Available sort fields for search results."""
    RELEVANCE = "relevance"
    LEASE_DATE = "lease_date"
    RECORDING_DATE = "recording_date"
    EXPIRATION_DATE = "expiration_date"
    LESSOR_NAME = "lessor_name"
    LESSEE_NAME = "lessee_name"
    COUNTY = "county"
    ACRES = "acres"
    ROYALTY_RATE = "royalty_rate"
    STATUS = "status"


class SortDirection(str, Enum):
    """Sort direction."""
    ASC = "asc"
    DESC = "desc"


class ExpirationWindow(str, Enum):
    """Pre-defined expiration windows for filtering."""
    NEXT_30_DAYS = "next_30_days"
    NEXT_60_DAYS = "next_60_days"
    NEXT_90_DAYS = "next_90_days"
    NEXT_180_DAYS = "next_180_days"
    NEXT_YEAR = "next_year"
    EXPIRED_LAST_30 = "expired_last_30"
    EXPIRED_LAST_90 = "expired_last_90"
    EXPIRED_LAST_YEAR = "expired_last_year"
    ALL_ACTIVE = "all_active"
    ALL_EXPIRED = "all_expired"


# ============================================================================
# SEARCH DATA MODELS
# ============================================================================


class LeaseSearchQuery(BaseModel):
    """A comprehensive search query for lease records."""
    # Text search
    query_text: Optional[str] = Field(None, description="Free-text search across all fields")
    lessor_name: Optional[str] = Field(None, description="Lessor name (supports fuzzy matching)")
    lessee_name: Optional[str] = Field(None, description="Lessee name (supports fuzzy matching)")
    operator_name: Optional[str] = Field(None, description="Current operator name")
    grantor: Optional[str] = Field(None, description="Grantor name (alias for lessor)")
    grantee: Optional[str] = Field(None, description="Grantee name (alias for lessee)")

    # Legal description
    section: Optional[str] = Field(None, description="Section number")
    block: Optional[str] = Field(None, description="Block designation")
    survey: Optional[str] = Field(None, description="Survey name")
    abstract_number: Optional[str] = Field(None, description="Abstract number")
    township: Optional[str] = Field(None, description="Township")
    range_value: Optional[str] = Field(None, description="Range")
    county: Optional[str] = Field(None, description="County name")

    # Date ranges
    lease_date_from: Optional[date] = Field(None, description="Lease date range start")
    lease_date_to: Optional[date] = Field(None, description="Lease date range end")
    recording_date_from: Optional[date] = Field(None, description="Recording date range start")
    recording_date_to: Optional[date] = Field(None, description="Recording date range end")
    expiration_date_from: Optional[date] = Field(None, description="Expiration date range start")
    expiration_date_to: Optional[date] = Field(None, description="Expiration date range end")

    # Status and properties
    status: Optional[LeaseStatus] = Field(None, description="Lease status filter")
    expiration_window: Optional[ExpirationWindow] = Field(None, description="Pre-defined expiration window")
    min_royalty_rate: Optional[float] = Field(None, ge=0.0, le=1.0, description="Minimum royalty rate (decimal)")
    max_royalty_rate: Optional[float] = Field(None, ge=0.0, le=1.0, description="Maximum royalty rate (decimal)")
    min_acres: Optional[float] = Field(None, ge=0.0, description="Minimum acreage")
    max_acres: Optional[float] = Field(None, description="Maximum acreage")
    formation: Optional[str] = Field(None, description="Target formation name")
    has_pugh_clause: Optional[bool] = Field(None, description="Filter by presence of Pugh clause")
    has_depth_limitation: Optional[bool] = Field(None, description="Filter by presence of depth limitation")
    has_continuous_development: Optional[bool] = Field(None, description="Filter by continuous development clause")

    # Document references
    document_number: Optional[str] = Field(None, description="County recording document number")
    volume: Optional[str] = Field(None, description="Recording volume")
    page: Optional[str] = Field(None, description="Recording page")
    book_page: Optional[str] = Field(None, description="Combined book/page reference")
    instrument_type: Optional[str] = Field(None, description="Instrument type (OGL, MOL, ASMT, etc.)")

    # Pagination and sorting
    page_number: int = Field(1, ge=1, description="Page number (1-based)")
    page_size: int = Field(20, ge=1, le=100, description="Results per page")
    sort_by: SortField = Field(SortField.RELEVANCE, description="Sort field")
    sort_direction: SortDirection = Field(SortDirection.DESC, description="Sort direction")

    # Options
    include_expired: bool = Field(True, description="Include expired leases in results")
    fuzzy_match: bool = Field(True, description="Enable fuzzy name matching")
    fuzzy_threshold: float = Field(0.75, ge=0.0, le=1.0, description="Fuzzy match threshold")


class LeaseSearchResult(BaseModel):
    """A single lease search result."""
    lease_id: str = Field(..., description="Unique lease identifier")
    relevance_score: float = Field(0.0, description="Search relevance score (0-1)")
    lessor_name: str = Field("", description="Lessor name")
    lessee_name: str = Field("", description="Lessee name")
    operator_name: Optional[str] = Field(None, description="Current operator")
    lease_date: Optional[date] = Field(None, description="Lease execution date")
    recording_date: Optional[date] = Field(None, description="County recording date")
    expiration_date: Optional[date] = Field(None, description="Primary term expiration date")
    status: LeaseStatus = Field(LeaseStatus.UNKNOWN, description="Current status")
    county: Optional[str] = Field(None, description="County")
    legal_description: Optional[str] = Field(None, description="Legal description text")
    section: Optional[str] = Field(None, description="Section")
    block: Optional[str] = Field(None, description="Block")
    survey: Optional[str] = Field(None, description="Survey name")
    abstract_number: Optional[str] = Field(None, description="Abstract number")
    acres: Optional[float] = Field(None, description="Total acres")
    royalty_rate: Optional[float] = Field(None, description="Royalty rate (decimal)")
    royalty_fraction: Optional[str] = Field(None, description="Royalty fraction (e.g., '1/4')")
    primary_term_years: Optional[int] = Field(None, description="Primary term in years")
    has_pugh_clause: Optional[bool] = Field(None, description="Contains Pugh clause")
    has_depth_limitation: Optional[bool] = Field(None, description="Contains depth limitation")
    has_continuous_development: Optional[bool] = Field(None, description="Contains continuous development clause")
    document_number: Optional[str] = Field(None, description="County document number")
    volume: Optional[str] = Field(None, description="Recording volume")
    page: Optional[str] = Field(None, description="Recording page")
    formations: List[str] = Field(default_factory=list, description="Target formations")
    days_until_expiration: Optional[int] = Field(None, description="Days until expiration (negative if expired)")
    match_highlights: Dict[str, str] = Field(default_factory=dict, description="Matched fields with context")
    source: str = Field("local", description="Data source (local, encore, shadowglass, r2)")


class SearchResponse(BaseModel):
    """Paginated search response."""
    query: LeaseSearchQuery
    results: List[LeaseSearchResult] = Field(default_factory=list)
    total_results: int = Field(0, description="Total matching results")
    page_number: int = Field(1, description="Current page number")
    page_size: int = Field(20, description="Results per page")
    total_pages: int = Field(0, description="Total number of pages")
    search_time_ms: float = Field(0.0, description="Search execution time in milliseconds")
    facets: Dict[str, Dict[str, int]] = Field(default_factory=dict, description="Facet counts for filtering")
    trace_id: str = Field("", description="Telemetry trace ID for this search")
    warnings: List[str] = Field(default_factory=list, description="Search warnings or notices")

    @property
    def has_more(self) -> bool:
        """Check if more pages exist."""
        return self.page_number < self.total_pages


class ExpirationAlertResult(BaseModel):
    """Result for expiration alert queries."""
    lease_id: str
    lessor_name: str
    lessee_name: str
    county: Optional[str]
    legal_description: Optional[str]
    expiration_date: date
    days_until_expiration: int
    status: LeaseStatus
    royalty_rate: Optional[float]
    acres: Optional[float]
    alert_level: str = Field("info", description="Alert level: critical, warning, info")
    recommended_action: str = Field("", description="Recommended action for the landman")


# ============================================================================
# SEARCH INDEX (IN-MEMORY FOR LOCAL DATA)
# ============================================================================


@dataclass
class LeaseIndexEntry:
    """An indexed lease record for fast searching."""
    lease_id: str
    lessor_name: str = ""
    lessee_name: str = ""
    operator_name: str = ""
    lease_date: Optional[date] = None
    recording_date: Optional[date] = None
    expiration_date: Optional[date] = None
    status: LeaseStatus = LeaseStatus.UNKNOWN
    county: str = ""
    legal_description: str = ""
    section: str = ""
    block: str = ""
    survey: str = ""
    abstract_number: str = ""
    township: str = ""
    range_value: str = ""
    acres: Optional[float] = None
    royalty_rate: Optional[float] = None
    royalty_fraction: str = ""
    primary_term_years: Optional[int] = None
    has_pugh_clause: bool = False
    has_depth_limitation: bool = False
    has_continuous_development: bool = False
    document_number: str = ""
    volume: str = ""
    page: str = ""
    book_page: str = ""
    instrument_type: str = ""
    formations: List[str] = field(default_factory=list)
    source: str = "local"
    raw_data: Dict[str, Any] = field(default_factory=dict)

    # Pre-computed search tokens
    _search_tokens: Set[str] = field(default_factory=set, repr=False)

    def compute_search_tokens(self) -> None:
        """Pre-compute search tokens for fast full-text matching."""
        text_fields = [
            self.lessor_name, self.lessee_name, self.operator_name,
            self.county, self.legal_description, self.section,
            self.block, self.survey, self.abstract_number,
            self.document_number, self.instrument_type,
        ]
        combined = " ".join(f for f in text_fields if f).lower()
        self._search_tokens = set(re.findall(r"[a-z0-9]+", combined))

    @property
    def days_until_expiration(self) -> Optional[int]:
        """Calculate days until expiration from today."""
        if self.expiration_date is None:
            return None
        return (self.expiration_date - date.today()).days


class LeaseSearchIndex:
    """In-memory search index for lease records with multi-field search."""

    def __init__(self) -> None:
        self._entries: Dict[str, LeaseIndexEntry] = {}
        self._by_county: Dict[str, List[str]] = defaultdict(list)
        self._by_lessor: Dict[str, List[str]] = defaultdict(list)
        self._by_lessee: Dict[str, List[str]] = defaultdict(list)
        self._by_section_block: Dict[str, List[str]] = defaultdict(list)
        self._by_status: Dict[LeaseStatus, List[str]] = defaultdict(list)
        self._by_operator: Dict[str, List[str]] = defaultdict(list)
        self._entry_count: int = 0
        logger.info("LM02 Search Index initialized")

    @property
    def total_entries(self) -> int:
        return self._entry_count

    def add_entry(self, entry: LeaseIndexEntry) -> None:
        """Add or update a lease entry in the index.

        Args:
            entry: The lease index entry to add.
        """
        entry.compute_search_tokens()

        # Remove old entry if exists
        if entry.lease_id in self._entries:
            self._remove_from_indexes(entry.lease_id)

        self._entries[entry.lease_id] = entry
        self._entry_count = len(self._entries)

        # Build inverted indexes
        if entry.county:
            self._by_county[entry.county.lower()].append(entry.lease_id)
        if entry.lessor_name:
            key = entry.lessor_name.lower().strip()
            self._by_lessor[key].append(entry.lease_id)
        if entry.lessee_name:
            key = entry.lessee_name.lower().strip()
            self._by_lessee[key].append(entry.lease_id)
        if entry.section and entry.block:
            key = f"{entry.section}|{entry.block}".lower()
            self._by_section_block[key].append(entry.lease_id)
        self._by_status[entry.status].append(entry.lease_id)
        if entry.operator_name:
            key = entry.operator_name.lower().strip()
            self._by_operator[key].append(entry.lease_id)

    def _remove_from_indexes(self, lease_id: str) -> None:
        """Remove a lease from all inverted indexes."""
        for idx in [self._by_county, self._by_lessor, self._by_lessee,
                     self._by_section_block, self._by_operator]:
            for key in list(idx.keys()):
                if lease_id in idx[key]:
                    idx[key].remove(lease_id)
                    if not idx[key]:
                        del idx[key]
        for status in list(self._by_status.keys()):
            if lease_id in self._by_status[status]:
                self._by_status[status].remove(lease_id)
                if not self._by_status[status]:
                    del self._by_status[status]

    def remove_entry(self, lease_id: str) -> bool:
        """Remove a lease entry from the index.

        Args:
            lease_id: The lease ID to remove.

        Returns:
            True if the entry was found and removed.
        """
        if lease_id not in self._entries:
            return False
        self._remove_from_indexes(lease_id)
        del self._entries[lease_id]
        self._entry_count = len(self._entries)
        return True

    def get_entry(self, lease_id: str) -> Optional[LeaseIndexEntry]:
        """Get a lease entry by ID."""
        return self._entries.get(lease_id)

    def bulk_add(self, entries: List[LeaseIndexEntry]) -> int:
        """Add multiple entries to the index.

        Args:
            entries: List of lease entries to add.

        Returns:
            Number of entries added.
        """
        count = 0
        for entry in entries:
            self.add_entry(entry)
            count += 1
        logger.info(f"Bulk added {count} entries to search index (total: {self._entry_count})")
        return count

    def search(self, query: LeaseSearchQuery) -> SearchResponse:
        """Execute a search query against the index.

        Args:
            query: The search query parameters.

        Returns:
            SearchResponse with paginated results.
        """
        start_time = time.monotonic()
        trace_id = hashlib.sha256(
            f"{datetime.now(timezone.utc).isoformat()}-{id(query)}".encode()
        ).hexdigest()[:16]

        candidates = self._get_candidates(query)
        scored = self._score_candidates(candidates, query)
        filtered = self._apply_filters(scored, query)

        # Sort
        sorted_results = self._sort_results(filtered, query.sort_by, query.sort_direction)

        # Paginate
        total = len(sorted_results)
        total_pages = max(1, (total + query.page_size - 1) // query.page_size)
        start_idx = (query.page_number - 1) * query.page_size
        end_idx = start_idx + query.page_size
        page_results = sorted_results[start_idx:end_idx]

        # Convert to search results
        results = [self._to_search_result(entry, score, highlights)
                    for entry, score, highlights in page_results]

        # Compute facets
        facets = self._compute_facets([e for e, _, _ in filtered])

        elapsed_ms = (time.monotonic() - start_time) * 1000

        response = SearchResponse(
            query=query,
            results=results,
            total_results=total,
            page_number=query.page_number,
            page_size=query.page_size,
            total_pages=total_pages,
            search_time_ms=round(elapsed_ms, 2),
            facets=facets,
            trace_id=trace_id,
        )

        logger.info(
            f"Search completed: {total} results in {elapsed_ms:.1f}ms, "
            f"page {query.page_number}/{total_pages}, trace={trace_id}"
        )

        return response

    def _get_candidates(self, query: LeaseSearchQuery) -> List[LeaseIndexEntry]:
        """Get candidate entries using inverted indexes for fast pre-filtering."""
        # If specific indexed fields are provided, use inverted indexes
        candidate_ids: Optional[Set[str]] = None

        if query.county:
            county_ids = set(self._by_county.get(query.county.lower(), []))
            candidate_ids = county_ids if candidate_ids is None else candidate_ids & county_ids

        if query.status:
            status_ids = set(self._by_status.get(query.status, []))
            candidate_ids = status_ids if candidate_ids is None else candidate_ids & status_ids

        if query.section and query.block:
            key = f"{query.section}|{query.block}".lower()
            sb_ids = set(self._by_section_block.get(key, []))
            candidate_ids = sb_ids if candidate_ids is None else candidate_ids & sb_ids

        # If no indexed fields narrowed it down, search all entries
        if candidate_ids is None:
            return list(self._entries.values())

        return [self._entries[lid] for lid in candidate_ids if lid in self._entries]

    def _score_candidates(
        self,
        candidates: List[LeaseIndexEntry],
        query: LeaseSearchQuery,
    ) -> List[Tuple[LeaseIndexEntry, float, Dict[str, str]]]:
        """Score candidates by relevance to the query."""
        scored: List[Tuple[LeaseIndexEntry, float, Dict[str, str]]] = []

        for entry in candidates:
            score = 0.0
            highlights: Dict[str, str] = {}

            # Free-text search
            if query.query_text:
                text_score, text_highlights = self._score_text_match(entry, query.query_text)
                score += text_score * 3.0
                highlights.update(text_highlights)

            # Lessor/grantor name match
            name_query = query.lessor_name or query.grantor
            if name_query:
                name_score = self._fuzzy_name_match(
                    name_query, entry.lessor_name, query.fuzzy_threshold if query.fuzzy_match else 1.0
                )
                if name_score > 0:
                    score += name_score * 5.0
                    highlights["lessor_name"] = entry.lessor_name

            # Lessee/grantee name match
            name_query2 = query.lessee_name or query.grantee
            if name_query2:
                name_score2 = self._fuzzy_name_match(
                    name_query2, entry.lessee_name, query.fuzzy_threshold if query.fuzzy_match else 1.0
                )
                if name_score2 > 0:
                    score += name_score2 * 5.0
                    highlights["lessee_name"] = entry.lessee_name

            # Operator name match
            if query.operator_name:
                op_score = self._fuzzy_name_match(
                    query.operator_name, entry.operator_name, query.fuzzy_threshold if query.fuzzy_match else 1.0
                )
                if op_score > 0:
                    score += op_score * 4.0
                    highlights["operator_name"] = entry.operator_name

            # Legal description components
            if query.section and entry.section and query.section.lower() == entry.section.lower():
                score += 3.0
                highlights["section"] = entry.section
            if query.block and entry.block and query.block.lower() == entry.block.lower():
                score += 3.0
                highlights["block"] = entry.block
            if query.survey and entry.survey:
                survey_score = self._fuzzy_name_match(query.survey, entry.survey, 0.7)
                if survey_score > 0:
                    score += survey_score * 2.0
                    highlights["survey"] = entry.survey
            if query.abstract_number and entry.abstract_number and query.abstract_number == entry.abstract_number:
                score += 4.0
                highlights["abstract_number"] = entry.abstract_number

            # County match (already used in candidate selection, but add score)
            if query.county and entry.county and query.county.lower() == entry.county.lower():
                score += 1.0
                highlights["county"] = entry.county

            # Document number exact match
            if query.document_number and entry.document_number:
                if query.document_number.lower() == entry.document_number.lower():
                    score += 10.0
                    highlights["document_number"] = entry.document_number

            # Volume/page match
            if query.volume and entry.volume and query.volume == entry.volume:
                score += 2.0
                highlights["volume"] = entry.volume
            if query.page and entry.page and query.page == entry.page:
                score += 2.0
                highlights["page"] = entry.page

            # Formation match
            if query.formation and entry.formations:
                formation_lower = query.formation.lower()
                for f in entry.formations:
                    if formation_lower in f.lower():
                        score += 2.0
                        highlights["formation"] = f
                        break

            # Instrument type match
            if query.instrument_type and entry.instrument_type:
                if query.instrument_type.lower() == entry.instrument_type.lower():
                    score += 2.0

            if score > 0 or not any([
                query.query_text, query.lessor_name, query.lessee_name, query.grantor,
                query.grantee, query.operator_name, query.section, query.block,
                query.survey, query.abstract_number, query.document_number,
                query.volume, query.page, query.formation, query.instrument_type,
            ]):
                # Include if scored OR if no text/name criteria (filters-only query)
                scored.append((entry, score, highlights))

        return scored

    def _apply_filters(
        self,
        scored: List[Tuple[LeaseIndexEntry, float, Dict[str, str]]],
        query: LeaseSearchQuery,
    ) -> List[Tuple[LeaseIndexEntry, float, Dict[str, str]]]:
        """Apply non-scoring filters to reduce results."""
        filtered = scored

        # Date range filters
        if query.lease_date_from:
            filtered = [(e, s, h) for e, s, h in filtered
                         if e.lease_date and e.lease_date >= query.lease_date_from]
        if query.lease_date_to:
            filtered = [(e, s, h) for e, s, h in filtered
                         if e.lease_date and e.lease_date <= query.lease_date_to]
        if query.recording_date_from:
            filtered = [(e, s, h) for e, s, h in filtered
                         if e.recording_date and e.recording_date >= query.recording_date_from]
        if query.recording_date_to:
            filtered = [(e, s, h) for e, s, h in filtered
                         if e.recording_date and e.recording_date <= query.recording_date_to]
        if query.expiration_date_from:
            filtered = [(e, s, h) for e, s, h in filtered
                         if e.expiration_date and e.expiration_date >= query.expiration_date_from]
        if query.expiration_date_to:
            filtered = [(e, s, h) for e, s, h in filtered
                         if e.expiration_date and e.expiration_date <= query.expiration_date_to]

        # Expiration window filter
        if query.expiration_window:
            filtered = self._apply_expiration_window(filtered, query.expiration_window)

        # Royalty rate filters
        if query.min_royalty_rate is not None:
            filtered = [(e, s, h) for e, s, h in filtered
                         if e.royalty_rate is not None and e.royalty_rate >= query.min_royalty_rate]
        if query.max_royalty_rate is not None:
            filtered = [(e, s, h) for e, s, h in filtered
                         if e.royalty_rate is not None and e.royalty_rate <= query.max_royalty_rate]

        # Acreage filters
        if query.min_acres is not None:
            filtered = [(e, s, h) for e, s, h in filtered
                         if e.acres is not None and e.acres >= query.min_acres]
        if query.max_acres is not None:
            filtered = [(e, s, h) for e, s, h in filtered
                         if e.acres is not None and e.acres <= query.max_acres]

        # Boolean clause filters
        if query.has_pugh_clause is not None:
            filtered = [(e, s, h) for e, s, h in filtered if e.has_pugh_clause == query.has_pugh_clause]
        if query.has_depth_limitation is not None:
            filtered = [(e, s, h) for e, s, h in filtered if e.has_depth_limitation == query.has_depth_limitation]
        if query.has_continuous_development is not None:
            filtered = [(e, s, h) for e, s, h in filtered
                         if e.has_continuous_development == query.has_continuous_development]

        # Expired filter
        if not query.include_expired:
            filtered = [(e, s, h) for e, s, h in filtered
                         if e.status not in (LeaseStatus.EXPIRED, LeaseStatus.TERMINATED, LeaseStatus.SURRENDERED)]

        return filtered

    def _apply_expiration_window(
        self,
        entries: List[Tuple[LeaseIndexEntry, float, Dict[str, str]]],
        window: ExpirationWindow,
    ) -> List[Tuple[LeaseIndexEntry, float, Dict[str, str]]]:
        """Apply an expiration window filter."""
        today = date.today()
        result: List[Tuple[LeaseIndexEntry, float, Dict[str, str]]] = []

        for entry, score, highlights in entries:
            if entry.expiration_date is None:
                continue
            days_until = (entry.expiration_date - today).days

            include = False
            if window == ExpirationWindow.NEXT_30_DAYS:
                include = 0 <= days_until <= 30
            elif window == ExpirationWindow.NEXT_60_DAYS:
                include = 0 <= days_until <= 60
            elif window == ExpirationWindow.NEXT_90_DAYS:
                include = 0 <= days_until <= 90
            elif window == ExpirationWindow.NEXT_180_DAYS:
                include = 0 <= days_until <= 180
            elif window == ExpirationWindow.NEXT_YEAR:
                include = 0 <= days_until <= 365
            elif window == ExpirationWindow.EXPIRED_LAST_30:
                include = -30 <= days_until < 0
            elif window == ExpirationWindow.EXPIRED_LAST_90:
                include = -90 <= days_until < 0
            elif window == ExpirationWindow.EXPIRED_LAST_YEAR:
                include = -365 <= days_until < 0
            elif window == ExpirationWindow.ALL_ACTIVE:
                include = days_until >= 0
            elif window == ExpirationWindow.ALL_EXPIRED:
                include = days_until < 0

            if include:
                result.append((entry, score, highlights))

        return result

    def _sort_results(
        self,
        results: List[Tuple[LeaseIndexEntry, float, Dict[str, str]]],
        sort_by: SortField,
        direction: SortDirection,
    ) -> List[Tuple[LeaseIndexEntry, float, Dict[str, str]]]:
        """Sort results by the specified field and direction."""
        reverse = direction == SortDirection.DESC

        def sort_key(item: Tuple[LeaseIndexEntry, float, Dict[str, str]]) -> Any:
            entry, score, _ = item
            if sort_by == SortField.RELEVANCE:
                return score
            elif sort_by == SortField.LEASE_DATE:
                return entry.lease_date or date.min
            elif sort_by == SortField.RECORDING_DATE:
                return entry.recording_date or date.min
            elif sort_by == SortField.EXPIRATION_DATE:
                return entry.expiration_date or date.min
            elif sort_by == SortField.LESSOR_NAME:
                return entry.lessor_name.lower()
            elif sort_by == SortField.LESSEE_NAME:
                return entry.lessee_name.lower()
            elif sort_by == SortField.COUNTY:
                return entry.county.lower()
            elif sort_by == SortField.ACRES:
                return entry.acres or 0.0
            elif sort_by == SortField.ROYALTY_RATE:
                return entry.royalty_rate or 0.0
            elif sort_by == SortField.STATUS:
                return entry.status.value
            return score

        return sorted(results, key=sort_key, reverse=reverse)

    def _to_search_result(
        self,
        entry: LeaseIndexEntry,
        score: float,
        highlights: Dict[str, str],
    ) -> LeaseSearchResult:
        """Convert an index entry to a search result."""
        max_score = max(score, 1.0)
        normalized_score = min(score / max_score, 1.0) if score > 0 else 0.0

        return LeaseSearchResult(
            lease_id=entry.lease_id,
            relevance_score=round(normalized_score, 4),
            lessor_name=entry.lessor_name,
            lessee_name=entry.lessee_name,
            operator_name=entry.operator_name or None,
            lease_date=entry.lease_date,
            recording_date=entry.recording_date,
            expiration_date=entry.expiration_date,
            status=entry.status,
            county=entry.county or None,
            legal_description=entry.legal_description or None,
            section=entry.section or None,
            block=entry.block or None,
            survey=entry.survey or None,
            abstract_number=entry.abstract_number or None,
            acres=entry.acres,
            royalty_rate=entry.royalty_rate,
            royalty_fraction=entry.royalty_fraction or None,
            primary_term_years=entry.primary_term_years,
            has_pugh_clause=entry.has_pugh_clause,
            has_depth_limitation=entry.has_depth_limitation,
            has_continuous_development=entry.has_continuous_development,
            document_number=entry.document_number or None,
            volume=entry.volume or None,
            page=entry.page or None,
            formations=entry.formations,
            days_until_expiration=entry.days_until_expiration,
            match_highlights=highlights,
            source=entry.source,
        )

    def _compute_facets(self, entries: List[LeaseIndexEntry]) -> Dict[str, Dict[str, int]]:
        """Compute facet counts from the result set."""
        facets: Dict[str, Dict[str, int]] = {
            "county": defaultdict(int),
            "status": defaultdict(int),
            "royalty_rate": defaultdict(int),
            "has_pugh_clause": defaultdict(int),
        }

        for entry in entries:
            if entry.county:
                facets["county"][entry.county] += 1
            facets["status"][entry.status.value] += 1
            if entry.royalty_rate is not None:
                bucket = f"{entry.royalty_rate:.4f}"
                facets["royalty_rate"][bucket] += 1
            facets["has_pugh_clause"][str(entry.has_pugh_clause)] += 1

        return {k: dict(v) for k, v in facets.items()}

    @staticmethod
    def _score_text_match(entry: LeaseIndexEntry, query_text: str) -> Tuple[float, Dict[str, str]]:
        """Score a free-text match against an entry's search tokens."""
        query_tokens = set(re.findall(r"[a-z0-9]+", query_text.lower()))
        if not query_tokens:
            return (0.0, {})

        matched = query_tokens & entry._search_tokens
        if not matched:
            return (0.0, {})

        score = len(matched) / len(query_tokens)
        highlights: Dict[str, str] = {"query_match": ", ".join(sorted(matched))}
        return (score, highlights)

    @staticmethod
    def _fuzzy_name_match(query: str, candidate: str, threshold: float) -> float:
        """Compute fuzzy match score between two names.

        Uses token-based overlap for robustness against name variations.

        Args:
            query: The search name.
            candidate: The candidate name from the index.
            threshold: Minimum score to consider a match.

        Returns:
            Match score (0.0 to 1.0), or 0.0 if below threshold.
        """
        if not query or not candidate:
            return 0.0

        q_lower = query.strip().lower()
        c_lower = candidate.strip().lower()

        # Exact match
        if q_lower == c_lower:
            return 1.0

        # Contains match
        if q_lower in c_lower or c_lower in q_lower:
            return 0.9

        # Token overlap
        q_tokens = set(re.findall(r"[a-z0-9]+", q_lower))
        c_tokens = set(re.findall(r"[a-z0-9]+", c_lower))

        if not q_tokens or not c_tokens:
            return 0.0

        intersection = q_tokens & c_tokens
        if not intersection:
            return 0.0

        # Jaccard-like score weighted toward query coverage
        query_coverage = len(intersection) / len(q_tokens)
        candidate_coverage = len(intersection) / len(c_tokens)
        score = (query_coverage * 0.7) + (candidate_coverage * 0.3)

        return score if score >= threshold else 0.0

    def get_statistics(self) -> Dict[str, Any]:
        """Get index statistics."""
        status_counts = {s.value: len(ids) for s, ids in self._by_status.items()}
        county_counts = {c: len(ids) for c, ids in self._by_county.items()}

        return {
            "total_entries": self._entry_count,
            "by_status": status_counts,
            "by_county": county_counts,
            "unique_lessors": len(self._by_lessor),
            "unique_lessees": len(self._by_lessee),
            "unique_operators": len(self._by_operator),
            "unique_section_blocks": len(self._by_section_block),
        }


# ============================================================================
# MODULE-LEVEL SEARCH INDEX INSTANCE
# ============================================================================

_SEARCH_INDEX = LeaseSearchIndex()


def get_search_index() -> LeaseSearchIndex:
    """Get the module-level search index instance."""
    return _SEARCH_INDEX


# ============================================================================
# CONVENIENCE SEARCH FUNCTIONS
# ============================================================================


def search_leases(query: LeaseSearchQuery) -> SearchResponse:
    """Execute a lease search using the module-level index.

    Args:
        query: The search query parameters.

    Returns:
        SearchResponse with results.
    """
    return _SEARCH_INDEX.search(query)


def search_by_lessor_lessee(
    lessor: Optional[str] = None,
    lessee: Optional[str] = None,
    county: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> SearchResponse:
    """Search leases by lessor and/or lessee name.

    Args:
        lessor: Lessor name to search.
        lessee: Lessee name to search.
        county: Optional county filter.
        page: Page number.
        page_size: Results per page.

    Returns:
        SearchResponse with matching leases.
    """
    query = LeaseSearchQuery(
        lessor_name=lessor,
        lessee_name=lessee,
        county=county,
        page_number=page,
        page_size=page_size,
        sort_by=SortField.RELEVANCE,
        sort_direction=SortDirection.DESC,
    )
    return _SEARCH_INDEX.search(query)


def search_by_legal_description(
    section: Optional[str] = None,
    block: Optional[str] = None,
    survey: Optional[str] = None,
    abstract_number: Optional[str] = None,
    county: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> SearchResponse:
    """Search leases by legal description components.

    Args:
        section: Section number.
        block: Block designation.
        survey: Survey name.
        abstract_number: Abstract number.
        county: County name.
        page: Page number.
        page_size: Results per page.

    Returns:
        SearchResponse with matching leases.
    """
    query = LeaseSearchQuery(
        section=section,
        block=block,
        survey=survey,
        abstract_number=abstract_number,
        county=county,
        page_number=page,
        page_size=page_size,
        sort_by=SortField.RELEVANCE,
        sort_direction=SortDirection.DESC,
    )
    return _SEARCH_INDEX.search(query)


def search_expiring_leases(
    window: ExpirationWindow = ExpirationWindow.NEXT_90_DAYS,
    county: Optional[str] = None,
    operator: Optional[str] = None,
    page: int = 1,
    page_size: int = 50,
) -> SearchResponse:
    """Search for leases expiring within a specified window.

    Args:
        window: Expiration window to filter by.
        county: Optional county filter.
        operator: Optional operator filter.
        page: Page number.
        page_size: Results per page.

    Returns:
        SearchResponse with expiring leases sorted by expiration date.
    """
    query = LeaseSearchQuery(
        expiration_window=window,
        county=county,
        operator_name=operator,
        page_number=page,
        page_size=page_size,
        sort_by=SortField.EXPIRATION_DATE,
        sort_direction=SortDirection.ASC,
    )
    return _SEARCH_INDEX.search(query)


def search_by_document(
    document_number: Optional[str] = None,
    volume: Optional[str] = None,
    page_num: Optional[str] = None,
    county: Optional[str] = None,
) -> SearchResponse:
    """Search leases by county recording references.

    Args:
        document_number: County document number.
        volume: Recording volume.
        page_num: Recording page.
        county: County name.

    Returns:
        SearchResponse with matching leases.
    """
    query = LeaseSearchQuery(
        document_number=document_number,
        volume=volume,
        page=page_num,
        county=county,
        page_number=1,
        page_size=20,
        sort_by=SortField.RELEVANCE,
        sort_direction=SortDirection.DESC,
    )
    return _SEARCH_INDEX.search(query)


def generate_expiration_alerts(
    county: Optional[str] = None,
    warning_days: List[int] = None,
) -> List[ExpirationAlertResult]:
    """Generate expiration alerts for leases within warning thresholds.

    Args:
        county: Optional county filter.
        warning_days: List of day thresholds (default: [30, 60, 90, 180, 365]).

    Returns:
        List of ExpirationAlertResult sorted by urgency.
    """
    if warning_days is None:
        warning_days = [30, 60, 90, 180, 365]

    today = date.today()
    max_window = max(warning_days)
    alerts: List[ExpirationAlertResult] = []

    for entry in _SEARCH_INDEX._entries.values():
        if entry.expiration_date is None:
            continue
        if county and entry.county.lower() != county.lower():
            continue

        days_until = (entry.expiration_date - today).days
        if days_until < 0 or days_until > max_window:
            continue

        # Determine alert level
        if days_until <= 30:
            alert_level = "critical"
            action = "IMMEDIATE ACTION: Verify lease status, contact operator, prepare top lease if needed"
        elif days_until <= 60:
            alert_level = "warning"
            action = "Review lease for saving clauses, confirm operator development plans"
        elif days_until <= 90:
            alert_level = "warning"
            action = "Schedule lease review, verify delay rental payments are current"
        elif days_until <= 180:
            alert_level = "info"
            action = "Monitor development activity, calendar future review date"
        else:
            alert_level = "info"
            action = "Note for long-term planning, verify lease provisions"

        alerts.append(ExpirationAlertResult(
            lease_id=entry.lease_id,
            lessor_name=entry.lessor_name,
            lessee_name=entry.lessee_name,
            county=entry.county or None,
            legal_description=entry.legal_description or None,
            expiration_date=entry.expiration_date,
            days_until_expiration=days_until,
            status=entry.status,
            royalty_rate=entry.royalty_rate,
            acres=entry.acres,
            alert_level=alert_level,
            recommended_action=action,
        ))

    # Sort by days until expiration (most urgent first)
    alerts.sort(key=lambda a: a.days_until_expiration)
    return alerts
