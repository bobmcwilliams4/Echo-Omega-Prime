"""
LM12 GIS Integration Engine — Search Module
Vector search fallback when doctrine cache misses, plus spatial search.

Provides semantic retrieval using TF-IDF cosine similarity for GIS doctrine
matching. No external vector DB dependency — self-contained and deterministic.

Author: ECHO OMEGA PRIME
Engine: LM12 GIS Integration
"""

from __future__ import annotations

import hashlib
import math
import re
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

from loguru import logger


# ==============================================================================
# SEARCH RESULT MODEL
# ==============================================================================

@dataclass
class SearchResult:
    """A single search result from the GIS doctrine corpus."""
    topic: str = ""
    score: float = 0.0
    keywords_matched: List[str] = field(default_factory=list)
    conclusion_preview: str = ""
    domain: str = ""
    confidence: str = ""
    authority_refs: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic": self.topic,
            "score": round(self.score, 4),
            "keywords_matched": self.keywords_matched,
            "conclusion_preview": self.conclusion_preview[:300],
            "domain": self.domain,
            "confidence": self.confidence,
            "authority_refs": self.authority_refs,
            "metadata": self.metadata,
        }


@dataclass
class SearchResponse:
    """Aggregated search response with multiple results."""
    query: str = ""
    query_hash: str = ""
    results: List[SearchResult] = field(default_factory=list)
    total_candidates: int = 0
    search_time_ms: float = 0.0
    method: str = "tfidf_cosine"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "query_hash": self.query_hash,
            "results": [r.to_dict() for r in self.results],
            "total_candidates": self.total_candidates,
            "search_time_ms": round(self.search_time_ms, 3),
            "method": self.method,
        }


@dataclass
class SearchDocument:
    """A document to be indexed in the search engine."""
    doc_id: str = ""
    content: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


# ==============================================================================
# TF-IDF VECTOR INDEX
# ==============================================================================

class TFIDFIndex:
    """
    Self-contained TF-IDF index for doctrine search.
    No external dependencies. Pure Python cosine similarity.
    """

    def __init__(self) -> None:
        self.documents: Dict[str, Dict[str, Any]] = {}
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.doc_term_freq: Dict[str, Counter] = {}
        self.doc_norms: Dict[str, float] = {}
        self.total_docs: int = 0
        self._built: bool = False
        self._stopwords: Set[str] = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
            "been", "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "could", "should", "may", "might", "shall", "can", "this",
            "that", "these", "those", "it", "its", "not", "no", "if", "then",
            "than", "when", "where", "which", "who", "whom", "how", "what", "all",
            "each", "every", "both", "few", "more", "most", "other", "some", "such",
            "only", "own", "same", "so", "very", "just", "because", "about", "into",
            "through", "during", "before", "after", "above", "below", "between",
        }

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into normalized terms."""
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s_-]', ' ', text)
        tokens = text.split()
        return [t for t in tokens if t not in self._stopwords and len(t) > 1]

    def add_document(self, doc_id: str, text: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a document to the index."""
        tokens = self._tokenize(text)
        term_freq = Counter(tokens)
        self.doc_term_freq[doc_id] = term_freq
        self.documents[doc_id] = {
            "text": text,
            "token_count": len(tokens),
            "metadata": metadata or {},
        }
        seen_terms: Set[str] = set()
        for token in tokens:
            if token not in seen_terms:
                self.term_doc_freq[token] += 1
                seen_terms.add(token)
        self.total_docs = len(self.documents)
        self._built = False

    def build(self) -> None:
        """Precompute document norms for fast cosine similarity."""
        if self.total_docs == 0:
            self._built = True
            return
        for doc_id, term_freq in self.doc_term_freq.items():
            norm_sq = 0.0
            for term, freq in term_freq.items():
                tfidf = self._tfidf(term, freq)
                norm_sq += tfidf * tfidf
            self.doc_norms[doc_id] = math.sqrt(norm_sq) if norm_sq > 0 else 1.0
        self._built = True
        logger.info(f"TF-IDF index built: {self.total_docs} documents, {len(self.term_doc_freq)} unique terms")

    def _tfidf(self, term: str, term_freq: int) -> float:
        """Compute TF-IDF weight for a term."""
        if self.total_docs == 0:
            return 0.0
        tf = 1 + math.log(term_freq) if term_freq > 0 else 0.0
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(self.total_docs / (1 + df)) if df > 0 else 0.0
        return tf * idf

    def search(self, query: str, top_k: int = 10, min_score: float = 0.05) -> List[Tuple[str, float, List[str]]]:
        """
        Search the index for documents matching the query.

        Returns list of (doc_id, score, matched_terms) tuples.
        """
        if not self._built:
            self.build()

        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        query_tf = Counter(query_tokens)
        query_norm_sq = 0.0
        query_tfidf: Dict[str, float] = {}
        for term, freq in query_tf.items():
            w = self._tfidf(term, freq)
            query_tfidf[term] = w
            query_norm_sq += w * w
        query_norm = math.sqrt(query_norm_sq) if query_norm_sq > 0 else 1.0

        scores: Dict[str, Tuple[float, List[str]]] = {}
        for doc_id, doc_tf in self.doc_term_freq.items():
            dot_product = 0.0
            matched_terms: List[str] = []
            for term, q_w in query_tfidf.items():
                if term in doc_tf:
                    d_w = self._tfidf(term, doc_tf[term])
                    dot_product += q_w * d_w
                    matched_terms.append(term)
            if dot_product > 0:
                cosine = dot_product / (query_norm * self.doc_norms.get(doc_id, 1.0))
                if cosine >= min_score:
                    scores[doc_id] = (cosine, matched_terms)

        sorted_results = sorted(scores.items(), key=lambda x: x[1][0], reverse=True)
        return [(doc_id, score, terms) for doc_id, (score, terms) in sorted_results[:top_k]]


