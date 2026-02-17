import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

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
    def __init__(self, bm25_k1: float = 1.5, bm25_b: float = 0.75):
        self._documents: Dict[int, SearchDocument] = {}
        self._inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_length: float = 0.0
        self._bm25_k1 = bm25_k1
        self._bm25_b = bm25_b
        self._lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._total_terms = 0
        self._tfidf_norms: Dict[int, float] = {}

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            self._documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self._doc_lengths[doc.id] = len(tokens)
            self._total_terms += len(tokens)
            term_counts = Counter(tokens)
            for term, count in term_counts.items():
                self._inverted_index[term][doc.id] = count
            self._avg_doc_length = (
                sum(self._doc_lengths.values()) / len(self._doc_lengths)
                if self._doc_lengths else 0.0
            )
            self._idf_cache.clear()
            self._tfidf_norms[doc.id] = self._compute_tfidf_norm(doc.id)

    def search(self, query: str, limit: int = 10, method: str = "bm25") -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        candidate_doc_ids = set()
        for token in query_tokens:
            candidate_doc_ids.update(self._inverted_index.get(token, {}).keys())
        scores = {}
        for doc_id in candidate_doc_ids:
            if method == "bm25":
                score = self._score_bm25(query_tokens, doc_id)
            elif method == "tfidf":
                score = self._score_tfidf(query_tokens, doc_id)
            else:
                score = self._score_bm25(query_tokens, doc_id)
            scores[doc_id] = score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self._documents[doc_id]
            snippet = self._make_snippet(doc.content, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            "documents": len(self._documents),
            "avg_doc_length": self._avg_doc_length,
            "total_terms": self._total_terms,
            "unique_terms": len(self._inverted_index),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        N = len(self._documents)
        df = len(self._inverted_index.get(term, {}))
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_tokens: List[str], doc_id: int) -> float:
        doc = self._documents[doc_id]
        doc_len = self._doc_lengths[doc_id]
        score = 0.0
        term_freqs = self._inverted_index
        for term in set(query_tokens):
            if doc_id not in term_freqs.get(term, {}):
                continue
            tf = term_freqs[term][doc_id]
            idf = self._compute_idf(term)
            denom = tf + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / (self._avg_doc_length + 1e-9))
            score += idf * ((tf * (self._bm25_k1 + 1)) / (denom + 1e-9))
        return score * doc.weight

    def _score_tfidf(self, query_tokens: List[str], doc_id: int) -> float:
        doc = self._documents[doc_id]
        doc_len = self._doc_lengths[doc_id]
        tfidf = 0.0
        norm = self._tfidf_norms.get(doc_id, 1.0)
        term_counts = Counter(self._tokenize(doc.content))
        for term in set(query_tokens):
            tf = term_counts.get(term, 0) / (doc_len or 1)
            idf = self._compute_idf(term)
            tfidf += tf * idf
        return (tfidf / (norm + 1e-9)) * doc.weight

    def _compute_tfidf_norm(self, doc_id: int) -> float:
        doc = self._documents[doc_id]
        doc_len = self._doc_lengths[doc_id]
        term_counts = Counter(self._tokenize(doc.content))
        norm = 0.0
        for term, count in term_counts.items():
            tf = count / (doc_len or 1)
            idf = self._compute_idf(term)
            norm += (tf * idf) ** 2
        return math.sqrt(norm)

    def _make_snippet(self, content: str, query_tokens: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            return ' '.join(tokens[:window])
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for qt in set(query_tokens):
            snippet = re.sub(rf'\b({re.escape(qt)})\b', r'*\1*', snippet, flags=re.IGNORECASE)
        return snippet

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1, "Darcy-Weisbach Equation",
            "The Darcy-Weisbach equation is used to calculate pressure drop due to friction in pipelines. It requires the friction factor, which is determined from the Moody chart.",
            ["hydraulics", "friction", "darcy-weisbach"], 1.0
        ),
        SearchDocument(
            2, "Moody Friction Factor",
            "The Moody chart provides friction factors for different Reynolds numbers and relative roughness, essential for pipeline pressure drop calculations.",
            ["hydraulics", "moody", "friction"], 1.0
        ),
        SearchDocument(
            3, "Pipeline Sizing by Velocity",
            "Pipeline sizing ensures fluid velocity remains within recommended limits to prevent erosion and minimize pressure drop.",
            ["sizing", "velocity", "design"], 1.0
        ),
        SearchDocument(
            4, "Pipeline Throughput Calculation",
            "Throughput is determined by pipeline diameter, fluid properties, and pressure gradient. Hydraulic calculations optimize throughput.",
            ["throughput", "hydraulics", "design"], 1.0
        ),
        SearchDocument(
            5, "API 5L Grade X52 Pipe",
            "API 5L X52 is a common pipeline steel grade, offering a balance of strength and weldability for oil and gas transmission.",
            ["materials", "api 5l", "x52"], 1.0
        ),
        SearchDocument(
            6, "API 5L Grade X65 Pipe",
            "API 5L X65 provides higher strength for pipelines, enabling higher operating pressures and longer spans between stations.",
            ["materials", "api 5l", "x65"], 1.0
        ),
        SearchDocument(
            7, "API 5L Grade X70 Pipe",
            "X70 grade pipe is used for high-pressure pipelines, offering improved toughness and weldability.",
            ["materials", "api 5l", "x70"], 1.0
        ),
        SearchDocument(
            8, "API 5L Grade X80 Pipe",
            "API 5L X80 is a high-strength steel used in demanding pipeline applications, supporting high pressures and long distances.",
            ["materials", "api 5l", "x80"], 1.0
        ),
        SearchDocument(
            9, "Welding Procedure Specification (WPS)",
            "A WPS outlines welding parameters and techniques to ensure consistent, high-quality pipeline welds.",
            ["welding", "wps", "procedures"], 1.0
        ),
        SearchDocument(
            10, "Procedure Qualification Record (PQR)",
            "The PQR documents tests and results validating a WPS for pipeline construction.",
            ["welding", "pqr", "qualification"], 1.0
        ),
        SearchDocument(
            11, "SMAW and GMAW Welding",
            "Shielded Metal Arc Welding (SMAW) and Gas Metal Arc Welding (GMAW) are common techniques for pipeline fabrication.",
            ["welding", "smaw", "gmaw"], 1.0
        ),
        SearchDocument(
            12, "FBE Pipeline Coating",
            "Fusion Bonded Epoxy (FBE) is a standard coating for corrosion protection of pipelines.",
            ["coating", "fbe", "corrosion"], 1.0
        ),
        SearchDocument(
            13, "Three-Layer Polyethylene Coating",
            "Three-layer polyethylene systems provide robust pipeline protection against corrosion and mechanical damage.",
            ["coating", "polyethylene", "corrosion"], 1.0
        ),
        SearchDocument(
            14, "ROW Clearing and Trenching",
            "Right-of-way (ROW) clearing and trenching are critical steps in pipeline construction, ensuring safe and efficient installation.",
            ["construction", "row", "trenching"], 1.0
        ),
        SearchDocument(
            15, "Backfill Procedures",
            "Proper backfill ensures pipeline stability and protects against mechanical damage after installation.",
            ["construction", "backfill", "installation"], 1.0
        ),
        SearchDocument(
            16, "Horizontal Directional Drilling (HDD)",
            "HDD is a trenchless method for installing pipelines under obstacles such as rivers and roads.",
            ["construction", "hdd", "trenchless"], 1.0
        ),
        SearchDocument(
            17, "Bore Crossing Techniques",
            "Bore crossing involves drilling beneath obstacles to lay pipelines with minimal surface disruption.",
            ["construction", "bore crossing", "hdd"], 1.0
        ),
        SearchDocument(
            18, "Pipeline Pigging: Cleaning and Gauging",
            "Pigging uses devices called pigs to clean and inspect pipelines, ensuring internal integrity.",
            ["pigging", "cleaning", "gauging"], 1.0
        ),
        SearchDocument(
            19, "Intelligent Pigging and ILI",
            "Intelligent pigs perform inline inspection (ILI) using technologies like MFL, ultrasonic, and caliper tools.",
            ["pigging", "ili", "inspection"], 1.0
        ),
        SearchDocument(
            20, "Pipeline Integrity Management (PIMS)",
            "PIMS programs, guided by API 1160, manage pipeline risks and ensure regulatory compliance.",
            ["integrity", "pims", "api 1160"], 1.0
        ),
        SearchDocument(
            21, "ASME B31.4 Pipeline Stress Analysis",
            "ASME B31.4 provides stress analysis criteria for liquid pipelines, covering design and operation.",
            ["stress", "asme b31.4", "analysis"], 1.0
        ),
        SearchDocument(
            22, "ASME B31.8 Pipeline Stress Analysis",
            "ASME B31.8 covers stress analysis for gas pipelines, ensuring safe operation under various loads.",
            ["stress", "asme b31.8", "analysis"], 1.0
        ),
        SearchDocument(
            23, "Cathodic Protection Survey",
            "CP surveys assess the effectiveness of cathodic protection systems in preventing pipeline corrosion.",
            ["cathodic protection", "cp", "survey"], 1.0
        ),
        SearchDocument(
            24, "CIPS and DCVG Techniques",
            "Close Interval Potential Survey (CIPS) and Direct Current Voltage Gradient (DCVG) detect coating defects and assess CP.",
            ["cathodic protection", "cips", "dcvg"], 1.0
        ),
        SearchDocument(
            25, "Pipeline SCADA and Leak Detection",
            "SCADA systems monitor pipeline operations and support leak detection using CPM and RTTM methods.",
            ["scada", "leak detection", "cpm", "rttm"], 1.0
        ),
        SearchDocument(
            26, "Pipeline Right of Way Acquisition",
            "ROW acquisition involves securing easements for pipeline installation and operation.",
            ["right of way", "easement", "acquisition"], 1.0
        ),
        SearchDocument(
            27, "PHMSA CFR 49 Parts 192 & 195",
            "PHMSA regulations CFR 49 Parts 192 and 195 govern the safety of gas and hazardous liquid pipelines.",
            ["regulatory", "phmsa", "cfr 49"], 1.0
        ),
        SearchDocument(
            28, "Hydrostatic Testing: Strength and Leak",
            "Hydrostatic testing verifies pipeline strength and leak tightness before commissioning.",
            ["hydrostatic testing", "strength", "leak"], 1.0
        ),
        SearchDocument(
            29, "Compressor Stations: Centrifugal and Reciprocating",
            "Compressor stations use centrifugal and reciprocating compressors to maintain pipeline pressure.",
            ["compressor", "centrifugal", "reciprocating"], 1.0
        ),
        SearchDocument(
            30, "Pump Stations: Centrifugal and Positive Displacement",
            "Pump stations employ centrifugal and positive displacement pumps for liquid pipeline operations.",
            ["pump", "centrifugal", "positive displacement"], 1.0
        ),
        SearchDocument(
            31, "Flow Assurance: Hydrate, Wax, Asphaltene",
            "Flow assurance addresses issues like hydrate, wax, and asphaltene formation that can impede pipeline flow.",
            ["flow assurance", "hydrate", "wax", "asphaltene"], 1.0
        ),
        SearchDocument(
            32, "Pipeline Decommissioning: Abandonment and Purging",
            "Decommissioning involves safely abandoning and purging pipelines at the end of their service life.",
            ["decommissioning", "abandonment", "purging"], 1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)