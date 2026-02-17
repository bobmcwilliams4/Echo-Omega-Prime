"""
LM03 Division Order Engine - Search Module
============================================

Search functionality for division order records, doctrine blocks,
interest owners, and revenue distribution data.

Includes:
- DoctrineSearchIndex with TF-IDF scoring
- DivisionOrderSearcher for multi-field search
- InterestTracer for chain-of-title interest tracking
- RevenueDistributionCalculator for payment computation
- SuspenseAnalyzer for suspense status management

500+ lines. Production-ready. Pure Python TF-IDF.

Author: ECHO OMEGA PRIME Build System
Engine: LM03 Division Order
"""

from __future__ import annotations

import hashlib
import math
import re
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from loguru import logger


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class SearchField(str, Enum):
    """Fields available for division order search."""
    OWNER_NAME = "owner_name"
    INTEREST_TYPE = "interest_type"
    WELL_NAME = "well_name"
    OPERATOR = "operator"
    LEGAL_DESCRIPTION = "legal_description"
    COUNTY = "county"
    TRACT = "tract"
    LEASE_NAME = "lease_name"
    SUSPENSE_CODE = "suspense_code"
    PAYMENT_STATUS = "payment_status"
    FULL_TEXT = "full_text"


class SortOrder(str, Enum):
    """Sort order options."""
    RELEVANCE_DESC = "relevance_desc"
    OWNER_ASC = "owner_asc"
    DECIMAL_DESC = "decimal_desc"
    DATE_ASC = "date_asc"
    DATE_DESC = "date_desc"


class SuspenseCode(str, Enum):
    """Standard suspense codes."""
    NO_DIVISION_ORDER = "S01"
    TITLE_DEFECT = "S02"
    ADDRESS_UNKNOWN = "S03"
    DECEASED_OWNER = "S04"
    PENDING_PROBATE = "S05"
    DISPUTE = "S06"
    MISSING_W9 = "S07"
    LIEN = "S08"
    MINOR = "S09"
    INCOMPETENT = "S10"
    BANKRUPTCY = "S11"
    IRS_LEVY = "S12"
    GARNISHMENT = "S13"
    OWNERSHIP_CHANGE = "S14"
    POOLING_DISPUTE = "S15"
    UNIT_PENDING = "S16"
    UNCLAIMED = "S17"
    FEDERAL_LIEN = "S18"
    COURT_ORDER = "S19"
    OPERATOR_REVIEW = "S20"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class SearchQuery:
    """A structured search query for division order records."""
    query_id: str = ""
    owner_name: Optional[str] = None
    interest_type: Optional[str] = None
    well_name: Optional[str] = None
    operator: Optional[str] = None
    legal_description: Optional[str] = None
    county: Optional[str] = None
    lease_name: Optional[str] = None
    suspense_code: Optional[str] = None
    decimal_min: Optional[Decimal] = None
    decimal_max: Optional[Decimal] = None
    effective_date_from: Optional[date] = None
    effective_date_to: Optional[date] = None
    full_text: Optional[str] = None
    max_results: int = 50
    offset: int = 0
    sort_order: SortOrder = SortOrder.RELEVANCE_DESC

    def __post_init__(self) -> None:
        if not self.query_id:
            parts = [
                self.owner_name or "",
                self.interest_type or "",
                self.well_name or "",
                self.full_text or "",
            ]
            h = hashlib.sha256("|".join(parts).encode()).hexdigest()[:12]
            self.query_id = f"Q-{h}"

    def has_criteria(self) -> bool:
        """Check if the query has any search criteria."""
        return any([
            self.owner_name, self.interest_type, self.well_name,
            self.operator, self.legal_description, self.county,
            self.lease_name, self.suspense_code, self.decimal_min,
            self.decimal_max, self.effective_date_from, self.effective_date_to,
            self.full_text,
        ])

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "query_id": self.query_id,
            "owner_name": self.owner_name,
            "interest_type": self.interest_type,
            "well_name": self.well_name,
            "operator": self.operator,
            "legal_description": self.legal_description,
            "county": self.county,
            "lease_name": self.lease_name,
            "suspense_code": self.suspense_code,
            "decimal_min": str(self.decimal_min) if self.decimal_min else None,
            "decimal_max": str(self.decimal_max) if self.decimal_max else None,
            "effective_date_from": self.effective_date_from.isoformat() if self.effective_date_from else None,
            "effective_date_to": self.effective_date_to.isoformat() if self.effective_date_to else None,
            "full_text": self.full_text,
            "max_results": self.max_results,
            "offset": self.offset,
            "sort_order": self.sort_order.value,
        }