# ==============================================================================
# GIS DOCTRINE SEARCH ENGINE
# ==============================================================================

class GISDoctrineSearch:
    """
    Full-text search over GIS doctrine blocks with domain-aware ranking.
    Provides the semantic retrieval layer (Layer 2) for cache misses.
    """

    def __init__(self) -> None:
        self._index: TFIDFIndex = TFIDFIndex()
        self._doctrine_metadata: Dict[str, Dict[str, Any]] = {}
        self._built: bool = False
        self._keyword_boost: float = 1.5
        self._domain_boost: float = 1.2

    def index_doctrine_block(
        self,
        topic: str,
        keywords: List[str],
        conclusion_template: str,
        reasoning_framework: str,
        confidence: str,
        domain: str = "general",
        authority_refs: Optional[List[str]] = None,
    ) -> None:
        """Index a single doctrine block for search."""
        text_parts = [
            topic,
            " ".join(keywords),
            conclusion_template,
            reasoning_framework,
        ]
        full_text = " ".join(text_parts)
        metadata = {
            "topic": topic,
            "keywords": keywords,
            "conclusion_preview": conclusion_template[:300],
            "confidence": confidence,
            "domain": domain,
            "authority_refs": authority_refs or [],
        }
        self._index.add_document(topic, full_text, metadata)
        self._doctrine_metadata[topic] = metadata
        self._built = False

    def build_index(self) -> None:
        """Build the search index after all doctrines are loaded."""
        self._index.build()
        self._built = True
        logger.info(f"GIS doctrine search index built: {len(self._doctrine_metadata)} blocks indexed")

    def search(
        self,
        query: str,
        top_k: int = 5,
        min_score: float = 0.05,
        domain_filter: Optional[str] = None,
    ) -> SearchResponse:
        """
        Search doctrine blocks for the given query.

        Args:
            query: Raw search query.
            top_k: Maximum results to return.
            min_score: Minimum relevance score threshold.
            domain_filter: Optional domain to filter results.

        Returns:
            SearchResponse with ranked results.
        """
        start = time.time()

        if not self._built:
            self.build_index()

        raw_results = self._index.search(query, top_k=top_k * 2, min_score=min_score)

        results: List[SearchResult] = []
        for doc_id, score, matched_terms in raw_results:
            meta = self._doctrine_metadata.get(doc_id, {})

            if domain_filter and meta.get("domain", "") != domain_filter:
                continue

            # Keyword boost: if query terms match doctrine keywords directly
            doctrine_keywords = [k.lower() for k in meta.get("keywords", [])]
            keyword_overlap = sum(1 for t in matched_terms if t in doctrine_keywords)
            boosted_score = score + (keyword_overlap * 0.1 * self._keyword_boost)

            result = SearchResult(
                topic=doc_id,
                score=boosted_score,
                keywords_matched=matched_terms,
                conclusion_preview=meta.get("conclusion_preview", ""),
                domain=meta.get("domain", "general"),
                confidence=meta.get("confidence", "UNKNOWN"),
                authority_refs=meta.get("authority_refs", []),
                metadata={"raw_score": score, "keyword_boost": keyword_overlap},
            )
            results.append(result)

        results.sort(key=lambda r: r.score, reverse=True)
        results = results[:top_k]

        search_time = (time.time() - start) * 1000

        response = SearchResponse(
            query=query,
            query_hash=hashlib.sha256(query.encode()).hexdigest()[:16],
            results=results,
            total_candidates=len(raw_results),
            search_time_ms=search_time,
            method="tfidf_cosine_boosted",
        )

        logger.debug(
            f"Search: '{query[:50]}' -> {len(results)} results in {search_time:.1f}ms "
            f"(top: {results[0].topic if results else 'none'} @ {results[0].score:.3f if results else 0})"
        )

        return response

    def get_related_doctrines(self, topic: str, top_k: int = 5) -> List[SearchResult]:
        """Find doctrines related to a given topic."""
        meta = self._doctrine_metadata.get(topic, {})
        if not meta:
            return []
        keywords = meta.get("keywords", [])
        query = f"{topic} {' '.join(keywords)}"
        response = self.search(query, top_k=top_k + 1, min_score=0.05)
        return [r for r in response.results if r.topic != topic][:top_k]

    def get_index_stats(self) -> Dict[str, Any]:
        """Return statistics about the search index."""
        return {
            "total_documents": self._index.total_docs,
            "unique_terms": len(self._index.term_doc_freq),
            "built": self._built,
            "domains": list(set(m.get("domain", "general") for m in self._doctrine_metadata.values())),
            "confidence_distribution": _count_values(
                [m.get("confidence", "UNKNOWN") for m in self._doctrine_metadata.values()]
            ),
        }


