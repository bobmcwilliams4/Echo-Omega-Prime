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
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.N = 0
        self.avgdl = 0.0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
        self.tf_cache: Dict[Tuple[int, str], float] = {}
        self.k1 = 1.5
        self.b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            tf = Counter(tokens)
            for term, freq in tf.items():
                self.inverted_index[term][doc.id] = freq
            self.N = len(self.documents)
            self.avgdl = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self.idf_cache.clear()
            self.tf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, {}).keys())
        scored = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc = self.documents[doc_id]
            # Weighted sum: BM25 (0.7), TF-IDF (0.3), document weight
            score = (0.7 * bm25_score + 0.3 * tfidf_score) * doc.weight
            snippet = self._make_snippet(doc.content, query_terms)
            scored.append(SearchResult(doc_id, score, doc.title, snippet))
        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "num_documents": self.N,
                "avg_doc_length": self.avgdl,
                "vocab_size": len(self.inverted_index)
            }

    def _tokenize(self, text: str) -> List[str]:
        # Lowercase, remove non-alphanumerics, split on whitespace
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = len(self.inverted_index.get(term, {}))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        tf = Counter(self._tokenize(doc.content))
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self.k1 * (1 - self.b + self.b * doc_len / (self.avgdl if self.avgdl > 0 else 1))
            score += idf * (f * (self.k1 + 1)) / denom
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        tf = Counter(self._tokenize(doc.content))
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            norm_tf = f / doc_len if doc_len > 0 else 0.0
            idf = self._compute_idf(term)
            score += norm_tf * idf
        return score

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:window])
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        # Highlight terms
        for term in set(query_terms):
            snippet = re.sub(r'\b(' + re.escape(term) + r')\b', r'*\1*', snippet, flags=re.IGNORECASE)
        return snippet

