"""
LG04 Legal Document Draft Engine - Search Module
==================================================
Vector search, TF-IDF indexing, clause retrieval, template matching,
and document similarity scoring for the legal document drafting engine.

Provides:
    - TF-IDF inverted index over doctrine blocks and clause library
    - Clause retrieval by category, jurisdiction, and similarity
    - Template matching and scoring
    - Document similarity analysis
    - Query hashing for determinism

Engine ID: LG04
Version: 1.0.0
"""

from __future__ import annotations

import hashlib
import math
import re
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, FrozenSet, List, Optional, Set, Tuple

from loguru import logger
from pydantic import BaseModel, Field


# ============================================================================
# CONSTANTS
# ============================================================================

DEFAULT_TOP_K = 5
SCORE_THRESHOLD = 0.3
MAX_TOKEN_LENGTH = 50
MIN_TOKEN_LENGTH = 2

LEGAL_STOPWORDS: FrozenSet[str] = frozenset({
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "shall", "can", "must",
    "it", "its", "this", "that", "these", "those", "such", "any", "all",
    "each", "every", "some", "no", "not", "only", "than", "so", "very",
})


# ============================================================================
# ENUMS
# ============================================================================


class SearchMode(str, Enum):
    """Search mode for different retrieval strategies."""

    DOCTRINE = "doctrine"
    CLAUSE = "clause"
    TEMPLATE = "template"
    SIMILARITY = "similarity"
    HYBRID = "hybrid"


class ClauseType(str, Enum):
    """Standard clause types in the clause library."""

    DEFINITIONS = "definitions"
    REPRESENTATIONS = "representations_warranties"
    COVENANTS = "covenants"
    INDEMNIFICATION = "indemnification"
    LIMITATION_LIABILITY = "limitation_of_liability"
    CONFIDENTIALITY = "confidentiality"
    TERMINATION = "termination"
    DISPUTE_RESOLUTION = "dispute_resolution"
    GOVERNING_LAW = "governing_law"
    FORCE_MAJEURE = "force_majeure"
    ASSIGNMENT = "assignment"
    NOTICES = "notices"
    SEVERABILITY = "severability"
    ENTIRE_AGREEMENT = "entire_agreement"
    AMENDMENT = "amendment"
    WAIVER = "waiver"
    COUNTERPARTS = "counterparts"
    SURVIVAL = "survival"
    NON_COMPETE = "non_compete"
    NON_SOLICITATION = "non_solicitation"
    IP_RIGHTS = "intellectual_property"
    INSURANCE = "insurance"
    COMPLIANCE = "compliance"
    BOILERPLATE = "boilerplate"


# ============================================================================
# PYDANTIC MODELS
# ============================================================================


class SearchResult(BaseModel):
    """A single search result from the index."""

    doc_id: str
    title: str = ""
    content: str = ""
    score: float = 0.0
    category: str = ""
    jurisdiction: str = ""
    document_type: str = ""
    clause_type: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)
    matched_tokens: List[str] = Field(default_factory=list)


class SearchResponse(BaseModel):
    """Full search response with metadata."""

    query: str
    query_hash: str = ""
    mode: SearchMode = SearchMode.DOCTRINE
    results: List[SearchResult] = Field(default_factory=list)
    total_matches: int = 0
    search_time_ms: float = 0.0
    top_k: int = DEFAULT_TOP_K
    score_threshold: float = SCORE_THRESHOLD


class ClauseTemplate(BaseModel):
    """A clause template from the clause library."""

    clause_id: str
    clause_type: str
    title: str
    content: str
    jurisdiction: str = ""
    document_types: List[str] = Field(default_factory=list)
    variables: List[str] = Field(default_factory=list)
    version: int = 1
    last_updated: str = ""
    word_count: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TemplateMatchResult(BaseModel):
    """Result of matching a query against clause templates."""

    template: ClauseTemplate
    match_score: float = 0.0
    matched_on: List[str] = Field(default_factory=list)


class DocumentSimilarityResult(BaseModel):
    """Result of document similarity comparison."""

    doc_a_id: str
    doc_b_id: str
    cosine_similarity: float = 0.0
    jaccard_similarity: float = 0.0
    shared_clauses: List[str] = Field(default_factory=list)
    unique_to_a: List[str] = Field(default_factory=list)
    unique_to_b: List[str] = Field(default_factory=list)


