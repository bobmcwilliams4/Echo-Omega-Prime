"""
LG05 LITIGATION RISK ENGINE - Case Law & Precedent Search Engine
High-performance search layer for case law retrieval, doctrine matching,
and precedent comparison operations.

Architecture:
    - In-memory inverted index for sub-millisecond lookup
    - TF-IDF scoring with configurable boost factors
    - Fuzzy matching via trigram similarity
    - Faceted search by litigation type, risk level, jurisdiction
    - Deterministic ranking for reproducible results

Engine: LG05 | Tier: 1 (LEGAL) | Mode: DET | Port: 8395 | Authority: 5.0
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
BOOST_CASE_TYPE: float = 1.5
BOOST_RISK_LEVEL: float = 1.3
BOOST_RECENT_PRECEDENT: float = 1.2
TRIGRAM_MIN_LENGTH: int = 3


# ============================================================================
# ENUMS
# ============================================================================

class SearchScope(str, Enum):
    CASES = "cases"
    DOCTRINES = "doctrines"
    STATUTES = "statutes"
    ALL = "all"


class SortOrder(str, Enum):
    RELEVANCE = "relevance"
    DATE = "date"
    RISK = "risk"
    JURISDICTION = "jurisdiction"


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
    litigation_type: Optional[str] = None
    jurisdiction: Optional[str] = None
    risk_level: Optional[str] = None
    year: Optional[int] = None
    citation: Optional[str] = None
    court: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    indexed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def text_for_index(self) -> str:
        """Combined text for indexing."""
        parts = [self.title, self.content]
        if self.litigation_type:
            parts.append(self.litigation_type)
        if self.jurisdiction:
            parts.append(self.jurisdiction)
        if self.citation:
            parts.append(self.citation)
        parts.extend(self.tags)
        return " ".join(parts)


@dataclass
class SearchQuery:
    """A search query with filters."""
    text: str
    scope: SearchScope = SearchScope.ALL
    litigation_type: Optional[str] = None
    jurisdiction: Optional[str] = None
    risk_level: Optional[str] = None
    min_year: Optional[int] = None
    max_year: Optional[int] = None
    court: Optional[str] = None
    max_results: int = MAX_RESULTS_DEFAULT
    sort_by: SortOrder = SortOrder.RELEVANCE
    fuzzy: bool = True


@dataclass
class SearchResult:
    """A single search result."""
    doc_id: str
    doc_type: str
    title: str
    snippet: str
    relevance_score: float
    litigation_type: Optional[str]
    jurisdiction: Optional[str]
    risk_level: Optional[str]
    year: Optional[int]
    citation: Optional[str]
    court: Optional[str]
    match_terms: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComparisonResult:
    """Result of comparing two cases or claims."""
    doc_a_id: str
    doc_b_id: str
    similarity_score: float
    common_terms: List[str]
    unique_to_a: List[str]
    unique_to_b: List[str]
    risk_differential: float
    recommendation: str


@dataclass
class CaseDiff:
    """Difference between two case analyses."""
    field_name: str
    value_a: str
    value_b: str
    significance: str


# ============================================================================
# TRIGRAM SIMILARITY
# ============================================================================

def _extract_trigrams(text: str) -> Set[str]:
    """Extract character trigrams from text."""
    text = text.lower().strip()
    if len(text) < TRIGRAM_MIN_LENGTH:
        return {text}
    padded = f"  {text} "
    return {padded[i:i + 3] for i in range(len(padded) - 2)}


def trigram_similarity(text_a: str, text_b: str) -> float:
    """Compute trigram similarity between two texts."""
    if not text_a or not text_b:
        return 0.0
    trigrams_a = _extract_trigrams(text_a)
    trigrams_b = _extract_trigrams(text_b)
    if not trigrams_a or not trigrams_b:
        return 0.0
    intersection = trigrams_a & trigrams_b
    union = trigrams_a | trigrams_b
    return len(intersection) / len(union) if union else 0.0


def extract_snippet(content: str, query_terms: List[str], max_length: int = 200) -> str:
    """Extract a relevant snippet from content around query terms."""
    if not content:
        return ""
    content_lower = content.lower()
    best_pos = 0
    best_score = 0

    for term in query_terms:
        term_lower = term.lower()
        pos = content_lower.find(term_lower)
        if pos >= 0:
            score = sum(1 for t in query_terms if t.lower() in content_lower[max(0, pos - 100):pos + 100])
            if score > best_score:
                best_score = score
                best_pos = pos

    start = max(0, best_pos - max_length // 2)
    end = min(len(content), start + max_length)
    snippet = content[start:end].strip()

    if start > 0:
        snippet = "..." + snippet
    if end < len(content):
        snippet = snippet + "..."

    return snippet


# ============================================================================
# TOKENIZER
# ============================================================================

_STOP_WORDS: FrozenSet[str] = frozenset({
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "has", "he", "in", "is", "it", "its", "of", "on", "or", "she",
    "that", "the", "to", "was", "were", "will", "with", "this",
    "but", "they", "have", "had", "what", "when", "where", "who",
    "which", "their", "been", "would", "could", "should", "may",
    "can", "do", "did", "does", "not", "no", "if", "than", "then",
    "there", "these", "those", "such", "so", "very", "just", "also",
})

_TOKEN_PATTERN = re.compile(r"[a-z0-9_]+(?:[-'][a-z0-9_]+)*", re.IGNORECASE)


def tokenize(text: str, remove_stops: bool = True) -> List[str]:
    """Tokenize text into terms."""
    if not text:
        return []
    tokens = _TOKEN_PATTERN.findall(text.lower())
    if remove_stops:
        tokens = [t for t in tokens if t not in _STOP_WORDS and len(t) > 1]
    return tokens


# ============================================================================
# INVERTED INDEX
# ============================================================================

class InvertedIndex:
    """In-memory inverted index for fast text search."""

    def __init__(self) -> None:
        self._index: Dict[str, Dict[str, float]] = defaultdict(dict)
        self._documents: Dict[str, SearchDocument] = {}
        self._doc_lengths: Dict[str, int] = {}
        self._total_docs: int = 0
        self._avg_doc_length: float = 0.0
        self._doc_count_by_term: Dict[str, int] = defaultdict(int)

    def add_document(self, doc: SearchDocument) -> None:
        """Index a document."""
        tokens = tokenize(doc.text_for_index)
        if not tokens:
            return

        self._documents[doc.doc_id] = doc
        self._doc_lengths[doc.doc_id] = len(tokens)
        self._total_docs += 1

        total_len = sum(self._doc_lengths.values())
        self._avg_doc_length = total_len / self._total_docs if self._total_docs else 0

        term_freq: Dict[str, int] = defaultdict(int)
        for token in tokens:
            term_freq[token] += 1

        seen_terms: Set[str] = set()
        for token, freq in term_freq.items():
            tf = freq / len(tokens)
            self._index[token][doc.doc_id] = tf
            if token not in seen_terms:
                self._doc_count_by_term[token] += 1
                seen_terms.add(token)

    def remove_document(self, doc_id: str) -> bool:
        """Remove a document from the index."""
        if doc_id not in self._documents:
            return False

        tokens_to_clean: List[str] = []
        for term, postings in self._index.items():
            if doc_id in postings:
                del postings[doc_id]
                tokens_to_clean.append(term)

        for term in tokens_to_clean:
            self._doc_count_by_term[term] = max(0, self._doc_count_by_term[term] - 1)
            if not self._index[term]:
                del self._index[term]
                del self._doc_count_by_term[term]

        del self._documents[doc_id]
        del self._doc_lengths[doc_id]
        self._total_docs -= 1
        if self._total_docs > 0:
            self._avg_doc_length = sum(self._doc_lengths.values()) / self._total_docs
        else:
            self._avg_doc_length = 0.0
        return True

    def search(self, query: SearchQuery) -> List[SearchResult]:
        """Execute a search query against the index."""
        start = time.time()
        query_tokens = tokenize(query.text)
        if not query_tokens:
            return []

        scores: Dict[str, float] = defaultdict(float)
        match_terms: Dict[str, List[str]] = defaultdict(list)

        for token in query_tokens:
            if token in self._index:
                idf = math.log(
                    (self._total_docs - self._doc_count_by_term.get(token, 0) + 0.5)
                    / (self._doc_count_by_term.get(token, 0) + 0.5)
                    + 1.0
                )
                for doc_id, tf in self._index[token].items():
                    doc_len = self._doc_lengths.get(doc_id, 1)
                    k1 = 1.5
                    b = 0.75
                    norm_tf = (tf * (k1 + 1)) / (
                        tf + k1 * (1 - b + b * doc_len / max(self._avg_doc_length, 1))
                    )
                    score = idf * norm_tf
                    scores[doc_id] += score
                    match_terms[doc_id].append(token)
            elif query.fuzzy:
                for indexed_term in self._index:
                    sim = trigram_similarity(token, indexed_term)
                    if sim >= FUZZY_THRESHOLD:
                        idf = math.log(
                            (self._total_docs + 0.5) / (self._doc_count_by_term.get(indexed_term, 0) + 0.5)
                        )
                        for doc_id, tf in self._index[indexed_term].items():
                            scores[doc_id] += idf * tf * sim * 0.5
                            if indexed_term not in match_terms[doc_id]:
                                match_terms[doc_id].append(f"~{indexed_term}")

        # Apply boosts
        for doc_id in list(scores.keys()):
            doc = self._documents.get(doc_id)
            if not doc:
                continue

            # Exact title match boost
            if query.text.lower() in doc.title.lower():
                scores[doc_id] *= BOOST_EXACT_MATCH

            # Litigation type boost
            if query.litigation_type and doc.litigation_type == query.litigation_type:
                scores[doc_id] *= BOOST_CASE_TYPE

            # Risk level boost
            if query.risk_level and doc.risk_level == query.risk_level:
                scores[doc_id] *= BOOST_RISK_LEVEL

            # Recent precedent boost
            if doc.year and doc.year >= 2015:
                scores[doc_id] *= BOOST_RECENT_PRECEDENT

            # Apply filters
            if query.scope != SearchScope.ALL and doc.doc_type != query.scope.value:
                scores[doc_id] = 0.0
            if query.litigation_type and doc.litigation_type and doc.litigation_type != query.litigation_type:
                scores[doc_id] *= 0.5
            if query.jurisdiction and doc.jurisdiction and doc.jurisdiction != query.jurisdiction:
                scores[doc_id] *= 0.7
            if query.min_year and doc.year and doc.year < query.min_year:
                scores[doc_id] = 0.0
            if query.max_year and doc.year and doc.year > query.max_year:
                scores[doc_id] = 0.0
            if query.court and doc.court and query.court.lower() not in doc.court.lower():
                scores[doc_id] *= 0.6

        # Filter and sort
        filtered = [(doc_id, score) for doc_id, score in scores.items() if score >= MIN_RELEVANCE_SCORE]

        if query.sort_by == SortOrder.RELEVANCE:
            filtered.sort(key=lambda x: x[1], reverse=True)
        elif query.sort_by == SortOrder.DATE:
            filtered.sort(
                key=lambda x: (self._documents[x[0]].year or 0, x[1]),
                reverse=True,
            )
        elif query.sort_by == SortOrder.RISK:
            risk_order = {"critical": 4, "high": 3, "medium": 2, "low": 1, "negligible": 0}
            filtered.sort(
                key=lambda x: (
                    risk_order.get(self._documents[x[0]].risk_level or "", 0),
                    x[1],
                ),
                reverse=True,
            )

        results: List[SearchResult] = []
        for doc_id, score in filtered[:query.max_results]:
            doc = self._documents[doc_id]
            snippet = extract_snippet(doc.content, query_tokens)
            results.append(SearchResult(
                doc_id=doc.doc_id,
                doc_type=doc.doc_type,
                title=doc.title,
                snippet=snippet,
                relevance_score=round(score, 4),
                litigation_type=doc.litigation_type,
                jurisdiction=doc.jurisdiction,
                risk_level=doc.risk_level,
                year=doc.year,
                citation=doc.citation,
                court=doc.court,
                match_terms=match_terms.get(doc_id, []),
                metadata=doc.metadata,
            ))

        elapsed = (time.time() - start) * 1000
        logger.debug(f"Search completed in {elapsed:.1f}ms | results={len(results)} | query={query.text[:80]}")
        return results

    @property
    def document_count(self) -> int:
        return self._total_docs

    @property
    def term_count(self) -> int:
        return len(self._index)

    def get_document(self, doc_id: str) -> Optional[SearchDocument]:
        return self._documents.get(doc_id)

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_documents": self._total_docs,
            "total_terms": len(self._index),
            "avg_doc_length": round(self._avg_doc_length, 1),
        }


# ============================================================================
# CASE COMPARISON
# ============================================================================

def compare_cases(
    index: InvertedIndex, doc_a_id: str, doc_b_id: str
) -> Optional[ComparisonResult]:
    """Compare two cases for similarity and differences."""
    doc_a = index.get_document(doc_a_id)
    doc_b = index.get_document(doc_b_id)
    if not doc_a or not doc_b:
        return None

    tokens_a = set(tokenize(doc_a.text_for_index))
    tokens_b = set(tokenize(doc_b.text_for_index))

    common = tokens_a & tokens_b
    only_a = tokens_a - tokens_b
    only_b = tokens_b - tokens_a

    union = tokens_a | tokens_b
    similarity = len(common) / len(union) if union else 0.0

    risk_order = {"critical": 4, "high": 3, "medium": 2, "low": 1, "negligible": 0}
    risk_a = risk_order.get(doc_a.risk_level or "medium", 2)
    risk_b = risk_order.get(doc_b.risk_level or "medium", 2)
    risk_diff = risk_a - risk_b

    if similarity > 0.7:
        recommendation = "Cases are highly similar; consider consolidating analysis"
    elif similarity > 0.4:
        recommendation = "Cases share moderate overlap; cross-reference key distinctions"
    else:
        recommendation = "Cases are largely distinct; analyze independently"

    return ComparisonResult(
        doc_a_id=doc_a_id,
        doc_b_id=doc_b_id,
        similarity_score=round(similarity, 4),
        common_terms=sorted(common)[:50],
        unique_to_a=sorted(only_a)[:30],
        unique_to_b=sorted(only_b)[:30],
        risk_differential=float(risk_diff),
        recommendation=recommendation,
    )


def detect_boilerplate(content: str, threshold: float = 0.6) -> bool:
    """Detect if content is boilerplate legal language."""
    boilerplate_phrases = [
        "to the fullest extent permitted by law",
        "notwithstanding anything to the contrary",
        "in no event shall",
        "without limitation",
        "shall be governed by and construed in accordance with",
        "hereby waives any and all claims",
        "to the maximum extent permitted",
        "in witness whereof",
        "the foregoing notwithstanding",
    ]
    content_lower = content.lower()
    matches = sum(1 for phrase in boilerplate_phrases if phrase in content_lower)
    ratio = matches / len(boilerplate_phrases) if boilerplate_phrases else 0
    return ratio >= threshold


def compute_customization_score(content: str) -> float:
    """Score how customized (vs. boilerplate) a legal document is."""
    tokens = tokenize(content)
    if not tokens:
        return 0.0

    unique_tokens = set(tokens)
    vocabulary_richness = len(unique_tokens) / len(tokens) if tokens else 0

    specific_indicators = [
        r"\b\d{1,2}/\d{1,2}/\d{4}\b",
        r"\$[\d,]+(?:\.\d{2})?",
        r"\b[A-Z][a-z]+\s(?:Corp|Inc|LLC|Ltd)\b",
        r"\bSection\s\d+\.\d+",
    ]

    specificity_count = 0
    for pattern in specific_indicators:
        specificity_count += len(re.findall(pattern, content))

    specificity_score = min(specificity_count / 10.0, 1.0)
    boilerplate_penalty = 0.3 if detect_boilerplate(content) else 0.0

    score = (vocabulary_richness * 0.4 + specificity_score * 0.6) - boilerplate_penalty
    return round(max(0.0, min(1.0, score)), 3)


# ============================================================================
# SINGLETON INDEX
# ============================================================================

_SEARCH_INDEX: Optional[InvertedIndex] = None


def get_search_index() -> InvertedIndex:
    """Get or create the singleton search index."""
    global _SEARCH_INDEX
    if _SEARCH_INDEX is None:
        _SEARCH_INDEX = InvertedIndex()
        _seed_index(_SEARCH_INDEX)
    return _SEARCH_INDEX


def _seed_index(index: InvertedIndex) -> None:
    """Seed the index with foundational case law from doctrine precedents."""
    from doctrines import DOCTRINE_CACHE

    for key, block in DOCTRINE_CACHE.items():
        # Index each doctrine as a document
        index.add_document(SearchDocument(
            doc_id=f"doctrine_{key}",
            doc_type="doctrines",
            title=block.topic,
            content=block.conclusion_template,
            litigation_type=block.category.value,
            risk_level=block.risk_severity.value,
            tags=block.keywords,
        ))

        # Index each precedent as a case document
        for prec in block.precedents:
            index.add_document(SearchDocument(
                doc_id=f"case_{prec.citation.replace(' ', '_').replace('.', '')}",
                doc_type="cases",
                title=prec.case_name,
                content=prec.holding,
                litigation_type=block.category.value,
                year=prec.year,
                citation=prec.citation,
                court=prec.court,
                risk_level=block.risk_severity.value,
                tags=[key],
            ))

    logger.info(f"Search index seeded | docs={index.document_count} | terms={index.term_count}")
