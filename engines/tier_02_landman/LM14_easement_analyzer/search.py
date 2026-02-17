"""
LM14 Easement Analyzer Engine - Search Module
================================================
Provides full-text search, faceted filtering, and geo-spatial lookup for
easements, rights-of-way, surface use agreements, and pipeline corridors.
Supports search by location, easement type, grantor, grantee, pipeline
operator, width, depth, instrument type, recording date, and status.

Components:
    - EasementRecord: Core data model for indexed easement records
    - EasementSearchIndex: TF-IDF inverted index with faceted filters
    - SearchQuery: Structured search request model
    - SearchResult: Ranked result with relevance score
    - build_search_index(): Build index from records
    - search_easements(): Execute search query
    - filter_by_location(): Geo filter by county/state
    - filter_by_type(): Filter by easement type
    - filter_by_operator(): Filter by pipeline operator
    - filter_by_dimensions(): Filter by width/depth range

Version: 1.0.0
Engine: LM14 Easement Analyzer
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

from loguru import logger


# ============================================================================
# ENUMS
# ============================================================================

class EasementType(str, Enum):
    EXPRESS = "express"
    IMPLIED_PRIOR_USE = "implied_prior_use"
    IMPLIED_NECESSITY = "implied_necessity"
    PRESCRIPTIVE = "prescriptive"
    APPURTENANT = "appurtenant"
    IN_GROSS = "in_gross"
    PIPELINE_ROW = "pipeline_row"
    ROAD = "road"
    UTILITY = "utility"
    CONSERVATION = "conservation"
    FLOWAGE = "flowage"
    RAILROAD = "railroad"
    SURFACE_USE = "surface_use"
    UNKNOWN = "unknown"


class EasementStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    ABANDONED = "abandoned"
    RELEASED = "released"
    DISPUTED = "disputed"
    PENDING = "pending"
    CONDEMNED = "condemned"
    UNKNOWN = "unknown"


class SortField(str, Enum):
    RELEVANCE = "relevance"
    DATE = "date"
    WIDTH = "width"
    COUNTY = "county"
    TYPE = "type"
    GRANTOR = "grantor"
    GRANTEE = "grantee"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


# ============================================================================
# EASEMENT RECORD MODEL
# ============================================================================

@dataclass
class EasementRecord:
    """Core data model for an indexed easement/ROW record."""

    record_id: str
    easement_type: EasementType
    status: EasementStatus

    # Parties
    grantor: str = ""
    grantee: str = ""
    pipeline_operator: str = ""

    # Location
    county: str = ""
    state: str = "TX"
    survey: str = ""
    abstract_number: str = ""
    section: str = ""
    block: str = ""
    township: str = ""
    range_: str = ""
    legal_description: str = ""

    # Recording info
    instrument_number: str = ""
    volume: str = ""
    page: str = ""
    recording_date: str = ""
    effective_date: str = ""
    expiration_date: str = ""

    # Dimensions
    width_ft: float = 0.0
    depth_ft: float = 0.0
    length_ft: float = 0.0
    acreage: float = 0.0
    temp_workspace_ft: float = 0.0

    # Pipeline specifics
    pipe_diameter_inches: float = 0.0
    product_type: str = ""
    operating_pressure_psi: float = 0.0

    # Financial
    consideration: float = 0.0
    annual_rental: float = 0.0

    # Description
    purpose: str = ""
    notes: str = ""
    restrictions: str = ""

    # Metadata
    source: str = ""
    indexed_at: str = ""
    content_hash: str = ""

    def __post_init__(self) -> None:
        if not self.indexed_at:
            self.indexed_at = datetime.now(timezone.utc).isoformat()
        if not self.content_hash:
            self.content_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        """SHA-256 hash of record content for deduplication."""
        payload = json.dumps(
            {
                "record_id": self.record_id,
                "easement_type": self.easement_type.value,
                "grantor": self.grantor,
                "grantee": self.grantee,
                "county": self.county,
                "instrument_number": self.instrument_number,
            },
            sort_keys=True,
        )
        return hashlib.sha256(payload.encode()).hexdigest()[:16]

    def searchable_text(self) -> str:
        """Concatenate all searchable fields into a single string."""
        parts = [
            self.grantor, self.grantee, self.pipeline_operator,
            self.county, self.state, self.survey, self.abstract_number,
            self.section, self.block, self.legal_description,
            self.instrument_number, self.purpose, self.notes,
            self.restrictions, self.product_type, self.source,
            self.easement_type.value, self.status.value,
            self.volume, self.page,
        ]
        return " ".join(p for p in parts if p).lower()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "record_id": self.record_id,
            "easement_type": self.easement_type.value,
            "status": self.status.value,
            "grantor": self.grantor,
            "grantee": self.grantee,
            "pipeline_operator": self.pipeline_operator,
            "county": self.county,
            "state": self.state,
            "survey": self.survey,
            "abstract_number": self.abstract_number,
            "section": self.section,
            "block": self.block,
            "township": self.township,
            "range": self.range_,
            "legal_description": self.legal_description,
            "instrument_number": self.instrument_number,
            "volume": self.volume,
            "page": self.page,
            "recording_date": self.recording_date,
            "effective_date": self.effective_date,
            "expiration_date": self.expiration_date,
            "width_ft": self.width_ft,
            "depth_ft": self.depth_ft,
            "length_ft": self.length_ft,
            "acreage": self.acreage,
            "temp_workspace_ft": self.temp_workspace_ft,
            "pipe_diameter_inches": self.pipe_diameter_inches,
            "product_type": self.product_type,
            "operating_pressure_psi": self.operating_pressure_psi,
            "consideration": self.consideration,
            "annual_rental": self.annual_rental,
            "purpose": self.purpose,
            "notes": self.notes,
            "restrictions": self.restrictions,
            "source": self.source,
            "content_hash": self.content_hash,
        }


# ============================================================================
# SEARCH QUERY MODEL
# ============================================================================

@dataclass
class SearchQuery:
    """Structured search request for the easement index."""

    # Free text
    query: str = ""

    # Filters
    easement_type: Optional[EasementType] = None
    status: Optional[EasementStatus] = None
    county: Optional[str] = None
    state: Optional[str] = None
    grantor: Optional[str] = None
    grantee: Optional[str] = None
    pipeline_operator: Optional[str] = None
    instrument_number: Optional[str] = None
    survey: Optional[str] = None
    abstract_number: Optional[str] = None
    product_type: Optional[str] = None
    source: Optional[str] = None

    # Dimension ranges
    min_width_ft: Optional[float] = None
    max_width_ft: Optional[float] = None
    min_depth_ft: Optional[float] = None
    max_depth_ft: Optional[float] = None
    min_diameter_inches: Optional[float] = None
    max_diameter_inches: Optional[float] = None

    # Date ranges
    recording_date_from: Optional[str] = None
    recording_date_to: Optional[str] = None

    # Pagination and sorting
    limit: int = 10
    offset: int = 0
    sort_by: SortField = SortField.RELEVANCE
    sort_order: SortOrder = SortOrder.DESC

    # Boost factors
    boost_texas: float = 1.5
    boost_permian: float = 1.3

    def has_filters(self) -> bool:
        """Return True if any filter is active."""
        filter_fields = [
            self.easement_type, self.status, self.county, self.state,
            self.grantor, self.grantee, self.pipeline_operator,
            self.instrument_number, self.survey, self.abstract_number,
            self.product_type, self.source,
            self.min_width_ft, self.max_width_ft,
            self.min_depth_ft, self.max_depth_ft,
            self.min_diameter_inches, self.max_diameter_inches,
            self.recording_date_from, self.recording_date_to,
        ]
        return any(f is not None for f in filter_fields)


# ============================================================================
# SEARCH RESULT MODEL
# ============================================================================

@dataclass
class SearchResult:
    """A single search result with relevance score."""

    record: EasementRecord
    score: float
    matched_terms: List[str] = dc_field(default_factory=list)
    highlights: Dict[str, str] = dc_field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "record": self.record.to_dict(),
            "score": round(self.score, 4),
            "matched_terms": self.matched_terms,
            "highlights": self.highlights,
        }


# ============================================================================
# SEARCH RESPONSE MODEL
# ============================================================================

@dataclass
class SearchResponse:
    """Complete search response with results and metadata."""

    results: List[SearchResult]
    total_hits: int
    query_time_ms: float
    offset: int
    limit: int
    facets: Dict[str, Dict[str, int]] = dc_field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "results": [r.to_dict() for r in self.results],
            "total_hits": self.total_hits,
            "query_time_ms": round(self.query_time_ms, 2),
            "offset": self.offset,
            "limit": self.limit,
            "facets": self.facets,
        }


# ============================================================================
# TF-IDF INVERTED INDEX
# ============================================================================

class TFIDFIndex:
    """Lightweight TF-IDF inverted index for easement record search."""

    def __init__(self) -> None:
        self._postings: Dict[str, Set[int]] = defaultdict(set)
        self._doc_freq: Dict[str, int] = Counter()
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_length: float = 0.0
        self._total_docs: int = 0

    def add_document(self, doc_id: int, text: str) -> None:
        """Add a document to the index."""
        tokens = self._tokenize(text)
        self._doc_lengths[doc_id] = len(tokens)
        seen: Set[str] = set()
        for token in tokens:
            self._postings[token].add(doc_id)
            if token not in seen:
                self._doc_freq[token] += 1
                seen.add(token)
        self._total_docs += 1
        total_length = sum(self._doc_lengths.values())
        self._avg_doc_length = total_length / max(self._total_docs, 1)

    def search(self, query: str, top_k: int = 50) -> List[Tuple[int, float]]:
        """Search the index and return (doc_id, score) pairs."""
        tokens = self._tokenize(query)
        if not tokens:
            return []

        scores: Dict[int, float] = defaultdict(float)

        for token in tokens:
            if token not in self._postings:
                continue
            df = self._doc_freq.get(token, 0)
            if df == 0:
                continue
            idf = math.log((self._total_docs - df + 0.5) / (df + 0.5) + 1.0)

            for doc_id in self._postings[token]:
                doc_len = self._doc_lengths.get(doc_id, 1)
                # BM25 scoring with k1=1.2, b=0.75
                tf = 1.0  # Binary TF for simplicity in inverted index
                k1 = 1.2
                b = 0.75
                norm = 1.0 - b + b * (doc_len / max(self._avg_doc_length, 1.0))
                tf_score = (tf * (k1 + 1.0)) / (tf + k1 * norm)
                scores[doc_id] += idf * tf_score

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into lowercase alphanumeric tokens."""
        return re.findall(r'[a-z0-9]+', text.lower())