# ============================================================================
# TOKENIZER
# ============================================================================


def _tokenize_for_search(text: str) -> List[str]:
    """Tokenize text for search indexing."""
    cleaned = re.sub(r"[^\w\s\-]", " ", text.lower())
    tokens = cleaned.split()
    result: List[str] = []
    for t in tokens:
        t = t.strip("-_ ")
        if (
            t
            and t not in LEGAL_STOPWORDS
            and MIN_TOKEN_LENGTH <= len(t) <= MAX_TOKEN_LENGTH
        ):
            result.append(t)
    return result


def _bigrams_for_search(tokens: List[str]) -> List[str]:
    """Generate bigrams from token list for search."""
    return [f"{tokens[i]}_{tokens[i + 1]}" for i in range(len(tokens) - 1)]


# ============================================================================
# TF-IDF INVERTED INDEX
# ============================================================================


@dataclass
class IndexDocument:
    """A document stored in the search index."""

    doc_id: str
    title: str = ""
    content: str = ""
    category: str = ""
    jurisdiction: str = ""
    document_type: str = ""
    clause_type: str = ""
    tokens: List[str] = field(default_factory=list)
    token_freqs: Dict[str, int] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class DoctrineSearchIndex:
    """
    TF-IDF inverted index for doctrine blocks and clause library.
    Supports multi-field search with category and jurisdiction filtering.
    """

    def __init__(self, top_k: int = DEFAULT_TOP_K, score_threshold: float = SCORE_THRESHOLD) -> None:
        self.top_k = top_k
        self.score_threshold = score_threshold

        self._documents: Dict[str, IndexDocument] = {}
        self._inverted_index: Dict[str, Set[str]] = defaultdict(set)
        self._doc_count = 0
        self._token_doc_freq: Dict[str, int] = defaultdict(int)
        self._avg_doc_length = 0.0
        self._total_tokens = 0

        self._clause_templates: Dict[str, ClauseTemplate] = {}
        self._clause_by_type: Dict[str, List[str]] = defaultdict(list)
        self._clause_by_jurisdiction: Dict[str, List[str]] = defaultdict(list)

    def add_document(
        self,
        doc_id: str,
        title: str,
        content: str,
        category: str = "",
        jurisdiction: str = "",
        document_type: str = "",
        clause_type: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a document to the search index."""
        full_text = f"{title} {content}"
        tokens = _tokenize_for_search(full_text)
        bigrams = _bigrams_for_search(tokens)
        all_tokens = tokens + bigrams

        token_freqs = Counter(all_tokens)

        doc = IndexDocument(
            doc_id=doc_id,
            title=title,
            content=content,
            category=category,
            jurisdiction=jurisdiction,
            document_type=document_type,
            clause_type=clause_type,
            tokens=all_tokens,
            token_freqs=dict(token_freqs),
            metadata=metadata or {},
        )

        self._documents[doc_id] = doc
        self._doc_count += 1
        self._total_tokens += len(all_tokens)
        self._avg_doc_length = self._total_tokens / self._doc_count

        unique_tokens_in_doc: Set[str] = set(all_tokens)
        for token in unique_tokens_in_doc:
            self._inverted_index[token].add(doc_id)
            self._token_doc_freq[token] += 1

    def add_clause_template(self, template: ClauseTemplate) -> None:
        """Add a clause template to the template library and index."""
        self._clause_templates[template.clause_id] = template
        self._clause_by_type[template.clause_type].append(template.clause_id)
        if template.jurisdiction:
            self._clause_by_jurisdiction[template.jurisdiction].append(template.clause_id)

        self.add_document(
            doc_id=template.clause_id,
            title=template.title,
            content=template.content,
            category="clause_template",
            jurisdiction=template.jurisdiction,
            document_type=",".join(template.document_types),
            clause_type=template.clause_type,
            metadata={"variables": template.variables, "version": template.version},
        )

    def search(
        self,
        query: str,
        top_k: Optional[int] = None,
        score_threshold: Optional[float] = None,
        category_filter: str = "",
        jurisdiction_filter: str = "",
        document_type_filter: str = "",
        clause_type_filter: str = "",
        mode: SearchMode = SearchMode.DOCTRINE,
    ) -> SearchResponse:
        """
        Search the index using TF-IDF scoring with optional filters.
        """
        start_time = time.time()
        k = top_k or self.top_k
        threshold = score_threshold or self.score_threshold

        query_tokens = _tokenize_for_search(query)
        query_bigrams = _bigrams_for_search(query_tokens)
        all_query_tokens = query_tokens + query_bigrams

        if not all_query_tokens:
            return SearchResponse(
                query=query,
                query_hash=compute_query_hash(query),
                mode=mode,
                search_time_ms=(time.time() - start_time) * 1000.0,
            )

        candidate_doc_ids: Set[str] = set()
        for token in all_query_tokens:
            if token in self._inverted_index:
                candidate_doc_ids.update(self._inverted_index[token])

        if category_filter:
            candidate_doc_ids = {
                did for did in candidate_doc_ids
                if self._documents[did].category == category_filter
            }
        if jurisdiction_filter:
            candidate_doc_ids = {
                did for did in candidate_doc_ids
                if self._documents[did].jurisdiction == jurisdiction_filter
                or not self._documents[did].jurisdiction
            }
        if document_type_filter:
            candidate_doc_ids = {
                did for did in candidate_doc_ids
                if document_type_filter in self._documents[did].document_type
            }
        if clause_type_filter:
            candidate_doc_ids = {
                did for did in candidate_doc_ids
                if self._documents[did].clause_type == clause_type_filter
            }

        scored_results: List[Tuple[str, float, List[str]]] = []
        for doc_id in candidate_doc_ids:
            doc = self._documents[doc_id]
            score, matched = self._compute_bm25_score(all_query_tokens, doc)
            if score >= threshold:
                scored_results.append((doc_id, score, matched))

        scored_results.sort(key=lambda x: x[1], reverse=True)
        top_results = scored_results[:k]

        results: List[SearchResult] = []
        for doc_id, score, matched in top_results:
            doc = self._documents[doc_id]
            results.append(SearchResult(
                doc_id=doc_id,
                title=doc.title,
                content=doc.content[:500],
                score=round(score, 4),
                category=doc.category,
                jurisdiction=doc.jurisdiction,
                document_type=doc.document_type,
                clause_type=doc.clause_type,
                metadata=doc.metadata,
                matched_tokens=matched,
            ))

        elapsed_ms = (time.time() - start_time) * 1000.0

        return SearchResponse(
            query=query,
            query_hash=compute_query_hash(query),
            mode=mode,
            results=results,
            total_matches=len(scored_results),
            search_time_ms=round(elapsed_ms, 2),
            top_k=k,
            score_threshold=threshold,
        )

    def _compute_bm25_score(
        self,
        query_tokens: List[str],
        doc: IndexDocument,
        k1: float = 1.5,
        b: float = 0.75,
    ) -> Tuple[float, List[str]]:
        """Compute BM25 score for a document against query tokens."""
        score = 0.0
        matched: List[str] = []
        doc_len = len(doc.tokens) if doc.tokens else 1
        avg_dl = self._avg_doc_length if self._avg_doc_length > 0 else 1.0

        for token in query_tokens:
            if token not in doc.token_freqs:
                continue
            tf = doc.token_freqs[token]
            df = self._token_doc_freq.get(token, 0)
            n = self._doc_count

            idf = math.log((n - df + 0.5) / (df + 0.5) + 1.0)
            tf_norm = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_len / avg_dl))
            score += idf * tf_norm
            matched.append(token)

        return score, matched

    # ========================================================================
    # CLAUSE TEMPLATE RETRIEVAL
    # ========================================================================

    def get_clause_templates_by_type(self, clause_type: str) -> List[ClauseTemplate]:
        """Retrieve all clause templates of a given type."""
        template_ids = self._clause_by_type.get(clause_type, [])
        return [self._clause_templates[tid] for tid in template_ids if tid in self._clause_templates]

    def get_clause_templates_by_jurisdiction(self, jurisdiction: str) -> List[ClauseTemplate]:
        """Retrieve all clause templates for a given jurisdiction."""
        template_ids = self._clause_by_jurisdiction.get(jurisdiction, [])
        return [self._clause_templates[tid] for tid in template_ids if tid in self._clause_templates]

    def get_clause_template(self, clause_id: str) -> Optional[ClauseTemplate]:
        """Retrieve a specific clause template by ID."""
        return self._clause_templates.get(clause_id)

    def match_templates(
        self,
        query: str,
        clause_type: str = "",
        jurisdiction: str = "",
        top_k: int = 5,
    ) -> List[TemplateMatchResult]:
        """Match query against clause templates with scoring."""
        search_resp = self.search(
            query=query,
            top_k=top_k,
            category_filter="clause_template",
            clause_type_filter=clause_type,
            jurisdiction_filter=jurisdiction,
            mode=SearchMode.TEMPLATE,
        )

        results: List[TemplateMatchResult] = []
        for sr in search_resp.results:
            template = self._clause_templates.get(sr.doc_id)
            if template:
                results.append(TemplateMatchResult(
                    template=template,
                    match_score=sr.score,
                    matched_on=sr.matched_tokens,
                ))
        return results

    # ========================================================================
    # DOCUMENT SIMILARITY
    # ========================================================================

    def compute_document_similarity(self, doc_a_id: str, doc_b_id: str) -> Optional[DocumentSimilarityResult]:
        """Compute similarity between two indexed documents."""
        doc_a = self._documents.get(doc_a_id)
        doc_b = self._documents.get(doc_b_id)
        if not doc_a or not doc_b:
            return None

        set_a = set(doc_a.tokens)
        set_b = set(doc_b.tokens)

        intersection = set_a & set_b
        union = set_a | set_b
        jaccard = len(intersection) / len(union) if union else 0.0

        vec_a = doc_a.token_freqs
        vec_b = doc_b.token_freqs
        all_tokens_set = set(vec_a.keys()) | set(vec_b.keys())
        dot_product = sum(vec_a.get(t, 0) * vec_b.get(t, 0) for t in all_tokens_set)
        mag_a = math.sqrt(sum(v ** 2 for v in vec_a.values())) if vec_a else 0.0
        mag_b = math.sqrt(sum(v ** 2 for v in vec_b.values())) if vec_b else 0.0
        cosine = dot_product / (mag_a * mag_b) if (mag_a > 0 and mag_b > 0) else 0.0

        clauses_a = {doc_a.clause_type} if doc_a.clause_type else set()
        clauses_b = {doc_b.clause_type} if doc_b.clause_type else set()
        shared = list(clauses_a & clauses_b)
        unique_a = list(clauses_a - clauses_b)
        unique_b = list(clauses_b - clauses_a)

        return DocumentSimilarityResult(
            doc_a_id=doc_a_id,
            doc_b_id=doc_b_id,
            cosine_similarity=round(cosine, 4),
            jaccard_similarity=round(jaccard, 4),
            shared_clauses=shared,
            unique_to_a=unique_a,
            unique_to_b=unique_b,
        )

    # ========================================================================
    # INDEX STATS
    # ========================================================================

    def get_stats(self) -> Dict[str, Any]:
        """Return index statistics."""
        return {
            "total_documents": self._doc_count,
            "total_unique_tokens": len(self._inverted_index),
            "total_tokens": self._total_tokens,
            "avg_doc_length": round(self._avg_doc_length, 2),
            "total_clause_templates": len(self._clause_templates),
            "clause_types": len(self._clause_by_type),
            "jurisdictions_indexed": len(self._clause_by_jurisdiction),
        }

    def get_all_clause_types(self) -> List[str]:
        """Return all clause types in the template library."""
        return sorted(self._clause_by_type.keys())

    def get_all_jurisdictions(self) -> List[str]:
        """Return all jurisdictions in the template library."""
        return sorted(self._clause_by_jurisdiction.keys())


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def compute_query_hash(query: str) -> str:
    """Compute SHA-256 hash of a query string for determinism tracking."""
    return hashlib.sha256(query.strip().lower().encode("utf-8")).hexdigest()


def compute_content_hash(content: str) -> str:
    """Compute SHA-256 hash of document content."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


# ============================================================================
# MODULE-LEVEL SINGLETON
# ============================================================================

_search_index: Optional[DoctrineSearchIndex] = None


def get_search_index(
    top_k: int = DEFAULT_TOP_K,
    score_threshold: float = SCORE_THRESHOLD,
) -> DoctrineSearchIndex:
    """Get or create the singleton search index."""
    global _search_index
    if _search_index is None:
        _search_index = DoctrineSearchIndex(top_k=top_k, score_threshold=score_threshold)
        logger.info("DoctrineSearchIndex initialized | top_k={} threshold={}", top_k, score_threshold)
    return _search_index


def reset_search_index() -> None:
    """Reset the singleton search index (for testing)."""
    global _search_index
    _search_index = None
