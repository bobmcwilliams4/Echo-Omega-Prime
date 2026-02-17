import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# --- Data Classes ---

class SearchDocument:
    def __init__(self, id: str, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = id
        self.title = title
        self.content = content
        self.tags = tags
        self.weight = weight

class SearchResult:
    def __init__(self, doc_id: str, score: float, title: str, snippet: str):
        self.doc_id = doc_id
        self.score = score
        self.title = title
        self.snippet = snippet

# --- Search Index Implementation ---

class SearchIndex:
    def __init__(self, bm25_k1: float = 1.5, bm25_b: float = 0.75):
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_doc_freqs: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self.bm25_k1 = bm25_k1
        self.bm25_b = bm25_b
        self._idf_cache: Dict[str, float] = {}

    def _tokenize(self, text: str) -> List[str]:
        # Simple tokenizer: lowercase, split on non-word chars, remove empty tokens
        return [t for t in re.split(r'\W+', text.lower()) if t]

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return  # Don't add duplicates
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            term_counts = Counter(tokens)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            for term in term_counts:
                self.doc_freqs[term] += 1
                self.term_doc_freqs[term][doc.id] = term_counts[term]
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs else 0.0
            self._idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        # IDF with log smoothing
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: str) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        doc = self.documents[doc_id]
        for term in query_terms:
            tf = self.term_doc_freqs.get(term, {}).get(doc_id, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            denom = tf + self.bm25_k1 * (1 - self.bm25_b + self.bm25_b * doc_length / (self.avg_doc_length or 1))
            score += idf * (tf * (self.bm25_k1 + 1)) / denom
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: str) -> float:
        # Term frequency normalization (log normalization)
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        doc = self.documents[doc_id]
        for term in query_terms:
            tf = self.term_doc_freqs.get(term, {}).get(doc_id, 0)
            if tf == 0:
                continue
            tf_norm = 1 + math.log(tf)
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        scores: Dict[str, float] = {}
        tfidf_scores: Dict[str, float] = {}
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.term_doc_freqs.get(term, {}).keys())
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(query_terms, doc_id)
            tfidf_score = self._score_tfidf(query_terms, doc_id)
            # Combine BM25 and TF-IDF (weighted average)
            score = 0.7 * bm25_score + 0.3 * tfidf_score
            scores[doc_id] = score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], snippet_len: int = 200) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:snippet_len] + ("..." if len(content) > snippet_len else "")
        start = max(positions[0] - 10, 0)
        end = min(start + 40, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        # Highlight query terms
        for t in set(query_terms):
            snippet = re.sub(rf'\b({re.escape(t)})\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet[:snippet_len] + ("..." if len(snippet) > snippet_len else "")

    def get_stats(self) -> Dict[str, int]:
        return {
            "total_documents": self.total_docs,
            "unique_terms": len(self.doc_freqs),
            "avg_doc_length": int(self.avg_doc_length),
        }

# --- Singleton Factory ---

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

# --- Pre-seed Domain Documents ---

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            id="1",
            title="RRC Well Data Alignment",
            content="Procedures for aligning Texas Railroad Commission well data with GIS layers, including spatial validation, coordinate transformation, and attribute joining.",
            tags=["well", "rrc", "alignment", "gis"],
            weight=1.2
        ),
        SearchDocument(
            id="2",
            title="Pipeline Route Mapping Standards",
            content="Best practices for mapping pipeline routes, ensuring accurate overlay with surface features, and resolving spatial conflicts in GIS environments.",
            tags=["pipeline", "route", "mapping", "overlay"],
            weight=1.1
        ),
        SearchDocument(
            id="3",
            title="Surface Feature Overlay Techniques",
            content="Techniques for overlaying surface features such as roads, hydrology, and topography onto base GIS layers for comprehensive spatial analysis.",
            tags=["surface", "feature", "overlay", "topography"],
            weight=1.0
        ),
        SearchDocument(
            id="4",
            title="Surface Owner Boundary Delineation",
            content="Methods for delineating surface owner boundaries using survey abstracts, deed records, and county GIS data.",
            tags=["surface owner", "boundary", "delineation", "survey"],
            weight=1.2
        ),
        SearchDocument(
            id="5",
            title="Mineral Owner Boundary Integration",
            content="Integrating mineral owner boundaries with existing GIS layers, including validation against lease and unit boundaries.",
            tags=["mineral owner", "boundary", "integration", "lease"],
            weight=1.1
        ),
        SearchDocument(
            id="6",
            title="Unit Boundary Overlay and Validation",
            content="Overlaying unit boundaries and validating against RRC and lease data for regulatory compliance.",
            tags=["unit", "boundary", "overlay", "validation"],
            weight=1.0
        ),
        SearchDocument(
            id="7",
            title="Lease Boundary QA/QC",
            content="Quality assurance and quality control procedures for lease boundary integration in GIS, including spatial accuracy checks.",
            tags=["lease", "boundary", "qa", "qc"],
            weight=1.1
        ),
        SearchDocument(
            id="8",
            title="Survey Abstract Boundary Overlay",
            content="Overlaying survey abstract boundaries and resolving discrepancies with county and state GIS layers.",
            tags=["survey", "abstract", "boundary", "overlay"],
            weight=1.0
        ),
        SearchDocument(
            id="9",
            title="County Boundary Alignment",
            content="Aligning county boundaries with other spatial layers to ensure consistency across GIS datasets.",
            tags=["county", "boundary", "alignment", "gis"],
            weight=1.0
        ),
        SearchDocument(
            id="10",
            title="Road Infrastructure Layer Integration",
            content="Integrating road infrastructure layers and validating connectivity with pipeline and well locations.",
            tags=["road", "infrastructure", "integration", "pipeline"],
            weight=1.0
        ),
        SearchDocument(
            id="11",
            title="Topographic Feature Overlay and Validation",
            content="Overlaying topographic features and validating elevation data for accurate spatial modeling.",
            tags=["topographic", "feature", "overlay", "validation"],
            weight=1.0
        ),
        SearchDocument(
            id="12",
            title="Hydrology Layer Conflict Resolution",
            content="Resolving conflicts between hydrology layers and other spatial features such as pipelines and roads.",
            tags=["hydrology", "layer", "conflict", "resolution"],
            weight=1.1
        ),
        SearchDocument(
            id="13",
            title="Soil Classification Overlay",
            content="Overlaying soil classification data and integrating with land use and hydrology layers for environmental analysis.",
            tags=["soil", "classification", "overlay", "land use"],
            weight=1.0
        ),
        SearchDocument(
            id="14",
            title="Land Use Classification Integration",
            content="Integrating land use classification data with surface and mineral boundaries for comprehensive GIS analysis.",
            tags=["land use", "classification", "integration", "gis"],
            weight=1.0
        ),
        SearchDocument(
            id="15",
            title="Aerial Imagery Integration",
            content="Procedures for integrating high-resolution aerial imagery with vector GIS layers for enhanced visualization.",
            tags=["aerial imagery", "integration", "visualization"],
            weight=1.0
        ),
        SearchDocument(
            id="16",
            title="Feature Attribute Joining and Validation",
            content="Joining feature attributes across layers and validating for consistency and completeness.",
            tags=["feature", "attribute", "joining", "validation"],
            weight=1.0
        ),
        SearchDocument(
            id="17",
            title="Spatial Query Operations",
            content="Performing spatial queries such as intersection, containment, and proximity analysis in GIS.",
            tags=["spatial", "query", "operations", "gis"],
            weight=1.0
        ),
        SearchDocument(
            id="18",
            title="Layer Styling and Symbology Standards",
            content="Applying standardized symbology and styling to GIS layers for consistent map presentation.",
            tags=["layer", "styling", "symbology", "standards"],
            weight=1.0
        ),
        SearchDocument(
            id="19",
            title="CRS Alignment and Transformation",
            content="Aligning coordinate reference systems (CRS) and transforming spatial data between projections.",
            tags=["crs", "alignment", "transformation", "projection"],
            weight=1.1
        ),
        SearchDocument(
            id="20",
            title="Feature Generalization and Simplification",
            content="Generalizing and simplifying complex features for efficient GIS rendering and analysis.",
            tags=["feature", "generalization", "simplification", "gis"],
            weight=1.0
        ),
        SearchDocument(
            id="21",
            title="QA/QC for GIS Layer Integration",
            content="Comprehensive QA/QC procedures for integrating multiple GIS layers, including topology checks and attribute validation.",
            tags=["qa", "qc", "gis", "integration"],
            weight=1.1
        ),
        SearchDocument(
            id="22",
            title="Survey Abstracts and Legal Descriptions",
            content="Using legal descriptions and survey abstracts to accurately map property boundaries in GIS.",
            tags=["survey", "abstract", "legal", "description"],
            weight=1.0
        ),
        SearchDocument(
            id="23",
            title="County GIS Data Sources",
            content="Overview of county-level GIS data sources for boundaries, roads, and land ownership.",
            tags=["county", "gis", "data", "sources"],
            weight=1.0
        ),
        SearchDocument(
            id="24",
            title="Spatial Data Conflict Resolution",
            content="Strategies for resolving conflicts between overlapping spatial datasets in GIS.",
            tags=["spatial", "data", "conflict", "resolution"],
            weight=1.0
        ),
        SearchDocument(
            id="25",
            title="Metadata Standards for GIS Layers",
            content="Implementing metadata standards for GIS layers to ensure data provenance and usability.",
            tags=["metadata", "standards", "gis", "layers"],
            weight=1.0
        ),
        SearchDocument(
            id="26",
            title="Hydrology and Floodplain Mapping",
            content="Mapping hydrology features and floodplains for risk assessment and regulatory compliance.",
            tags=["hydrology", "floodplain", "mapping", "risk"],
            weight=1.0
        ),
        SearchDocument(
            id="27",
            title="Integrating Soil and Land Use Data",
            content="Combining soil and land use data for environmental impact studies in GIS.",
            tags=["soil", "land use", "integration", "environmental"],
            weight=1.0
        ),
        SearchDocument(
            id="28",
            title="GIS Layer Version Control",
            content="Managing versions of GIS layers to track changes and support rollback.",
            tags=["gis", "layer", "version", "control"],
            weight=1.0
        ),
        SearchDocument(
            id="29",
            title="Automated Spatial QA/QC Tools",
            content="Using automated tools for spatial QA/QC to detect errors in GIS layers.",
            tags=["automated", "spatial", "qa", "qc"],
            weight=1.0
        ),
        SearchDocument(
            id="30",
            title="Integration of Survey and GPS Data",
            content="Integrating survey and GPS data for high-precision GIS mapping.",
            tags=["survey", "gps", "integration", "precision"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)