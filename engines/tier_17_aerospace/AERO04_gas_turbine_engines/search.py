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
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.total_terms: int = 0
        self.lock = threading.Lock()
        self.avg_doc_length: float = 0.0
        self.k1 = 1.5
        self.b = 0.75
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = {}
        self._preseeded = False

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9_]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_terms += len(tokens)
            tf_counter = Counter(tokens)
            self.term_freqs[doc.id] = tf_counter
            for term in tf_counter:
                self.term_doc_freqs[term] += 1
            self._idf_cache.clear()
            self._tfidf_cache.clear()
            self.avg_doc_length = (
                sum(self.doc_lengths.values()) / len(self.doc_lengths)
                if self.doc_lengths else 0.0
            )

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        N = len(self.documents)
        n_q = self.term_doc_freqs.get(term, 0)
        idf = math.log(1 + (N - n_q + 0.5) / (n_q + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        tf_counter = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            idf = self._compute_idf(term)
            tf = tf_counter.get(term, 0)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            if denominator == 0:
                continue
            score += idf * numerator / denominator
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        if doc_id in self._tfidf_cache:
            tfidf_vec = self._tfidf_cache[doc_id]
        else:
            tf_counter = self.term_freqs[doc_id]
            doc_len = self.doc_lengths[doc_id]
            tfidf_vec = {}
            for term in tf_counter:
                tf = tf_counter[term] / doc_len
                idf = self._compute_idf(term)
                tfidf_vec[term] = tf * idf
            self._tfidf_cache[doc_id] = tfidf_vec
        score = 0.0
        for term in query_terms:
            score += tfidf_vec.get(term, 0.0)
        return score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scores = []
        for doc_id in self.documents:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                snippet = self._make_snippet(doc_id, query_terms)
                result = SearchResult(doc_id, score, self.documents[doc_id].title, snippet)
                scores.append(result)
        scores.sort(key=lambda r: r.score, reverse=True)
        return scores[:limit]

    def _make_snippet(self, doc_id: int, query_terms: List[str], max_len: int = 160) -> str:
        content = self.documents[doc_id].content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:max_len]
        else:
            start = max(positions[0] - 10, 0)
            end = min(start + 40, len(tokens))
            snippet_tokens = tokens[start:end]
            snippet = ' '.join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(r'\b({})\b'.format(re.escape(term)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet[:max_len] + ('...' if len(snippet) > max_len else '')

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                'num_documents': len(self.documents),
                'avg_doc_length': self.avg_doc_length,
                'total_terms': self.total_terms,
                'num_unique_terms': len(self.term_doc_freqs),
            }

# Singleton factory
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
    if getattr(index, '_preseeded', False):
        return
    docs = [
        SearchDocument(
            1,
            "Brayton Cycle Overview",
            "The Brayton cycle is the fundamental thermodynamic cycle for gas turbine engines, including the AERO04. It consists of four processes: compression, heat addition, expansion, and heat rejection.",
            ["brayton_cycle", "thermodynamics", "overview"],
            1.0
        ),
        SearchDocument(
            2,
            "Axial Compressor Fundamentals",
            "Axial compressors are used in the AERO04 engine to increase air pressure before combustion. They consist of multiple stages of rotating and stationary blades.",
            ["axial_compressor", "design", "fundamentals"],
            1.0
        ),
        SearchDocument(
            3,
            "Compressor Stage Efficiency",
            "The efficiency of each compressor stage in the AERO04 is determined by blade profile, tip clearance, and flow velocity. High efficiency reduces fuel consumption.",
            ["axial_compressor", "efficiency", "stage"],
            1.0
        ),
        SearchDocument(
            4,
            "Thermodynamic Properties of Air",
            "Air properties such as specific heat, gas constant, and ratio of specific heats are critical for Brayton cycle calculations in AERO04 engines.",
            ["thermodynamics", "air_properties"],
            1.0
        ),
        SearchDocument(
            5,
            "Pressure Ratio in Gas Turbines",
            "Pressure ratio is a key design parameter for the AERO04 gas turbine. Higher ratios improve thermal efficiency but increase mechanical stress.",
            ["pressure_ratio", "gas_turbine", "design"],
            1.0
        ),
        SearchDocument(
            6,
            "Combustion Chamber Design",
            "The combustion chamber in the AERO04 engine must ensure efficient mixing of fuel and air, stable flame, and minimal pressure loss.",
            ["combustion", "chamber", "design"],
            1.0
        ),
        SearchDocument(
            7,
            "Turbine Blade Cooling",
            "AERO04 turbine blades are cooled using advanced techniques such as film cooling and internal air passages to withstand high temperatures.",
            ["turbine", "blade", "cooling"],
            1.0
        ),
        SearchDocument(
            8,
            "Thermal Efficiency Calculation",
            "Thermal efficiency of the Brayton cycle is calculated using the pressure ratio and specific heat ratio. AERO04 achieves high efficiency through optimized design.",
            ["brayton_cycle", "thermal_efficiency"],
            1.0
        ),
        SearchDocument(
            9,
            "Compressor Surge and Stall",
            "Surge and stall are undesirable phenomena in axial compressors. The AERO04 design minimizes these by careful blade geometry and control systems.",
            ["axial_compressor", "surge", "stall"],
            1.0
        ),
        SearchDocument(
            10,
            "Gas Turbine Materials",
            "Materials used in AERO04 gas turbines must withstand high temperatures and stresses. Nickel-based superalloys are commonly used.",
            ["gas_turbine", "materials", "superalloys"],
            1.0
        ),
        SearchDocument(
            11,
            "Compressor Map Interpretation",
            "Compressor maps show the relationship between pressure ratio, mass flow, and efficiency. AERO04 uses these maps for performance tuning.",
            ["axial_compressor", "map", "performance"],
            1.0
        ),
        SearchDocument(
            12,
            "Blade Aerodynamics",
            "Aerodynamic design of compressor and turbine blades in AERO04 is crucial for maximizing efficiency and minimizing losses.",
            ["blade", "aerodynamics", "design"],
            1.0
        ),
        SearchDocument(
            13,
            "Gas Turbine Cycle Simulation",
            "Simulation tools are used to model the Brayton cycle in AERO04 engines, predicting performance under various operating conditions.",
            ["brayton_cycle", "simulation", "performance"],
            1.0
        ),
        SearchDocument(
            14,
            "Compressor Flow Stability",
            "Stable flow in the axial compressor is achieved by proper blade spacing and angle. AERO04 incorporates variable stator vanes for control.",
            ["axial_compressor", "flow", "stability"],
            1.0
        ),
        SearchDocument(
            15,
            "Fuel Injection Techniques",
            "AERO04 uses advanced fuel injection methods to ensure uniform combustion and reduce emissions.",
            ["combustion", "fuel_injection", "emissions"],
            1.0
        ),
        SearchDocument(
            16,
            "Turbine Expansion Process",
            "Expansion of hot gases in the turbine produces mechanical work. AERO04 turbines are optimized for maximum energy extraction.",
            ["turbine", "expansion", "energy"],
            1.0
        ),
        SearchDocument(
            17,
            "Compressor Blade Materials",
            "Compressor blades in AERO04 are made from titanium alloys for high strength and low weight.",
            ["axial_compressor", "blade", "materials"],
            1.0
        ),
        SearchDocument(
            18,
            "Cycle Pressure Losses",
            "Pressure losses occur in the compressor, combustor, and turbine. Minimizing these losses is key to AERO04 efficiency.",
            ["brayton_cycle", "pressure_loss", "efficiency"],
            1.0
        ),
        SearchDocument(
            19,
            "Gas Turbine Control Systems",
            "AERO04 engines use electronic control systems to manage fuel flow, compressor speed, and turbine temperature.",
            ["gas_turbine", "control", "systems"],
            1.0
        ),
        SearchDocument(
            20,
            "Compressor Stage Matching",
            "Matching the flow and pressure across compressor stages is critical for AERO04 performance and reliability.",
            ["axial_compressor", "stage", "matching"],
            1.0
        ),
        SearchDocument(
            21,
            "Brayton Cycle Regeneration",
            "Regenerative heat exchangers in AERO04 recover exhaust heat to preheat incoming air, improving cycle efficiency.",
            ["brayton_cycle", "regeneration", "heat_exchanger"],
            1.0
        ),
        SearchDocument(
            22,
            "Turbine Stage Efficiency",
            "Turbine stage efficiency in AERO04 is maximized by optimizing blade shape and cooling methods.",
            ["turbine", "stage", "efficiency"],
            1.0
        ),
        SearchDocument(
            23,
            "Compressor Blade Profile Design",
            "Blade profile design in AERO04 axial compressors affects flow stability and efficiency. Computational tools are used for optimization.",
            ["axial_compressor", "blade", "profile"],
            1.0
        ),
        SearchDocument(
            24,
            "Combustor Pressure Drop",
            "Pressure drop in the combustor must be minimized to maintain AERO04 engine efficiency. Design focuses on flow uniformity.",
            ["combustion", "pressure_drop", "design"],
            1.0
        ),
        SearchDocument(
            25,
            "Gas Turbine Exhaust Emissions",
            "AERO04 engines are designed to minimize NOx and CO emissions through advanced combustion techniques.",
            ["gas_turbine", "exhaust", "emissions"],
            1.0
        ),
        SearchDocument(
            26,
            "Axial Compressor Stage Number",
            "The number of stages in the AERO04 axial compressor is chosen based on desired pressure ratio and efficiency.",
            ["axial_compressor", "stage", "number"],
            1.0
        ),
        SearchDocument(
            27,
            "Cycle Heat Addition",
            "Heat addition in the Brayton cycle occurs in the combustor. AERO04 optimizes this process for maximum thermal efficiency.",
            ["brayton_cycle", "heat_addition", "combustion"],
            1.0
        ),
        SearchDocument(
            28,
            "Compressor Tip Clearance",
            "Tip clearance in AERO04 compressors is minimized to reduce leakage and improve efficiency.",
            ["axial_compressor", "tip_clearance", "efficiency"],
            1.0
        ),
        SearchDocument(
            29,
            "Turbine Exhaust Temperature",
            "Exhaust temperature is monitored in AERO04 turbines to prevent overheating and ensure safe operation.",
            ["turbine", "exhaust", "temperature"],
            1.0
        ),
        SearchDocument(
            30,
            "Compressor Blade Vibration",
            "Vibration analysis is performed on AERO04 compressor blades to prevent fatigue and failure.",
            ["axial_compressor", "blade", "vibration"],
            1.0
        ),
        SearchDocument(
            31,
            "Brayton Cycle Applications",
            "The Brayton cycle is used in AERO04 for aircraft propulsion and power generation.",
            ["brayton_cycle", "applications"],
            1.0
        ),
        SearchDocument(
            32,
            "Gas Turbine Startup Procedures",
            "AERO04 startup involves sequential activation of compressor, combustor, and turbine stages, monitored by control systems.",
            ["gas_turbine", "startup", "procedures"],
            1.0
        ),
        SearchDocument(
            33,
            "Compressor Blade Angle Optimization",
            "Blade angle in AERO04 compressors is optimized for maximum pressure rise and minimal losses.",
            ["axial_compressor", "blade", "angle"],
            1.0
        ),
        SearchDocument(
            34,
            "Cycle Work Output",
            "Work output in the Brayton cycle is calculated from enthalpy differences across turbine and compressor stages.",
            ["brayton_cycle", "work_output"],
            1.0
        ),
        SearchDocument(
            35,
            "Combustor Flame Stability",
            "Flame stability in AERO04 combustors is achieved by controlling air-fuel ratio and flow patterns.",
            ["combustion", "flame_stability"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)
    index._preseeded = True