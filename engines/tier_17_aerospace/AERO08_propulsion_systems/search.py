import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

# --- Data Classes ---

class SearchDocument:
    def __init__(self, id: int, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = id
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

# --- Search Index Implementation ---

class SearchIndex:
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.N: int = 0
        self.avg_doc_length: float = 0.0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            tf = Counter(tokens)
            self.documents[doc.id] = doc
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf.keys():
                self.doc_freqs[term] += 1
                self.inverted_index[term].add(doc.id)
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, set()))
        scored: List[Tuple[int, float]] = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc_weight = self.documents[doc_id].weight
            score = 0.7 * bm25_score + 0.3 * tfidf_score
            score *= doc_weight
            scored.append((doc_id, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "num_documents": self.N,
                "avg_doc_length": self.avg_doc_length,
                "vocab_size": len(self.doc_freqs)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / (self.avg_doc_length + 1e-9))
            numer = freq * (self._bm25_k1 + 1)
            score += idf * numer / (denom + 1e-9)
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            tf_norm = tf[term] / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = []
        for i, t in enumerate(tokens):
            if t in query_terms:
                positions.append(i)
        if not positions:
            return ' '.join(tokens[:window]) + '...'
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        return snippet + '...'

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
            1,
            "Turbofan Bypass Ratio Optimization",
            "Bypass ratio optimization in modern turbofan engines improves propulsive efficiency and reduces specific fuel consumption. The AERO08 engine utilizes a high bypass ratio for optimal cruise performance, balancing core size and fan diameter.",
            ["turbofan", "bypass ratio", "optimization", "propulsion"],
            1.0
        ),
        SearchDocument(
            2,
            "Compressor Surge and Stall Phenomena",
            "Compressor surge and stall are critical phenomena affecting engine stability. The AERO08's multi-stage axial compressor employs variable stator vanes and bleed valves to mitigate surge and stall during transient operations.",
            ["compressor", "surge", "stall", "stability"],
            1.0
        ),
        SearchDocument(
            3,
            "Turbine Blade Cooling Technology",
            "Advanced turbine blade cooling in the AERO08 engine uses internal air passages, film cooling, and thermal barrier coatings. This enables operation at higher turbine inlet temperatures, improving thermal efficiency.",
            ["turbine", "blade cooling", "thermal", "coating"],
            1.0
        ),
        SearchDocument(
            4,
            "Full Authority Digital Engine Control (FADEC)",
            "The AERO08's FADEC system provides precise control of fuel flow, variable geometry, and engine parameters. FADEC enhances engine performance, safety, and maintenance diagnostics.",
            ["FADEC", "digital control", "engine management"],
            1.0
        ),
        SearchDocument(
            5,
            "Engine Condition Monitoring (ECM) and EGT Margin",
            "Engine Condition Monitoring in the AERO08 tracks parameters such as EGT margin, vibration, and oil debris. ECM supports predictive maintenance and extends engine life.",
            ["ECM", "EGT margin", "monitoring", "maintenance"],
            1.0
        ),
        SearchDocument(
            6,
            "Thrust Specific Fuel Consumption (TSFC) Optimization",
            "TSFC optimization in the AERO08 is achieved through high bypass ratios, advanced materials, and low-pressure turbine efficiency. Lower TSFC translates to reduced operating costs.",
            ["TSFC", "fuel consumption", "optimization"],
            1.0
        ),
        SearchDocument(
            7,
            "Bird Strike and Foreign Object Damage (FOD) Tolerance",
            "The AERO08 engine incorporates reinforced fan blades and inlet screens to improve bird strike and FOD tolerance. Design validation includes bird ingestion tests per certification requirements.",
            ["bird strike", "FOD", "tolerance", "safety"],
            1.0
        ),
        SearchDocument(
            8,
            "Engine-Airframe Integration and Nacelle Design",
            "AERO08's nacelle design minimizes drag and optimizes airflow for engine-airframe integration. Pylon mounting and acoustic liners reduce noise and improve aerodynamic performance.",
            ["integration", "nacelle", "airframe", "design"],
            1.0
        ),
        SearchDocument(
            9,
            "Life-Limited Parts (LLP) Management and Rotordynamics",
            "LLP management in the AERO08 tracks cycles and usage of critical rotating components. Rotordynamics analysis ensures vibration levels remain within safe limits throughout the engine life.",
            ["LLP", "rotordynamics", "vibration", "lifecycle"],
            1.0
        ),
        SearchDocument(
            10,
            "Variable Stator Vanes in Compressor Control",
            "Variable stator vanes in the AERO08 axial compressor adjust airflow angles, enhancing surge margin and part-speed efficiency. Controlled by the FADEC, these vanes optimize compressor performance.",
            ["compressor", "variable stator", "FADEC"],
            1.0
        ),
        SearchDocument(
            11,
            "Thermal Barrier Coatings for Turbine Blades",
            "Thermal barrier coatings protect AERO08 turbine blades from high-temperature gases, reducing oxidation and thermal fatigue. This extends blade life and maintains efficiency.",
            ["thermal coating", "turbine", "blade", "protection"],
            1.0
        ),
        SearchDocument(
            12,
            "Advanced Materials in Fan and Compressor",
            "The AERO08 engine uses titanium alloys and composite materials in fan and compressor sections, reducing weight and improving fatigue resistance.",
            ["materials", "fan", "compressor", "titanium"],
            1.0
        ),
        SearchDocument(
            13,
            "Engine Vibration Monitoring and Diagnostics",
            "Vibration sensors in the AERO08 provide real-time monitoring of rotordynamics. Data is analyzed by the ECM for early detection of imbalance or bearing wear.",
            ["vibration", "monitoring", "diagnostics", "rotordynamics"],
            1.0
        ),
        SearchDocument(
            14,
            "Low Emissions Combustor Design",
            "AERO08's combustor employs lean-burn technology and staged fuel injection to minimize NOx and CO emissions, meeting stringent environmental regulations.",
            ["combustor", "emissions", "NOx", "environment"],
            1.0
        ),
        SearchDocument(
            15,
            "Fan Blade Out (FBO) Containment",
            "The fan case in the AERO08 is designed to contain fan blade out events, protecting the airframe and minimizing risk to passengers and crew.",
            ["fan blade", "containment", "safety"],
            1.0
        ),
        SearchDocument(
            16,
            "Oil System and Bearing Lubrication",
            "AERO08's oil system ensures continuous lubrication of bearings and gears. Oil debris monitoring supports ECM and helps prevent catastrophic failures.",
            ["oil system", "lubrication", "bearings", "maintenance"],
            1.0
        ),
        SearchDocument(
            17,
            "Health Monitoring using Vibration and EGT Data",
            "The ECM in AERO08 correlates vibration and exhaust gas temperature data to predict maintenance needs and optimize engine availability.",
            ["health monitoring", "vibration", "EGT", "ECM"],
            1.0
        ),
        SearchDocument(
            18,
            "High-Pressure Turbine Cooling Passages",
            "High-pressure turbine blades in the AERO08 feature serpentine cooling passages and film cooling holes, enabling operation at elevated temperatures.",
            ["turbine", "cooling", "high-pressure", "film cooling"],
            1.0
        ),
        SearchDocument(
            19,
            "Fan and Nacelle Acoustic Treatments",
            "Acoustic liners in the AERO08 nacelle and fan duct reduce engine noise, improving cabin comfort and community acceptance.",
            ["acoustic", "nacelle", "fan", "noise"],
            1.0
        ),
        SearchDocument(
            20,
            "Compressor Bleed Systems",
            "Compressor bleed valves in the AERO08 manage airflow during start and transient conditions, preventing surge and supporting anti-icing.",
            ["compressor", "bleed", "surge", "anti-icing"],
            1.0
        ),
        SearchDocument(
            21,
            "FADEC Redundancy and Safety Features",
            "The AERO08 FADEC includes redundant processors and power supplies, ensuring safe engine operation even in the event of a single failure.",
            ["FADEC", "redundancy", "safety"],
            1.0
        ),
        SearchDocument(
            22,
            "Thrust Reverser Integration",
            "AERO08's thrust reverser system is integrated with the nacelle and FADEC, improving landing performance and safety.",
            ["thrust reverser", "nacelle", "FADEC"],
            1.0
        ),
        SearchDocument(
            23,
            "Foreign Object Damage Prevention Strategies",
            "The AERO08 employs inlet debris screens and regular inspection protocols to minimize the risk of foreign object damage.",
            ["FOD", "prevention", "inspection"],
            1.0
        ),
        SearchDocument(
            24,
            "Engine Cycle Tracking for LLP Management",
            "AERO08's ECM records engine cycles and usage for each life-limited part, supporting regulatory compliance and safe operation.",
            ["LLP", "cycle tracking", "ECM"],
            1.0
        ),
        SearchDocument(
            25,
            "Aerodynamic Optimization of Fan Blades",
            "The AERO08 fan blades are aerodynamically optimized for high bypass ratio, reducing noise and improving propulsive efficiency.",
            ["fan", "aerodynamics", "bypass ratio", "optimization"],
            1.0
        ),
        SearchDocument(
            26,
            "Engine Start Sequence and FADEC Control",
            "AERO08's FADEC manages the engine start sequence, controlling fuel flow, ignition, and compressor bleed to ensure reliable starts.",
            ["engine start", "FADEC", "control"],
            1.0
        ),
        SearchDocument(
            27,
            "Rotordynamics Analysis and Balancing",
            "Comprehensive rotordynamics analysis in the AERO08 ensures safe operation across the speed range, with balancing procedures minimizing vibration.",
            ["rotordynamics", "balancing", "vibration"],
            1.0
        ),
        SearchDocument(
            28,
            "Compressor Map and Surge Margin",
            "The compressor map for the AERO08 defines surge margin boundaries and guides FADEC control logic for safe operation.",
            ["compressor", "surge margin", "map"],
            1.0
        ),
        SearchDocument(
            29,
            "EGT Margin Monitoring and Engine Life",
            "Maintaining EGT margin in the AERO08 is crucial for maximizing engine life and scheduling overhauls.",
            ["EGT margin", "engine life", "monitoring"],
            1.0
        ),
        SearchDocument(
            30,
            "Nacelle Anti-Ice Systems",
            "The AERO08 nacelle features anti-ice systems using compressor bleed air to prevent ice accumulation during flight.",
            ["nacelle", "anti-ice", "bleed air"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)