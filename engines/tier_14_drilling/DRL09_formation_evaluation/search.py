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
        self.doc_lengths: Dict[int, int] = {}
        self.term_doc_freqs: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.term_df: Dict[str, int] = defaultdict(int)
        self.N = 0
        self.avgdl = 0.0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._doc_tfidf: Dict[int, Dict[str, float]] = defaultdict(dict)
        self._tfidf_norm: Dict[int, float] = {}
        self._token_pattern = re.compile(r'\b\w+\b')

    def _tokenize(self, text: str) -> List[str]:
        return [t.lower() for t in self._token_pattern.findall(text)]

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            term_freq = Counter(tokens)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            for term, freq in term_freq.items():
                self.term_doc_freqs[term][doc.id] = freq
            for term in term_freq:
                self.term_df[term] += 1
            self.N += 1
            self.avgdl = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self._idf_cache.clear()
            self._compute_tfidf_for_doc(doc.id, term_freq)

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_df.get(term, 0)
        idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _compute_tfidf_for_doc(self, doc_id: int, term_freq: Counter):
        tfidf = {}
        norm = 0.0
        for term, freq in term_freq.items():
            tf = freq / self.doc_lengths[doc_id]
            idf = self._compute_idf(term)
            tfidf_val = tf * idf
            tfidf[term] = tfidf_val
            norm += tfidf_val ** 2
        norm = math.sqrt(norm) if norm > 0 else 1.0
        self._doc_tfidf[doc_id] = tfidf
        self._tfidf_norm[doc_id] = norm

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc_len = self.doc_lengths[doc_id]
        doc = self.documents[doc_id]
        for term in query_terms:
            if doc_id not in self.term_doc_freqs.get(term, {}):
                continue
            freq = self.term_doc_freqs[term][doc_id]
            idf = self._compute_idf(term)
            denom = freq + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
            numer = freq * (self.k1 + 1)
            score += idf * numer / denom
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tfidf = self._doc_tfidf.get(doc_id, {})
        norm = self._tfidf_norm.get(doc_id, 1.0)
        score = 0.0
        for term in query_terms:
            score += tfidf.get(term, 0.0)
        return score / norm

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[int, float] = defaultdict(float)
        candidate_docs: Set[int] = set()
        for term in query_terms:
            candidate_docs.update(self.term_doc_freqs.get(term, {}).keys())
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(query_terms, doc_id)
            tfidf_score = self._score_tfidf(query_terms, doc_id)
            score = 0.7 * bm25_score + 0.3 * tfidf_score
            doc_scores[doc_id] = score
        top_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in top_docs:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:160] + "..." if len(content) > 160 else content
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        for qt in set(query_terms):
            snippet = re.sub(r'\b({})\b'.format(re.escape(qt)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + "..."

    def get_stats(self) -> Dict[str, int]:
        return {
            "documents": self.N,
            "avgdl": int(self.avgdl),
            "unique_terms": len(self.term_df),
        }

# Singleton factory for SearchIndex
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

def _seed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Gamma Ray Log for Lithology Identification",
            "The gamma ray log is used to distinguish shale from non-shale formations. High gamma readings indicate shale, while low readings suggest sandstones, carbonates, or evaporites. The tool measures natural radioactivity, mainly from potassium, thorium, and uranium.",
            ["gamma ray", "lithology", "shale", "petrophysics"],
            1.0
        ),
        SearchDocument(
            2,
            "Shale Volume Calculation Models",
            "Shale volume (Vsh) is estimated from gamma ray logs using linear, Larionov, or Clavier models. Accurate Vsh estimation is crucial for net-to-gross and reservoir quality assessment.",
            ["shale volume", "gamma ray", "Vsh", "models"],
            1.0
        ),
        SearchDocument(
            3,
            "Deep Resistivity Tools: Laterolog vs Induction",
            "Laterolog tools are preferred in conductive muds, while induction tools are optimal for resistive mud environments. Both measure formation resistivity but operate on different physical principles.",
            ["resistivity", "laterolog", "induction", "tools"],
            1.0
        ),
        SearchDocument(
            4,
            "Micro-Resistivity and Rxo Measurement",
            "Micro-resistivity devices (e.g., MicroSFL, ML) measure flushed zone resistivity (Rxo), helping to evaluate mud invasion and hydrocarbon presence near the borehole.",
            ["micro-resistivity", "Rxo", "invasion", "logs"],
            1.0
        ),
        SearchDocument(
            5,
            "Density Log: Bulk Density and Porosity",
            "The density log provides bulk density (RHOB), used to calculate formation porosity. Corrections are necessary for borehole effects, shale content, and gas presence.",
            ["density log", "bulk density", "porosity", "RHOB"],
            1.0
        ),
        SearchDocument(
            6,
            "Neutron Log: Hydrogen Index Porosity",
            "Neutron logs respond to hydrogen atoms, estimating porosity (PHIN). Gas-bearing zones may show low neutron porosity due to low hydrogen content.",
            ["neutron log", "hydrogen index", "porosity", "PHIN"],
            1.0
        ),
        SearchDocument(
            7,
            "Sonic Log and Wyllie Time Average Equation",
            "Sonic logs measure interval transit time (DT). The Wyllie equation relates DT to porosity, assuming a two-component system (matrix and fluid).",
            ["sonic log", "Wyllie", "porosity", "DT"],
            1.0
        ),
        SearchDocument(
            8,
            "Archie Equation: Water Saturation Calculation",
            "Archie's equation calculates water saturation (Sw) in clean formations using deep resistivity (Rt), porosity, and formation water resistivity (Rw).",
            ["Archie", "water saturation", "Sw", "Rw"],
            1.0
        ),
        SearchDocument(
            9,
            "Formation Water Resistivity (Rw) Determination",
            "Rw is determined from SP log, formation water samples, or empirical equations. Accurate Rw is essential for reliable Sw calculations.",
            ["Rw", "formation water", "SP log", "resistivity"],
            1.0
        ),
        SearchDocument(
            10,
            "Spontaneous Potential (SP) Log Interpretation",
            "SP logs help identify permeable zones and estimate shale content. The SP deflection is related to formation water salinity and shale volume.",
            ["SP log", "permeability", "shale", "salinity"],
            1.0
        ),
        SearchDocument(
            11,
            "Caliper Log: Borehole Size and Formation Quality",
            "Caliper logs measure borehole diameter, indicating washouts, caving, or tight formations. Borehole quality affects log interpretation accuracy.",
            ["caliper log", "borehole size", "formation quality"],
            1.0
        ),
        SearchDocument(
            12,
            "NMR Logging: T2 Distributions and Permeability",
            "Nuclear Magnetic Resonance (NMR) logs provide T2 relaxation distributions, from which porosity and permeability can be estimated. NMR distinguishes bound and free fluids.",
            ["NMR", "T2", "permeability", "porosity"],
            1.0
        ),
        SearchDocument(
            13,
            "Formation Pressure Testing: MDT, RFT, DST",
            "Formation testers (MDT, RFT) measure formation pressure and obtain fluid samples. DSTs provide dynamic flow data for reservoir evaluation.",
            ["MDT", "RFT", "DST", "pressure testing"],
            1.0
        ),
        SearchDocument(
            14,
            "Mud Logging: Gas Shows and Cuttings Analysis",
            "Mud logging monitors gas shows, lithology, and hydrocarbon indications in cuttings. It provides real-time data during drilling.",
            ["mud logging", "gas shows", "cuttings", "drilling"],
            1.0
        ),
        SearchDocument(
            15,
            "LWD vs Wireline: Logging While Drilling Comparison",
            "LWD provides real-time formation evaluation while drilling, whereas wireline logs are acquired after drilling. LWD is advantageous in unstable boreholes.",
            ["LWD", "wireline", "logging", "drilling"],
            1.0
        ),
        SearchDocument(
            16,
            "Neutron-Density Crossplot for Lithology and Gas",
            "Crossplotting neutron and density porosity helps distinguish gas zones, shales, and lithology types. Gas effect shows as a crossover.",
            ["neutron-density", "crossplot", "lithology", "gas"],
            1.0
        ),
        SearchDocument(
            17,
            "M-N Plot and MID Plot for Complex Lithology",
            "M-N and MID plots use neutron, density, and sonic logs to resolve complex lithologies such as dolomite, anhydrite, and shaly sands.",
            ["M-N plot", "MID plot", "complex lithology"],
            1.0
        ),
        SearchDocument(
            18,
            "Thin Bed Analysis and Vertical Resolution",
            "Thin beds may not be resolved by conventional logs due to limited vertical resolution. High-resolution tools and deconvolution techniques improve thin bed evaluation.",
            ["thin bed", "vertical resolution", "logs"],
            1.0
        ),
        SearchDocument(
            19,
            "Invasion Profile and Radial Resistivity Variations",
            "Resistivity logs reveal invasion profiles, with shallow, medium, and deep measurements indicating mud filtrate penetration and hydrocarbon distribution.",
            ["invasion", "radial resistivity", "logs"],
            1.0
        ),
        SearchDocument(
            20,
            "Formation Damage Identification via Logs",
            "Formation damage is indicated by decreased permeability, altered resistivity profiles, and reduced production. Logs help diagnose and quantify damage.",
            ["formation damage", "logs", "permeability"],
            1.0
        ),
        SearchDocument(
            21,
            "Core Analysis Correlation with Log Data",
            "Core analysis provides ground truth for porosity, permeability, and saturation. Correlating core and log data improves petrophysical models.",
            ["core analysis", "logs", "correlation"],
            1.0
        ),
        SearchDocument(
            22,
            "Pay Zone Identification Criteria",
            "Pay zones are defined by porosity, hydrocarbon saturation, permeability, and net thickness. Logs and core data are integrated for pay identification.",
            ["pay zone", "criteria", "logs", "hydrocarbon"],
            1.0
        ),
        SearchDocument(
            23,
            "Net-to-Gross Calculation and Reservoir Volume",
            "Net-to-gross ratio is the proportion of reservoir rock to total interval. It impacts hydrocarbon volume calculations and field development.",
            ["net-to-gross", "reservoir volume", "calculation"],
            1.0
        ),
        SearchDocument(
            24,
            "Petrophysical Cutoff Optimization",
            "Cutoffs for porosity, water saturation, and permeability are optimized to define net pay and reservoir quality. Statistical methods and core calibration are used.",
            ["petrophysical cutoff", "optimization", "net pay"],
            1.0
        ),
        SearchDocument(
            25,
            "Permian Basin: Spraberry Formation Characteristics",
            "Spraberry formation is characterized by low permeability, laminated shales, and complex lithology. Advanced logging and core analysis are required for evaluation.",
            ["Permian Basin", "Spraberry", "formation", "characteristics"],
            1.0
        ),
        SearchDocument(
            26,
            "Permian Basin: Wolfcamp Formation Evaluation",
            "Wolfcamp formation exhibits high organic content, variable lithology, and overpressure. Integrated petrophysical analysis is essential for reservoir assessment.",
            ["Permian Basin", "Wolfcamp", "formation", "evaluation"],
            1.0
        ),
        SearchDocument(
            27,
            "Permian Basin: Bone Spring Formation (Delaware Basin)",
            "Bone Spring formation in the Delaware Basin features mixed carbonate-siliciclastic lithology, high TOC, and complex reservoir properties.",
            ["Permian Basin", "Bone Spring", "Delaware Basin", "formation"],
            1.0
        ),
        SearchDocument(
            28,
            "Archie Equation Limitations in Shaly Sands",
            "Archie's equation assumes clean formations. In shaly sands, modified models (e.g., Simandoux, Dual Water) are preferred for accurate water saturation.",
            ["Archie", "shaly sands", "Simandoux", "water saturation"],
            1.0
        ),
        SearchDocument(
            29,
            "Advanced NMR Applications: Free Fluid Index",
            "NMR logs provide Free Fluid Index (FFI) and Bound Fluid Volume (BFV), aiding in movable hydrocarbon estimation and reservoir quality.",
            ["NMR", "FFI", "BFV", "hydrocarbon"],
            1.0
        ),
        SearchDocument(
            30,
            "High-Resolution Micro-Resistivity Imaging",
            "Micro-resistivity imaging tools (e.g., FMI, OBMI) deliver high-resolution images for fracture, bedding, and structural interpretation.",
            ["micro-resistivity", "imaging", "FMI", "fractures"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)