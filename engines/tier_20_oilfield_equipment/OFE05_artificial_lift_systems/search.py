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
        self.inverted_index: Dict[str, List[Tuple[int, int]]] = defaultdict(list)
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.total_terms = 0
        self.lock = threading.Lock()
        self.avg_doc_length = 0.0
        self.k1 = 1.5
        self.b = 0.75
        self.idf_cache: Dict[str, float] = {}
        self.tf_cache: Dict[Tuple[int, str], float] = {}
        self._initialized = False

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            term_counts = Counter(tokens)
            doc_length = len(tokens)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = doc_length
            self.total_terms += doc_length
            for term, freq in term_counts.items():
                self.inverted_index[term].append((doc.id, freq))
                self.term_doc_freq[term] += 1
                self.tf_cache[(doc.id, term)] = freq / doc_length
            self.avg_doc_length = self.total_terms / len(self.documents)
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[int, float] = defaultdict(float)
        for term in query_terms:
            idf = self._compute_idf(term)
            postings = self.inverted_index.get(term, [])
            for doc_id, freq in postings:
                doc = self.documents[doc_id]
                score = self._score_bm25(doc_id, term, freq, idf, doc.weight)
                doc_scores[doc_id] += score
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "num_documents": len(self.documents),
                "avg_doc_length": self.avg_doc_length,
                "total_terms": self.total_terms,
                "unique_terms": len(self.inverted_index)
            }

    def _tokenize(self, text: str) -> List[str]:
        return [t for t in re.findall(r'\b\w+\b', text.lower()) if len(t) > 1]

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        N = len(self.documents)
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, term: str, freq: int, idf: float, weight: float) -> float:
        doc_length = self.doc_lengths[doc_id]
        avgdl = self.avg_doc_length if self.avg_doc_length > 0 else 1
        tf = freq
        denom = tf + self.k1 * (1 - self.b + self.b * doc_length / avgdl)
        bm25 = idf * ((tf * (self.k1 + 1)) / (denom + 1e-10))
        # TF-IDF normalization
        tfidf = (freq / doc_length) * idf
        return (bm25 * 0.7 + tfidf * 0.3) * weight

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:window]) + ('...' if len(tokens) > window else '')
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet = tokens[start:end]
        return ' '.join(snippet) + ('...' if end < len(tokens) else '')

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    if _search_index_instance is None:
        with _search_index_lock:
            if _search_index_instance is None:
                idx = SearchIndex()
                _preseed_documents(idx)
                _search_index_instance = idx
    return _search_index_instance

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Beam Pump Selection Criteria",
            "Beam pump selection involves evaluating well depth, fluid production rate, tubing size, and pump size. Considerations include rod string design, prime mover capacity, and expected production optimization.",
            ["beam pump", "selection", "sizing", "rod string", "prime mover"],
            1.0
        ),
        SearchDocument(
            2,
            "Beam Pump Sizing Methodology",
            "Proper sizing of beam pumps ensures efficient artificial lift. Calculate required pump displacement, select suitable plunger size, and match stroke length and speed to reservoir inflow.",
            ["beam pump", "sizing", "displacement", "stroke length", "artificial lift"],
            1.0
        ),
        SearchDocument(
            3,
            "Dynamometer Card Interpretation",
            "Dynamometer cards are used to analyze downhole pump performance. Surface and pump cards reveal issues such as gas interference, fluid pound, and rod string problems.",
            ["dynamometer", "card analysis", "pump performance", "rod string"],
            1.0
        ),
        SearchDocument(
            4,
            "ESP Selection Guidelines",
            "ESP selection requires matching pump capacity to well inflow, considering fluid properties, gas content, and required lift. Motor cooling and shrouding are critical for reliability.",
            ["esp", "selection", "motor cooling", "shrouding", "lift"],
            1.0
        ),
        SearchDocument(
            5,
            "ESP Sizing Calculations",
            "Sizing an ESP involves determining the total dynamic head, selecting appropriate pump stages, and ensuring motor and seal compatibility with well conditions.",
            ["esp", "sizing", "dynamic head", "pump stages", "motor"],
            1.0
        ),
        SearchDocument(
            6,
            "ESP Failure Analysis Techniques",
            "Common ESP failures include motor overheating, gas lock, scale deposition, and seal failures. Root cause analysis uses run data, failure patterns, and component inspection.",
            ["esp", "failure analysis", "motor", "gas lock", "scale"],
            1.0
        ),
        SearchDocument(
            7,
            "Gas Lift Valve Spacing and Design",
            "Gas lift valve spacing is determined by well depth, injection pressure, and unloading sequence. Proper design ensures efficient gas utilization and stable lift operations.",
            ["gas lift", "valve spacing", "design", "injection pressure"],
            1.0
        ),
        SearchDocument(
            8,
            "Progressive Cavity Pump (PCP) Applications",
            "PCPs are suitable for handling viscous fluids and sand-laden production. Application considerations include elastomer compatibility, torque requirements, and pump geometry.",
            ["pcp", "progressive cavity pump", "applications", "viscous fluids"],
            1.0
        ),
        SearchDocument(
            9,
            "Plunger Lift System Overview",
            "Plunger lift is used for intermittent production wells. System design includes plunger type selection, controller settings, and surface equipment configuration.",
            ["plunger lift", "system", "intermittent production", "controller"],
            1.0
        ),
        SearchDocument(
            10,
            "Hydraulic Jet Pump Systems",
            "Hydraulic jet pumps utilize high-pressure power fluid to lift produced fluids. Design involves nozzle and throat sizing, power fluid selection, and surface equipment integration.",
            ["hydraulic jet pump", "systems", "design", "power fluid"],
            1.0
        ),
        SearchDocument(
            11,
            "Rod String Design and API 11L",
            "Rod string design follows API 11L standards. Key factors include rod grade selection, tapering, fatigue analysis, and maximum allowable load.",
            ["rod string", "design", "api 11l", "tapering"],
            1.0
        ),
        SearchDocument(
            12,
            "VFD Application for ESP",
            "Variable Frequency Drives (VFD) for ESPs enable speed control, soft starts, and improved energy efficiency. VFD selection considers voltage, current, and harmonics.",
            ["vfd", "esp", "variable frequency drive", "speed control"],
            1.0
        ),
        SearchDocument(
            13,
            "Artificial Lift Method Selection Decision Tree",
            "A decision tree for artificial lift method selection evaluates reservoir pressure, fluid properties, well deviation, and economic factors to recommend the optimal lift system.",
            ["artificial lift", "decision tree", "method selection"],
            1.0
        ),
        SearchDocument(
            14,
            "Gas Anchor and Separator Design",
            "Gas anchors and separators prevent free gas entry into pumps. Design parameters include separator length, diameter, and placement relative to perforations.",
            ["gas anchor", "separator", "design", "free gas"],
            1.0
        ),
        SearchDocument(
            15,
            "Tubing Anchor and Catcher Design",
            "Tubing anchors and catchers secure the tubing string and prevent movement. Selection depends on well deviation, expected loads, and compatibility with artificial lift equipment.",
            ["tubing anchor", "catcher", "design", "artificial lift"],
            1.0
        ),
        SearchDocument(
            16,
            "Pumping Unit Geometry and API 11E Classes",
            "Pumping unit geometry affects stroke length, torque, and counterbalance. API 11E classifies units by geometry and load rating for proper selection.",
            ["pumping unit", "geometry", "api 11e", "stroke length"],
            1.0
        ),
        SearchDocument(
            17,
            "Polished Rod Clamp and Stuffing Box",
            "Polished rod clamps secure the rod string at surface, while stuffing boxes provide a seal to prevent fluid leaks. Selection considers rod size and wellhead configuration.",
            ["polished rod clamp", "stuffing box", "seal", "wellhead"],
            1.0
        ),
        SearchDocument(
            18,
            "Production Optimization via Lift Method",
            "Optimizing production involves selecting the most suitable artificial lift method, adjusting operating parameters, and monitoring well performance for continuous improvement.",
            ["production optimization", "lift method", "artificial lift"],
            1.0
        ),
        SearchDocument(
            19,
            "ESP Motor Cooling and Shrouding",
            "ESP motor cooling is enhanced by shrouds that direct fluid flow over the motor. Proper shroud design prevents overheating and extends motor life.",
            ["esp", "motor cooling", "shrouding", "design"],
            1.0
        ),
        SearchDocument(
            20,
            "Beam Pump Prime Mover Selection",
            "Prime mover selection for beam pumps considers power requirements, fuel availability, and automation needs. Electric motors and gas engines are common options.",
            ["beam pump", "prime mover", "selection", "power"],
            1.0
        ),
        SearchDocument(
            21,
            "Rod String Fatigue Analysis",
            "Fatigue analysis of rod strings predicts failure risk under cyclic loading. Use S-N curves and Goodman diagrams to assess design life.",
            ["rod string", "fatigue", "analysis", "design life"],
            1.0
        ),
        SearchDocument(
            22,
            "ESP Seal Section Design",
            "Seal section design in ESPs isolates well fluids from the motor. Selection depends on temperature, pressure, and fluid compatibility.",
            ["esp", "seal section", "design", "fluid compatibility"],
            1.0
        ),
        SearchDocument(
            23,
            "Gas Lift Unloading Sequence",
            "Efficient gas lift unloading requires proper valve opening pressures and sequence control. Monitor casing and tubing pressures for optimization.",
            ["gas lift", "unloading", "valve", "sequence"],
            1.0
        ),
        SearchDocument(
            24,
            "PCP Elastomer Selection",
            "Elastomer selection for PCPs depends on produced fluid chemistry, temperature, and mechanical stresses. Compatibility ensures pump longevity.",
            ["pcp", "elastomer", "selection", "compatibility"],
            1.0
        ),
        SearchDocument(
            25,
            "Plunger Lift Controller Settings",
            "Controller settings for plunger lift systems include arrival sensor calibration, cycle timing, and pressure setpoints to maximize production.",
            ["plunger lift", "controller", "settings", "production"],
            1.0
        ),
        SearchDocument(
            26,
            "Hydraulic Jet Pump Power Fluid Selection",
            "Selecting power fluid for hydraulic jet pumps involves evaluating compatibility with produced fluids, minimizing scaling, and optimizing energy efficiency.",
            ["hydraulic jet pump", "power fluid", "selection", "scaling"],
            1.0
        ),
        SearchDocument(
            27,
            "API 11L Rod Grade Comparison",
            "API 11L rod grades differ in strength, fatigue resistance, and cost. Select appropriate grade based on well conditions and expected loads.",
            ["api 11l", "rod grade", "comparison", "selection"],
            1.0
        ),
        SearchDocument(
            28,
            "ESP Harmonic Mitigation with VFDs",
            "VFDs can introduce harmonics affecting ESP operation. Use filters and proper grounding to mitigate harmonic distortion and protect equipment.",
            ["esp", "vfd", "harmonics", "mitigation"],
            1.0
        ),
        SearchDocument(
            29,
            "Gas Anchor Placement Guidelines",
            "Proper placement of gas anchors ensures efficient gas separation and prevents pump gas lock. Position anchors below perforations when possible.",
            ["gas anchor", "placement", "guidelines", "gas lock"],
            1.0
        ),
        SearchDocument(
            30,
            "Beam Pump Rod Tapering Strategies",
            "Rod tapering reduces weight and improves fatigue life in beam pump installations. Design tapers based on load distribution and well deviation.",
            ["beam pump", "rod tapering", "fatigue", "design"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)