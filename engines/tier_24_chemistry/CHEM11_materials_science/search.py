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
    def __init__(self, bm25_k1: float = 1.5, bm25_b: float = 0.75):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_doc_freqs: Dict[int, Counter] = {}
        self.inverted_index: Dict[str, set] = defaultdict(set)
        self.bm25_k1 = bm25_k1
        self.bm25_b = bm25_b
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.lock = threading.Lock()
        self._dirty_stats = True

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            term_freq = Counter(tokens)
            self.term_doc_freqs[doc.id] = term_freq
            self.doc_lengths[doc.id] = len(tokens)
            self.documents[doc.id] = doc
            for term in term_freq:
                self.doc_freqs[term] += 1
                self.inverted_index[term].add(doc.id)
            self._dirty_stats = True

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        with self.lock:
            if self._dirty_stats:
                self._update_stats()
            candidate_doc_ids = set()
            for term in query_terms:
                candidate_doc_ids.update(self.inverted_index.get(term, set()))
            scores = []
            for doc_id in candidate_doc_ids:
                bm25_score = self._score_bm25(query_terms, doc_id)
                tfidf_score = self._score_tfidf(query_terms, doc_id)
                final_score = 0.7 * bm25_score + 0.3 * tfidf_score
                doc = self.documents[doc_id]
                snippet = self._make_snippet(doc, query_terms)
                scores.append(SearchResult(doc_id, final_score, doc.title, snippet))
            scores.sort(key=lambda x: x.score, reverse=True)
            return scores[:limit]

    def get_stats(self) -> Dict:
        with self.lock:
            if self._dirty_stats:
                self._update_stats()
            return {
                "num_documents": len(self.documents),
                "avg_doc_length": self.avg_doc_length,
                "num_terms": len(self.doc_freqs)
            }

    def _tokenize(self, text: str) -> List[str]:
        return [t.lower() for t in re.findall(r'\b\w+\b', text)]

    def _compute_idf(self, term: str) -> float:
        N = len(self.documents)
        df = self.doc_freqs.get(term, 0)
        return math.log(1 + (N - df + 0.5) / (df + 0.5))

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            idf = self._compute_idf(term)
            tf = self.term_doc_freqs[doc_id].get(term, 0)
            numerator = tf * (self.bm25_k1 + 1)
            denominator = tf + self.bm25_k1 * (1 - self.bm25_b + self.bm25_b * doc_len / self.avg_doc_length)
            score += idf * numerator / denominator if denominator != 0 else 0.0
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        tf_norm = self._tf_norm(self.term_doc_freqs[doc_id])
        for term in query_terms:
            tf = self.term_doc_freqs[doc_id].get(term, 0)
            idf = self._compute_idf(term)
            score += tf_norm.get(term, 0.0) * idf
        return score * doc.weight

    def _tf_norm(self, term_freq: Counter) -> Dict[str, float]:
        max_tf = max(term_freq.values()) if term_freq else 1
        return {term: freq / max_tf for term, freq in term_freq.items()}

    def _update_stats(self):
        total_len = sum(self.doc_lengths.values())
        self.avg_doc_length = total_len / len(self.doc_lengths) if self.doc_lengths else 0.0
        self._dirty_stats = False

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:window*2]
            return snippet + "..." if len(content) > window*2 else snippet
        start = max(positions[0] - window, 0)
        end = min(positions[0] + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        return snippet + "..." if end < len(tokens) else snippet

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1, "Body-Centered Cubic (BCC) Structure",
            "The body-centered cubic (BCC) crystal structure consists of atoms at each corner of a cube and a single atom at the center. Common BCC metals include iron (at room temperature), chromium, and tungsten.",
            ["crystal structure", "bcc", "metals"], 1.0
        ),
        SearchDocument(
            2, "Face-Centered Cubic (FCC) Structure",
            "The face-centered cubic (FCC) structure has atoms at each corner and at the centers of all cube faces. Examples include aluminum, copper, gold, and silver.",
            ["crystal structure", "fcc", "metals"], 1.0
        ),
        SearchDocument(
            3, "Hexagonal Close-Packed (HCP) Structure",
            "The hexagonal close-packed (HCP) structure features atoms arranged in a hexagonal lattice. Magnesium, titanium, and zinc are typical HCP metals.",
            ["crystal structure", "hcp", "metals"], 1.0
        ),
        SearchDocument(
            4, "Binary Eutectic Phase Diagrams",
            "Binary eutectic systems display a phase diagram with a eutectic point where the lowest melting temperature occurs. At this composition, two solid phases crystallize simultaneously from the liquid.",
            ["phase diagram", "binary", "eutectic"], 1.0
        ),
        SearchDocument(
            5, "Ternary Phase Diagrams",
            "Ternary phase diagrams represent systems with three components. They are often depicted as equilateral triangles, showing phase regions and tie lines for alloys.",
            ["phase diagram", "ternary", "alloys"], 1.0
        ),
        SearchDocument(
            6, "Fick's First Law of Diffusion",
            "Fick's first law states that the diffusion flux is proportional to the concentration gradient. It applies to steady-state diffusion and is expressed as J = -D (dC/dx).",
            ["diffusion", "fick", "first law"], 1.0
        ),
        SearchDocument(
            7, "Fick's Second Law of Diffusion",
            "Fick's second law describes non-steady-state diffusion, relating the change in concentration with time to the second derivative of concentration with position.",
            ["diffusion", "fick", "second law"], 1.0
        ),
        SearchDocument(
            8, "Yield Strength in Metals",
            "Yield strength is the stress at which a material begins to deform plastically. It is determined from the stress-strain curve and is critical for engineering design.",
            ["mechanical properties", "yield strength"], 1.0
        ),
        SearchDocument(
            9, "Tensile Strength in Materials",
            "Tensile strength is the maximum stress a material can withstand while being stretched before necking. It is a key mechanical property for structural applications.",
            ["mechanical properties", "tensile strength"], 1.0
        ),
        SearchDocument(
            10, "Annealing Heat Treatment",
            "Annealing involves heating a material and then cooling it slowly to remove internal stresses and increase ductility. It is commonly used for metals and alloys.",
            ["heat treatment", "annealing"], 1.0
        ),
        SearchDocument(
            11, "Quenching Process",
            "Quenching is a heat treatment process where a material is rapidly cooled, usually in water or oil, to increase hardness. It can also increase brittleness.",
            ["heat treatment", "quenching"], 1.0
        ),
        SearchDocument(
            12, "Tempering Process",
            "Tempering follows quenching and involves reheating the material to a lower temperature, then cooling it. This reduces brittleness while maintaining hardness.",
            ["heat treatment", "tempering"], 1.0
        ),
        SearchDocument(
            13, "Galvanic Corrosion",
            "Galvanic corrosion occurs when two dissimilar metals are electrically connected in a corrosive environment, causing one metal to corrode preferentially.",
            ["corrosion", "galvanic"], 1.0
        ),
        SearchDocument(
            14, "Pitting Corrosion",
            "Pitting corrosion is a localized form of corrosion that leads to the creation of small holes or pits in the material, often in passive metals like stainless steel.",
            ["corrosion", "pitting"], 1.0
        ),
        SearchDocument(
            15, "Crevice Corrosion",
            "Crevice corrosion occurs in confined spaces where the access of the working fluid is limited, such as under gaskets or deposits.",
            ["corrosion", "crevice"], 1.0
        ),
        SearchDocument(
            16, "Stress Corrosion Cracking",
            "Stress corrosion cracking is the growth of cracks in a corrosive environment, accelerated by tensile stress. It can lead to sudden failure of metals.",
            ["corrosion", "stress"], 1.0
        ),
        SearchDocument(
            17, "Polymer Chain Architecture",
            "Polymer chain architecture refers to the arrangement of monomer units in a polymer. Linear, branched, and crosslinked architectures influence properties like strength and flexibility.",
            ["polymers", "chain architecture"], 1.0
        ),
        SearchDocument(
            18, "Polymer Crystallinity",
            "Crystallinity in polymers describes the degree of structural order. Higher crystallinity generally increases strength and chemical resistance but decreases flexibility.",
            ["polymers", "crystallinity"], 1.0
        ),
        SearchDocument(
            19, "Slip Systems in BCC Crystals",
            "BCC crystals have multiple slip systems, but the lack of close-packed planes makes slip more difficult compared to FCC structures, affecting ductility.",
            ["crystal structure", "bcc", "slip"], 1.0
        ),
        SearchDocument(
            20, "Stacking Faults in FCC Metals",
            "FCC metals are prone to stacking faults due to their close-packed planes. These faults influence mechanical properties such as work hardening.",
            ["crystal structure", "fcc", "stacking faults"], 1.0
        ),
        SearchDocument(
            21, "Eutectic Reactions in Binary Alloys",
            "A eutectic reaction involves a liquid transforming into two solid phases at a specific composition and temperature, characteristic of binary eutectic systems.",
            ["phase diagram", "eutectic", "binary"], 1.0
        ),
        SearchDocument(
            22, "Lever Rule in Phase Diagrams",
            "The lever rule is used to determine the proportion of phases in a two-phase region of a binary phase diagram.",
            ["phase diagram", "lever rule"], 1.0
        ),
        SearchDocument(
            23, "Diffusion Coefficient in Metals",
            "The diffusion coefficient quantifies how fast atoms or molecules diffuse in a material. It depends on temperature and crystal structure.",
            ["diffusion", "coefficient"], 1.0
        ),
        SearchDocument(
            24, "Precipitation Hardening",
            "Precipitation hardening is a heat treatment that increases the yield strength of malleable materials, including most structural alloys.",
            ["heat treatment", "precipitation hardening"], 1.0
        ),
        SearchDocument(
            25, "Passivation in Corrosion Protection",
            "Passivation involves forming a thin oxide layer on the surface of metals, such as stainless steel, to protect against corrosion.",
            ["corrosion", "passivation"], 1.0
        ),
        SearchDocument(
            26, "Dislocation Motion in HCP Metals",
            "HCP metals have fewer slip systems, making dislocation motion and plastic deformation more difficult compared to FCC or BCC metals.",
            ["crystal structure", "hcp", "dislocation"], 1.0
        ),
        SearchDocument(
            27, "Phase Rule for Ternary Systems",
            "The Gibbs phase rule helps determine the number of phases present in ternary systems, accounting for components and degrees of freedom.",
            ["phase diagram", "ternary", "gibbs rule"], 1.0
        ),
        SearchDocument(
            28, "Thermal Conductivity of Metals",
            "Thermal conductivity is generally higher in metals with close-packed structures like FCC and HCP, due to efficient atomic packing.",
            ["thermal conductivity", "fcc", "hcp"], 1.0
        ),
        SearchDocument(
            29, "Martensitic Transformation",
            "Martensitic transformation is a diffusionless phase change, important in steels during quenching, leading to a hard but brittle microstructure.",
            ["heat treatment", "martensite", "quenching"], 1.0
        ),
        SearchDocument(
            30, "Chain Branching in Polymers",
            "Chain branching in polymers affects density, crystallinity, and melting temperature. Branched polymers are usually less crystalline than linear ones.",
            ["polymers", "branching"], 1.0
        ),
        SearchDocument(
            31, "Fatigue Strength of Materials",
            "Fatigue strength is the highest stress a material can withstand for a given number of cycles without failing. It is critical for components under cyclic loading.",
            ["mechanical properties", "fatigue strength"], 1.0
        ),
        SearchDocument(
            32, "Carbide Precipitation in Stainless Steel",
            "Carbide precipitation can occur in stainless steels during improper heat treatment, leading to sensitization and increased susceptibility to intergranular corrosion.",
            ["corrosion", "carbide precipitation", "stainless steel"], 1.0
        ),
        SearchDocument(
            33, "Tie Lines in Ternary Phase Diagrams",
            "Tie lines connect compositions in equilibrium in ternary phase diagrams, helping to determine phase fractions.",
            ["phase diagram", "ternary", "tie lines"], 1.0
        ),
        SearchDocument(
            34, "Creep in Metals",
            "Creep is the slow, time-dependent deformation of materials under constant stress, significant at high temperatures.",
            ["mechanical properties", "creep"], 1.0
        ),
        SearchDocument(
            35, "Glass Transition in Polymers",
            "The glass transition temperature is the point where an amorphous polymer transitions from a brittle, glassy state to a ductile, rubbery state.",
            ["polymers", "glass transition"], 1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)