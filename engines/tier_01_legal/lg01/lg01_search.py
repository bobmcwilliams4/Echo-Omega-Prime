"""
Contract Analysis Engine - TF-IDF Search Index
Inverted index built from doctrine blocks for fast similarity retrieval.

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
Engine: LG01 - Contract Analysis Engine
Version: 1.0.0
"""

from __future__ import annotations
import math
import re
import time
import hashlib
from collections import Counter, defaultdict
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Set, Tuple
from loguru import logger

# Search result dataclass
@dataclass
class SearchResult:
    """A single search result with score and metadata."""
    doctrine_key: str
    topic: str
    score: float
    matched_terms: List[str]
    snippet: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


@dataclass
class SearchStats:
    """Statistics about the search index."""
    total_documents: int = 0
    total_terms: int = 0
    avg_doc_length: float = 0.0
    index_build_time_ms: float = 0.0
    last_query_time_ms: float = 0.0
    total_queries: int = 0
    total_misses: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


# Stop words for contract law domain
STOP_WORDS: Set[str] = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "must", "need",
    "and", "or", "but", "not", "no", "nor", "so", "yet", "both",
    "in", "on", "at", "to", "for", "of", "with", "by", "from",
    "up", "about", "into", "through", "during", "before", "after",
    "above", "below", "between", "under", "over",
    "this", "that", "these", "those", "it", "its", "they", "them",
    "he", "she", "we", "you", "i", "me", "my", "your", "his", "her",
    "if", "then", "than", "when", "where", "how", "what", "which", "who",
    "all", "each", "every", "any", "some", "most", "more", "other",
    "also", "just", "only", "very", "much", "such", "own",
}

# Domain-specific terms that should NOT be filtered even if common
DOMAIN_TERMS: Set[str] = {
    "contract", "clause", "breach", "consideration", "offer", "acceptance",
    "intent", "capacity", "damages", "remedy", "unconscionable", "equity",
    "parol", "statute", "frauds", "performance", "condition", "warranty",
    "covenant", "estoppel", "rescission", "reformation", "restitution",
    "specific", "assignment", "delegation", "novation", "discharge",
}


