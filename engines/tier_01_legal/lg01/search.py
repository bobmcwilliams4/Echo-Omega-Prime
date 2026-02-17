"""
LG01 CONTRACT ANALYSIS ENGINE - Contract Clause Search Engine
High-performance search layer for contract clause retrieval, doctrine matching,
and contract comparison operations.

Architecture:
    - In-memory inverted index for sub-millisecond clause lookup
    - TF-IDF scoring with configurable boost factors
    - Fuzzy matching via trigram similarity
    - Faceted search by clause type, risk level, contract type
    - Deterministic ranking for reproducible results

Engine: LG01 Contract Analysis Engine
Tier: 1 (LEGAL)
Mode: DET (Deterministic)
Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
"""

import hashlib
import math
import re
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Any, FrozenSet

from loguru import logger


# ============================================================================
# CONFIGURATION
# ============================================================================

MAX_RESULTS_DEFAULT: int = 50
MIN_RELEVANCE_SCORE: float = 0.3
FUZZY_THRESHOLD: float = 0.7
BOOST_EXACT_MATCH: float = 2.0
BOOST_CLAUSE_TYPE: float = 1.5
BOOST_RISK_LEVEL: float = 1.3
BOOST_RECENT: float = 1.1
TRIGRAM_MIN_LENGTH: int = 3


# ============================================================================
# ENUMS
# ============================================================================

class SearchScope(str, Enum):
    """Scope of search operation."""
    CLAUSES = "clauses"
    DOCTRINES = "doctrines"
    CONTRACTS = "contracts"
    ALL = "all"


class SortOrder(str, Enum):
    """Sort order for search results."""
    RELEVANCE = "relevance"
    DATE = "date"
    RISK = "risk"
    CLAUSE_TYPE = "clause_type"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class SearchDocument:
    """A searchable document in the index."""
    doc_id: str
    doc_type: str
    title: str
    content: str
    clause_type: Optional[str] = None
    contract_type: Optional[str] = None
    risk_level: Optional[str] = None
    jurisdiction: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    content_hash: str = ""

    def __post_init__(self) -> None:
        if not self.content_hash:
            self.content_hash = hashlib.sha256(self.content.encode("utf-8")).hexdigest()[:16]


