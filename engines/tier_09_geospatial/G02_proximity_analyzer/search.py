import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Any, Optional

class SearchDocument:
    def __init__(self, doc_id: int, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = doc_id
        self.title = title
        self.content = content
        self.tags = tags
        self.weight = weight

class SearchResult:
    def __init__(self, doc_id: int, score: float, title: str, snippet: str):
        self.doc_id = doc_id
        self.score = score
        self.title = title
        self.snippet = snippet

class SearchIndex:
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.total_docs: int = 0
        self.avg_doc_length: float = 0.0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._preseeded = False

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            tf_counter = Counter(tokens)
            self.term_freqs[doc.id] = dict(tf_counter)
            for term in tf_counter:
                self.term_doc_freq[term] += 1
            self._idf_cache.clear()
            self._update_avg_doc_length()

    def _update_avg_doc_length(self):
        if self.total_docs == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        tokens = text.split()
        return [t for t in tokens if len(t) > 1]

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int, k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        tf_dict = self.term_freqs[doc_id]
        for term in query_terms:
            idf = self._compute_idf(term)
            tf = tf_dict.get(term, 0)
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * doc_len / self.avg_doc_length)
            if denominator == 0:
                continue
            score += idf * (numerator / denominator)
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        tf_dict = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            tf = tf_dict.get(term, 0)
            if tf == 0:
                continue
            norm_tf = tf / doc_len
            idf = self._compute_idf(term)
            score += norm_tf * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, method: str = "bm25") -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        heap = []
        for doc_id in self.documents:
            if method == "bm25":
                score = self._score_bm25(query_terms, doc_id)
            elif method == "tfidf":
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                heapq.heappush(heap, (-score, doc_id))
        results = []
        for _ in range(min(limit, len(heap))):
            neg_score, doc_id = heapq.heappop(heap)
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, -neg_score, doc.title, snippet))
        return results

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str]) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:160] + "..." if len(content) > 160 else content
        start = max(positions[0] - 10, 0)
        end = min(positions[0] + 10, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        return snippet + "..." if len(snippet_tokens) < len(tokens) else snippet

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_docs": self.total_docs,
            "avg_doc_length": self.avg_doc_length,
            "unique_terms": len(self.term_doc_freq),
            "documents": list(self.documents.keys())
        }

    def _preseed_documents(self):
        if self._preseeded:
            return
        docs = [
            SearchDocument(
                1,
                "Rule 37 Well Spacing Exception",
                "Analysis of RRC Statewide Rule 37 for well spacing exceptions, including minimum distance requirements between wells and property lines.",
                ["rule37", "well_spacing", "exception", "rrc"],
                1.0
            ),
            SearchDocument(
                2,
                "Density Spacing Exception Analysis",
                "Evaluation of density spacing exceptions under RRC regulations, covering allowable well density per acre and exception criteria.",
                ["density", "spacing", "exception", "regulation"],
                1.0
            ),
            SearchDocument(
                3,
                "Setback from Property Lines",
                "Calculating setbacks from lease and property boundaries for oil and gas wells, including geometric and regulatory considerations.",
                ["setback", "property_line", "geometry", "regulation"],
                1.0
            ),
            SearchDocument(
                4,
                "Proration Unit Calculations",
                "Methods for calculating proration units based on lease acreage and well location, including formulas and geometric approaches.",
                ["proration", "unit", "calculation", "acreage"],
                1.0
            ),
            SearchDocument(
                5,
                "Pooling Unit Geometry",
                "Geometric analysis of pooling units, including polygonal lease boundaries and intersection detection for unit formation.",
                ["pooling", "unit", "geometry", "polygon"],
                1.0
            ),
            SearchDocument(
                6,
                "Haversine Distance Formula Application",
                "Application of the Haversine formula to compute distances between geographic coordinates for well and facility proximity analysis.",
                ["haversine", "distance", "formula", "proximity"],
                1.0
            ),
            SearchDocument(
                7,
                "Vincenty Distance Formula Application",
                "Using Vincenty formula for accurate geodetic distance calculations between wells, pipelines, and lease boundaries.",
                ["vincenty", "distance", "formula", "geodetic"],
                1.0
            ),
            SearchDocument(
                8,
                "Point-to-Line Distance Calculation",
                "Algorithms for calculating minimum distance from a well location to lease boundary lines or setback lines.",
                ["point_line", "distance", "calculation", "algorithm"],
                1.0
            ),
            SearchDocument(
                9,
                "Point-in-Polygon Testing",
                "Methods for determining if a well or facility location falls within a lease or pooling unit polygon using ray casting and winding number algorithms.",
                ["point_polygon", "testing", "ray_casting", "winding_number"],
                1.0
            ),
            SearchDocument(
                10,
                "Polygon Intersection Detection",
                "Detection of intersection between lease polygons for pooling and unit formation, including geometric algorithms and regulatory implications.",
                ["polygon", "intersection", "detection", "pooling"],
                1.0
            ),
            SearchDocument(
                11,
                "Buffer Zone Calculations",
                "Calculation of buffer zones around wells, pipelines, and facilities for regulatory setback compliance and spatial analysis.",
                ["buffer_zone", "calculation", "setback", "compliance"],
                1.0
            ),
            SearchDocument(
                12,
                "Well Pad Proximity Analysis",
                "Analysis of well pad proximity to lease boundaries, property lines, and other wells using spatial distance formulas.",
                ["well_pad", "proximity", "analysis", "spatial"],
                1.0
            ),
            SearchDocument(
                13,
                "Pipeline Route Proximity",
                "Evaluation of pipeline route proximity to wells, lease boundaries, and dwellings for regulatory compliance and risk assessment.",
                ["pipeline", "route", "proximity", "regulatory"],
                1.0
            ),
            SearchDocument(
                14,
                "Facility Setback from Dwellings",
                "Regulatory analysis of facility setbacks from residential dwellings, including minimum distance requirements and geometric calculations.",
                ["facility", "setback", "dwelling", "regulatory"],
                1.0
            ),
            SearchDocument(
                15,
                "Lease Boundary Distance Calculation",
                "Methods for calculating distance from well locations to lease boundaries using geometric and geodetic formulas.",
                ["lease", "boundary", "distance", "calculation"],
                1.0
            ),
            SearchDocument(
                16,
                "Horizontal Well Lateral Path Analysis",
                "Geometric and regulatory analysis of horizontal well lateral paths, including setback compliance and collision detection.",
                ["horizontal", "well", "lateral", "path", "analysis"],
                1.0
            ),
            SearchDocument(
                17,
                "Directional Survey Interpolation",
                "Interpolation of directional survey data for well path analysis, including minimum curvature and regulatory compliance.",
                ["directional", "survey", "interpolation", "well_path"],
                1.0
            ),
            SearchDocument(
                18,
                "Minimum Curvature Method",
                "Implementation of the minimum curvature method for directional well path calculation and spatial interpolation.",
                ["minimum_curvature", "method", "directional", "interpolation"],
                1.0
            ),
            SearchDocument(
                19,
                "Well Path Collision Detection",
                "Detection of potential collisions between well paths using geometric algorithms and regulatory setback requirements.",
                ["well_path", "collision", "detection", "algorithm"],
                1.0
            ),
            SearchDocument(
                20,
                "Surface to Bottomhole Offset Calculation",
                "Calculation of offset between surface and bottomhole locations for directional and horizontal wells using geodetic formulas.",
                ["surface", "bottomhole", "offset", "calculation"],
                1.0
            ),
            SearchDocument(
                21,
                "Lease Boundary Polygon Construction",
                "Construction of lease boundary polygons from survey data for spatial analysis and pooling unit formation.",
                ["lease", "boundary", "polygon", "construction"],
                1.0
            ),
            SearchDocument(
                22,
                "Spatial Indexing for Well Locations",
                "Use of spatial indexing techniques for efficient proximity analysis of well locations and regulatory compliance checks.",
                ["spatial_indexing", "well_location", "proximity", "compliance"],
                1.0
            ),
            SearchDocument(
                23,
                "Regulatory Compliance Checklist",
                "Checklist for regulatory compliance in well spacing, density, setback, and pooling unit formation under RRC rules.",
                ["regulatory", "compliance", "checklist", "rrc"],
                1.0
            ),
            SearchDocument(
                24,
                "Geometric Algorithms for Lease Analysis",
                "Overview of geometric algorithms used in lease boundary analysis, pooling unit formation, and setback calculations.",
                ["geometric", "algorithm", "lease", "analysis"],
                1.0
            ),
            SearchDocument(
                25,
                "GIS Integration for Well Spacing",
                "Integration of GIS data for well spacing, lease boundary mapping, and regulatory analysis under Statewide Rule 37.",
                ["gis", "well_spacing", "mapping", "rule37"],
                1.0
            ),
            SearchDocument(
                26,
                "Exception Application Workflow",
                "Workflow for applying for spacing and density exceptions under RRC rules, including documentation and spatial analysis.",
                ["exception", "application", "workflow", "rrc"],
                1.0
            ),
            SearchDocument(
                27,
                "Spatial Buffer Construction",
                "Construction of spatial buffers for setback analysis around wells, pipelines, and facilities using geometric algorithms.",
                ["spatial", "buffer", "construction", "setback"],
                1.0
            ),
            SearchDocument(
                28,
                "Lease Acreage Calculation",
                "Methods for calculating lease acreage from survey data and polygonal boundaries for proration and pooling analysis.",
                ["lease", "acreage", "calculation", "survey"],
                1.0
            ),
            SearchDocument(
                29,
                "Well Spacing Compliance Audit",
                "Audit procedures for verifying well spacing compliance with Statewide Rule 37 and density regulations.",
                ["well_spacing", "compliance", "audit", "rule37"],
                1.0
            ),
            SearchDocument(
                30,
                "Directional Well Path Geometry",
                "Geometric modeling of directional well paths for collision detection and setback compliance analysis.",
                ["directional", "well_path", "geometry", "collision"],
                1.0
            ),
        ]
        for doc in docs:
            self.add_document(doc)
        self._preseeded = True

def get_search_index() -> SearchIndex:
    if not hasattr(get_search_index, "_instance"):
        get_search_index._instance = SearchIndex()
        get_search_index._instance._preseed_documents()
    return get_search_index._instance