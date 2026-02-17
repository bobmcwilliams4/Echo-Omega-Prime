import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

# --- Data Classes ---

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

# --- Search Index ---

class SearchIndex:
    def __init__(self, bm25_k1: float = 1.5, bm25_b: float = 0.75):
        self._documents: Dict[int, SearchDocument] = {}
        self._doc_tokens: Dict[int, List[str]] = {}
        self._inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self._term_freqs: Dict[int, Counter] = {}
        self._doc_lengths: Dict[int, int] = {}
        self._bm25_k1 = bm25_k1
        self._bm25_b = bm25_b
        self._avg_doc_len = 0.0
        self._lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._corpus_size = 0

    def add_document(self, doc: SearchDocument):
        with self._lock:
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            self._documents[doc.id] = doc
            self._doc_tokens[doc.id] = tokens
            tf = Counter(tokens)
            self._term_freqs[doc.id] = tf
            self._doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self._inverted_index[term].add(doc.id)
            self._corpus_size = len(self._documents)
            self._avg_doc_len = sum(self._doc_lengths.values()) / self._corpus_size if self._corpus_size else 0.0
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
        candidate_docs = set()
        for term in query_tokens:
            candidate_docs.update(self._inverted_index.get(term, set()))
        scored_results: List[Tuple[int, float]] = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_tokens)
            tfidf_score = self._score_tfidf(doc_id, query_tokens)
            doc = self._documents[doc_id]
            # Combine scores: BM25 (0.7), TF-IDF (0.3), weighted by doc.weight
            score = (0.7 * bm25_score + 0.3 * tfidf_score) * doc.weight
            scored_results.append((doc_id, score))
        scored_results.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored_results[:limit]:
            doc = self._documents[doc_id]
            snippet = self._make_snippet(doc, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                "documents": len(self._documents),
                "avg_doc_length": self._avg_doc_len,
                "unique_terms": len(self._inverted_index),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = len(self._inverted_index.get(term, []))
        N = self._corpus_size
        # BM25 IDF with +0.5 smoothing
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_tokens: List[str]) -> float:
        tf = self._term_freqs[doc_id]
        doc_len = self._doc_lengths[doc_id]
        score = 0.0
        for term in set(query_tokens):
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / (self._avg_doc_len or 1))
            score += idf * (freq * (self._bm25_k1 + 1)) / (denom or 1)
        return score

    def _score_tfidf(self, doc_id: int, query_tokens: List[str]) -> float:
        tf = self._term_freqs[doc_id]
        doc_len = self._doc_lengths[doc_id]
        score = 0.0
        for term in set(query_tokens):
            if term not in tf:
                continue
            tf_norm = tf[term] / (doc_len or 1)
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], window: int = 24) -> str:
        content = doc.content
        content_tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(content_tokens) if t in query_tokens]
        if not positions:
            return content[:160] + ("..." if len(content) > 160 else "")
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(content_tokens))
        snippet_tokens = content_tokens[start:end]
        snippet = " ".join(snippet_tokens)
        # Highlight query terms
        for qt in set(query_tokens):
            snippet = re.sub(r'\b({})\b'.format(re.escape(qt)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + ("..." if end < len(content_tokens) else "")

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

# --- Pre-seed Documents ---

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Diesel-Electric Prime Mover Integration",
            "The diesel engine (prime mover) in a locomotive is coupled to the main alternator, converting mechanical energy into electrical energy for traction motors. Integration ensures optimal power delivery and fuel efficiency.",
            ["prime mover", "alternator", "integration"],
            1.0
        ),
        SearchDocument(
            2,
            "DC Series Traction Motors",
            "DC series traction motors are widely used in older locomotives due to their high starting torque and simple control via series-parallel connections and field weakening.",
            ["traction motor", "dc series", "torque"],
            1.0
        ),
        SearchDocument(
            3,
            "AC Induction Traction Motors",
            "Modern locomotives employ AC induction motors for improved efficiency, reduced maintenance, and compatibility with advanced inverter control systems.",
            ["traction motor", "ac induction", "efficiency"],
            1.0
        ),
        SearchDocument(
            4,
            "Inverter and Rectifier Systems",
            "Inverters convert DC from the main alternator to variable-frequency AC for traction motors. Rectifiers convert AC to DC for auxiliary systems. Both are key in power electronics integration.",
            ["inverter", "rectifier", "power electronics"],
            1.0
        ),
        SearchDocument(
            5,
            "Chopper Control in Locomotives",
            "Chopper systems regulate voltage to DC traction motors by rapidly switching the supply, enabling smooth acceleration and improved energy efficiency.",
            ["chopper", "dc motor", "acceleration"],
            1.0
        ),
        SearchDocument(
            6,
            "Dynamic Braking: Resistive Systems",
            "Resistive dynamic braking dissipates kinetic energy as heat in resistor grids, reducing wear on friction brakes and improving train handling on downgrades.",
            ["dynamic braking", "resistive", "brake grid"],
            1.0
        ),
        SearchDocument(
            7,
            "Dynamic Braking: Regenerative Systems",
            "Regenerative dynamic braking returns energy to the power supply or grid, increasing overall energy efficiency in electrified rail systems.",
            ["dynamic braking", "regenerative", "energy recovery"],
            1.0
        ),
        SearchDocument(
            8,
            "Davis Equation for Train Resistance",
            "The Davis Equation models train resistance as a function of rolling, bearing, and aerodynamic drag, plus grade effects. Accurate resistance calculation is crucial for tractive effort estimation.",
            ["davis equation", "train resistance", "grade"],
            1.0
        ),
        SearchDocument(
            9,
            "Tractive Effort and Adhesion",
            "Tractive effort is limited by wheel-rail adhesion, which depends on rail conditions, locomotive weight, and wheel slip detection systems.",
            ["tractive effort", "adhesion", "wheel slip"],
            1.0
        ),
        SearchDocument(
            10,
            "Locomotive Consist and MU Operation",
            "Multiple Unit (MU) operation allows several locomotives to be controlled from a single cab, forming a consist. Proper consist management optimizes power and braking.",
            ["consist", "mu operation", "multiple unit"],
            1.0
        ),
        SearchDocument(
            11,
            "Distributed Power Control",
            "Distributed power involves remote control of locomotives placed throughout the train, reducing in-train forces and improving handling on long consists.",
            ["distributed power", "remote control", "train handling"],
            1.0
        ),
        SearchDocument(
            12,
            "Fuel Efficiency and Throttle Notch Management",
            "Locomotive throttle notches (1-8) control engine output. Efficient notch management and load control reduce fuel consumption and emissions.",
            ["fuel efficiency", "notch", "throttle"],
            1.0
        ),
        SearchDocument(
            13,
            "EMD Locomotive Model Specifications",
            "EMD locomotives, such as the SD70ACe, feature AC traction, microprocessor controls, and Tier 4 emissions compliance. Model specs include horsepower, weight, and tractive effort.",
            ["emd", "specifications", "sd70ace"],
            1.0
        ),
        SearchDocument(
            14,
            "GE Locomotive Model Specifications",
            "GE Evolution Series locomotives use AC traction, advanced cooling, and meet Tier 4 standards. Key models include ES44AC and ET44AC.",
            ["ge", "specifications", "evolution series"],
            1.0
        ),
        SearchDocument(
            15,
            "EPA Tier 4 Emissions Standards",
            "Tier 4 standards set strict limits on NOx and particulate emissions from new locomotives, requiring advanced aftertreatment and engine technologies.",
            ["epa", "tier 4", "emissions"],
            1.0
        ),
        SearchDocument(
            16,
            "Head End Power (HEP) and Hotel Load",
            "HEP supplies electricity for passenger car lighting, HVAC, and hotel loads. Modern locomotives use dedicated alternators or inverters for HEP.",
            ["hep", "hotel load", "passenger"],
            1.0
        ),
        SearchDocument(
            17,
            "Locomotive Maintenance Practices",
            "Routine maintenance includes engine inspections, air brake testing, and FRA 49 CFR 229 compliance checks to ensure safety and reliability.",
            ["maintenance", "fra", "inspection"],
            1.0
        ),
        SearchDocument(
            18,
            "Positive Train Control (PTC) Implementation",
            "PTC is a safety overlay system that prevents train-to-train collisions, overspeed derailments, and unauthorized movements using GPS, wireless, and onboard computers.",
            ["ptc", "positive train control", "safety"],
            1.0
        ),
        SearchDocument(
            19,
            "Locomotive Event Recorder and Data Management",
            "Event recorders log operational data such as speed, throttle position, and brake applications for incident investigation and performance analysis.",
            ["event recorder", "data", "logging"],
            1.0
        ),
        SearchDocument(
            20,
            "Wheel Slip Detection and Adhesion Control",
            "Wheel slip detection systems monitor axle speeds and adjust traction power to maximize adhesion, especially during acceleration or on slippery rails.",
            ["wheel slip", "adhesion", "traction control"],
            1.0
        ),
        SearchDocument(
            21,
            "Air Brake Systems: Independent and Automatic",
            "Locomotives use independent and automatic air brakes for train and locomotive control. Proper operation ensures safe train handling and stopping.",
            ["air brake", "independent", "automatic"],
            1.0
        ),
        SearchDocument(
            22,
            "Draft Gear and Coupler Buff Forces",
            "Draft gear absorbs buff and draft forces between railcars, reducing damage and improving train handling during acceleration and braking.",
            ["draft gear", "coupler", "buff force"],
            1.0
        ),
        SearchDocument(
            23,
            "Locomotive Remote Control and Belt Pack Operation",
            "Remote control systems, including belt packs, allow ground personnel to operate locomotives for switching and yard movements, enhancing safety and efficiency.",
            ["remote control", "belt pack", "yard"],
            1.0
        ),
        SearchDocument(
            24,
            "Crankcase Ventilation, Turbocharging, and Aftercooling",
            "Modern diesel engines use crankcase ventilation to reduce emissions, turbochargers for increased power, and aftercoolers to lower intake air temperature.",
            ["crankcase", "turbocharging", "aftercooling"],
            1.0
        ),
        SearchDocument(
            25,
            "Locomotive Cooling System and Radiator Fan Control",
            "Efficient cooling systems and variable-speed radiator fans maintain optimal engine temperature, improving reliability and reducing fuel consumption.",
            ["cooling system", "radiator", "fan control"],
            1.0
        ),
        SearchDocument(
            26,
            "Locomotive Air Compressor Operation",
            "Air compressors supply compressed air for brake systems and auxiliary equipment. Maintenance includes checking for leaks and proper lubrication.",
            ["air compressor", "brake", "auxiliary"],
            1.0
        ),
        SearchDocument(
            27,
            "Microprocessor Controls in Locomotives",
            "Microprocessor-based controls manage engine functions, traction power, diagnostics, and communication with PTC and event recorders.",
            ["microprocessor", "controls", "diagnostics"],
            1.0
        ),
        SearchDocument(
            28,
            "Locomotive Sanding Systems",
            "Sanding systems deposit sand on rails to improve adhesion during low-traction conditions, reducing wheel slip and enhancing tractive effort.",
            ["sanding", "adhesion", "wheel slip"],
            1.0
        ),
        SearchDocument(
            29,
            "Locomotive Horn, Bell, and Safety Appliances",
            "Safety appliances such as horns, bells, and lights are required for compliance with FRA regulations and safe train operation.",
            ["horn", "bell", "safety"],
            1.0
        ),
        SearchDocument(
            30,
            "Locomotive Battery and Starting Systems",
            "Batteries provide power for engine starting, control circuits, and emergency lighting. Regular testing ensures reliable operation.",
            ["battery", "starting", "emergency"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)