@dataclass
class SearchResult:
    """A single search result with scoring details."""
    doc_id: str
    doc_type: str
    title: str
    snippet: str
    relevance_score: float
    clause_type: Optional[str] = None
    contract_type: Optional[str] = None
    risk_level: Optional[str] = None
    jurisdiction: Optional[str] = None
    match_terms: List[str] = field(default_factory=list)
    highlight_positions: List[Tuple[int, int]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for API response."""
        return {
            "doc_id": self.doc_id,
            "doc_type": self.doc_type,
            "title": self.title,
            "snippet": self.snippet,
            "relevance_score": round(self.relevance_score, 4),
            "clause_type": self.clause_type,
            "contract_type": self.contract_type,
            "risk_level": self.risk_level,
            "jurisdiction": self.jurisdiction,
            "match_terms": self.match_terms,
            "metadata": self.metadata,
        }


@dataclass
class SearchQuery:
    """Structured search query with filters."""
    query_text: str
    scope: SearchScope = SearchScope.ALL
    clause_type_filter: Optional[str] = None
    contract_type_filter: Optional[str] = None
    risk_level_filter: Optional[str] = None
    jurisdiction_filter: Optional[str] = None
    tag_filter: Optional[List[str]] = None
    max_results: int = MAX_RESULTS_DEFAULT
    sort_by: SortOrder = SortOrder.RELEVANCE
    min_score: float = MIN_RELEVANCE_SCORE
    fuzzy_enabled: bool = True


@dataclass
class SearchStats:
    """Search engine statistics."""
    total_documents: int
    total_terms: int
    index_size_bytes: int
    avg_document_length: float
    queries_processed: int
    avg_query_latency_ms: float
    cache_hit_rate: float
    last_indexed: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for API response."""
        return {
            "total_documents": self.total_documents,
            "total_terms": self.total_terms,
            "index_size_bytes": self.index_size_bytes,
            "avg_document_length": round(self.avg_document_length, 2),
            "queries_processed": self.queries_processed,
            "avg_query_latency_ms": round(self.avg_query_latency_ms, 2),
            "cache_hit_rate": round(self.cache_hit_rate, 3),
            "last_indexed": self.last_indexed,
        }


# ============================================================================
# TEXT PROCESSING UTILITIES
# ============================================================================

_STOP_WORDS: FrozenSet[str] = frozenset({
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "shall", "should", "may", "might", "can", "could", "must",
    "that", "this", "these", "those", "it", "its", "not", "no", "nor",
    "so", "if", "then", "than", "too", "very", "just", "about", "above",
    "after", "again", "all", "also", "any", "because", "before", "between",
    "both", "each", "few", "here", "how", "into", "more", "most", "other",
    "out", "own", "same", "some", "such", "there", "through", "under",
    "up", "what", "when", "where", "which", "while", "who", "whom", "why",
})

_LEGAL_STOP_WORDS: FrozenSet[str] = frozenset({
    "herein", "hereof", "hereto", "hereby", "hereunder", "hereinafter",
    "thereof", "thereto", "therein", "thereby", "thereunder", "thereupon",
    "whereas", "witnesseth", "notwithstanding", "aforesaid", "aforementioned",
    "pursuant", "henceforth", "forthwith",
})

_TOKEN_PATTERN: re.Pattern = re.compile(r"[a-zA-Z][a-zA-Z0-9\-']*[a-zA-Z0-9]|[a-zA-Z]", re.ASCII)


def tokenize(text: str) -> List[str]:
    """Tokenize text into lowercase terms, removing stop words.

    Args:
        text: Raw text to tokenize.

    Returns:
        List of lowercase tokens with stop words removed.
    """
    tokens = _TOKEN_PATTERN.findall(text.lower())
    return [t for t in tokens if t not in _STOP_WORDS and t not in _LEGAL_STOP_WORDS and len(t) > 1]


def extract_ngrams(text: str, n: int = 3) -> Set[str]:
    """Extract character n-grams from text for fuzzy matching.

    Args:
        text: Input text.
        n: N-gram size (default 3 for trigrams).

    Returns:
        Set of n-gram strings.
    """
    padded = f"  {text.lower()}  "
    return {padded[i:i + n] for i in range(len(padded) - n + 1)}


def trigram_similarity(text1: str, text2: str) -> float:
    """Compute trigram similarity between two strings.

    Args:
        text1: First string.
        text2: Second string.

    Returns:
        Similarity score between 0.0 and 1.0.
    """
    if not text1 or not text2:
        return 0.0
    trigrams1 = extract_ngrams(text1)
    trigrams2 = extract_ngrams(text2)
    intersection = trigrams1 & trigrams2
    union = trigrams1 | trigrams2
    if not union:
        return 0.0
    return len(intersection) / len(union)


def extract_snippet(content: str, query_terms: List[str], max_length: int = 300) -> str:
    """Extract a relevant snippet from content around matching terms.

    Args:
        content: Full document content.
        query_terms: Terms to find in content.
        max_length: Maximum snippet length.

    Returns:
        Extracted snippet with context around first match.
    """
    if not content:
        return ""
    if not query_terms:
        return content[:max_length] + ("..." if len(content) > max_length else "")

    lower_content = content.lower()
    best_pos = -1
    for term in query_terms:
        pos = lower_content.find(term.lower())
        if pos != -1:
            best_pos = pos
            break

    if best_pos == -1:
        return content[:max_length] + ("..." if len(content) > max_length else "")

    context = max_length // 2
    start = max(0, best_pos - context)
    end = min(len(content), best_pos + context)
    snippet = content[start:end]

    if start > 0:
        snippet = "..." + snippet
    if end < len(content):
        snippet = snippet + "..."

    return snippet


# ============================================================================
# INVERTED INDEX
# ============================================================================

class InvertedIndex:
    """In-memory inverted index for fast full-text search.

    Supports TF-IDF scoring, exact match boosting, and fuzzy matching
    via trigram similarity. Thread-safe for concurrent reads.
    """

    def __init__(self) -> None:
        self._index: Dict[str, Dict[str, float]] = defaultdict(dict)
        self._documents: Dict[str, SearchDocument] = {}
        self._doc_lengths: Dict[str, int] = {}
        self._doc_term_freqs: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self._total_docs: int = 0
        self._total_terms: int = 0
        self._avg_doc_length: float = 0.0
        self._term_doc_counts: Dict[str, int] = defaultdict(int)
        self._last_indexed: Optional[str] = None

    def add_document(self, doc: SearchDocument) -> None:
        """Add a document to the index.

        Args:
            doc: SearchDocument to index.
        """
        self._documents[doc.doc_id] = doc

        terms = tokenize(doc.content)
        if doc.title:
            title_terms = tokenize(doc.title)
            terms.extend(title_terms)
            terms.extend(title_terms)

        if doc.clause_type:
            clause_terms = tokenize(doc.clause_type.replace("_", " "))
            terms.extend(clause_terms)
            terms.extend(clause_terms)

        for tag in doc.tags:
            terms.extend(tokenize(tag))

        self._doc_lengths[doc.doc_id] = len(terms)

        term_counts: Dict[str, int] = defaultdict(int)
        for term in terms:
            term_counts[term] += 1

        seen_terms: Set[str] = set()
        for term, count in term_counts.items():
            tf = count / max(1, len(terms))
            self._index[term][doc.doc_id] = tf
            self._doc_term_freqs[doc.doc_id][term] = count
            if term not in seen_terms:
                self._term_doc_counts[term] += 1
                seen_terms.add(term)

        self._total_docs = len(self._documents)
        self._total_terms = len(self._index)
        total_length = sum(self._doc_lengths.values())
        self._avg_doc_length = total_length / max(1, self._total_docs)
        self._last_indexed = datetime.now(timezone.utc).isoformat()

    def remove_document(self, doc_id: str) -> bool:
        """Remove a document from the index.

        Args:
            doc_id: ID of document to remove.

        Returns:
            True if document was found and removed.
        """
        if doc_id not in self._documents:
            return False

        for term in list(self._index.keys()):
            if doc_id in self._index[term]:
                del self._index[term][doc_id]
                self._term_doc_counts[term] = max(0, self._term_doc_counts[term] - 1)
                if not self._index[term]:
                    del self._index[term]
                    del self._term_doc_counts[term]

        del self._documents[doc_id]
        if doc_id in self._doc_lengths:
            del self._doc_lengths[doc_id]
        if doc_id in self._doc_term_freqs:
            del self._doc_term_freqs[doc_id]

        self._total_docs = len(self._documents)
        self._total_terms = len(self._index)
        if self._total_docs > 0:
            self._avg_doc_length = sum(self._doc_lengths.values()) / self._total_docs
        else:
            self._avg_doc_length = 0.0

        return True

    def search(self, query: SearchQuery) -> List[SearchResult]:
        """Execute a search query against the index.

        Args:
            query: Structured search query with filters and options.

        Returns:
            Ranked list of SearchResult objects.
        """
        start_time = time.time()

        query_terms = tokenize(query.query_text)
        if not query_terms and not query.clause_type_filter:
            return []

        scores: Dict[str, float] = defaultdict(float)
        match_terms: Dict[str, Set[str]] = defaultdict(set)

        for term in query_terms:
            if term in self._index:
                idf = math.log(1 + self._total_docs / (1 + self._term_doc_counts.get(term, 0)))
                for doc_id, tf in self._index[term].items():
                    doc_len = self._doc_lengths.get(doc_id, 1)
                    bm25_tf = (tf * 2.2) / (tf + 1.2 * (1 - 0.75 + 0.75 * doc_len / max(1, self._avg_doc_length)))
                    scores[doc_id] += bm25_tf * idf
                    match_terms[doc_id].add(term)

        if query.fuzzy_enabled and query_terms:
            query_text_lower = query.query_text.lower()
            for doc_id, doc in self._documents.items():
                if doc_id in scores:
                    continue
                similarity = trigram_similarity(query_text_lower, doc.title.lower() if doc.title else "")
                if similarity >= FUZZY_THRESHOLD:
                    scores[doc_id] = similarity * 0.5
                    match_terms[doc_id].add(f"~fuzzy:{query.query_text}")

        exact_phrase = query.query_text.lower()
        for doc_id, doc in self._documents.items():
            if exact_phrase in doc.content.lower() or (doc.title and exact_phrase in doc.title.lower()):
                scores[doc_id] = scores.get(doc_id, 0) * BOOST_EXACT_MATCH
                if not scores.get(doc_id):
                    scores[doc_id] = BOOST_EXACT_MATCH
                match_terms[doc_id].add(f"exact:{query.query_text}")

        filtered_scores: Dict[str, float] = {}
        for doc_id, score in scores.items():
            doc = self._documents.get(doc_id)
            if not doc:
                continue

            if query.scope != SearchScope.ALL:
                if query.scope == SearchScope.CLAUSES and doc.doc_type != "clause":
                    continue
                if query.scope == SearchScope.DOCTRINES and doc.doc_type != "doctrine":
                    continue
                if query.scope == SearchScope.CONTRACTS and doc.doc_type != "contract":
                    continue

            if query.clause_type_filter and doc.clause_type != query.clause_type_filter:
                continue
            if query.contract_type_filter and doc.contract_type != query.contract_type_filter:
                continue
            if query.risk_level_filter and doc.risk_level != query.risk_level_filter:
                continue
            if query.jurisdiction_filter and doc.jurisdiction != query.jurisdiction_filter:
                continue
            if query.tag_filter:
                doc_tags_lower = {t.lower() for t in doc.tags}
                if not any(t.lower() in doc_tags_lower for t in query.tag_filter):
                    continue

            boosted_score = score
            if doc.clause_type and query.clause_type_filter and doc.clause_type == query.clause_type_filter:
                boosted_score *= BOOST_CLAUSE_TYPE
            if doc.risk_level in ("critical", "high"):
                boosted_score *= BOOST_RISK_LEVEL

            if boosted_score >= query.min_score:
                filtered_scores[doc_id] = boosted_score

        sorted_docs = sorted(filtered_scores.items(), key=lambda x: -x[1])

        if query.sort_by == SortOrder.DATE:
            sorted_docs = sorted(
                filtered_scores.items(),
                key=lambda x: self._documents[x[0]].timestamp,
                reverse=True,
            )
        elif query.sort_by == SortOrder.RISK:
            risk_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "negligible": 4}
            sorted_docs = sorted(
                filtered_scores.items(),
                key=lambda x: (
                    risk_order.get(self._documents[x[0]].risk_level or "negligible", 5),
                    -x[1],
                ),
            )

        results: List[SearchResult] = []
        for doc_id, score in sorted_docs[:query.max_results]:
            doc = self._documents[doc_id]
            snippet = extract_snippet(doc.content, list(match_terms.get(doc_id, set())), 300)
            results.append(SearchResult(
                doc_id=doc.doc_id,
                doc_type=doc.doc_type,
                title=doc.title,
                snippet=snippet,
                relevance_score=score,
                clause_type=doc.clause_type,
                contract_type=doc.contract_type,
                risk_level=doc.risk_level,
                jurisdiction=doc.jurisdiction,
                match_terms=sorted(match_terms.get(doc_id, set())),
                metadata=doc.metadata,
            ))

        elapsed_ms = (time.time() - start_time) * 1000
        logger.debug(
            "Search completed: query='{}' results={} latency={:.1f}ms",
            query.query_text[:50], len(results), elapsed_ms,
        )

        return results

    def get_document(self, doc_id: str) -> Optional[SearchDocument]:
        """Retrieve a document by ID."""
        return self._documents.get(doc_id)

    def get_stats(self) -> SearchStats:
        """Get index statistics."""
        index_bytes = sum(
            len(term.encode("utf-8")) + len(docs) * 16
            for term, docs in self._index.items()
        )
        return SearchStats(
            total_documents=self._total_docs,
            total_terms=self._total_terms,
            index_size_bytes=index_bytes,
            avg_document_length=self._avg_doc_length,
            queries_processed=0,
            avg_query_latency_ms=0.0,
            cache_hit_rate=0.0,
            last_indexed=self._last_indexed,
        )

    def get_all_clause_types(self) -> List[str]:
        """Get all unique clause types in the index."""
        types: Set[str] = set()
        for doc in self._documents.values():
            if doc.clause_type:
                types.add(doc.clause_type)
        return sorted(types)

    def get_all_contract_types(self) -> List[str]:
        """Get all unique contract types in the index."""
        types: Set[str] = set()
        for doc in self._documents.values():
            if doc.contract_type:
                types.add(doc.contract_type)
        return sorted(types)

    def get_documents_by_type(self, doc_type: str) -> List[SearchDocument]:
        """Get all documents of a specific type."""
        return [doc for doc in self._documents.values() if doc.doc_type == doc_type]

    def clear(self) -> None:
        """Clear the entire index."""
        self._index.clear()
        self._documents.clear()
        self._doc_lengths.clear()
        self._doc_term_freqs.clear()
        self._term_doc_counts.clear()
        self._total_docs = 0
        self._total_terms = 0
        self._avg_doc_length = 0.0


