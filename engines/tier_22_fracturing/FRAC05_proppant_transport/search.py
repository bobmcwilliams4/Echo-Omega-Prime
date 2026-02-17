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
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
        self._initialized = False

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + ' ' + doc.content + ' ' + ' '.join(doc.tags))
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            for term in tf:
                self.doc_freqs[term] += 1
            self.doc_lengths[doc.id] = len(tokens)
            self.documents[doc.id] = doc
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        idf = self._compute_idf(query_terms)
        candidate_docs = set()
        for term in query_terms:
            for doc_id in self.term_freqs:
                if term in self.term_freqs[doc_id]:
                    candidate_docs.add(doc_id)
        scored = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_terms, idf)
            tfidf_score = self._score_tfidf(doc_id, query_terms, idf)
            doc = self.documents[doc_id]
            final_score = (bm25_score * 0.7 + tfidf_score * 0.3) * doc.weight
            snippet = self._make_snippet(doc, query_terms)
            scored.append(SearchResult(doc_id, final_score, doc.title, snippet))
        scored.sort(key=lambda r: r.score, reverse=True)
        return scored[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                'num_documents': self.N,
                'avg_doc_length': self.avg_doc_length,
                'unique_terms': len(self.doc_freqs)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9\-\.]+\b', text)
        return tokens

    def _compute_idf(self, terms: List[str]) -> Dict[str, float]:
        idf = {}
        for term in terms:
            if term in self.idf_cache:
                idf[term] = self.idf_cache[term]
                continue
            df = self.doc_freqs.get(term, 0)
            if df == 0:
                idf_val = 0.0
            else:
                idf_val = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
            idf[term] = idf_val
            self.idf_cache[term] = idf_val
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str], idf: Dict[str, float]) -> float:
        score = 0.0
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            if term not in tf:
                continue
            f = tf[term]
            denom = f + self.k1 * (1 - self.b + self.b * doc_len / (self.avg_doc_length or 1))
            score += idf.get(term, 0.0) * (f * (self.k1 + 1)) / denom
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str], idf: Dict[str, float]) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            tf_norm = tf[term] / doc_len
            score += tf_norm * idf.get(term, 0.0)
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            idx = content_lower.find(term)
            if idx != -1:
                positions.append(idx)
        if not positions:
            return content[:window] + '...' if len(content) > window else content
        start = max(min(positions) - window // 2, 0)
        end = min(start + window, len(content))
        snippet = content[start:end]
        for term in query_terms:
            snippet = re.sub(f'({re.escape(term)})', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + ('...' if end < len(content) else '')

# Singleton factory for search index
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1, "Stokes Law for Proppant Settling",
            "Stokes Law describes the settling velocity of small, spherical proppant particles in a viscous fluid. It is valid for low Reynolds numbers and is given by v = (2/9) * (r^2 * (ρ_p - ρ_f) * g) / μ.",
            ["settling", "stokes", "proppant", "fluid"], 1.0
        ),
        SearchDocument(
            2, "Hindered Settling in Proppant Transport",
            "At higher proppant concentrations, particle interactions reduce settling velocity. The Richardson-Zaki equation models hindered settling, accounting for maximum packing and fluid drag.",
            ["hindered", "settling", "richardson-zaki", "packing"], 1.0
        ),
        SearchDocument(
            3, "Tip Accumulation in Fracture Proppant Convection",
            "Proppant accumulates at fracture tips due to gravity currents and flow convergence. This can lead to uneven proppant distribution and potential screen-out risks.",
            ["tip", "accumulation", "gravity", "convection"], 1.0
        ),
        SearchDocument(
            4, "Gravity Currents in Proppant Placement",
            "Gravity-driven flow of proppant-laden slurry can cause proppant to settle preferentially along the bottom of fractures, affecting vertical coverage and conductivity.",
            ["gravity", "currents", "placement", "vertical"], 1.0
        ),
        SearchDocument(
            5, "Power Law Model for Slurry Rheology",
            "Non-Newtonian fluids are often modeled with the power law: τ = Kγ^n. The flow behavior index n and consistency K determine viscosity under shear.",
            ["rheology", "power-law", "non-newtonian", "viscosity"], 1.0
        ),
        SearchDocument(
            6, "Herschel-Bulkley Model in Proppant Transport",
            "The Herschel-Bulkley model extends the power law by adding a yield stress: τ = τ_y + Kγ^n. It captures both plastic and shear-thinning behavior of fracturing fluids.",
            ["herschel-bulkley", "yield-stress", "plastic", "shear-thinning"], 1.0
        ),
        SearchDocument(
            7, "Maximum Packing Fraction of Proppant",
            "The maximum packing fraction defines the highest volume fraction of proppant that can be suspended before bridging or screen-out occurs, typically 0.6-0.64 for spherical particles.",
            ["packing", "fraction", "screen-out", "bridging"], 1.0
        ),
        SearchDocument(
            8, "Microseismic Mapping of Proppant Distribution",
            "Microseismic events induced by fracturing can be used to infer the spatial distribution of proppant within the created fracture network.",
            ["microseismic", "mapping", "distribution", "fracture"], 1.0
        ),
        SearchDocument(
            9, "Fiber Optic Mapping of Proppant",
            "Fiber optic distributed temperature and acoustic sensing (DTS/DAS) enables real-time mapping of proppant placement and movement within fractures.",
            ["fiber-optic", "DTS", "DAS", "mapping"], 1.0
        ),
        SearchDocument(
            10, "Screen-Out in Proppant Flowback",
            "Screen-out occurs when proppant bridges the fracture or wellbore, blocking further slurry flow and potentially damaging the well.",
            ["screen-out", "flowback", "bridging", "fracture"], 1.0
        ),
        SearchDocument(
            11, "Bridging and Tail-In Phenomena",
            "Bridging happens when proppant particles form a stable arch, halting flow. Tail-in refers to the final stage of proppant injection, often with fine particles to prevent bridging.",
            ["bridging", "tail-in", "proppant", "injection"], 1.0
        ),
        SearchDocument(
            12, "API RP 19C Proppant Conductivity Testing",
            "API RP 19C outlines standard laboratory procedures for measuring proppant conductivity and crush strength under simulated reservoir conditions.",
            ["API", "RP19C", "conductivity", "crush-strength"], 1.0
        ),
        SearchDocument(
            13, "Soft Formation Conductivity Loss",
            "In soft formations, proppant embedment reduces fracture conductivity over time, especially under high closure stress and temperature cycling.",
            ["embedment", "soft-formation", "conductivity", "stress"], 1.0
        ),
        SearchDocument(
            14, "Lab vs Field Correction Factors for Proppant Conductivity",
            "Field conditions often differ from laboratory tests. Correction factors account for differences in temperature, stress, and fluid chemistry.",
            ["conductivity", "correction", "lab", "field"], 1.0
        ),
        SearchDocument(
            15, "Long-Term Conductivity Degradation",
            "Repeated stress and temperature cycling can degrade proppant pack conductivity. Monitoring and modeling are essential for long-term production.",
            ["degradation", "long-term", "conductivity", "cycling"], 1.0
        ),
        SearchDocument(
            16, "Sintered Bauxite and Lightweight Ceramic Proppant",
            "Sintered bauxite offers high strength for deep, high-stress wells. Lightweight ceramics provide economy and improved transport for shallower applications.",
            ["ceramic", "bauxite", "lightweight", "strength"], 1.0
        ),
        SearchDocument(
            17, "Resin-Coated Proppant: Curable vs Precured",
            "Resin coatings improve proppant flowback control. Curable resins consolidate in-situ, while precured resins offer immediate strength.",
            ["resin-coated", "curable", "precured", "flowback"], 1.0
        ),
        SearchDocument(
            18, "100-Mesh Sand Pumping for Microproppant",
            "100-mesh sand is used as microproppant to improve near-wellbore conductivity and reduce formation damage.",
            ["100-mesh", "microproppant", "sand", "near-wellbore"], 1.0
        ),
        SearchDocument(
            19, "In-Situ Proppant Generation and Channel Fracturing",
            "ISPS and channel fracturing techniques generate proppant or proppant-free channels in-situ to enhance fracture conductivity.",
            ["in-situ", "ISPS", "channel", "fracturing"], 1.0
        ),
        SearchDocument(
            20, "Radioactive Tracer Diagnostics for Proppant Placement",
            "Radioactive tracers can be attached to proppant to track placement and distribution within the fracture using gamma logging.",
            ["tracer", "radioactive", "diagnostics", "placement"], 1.0
        ),
        SearchDocument(
            21, "Distributed Acoustic Sensing (DAS) for Proppant",
            "DAS technology uses fiber optics to detect acoustic signals from proppant movement, enabling real-time fracture diagnostics.",
            ["DAS", "acoustic", "fiber-optic", "diagnostics"], 1.0
        ),
        SearchDocument(
            22, "Distributed Temperature Sensing (DTS) in Proppant Mapping",
            "DTS provides temperature profiles along the wellbore, revealing proppant placement and fluid movement patterns.",
            ["DTS", "temperature", "mapping", "placement"], 1.0
        ),
        SearchDocument(
            23, "Friction Pressure Prediction for Proppant-Laden Fluids",
            "Accurate prediction of friction pressure is critical for slurry design. Models account for proppant concentration, fluid rheology, and pipe geometry.",
            ["friction", "pressure", "slurry", "prediction"], 1.0
        ),
        SearchDocument(
            24, "Proppant Ramp Schedule Optimization",
            "Optimizing the proppant ramp schedule maximizes fracture conductivity while minimizing screen-out risk by controlling concentration increases.",
            ["ramp", "schedule", "optimization", "concentration"], 1.0
        ),
        SearchDocument(
            25, "Multi-Layer Proppant Placement for Vertical Coverage",
            "Multi-layer placement techniques improve vertical coverage of proppant in thick reservoirs, enhancing overall fracture conductivity.",
            ["multi-layer", "vertical", "coverage", "placement"], 1.0
        ),
        SearchDocument(
            26, "Proppant Size and Shape Effects",
            "Proppant size and sphericity affect settling velocity, packing, and conductivity. Uniform, round proppants are preferred for optimal performance.",
            ["size", "shape", "sphericity", "performance"], 1.0
        ),
        SearchDocument(
            27, "Proppant Transport in Slickwater Fluids",
            "Slickwater fluids have low viscosity, requiring higher velocities or smaller proppant to prevent settling and ensure transport.",
            ["slickwater", "transport", "settling", "velocity"], 1.0
        ),
        SearchDocument(
            28, "Proppant Flowback Control Additives",
            "Chemical additives such as tackifiers and resins help retain proppant in the fracture, reducing flowback during production.",
            ["flowback", "additives", "tackifier", "resin"], 1.0
        ),
        SearchDocument(
            29, "Proppant Embedment Modeling",
            "Finite element models predict proppant embedment and its impact on fracture conductivity, considering formation hardness and stress.",
            ["embedment", "modeling", "hardness", "stress"], 1.0
        ),
        SearchDocument(
            30, "Proppant Degradation Under High Temperature",
            "High temperatures can weaken proppant, causing fines generation and conductivity loss. Selection of thermally stable proppant is critical.",
            ["degradation", "temperature", "fines", "stability"], 1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)