@dataclass
class SearchResult:
    """A single search result with relevance scoring."""
    owner_name: str
    interest_type: str
    decimal_interest: str
    well_name: str
    operator: str
    county: Optional[str] = None
    legal_description: Optional[str] = None
    lease_name: Optional[str] = None
    effective_date: Optional[date] = None
    suspense_code: Optional[str] = None
    suspense_reason: Optional[str] = None
    relevance_score: float = 0.0
    match_fields: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "owner_name": self.owner_name,
            "interest_type": self.interest_type,
            "decimal_interest": self.decimal_interest,
            "well_name": self.well_name,
            "operator": self.operator,
            "county": self.county,
            "legal_description": self.legal_description,
            "lease_name": self.lease_name,
            "effective_date": self.effective_date.isoformat() if self.effective_date else None,
            "suspense_code": self.suspense_code,
            "suspense_reason": self.suspense_reason,
            "relevance_score": round(self.relevance_score, 4),
            "match_fields": self.match_fields,
        }


@dataclass
class SearchResponse:
    """Response wrapper for search results."""
    query_id: str
    total_matches: int
    results: List[SearchResult]
    execution_time_ms: float
    offset: int = 0
    limit: int = 50

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "query_id": self.query_id,
            "total_matches": self.total_matches,
            "results": [r.to_dict() for r in self.results],
            "execution_time_ms": round(self.execution_time_ms, 2),
            "offset": self.offset,
            "limit": self.limit,
        }


# ---------------------------------------------------------------------------
# TF-IDF Index
# ---------------------------------------------------------------------------

_STOP_WORDS: Set[str] = {
    "the", "a", "an", "and", "or", "of", "to", "in", "for", "is", "on",
    "at", "by", "with", "from", "as", "be", "was", "are", "were", "been",
    "has", "have", "had", "do", "does", "did", "but", "not", "this", "that",
    "it", "its", "can", "will", "may", "shall", "should", "would", "could",
    "all", "each", "every", "any", "no", "nor", "so", "than", "too",
}


def _tokenize(text: str) -> List[str]:
    """Tokenize text into lowercase words, removing stop words.

    Args:
        text: Input text.

    Returns:
        List of filtered tokens.
    """
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return [w for w in words if w not in _STOP_WORDS and len(w) > 1]


