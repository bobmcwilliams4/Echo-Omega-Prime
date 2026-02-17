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
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.lock = threading.Lock()
        self.total_docs: int = 0
        self.idf_cache: Dict[str, float] = {}
        self.tf_idf_cache: Dict[int, Dict[str, float]] = defaultdict(dict)

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9\-]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            for token in tokens:
                self.term_freqs[doc.id][token] += 1
            for token in set(tokens):
                self.term_doc_freq[token] += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs
            self.idf_cache.clear()
            self.tf_idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        score = 0.0
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            denom = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * (tf * (self.k1 + 1)) / denom
        return score * doc.weight

    def _score_tf_idf(self, query_terms: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        tf_idf_score = 0.0
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_len
            idf = self._compute_idf(term)
            tf_idf_score += tf_norm * idf
        return tf_idf_score * doc.weight

    def search(self, query: str, limit: int = 10, use_tf_idf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scores: List[Tuple[int, float]] = []
        for doc_id in self.documents:
            if use_tf_idf:
                score = self._score_tf_idf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                scores.append((doc_id, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scores[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str], max_len: int = 160) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = ' '.join(tokens[:max_len])
            return snippet[:max_len] + ('...' if len(snippet) > max_len else '')
        start = max(positions[0] - 10, 0)
        end = min(start + max_len, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return snippet[:max_len] + ('...' if len(snippet) > max_len else '')

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
        }

_index_singleton = None
_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _index_singleton
    with _index_lock:
        if _index_singleton is None:
            _index_singleton = SearchIndex()
            _seed_domain_documents(_index_singleton)
        return _index_singleton

def _seed_domain_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Vogel IPR for Solution Gas Drive Reservoirs",
            "Vogel's inflow performance relationship (IPR) is used to estimate well deliverability in solution gas drive reservoirs. The equation accounts for non-linear flow behavior as pressure declines below bubble point. Key parameters include reservoir pressure, flowing bottomhole pressure, and productivity index.",
            ["IPR", "Vogel", "Solution Gas Drive", "Reservoir Engineering"],
            1.0
        ),
        SearchDocument(
            2,
            "Fetkovich IPR for Gas Wells",
            "Fetkovich's IPR combines analytical and empirical approaches for gas well performance. The method uses pseudo-pressure and flow rate to derive deliverability curves. It is widely used for gas reservoir analysis and well optimization.",
            ["IPR", "Fetkovich", "Gas Wells", "Reservoir Engineering"],
            1.0
        ),
        SearchDocument(
            3,
            "Nodal Analysis - System Optimization",
            "Nodal analysis evaluates pressure drops across production systems, optimizing well and surface equipment. It integrates reservoir, tubing, and surface constraints to maximize production and identify bottlenecks.",
            ["Nodal Analysis", "System Optimization", "Production Engineering"],
            1.0
        ),
        SearchDocument(
            4,
            "Skin Factor and Flow Efficiency",
            "Skin factor quantifies near-wellbore damage or stimulation. Positive skin indicates formation damage, reducing flow efficiency. Negative skin reflects improved flow due to stimulation. Flow efficiency compares actual to ideal well performance.",
            ["Skin Factor", "Flow Efficiency", "Well Testing"],
            1.0
        ),
        SearchDocument(
            5,
            "Productivity Index and Reservoir Deliverability",
            "Productivity index (PI) measures well deliverability, defined as flow rate per unit pressure drop. High PI indicates efficient reservoir-well communication. PI is used in IPR and production forecasting.",
            ["Productivity Index", "Reservoir Deliverability", "IPR"],
            1.0
        ),
        SearchDocument(
            6,
            "Water Cut and GOR Trending - Reservoir Surveillance",
            "Water cut and gas-oil ratio (GOR) trends are monitored for reservoir surveillance. Increasing water cut signals encroachment or breakthrough, while GOR changes indicate gas cap expansion or depletion.",
            ["Water Cut", "GOR", "Reservoir Surveillance"],
            1.0
        ),
        SearchDocument(
            7,
            "Pressure Buildup Test Analysis",
            "Pressure buildup tests assess reservoir properties and well performance. Analysis includes derivative plots, skin factor estimation, and permeability calculation. The Horner plot is commonly used for interpretation.",
            ["Pressure Buildup", "Well Testing", "Reservoir Engineering"],
            1.0
        ),
        SearchDocument(
            8,
            "Material Balance Equation - Reservoir Drive",
            "Material balance equations quantify reservoir drive mechanisms. They relate fluid withdrawal, pressure decline, and drive energy. Used for volumetric calculations and drive mechanism identification.",
            ["Material Balance", "Reservoir Drive", "Reservoir Engineering"],
            1.0
        ),
        SearchDocument(
            9,
            "Flowing Bottomhole Pressure Estimation",
            "Estimating flowing bottomhole pressure (FBHP) is crucial for production optimization. Methods include direct measurement, gradient surveys, and pressure drop calculations using multiphase flow correlations.",
            ["Bottomhole Pressure", "Production Optimization", "Multiphase Flow"],
            1.0
        ),
        SearchDocument(
            10,
            "Choke Sizing and Critical Flow",
            "Choke sizing determines optimal flow rates and prevents formation damage. Critical flow occurs when downstream pressure falls below sonic velocity threshold. Proper choke selection ensures stable production.",
            ["Choke Sizing", "Critical Flow", "Production Engineering"],
            1.0
        ),
        SearchDocument(
            11,
            "Production System Optimization - Economic Limit",
            "Optimizing production systems involves balancing technical and economic factors. Economic limit is reached when operating costs exceed revenue. System optimization delays economic limit and maximizes recovery.",
            ["Production Optimization", "Economic Limit", "Production Engineering"],
            1.0
        ),
        SearchDocument(
            12,
            "Artificial Lift Selection - Transition from Natural Flow",
            "Artificial lift methods are applied when reservoir pressure cannot sustain natural flow. Selection depends on well depth, fluid properties, and production rates. Common methods include ESP, gas lift, and rod pumping.",
            ["Artificial Lift", "Natural Flow", "Production Engineering"],
            1.0
        ),
        SearchDocument(
            13,
            "Horizontal Well Productivity - Permian Unconventionals",
            "Horizontal wells in Permian unconventional reservoirs enhance productivity by increasing contact area. Productivity depends on fracture density, reservoir properties, and completion design.",
            ["Horizontal Wells", "Permian Basin", "Unconventional Reservoirs"],
            1.0
        ),
        SearchDocument(
            14,
            "Production Data Quality Control and Validation",
            "Quality control of production data ensures reliability for analysis and decision-making. Validation includes checking for outliers, consistency, and completeness. Accurate data is essential for surveillance and forecasting.",
            ["Production Data", "Quality Control", "Validation"],
            1.0
        ),
        SearchDocument(
            15,
            "Multiphase Flow Correlations - Hagedorn-Brown",
            "Hagedorn-Brown correlation models multiphase flow in vertical wells. It accounts for gas-liquid interactions, pressure drop, and temperature effects. Used for gradient calculations and FBHP estimation.",
            ["Multiphase Flow", "Hagedorn-Brown", "Flow Correlations"],
            1.0
        ),
        SearchDocument(
            16,
            "Beggs-Brill Correlation - Inclined Multiphase Flow",
            "Beggs-Brill correlation estimates pressure drop in inclined pipes with multiphase flow. It considers holdup, slip, and flow regime transitions. Widely used in nodal analysis and well design.",
            ["Beggs-Brill", "Multiphase Flow", "Inclined Pipes"],
            1.0
        ),
        SearchDocument(
            17,
            "Decline Curve Analysis - Arps Equations",
            "Arps equations model production decline trends. Exponential, hyperbolic, and harmonic decline types are used for forecasting and reserve estimation. Decline analysis supports economic evaluation.",
            ["Decline Curve", "Arps", "Production Forecasting"],
            1.0
        ),
        SearchDocument(
            18,
            "Wellbore Storage Effect in Well Testing",
            "Wellbore storage affects early-time pressure response in well tests. It can mask reservoir properties and delay interpretation. Correction methods improve analysis accuracy.",
            ["Wellbore Storage", "Well Testing", "Reservoir Engineering"],
            1.0
        ),
        SearchDocument(
            19,
            "Permian Basin Production Characteristics",
            "Permian Basin features diverse production profiles, including conventional and unconventional reservoirs. Horizontal drilling and hydraulic fracturing have increased recovery and productivity.",
            ["Permian Basin", "Production Characteristics", "Unconventional"],
            1.0
        ),
        SearchDocument(
            20,
            "Production Allocation and Commingled Flow",
            "Production allocation assigns flow rates to individual wells or zones in commingled systems. Methods include tracer analysis, rate testing, and mathematical modeling. Accurate allocation supports reservoir management.",
            ["Production Allocation", "Commingled Flow", "Reservoir Management"],
            1.0
        ),
        SearchDocument(
            21,
            "Reservoir Surveillance - Water Cut and GOR Trending",
            "Reservoir surveillance relies on monitoring water cut and gas-oil ratio (GOR) to detect changes in reservoir behavior. Trending helps identify breakthrough, gas cap expansion, and depletion.",
            ["Reservoir Surveillance", "Water Cut", "GOR"],
            1.0
        ),
        SearchDocument(
            22,
            "Economic Limit Determination in Production Systems",
            "Economic limit is the point where production revenue equals operating costs. Determining economic limit guides shut-in decisions and field development planning.",
            ["Economic Limit", "Production Systems", "Field Development"],
            1.0
        ),
        SearchDocument(
            23,
            "ESP and Gas Lift - Artificial Lift Methods",
            "Electric submersible pumps (ESP) and gas lift are common artificial lift methods. ESPs are suited for high-rate wells, while gas lift is flexible for varying production. Selection depends on reservoir and well conditions.",
            ["ESP", "Gas Lift", "Artificial Lift"],
            1.0
        ),
        SearchDocument(
            24,
            "Reservoir Drive Mechanisms - Material Balance",
            "Material balance analysis identifies reservoir drive mechanisms such as solution gas, water drive, and gas cap expansion. It informs recovery strategy and reserves estimation.",
            ["Material Balance", "Drive Mechanisms", "Reservoir Engineering"],
            1.0
        ),
        SearchDocument(
            25,
            "Well Testing - Pressure Buildup and Drawdown",
            "Pressure buildup and drawdown tests provide insight into reservoir properties, skin factor, and permeability. Interpretation uses derivative analysis and type curves.",
            ["Well Testing", "Pressure Buildup", "Drawdown"],
            1.0
        ),
        SearchDocument(
            26,
            "Choke Management for Well Performance",
            "Choke management optimizes well performance by controlling flow rates and preventing sand production. Proper choke selection extends well life and maintains reservoir integrity.",
            ["Choke Management", "Well Performance", "Production Engineering"],
            1.0
        ),
        SearchDocument(
            27,
            "Rod Pumping - Artificial Lift Selection",
            "Rod pumping is a widely used artificial lift method for low-rate wells. Selection criteria include depth, fluid properties, and maintenance requirements.",
            ["Rod Pumping", "Artificial Lift", "Production Engineering"],
            1.0
        ),
        SearchDocument(
            28,
            "Hydraulic Fracturing in Permian Basin",
            "Hydraulic fracturing enhances productivity in Permian Basin unconventional reservoirs. Fracture design and proppant selection are critical for maximizing recovery.",
            ["Hydraulic Fracturing", "Permian Basin", "Unconventional"],
            1.0
        ),
        SearchDocument(
            29,
            "Production Forecasting Using Decline Curve Analysis",
            "Decline curve analysis forecasts future production and estimates reserves. Arps equations are used for fitting historical data and predicting performance.",
            ["Production Forecasting", "Decline Curve", "Arps"],
            1.0
        ),
        SearchDocument(
            30,
            "Multiphase Flow - Gradient Surveys and Correlations",
            "Gradient surveys and multiphase flow correlations estimate pressure profiles in wells. Hagedorn-Brown and Beggs-Brill models are applied for accurate FBHP calculations.",
            ["Multiphase Flow", "Gradient Surveys", "Correlations"],
            1.0
        ),
        SearchDocument(
            31,
            "Reservoir Management - Production Allocation",
            "Production allocation is essential for managing commingled reservoirs. Techniques include rate testing, tracer methods, and mathematical modeling.",
            ["Reservoir Management", "Production Allocation", "Commingled Flow"],
            1.0
        ),
        SearchDocument(
            32,
            "Wellbore Storage Correction in Pressure Tests",
            "Correcting for wellbore storage improves pressure test interpretation. Early-time data is adjusted to reveal true reservoir properties.",
            ["Wellbore Storage", "Pressure Tests", "Correction"],
            1.0
        ),
        SearchDocument(
            33,
            "Reservoir Deliverability - Productivity Index",
            "Reservoir deliverability is quantified by productivity index (PI), which relates flow rate to pressure drop. High PI indicates efficient well-reservoir communication.",
            ["Reservoir Deliverability", "Productivity Index", "IPR"],
            1.0
        ),
        SearchDocument(
            34,
            "Inclined Pipe Flow - Beggs-Brill Correlation",
            "Beggs-Brill correlation models multiphase flow in inclined pipes. It accounts for holdup, slip, and flow regime changes, supporting nodal analysis.",
            ["Inclined Pipe", "Beggs-Brill", "Multiphase Flow"],
            1.0
        ),
        SearchDocument(
            35,
            "Solution Gas Drive Reservoirs - Vogel IPR",
            "Vogel's IPR is applied to solution gas drive reservoirs to estimate well performance. The relationship is non-linear and incorporates reservoir pressure, FBHP, and productivity index.",
            ["Solution Gas Drive", "Vogel IPR", "Reservoir Engineering"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)