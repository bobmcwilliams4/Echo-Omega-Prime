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
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N = 0
        self.inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._recompute_stats = True

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.doc_freqs[term] += 1
                self.inverted_index[term].add(doc.id)
            self.documents[doc.id] = doc
            self.N += 1
            self._recompute_stats = True

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        doc_scores: Dict[int, float] = defaultdict(float)
        tfidf_scores: Dict[int, float] = defaultdict(float)
        query_term_counts = Counter(query_terms)
        self._ensure_stats()
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, set()))
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc = self.documents[doc_id]
            total_score = 0.7 * bm25_score + 0.3 * tfidf_score
            total_score *= doc.weight
            doc_scores[doc_id] = total_score
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id=doc_id, score=score, title=doc.title, snippet=snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        self._ensure_stats()
        return {
            "num_documents": self.N,
            "avg_doc_length": self.avg_doc_length,
            "vocab_size": len(self.doc_freqs),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9\-\_\.]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self.term_freqs[doc_id]
        doc_length = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + self.k1 * (1 - self.b + self.b * doc_length / self.avg_doc_length)
            score += idf * (freq * (self.k1 + 1)) / denom
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self.term_freqs[doc_id]
        doc_length = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            freq = tf.get(term, 0)
            if freq == 0:
                continue
            tf_norm = freq / doc_length
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = ' '.join(tokens[:window])
            return snippet + ('...' if len(tokens) > window else '')
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return '...' + snippet + ('...' if end < len(tokens) else '')

    def _ensure_stats(self):
        if self._recompute_stats:
            total_length = sum(self.doc_lengths.values())
            self.avg_doc_length = total_length / self.N if self.N > 0 else 0.0
            self.idf_cache.clear()
            self._recompute_stats = False