class DoctrineSearchIndex:
    """TF-IDF inverted index over doctrine blocks.

    Builds an index from doctrine cache blocks for fast relevance-scored search.
    """

    def __init__(self) -> None:
        """Initialize an empty search index."""
        self._documents: Dict[str, str] = {}
        self._doc_metadata: Dict[str, Dict[str, Any]] = {}
        self._term_doc_freq: Dict[str, int] = defaultdict(int)
        self._doc_term_freq: Dict[str, Dict[str, int]] = {}
        self._doc_lengths: Dict[str, int] = {}
        self._total_docs: int = 0
        logger.debug("DoctrineSearchIndex initialized")

    def add_document(
        self,
        doc_id: str,
        text: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a document to the index.

        Args:
            doc_id: Unique document identifier.
            text: Document text content.
            metadata: Optional metadata dictionary.
        """
        tokens = _tokenize(text)
        self._documents[doc_id] = text
        self._doc_metadata[doc_id] = metadata or {}
        term_counts = Counter(tokens)
        self._doc_term_freq[doc_id] = dict(term_counts)
        self._doc_lengths[doc_id] = len(tokens)
        for term in term_counts:
            self._term_doc_freq[term] += 1
        self._total_docs += 1

    def search(self, query: str, max_results: int = 10) -> List[Tuple[str, float, Dict[str, Any]]]:
        """Search the index using TF-IDF scoring.

        Args:
            query: Search query string.
            max_results: Maximum results to return.

        Returns:
            List of (doc_id, score, metadata) tuples sorted by relevance.
        """
        query_tokens = _tokenize(query)
        if not query_tokens:
            return []
        scores: Dict[str, float] = defaultdict(float)
        for term in query_tokens:
            if term not in self._term_doc_freq:
                continue
            df = self._term_doc_freq[term]
            idf = math.log((self._total_docs + 1) / (df + 1)) + 1.0
            for doc_id, term_freqs in self._doc_term_freq.items():
                if term in term_freqs:
                    tf = term_freqs[term] / max(self._doc_lengths.get(doc_id, 1), 1)
                    scores[doc_id] += tf * idf

        if not scores:
            return []
        max_score = max(scores.values()) if scores else 1.0
        results: List[Tuple[str, float, Dict[str, Any]]] = []
        for doc_id, score in scores.items():
            normalized = score / max_score if max_score > 0 else 0.0
            results.append((doc_id, normalized, self._doc_metadata.get(doc_id, {})))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:max_results]

    def get_document(self, doc_id: str) -> Optional[str]:
        """Get document text by ID."""
        return self._documents.get(doc_id)

    def get_document_count(self) -> int:
        """Get total number of indexed documents."""
        return self._total_docs

    def get_vocabulary_size(self) -> int:
        """Get number of unique terms in the index."""
        return len(self._term_doc_freq)

    def health_check(self) -> Dict[str, Any]:
        """Return index health status."""
        return {
            "status": "healthy",
            "total_documents": self._total_docs,
            "vocabulary_size": len(self._term_doc_freq),
            "avg_doc_length": (
                sum(self._doc_lengths.values()) / max(len(self._doc_lengths), 1)
                if self._doc_lengths else 0
            ),
        }


# ---------------------------------------------------------------------------
# Division Order Searcher
# ---------------------------------------------------------------------------

class DivisionOrderSearcher:
    """Multi-field search for division order records.

    Supports owner name, interest type, well name, operator, county,
    decimal range, date range, and suspense status filtering.
    """

    def __init__(self) -> None:
        """Initialize the searcher."""
        self._records: List[Dict[str, Any]] = []
        self._name_index: Dict[str, List[int]] = defaultdict(list)
        logger.debug("DivisionOrderSearcher initialized")

    def add_record(self, record: Dict[str, Any]) -> None:
        """Add a division order record to the searchable index.

        Args:
            record: Dictionary with owner_name, interest_type, decimal_interest,
                    well_name, operator, county, etc.
        """
        idx = len(self._records)
        self._records.append(record)
        owner = record.get("owner_name", "").upper()
        for part in owner.split():
            self._name_index[part].append(idx)

    def search(self, query: SearchQuery) -> SearchResponse:
        """Execute a search query against division order records.

        Args:
            query: Structured search query.

        Returns:
            SearchResponse with matching results.
        """
        start = time.time()
        candidates = list(range(len(self._records)))

        if query.owner_name:
            candidates = self._filter_by_name(candidates, query.owner_name)
        if query.interest_type:
            candidates = [
                i for i in candidates
                if self._records[i].get("interest_type", "").upper() == query.interest_type.upper()
            ]
        if query.well_name:
            well_upper = query.well_name.upper()
            candidates = [
                i for i in candidates
                if well_upper in self._records[i].get("well_name", "").upper()
            ]
        if query.operator:
            op_upper = query.operator.upper()
            candidates = [
                i for i in candidates
                if op_upper in self._records[i].get("operator", "").upper()
            ]
        if query.county:
            county_upper = query.county.upper()
            candidates = [
                i for i in candidates
                if self._records[i].get("county", "").upper() == county_upper
            ]
        if query.suspense_code:
            candidates = [
                i for i in candidates
                if self._records[i].get("suspense_code", "") == query.suspense_code
            ]
        if query.decimal_min is not None:
            candidates = [
                i for i in candidates
                if Decimal(str(self._records[i].get("decimal_interest", "0"))) >= query.decimal_min
            ]
        if query.decimal_max is not None:
            candidates = [
                i for i in candidates
                if Decimal(str(self._records[i].get("decimal_interest", "1"))) <= query.decimal_max
            ]

        results: List[SearchResult] = []
        for idx in candidates:
            rec = self._records[idx]
            score = self._compute_relevance(rec, query)
            match_fields = self._get_match_fields(rec, query)
            results.append(SearchResult(
                owner_name=rec.get("owner_name", ""),
                interest_type=rec.get("interest_type", ""),
                decimal_interest=rec.get("decimal_interest", "0"),
                well_name=rec.get("well_name", ""),
                operator=rec.get("operator", ""),
                county=rec.get("county"),
                legal_description=rec.get("legal_description"),
                lease_name=rec.get("lease_name"),
                effective_date=rec.get("effective_date"),
                suspense_code=rec.get("suspense_code"),
                suspense_reason=rec.get("suspense_reason"),
                relevance_score=score,
                match_fields=match_fields,
            ))

        if query.sort_order == SortOrder.RELEVANCE_DESC:
            results.sort(key=lambda r: r.relevance_score, reverse=True)
        elif query.sort_order == SortOrder.OWNER_ASC:
            results.sort(key=lambda r: r.owner_name)
        elif query.sort_order == SortOrder.DECIMAL_DESC:
            results.sort(key=lambda r: Decimal(r.decimal_interest), reverse=True)
        elif query.sort_order == SortOrder.DATE_ASC:
            results.sort(key=lambda r: r.effective_date or date.min)
        elif query.sort_order == SortOrder.DATE_DESC:
            results.sort(key=lambda r: r.effective_date or date.min, reverse=True)

        total = len(results)
        page = results[query.offset:query.offset + query.max_results]
        elapsed = (time.time() - start) * 1000

        return SearchResponse(
            query_id=query.query_id,
            total_matches=total,
            results=page,
            execution_time_ms=elapsed,
            offset=query.offset,
            limit=query.max_results,
        )

    def _filter_by_name(self, candidates: List[int], name: str) -> List[int]:
        """Filter candidates by owner name with fuzzy matching."""
        name_upper = name.upper()
        name_parts = name_upper.split()
        matching: Set[int] = set()
        for part in name_parts:
            if part in self._name_index:
                matching.update(self._name_index[part])
        if not matching:
            for idx in candidates:
                owner = self._records[idx].get("owner_name", "").upper()
                if name_upper in owner:
                    matching.add(idx)
        return [i for i in candidates if i in matching]

    def _compute_relevance(self, record: Dict[str, Any], query: SearchQuery) -> float:
        """Compute relevance score for a record against a query."""
        score = 0.0
        if query.owner_name:
            owner = record.get("owner_name", "").upper()
            query_upper = query.owner_name.upper()
            if query_upper == owner:
                score += 0.40
            elif query_upper in owner:
                score += 0.25
        if query.interest_type and record.get("interest_type", "").upper() == query.interest_type.upper():
            score += 0.20
        if query.well_name and query.well_name.upper() in record.get("well_name", "").upper():
            score += 0.20
        if query.county and record.get("county", "").upper() == query.county.upper():
            score += 0.10
        if query.operator and query.operator.upper() in record.get("operator", "").upper():
            score += 0.10
        return min(score, 1.0)

    def _get_match_fields(self, record: Dict[str, Any], query: SearchQuery) -> List[str]:
        """Identify which fields matched the query."""
        matched: List[str] = []
        if query.owner_name and query.owner_name.upper() in record.get("owner_name", "").upper():
            matched.append("owner_name")
        if query.interest_type and record.get("interest_type", "").upper() == query.interest_type.upper():
            matched.append("interest_type")
        if query.well_name and query.well_name.upper() in record.get("well_name", "").upper():
            matched.append("well_name")
        if query.operator and query.operator.upper() in record.get("operator", "").upper():
            matched.append("operator")
        if query.county and record.get("county", "").upper() == query.county.upper():
            matched.append("county")
        return matched

    def get_record_count(self) -> int:
        """Return total number of indexed records."""
        return len(self._records)


# ---------------------------------------------------------------------------
# Interest Tracer
# ---------------------------------------------------------------------------

class InterestTracer:
    """Traces interests through a chain of conveyance events.

    Tracks each owner's current decimal interest across all conveyances,
    applying Duhig rule when applicable, and computing final positions.
    """

    QUANTIZE_SPEC = Decimal("0.00000001")
    ROUNDING = ROUND_HALF_UP

    def __init__(self) -> None:
        """Initialize the interest tracer."""
        self._ownership: Dict[str, Decimal] = {}
        self._trace_log: List[Dict[str, Any]] = []
        logger.debug("InterestTracer initialized")

    def set_initial_ownership(self, owner: str, interest: Decimal) -> None:
        """Set the initial ownership for the sovereign or original patentee.

        Args:
            owner: Owner name.
            interest: Initial interest decimal (typically 1.0).
        """
        self._ownership[owner.upper()] = interest
        self._trace_log.append({
            "event": "initial_ownership",
            "owner": owner,
            "interest": str(interest),
        })

    def process_conveyance(
        self,
        grantor: str,
        grantee: str,
        interest_conveyed: Decimal,
        reservation: Optional[Decimal] = None,
        is_warranty_deed: bool = False,
        document_ref: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Process a conveyance through the chain.

        Applies Duhig rule if warranty deed and grantor lacks sufficient interest.

        Args:
            grantor: Grantor name.
            grantee: Grantee name.
            interest_conveyed: Interest amount being conveyed.
            reservation: Optional interest reserved by grantor.
            is_warranty_deed: Whether the conveyance is by warranty deed.
            document_ref: Optional document reference.

        Returns:
            Dictionary with conveyance result details.
        """
        grantor_upper = grantor.upper()
        grantee_upper = grantee.upper()
        current_ownership = self._ownership.get(grantor_upper, Decimal("0"))

        reservation_amount = reservation or Decimal("0")
        needed = interest_conveyed + reservation_amount
        duhig_applied = False

        if is_warranty_deed and current_ownership < needed and current_ownership > Decimal("0"):
            grantee_gets = current_ownership
            grantor_keeps = Decimal("0")
            duhig_applied = True
            logger.info(
                "Duhig rule applied: {g} only owns {o}, cannot satisfy conveyance {c} + reservation {r}",
                g=grantor, o=current_ownership, c=interest_conveyed, r=reservation_amount,
            )
        elif current_ownership >= interest_conveyed:
            grantee_gets = interest_conveyed
            grantor_keeps = current_ownership - interest_conveyed
        else:
            grantee_gets = current_ownership
            grantor_keeps = Decimal("0")

        self._ownership[grantor_upper] = grantor_keeps.quantize(self.QUANTIZE_SPEC, rounding=self.ROUNDING)
        existing_grantee = self._ownership.get(grantee_upper, Decimal("0"))
        self._ownership[grantee_upper] = (existing_grantee + grantee_gets).quantize(
            self.QUANTIZE_SPEC, rounding=self.ROUNDING
        )

        if self._ownership[grantor_upper] == Decimal("0"):
            del self._ownership[grantor_upper]

        result = {
            "grantor": grantor,
            "grantee": grantee,
            "interest_conveyed": str(interest_conveyed),
            "reservation": str(reservation_amount),
            "grantor_prior_ownership": str(current_ownership),
            "grantee_receives": str(grantee_gets),
            "grantor_retains": str(grantor_keeps),
            "duhig_applied": duhig_applied,
            "document_ref": document_ref,
        }
        self._trace_log.append(result)
        return result

    def get_current_ownership(self) -> Dict[str, str]:
        """Return current ownership positions.

        Returns:
            Dictionary mapping owner names to their decimal interest strings.
        """
        return {k: str(v) for k, v in self._ownership.items() if v > Decimal("0")}

    def get_trace_log(self) -> List[Dict[str, Any]]:
        """Return the full trace log."""
        return list(self._trace_log)

    def unity_check(self) -> Dict[str, Any]:
        """Verify ownership sums to unity."""
        total = sum(self._ownership.values(), Decimal("0")).quantize(
            self.QUANTIZE_SPEC, rounding=self.ROUNDING
        )
        deviation = abs(total - Decimal("1.00000000"))
        return {
            "total": str(total),
            "deviation": str(deviation),
            "passes": deviation <= Decimal("0.00001000"),
            "owner_count": len(self._ownership),
        }


# ---------------------------------------------------------------------------
# Revenue Distribution Calculator
# ---------------------------------------------------------------------------

class RevenueDistributionCalculator:
    """Computes revenue distribution for a well or unit.

    Takes gross revenue and a pay deck, applies severance tax
    and deductions, and computes individual owner payments.
    """

    OIL_SEVERANCE_RATE = Decimal("0.046")
    GAS_SEVERANCE_RATE = Decimal("0.075")

    def __init__(self) -> None:
        """Initialize the calculator."""
        self._distribution_log: List[Dict[str, Any]] = []

    def distribute(
        self,
        gross_revenue: Decimal,
        product_type: str,
        pay_deck: List[Dict[str, Any]],
        deductions: Decimal = Decimal("0"),
        custom_tax_rate: Optional[Decimal] = None,
    ) -> Dict[str, Any]:
        """Distribute revenue to all owners in the pay deck.

        Args:
            gross_revenue: Total gross revenue for the period.
            product_type: 'OIL' or 'GAS'.
            pay_deck: List of pay deck entries with owner_name, decimal_interest, interest_type.
            deductions: Total post-production deductions.
            custom_tax_rate: Override severance tax rate.

        Returns:
            Distribution result with individual payments and totals.
        """
        tax_rate = custom_tax_rate
        if tax_rate is None:
            tax_rate = self.OIL_SEVERANCE_RATE if product_type.upper() == "OIL" else self.GAS_SEVERANCE_RATE

        total_tax = (gross_revenue * tax_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        net_revenue = gross_revenue - total_tax - deductions

        payments: List[Dict[str, Any]] = []
        total_distributed = Decimal("0")
        total_suspense = Decimal("0")

        for entry in pay_deck:
            decimal_interest = Decimal(str(entry.get("decimal_interest", "0")))
            owner_share = (net_revenue * decimal_interest).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            owner_tax = (total_tax * decimal_interest).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            is_suspense = entry.get("suspense_code") is not None

            payment = {
                "owner_name": entry.get("owner_name", ""),
                "interest_type": entry.get("interest_type", ""),
                "decimal_interest": str(decimal_interest),
                "gross_share": str((gross_revenue * decimal_interest).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
                "severance_tax": str(owner_tax),
                "deductions": str((deductions * decimal_interest).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
                "net_payment": str(owner_share),
                "suspense": is_suspense,
                "suspense_code": entry.get("suspense_code"),
            }
            payments.append(payment)

            if is_suspense:
                total_suspense += owner_share
            else:
                total_distributed += owner_share

        result = {
            "gross_revenue": str(gross_revenue),
            "product_type": product_type.upper(),
            "severance_tax_rate": str(tax_rate),
            "total_severance_tax": str(total_tax),
            "total_deductions": str(deductions),
            "net_revenue": str(net_revenue),
            "total_distributed": str(total_distributed),
            "total_suspense": str(total_suspense),
            "payment_count": len(payments),
            "suspense_count": sum(1 for p in payments if p["suspense"]),
            "payments": payments,
        }
        self._distribution_log.append(result)
        return result

    def get_distribution_log(self) -> List[Dict[str, Any]]:
        """Return the distribution audit log."""
        return list(self._distribution_log)


# ---------------------------------------------------------------------------
# Suspense Analyzer
# ---------------------------------------------------------------------------

class SuspenseAnalyzer:
    """Analyzes suspense status for division order administration.

    Tracks suspense entries, identifies escheat candidates,
    and generates suspense reports.
    """

    ESCHEAT_THRESHOLD_MONTHS = 36

    def __init__(self) -> None:
        """Initialize the suspense analyzer."""
        self._suspense_entries: List[Dict[str, Any]] = []

    def add_suspense_entry(
        self,
        owner_name: str,
        interest_type: str,
        decimal_interest: str,
        well_name: str,
        suspense_code: str,
        suspense_date: date,
        accumulated_amount: Decimal = Decimal("0"),
        notes: Optional[str] = None,
    ) -> None:
        """Add a suspense entry.

        Args:
            owner_name: Owner name.
            interest_type: Interest type code.
            decimal_interest: Decimal interest string.
            well_name: Well name.
            suspense_code: Suspense reason code (S01-S20).
            suspense_date: Date placed in suspense.
            accumulated_amount: Total revenue accumulated in suspense.
            notes: Optional notes.
        """
        self._suspense_entries.append({
            "owner_name": owner_name,
            "interest_type": interest_type,
            "decimal_interest": decimal_interest,
            "well_name": well_name,
            "suspense_code": suspense_code,
            "suspense_date": suspense_date,
            "accumulated_amount": str(accumulated_amount),
            "notes": notes,
        })

    def get_escheat_candidates(self, as_of_date: date) -> List[Dict[str, Any]]:
        """Identify entries that have been in suspense long enough for escheat.

        Args:
            as_of_date: Current date for comparison.

        Returns:
            List of entries that are escheat candidates.
        """
        candidates: List[Dict[str, Any]] = []
        for entry in self._suspense_entries:
            susp_date = entry["suspense_date"]
            months_in_suspense = (as_of_date.year - susp_date.year) * 12 + (as_of_date.month - susp_date.month)
            if months_in_suspense >= self.ESCHEAT_THRESHOLD_MONTHS:
                candidates.append({
                    **entry,
                    "months_in_suspense": months_in_suspense,
                    "escheat_eligible": True,
                    "suspense_date": susp_date.isoformat(),
                })
        return candidates

    def get_suspense_summary(self) -> Dict[str, Any]:
        """Generate a summary of all suspense entries.

        Returns:
            Summary dictionary.
        """
        by_code: Dict[str, int] = defaultdict(int)
        total_amount = Decimal("0")
        for entry in self._suspense_entries:
            by_code[entry["suspense_code"]] += 1
            total_amount += Decimal(entry["accumulated_amount"])

        return {
            "total_entries": len(self._suspense_entries),
            "total_accumulated_amount": str(total_amount),
            "by_suspense_code": dict(by_code),
        }

    def get_all_entries(self) -> List[Dict[str, Any]]:
        """Return all suspense entries."""
        result = []
        for entry in self._suspense_entries:
            copy = dict(entry)
            if isinstance(copy.get("suspense_date"), date):
                copy["suspense_date"] = copy["suspense_date"].isoformat()
            result.append(copy)
        return result
