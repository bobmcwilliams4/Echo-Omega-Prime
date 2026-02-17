import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

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
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            tf = Counter(tokens)
            self.documents[doc.id] = doc
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.doc_freqs[term] += 1
                self.inverted_index[term].add(doc.id)
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs
            self.idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * (freq * (self.k1 + 1)) / denom
        score *= self.documents[doc_id].weight
        return score

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            tf_norm = tf[term] / doc_len if doc_len > 0 else 0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        score *= self.documents[doc_id].weight
        return score

    def _make_snippet(self, content: str, query_terms: List[str], maxlen: int = 160) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = ' '.join(tokens[:maxlen])
            return snippet[:maxlen] + ('...' if len(snippet) > maxlen else '')
        start = max(positions[0] - 10, 0)
        end = min(start + 30, len(tokens))
        snippet = ' '.join(tokens[start:end])
        for term in set(query_terms):
            snippet = re.sub(r'\b({})\b'.format(re.escape(term)), r'*\1*', snippet, flags=re.IGNORECASE)
        return snippet[:maxlen] + ('...' if len(snippet) > maxlen else '')

    def search(self, query: str, limit: int = 10, method: str = 'bm25') -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, set()))
        scored: List[Tuple[int, float]] = []
        for doc_id in candidate_docs:
            if method == 'bm25':
                score = self._score_bm25(query_terms, doc_id)
            else:
                score = self._score_tfidf(query_terms, doc_id)
            if score > 0:
                scored.append((doc_id, score))
        scored.sort(key=lambda x: -x[1])
        results = []
        for doc_id, score in scored[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, int]:
        return {
            'documents': self.total_docs,
            'unique_terms': len(self.doc_freqs),
            'avg_doc_length': int(self.avg_doc_length),
        }

# Singleton factory for SearchIndex
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            idx = SearchIndex()
            _seed_documents(idx)
            _search_index_instance = idx
        return _search_index_instance