# ============================================================================
# EASEMENT SEARCH INDEX
# ============================================================================

PERMIAN_COUNTIES: Set[str] = {
    "andrews", "borden", "crane", "crockett", "dawson", "ector",
    "gaines", "glasscock", "howard", "irion", "lea", "loving",
    "martin", "midland", "mitchell", "pecos", "reagan", "reeves",
    "scurry", "sterling", "terrell", "upton", "ward", "winkler", "yoakum",
}


class EasementSearchIndex:
    """Full-text + faceted search over easement records."""

    def __init__(self) -> None:
        self._records: List[EasementRecord] = []
        self._by_id: Dict[str, int] = {}
        self._tfidf: TFIDFIndex = TFIDFIndex()
        self._build_time: float = 0.0

        # Facet indices
        self._by_type: Dict[str, List[int]] = defaultdict(list)
        self._by_status: Dict[str, List[int]] = defaultdict(list)
        self._by_county: Dict[str, List[int]] = defaultdict(list)
        self._by_state: Dict[str, List[int]] = defaultdict(list)
        self._by_grantor: Dict[str, List[int]] = defaultdict(list)
        self._by_grantee: Dict[str, List[int]] = defaultdict(list)
        self._by_operator: Dict[str, List[int]] = defaultdict(list)
        self._by_product: Dict[str, List[int]] = defaultdict(list)

    @property
    def size(self) -> int:
        return len(self._records)

    def build(self, records: List[EasementRecord]) -> None:
        """Build the search index from a list of easement records."""
        start = time.time()
        self._records = list(records)
        self._by_id.clear()
        self._tfidf = TFIDFIndex()
        self._by_type.clear()
        self._by_status.clear()
        self._by_county.clear()
        self._by_state.clear()
        self._by_grantor.clear()
        self._by_grantee.clear()
        self._by_operator.clear()
        self._by_product.clear()

        for idx, rec in enumerate(records):
            self._by_id[rec.record_id] = idx
            self._tfidf.add_document(idx, rec.searchable_text())

            self._by_type[rec.easement_type.value.lower()].append(idx)
            self._by_status[rec.status.value.lower()].append(idx)
            if rec.county:
                self._by_county[rec.county.lower()].append(idx)
            if rec.state:
                self._by_state[rec.state.lower()].append(idx)
            if rec.grantor:
                self._by_grantor[rec.grantor.lower()].append(idx)
            if rec.grantee:
                self._by_grantee[rec.grantee.lower()].append(idx)
            if rec.pipeline_operator:
                self._by_operator[rec.pipeline_operator.lower()].append(idx)
            if rec.product_type:
                self._by_product[rec.product_type.lower()].append(idx)

        self._build_time = time.time() - start
        logger.info(f"Easement search index built: {len(records)} records in {self._build_time:.3f}s")

    def add_record(self, record: EasementRecord) -> None:
        """Add a single record to the live index."""
        idx = len(self._records)
        self._records.append(record)
        self._by_id[record.record_id] = idx
        self._tfidf.add_document(idx, record.searchable_text())

        self._by_type[record.easement_type.value.lower()].append(idx)
        self._by_status[record.status.value.lower()].append(idx)
        if record.county:
            self._by_county[record.county.lower()].append(idx)
        if record.state:
            self._by_state[record.state.lower()].append(idx)
        if record.grantor:
            self._by_grantor[record.grantor.lower()].append(idx)
        if record.grantee:
            self._by_grantee[record.grantee.lower()].append(idx)
        if record.pipeline_operator:
            self._by_operator[record.pipeline_operator.lower()].append(idx)
        if record.product_type:
            self._by_product[record.product_type.lower()].append(idx)

    def get_by_id(self, record_id: str) -> Optional[EasementRecord]:
        """Retrieve a record by ID."""
        idx = self._by_id.get(record_id)
        if idx is not None and idx < len(self._records):
            return self._records[idx]
        return None

    def search(self, query: SearchQuery) -> SearchResponse:
        """Execute a search query and return ranked results."""
        start = time.time()

        # Phase 1: Get candidate set from filters
        candidate_indices: Optional[Set[int]] = None

        if query.has_filters():
            candidate_indices = self._apply_filters(query)

        # Phase 2: Score candidates with TF-IDF
        if query.query.strip():
            tfidf_results = self._tfidf.search(query.query, top_k=500)
            scored: Dict[int, float] = {}
            for doc_id, score in tfidf_results:
                if candidate_indices is not None and doc_id not in candidate_indices:
                    continue
                scored[doc_id] = score
        elif candidate_indices is not None:
            scored = {idx: 1.0 for idx in candidate_indices}
        else:
            scored = {idx: 1.0 for idx in range(len(self._records))}

        # Phase 3: Apply boost factors
        for doc_id in list(scored.keys()):
            rec = self._records[doc_id]
            if rec.state.lower() == "tx":
                scored[doc_id] *= query.boost_texas
            if rec.county.lower() in PERMIAN_COUNTIES:
                scored[doc_id] *= query.boost_permian

        # Phase 4: Sort
        if query.sort_by == SortField.RELEVANCE:
            ranked = sorted(scored.items(), key=lambda x: x[1], reverse=(query.sort_order == SortOrder.DESC))
        elif query.sort_by == SortField.DATE:
            ranked = sorted(
                scored.items(),
                key=lambda x: self._records[x[0]].recording_date or "",
                reverse=(query.sort_order == SortOrder.DESC),
            )
        elif query.sort_by == SortField.WIDTH:
            ranked = sorted(
                scored.items(),
                key=lambda x: self._records[x[0]].width_ft,
                reverse=(query.sort_order == SortOrder.DESC),
            )
        elif query.sort_by == SortField.COUNTY:
            ranked = sorted(
                scored.items(),
                key=lambda x: self._records[x[0]].county.lower(),
                reverse=(query.sort_order == SortOrder.DESC),
            )
        elif query.sort_by == SortField.TYPE:
            ranked = sorted(
                scored.items(),
                key=lambda x: self._records[x[0]].easement_type.value,
                reverse=(query.sort_order == SortOrder.DESC),
            )
        elif query.sort_by == SortField.GRANTOR:
            ranked = sorted(
                scored.items(),
                key=lambda x: self._records[x[0]].grantor.lower(),
                reverse=(query.sort_order == SortOrder.DESC),
            )
        elif query.sort_by == SortField.GRANTEE:
            ranked = sorted(
                scored.items(),
                key=lambda x: self._records[x[0]].grantee.lower(),
                reverse=(query.sort_order == SortOrder.DESC),
            )
        else:
            ranked = sorted(scored.items(), key=lambda x: x[1], reverse=True)

        total_hits = len(ranked)

        # Phase 5: Paginate
        page = ranked[query.offset: query.offset + query.limit]

        # Phase 6: Build results with highlights
        query_tokens = set(re.findall(r'[a-z0-9]+', query.query.lower())) if query.query else set()
        results: List[SearchResult] = []
        for doc_id, score in page:
            rec = self._records[doc_id]
            matched = [t for t in query_tokens if t in rec.searchable_text()]
            highlights = self._build_highlights(rec, query_tokens)
            results.append(SearchResult(
                record=rec,
                score=score,
                matched_terms=matched,
                highlights=highlights,
            ))

        # Phase 7: Build facets
        facet_source = scored.keys() if scored else range(len(self._records))
        facets = self._build_facets(set(facet_source))

        query_time = (time.time() - start) * 1000

        return SearchResponse(
            results=results,
            total_hits=total_hits,
            query_time_ms=query_time,
            offset=query.offset,
            limit=query.limit,
            facets=facets,
        )

    def _apply_filters(self, query: SearchQuery) -> Set[int]:
        """Apply all filters and return intersection of matching indices."""
        sets: List[Set[int]] = []

        if query.easement_type is not None:
            indices = self._by_type.get(query.easement_type.value.lower(), [])
            sets.append(set(indices))

        if query.status is not None:
            indices = self._by_status.get(query.status.value.lower(), [])
            sets.append(set(indices))

        if query.county is not None:
            indices = self._by_county.get(query.county.lower(), [])
            sets.append(set(indices))

        if query.state is not None:
            indices = self._by_state.get(query.state.lower(), [])
            sets.append(set(indices))

        if query.grantor is not None:
            grantor_lower = query.grantor.lower()
            matching = set()
            for key, indices in self._by_grantor.items():
                if grantor_lower in key:
                    matching.update(indices)
            sets.append(matching)

        if query.grantee is not None:
            grantee_lower = query.grantee.lower()
            matching = set()
            for key, indices in self._by_grantee.items():
                if grantee_lower in key:
                    matching.update(indices)
            sets.append(matching)

        if query.pipeline_operator is not None:
            op_lower = query.pipeline_operator.lower()
            matching = set()
            for key, indices in self._by_operator.items():
                if op_lower in key:
                    matching.update(indices)
            sets.append(matching)

        if query.instrument_number is not None:
            inst_lower = query.instrument_number.lower()
            matching = {
                idx for idx, rec in enumerate(self._records)
                if inst_lower in rec.instrument_number.lower()
            }
            sets.append(matching)

        if query.survey is not None:
            survey_lower = query.survey.lower()
            matching = {
                idx for idx, rec in enumerate(self._records)
                if survey_lower in rec.survey.lower()
            }
            sets.append(matching)

        if query.abstract_number is not None:
            abs_lower = query.abstract_number.lower()
            matching = {
                idx for idx, rec in enumerate(self._records)
                if abs_lower in rec.abstract_number.lower()
            }
            sets.append(matching)

        if query.product_type is not None:
            indices = self._by_product.get(query.product_type.lower(), [])
            sets.append(set(indices))

        if query.source is not None:
            source_lower = query.source.lower()
            matching = {
                idx for idx, rec in enumerate(self._records)
                if source_lower in rec.source.lower()
            }
            sets.append(matching)

        # Dimension range filters
        if query.min_width_ft is not None:
            matching = {
                idx for idx, rec in enumerate(self._records)
                if rec.width_ft >= query.min_width_ft
            }
            sets.append(matching)

        if query.max_width_ft is not None:
            matching = {
                idx for idx, rec in enumerate(self._records)
                if rec.width_ft <= query.max_width_ft or rec.width_ft == 0.0
            }
            sets.append(matching)

        if query.min_depth_ft is not None:
            matching = {
                idx for idx, rec in enumerate(self._records)
                if rec.depth_ft >= query.min_depth_ft
            }
            sets.append(matching)

        if query.max_depth_ft is not None:
            matching = {
                idx for idx, rec in enumerate(self._records)
                if rec.depth_ft <= query.max_depth_ft or rec.depth_ft == 0.0
            }
            sets.append(matching)

        if query.min_diameter_inches is not None:
            matching = {
                idx for idx, rec in enumerate(self._records)
                if rec.pipe_diameter_inches >= query.min_diameter_inches
            }
            sets.append(matching)

        if query.max_diameter_inches is not None:
            matching = {
                idx for idx, rec in enumerate(self._records)
                if rec.pipe_diameter_inches <= query.max_diameter_inches or rec.pipe_diameter_inches == 0.0
            }
            sets.append(matching)

        # Date range filters
        if query.recording_date_from is not None:
            matching = {
                idx for idx, rec in enumerate(self._records)
                if rec.recording_date >= query.recording_date_from
            }
            sets.append(matching)

        if query.recording_date_to is not None:
            matching = {
                idx for idx, rec in enumerate(self._records)
                if rec.recording_date <= query.recording_date_to or not rec.recording_date
            }
            sets.append(matching)

        if not sets:
            return set(range(len(self._records)))

        result = sets[0]
        for s in sets[1:]:
            result = result.intersection(s)
        return result

    def _build_highlights(self, record: EasementRecord, query_tokens: Set[str]) -> Dict[str, str]:
        """Build highlight snippets for matched fields."""
        highlights: Dict[str, str] = {}
        if not query_tokens:
            return highlights

        fields = {
            "grantor": record.grantor,
            "grantee": record.grantee,
            "pipeline_operator": record.pipeline_operator,
            "purpose": record.purpose,
            "notes": record.notes,
            "legal_description": record.legal_description,
            "county": record.county,
        }

        for field_name, field_value in fields.items():
            if not field_value:
                continue
            field_lower = field_value.lower()
            for token in query_tokens:
                if token in field_lower:
                    highlighted = re.sub(
                        f'({re.escape(token)})',
                        r'**\1**',
                        field_value,
                        flags=re.IGNORECASE,
                    )
                    highlights[field_name] = highlighted
                    break

        return highlights

    def _build_facets(self, doc_ids: Set[int]) -> Dict[str, Dict[str, int]]:
        """Build facet counts for the result set."""
        type_counts: Dict[str, int] = Counter()
        status_counts: Dict[str, int] = Counter()
        county_counts: Dict[str, int] = Counter()
        operator_counts: Dict[str, int] = Counter()
        product_counts: Dict[str, int] = Counter()

        for doc_id in doc_ids:
            if doc_id >= len(self._records):
                continue
            rec = self._records[doc_id]
            type_counts[rec.easement_type.value] += 1
            status_counts[rec.status.value] += 1
            if rec.county:
                county_counts[rec.county] += 1
            if rec.pipeline_operator:
                operator_counts[rec.pipeline_operator] += 1
            if rec.product_type:
                product_counts[rec.product_type] += 1

        return {
            "easement_type": dict(type_counts.most_common(20)),
            "status": dict(status_counts.most_common(10)),
            "county": dict(county_counts.most_common(30)),
            "pipeline_operator": dict(operator_counts.most_common(20)),
            "product_type": dict(product_counts.most_common(10)),
        }

    def facet_summary(self) -> Dict[str, Any]:
        """Return summary of all facets across the entire index."""
        all_ids = set(range(len(self._records)))
        return self._build_facets(all_ids)

    def get_records_by_type(self, easement_type: EasementType) -> List[EasementRecord]:
        """Get all records of a given type."""
        indices = self._by_type.get(easement_type.value.lower(), [])
        return [self._records[i] for i in indices]

    def get_records_by_county(self, county: str) -> List[EasementRecord]:
        """Get all records in a given county."""
        indices = self._by_county.get(county.lower(), [])
        return [self._records[i] for i in indices]

    def get_records_by_operator(self, operator: str) -> List[EasementRecord]:
        """Get all records for a given pipeline operator."""
        op_lower = operator.lower()
        matching: List[EasementRecord] = []
        for key, indices in self._by_operator.items():
            if op_lower in key:
                matching.extend(self._records[i] for i in indices)
        return matching

    def export_all(self) -> List[Dict[str, Any]]:
        """Export all records as serializable dicts."""
        return [r.to_dict() for r in self._records]