# ============================================================================
# CONTRACT COMPARISON ENGINE
# ============================================================================

@dataclass
class ClauseDiff:
    """Difference between two clauses."""
    clause_type: str
    status: str  # "added", "removed", "modified", "unchanged"
    contract_a_text: Optional[str]
    contract_b_text: Optional[str]
    similarity_score: float
    risk_delta: Optional[str] = None
    significance: str = "medium"
    recommendation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for API response."""
        return {
            "clause_type": self.clause_type,
            "status": self.status,
            "contract_a_text": self.contract_a_text[:500] if self.contract_a_text else None,
            "contract_b_text": self.contract_b_text[:500] if self.contract_b_text else None,
            "similarity_score": round(self.similarity_score, 4),
            "risk_delta": self.risk_delta,
            "significance": self.significance,
            "recommendation": self.recommendation,
        }


@dataclass
class ComparisonResult:
    """Result of comparing two contracts."""
    comparison_id: str
    contract_a_id: str
    contract_b_id: str
    timestamp: str
    total_clauses_compared: int
    clauses_added: int
    clauses_removed: int
    clauses_modified: int
    clauses_unchanged: int
    overall_similarity: float
    risk_assessment_delta: str
    diffs: List[ClauseDiff]
    determinism_hash: str

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for API response."""
        return {
            "comparison_id": self.comparison_id,
            "contract_a_id": self.contract_a_id,
            "contract_b_id": self.contract_b_id,
            "timestamp": self.timestamp,
            "total_clauses_compared": self.total_clauses_compared,
            "clauses_added": self.clauses_added,
            "clauses_removed": self.clauses_removed,
            "clauses_modified": self.clauses_modified,
            "clauses_unchanged": self.clauses_unchanged,
            "overall_similarity": round(self.overall_similarity, 4),
            "risk_assessment_delta": self.risk_assessment_delta,
            "diffs": [d.to_dict() for d in self.diffs],
            "determinism_hash": self.determinism_hash,
        }