def _seed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Reciprocating Compressor Clearance Volume",
            "Clearance volume is the space remaining in the cylinder of a reciprocating compressor when the piston is at the end of its stroke. It affects volumetric efficiency and capacity. Proper calculation and minimization of clearance volume are crucial for optimal compressor performance.",
            ["reciprocating", "clearance_volume", "capacity"],
            1.0
        ),
        SearchDocument(
            2,
            "Centrifugal Compressor Surge Control",
            "Surge is an unstable operating condition in centrifugal compressors. Surge control systems use recycle valves, anti-surge controllers, and instrumentation to maintain safe operation. Proper surge control prevents damage and ensures reliability.",
            ["centrifugal", "surge_control", "safety"],
            1.0
        ),
        SearchDocument(
            3,
            "Polytropic vs Isentropic Efficiency in Compressors",
            "Polytropic efficiency considers real gas behavior and is used for performance evaluation of compressors. Isentropic efficiency assumes ideal reversible processes. Understanding the difference is essential for accurate compressor analysis.",
            ["efficiency", "polytropic", "isentropic"],
            1.0
        ),
        SearchDocument(
            4,
            "Rod Load Analysis in Reciprocating Compressors",
            "Rod load is the net force transmitted through the compressor piston rod. Accurate rod load analysis ensures mechanical integrity and prevents failures. It involves gas, inertia, and friction forces.",
            ["reciprocating", "rod_load", "mechanical"],
            1.0
        ),
        SearchDocument(
            5,
            "Benefits of Intercooling in Multistage Compression",
            "Intercooling between compression stages reduces gas temperature, improves efficiency, and decreases power consumption. Proper intercooler design is important for multistage compressors.",
            ["intercooling", "multistage", "efficiency"],
            1.0
        ),
        SearchDocument(
            6,
            "Gas Properties Affecting Compression Performance",
            "Gas molecular weight, specific heat ratio, and compressibility factor influence compressor selection and performance. Accurate gas analysis is required for reliable operation.",
            ["gas_properties", "compression", "performance"],
            1.0
        ),
        SearchDocument(
            7,
            "Compressor Valve Design and Maintenance",
            "Valves are critical for reciprocating compressor reliability. Proper design, material selection, and regular maintenance reduce downtime and extend valve life.",
            ["valve", "design", "maintenance", "reciprocating"],
            1.0
        ),
        SearchDocument(
            8,
            "Packing and Rider Ring Wear Mechanisms",
            "Packing and rider rings prevent gas leakage and support the piston. Wear mechanisms include abrasion, heat, and chemical attack. Monitoring and timely replacement are essential.",
            ["packing", "rider_ring", "wear", "maintenance"],
            1.0
        ),
        SearchDocument(
            9,
            "API 618 Reciprocating Compressor Standards Compliance",
            "API 618 provides design and testing standards for reciprocating compressors in the oil and gas industry. Compliance ensures safety, reliability, and interchangeability.",
            ["api_618", "reciprocating", "standards"],
            1.0
        ),
        SearchDocument(
            10,
            "API 617 Centrifugal Compressor Standards Compliance",
            "API 617 covers centrifugal and axial compressor standards. It specifies requirements for design, materials, and testing to ensure high reliability.",
            ["api_617", "centrifugal", "standards"],
            1.0
        ),
        SearchDocument(
            11,
            "Capacity Control Methods Comparison",
            "Capacity control in compressors can be achieved through speed variation, suction throttling, clearance pockets, or bypass. The selection depends on process requirements and compressor type.",
            ["capacity_control", "comparison", "methods"],
            1.0
        ),
        SearchDocument(
            12,
            "Vibration Monitoring per API 670",
            "API 670 outlines vibration monitoring and protection systems for compressors. Continuous monitoring helps detect faults early and prevent catastrophic failures.",
            ["vibration", "monitoring", "api_670"],
            1.0
        ),
        SearchDocument(
            13,
            "Screw Compressor Applications and Limitations",
            "Screw compressors are suitable for moderate pressure and continuous duty applications. Limitations include lower efficiency at high pressure ratios and sensitivity to liquid carryover.",
            ["screw_compressor", "applications", "limitations"],
            1.0
        ),
        SearchDocument(
            14,
            "Compression Ratio Calculation in Multistage Compressors",
            "The overall compression ratio is divided among stages to minimize discharge temperature and power. Proper calculation ensures efficient operation and equipment longevity.",
            ["compression_ratio", "multistage", "calculation"],
            1.0
        ),
        SearchDocument(
            15,
            "Field Gas Compression for Gas Lift Operations",
            "Compressors are used to inject gas into wells for artificial lift. Field gas compression systems must handle variable flows and compositions typical of oilfield operations.",
            ["field_gas", "compression", "gas_lift"],
            1.0
        ),
        SearchDocument(
            16,
            "Gas Dehydration Before Compression",
            "Removing water vapor from gas before compression prevents hydrate formation and corrosion. Common methods include glycol dehydration and molecular sieves.",
            ["gas_dehydration", "compression", "corrosion"],
            1.0
        ),
        SearchDocument(
            17,
            "Compressor Driver Selection: Engine, Motor, or Turbine",
            "Compressor drivers include electric motors, gas engines, and turbines. Selection depends on site conditions, power requirements, and operational flexibility.",
            ["driver_selection", "engine", "motor", "turbine"],
            1.0
        ),
        SearchDocument(
            18,
            "Compressor Station Design and Layout",
            "Station design considers equipment arrangement, safety distances, maintenance access, and noise control. Proper layout improves reliability and reduces operational risks.",
            ["station_design", "layout", "safety"],
            1.0
        ),
        SearchDocument(
            19,
            "NGL Recovery: Compression and Refrigeration",
            "Natural Gas Liquids (NGL) recovery uses compression and refrigeration to condense heavier hydrocarbons. Efficient integration of compressors is critical for plant economics.",
            ["ngl_recovery", "compression", "refrigeration"],
            1.0
        ),
        SearchDocument(
            20,
            "Gas Gathering Compression Systems",
            "Gas gathering systems use compressors to collect low-pressure gas from multiple wells. Design challenges include fluctuating flows and remote operation.",
            ["gas_gathering", "compression", "systems"],
            1.0
        ),
        SearchDocument(
            21,
            "Reciprocating Compressor Unloading Methods",
            "Unloading methods such as clearance pockets and suction valve unloaders allow reciprocating compressors to operate at reduced capacity. Proper selection improves efficiency.",
            ["reciprocating", "unloading", "capacity_control"],
            1.0
        ),
        SearchDocument(
            22,
            "Centrifugal Compressor Performance Curves",
            "Performance curves show the relationship between flow, head, and efficiency. Understanding these curves is essential for proper compressor selection and operation.",
            ["centrifugal", "performance", "curves"],
            1.0
        ),
        SearchDocument(
            23,
            "Reciprocating Compressor Pulsation and Vibration Control",
            "Pulsation bottles and dampeners are used to control pressure pulsations. Proper design minimizes vibration and extends equipment life.",
            ["reciprocating", "pulsation", "vibration"],
            1.0
        ),
        SearchDocument(
            24,
            "Lubrication Systems for Compressors",
            "Adequate lubrication reduces wear and prevents overheating in compressor bearings and cylinders. System design must ensure reliable oil delivery under all conditions.",
            ["lubrication", "systems", "maintenance"],
            1.0
        ),
        SearchDocument(
            25,
            "Condition Monitoring Techniques for Compressors",
            "Techniques include vibration analysis, thermography, and oil analysis. Early detection of faults reduces downtime and maintenance costs.",
            ["condition_monitoring", "vibration", "maintenance"],
            1.0
        ),
        SearchDocument(
            26,
            "Reciprocating Compressor Efficiency Improvement Strategies",
            "Efficiency can be improved by minimizing clearance volume, optimizing valve design, and maintaining proper lubrication. Regular monitoring is essential.",
            ["reciprocating", "efficiency", "improvement"],
            1.0
        ),
        SearchDocument(
            27,
            "Centrifugal Compressor Anti-Surge Valve Sizing",
            "Proper sizing of anti-surge valves is critical for effective surge control. Valve response time and capacity must match compressor dynamics.",
            ["centrifugal", "anti_surge", "valve"],
            1.0
        ),
        SearchDocument(
            28,
            "Reciprocating Compressor Cylinder Materials",
            "Cylinder material selection affects compressor durability and suitability for corrosive or high-pressure gases. Common materials include cast iron and alloy steels.",
            ["reciprocating", "cylinder", "materials"],
            1.0
        ),
        SearchDocument(
            29,
            "Centrifugal Compressor Impeller Design",
            "Impeller design influences compressor efficiency, surge margin, and operating range. Computational tools aid in optimizing impeller geometry.",
            ["centrifugal", "impeller", "design"],
            1.0
        ),
        SearchDocument(
            30,
            "Reciprocating Compressor Start-Up and Shutdown Procedures",
            "Proper start-up and shutdown procedures prevent mechanical shock and ensure safety. Steps include pre-lubrication, venting, and gradual pressurization.",
            ["reciprocating", "start_up", "shutdown"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)