class ContractSearchIndex:
    """
    TF-IDF inverted index for contract doctrine search.

    Architecture:
    - Tokenize doctrine blocks (topic + quick_answer + full_doctrine)
    - Build inverted index mapping terms to document lists with TF
    - Compute IDF at query time
    - Score using BM25 variant for better performance
    - Return top-k results above threshold

    BM25 Formula:
    score(D,Q) = Σ IDF(qi) * (f(qi,D) * (k1 + 1)) / (f(qi,D) + k1 * (1 - b + b * |D| / avgdl))

    where:
    - f(qi,D) = term frequency of qi in document D
    - |D| = length of document D in words
    - avgdl = average document length in the collection
    - k1 = 1.5 (term frequency saturation parameter)
    - b = 0.75 (length normalization parameter)
    - IDF(qi) = log((N - n(qi) + 0.5) / (n(qi) + 0.5))
    - N = total number of documents
    - n(qi) = number of documents containing qi
    """

    def __init__(self):
        self._inverted_index: Dict[str, Dict[str, float]] = defaultdict(dict)  # term -> {doc_key: tf}
        self._doc_lengths: Dict[str, int] = {}  # doc_key -> total terms
        self._doc_topics: Dict[str, str] = {}  # doc_key -> topic name
        self._doc_snippets: Dict[str, str] = {}  # doc_key -> quick_answer
        self._doc_full_text: Dict[str, str] = {}  # doc_key -> full text for snippet extraction
        self._total_docs: int = 0
        self._avg_doc_length: float = 0.0
        self._stats = SearchStats()
        self._miss_log: List[Dict[str, Any]] = []  # Track misses for gap identification
        self._built = False
        logger.info("ContractSearchIndex initialized")

    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into normalized terms, removing stop words.

        Process:
        1. Lowercase
        2. Extract alphanumeric sequences
        3. Filter stop words (except domain terms)
        4. Filter single-character tokens
        5. Return list of terms
        """
        if not text:
            return []

        # Lowercase and extract words
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)

        # Filter stop words but preserve domain terms
        filtered = [
            token for token in tokens
            if len(token) > 1 and (token in DOMAIN_TERMS or token not in STOP_WORDS)
        ]

        return filtered

    def build_index(self, doctrine_cache: Dict[str, Any]) -> None:
        """
        Build inverted index from doctrine cache.

        Args:
            doctrine_cache: Dict mapping doctrine keys to doctrine objects
                           Each object must have: topic, quick_answer, full_doctrine
        """
        start_time = time.perf_counter()
        logger.info(f"Building search index from {len(doctrine_cache)} doctrine blocks")

        self._inverted_index.clear()
        self._doc_lengths.clear()
        self._doc_topics.clear()
        self._doc_snippets.clear()
        self._doc_full_text.clear()
        self._total_docs = 0
        self._avg_doc_length = 0.0

        total_length = 0

        for doc_key, doctrine in doctrine_cache.items():
            # Extract text fields
            topic = getattr(doctrine, 'topic', '')
            quick_answer = getattr(doctrine, 'quick_answer', '')
            full_doctrine = getattr(doctrine, 'full_doctrine', '')

            # Combine all text (weight topic higher by repeating 3x)
            combined_text = f"{topic} {topic} {topic} {quick_answer} {full_doctrine}"

            # Tokenize
            tokens = self._tokenize(combined_text)

            if not tokens:
                logger.warning(f"No tokens extracted from doctrine {doc_key}")
                continue

            # Count term frequencies
            term_counts = Counter(tokens)

            # Store in inverted index
            for term, count in term_counts.items():
                self._inverted_index[term][doc_key] = float(count)

            # Store document metadata
            self._doc_lengths[doc_key] = len(tokens)
            self._doc_topics[doc_key] = topic
            self._doc_snippets[doc_key] = quick_answer[:200]  # First 200 chars
            self._doc_full_text[doc_key] = combined_text

            total_length += len(tokens)
            self._total_docs += 1

        # Compute average document length
        if self._total_docs > 0:
            self._avg_doc_length = total_length / self._total_docs

        # Update stats
        self._stats.total_documents = self._total_docs
        self._stats.total_terms = len(self._inverted_index)
        self._stats.avg_doc_length = self._avg_doc_length
        self._stats.index_build_time_ms = (time.perf_counter() - start_time) * 1000

        self._built = True

        logger.success(
            f"Search index built: {self._total_docs} docs, "
            f"{self._stats.total_terms} unique terms, "
            f"avg doc length {self._avg_doc_length:.1f}, "
            f"time {self._stats.index_build_time_ms:.2f}ms"
        )

    def search_similar(
        self,
        query: str,
        k: int = 5,
        threshold: float = 0.3
    ) -> List[SearchResult]:
        """
        Search for similar doctrine blocks using BM25 scoring.

        Args:
            query: Search query string
            k: Number of results to return
            threshold: Minimum score threshold (0.0 - 1.0)

        Returns:
            List of SearchResult objects sorted by score descending
        """
        start_time = time.perf_counter()

        if not self._built:
            logger.warning("Search index not built, returning empty results")
            return []

        if not query or not query.strip():
            logger.warning("Empty query provided")
            return []

        # Tokenize query
        query_terms = self._tokenize(query)

        if not query_terms:
            logger.warning(f"No valid terms in query: {query}")
            self._stats.total_misses += 1
            self._miss_log.append({
                "query": query,
                "timestamp": time.time(),
                "reason": "no_valid_terms",
            })
            return []

        logger.debug(f"Query terms: {query_terms}")

        # Score all documents that contain at least one query term
        candidate_docs: Set[str] = set()
        for term in query_terms:
            if term in self._inverted_index:
                candidate_docs.update(self._inverted_index[term].keys())

        if not candidate_docs:
            logger.info(f"No documents match query: {query}")
            self._stats.total_misses += 1
            self._miss_log.append({
                "query": query,
                "timestamp": time.time(),
                "reason": "no_matching_docs",
                "query_terms": query_terms,
            })
            return []

        logger.debug(f"Found {len(candidate_docs)} candidate documents")

        # Score each candidate document
        scored_docs: List[Tuple[str, float, List[str]]] = []

        for doc_key in candidate_docs:
            score, matched_terms = self._compute_bm25_score(query_terms, doc_key)

            if score >= threshold:
                scored_docs.append((doc_key, score, matched_terms))

        # Sort by score descending
        scored_docs.sort(key=lambda x: x[1], reverse=True)

        # Take top k
        top_docs = scored_docs[:k]

        # Build results
        results: List[SearchResult] = []
        for doc_key, score, matched_terms in top_docs:
            # Extract snippet around matched terms
            snippet = self._extract_snippet(doc_key, matched_terms)

            results.append(SearchResult(
                doctrine_key=doc_key,
                topic=self._doc_topics.get(doc_key, "Unknown"),
                score=score,
                matched_terms=matched_terms,
                snippet=snippet,
            ))

        # Update stats
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        self._stats.last_query_time_ms = elapsed_ms
        self._stats.total_queries += 1

        if not results:
            self._stats.total_misses += 1
            self._miss_log.append({
                "query": query,
                "timestamp": time.time(),
                "reason": "below_threshold",
                "query_terms": query_terms,
                "max_score": scored_docs[0][1] if scored_docs else 0.0,
            })

        logger.info(
            f"Search completed: {len(results)} results for '{query}' "
            f"in {elapsed_ms:.2f}ms"
        )

        return results

    def _compute_bm25_score(
        self,
        query_terms: List[str],
        doc_key: str
    ) -> Tuple[float, List[str]]:
        """
        Compute BM25 score for a document given query terms.

        BM25 parameters:
        - k1 = 1.5 (term frequency saturation)
        - b = 0.75 (length normalization)

        Args:
            query_terms: List of tokenized query terms
            doc_key: Document key to score

        Returns:
            Tuple of (score, matched_terms)
        """
        k1 = 1.5
        b = 0.75

        score = 0.0
        matched_terms: List[str] = []

        doc_length = self._doc_lengths.get(doc_key, 0)

        if doc_length == 0:
            return 0.0, []

        # Compute length normalization factor
        length_norm = 1 - b + b * (doc_length / self._avg_doc_length)

        for term in query_terms:
            # Get term frequency in document
            if term not in self._inverted_index:
                continue

            if doc_key not in self._inverted_index[term]:
                continue

            matched_terms.append(term)

            tf = self._inverted_index[term][doc_key]

            # Compute IDF
            # IDF = log((N - n + 0.5) / (n + 0.5))
            n = len(self._inverted_index[term])  # num docs containing term
            idf = math.log((self._total_docs - n + 0.5) / (n + 0.5) + 1.0)

            # BM25 component for this term
            # (tf * (k1 + 1)) / (tf + k1 * length_norm)
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * length_norm

            term_score = idf * (numerator / denominator)
            score += term_score

        # Normalize score to 0-1 range based on query length
        # Max possible score is if all terms appear with high frequency
        if len(query_terms) > 0:
            score = score / (len(query_terms) * 5.0)  # Empirical normalization
            score = min(1.0, max(0.0, score))  # Clamp to [0, 1]

        return score, matched_terms

    def _extract_snippet(self, doc_key: str, matched_terms: List[str]) -> str:
        """
        Extract a snippet from the document around matched terms.

        Args:
            doc_key: Document key
            matched_terms: List of matched query terms

        Returns:
            Snippet string (up to 200 chars)
        """
        # First try quick_answer
        snippet = self._doc_snippets.get(doc_key, "")

        if snippet:
            return snippet

        # Otherwise extract from full text around first matched term
        full_text = self._doc_full_text.get(doc_key, "")

        if not full_text or not matched_terms:
            return ""

        # Find first occurrence of any matched term
        full_text_lower = full_text.lower()
        min_pos = len(full_text)

        for term in matched_terms:
            pos = full_text_lower.find(term)
            if pos != -1 and pos < min_pos:
                min_pos = pos

        if min_pos == len(full_text):
            # No match found, return beginning
            return full_text[:200]

        # Extract window around match
        start = max(0, min_pos - 50)
        end = min(len(full_text), min_pos + 150)

        snippet = full_text[start:end]

        # Clean up
        if start > 0:
            snippet = "..." + snippet
        if end < len(full_text):
            snippet = snippet + "..."

        return snippet

    def get_stats(self) -> Dict[str, Any]:
        """
        Return search index statistics.

        Returns:
            Dictionary containing index stats
        """
        return {
            "total_documents": self._stats.total_documents,
            "total_terms": self._stats.total_terms,
            "avg_doc_length": round(self._stats.avg_doc_length, 2),
            "index_build_time_ms": round(self._stats.index_build_time_ms, 2),
            "last_query_time_ms": round(self._stats.last_query_time_ms, 2),
            "total_queries": self._stats.total_queries,
            "total_misses": self._stats.total_misses,
            "miss_rate": round(
                self._stats.total_misses / self._stats.total_queries * 100, 2
            ) if self._stats.total_queries > 0 else 0.0,
            "built": self._built,
        }

    def get_miss_log(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Return recent search misses for doctrine gap identification.

        Args:
            limit: Maximum number of misses to return

        Returns:
            List of miss log entries (most recent first)
        """
        return self._miss_log[-limit:][::-1]  # Last N, reversed

    def clear_miss_log(self) -> None:
        """Clear the miss log."""
        self._miss_log.clear()
        logger.info("Miss log cleared")

    def get_term_stats(self, term: str) -> Dict[str, Any]:
        """
        Get statistics about a specific term.

        Args:
            term: Term to analyze

        Returns:
            Dictionary with term statistics
        """
        term_lower = term.lower()

        if term_lower not in self._inverted_index:
            return {
                "term": term,
                "found": False,
                "doc_count": 0,
                "total_occurrences": 0,
            }

        doc_tfs = self._inverted_index[term_lower]
        total_occurrences = sum(doc_tfs.values())

        # Compute IDF
        n = len(doc_tfs)
        idf = math.log((self._total_docs - n + 0.5) / (n + 0.5) + 1.0)

        return {
            "term": term,
            "found": True,
            "doc_count": n,
            "total_occurrences": int(total_occurrences),
            "idf": round(idf, 4),
            "avg_tf": round(total_occurrences / n, 2),
        }


# Singleton instance
_index: Optional[ContractSearchIndex] = None


def get_search_index() -> ContractSearchIndex:
    """Get the singleton search index instance."""
    global _index
    if _index is None:
        _index = ContractSearchIndex()
        logger.debug("Created singleton ContractSearchIndex")
    return _index


def search_doctrines(query: str, k: int = 5) -> List[SearchResult]:
    """
    Convenience function to search doctrines.

    Args:
        query: Search query
        k: Number of results to return

    Returns:
        List of SearchResult objects
    """
    return get_search_index().search_similar(query, k=k)