# ============================================================================
# MODULE-LEVEL FUNCTIONS
# ============================================================================

_SEARCH_INDEX: Optional[EasementSearchIndex] = None


def build_search_index(records: Optional[List[EasementRecord]] = None) -> EasementSearchIndex:
    """Build and return the global search index."""
    global _SEARCH_INDEX
    _SEARCH_INDEX = EasementSearchIndex()
    if records:
        _SEARCH_INDEX.build(records)
    logger.info(f"LM14 search index built: {_SEARCH_INDEX.size} records")
    return _SEARCH_INDEX


def get_search_index() -> EasementSearchIndex:
    """Return the global search index, building if necessary."""
    global _SEARCH_INDEX
    if _SEARCH_INDEX is None:
        return build_search_index()
    return _SEARCH_INDEX


def search_easements(
    query: str = "",
    easement_type: Optional[str] = None,
    county: Optional[str] = None,
    state: Optional[str] = None,
    grantor: Optional[str] = None,
    grantee: Optional[str] = None,
    pipeline_operator: Optional[str] = None,
    min_width_ft: Optional[float] = None,
    max_width_ft: Optional[float] = None,
    min_depth_ft: Optional[float] = None,
    max_depth_ft: Optional[float] = None,
    limit: int = 10,
    offset: int = 0,
) -> SearchResponse:
    """Convenience function for simple searches."""
    etype = None
    if easement_type:
        try:
            etype = EasementType(easement_type)
        except ValueError:
            logger.warning(f"Unknown easement type: {easement_type}")

    sq = SearchQuery(
        query=query,
        easement_type=etype,
        county=county,
        state=state,
        grantor=grantor,
        grantee=grantee,
        pipeline_operator=pipeline_operator,
        min_width_ft=min_width_ft,
        max_width_ft=max_width_ft,
        min_depth_ft=min_depth_ft,
        max_depth_ft=max_depth_ft,
        limit=limit,
        offset=offset,
    )
    return get_search_index().search(sq)