# Singleton factory for SearchIndex
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
            1, "Two-Phase vs Three-Phase Separator Selection",
            "Two-phase separators remove gas from liquid, while three-phase separators also split oil and water. Selection depends on fluid composition and downstream requirements.",
            ["separator", "phase", "selection"], 1.0
        ),
        SearchDocument(
            2, "Horizontal vs Vertical Separator Configuration",
            "Horizontal separators are preferred for high liquid volumes and low vertical space. Vertical separators handle large gas flows and are easier to clean.",
            ["separator", "configuration", "horizontal", "vertical"], 1.0
        ),
        SearchDocument(
            3, "Oil-Water Retention Time Calculation (Stokes Law)",
            "Retention time for oil-water separation is calculated using Stokes Law. Droplet settling velocity depends on viscosity, density difference, and droplet size.",
            ["oil", "water", "stokes", "retention", "calculation"], 1.0
        ),
        SearchDocument(
            4, "Gas-Liquid Retention Time (Vapor Dropout)",
            "Gas-liquid separators must provide sufficient retention time for vapor dropout. Sizing considers gas velocity and vessel cross-sectional area.",
            ["gas", "liquid", "retention", "vapor", "dropout"], 1.0
        ),
        SearchDocument(
            5, "Heater Treater Design and Operation",
            "Heater treaters use heat to enhance oil-water separation. Key design factors include firetube sizing, emulsion breaking, and temperature control.",
            ["heater", "treater", "design", "operation"], 1.0
        ),
        SearchDocument(
            6, "Free Water Knockout (FWKO) Sizing",
            "FWKO vessels remove free water before oil enters separators. Sizing is based on inlet water cut, retention time, and expected solids.",
            ["fwko", "sizing", "water", "knockout"], 1.0
        ),
        SearchDocument(
            7, "Mist Extractor Selection: Vane vs Mesh Pad",
            "Vane mist extractors are suitable for high gas flows and low pressure drop. Mesh pads are effective for fine mist but can plug with solids.",
            ["mist", "extractor", "vane", "mesh", "selection"], 1.0
        ),
        SearchDocument(
            8, "Dump Valve Sizing and Level Control",
            "Dump valves regulate liquid level in separators. Sizing considers maximum flow, pressure drop, and control system response.",
            ["dump", "valve", "sizing", "level", "control"], 1.0
        ),
        SearchDocument(
            9, "Separator Vessel Design per ASME Section VIII",
            "Separator vessels must comply with ASME Section VIII for pressure integrity. Design includes wall thickness, nozzle sizing, and code stamping.",
            ["asme", "section viii", "vessel", "design"], 1.0
        ),
        SearchDocument(
            10, "Sand Jet and Sand Drain Systems",
            "Sand jetting systems remove accumulated solids from separator bottoms. Design includes nozzle placement, jet velocity, and drain line sizing.",
            ["sand", "jet", "drain", "system"], 1.0
        ),
        SearchDocument(
            11, "H2S Service and Sour Gas Considerations",
            "Sour service requires corrosion-resistant materials and safety systems. H2S detection, venting, and material selection are critical.",
            ["h2s", "sour", "gas", "service"], 1.0
        ),
        SearchDocument(
            12, "LACT Unit Design and Custody Transfer",
            "LACT (Lease Automatic Custody Transfer) units measure and transfer oil for sale. Key aspects include meter proving, sampling, and ticketing.",
            ["lact", "custody", "transfer", "design"], 1.0
        ),
        SearchDocument(
            13, "Pressure Control and Back Pressure Regulation",
            "Separators use pressure control valves to maintain operating pressure and prevent overpressure. Back pressure regulation ensures stable flow.",
            ["pressure", "control", "back", "regulation"], 1.0
        ),
        SearchDocument(
            14, "Emulsion Breaking in Oil-Water Separation",
            "Emulsions hinder oil-water separation. Chemical demulsifiers and heat can be used to break emulsions and improve separation efficiency.",
            ["emulsion", "breaking", "oil", "water"], 1.0
        ),
        SearchDocument(
            15, "Internals: Inlet Diverters and Coalescers",
            "Inlet diverters reduce fluid velocity and promote phase separation. Coalescers enhance droplet growth for improved oil-water separation.",
            ["internals", "inlet", "diverter", "coalescer"], 1.0
        ),
        SearchDocument(
            16, "Separator Sizing for Slug Flow",
            "Slug flow requires separators with surge volume and proper internals to handle intermittent liquid surges without carryover.",
            ["separator", "sizing", "slug", "flow"], 1.0
        ),
        SearchDocument(
            17, "API 12J Separator Sizing Guidelines",
            "API 12J provides industry standards for separator sizing, including retention times, velocities, and design margins.",
            ["api", "12j", "separator", "sizing"], 1.0
        ),
        SearchDocument(
            18, "Centrifugal vs Gravity Separation",
            "Centrifugal separators use rotational forces to enhance phase separation. Gravity separators rely on density differences and retention time.",
            ["centrifugal", "gravity", "separation"], 1.0
        ),
        SearchDocument(
            19, "Desanding Hydrocyclones",
            "Hydrocyclones remove sand and solids from produced fluids. They are used upstream of separators to reduce sand loading.",
            ["desanding", "hydrocyclone", "sand"], 1.0
        ),
        SearchDocument(
            20, "Level Measurement Technologies",
            "Level transmitters use float, capacitance, or radar to measure liquid levels in separators. Accurate level control prevents carryover.",
            ["level", "measurement", "transmitter"], 1.0
        ),
        SearchDocument(
            21, "Gas Boot Design",
            "Gas boots are used in three-phase separators to handle separated gas. Proper sizing prevents gas carry-under and liquid carryover.",
            ["gas", "boot", "design"], 1.0
        ),
        SearchDocument(
            22, "Vessel Internals: Baffles and Weirs",
            "Baffles and weirs control fluid flow and phase separation inside vessels. They help prevent short-circuiting and improve efficiency.",
            ["baffle", "weir", "internals"], 1.0
        ),
        SearchDocument(
            23, "Separator Startup and Shutdown Procedures",
            "Proper procedures for startup and shutdown prevent upsets and equipment damage. Steps include venting, filling, and pressure equalization.",
            ["separator", "startup", "shutdown"], 1.0
        ),
        SearchDocument(
            24, "Corrosion Monitoring in Separators",
            "Corrosion probes and coupons are used to monitor internal corrosion rates. Regular inspection and chemical treatment are essential.",
            ["corrosion", "monitoring", "separator"], 1.0
        ),
        SearchDocument(
            25, "Separator Troubleshooting Guide",
            "Common separator issues include foaming, carryover, and emulsion formation. Troubleshooting involves checking internals, controls, and process conditions.",
            ["separator", "troubleshooting", "guide"], 1.0
        ),
        SearchDocument(
            26, "Design for Cold Climate Operation",
            "Separators in cold climates require insulation, heat tracing, and freeze protection for dump valves and instrumentation.",
            ["design", "cold", "climate", "operation"], 1.0
        ),
        SearchDocument(
            27, "Separator Maintenance Best Practices",
            "Routine maintenance includes cleaning internals, inspecting pressure relief devices, and verifying instrumentation accuracy.",
            ["separator", "maintenance", "best", "practices"], 1.0
        ),
        SearchDocument(
            28, "Foam Control in Separators",
            "Foam can cause carryover and process upsets. Foam control methods include chemical antifoam injection and proper vessel sizing.",
            ["foam", "control", "separator"], 1.0
        ),
        SearchDocument(
            29, "Produced Water Disposal Options",
            "Produced water from separators can be injected, treated, or disposed. Selection depends on regulations and water quality.",
            ["produced", "water", "disposal"], 1.0
        ),
        SearchDocument(
            30, "Separator Instrumentation and Automation",
            "Modern separators use PLCs and SCADA for automated control of valves, levels, and pressures. Instrumentation reliability is critical.",
            ["separator", "instrumentation", "automation"], 1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)