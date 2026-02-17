import math
import re
import threading
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

class SearchDocument:
    def __init__(self, doc_id: str, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = doc_id
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

class SearchIndex:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.inverted_index: Dict[str, Dict[str, int]] = defaultdict(dict)  # term -> doc_id -> tf
        self.doc_freqs: Dict[str, int] = {}  # term -> df
        self.N: int = 0  # total documents
        self.lock = threading.Lock()

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                # Remove old document data before adding new
                self._remove_document(doc.id)
            tokens = self._tokenize(doc.title + " " + doc.content)
            tf_counter = Counter(tokens)
            doc_len = len(tokens)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = doc_len
            self.N += 1
            for term, tf in tf_counter.items():
                if doc.id not in self.inverted_index[term]:
                    self.inverted_index[term][doc.id] = tf
                else:
                    self.inverted_index[term][doc.id] += tf
            # Recompute document frequencies
            self._recompute_doc_freqs()
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0

    def _remove_document(self, doc_id: str):
        if doc_id not in self.documents:
            return
        # Remove doc from inverted index
        for term in list(self.inverted_index.keys()):
            if doc_id in self.inverted_index[term]:
                del self.inverted_index[term][doc_id]
                if len(self.inverted_index[term]) == 0:
                    del self.inverted_index[term]
        # Remove doc length and document
        del self.doc_lengths[doc_id]
        del self.documents[doc_id]
        self.N -= 1
        self._recompute_doc_freqs()
        self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0

    def _recompute_doc_freqs(self):
        self.doc_freqs = {term: len(doc_dict) for term, doc_dict in self.inverted_index.items()}

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            return 0.0
        return math.log(1 + (self.N - df + 0.5) / (df + 0.5))

    def _score_bm25(self, query_terms: List[str], doc_id: str) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        if doc_len == 0:
            return 0.0
        term_freqs = self.inverted_index
        for term in query_terms:
            if doc_id not in self.inverted_index.get(term, {}):
                continue
            tf = self.inverted_index[term][doc_id]
            idf = self._compute_idf(term)
            denom = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * tf * (self.k1 + 1) / denom
        # Weight boost
        weight = self.documents[doc_id].weight if doc_id in self.documents else 1.0
        return score * weight

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        with self.lock:
            query_terms = self._tokenize(query)
            if not query_terms or self.N == 0:
                return []
            candidate_docs = set()
            for term in query_terms:
                candidate_docs.update(self.inverted_index.get(term, {}).keys())
            scored_docs: List[Tuple[str, float]] = []
            for doc_id in candidate_docs:
                score = self._score_bm25(query_terms, doc_id)
                if score > 0:
                    scored_docs.append((doc_id, score))
            scored_docs.sort(key=lambda x: x[1], reverse=True)
            results = []
            for doc_id, score in scored_docs[:limit]:
                doc = self.documents[doc_id]
                snippet = self._make_snippet(doc.content, query_terms)
                results.append(SearchResult(doc_id, score, doc.title, snippet))
            return results

    def _make_snippet(self, content: str, query_terms: List[str], snippet_length: int = 160) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            start = 0
            while True:
                idx = content_lower.find(term, start)
                if idx == -1:
                    break
                positions.append(idx)
                start = idx + 1
        if not positions:
            snippet = content[:snippet_length].strip()
            if len(content) > snippet_length:
                snippet += "..."
            return snippet
        start_pos = max(min(positions) - snippet_length // 4, 0)
        end_pos = min(start_pos + snippet_length, len(content))
        snippet = content[start_pos:end_pos].strip()
        if start_pos > 0:
            snippet = "..." + snippet
        if end_pos < len(content):
            snippet += "..."
        return snippet

    def get_stats(self) -> Dict[str, int]:
        with self.lock:
            return {
                "total_documents": self.N,
                "total_terms": len(self.inverted_index),
                "average_document_length": int(self.avg_doc_length),
            }

_singleton_instance = None
_singleton_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _singleton_instance
    with _singleton_lock:
        if _singleton_instance is None:
            _singleton_instance = SearchIndex()
            _seed_documents(_singleton_instance)
        return _singleton_instance

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            "doc001",
            "Refrigeration Cycle Fundamentals",
            "The refrigeration cycle is the foundation of HVAC systems, involving compression, condensation, expansion, and evaporation phases to transfer heat effectively.",
            ["refrigeration", "fundamentals", "hvac"],
            1.2
        ),
        SearchDocument(
            "doc002",
            "Compressor Technology & Diagnosis",
            "Compressors increase refrigerant pressure and temperature. Diagnosis involves checking for abnormal noises, capacity loss, and pressure anomalies.",
            ["compressor", "diagnosis", "technology"],
            1.3
        ),
        SearchDocument(
            "doc003",
            "Condenser Design & Airflow",
            "Condensers reject heat from the refrigerant to ambient air. Proper airflow design ensures efficient heat exchange and prevents system overheating.",
            ["condenser", "design", "airflow"],
            1.1
        ),
        SearchDocument(
            "doc004",
            "Evaporator Design & Icing Prevention",
            "Evaporators absorb heat from the cabin air. Icing prevention techniques include proper airflow and defrost cycles to maintain system efficiency.",
            ["evaporator", "icing", "design"],
            1.1
        ),
        SearchDocument(
            "doc005",
            "Expansion Devices - TXV vs. Orifice Tube",
            "Thermostatic Expansion Valves (TXV) and Orifice Tubes regulate refrigerant flow differently, affecting system responsiveness and efficiency.",
            ["expansion", "txv", "orifice tube"],
            1.2
        ),
        SearchDocument(
            "doc006",
            "Receiver-Drier vs. Accumulator Function",
            "Receiver-driers store liquid refrigerant and remove moisture, while accumulators protect compressors from liquid slugging by storing excess refrigerant vapor.",
            ["receiver-drier", "accumulator", "function"],
            1.2
        ),
        SearchDocument(
            "doc007",
            "A/C System Pressure Diagnosis",
            "Pressure diagnosis involves measuring high and low side pressures to identify leaks, blockages, or compressor issues in the A/C system.",
            ["pressure", "diagnosis", "a/c system"],
            1.3
        ),
        SearchDocument(
            "doc008",
            "Refrigerant Recovery & EPA 609 Compliance",
            "Proper refrigerant recovery is essential for environmental protection and EPA 609 compliance, requiring certified equipment and procedures.",
            ["refrigerant", "recovery", "epa 609"],
            1.4
        ),
        SearchDocument(
            "doc009",
            "Cabin Air Filtration & Air Quality",
            "Cabin air filters remove dust, pollen, and pollutants, improving air quality and passenger comfort inside the vehicle.",
            ["cabin air", "filtration", "air quality"],
            1.0
        ),
        SearchDocument(
            "doc010",
            "Heater Core Operation & Diagnosis",
            "Heater cores transfer engine heat to cabin air. Diagnosis includes checking for leaks, blockages, and proper coolant flow.",
            ["heater core", "operation", "diagnosis"],
            1.1
        ),
        SearchDocument(
            "doc011",
            "Blend Door Actuators & Mode Door Control",
            "Blend door actuators control air temperature blend, while mode doors direct airflow to different vents for passenger comfort.",
            ["blend door", "actuators", "mode door"],
            1.2
        ),
        SearchDocument(
            "doc012",
            "Automatic Climate Control Systems",
            "Automatic climate control systems use sensors and actuators to maintain desired cabin temperature and humidity automatically.",
            ["automatic", "climate control", "systems"],
            1.3
        ),
        SearchDocument(
            "doc013",
            "Heat Pump Systems for Electric Vehicles",
            "Heat pumps provide efficient heating and cooling in electric vehicles by transferring heat between the cabin and ambient environment.",
            ["heat pump", "electric vehicles", "hvac"],
            1.4
        ),
        SearchDocument(
            "doc014",
            "A/C System Leak Detection Methods",
            "Leak detection methods include UV dye, electronic leak detectors, and soap bubble tests to locate refrigerant leaks in A/C systems.",
            ["leak detection", "a/c system", "methods"],
            1.3
        ),
        SearchDocument(
            "doc015",
            "Compressor Types and Their Applications",
            "Various compressor types include reciprocating, rotary, scroll, and centrifugal, each suited for different HVAC system requirements.",
            ["compressor", "types", "applications"],
            1.2
        ),
        SearchDocument(
            "doc016",
            "Refrigerant Types and Environmental Impact",
            "Different refrigerants have varying environmental impacts; newer refrigerants aim to reduce ozone depletion and global warming potential.",
            ["refrigerant", "environment", "impact"],
            1.3
        ),
        SearchDocument(
            "doc017",
            "System Charging Procedures",
            "Proper system charging ensures optimal refrigerant levels, preventing performance issues and system damage.",
            ["system charging", "procedures", "hvac"],
            1.2
        ),
        SearchDocument(
            "doc018",
            "Thermodynamics of Refrigeration",
            "Understanding thermodynamics principles is critical for analyzing refrigeration cycle efficiency and performance.",
            ["thermodynamics", "refrigeration", "principles"],
            1.1
        ),
        SearchDocument(
            "doc019",
            "Airflow Management in HVAC Systems",
            "Effective airflow management improves heat exchange and passenger comfort by optimizing duct design and fan operation.",
            ["airflow", "management", "hvac"],
            1.1
        ),
        SearchDocument(
            "doc020",
            "Diagnostics of HVAC Electrical Components",
            "Electrical diagnostics include testing switches, relays, sensors, and actuators to ensure HVAC system functionality.",
            ["diagnostics", "electrical", "hvac"],
            1.2
        ),
        SearchDocument(
            "doc021",
            "Maintenance Best Practices for HVAC Systems",
            "Regular maintenance includes filter replacement, refrigerant checks, and system cleaning to extend HVAC system life.",
            ["maintenance", "best practices", "hvac"],
            1.0
        ),
        SearchDocument(
            "doc022",
            "Impact of Ambient Conditions on HVAC Performance",
            "Ambient temperature and humidity significantly affect HVAC system efficiency and capacity.",
            ["ambient conditions", "performance", "hvac"],
            1.1
        ),
        SearchDocument(
            "doc023",
            "Heat Exchanger Materials and Corrosion",
            "Material selection for heat exchangers affects durability and resistance to corrosion in HVAC systems.",
            ["heat exchanger", "materials", "corrosion"],
            1.0
        ),
        SearchDocument(
            "doc024",
            "Sensor Technologies in Climate Control",
            "Sensors measure temperature, humidity, and pressure to enable precise climate control in modern HVAC systems.",
            ["sensor", "technology", "climate control"],
            1.2
        ),
        SearchDocument(
            "doc025",
            "Energy Efficiency in Automotive HVAC",
            "Improving energy efficiency reduces fuel consumption and emissions while maintaining cabin comfort.",
            ["energy efficiency", "automotive", "hvac"],
            1.3
        ),
        SearchDocument(
            "doc026",
            "Troubleshooting Common HVAC Faults",
            "Systematic troubleshooting helps identify and resolve common HVAC faults such as leaks, electrical failures, and mechanical wear.",
            ["troubleshooting", "faults", "hvac"],
            1.3
        ),
    ]
    for doc in docs:
        index.add_document(doc)