def compare_clauses(
    clauses_a: Dict[str, str],
    clauses_b: Dict[str, str],
    contract_a_id: str = "contract_a",
    contract_b_id: str = "contract_b",
) -> ComparisonResult:
    """Compare two sets of contract clauses.

    Args:
        clauses_a: Dict mapping clause_type to clause text for contract A.
        clauses_b: Dict mapping clause_type to clause text for contract B.
        contract_a_id: Identifier for contract A.
        contract_b_id: Identifier for contract B.

    Returns:
        ComparisonResult with detailed diff analysis.
    """
    comparison_id = str(uuid.uuid4())
    all_types = sorted(set(list(clauses_a.keys()) + list(clauses_b.keys())))

    diffs: List[ClauseDiff] = []
    added = 0
    removed = 0
    modified = 0
    unchanged = 0
    total_similarity = 0.0

    high_risk_types = {
        "indemnification", "limitation_of_liability", "termination",
        "governing_law", "dispute_resolution", "confidentiality",
        "change_of_control", "force_majeure", "assignment",
    }

    for clause_type in all_types:
        text_a = clauses_a.get(clause_type)
        text_b = clauses_b.get(clause_type)

        if text_a and not text_b:
            diffs.append(ClauseDiff(
                clause_type=clause_type,
                status="removed",
                contract_a_text=text_a,
                contract_b_text=None,
                similarity_score=0.0,
                risk_delta="increased" if clause_type in high_risk_types else "neutral",
                significance="high" if clause_type in high_risk_types else "medium",
                recommendation=f"Clause '{clause_type}' removed in contract B. Review if this creates exposure.",
            ))
            removed += 1

        elif not text_a and text_b:
            diffs.append(ClauseDiff(
                clause_type=clause_type,
                status="added",
                contract_a_text=None,
                contract_b_text=text_b,
                similarity_score=0.0,
                risk_delta="review_needed",
                significance="high" if clause_type in high_risk_types else "medium",
                recommendation=f"New clause '{clause_type}' added in contract B. Review terms carefully.",
            ))
            added += 1

        elif text_a and text_b:
            sim = trigram_similarity(text_a, text_b)
            total_similarity += sim

            if sim > 0.95:
                diffs.append(ClauseDiff(
                    clause_type=clause_type,
                    status="unchanged",
                    contract_a_text=text_a,
                    contract_b_text=text_b,
                    similarity_score=sim,
                    risk_delta="neutral",
                    significance="low",
                    recommendation="No material change detected.",
                ))
                unchanged += 1
            else:
                significance = "high" if clause_type in high_risk_types and sim < 0.7 else "medium"
                risk_delta = "review_needed" if sim < 0.7 else "minor_change"
                diffs.append(ClauseDiff(
                    clause_type=clause_type,
                    status="modified",
                    contract_a_text=text_a,
                    contract_b_text=text_b,
                    similarity_score=sim,
                    risk_delta=risk_delta,
                    significance=significance,
                    recommendation=f"Clause '{clause_type}' modified (similarity: {sim:.1%}). Review changes.",
                ))
                modified += 1

    total_compared = len(all_types)
    overall_sim = total_similarity / max(1, total_compared - added - removed)

    if removed > 3 and any(d.clause_type in high_risk_types for d in diffs if d.status == "removed"):
        risk_delta = "significantly_increased"
    elif modified > 5:
        risk_delta = "moderately_increased"
    elif added > 0 and modified == 0 and removed == 0:
        risk_delta = "review_additions"
    else:
        risk_delta = "minimal_change"

    hash_input = f"{contract_a_id}|{contract_b_id}|{json.dumps(sorted(all_types))}"
    determinism_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    return ComparisonResult(
        comparison_id=comparison_id,
        contract_a_id=contract_a_id,
        contract_b_id=contract_b_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        total_clauses_compared=total_compared,
        clauses_added=added,
        clauses_removed=removed,
        clauses_modified=modified,
        clauses_unchanged=unchanged,
        overall_similarity=overall_sim,
        risk_assessment_delta=risk_delta,
        diffs=diffs,
        determinism_hash=determinism_hash,
    )