# ==============================================================================
# SPATIAL SEARCH UTILITIES
# ==============================================================================

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two points on Earth.

    Args:
        lat1, lon1: First point in decimal degrees.
        lat2, lon2: Second point in decimal degrees.

    Returns:
        Distance in feet.
    """
    R_FEET = 20_902_231.0  # Earth radius in feet
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R_FEET * c


def point_in_polygon(point: Tuple[float, float], polygon: List[Tuple[float, float]]) -> bool:
    """
    Ray-casting algorithm to determine if a point is inside a polygon.

    Args:
        point: (x, y) coordinate pair.
        polygon: List of (x, y) vertices defining the polygon.

    Returns:
        True if point is inside the polygon.
    """
    x, y = point
    n = len(polygon)
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def polygon_area_acres(vertices: List[Tuple[float, float]]) -> float:
    """
    Calculate the area of a polygon using the Shoelace formula.

    Args:
        vertices: List of (x, y) coordinate pairs in feet.

    Returns:
        Area in acres (1 acre = 43,560 sq ft).
    """
    n = len(vertices)
    if n < 3:
        return 0.0
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    area_sqft = abs(area) / 2.0
    return area_sqft / 43560.0


def bearing_distance_to_xy(
    start_x: float,
    start_y: float,
    bearing_degrees: float,
    distance_feet: float,
) -> Tuple[float, float]:
    """
    Calculate endpoint from a starting point, bearing, and distance.

    Args:
        start_x: Starting X coordinate (easting) in feet.
        start_y: Starting Y coordinate (northing) in feet.
        bearing_degrees: Bearing in decimal degrees from north (clockwise).
        distance_feet: Distance in feet.

    Returns:
        (end_x, end_y) coordinate pair.
    """
    bearing_rad = math.radians(bearing_degrees)
    dx = distance_feet * math.sin(bearing_rad)
    dy = distance_feet * math.cos(bearing_rad)
    return (start_x + dx, start_y + dy)


def parse_bearing_string(bearing_str: str) -> Optional[float]:
    """
    Parse a survey bearing string to decimal degrees.

    Formats accepted:
        N 45d 30' 15" E  -> 45.504167 degrees
        S 30d 00' 00" W  -> 210.0 degrees (from north, clockwise)

    Args:
        bearing_str: Raw bearing string.

    Returns:
        Bearing in decimal degrees from north (clockwise), or None if parse fails.
    """
    pattern = re.compile(
        r'([NS])\s*(\d{1,3})\s*[dD\u00b0]\s*(\d{1,2})\s*[\'\u2032]\s*'
        r'(?:(\d{1,2}(?:\.\d+)?)\s*["\u2033]\s*)?([EW])',
        re.IGNORECASE,
    )
    match = pattern.match(bearing_str.strip())
    if not match:
        return None

    ns = match.group(1).upper()
    degrees = int(match.group(2))
    minutes = int(match.group(3))
    seconds = float(match.group(4)) if match.group(4) else 0.0
    ew = match.group(5).upper()

    decimal_angle = degrees + minutes / 60.0 + seconds / 3600.0

    # Convert quadrant bearing to azimuth (from north, clockwise)
    if ns == "N" and ew == "E":
        azimuth = decimal_angle
    elif ns == "S" and ew == "E":
        azimuth = 180.0 - decimal_angle
    elif ns == "S" and ew == "W":
        azimuth = 180.0 + decimal_angle
    elif ns == "N" and ew == "W":
        azimuth = 360.0 - decimal_angle
    else:
        return None

    return azimuth


def convert_varas_to_feet(varas: float) -> float:
    """Convert Texas varas to feet. 1 vara = 33.3333 inches = 2.7778 feet."""
    return varas * (100.0 / 36.0)


def convert_chains_to_feet(chains: float) -> float:
    """Convert Gunter's chains to feet. 1 chain = 66 feet."""
    return chains * 66.0


def convert_rods_to_feet(rods: float) -> float:
    """Convert rods/perches/poles to feet. 1 rod = 16.5 feet."""
    return rods * 16.5


def convert_links_to_feet(links: float) -> float:
    """Convert links to feet. 1 link = 0.66 feet."""
    return links * 0.66


def _count_values(values: List[str]) -> Dict[str, int]:
    """Count occurrences of each value in a list."""
    counts: Dict[str, int] = defaultdict(int)
    for v in values:
        counts[v] += 1
    return dict(counts)