def filter_by_location(county: Optional[str] = None, state: Optional[str] = None) -> List[EasementRecord]:
    """Filter records by county and/or state."""
    idx = get_search_index()
    sq = SearchQuery(county=county, state=state, limit=1000)
    response = idx.search(sq)
    return [r.record for r in response.results]


def filter_by_type(easement_type: EasementType) -> List[EasementRecord]:
    """Filter records by easement type."""
    return get_search_index().get_records_by_type(easement_type)


def filter_by_operator(operator: str) -> List[EasementRecord]:
    """Filter records by pipeline operator."""
    return get_search_index().get_records_by_operator(operator)


def filter_by_dimensions(
    min_width_ft: Optional[float] = None,
    max_width_ft: Optional[float] = None,
    min_depth_ft: Optional[float] = None,
    max_depth_ft: Optional[float] = None,
) -> List[EasementRecord]:
    """Filter records by dimension ranges."""
    sq = SearchQuery(
        min_width_ft=min_width_ft,
        max_width_ft=max_width_ft,
        min_depth_ft=min_depth_ft,
        max_depth_ft=max_depth_ft,
        limit=1000,
    )
    response = get_search_index().search(sq)
    return [r.record for r in response.results]


def search_index_health() -> Dict[str, Any]:
    """Return health metrics for the search index."""
    idx = get_search_index()
    return {
        "total_records": idx.size,
        "build_time_sec": round(idx._build_time, 4),
        "facets": idx.facet_summary(),
    }