# ============================================================================
# BOILERPLATE DETECTOR
# ============================================================================

_BOILERPLATE_SIGNATURES: Dict[str, List[str]] = {
    "severability": [
        "if any provision of this agreement",
        "shall be deemed invalid",
        "remaining provisions shall continue",
        "severable",
    ],
    "entire_agreement": [
        "entire agreement between the parties",
        "supersedes all prior",
        "all prior agreements",
        "prior negotiations",
    ],
    "counterparts": [
        "executed in counterparts",
        "each of which shall be deemed an original",
        "facsimile signature",
    ],
    "waiver": [
        "failure to enforce",
        "shall not constitute a waiver",
        "no waiver shall be effective",
        "waiver of any breach",
    ],
    "headings": [
        "headings are for convenience only",
        "shall not affect the interpretation",
        "section headings",
    ],
    "notices": [
        "all notices shall be in writing",
        "deemed given when delivered",
        "certified mail return receipt",
        "overnight courier",
    ],
    "amendment": [
        "may not be amended except",
        "in writing signed by both parties",
        "written amendment",
        "no oral modification",
    ],
    "assignment_standard": [
        "may not assign this agreement",
        "without the prior written consent",
        "binding upon successors",
    ],
    "governing_law_standard": [
        "governed by and construed in accordance with",
        "the laws of the state of",
        "without regard to conflict of laws",
    ],
    "force_majeure_standard": [
        "neither party shall be liable",
        "beyond reasonable control",
        "acts of god",
        "force majeure event",
    ],
}


