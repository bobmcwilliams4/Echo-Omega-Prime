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
        self.N: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[Tuple[int, str], float] = {}

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.title + " " + doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.doc_freqs[term] += 1
                self.inverted_index[term].add(doc.id)
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

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

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        tf = self.term_freqs[doc_id]
        score = 0.0
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + self.k1 * (1 - self.b + self.b * doc_len / (self.avg_doc_length or 1))
            score += idf * freq * (self.k1 + 1) / denom
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            cache_key = (doc_id, term)
            if cache_key in self._tfidf_cache:
                tfidf = self._tfidf_cache[cache_key]
            else:
                tf_norm = tf[term] / doc_len if doc_len else 0.0
                idf = self._compute_idf(term)
                tfidf = tf_norm * idf
                self._tfidf_cache[cache_key] = tfidf
            score += tfidf
        return score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidate_docs: Set[int] = set()
        for term in query_terms:
            candidate_docs |= self.inverted_index.get(term, set())
        scored: List[Tuple[float, int]] = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(query_terms, doc_id)
            tfidf_score = self._score_tfidf(query_terms, doc_id)
            score = bm25_score * 0.7 + tfidf_score * 0.3
            if score > 0:
                scored.append((score, doc_id))
        scored.sort(reverse=True)
        results = []
        for score, doc_id in scored[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = " ".join(tokens[:window])
        else:
            start = max(positions[0] - window // 2, 0)
            end = min(start + window, len(tokens))
            snippet = " ".join(tokens[start:end])
        return snippet

    def get_stats(self) -> Dict[str, int]:
        return {
            "documents": self.N,
            "unique_terms": len(self.doc_freqs),
            "avg_doc_length": int(self.avg_doc_length)
        }

# Singleton factory for the search index
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
            "UBD Principles and Formation Pressure",
            "Underbalanced Drilling (UBD) maintains wellbore pressure below formation pressure to prevent formation damage and enhance reservoir productivity. Accurate prediction and management of formation pressure are critical for safe and efficient UBD operations.",
            ["UBD", "formation pressure", "principles"],
            1.0
        ),
        SearchDocument(
            2,
            "Managed Pressure Drilling: Backpressure Control",
            "MPD uses surface backpressure to precisely control bottomhole pressure, enabling drilling in narrow pressure windows and reducing the risk of kicks and losses. Automatic choke systems are often employed for real-time pressure adjustments.",
            ["MPD", "backpressure", "control"],
            1.0
        ),
        SearchDocument(
            3,
            "Nitrogen Injection and Membrane PSA Generation Rates",
            "Nitrogen is commonly injected in UBD to reduce hydrostatic pressure. Membrane and Pressure Swing Adsorption (PSA) units generate nitrogen at rates matched to well requirements, ensuring consistent underbalanced conditions.",
            ["nitrogen", "injection", "PSA", "membrane"],
            1.0
        ),
        SearchDocument(
            4,
            "Four-Phase Flow Modeling in UBD",
            "Modeling the simultaneous flow of gas, liquid, solids, and cuttings is essential in UBD for accurate prediction of pressure drops and hole cleaning efficiency. Advanced simulators account for phase interactions and transient effects.",
            ["four-phase", "flow", "modeling", "UBD"],
            1.0
        ),
        SearchDocument(
            5,
            "Rotating Control Device (RCD) Pressure Rating",
            "RCDs are critical for sealing the annulus during UBD and MPD operations. Their pressure ratings must exceed expected surface pressures to ensure safety and regulatory compliance.",
            ["RCD", "pressure rating", "safety"],
            1.0
        ),
        SearchDocument(
            6,
            "Continuous Circulation System and Non-Return Valves",
            "Continuous circulation systems maintain constant bottomhole pressure during connections. Non-return valves prevent backflow and are vital for well control in UBD and MPD operations.",
            ["continuous circulation", "non-return valve", "well control"],
            1.0
        ),
        SearchDocument(
            7,
            "UBD Wellbore Hydraulics and ECD Management",
            "Effective management of Equivalent Circulating Density (ECD) is crucial in UBD to avoid formation influx or losses. Hydraulic models help optimize fluid properties and flow rates.",
            ["hydraulics", "ECD", "management", "UBD"],
            1.0
        ),
        SearchDocument(
            8,
            "Formation Damage and Skin Factor Prevention",
            "UBD minimizes formation damage by reducing invasion of drilling fluids. Proper fluid selection and pressure management prevent increases in skin factor and preserve reservoir permeability.",
            ["formation damage", "skin factor", "prevention"],
            1.0
        ),
        SearchDocument(
            9,
            "Reservoir Influx Management and Kick Detection",
            "Early kick detection is enabled by real-time monitoring of flow rates and pressures. UBD operations require robust influx management strategies to prevent well control incidents.",
            ["kick detection", "influx management", "reservoir"],
            1.0
        ),
        SearchDocument(
            10,
            "UBD Casing Design: Burst, Collapse, Tension",
            "Casing in UBD must withstand burst, collapse, and tension loads under underbalanced conditions. Design considers maximum anticipated pressures and operational scenarios.",
            ["casing design", "burst", "collapse", "tension"],
            1.0
        ),
        SearchDocument(
            11,
            "Snubbing Operations and Pipe Light Conditions",
            "Snubbing allows pipe movement under pressure. Pipe light conditions, where buoyancy reduces pipe weight, require careful control to avoid equipment damage or well control issues.",
            ["snubbing", "pipe light", "operations"],
            1.0
        ),
        SearchDocument(
            12,
            "Gas Flaring and Environmental Disposal",
            "Produced gas during UBD is often flared or routed to environmental disposal systems. Compliance with emissions regulations is essential for safe and responsible operations.",
            ["gas flaring", "environmental", "disposal"],
            1.0
        ),
        SearchDocument(
            13,
            "UBD BHA Considerations: MWD/LWD Compatibility",
            "Bottomhole Assembly (BHA) design in UBD must ensure compatibility with Measurement While Drilling (MWD) and Logging While Drilling (LWD) tools, which may be affected by multiphase flow and pressure variations.",
            ["BHA", "MWD", "LWD", "compatibility"],
            1.0
        ),
        SearchDocument(
            14,
            "Produced Fluid Handling and Separator Design",
            "Surface separation systems are designed to handle multiphase produced fluids during UBD. Separator sizing and configuration depend on expected flow rates and fluid properties.",
            ["produced fluid", "separator", "design"],
            1.0
        ),
        SearchDocument(
            15,
            "UBD Economic Analysis: Rate of Penetration Improvement",
            "UBD can significantly improve rate of penetration (ROP) by reducing bottomhole pressure and minimizing formation damage. Economic analysis weighs increased productivity against operational costs.",
            ["economic analysis", "ROP", "penetration"],
            1.0
        ),
        SearchDocument(
            16,
            "Formation Evaluation While Drilling (UBD)",
            "Real-time formation evaluation in UBD uses advanced sensors and logging tools to assess reservoir properties and optimize drilling parameters.",
            ["formation evaluation", "while drilling", "UBD"],
            1.0
        ),
        SearchDocument(
            17,
            "Well Control and UBD Barrier Philosophy",
            "UBD requires a robust barrier philosophy, including mechanical and fluid barriers, to maintain well control under dynamic pressure conditions.",
            ["well control", "barrier", "philosophy"],
            1.0
        ),
        SearchDocument(
            18,
            "MPD Automatic Choke PID Control",
            "Automatic chokes in MPD use PID controllers to maintain constant bottomhole pressure by adjusting choke position in response to pressure fluctuations.",
            ["MPD", "automatic choke", "PID", "control"],
            1.0
        ),
        SearchDocument(
            19,
            "MPD Constant Bottomhole Pressure (CBHP) Method",
            "The CBHP method in MPD maintains a steady bottomhole pressure throughout drilling, tripping, and connections, reducing the risk of influx or losses.",
            ["MPD", "CBHP", "constant bottomhole pressure"],
            1.0
        ),
        SearchDocument(
            20,
            "UBD Horizontal Well Applications",
            "UBD is particularly beneficial in horizontal and extended reach wells, where conventional overbalanced drilling may cause severe formation damage and productivity loss.",
            ["horizontal well", "UBD", "extended reach"],
            1.0
        ),
        SearchDocument(
            21,
            "Extended Reach Drilling in UBD",
            "Extended reach drilling (ERD) with UBD techniques enables access to distant reservoir targets while minimizing formation damage and maximizing production.",
            ["extended reach", "drilling", "UBD", "ERD"],
            1.0
        ),
        SearchDocument(
            22,
            "UBD Fluid Selection and Properties",
            "Selection of appropriate drilling fluids in UBD is critical for maintaining underbalanced conditions, optimizing hole cleaning, and minimizing formation damage.",
            ["fluid selection", "UBD", "properties"],
            1.0
        ),
        SearchDocument(
            23,
            "UBD Surface Equipment and Safety Systems",
            "Surface equipment for UBD includes RCDs, separators, and emergency shutdown systems. Safety systems are designed to handle multiphase flow and high-pressure scenarios.",
            ["surface equipment", "safety", "UBD"],
            1.0
        ),
        SearchDocument(
            24,
            "UBD Training and Competency",
            "Comprehensive training programs ensure personnel competency in UBD operations, focusing on well control, equipment operation, and emergency response.",
            ["training", "competency", "UBD"],
            1.0
        ),
        SearchDocument(
            25,
            "UBD Data Acquisition and Real-Time Monitoring",
            "Real-time data acquisition systems in UBD provide continuous monitoring of pressure, flow, and gas levels, enabling proactive decision-making and early kick detection.",
            ["data acquisition", "real-time", "monitoring", "UBD"],
            1.0
        ),
        SearchDocument(
            26,
            "UBD Well Planning and Risk Assessment",
            "Thorough well planning and risk assessment are essential for successful UBD projects, addressing formation pressure uncertainties and operational hazards.",
            ["well planning", "risk assessment", "UBD"],
            1.0
        ),
        SearchDocument(
            27,
            "UBD and MPD Transition Strategies",
            "Transitioning between UBD and MPD modes requires careful management of pressure and flow to maintain well control and operational efficiency.",
            ["transition", "UBD", "MPD", "strategy"],
            1.0
        ),
        SearchDocument(
            28,
            "UBD Cuttings Transport and Hole Cleaning",
            "Efficient cuttings transport is vital in UBD, especially in deviated and horizontal wells. Fluid velocity and rheology are optimized for effective hole cleaning.",
            ["cuttings transport", "hole cleaning", "UBD"],
            1.0
        ),
        SearchDocument(
            29,
            "UBD Annular Pressure Management",
            "Annular pressure management in UBD involves real-time monitoring and control to prevent influx, losses, and wellbore instability.",
            ["annular pressure", "management", "UBD"],
            1.0
        ),
        SearchDocument(
            30,
            "UBD Well Integrity and Casing Shoe Isolation",
            "Maintaining well integrity in UBD includes proper casing shoe isolation and cementing practices to prevent crossflow and maintain zonal isolation.",
            ["well integrity", "casing shoe", "isolation", "UBD"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)