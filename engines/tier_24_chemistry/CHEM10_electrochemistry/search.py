import math
import re
import threading
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

class SearchDocument:
    def __init__(self, id: str, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = id
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
        self.doc_freqs: Dict[str, int] = defaultdict(int)  # document frequency per term
        self.term_freqs: Dict[str, Dict[str, int]] = defaultdict(dict)  # term -> doc_id -> freq
        self.doc_lengths: Dict[str, int] = {}  # doc_id -> length (number of tokens)
        self.avg_doc_length: float = 0.0
        self.N: int = 0  # total number of documents
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
        self.tf_idf_cache: Dict[str, Dict[str, float]] = {}  # doc_id -> term -> tf-idf score

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                # Remove old frequencies
                old_doc = self.documents[doc.id]
                old_tokens = self._tokenize(old_doc.content)
                old_tf = Counter(old_tokens)
                for term in old_tf:
                    if doc.id in self.term_freqs[term]:
                        del self.term_freqs[term][doc.id]
                    self.doc_freqs[term] = max(0, self.doc_freqs[term] - 1)
                if doc.id in self.doc_lengths:
                    del self.doc_lengths[doc.id]
                if doc.id in self.tf_idf_cache:
                    del self.tf_idf_cache[doc.id]
                self.N -= 1

            tokens = self._tokenize(doc.content)
            tf = Counter(tokens)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.N += 1
            for term, freq in tf.items():
                if doc.id not in self.term_freqs[term]:
                    self.doc_freqs[term] += 1
                self.term_freqs[term][doc.id] = freq
            self._update_avg_doc_length()
            self.idf_cache.clear()
            self.tf_idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        tokens = self._tokenize(query)
        if not tokens:
            return []
        with self.lock:
            scores = defaultdict(float)
            query_tf = Counter(tokens)
            query_norm = 0.0
            # Compute IDF for query terms
            idfs = {term: self._compute_idf(term) for term in query_tf}
            # Compute query vector length for cosine similarity (TF-IDF)
            for term, freq in query_tf.items():
                tf_norm = freq / max(query_tf.values())
                idf = idfs.get(term, 0.0)
                query_norm += (tf_norm * idf) ** 2
            query_norm = math.sqrt(query_norm) if query_norm > 0 else 1.0

            # BM25 scoring
            for term in set(tokens):
                if term not in self.term_freqs:
                    continue
                idf = self._compute_idf(term)
                posting = self.term_freqs[term]
                for doc_id, freq in posting.items():
                    score = self._score_bm25(freq, idf, self.doc_lengths[doc_id])
                    scores[doc_id] += score

            # Normalize BM25 scores by document weight and add TF-IDF cosine similarity as tie breaker
            results = []
            for doc_id, bm25_score in scores.items():
                doc = self.documents[doc_id]
                # Compute TF-IDF cosine similarity between query and document
                doc_tf_idf = self._get_doc_tf_idf(doc_id)
                dot = 0.0
                doc_norm = 0.0
                for term, q_freq in query_tf.items():
                    q_tf_norm = q_freq / max(query_tf.values())
                    q_idf = idfs.get(term, 0.0)
                    q_weight = q_tf_norm * q_idf
                    d_weight = doc_tf_idf.get(term, 0.0)
                    dot += q_weight * d_weight
                for d_weight in doc_tf_idf.values():
                    doc_norm += d_weight ** 2
                doc_norm = math.sqrt(doc_norm) if doc_norm > 0 else 1.0
                cosine_sim = dot / (query_norm * doc_norm)
                combined_score = bm25_score * doc.weight + cosine_sim * 0.1
                snippet = self._make_snippet(doc.content, tokens)
                results.append(SearchResult(doc_id=doc_id, score=combined_score, title=doc.title, snippet=snippet))

            results.sort(key=lambda r: r.score, reverse=True)
            return results[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "num_documents": self.N,
                "avg_doc_length": self.avg_doc_length,
                "num_terms": len(self.doc_freqs),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
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

    def _score_bm25(self, freq: int, idf: float, doc_len: int) -> float:
        denom = freq + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
        score = idf * freq * (self.k1 + 1) / denom if denom > 0 else 0.0
        return score

    def _update_avg_doc_length(self):
        if self.N == 0:
            self.avg_doc_length = 0.0
            return
        total_length = sum(self.doc_lengths.values())
        self.avg_doc_length = total_length / self.N

    def _get_doc_tf_idf(self, doc_id: str) -> Dict[str, float]:
        if doc_id in self.tf_idf_cache:
            return self.tf_idf_cache[doc_id]
        tf_idf = {}
        doc_len = self.doc_lengths.get(doc_id, 1)
        max_tf = 1
        # Find max tf in document for normalization
        for term, posting in self.term_freqs.items():
            if doc_id in posting:
                if posting[doc_id] > max_tf:
                    max_tf = posting[doc_id]
        for term, posting in self.term_freqs.items():
            if doc_id in posting:
                tf = posting[doc_id] / max_tf
                idf = self._compute_idf(term)
                tf_idf[term] = tf * idf
        self.tf_idf_cache[doc_id] = tf_idf
        return tf_idf

    def _make_snippet(self, content: str, query_terms: List[str], snippet_len: int = 160) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            pos = content_lower.find(term)
            if pos >= 0:
                positions.append(pos)
        if not positions:
            snippet = content[:snippet_len].strip()
            if len(content) > snippet_len:
                snippet += "..."
            return snippet
        start = max(min(positions) - snippet_len // 4, 0)
        end = start + snippet_len
        snippet = content[start:end].strip()
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet += "..."
        return snippet

_singleton_instance = None
_singleton_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _singleton_instance
    if _singleton_instance is None:
        with _singleton_lock:
            if _singleton_instance is None:
                _singleton_instance = SearchIndex()
                _seed_documents(_singleton_instance)
    return _singleton_instance

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            id="doc001",
            title="Nernst Equation and Electrode Potential",
            content=(
                "The Nernst equation relates the reduction potential of an electrochemical reaction "
                "to the standard electrode potential, temperature, activity, and reaction quotient. "
                "It is fundamental in calculating electrode potentials under non-standard conditions."
            ),
            tags=["nernst", "electrode potential", "electrochemistry"],
            weight=1.2,
        ),
        SearchDocument(
            id="doc002",
            title="Butler-Volmer Kinetics and Exchange Current Density",
            content=(
                "Butler-Volmer equation describes the current-overpotential relationship for electrode reactions. "
                "Exchange current density is a key parameter representing the rate of electron transfer at equilibrium."
            ),
            tags=["butler-volmer", "kinetics", "exchange current density"],
            weight=1.3,
        ),
        SearchDocument(
            id="doc003",
            title="Cyclic Voltammetry Interpretation",
            content=(
                "Cyclic voltammetry is an electrochemical technique used to study redox processes, "
                "reaction kinetics, and diffusion coefficients by measuring current response to a linearly "
                "varied potential."
            ),
            tags=["cyclic voltammetry", "cv", "electrochemical techniques"],
            weight=1.1,
        ),
        SearchDocument(
            id="doc004",
            title="Electrochemical Impedance Spectroscopy (EIS)",
            content=(
                "EIS measures the impedance of an electrochemical system over a range of frequencies, "
                "providing insights into charge transfer resistance, double-layer capacitance, and diffusion."
            ),
            tags=["EIS", "impedance", "spectroscopy"],
            weight=1.2,
        ),
        SearchDocument(
            id="doc005",
            title="Lithium-Ion Battery Electrochemistry",
            content=(
                "Lithium-ion batteries operate based on lithium ion intercalation and deintercalation in electrode materials, "
                "with electrochemical reactions governing charge and discharge cycles."
            ),
            tags=["lithium-ion battery", "battery", "electrochemistry"],
            weight=1.4,
        ),
        SearchDocument(
            id="doc006",
            title="Proton Exchange Membrane Fuel Cells (PEMFC)",
            content=(
                "PEM fuel cells convert chemical energy from hydrogen and oxygen into electrical energy, "
                "using a proton exchange membrane as electrolyte."
            ),
            tags=["PEMFC", "fuel cells", "proton exchange membrane"],
            weight=1.3,
        ),
        SearchDocument(
            id="doc007",
            title="Water Electrolysis: Alkaline, PEM, and SOEC",
            content=(
                "Water electrolysis splits water into hydrogen and oxygen using electrical energy. "
                "Alkaline, PEM, and Solid Oxide Electrolyzer Cells (SOEC) are common types with different electrolytes."
            ),
            tags=["water electrolysis", "alkaline", "PEM", "SOEC"],
            weight=1.3,
        ),
        SearchDocument(
            id="doc008",
            title="Corrosion Electrochemistry and Polarization Curves",
            content=(
                "Corrosion involves electrochemical reactions causing material degradation. "
                "Polarization curves characterize corrosion rates and mechanisms."
            ),
            tags=["corrosion", "polarization curves", "electrochemistry"],
            weight=1.2,
        ),
        SearchDocument(
            id="doc009",
            title="Electroplating and Electrodeposition",
            content=(
                "Electroplating deposits a metal coating on a substrate via electrodeposition, "
                "involving reduction of metal ions at the cathode."
            ),
            tags=["electroplating", "electrodeposition", "metal coating"],
            weight=1.1,
        ),
        SearchDocument(
            id="doc010",
            title="Supercapacitors and Double-Layer Capacitance",
            content=(
                "Supercapacitors store energy through electrostatic charge accumulation at the electrode-electrolyte interface, "
                "exploiting double-layer capacitance."
            ),
            tags=["supercapacitors", "double-layer capacitance", "energy storage"],
            weight=1.2,
        ),
        SearchDocument(
            id="doc011",
            title="Potentiostats and Electrochemical Instrumentation",
            content=(
                "Potentiostats control the voltage between working and reference electrodes, "
                "enabling various electrochemical measurements."
            ),
            tags=["potentiostat", "instrumentation", "electrochemistry"],
            weight=1.0,
        ),
        SearchDocument(
            id="doc012",
            title="Electrochemical Sensors and Biosensors",
            content=(
                "Electrochemical sensors detect chemical species by converting chemical information into electrical signals. "
                "Biosensors use biological recognition elements."
            ),
            tags=["sensors", "biosensors", "electrochemistry"],
            weight=1.1,
        ),
        SearchDocument(
            id="doc013",
            title="Electrochemical Capacitors vs Batteries",
            content=(
                "Electrochemical capacitors provide high power density and fast charge/discharge, "
                "while batteries offer higher energy density but slower kinetics."
            ),
            tags=["capacitors", "batteries", "energy storage"],
            weight=1.0,
        ),
        SearchDocument(
            id="doc014",
            title="Electrowinning and Electrorefining of Metals",
            content=(
                "Electrowinning extracts metals from solutions by electrodeposition, "
                "and electrorefining purifies metals using controlled electrochemical processes."
            ),
            tags=["electrowinning", "electrorefining", "metals"],
            weight=1.2,
        ),
        SearchDocument(
            id="doc015",
            title="Electron Transfer Kinetics and Marcus Theory",
            content=(
                "Marcus theory explains electron transfer rates in redox reactions, "
                "considering reorganization energy and activation barriers."
            ),
            tags=["electron transfer", "marcus theory", "kinetics"],
            weight=1.3,
        ),
        SearchDocument(
            id="doc016",
            title="Electrochemical CO2 Reduction",
            content=(
                "Electrochemical CO2 reduction converts carbon dioxide into value-added chemicals "
                "using catalysts and applied potentials."
            ),
            tags=["CO2 reduction", "electrochemistry", "catalysis"],
            weight=1.4,
        ),
        SearchDocument(
            id="doc017",
            title="Ionic Conductivity in Solid Electrolytes",
            content=(
                "Solid electrolytes conduct ions without liquid solvents, "
                "important for solid-state batteries and fuel cells."
            ),
            tags=["ionic conductivity", "solid electrolytes", "batteries"],
            weight=1.2,
        ),
        SearchDocument(
            id="doc018",
            title="Redox Flow Batteries",
            content=(
                "Redox flow batteries store energy in liquid electrolytes separated by membranes, "
                "allowing scalable and flexible energy storage."
            ),
            tags=["redox flow batteries", "energy storage", "electrochemistry"],
            weight=1.3,
        ),
        SearchDocument(
            id="doc019",
            title="pH Measurement and Glass Electrode",
            content=(
                "Glass electrodes measure pH by detecting hydrogen ion activity, "
                "providing accurate acidity measurements."
            ),
            tags=["pH measurement", "glass electrode", "sensors"],
            weight=1.1,
        ),
        SearchDocument(
            id="doc020",
            title="Electrochemical Machining (ECM)",
            content=(
                "ECM removes metal by anodic dissolution using controlled electrochemical reactions, "
                "enabling precise machining without mechanical stress."
            ),
            tags=["ECM", "electrochemical machining", "manufacturing"],
            weight=1.2,
        ),
        SearchDocument(
            id="doc021",
            title="Fundamentals of Electrode Potentials",
            content=(
                "Electrode potentials arise from redox reactions and depend on ion activities, "
                "temperature, and electrode surface properties."
            ),
            tags=["electrode potentials", "redox", "fundamentals"],
            weight=1.0,
        ),
        SearchDocument(
            id="doc022",
            title="Charge Transfer Resistance in Electrochemical Systems",
            content=(
                "Charge transfer resistance quantifies the difficulty of electron transfer at electrode interfaces, "
                "affecting reaction kinetics."
            ),
            tags=["charge transfer resistance", "kinetics", "electrochemistry"],
            weight=1.1,
        ),
        SearchDocument(
            id="doc023",
            title="Diffusion in Electrochemical Reactions",
            content=(
                "Diffusion controls mass transport of reactants and products in electrochemical cells, "
                "influencing current and reaction rates."
            ),
            tags=["diffusion", "mass transport", "electrochemistry"],
            weight=1.0,
        ),
        SearchDocument(
            id="doc024",
            title="Electrode Surface Modification Techniques",
            content=(
                "Surface modification enhances electrode performance by altering morphology, "
                "chemistry, or catalytic activity."
            ),
            tags=["surface modification", "electrodes", "catalysis"],
            weight=1.1,
        ),
        SearchDocument(
            id="doc025",
            title="Electrochemical Stability Window",
            content=(
                "The electrochemical stability window defines the potential range where electrolytes remain stable "
                "without decomposition."
            ),
            tags=["stability window", "electrolytes", "electrochemistry"],
            weight=1.2,
        ),
        SearchDocument(
            id="doc026",
            title="Electrochemical Double Layer Structure",
            content=(
                "The double layer consists of charged layers at the electrode-electrolyte interface, "
                "affecting capacitance and reaction kinetics."
            ),
            tags=["double layer", "interface", "electrochemistry"],
            weight=1.1,
        ),
        SearchDocument(
            id="doc027",
            title="Electrochemical Reaction Mechanisms",
            content=(
                "Understanding reaction mechanisms helps optimize electrode materials and operating conditions "
                "for better performance."
            ),
            tags=["reaction mechanisms", "electrochemistry", "catalysis"],
            weight=1.3,
        ),
    ]
    for doc in docs:
        index.add_document(doc)