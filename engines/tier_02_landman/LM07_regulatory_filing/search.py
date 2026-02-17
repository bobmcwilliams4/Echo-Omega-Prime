"""
LM07 Regulatory Filing Engine - Vector Search Module
=====================================================
Semantic retrieval fallback when doctrine cache misses.
Uses cosine similarity on TF-IDF vectors for regulatory filing domain.
"""

from __future__ import annotations

import hashlib
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any, Optional

from loguru import logger


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MAX_RESULTS = 10
MIN_SCORE_THRESHOLD = 0.15
IDF_SMOOTHING = 1.0


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------
@dataclass
class SearchDocument:
    """A document in the search index."""
    doc_id: str
    title: str
    content: str
    domain: str = ""
    jurisdiction: str = ""
    form_types: list[str] = field(default_factory=list)
    rules: list[str] = field(default_factory=list)
    authority: str = ""
    weight: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)
    term_frequencies: dict[str, float] = field(default_factory=dict)
    magnitude: float = 0.0


@dataclass
class SearchResult:
    """A search result with relevance scoring."""
    doc_id: str
    title: str
    score: float
    content_snippet: str
    domain: str
    jurisdiction: str
    form_types: list[str]
    rules: list[str]
    authority: str
    metadata: dict[str, Any]


# ---------------------------------------------------------------------------
# Text processing
# ---------------------------------------------------------------------------
STOP_WORDS = frozenset({
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "to", "of", "in", "for",
    "on", "with", "at", "by", "from", "as", "into", "through", "during",
    "before", "after", "above", "below", "between", "under", "about",
    "and", "but", "or", "nor", "not", "so", "yet", "both", "either",
    "neither", "each", "every", "all", "any", "few", "more", "most",
    "other", "some", "such", "no", "only", "own", "same", "than", "too",
    "very", "just", "because", "if", "when", "what", "how", "which", "who",
    "this", "that", "these", "those",
})


def tokenize(text: str) -> list[str]:
    """Tokenize text into normalized terms."""
    text = text.lower()
    text = re.sub(r"[^\w\s\-]", " ", text)
    tokens = text.split()
    return [t for t in tokens if t not in STOP_WORDS and len(t) > 1]


def compute_tf(tokens: list[str]) -> dict[str, float]:
    """Compute term frequency with augmented normalization."""
    counts = Counter(tokens)
    if not counts:
        return {}
    max_count = max(counts.values())
    return {term: 0.5 + 0.5 * (count / max_count) for term, count in counts.items()}


def snippet(content: str, query_terms: list[str], max_len: int = 300) -> str:
    """Extract the most relevant snippet from content."""
    sentences = re.split(r"[.!?]\s+", content)
    if not sentences:
        return content[:max_len]

    best_score = -1
    best_sentence = sentences[0]
    for sentence in sentences:
        lower_sentence = sentence.lower()
        score = sum(1 for t in query_terms if t in lower_sentence)
        if score > best_score:
            best_score = score
            best_sentence = sentence

    if len(best_sentence) > max_len:
        return best_sentence[:max_len] + "..."
    return best_sentence