# Singleton factory for SearchIndex
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
    docs = [
        SearchDocument(
            1, "Overburden Stress Determination",
            "Overburden stress is calculated by integrating the density log from the surface to the depth of interest. This is critical for wellbore stability analysis.",
            ["in-situ", "overburden", "stress", "density"], 1.0
        ),
        SearchDocument(
            2, "Horizontal In-situ Stress Estimation",
            "Minimum and maximum horizontal stresses are estimated using leak-off tests, mini-frac, and log-derived poroelastic models.",
            ["in-situ", "horizontal", "stress", "poromechanics"], 1.0
        ),
        SearchDocument(
            3, "Mohr-Coulomb Failure Criterion",
            "The Mohr-Coulomb criterion defines failure by the relationship between shear and normal stresses, incorporating cohesion and friction angle.",
            ["failure", "mohr-coulomb", "cohesion", "friction"], 1.0
        ),
        SearchDocument(
            4, "Cohesion and Friction Angle in Shale",
            "Cohesion and friction angle are derived from triaxial tests and are essential for predicting wellbore collapse.",
            ["shale", "cohesion", "friction", "collapse"], 1.0
        ),
        SearchDocument(
            5, "Mud Weight Window: Collapse and Fracture Gradient",
            "The mud weight window is bounded by the collapse gradient (lower bound) and fracture gradient (upper bound), ensuring safe drilling.",
            ["mud-weight", "collapse", "fracture", "gradient"], 1.0
        ),
        SearchDocument(
            6, "Shale Reactivity: Cation Exchange Capacity",
            "High CEC in shales increases water uptake, affecting wellbore stability through swelling and chemical interactions.",
            ["shale", "reactivity", "cec", "swelling"], 1.0
        ),
        SearchDocument(
            7, "Water Activity and Osmotic Effects",
            "Water activity differences between mud and formation drive osmotic flows, influencing shale stability and hydration.",
            ["water-activity", "osmotic", "shale", "hydration"], 1.0
        ),
        SearchDocument(
            8, "Kirsch Solution for Stress Concentration",
            "The Kirsch equations describe stress distribution around a circular wellbore, predicting zones of breakout and tensile failure.",
            ["kirsch", "stress", "concentration", "breakout"], 1.0
        ),
        SearchDocument(
            9, "Borehole Breakout Mechanisms",
            "Breakouts occur when tangential stress exceeds rock strength, typically aligned with minimum horizontal stress.",
            ["breakout", "borehole", "stress", "failure"], 1.0
        ),
        SearchDocument(
            10, "Tensile and Drilling-Induced Fractures",
            "Tensile fractures form when mud pressure exceeds the minimum principal stress, leading to wellbore instability.",
            ["tensile", "fracture", "drilling-induced", "instability"], 1.0
        ),
        SearchDocument(
            11, "Mechanical Earth Model (MEM) 1D Construction",
            "A 1D MEM integrates logs, core, and test data to model mechanical properties and stress profiles along the well.",
            ["mem", "1d", "mechanical", "logs"], 1.0
        ),
        SearchDocument(
            12, "Mechanical Earth Model (MEM) 3D Construction",
            "3D MEMs combine seismic, logs, and geostatistics to map stress and property variations in the reservoir.",
            ["mem", "3d", "mechanical", "seismic"], 1.0
        ),
        SearchDocument(
            13, "Pore Pressure Prediction: Eaton Method",
            "The Eaton method uses sonic or resistivity log deviations to estimate abnormal pore pressure in shales.",
            ["pore-pressure", "eaton", "sonic", "shale"], 1.0
        ),
        SearchDocument(
            14, "Pore Pressure Prediction: Bowers Method",
            "Bowers' method refines pore pressure prediction by relating velocity reduction to effective stress in compacting shales.",
            ["pore-pressure", "bowers", "velocity", "compaction"], 1.0
        ),
        SearchDocument(
            15, "Fracture Gradient: Daines and Breckels Methods",
            "Daines and Breckels provide empirical correlations for fracture gradient prediction using overburden and pore pressure.",
            ["fracture-gradient", "daines", "breckels", "overburden"], 1.0
        ),
        SearchDocument(
            16, "Wellbore Stability: Mogi-Coulomb and Drucker-Prager",
            "Advanced criteria like Mogi-Coulomb and Drucker-Prager account for intermediate principal stress in wellbore failure.",
            ["wellbore", "stability", "mogi-coulomb", "drucker-prager"], 1.0
        ),
        SearchDocument(
            17, "Chemical-Mechanical Coupling in Shale",
            "Shale-fluid interaction modifies effective stress and strength, requiring coupled chemical-mechanical modeling.",
            ["chemical", "mechanical", "shale", "coupling"], 1.0
        ),
        SearchDocument(
            18, "Time-Dependent Instability: Creep and Swelling",
            "Creep and swelling cause delayed wellbore collapse, especially in reactive shales under stress and fluid exposure.",
            ["creep", "swelling", "instability", "shale"], 1.0
        ),
        SearchDocument(
            19, "Stuck Pipe: Differential Sticking",
            "Differential sticking occurs when high mud overbalance forces drill pipe against permeable formations.",
            ["stuck-pipe", "differential-sticking", "mud", "permeability"], 1.0
        ),
        SearchDocument(
            20, "Stuck Pipe: Key Seating",
            "Key seating results from excessive dogleg severity, creating narrow ledges that trap the drill string.",
            ["stuck-pipe", "key-seating", "dogleg", "drilling"], 1.0
        ),
        SearchDocument(
            21, "Lost Circulation: Preventive LCM",
            "Preventive lost circulation materials (LCM) are added to mud to bridge fractures and prevent fluid loss.",
            ["lost-circulation", "lcm", "fractures", "mud"], 1.0
        ),
        SearchDocument(
            22, "Lost Circulation: Squeeze Techniques",
            "Squeeze cementing and pills are remedial techniques to seal lost circulation zones during drilling.",
            ["lost-circulation", "squeeze", "cement", "remedial"], 1.0
        ),
        SearchDocument(
            23, "Sand Production Onset Prediction",
            "Sanding risk is predicted using critical drawdown and rock strength analysis, preventing wellbore failure.",
            ["sand-production", "sanding", "drawdown", "strength"], 1.0
        ),
        SearchDocument(
            24, "Casing Deformation: Formation Movement",
            "Casing deformation is caused by formation movement, compaction, and stress changes in the reservoir.",
            ["casing", "deformation", "compaction", "movement"], 1.0
        ),
        SearchDocument(
            25, "Thermal Stress Effects in Wellbores",
            "Thermal cooling or heating during drilling induces additional stresses, affecting wellbore integrity.",
            ["thermal", "stress", "wellbore", "drilling"], 1.0
        ),
        SearchDocument(
            26, "Wellbore Breathing and Ballooning",
            "Formation breathing and ballooning are reversible mud losses and gains due to wellbore stress cycling.",
            ["breathing", "ballooning", "wellbore", "stress"], 1.0
        ),
        SearchDocument(
            27, "Geomechanical Logging: Sonic and Dipole",
            "Sonic and dipole logs provide dynamic elastic properties for MEM construction and stress analysis.",
            ["geomechanical", "logging", "sonic", "dipole"], 1.0
        ),
        SearchDocument(
            28, "Depletion-Induced Stress Changes",
            "Reservoir compaction from depletion alters in-situ stress, affecting wellbore stability and casing integrity.",
            ["depletion", "stress", "compaction", "wellbore"], 1.0
        ),
        SearchDocument(
            29, "Cross-Dipole Sonic Logging",
            "Cross-dipole sonic logs resolve anisotropy and stress orientation for advanced geomechanical models.",
            ["cross-dipole", "sonic", "anisotropy", "stress"], 1.0
        ),
        SearchDocument(
            30, "Formation Testing for Stress and Pore Pressure",
            "Formation testing tools measure in-situ stress and pore pressure, validating MEM and wellbore stability models.",
            ["formation-testing", "stress", "pore-pressure", "mem"], 1.0
        ),
        SearchDocument(
            31, "Compaction and Subsidence Effects",
            "Formation compaction leads to surface subsidence and casing deformation, requiring geomechanical monitoring.",
            ["compaction", "subsidence", "casing", "deformation"], 1.0
        ),
        SearchDocument(
            32, "Drilling-Induced Tensile Fracture Identification",
            "Tensile fractures induced by drilling are identified using borehole imaging and pressure analysis.",
            ["tensile-fracture", "drilling", "borehole", "imaging"], 1.0
        ),
        SearchDocument(
            33, "Preventing Wellbore Collapse in Swelling Shales",
            "Optimizing mud chemistry and weight helps prevent collapse in swelling, reactive shales.",
            ["wellbore", "collapse", "swelling", "shale"], 1.0
        ),
        SearchDocument(
            34, "Advanced Pore Pressure Prediction Techniques",
            "Machine learning and advanced log analysis improve pore pressure prediction accuracy in complex formations.",
            ["pore-pressure", "prediction", "machine-learning", "logs"], 1.0
        ),
        SearchDocument(
            35, "Sonic Log Anisotropy and Stress Orientation",
            "Sonic log anisotropy analysis reveals in-situ stress orientation and fracture networks.",
            ["sonic", "anisotropy", "stress", "fracture"], 1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)