def detect_boilerplate(clause_text: str, clause_type: Optional[str] = None) -> Tuple[bool, float, str]:
    """Detect whether a clause is standard boilerplate.

    Args:
        clause_text: The clause text to analyze.
        clause_type: Optional clause type hint.

    Returns:
        Tuple of (is_boilerplate, confidence, matched_pattern).
    """
    lower_text = clause_text.lower()

    best_match = ""
    best_score = 0.0

    for pattern_name, signatures in _BOILERPLATE_SIGNATURES.items():
        matched = sum(1 for sig in signatures if sig in lower_text)
        total = len(signatures)
        if total > 0:
            score = matched / total
            if score > best_score:
                best_score = score
                best_match = pattern_name

    if clause_type and clause_type.lower().replace("_", " ") in best_match.replace("_", " "):
        best_score = min(1.0, best_score * 1.2)

    is_boilerplate = best_score >= 0.5
    return is_boilerplate, round(best_score, 3), best_match


def compute_customization_score(clause_text: str, clause_type: Optional[str] = None) -> float:
    """Compute how customized a clause is vs standard boilerplate.

    A score of 0.0 means fully standard boilerplate.
    A score of 1.0 means fully customized language.

    Args:
        clause_text: The clause text to analyze.
        clause_type: Optional clause type hint.

    Returns:
        Customization score between 0.0 and 1.0.
    """
    is_boilerplate, boilerplate_confidence, _ = detect_boilerplate(clause_text, clause_type)
    return round(1.0 - boilerplate_confidence, 3)


# Need json for compare_clauses hash computation
import json

# ============================================================================
# SINGLETON INDEX
# ============================================================================

_global_index: Optional[InvertedIndex] = None


def get_search_index() -> InvertedIndex:
    """Get the global search index singleton."""
    global _global_index
    if _global_index is None:
        _global_index = InvertedIndex()
        logger.info("LG01 search index initialized")
    return _global_index