# ---------------------------------------------------------------------------
# Vector Search Engine
# ---------------------------------------------------------------------------
class VectorSearchEngine:
    """TF-IDF based vector search for regulatory filing doctrine retrieval."""

    def __init__(self) -> None:
        self._documents: dict[str, SearchDocument] = {}
        self._idf: dict[str, float] = {}
        self._doc_count: int = 0
        self._term_doc_counts: dict[str, int] = defaultdict(int)
        self._indexed: bool = False
        logger.info("LM07 VectorSearchEngine initialized")

    @property
    def document_count(self) -> int:
        return self._doc_count

    @property
    def vocabulary_size(self) -> int:
        return len(self._idf)

    def add_document(self, doc: SearchDocument) -> None:
        """Add a document to the index."""
        tokens = tokenize(doc.content + " " + doc.title)
        doc.term_frequencies = compute_tf(tokens)
        unique_terms = set(tokens)
        for term in unique_terms:
            self._term_doc_counts[term] += 1
        self._documents[doc.doc_id] = doc
        self._doc_count += 1
        self._indexed = False

    def add_documents(self, docs: list[SearchDocument]) -> None:
        """Add multiple documents."""
        for doc in docs:
            self.add_document(doc)

    def build_index(self) -> None:
        """Compute IDF values and document magnitudes."""
        if self._doc_count == 0:
            logger.warning("No documents to index")
            return

        # Compute IDF
        self._idf = {}
        for term, doc_count in self._term_doc_counts.items():
            self._idf[term] = math.log(
                (self._doc_count + IDF_SMOOTHING) / (doc_count + IDF_SMOOTHING)
            ) + IDF_SMOOTHING

        # Compute document magnitudes
        for doc in self._documents.values():
            magnitude_sq = 0.0
            for term, tf in doc.term_frequencies.items():
                idf = self._idf.get(term, 0.0)
                tfidf = tf * idf
                magnitude_sq += tfidf * tfidf
            doc.magnitude = math.sqrt(magnitude_sq) if magnitude_sq > 0 else 1.0

        self._indexed = True
        logger.info(
            "LM07 search index built | docs={} | vocab={} | terms={}",
            self._doc_count, len(self._idf), sum(self._term_doc_counts.values()),
        )

    def search(
        self,
        query: str,
        max_results: int = MAX_RESULTS,
        min_score: float = MIN_SCORE_THRESHOLD,
        jurisdiction_filter: Optional[str] = None,
        form_type_filter: Optional[str] = None,
        domain_filter: Optional[str] = None,
    ) -> list[SearchResult]:
        """Search for documents matching query."""
        if not self._indexed:
            self.build_index()

        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        query_tf = compute_tf(query_tokens)
        query_vector: dict[str, float] = {}
        query_magnitude_sq = 0.0

        for term, tf in query_tf.items():
            idf = self._idf.get(term, 0.0)
            tfidf = tf * idf
            query_vector[term] = tfidf
            query_magnitude_sq += tfidf * tfidf

        query_magnitude = math.sqrt(query_magnitude_sq) if query_magnitude_sq > 0 else 1.0

        results: list[SearchResult] = []
        for doc in self._documents.values():
            # Apply filters
            if jurisdiction_filter and doc.jurisdiction != jurisdiction_filter:
                continue
            if form_type_filter and form_type_filter not in doc.form_types:
                continue
            if domain_filter and doc.domain != domain_filter:
                continue

            # Cosine similarity
            dot_product = 0.0
            for term, q_tfidf in query_vector.items():
                d_tf = doc.term_frequencies.get(term, 0.0)
                d_idf = self._idf.get(term, 0.0)
                d_tfidf = d_tf * d_idf
                dot_product += q_tfidf * d_tfidf

            similarity = dot_product / (query_magnitude * doc.magnitude)
            weighted_score = similarity * doc.weight

            if weighted_score >= min_score:
                results.append(SearchResult(
                    doc_id=doc.doc_id,
                    title=doc.title,
                    score=round(weighted_score, 4),
                    content_snippet=snippet(doc.content, query_tokens),
                    domain=doc.domain,
                    jurisdiction=doc.jurisdiction,
                    form_types=doc.form_types,
                    rules=doc.rules,
                    authority=doc.authority,
                    metadata=doc.metadata,
                ))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:max_results]

    def get_document(self, doc_id: str) -> Optional[SearchDocument]:
        return self._documents.get(doc_id)

    def get_stats(self) -> dict[str, Any]:
        return {
            "document_count": self._doc_count,
            "vocabulary_size": len(self._idf),
            "indexed": self._indexed,
            "jurisdictions": list(set(d.jurisdiction for d in self._documents.values() if d.jurisdiction)),
            "domains": list(set(d.domain for d in self._documents.values() if d.domain)),
            "form_types": list(set(ft for d in self._documents.values() for ft in d.form_types)),
        }

    def compute_result_hash(self, query: str, results: list[SearchResult]) -> str:
        """Compute determinism hash over search results."""
        payload = query + "|" + "|".join(
            f"{r.doc_id}:{r.score}" for r in results
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
