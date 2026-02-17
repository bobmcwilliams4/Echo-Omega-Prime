"""
LM09 Runsheet Generator — Vector Search Module
Engine ID: LM09 | Port: 8509
Semantic retrieval fallback for run sheet generation queries
when doctrine cache misses occur.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import threading
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from loguru import logger


@dataclass
class SearchDocument:
    """A searchable document in the vector store."""
    doc_id: str
    title: str
    content: str
    category: str
    keywords: list[str]
    authority_weight: float = 0.5
    term_frequencies: dict[str, float] = field(default_factory=dict)
    norm: float = 0.0

    def compute_tf(self) -> None:
        """Compute term frequency vector for the document."""
        words = _tokenize(self.content + " " + self.title + " " + " ".join(self.keywords))
        freq: dict[str, int] = defaultdict(int)
        for w in words:
            freq[w] += 1
        total = len(words) if words else 1
        self.term_frequencies = {w: c / total for w, c in freq.items()}
        self.norm = math.sqrt(sum(v * v for v in self.term_frequencies.values()))


@dataclass
class SearchResult:
    """A single search result with relevance scoring."""
    doc_id: str
    title: str
    content_snippet: str
    category: str
    relevance_score: float
    authority_weight: float
    combined_score: float
    matched_keywords: list[str]


def _tokenize(text: str) -> list[str]:
    """Tokenize text into lowercase alphanumeric words."""
    return re.findall(r"[a-z0-9]+", text.lower())


def _compute_idf(documents: list[SearchDocument]) -> dict[str, float]:
    """Compute inverse document frequency for all terms."""
    n = len(documents)
    if n == 0:
        return {}
    doc_freq: dict[str, int] = defaultdict(int)
    for doc in documents:
        seen = set()
        for term in doc.term_frequencies:
            if term not in seen:
                doc_freq[term] += 1
                seen.add(term)
    return {term: math.log((n + 1) / (df + 1)) + 1.0 for term, df in doc_freq.items()}


class RunsheetVectorSearch:
    """TF-IDF-based semantic search for run sheet domain knowledge."""

    def __init__(self, index_path: Optional[Path] = None) -> None:
        self.index_path = index_path or Path("vectors/lm09_runsheet.db")
        self._lock = threading.RLock()  # RLock: get_index_stats() calls get_category_stats() under lock
        self._documents: list[SearchDocument] = []
        self._doc_index: dict[str, SearchDocument] = {}
        self._idf: dict[str, float] = {}
        self._category_index: dict[str, list[str]] = defaultdict(list)
        self._loaded = False
        logger.info("RunsheetVectorSearch initialized, index_path={}", self.index_path)

    def add_document(self, doc: SearchDocument) -> None:
        """Add a document to the search index."""
        doc.compute_tf()
        with self._lock:
            self._documents.append(doc)
            self._doc_index[doc.doc_id] = doc
            self._category_index[doc.category].append(doc.doc_id)
            self._idf = _compute_idf(self._documents)

    def add_documents(self, docs: list[SearchDocument]) -> None:
        """Bulk add documents and recompute IDF."""
        for doc in docs:
            doc.compute_tf()
        with self._lock:
            self._documents.extend(docs)
            for doc in docs:
                self._doc_index[doc.doc_id] = doc
                self._category_index[doc.category].append(doc.doc_id)
            self._idf = _compute_idf(self._documents)
        logger.info("Added {} documents, total={}", len(docs), len(self._documents))

    def search(
        self,
        query: str,
        top_k: int = 10,
        category_filter: Optional[str] = None,
        min_score: float = 0.01,
    ) -> list[SearchResult]:
        """Search for documents matching the query."""
        query_tokens = _tokenize(query)
        if not query_tokens:
            return []
        query_tf: dict[str, float] = defaultdict(float)
        for t in query_tokens:
            query_tf[t] += 1
        total_q = len(query_tokens)
        query_tf = {t: c / total_q for t, c in query_tf.items()}
        with self._lock:
            candidates = self._documents
            if category_filter:
                doc_ids = self._category_index.get(category_filter, [])
                candidates = [self._doc_index[did] for did in doc_ids if did in self._doc_index]
            results: list[SearchResult] = []
            for doc in candidates:
                score = self._cosine_similarity(query_tf, doc.term_frequencies, doc.norm)
                if score < min_score:
                    continue
                keyword_matches = [kw for kw in doc.keywords if kw.lower() in query.lower()]
                keyword_boost = len(keyword_matches) * 0.05
                combined = (score * 0.7) + (doc.authority_weight * 0.2) + (keyword_boost * 0.1)
                snippet = doc.content[:300] + "..." if len(doc.content) > 300 else doc.content
                results.append(SearchResult(
                    doc_id=doc.doc_id,
                    title=doc.title,
                    content_snippet=snippet,
                    category=doc.category,
                    relevance_score=round(score, 6),
                    authority_weight=doc.authority_weight,
                    combined_score=round(combined, 6),
                    matched_keywords=keyword_matches,
                ))
            results.sort(key=lambda r: r.combined_score, reverse=True)
            return results[:top_k]

    def _cosine_similarity(
        self,
        query_tf: dict[str, float],
        doc_tf: dict[str, float],
        doc_norm: float,
    ) -> float:
        """Compute TF-IDF weighted cosine similarity."""
        if doc_norm == 0:
            return 0.0
        dot_product = 0.0
        query_norm_sq = 0.0
        for term, qtf in query_tf.items():
            idf = self._idf.get(term, 1.0)
            q_weight = qtf * idf
            d_weight = doc_tf.get(term, 0.0) * idf
            dot_product += q_weight * d_weight
            query_norm_sq += q_weight * q_weight
        query_norm = math.sqrt(query_norm_sq) if query_norm_sq > 0 else 1.0
        doc_idf_norm = 0.0
        for term, dtf in doc_tf.items():
            idf = self._idf.get(term, 1.0)
            doc_idf_norm += (dtf * idf) ** 2
        doc_idf_norm = math.sqrt(doc_idf_norm) if doc_idf_norm > 0 else 1.0
        return dot_product / (query_norm * doc_idf_norm)

    def get_document(self, doc_id: str) -> Optional[SearchDocument]:
        """Retrieve a specific document by ID."""
        with self._lock:
            return self._doc_index.get(doc_id)

    def get_category_stats(self) -> dict[str, int]:
        """Return document count per category."""
        with self._lock:
            return {cat: len(ids) for cat, ids in self._category_index.items()}

    def get_index_stats(self) -> dict[str, Any]:
        """Return overall index statistics."""
        with self._lock:
            return {
                "total_documents": len(self._documents),
                "total_terms": len(self._idf),
                "categories": self.get_category_stats(),
                "index_path": str(self.index_path),
            }

    def save_index(self) -> None:
        """Persist the index to disk."""
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        with self._lock:
            data = {
                "documents": [
                    {
                        "doc_id": d.doc_id,
                        "title": d.title,
                        "content": d.content,
                        "category": d.category,
                        "keywords": d.keywords,
                        "authority_weight": d.authority_weight,
                    }
                    for d in self._documents
                ],
            }
        with self.index_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logger.info("Index saved to {} ({} documents)", self.index_path, len(self._documents))

    def load_index(self) -> bool:
        """Load the index from disk."""
        if not self.index_path.exists():
            logger.warning("Index file not found: {}", self.index_path)
            return False
        try:
            with self.index_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            docs = [
                SearchDocument(
                    doc_id=d["doc_id"],
                    title=d["title"],
                    content=d["content"],
                    category=d["category"],
                    keywords=d["keywords"],
                    authority_weight=d.get("authority_weight", 0.5),
                )
                for d in data.get("documents", [])
            ]
            self.add_documents(docs)
            self._loaded = True
            logger.info("Index loaded from {} ({} documents)", self.index_path, len(docs))
            return True
        except (json.JSONDecodeError, KeyError, OSError) as exc:
            logger.error("Failed to load index: {}", exc)
            return False
