"""
LM06 Right of Way Engine - Search Index & Retrieval
====================================================
TF-IDF inverted index for ROW records, pipeline easements, crossing agreements,
condemnation proceedings, and surface use agreements.

Provides: Full-text search, filtering by location/type/operator/dimensions,
sorting, pagination, and relevance scoring.
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from loguru import logger
from pydantic import BaseModel, Field


# ============================================================================
# ENUMS
# ============================================================================

class ROWType(str, Enum):
    PIPELINE_EASEMENT = "pipeline_easement"
    TEMPORARY_EASEMENT = "temporary_easement"
    FEE_SIMPLE = "fee_simple"
    CROSSING_AGREEMENT = "crossing_agreement"
    SURFACE_USE_AGREEMENT = "surface_use_agreement"
    AERIAL_EASEMENT = "aerial_easement"
    SUBSURFACE_EASEMENT = "subsurface_easement"


class ROWStatus(str, Enum):
    ACTIVE = "active"
    PENDING = "pending"
    EXPIRED = "expired"
    TERMINATED = "terminated"
    ABANDONED = "abandoned"


class SortField(str, Enum):
    RELEVANCE = "relevance"
    DATE = "date"
    WIDTH = "width"
    COMPENSATION = "compensation"
    COUNTY = "county"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


# ============================================================================
# DATACLASSES
# ============================================================================

@dataclass
class ROWRecord:
    """Represents a single ROW record (easement, crossing, etc.)."""
    record_id: str
    row_type: ROWType
    status: ROWStatus
    grantor: str
    grantee: str
    operator: Optional[str]
    county: str
    state: str = "TX"
    width_feet: Optional[float] = None
    depth_inches: Optional[int] = None
    length_feet: Optional[float] = None
    compensation_total: Optional[float] = None
    compensation_per_acre: Optional[float] = None
    execution_date: Optional[datetime] = None
    recording_date: Optional[datetime] = None
    volume: Optional[str] = None
    page: Optional[str] = None
    legal_description: Optional[str] = None
    pipeline_diameter_inches: Optional[int] = None
    pipeline_material: Optional[str] = None
    crossing_type: Optional[str] = None  # railroad, highway, river, etc.
    ferc_docket: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class SearchIndex:
    """TF-IDF inverted index for ROW records."""
    # Inverted index: term -> {record_id -> term_frequency}
    term_index: Dict[str, Dict[str, int]] = field(default_factory=dict)

    # Document frequencies: term -> number of documents containing term
    doc_frequencies: Dict[str, int] = field(default_factory=dict)

    # Total documents
    total_docs: int = 0

    # Record storage: record_id -> ROWRecord
    records: Dict[str, ROWRecord] = field(default_factory=dict)

    # Metadata indexes for filtering
    county_index: Dict[str, Set[str]] = field(default_factory=dict)
    operator_index: Dict[str, Set[str]] = field(default_factory=dict)
    type_index: Dict[ROWType, Set[str]] = field(default_factory=dict)
    status_index: Dict[ROWStatus, Set[str]] = field(default_factory=dict)


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class SearchQuery(BaseModel):
    """Search query parameters."""
    query: str = Field(..., min_length=1, description="Search query text")
    county: Optional[str] = Field(default=None, description="Filter by county")
    state: Optional[str] = Field(default="TX", description="Filter by state")
    row_type: Optional[ROWType] = Field(default=None, description="Filter by ROW type")
    status: Optional[ROWStatus] = Field(default=None, description="Filter by status")
    operator: Optional[str] = Field(default=None, description="Filter by operator")
    grantor: Optional[str] = Field(default=None, description="Filter by grantor")
    grantee: Optional[str] = Field(default=None, description="Filter by grantee")
    min_width: Optional[float] = Field(default=None, description="Min ROW width (feet)")
    max_width: Optional[float] = Field(default=None, description="Max ROW width (feet)")
    min_compensation: Optional[float] = Field(default=None, description="Min compensation ($)")
    max_compensation: Optional[float] = Field(default=None, description="Max compensation ($)")
    start_date: Optional[datetime] = Field(default=None, description="Execution date start")
    end_date: Optional[datetime] = Field(default=None, description="Execution date end")
    sort_by: SortField = Field(default=SortField.RELEVANCE, description="Sort field")
    sort_order: SortOrder = Field(default=SortOrder.DESC, description="Sort order")
    limit: int = Field(default=20, ge=1, le=100, description="Max results")
    offset: int = Field(default=0, ge=0, description="Result offset (pagination)")


class SearchResult(BaseModel):
    """Single search result with relevance score."""
    record_id: str
    score: float
    row_type: str
    status: str
    grantor: str
    grantee: str
    operator: Optional[str]
    county: str
    state: str
    width_feet: Optional[float]
    compensation_total: Optional[float]
    execution_date: Optional[datetime]
    snippet: str


class SearchResponse(BaseModel):
    """Search response with results and metadata."""
    query: str
    total_results: int
    returned_results: int
    offset: int
    results: List[SearchResult]
    facets: Dict[str, Dict[str, int]]  # e.g., {"county": {"reeves": 10, "ector": 5}}
    search_time_ms: float


# ============================================================================
# SEARCH INDEX CONSTRUCTION
# ============================================================================

def tokenize(text: str) -> List[str]:
    """
    Tokenize text into searchable terms.

    Args:
        text: Input text

    Returns:
        List of lowercase tokens
    """
    if not text:
        return []

    # Lowercase, split on whitespace and punctuation
    import re
    tokens = re.findall(r'\b\w+\b', text.lower())

    # Filter stopwords
    stopwords = {
        'the', 'and', 'or', 'of', 'to', 'in', 'a', 'an', 'is', 'for', 'on', 'at', 'by',
        'with', 'from', 'as', 'be', 'was', 'are', 'has', 'have', 'had', 'this', 'that',
    }
    tokens = [t for t in tokens if t not in stopwords and len(t) > 2]

    return tokens


def build_search_index(records: List[ROWRecord]) -> SearchIndex:
    """
    Build TF-IDF inverted index from ROW records.

    Args:
        records: List of ROWRecord objects

    Returns:
        SearchIndex with inverted index and metadata indexes
    """
    index = SearchIndex()

    for record in records:
        # Add to record storage
        index.records[record.record_id] = record
        index.total_docs += 1

        # Build searchable text from record fields
        searchable_text = ' '.join(filter(None, [
            record.grantor,
            record.grantee,
            record.operator or '',
            record.county,
            record.state,
            record.row_type.value,
            record.status.value,
            record.legal_description or '',
            record.notes or '',
            record.crossing_type or '',
            record.ferc_docket or '',
        ]))

        # Tokenize
        tokens = tokenize(searchable_text)

        # Count term frequencies
        term_counts = Counter(tokens)

        # Update inverted index
        for term, count in term_counts.items():
            if term not in index.term_index:
                index.term_index[term] = {}
            index.term_index[term][record.record_id] = count

            # Update document frequency
            if term not in index.doc_frequencies:
                index.doc_frequencies[term] = 0
            index.doc_frequencies[term] += 1

        # Update metadata indexes
        county_key = record.county.lower()
        if county_key not in index.county_index:
            index.county_index[county_key] = set()
        index.county_index[county_key].add(record.record_id)

        if record.operator:
            operator_key = record.operator.lower()
            if operator_key not in index.operator_index:
                index.operator_index[operator_key] = set()
            index.operator_index[operator_key].add(record.record_id)

        if record.row_type not in index.type_index:
            index.type_index[record.row_type] = set()
        index.type_index[record.row_type].add(record.record_id)

        if record.status not in index.status_index:
            index.status_index[record.status] = set()
        index.status_index[record.status].add(record.record_id)

    logger.info(f"Built search index: {index.total_docs} records, {len(index.term_index)} unique terms")
    return index


# ============================================================================
# SEARCH FUNCTIONS
# ============================================================================

def calculate_tf_idf(term: str, record_id: str, index: SearchIndex) -> float:
    """
    Calculate TF-IDF score for a term in a document.

    Args:
        term: Search term
        record_id: Record ID
        index: Search index

    Returns:
        TF-IDF score
    """
    if term not in index.term_index or record_id not in index.term_index[term]:
        return 0.0

    # Term frequency (TF)
    tf = index.term_index[term][record_id]

    # Inverse document frequency (IDF)
    doc_freq = index.doc_frequencies.get(term, 1)
    idf = math.log((index.total_docs + 1) / (doc_freq + 1))

    return tf * idf


def search_records(query: SearchQuery, index: SearchIndex) -> SearchResponse:
    """
    Search ROW records using TF-IDF ranking.

    Args:
        query: Search query with filters
        index: Search index

    Returns:
        SearchResponse with ranked results
    """
    import time
    start_time = time.time()

    # Tokenize query
    query_tokens = tokenize(query.query)

    # Score all documents
    scores: Dict[str, float] = defaultdict(float)

    for term in query_tokens:
        if term in index.term_index:
            for record_id in index.term_index[term]:
                scores[record_id] += calculate_tf_idf(term, record_id, index)

    # Filter by criteria
    filtered_ids = set(scores.keys()) if scores else set(index.records.keys())

    if query.county:
        county_key = query.county.lower()
        county_ids = index.county_index.get(county_key, set())
        filtered_ids &= county_ids

    if query.operator:
        operator_key = query.operator.lower()
        operator_ids = index.operator_index.get(operator_key, set())
        filtered_ids &= operator_ids

    if query.row_type:
        type_ids = index.type_index.get(query.row_type, set())
        filtered_ids &= type_ids

    if query.status:
        status_ids = index.status_index.get(query.status, set())
        filtered_ids &= status_ids

    if query.grantor:
        grantor_lower = query.grantor.lower()
        grantor_ids = {rid for rid, rec in index.records.items() if grantor_lower in rec.grantor.lower()}
        filtered_ids &= grantor_ids

    if query.grantee:
        grantee_lower = query.grantee.lower()
        grantee_ids = {rid for rid, rec in index.records.items() if grantee_lower in rec.grantee.lower()}
        filtered_ids &= grantee_ids

    # Dimension filters
    if query.min_width is not None or query.max_width is not None:
        width_ids = set()
        for rid in filtered_ids:
            rec = index.records[rid]
            if rec.width_feet is not None:
                if query.min_width is not None and rec.width_feet < query.min_width:
                    continue
                if query.max_width is not None and rec.width_feet > query.max_width:
                    continue
                width_ids.add(rid)
        filtered_ids &= width_ids

    if query.min_compensation is not None or query.max_compensation is not None:
        comp_ids = set()
        for rid in filtered_ids:
            rec = index.records[rid]
            if rec.compensation_total is not None:
                if query.min_compensation is not None and rec.compensation_total < query.min_compensation:
                    continue
                if query.max_compensation is not None and rec.compensation_total > query.max_compensation:
                    continue
                comp_ids.add(rid)
        filtered_ids &= comp_ids

    # Date filters
    if query.start_date is not None or query.end_date is not None:
        date_ids = set()
        for rid in filtered_ids:
            rec = index.records[rid]
            if rec.execution_date is not None:
                if query.start_date is not None and rec.execution_date < query.start_date:
                    continue
                if query.end_date is not None and rec.execution_date > query.end_date:
                    continue
                date_ids.add(rid)
        filtered_ids &= date_ids

    # Sort results
    sorted_ids = sorted(
        filtered_ids,
        key=lambda rid: (
            scores[rid] if query.sort_by == SortField.RELEVANCE else
            (index.records[rid].execution_date or datetime.min) if query.sort_by == SortField.DATE else
            (index.records[rid].width_feet or 0) if query.sort_by == SortField.WIDTH else
            (index.records[rid].compensation_total or 0) if query.sort_by == SortField.COMPENSATION else
            index.records[rid].county
        ),
        reverse=(query.sort_order == SortOrder.DESC)
    )

    # Pagination
    total_results = len(sorted_ids)
    paginated_ids = sorted_ids[query.offset:query.offset + query.limit]

    # Build results
    results = []
    for rid in paginated_ids:
        rec = index.records[rid]
        snippet = f"{rec.grantor} to {rec.grantee} | {rec.county} County, {rec.state}"
        if rec.width_feet:
            snippet += f" | {rec.width_feet} ft wide"
        if rec.compensation_total:
            snippet += f" | ${rec.compensation_total:,.2f}"

        results.append(SearchResult(
            record_id=rid,
            score=scores.get(rid, 0.0),
            row_type=rec.row_type.value,
            status=rec.status.value,
            grantor=rec.grantor,
            grantee=rec.grantee,
            operator=rec.operator,
            county=rec.county,
            state=rec.state,
            width_feet=rec.width_feet,
            compensation_total=rec.compensation_total,
            execution_date=rec.execution_date,
            snippet=snippet,
        ))

    # Build facets
    facets = {
        "county": {},
        "operator": {},
        "row_type": {},
        "status": {},
    }

    for rid in filtered_ids:
        rec = index.records[rid]
        facets["county"][rec.county] = facets["county"].get(rec.county, 0) + 1
        if rec.operator:
            facets["operator"][rec.operator] = facets["operator"].get(rec.operator, 0) + 1
        facets["row_type"][rec.row_type.value] = facets["row_type"].get(rec.row_type.value, 0) + 1
        facets["status"][rec.status.value] = facets["status"].get(rec.status.value, 0) + 1

    search_time_ms = (time.time() - start_time) * 1000

    return SearchResponse(
        query=query.query,
        total_results=total_results,
        returned_results=len(results),
        offset=query.offset,
        results=results,
        facets=facets,
        search_time_ms=search_time_ms,
    )


def filter_by_location(county: Optional[str], state: str, index: SearchIndex) -> Set[str]:
    """Filter records by location."""
    if county:
        county_key = county.lower()
        return index.county_index.get(county_key, set())
    return set(index.records.keys())


def filter_by_type(row_type: ROWType, index: SearchIndex) -> Set[str]:
    """Filter records by ROW type."""
    return index.type_index.get(row_type, set())


def filter_by_operator(operator: str, index: SearchIndex) -> Set[str]:
    """Filter records by operator."""
    operator_key = operator.lower()
    return index.operator_index.get(operator_key, set())


def filter_by_dimensions(
    min_width: Optional[float],
    max_width: Optional[float],
    index: SearchIndex
) -> Set[str]:
    """Filter records by ROW width."""
    result_ids = set()
    for rid, rec in index.records.items():
        if rec.width_feet is None:
            continue
        if min_width is not None and rec.width_feet < min_width:
            continue
        if max_width is not None and rec.width_feet > max_width:
            continue
        result_ids.add(rid)
    return result_ids


# ============================================================================
# SINGLETON INDEX
# ============================================================================

_SEARCH_INDEX: Optional[SearchIndex] = None


def get_search_index() -> SearchIndex:
    """Get or initialize search index."""
    global _SEARCH_INDEX
    if _SEARCH_INDEX is None:
        # Initialize with empty index (will be populated by engine on startup)
        _SEARCH_INDEX = SearchIndex()
        logger.info("Initialized empty search index")
    return _SEARCH_INDEX


def search_index_health() -> Dict[str, Any]:
    """Get search index health statistics."""
    index = get_search_index()
    return {
        "total_records": index.total_docs,
        "unique_terms": len(index.term_index),
        "counties": len(index.county_index),
        "operators": len(index.operator_index),
        "row_types": len(index.type_index),
        "statuses": len(index.status_index),
        "avg_terms_per_doc": sum(len(docs) for docs in index.term_index.values()) / max(index.total_docs, 1),
    }


# ============================================================================
# EXPORT FOR TESTING
# ============================================================================

if __name__ == "__main__":
    # Test search index
    test_records = [
        ROWRecord(
            record_id="REC001",
            row_type=ROWType.PIPELINE_EASEMENT,
            status=ROWStatus.ACTIVE,
            grantor="John Doe",
            grantee="Energy Transfer",
            operator="energy_transfer",
            county="Reeves",
            state="TX",
            width_feet=75.0,
            compensation_total=50000.0,
            execution_date=datetime(2020, 3, 15),
        ),
        ROWRecord(
            record_id="REC002",
            row_type=ROWType.CROSSING_AGREEMENT,
            status=ROWStatus.ACTIVE,
            grantor="BNSF Railway",
            grantee="Enterprise Products",
            operator="enterprise_products",
            county="Ector",
            state="TX",
            crossing_type="railroad",
            compensation_total=25000.0,
            execution_date=datetime(2021, 7, 10),
        ),
    ]

    print("=== Building Search Index ===")
    index = build_search_index(test_records)
    print(f"Index: {index.total_docs} records, {len(index.term_index)} terms\n")

    print("=== Search Test ===")
    query = SearchQuery(query="energy transfer reeves", limit=10)
    response = search_records(query, index)
    print(f"Query: {response.query}")
    print(f"Results: {response.total_results} total, {response.returned_results} returned")
    print(f"Search time: {response.search_time_ms:.2f} ms\n")

    for result in response.results:
        print(f"[{result.score:.2f}] {result.snippet}")
