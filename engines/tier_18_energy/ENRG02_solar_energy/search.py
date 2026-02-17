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
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self.total_docs: int = 0
        self.tf_idf_matrix: Dict[int, Dict[str, float]] = defaultdict(dict)
        self._recompute_stats()

    def add_document(self, doc: SearchDocument):
        with self.lock:
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.term_freqs[doc.id] = Counter(tokens)
            for term in set(tokens):
                self.term_doc_freq[term] += 1
            self.total_docs = len(self.documents)
            self._recompute_stats()
            self._compute_tf_idf(doc.id)

    def search(self, query: str, limit: int = 10, use_tf_idf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[int, float] = defaultdict(float)
        for doc_id, doc in self.documents.items():
            if use_tf_idf:
                score = self._score_tf_idf(doc_id, query_terms)
            else:
                score = self._score_bm25(doc_id, query_terms)
            if score > 0:
                doc_scores[doc_id] = score
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            "total_docs": self.total_docs,
            "avg_doc_length": self.avg_doc_length,
            "unique_terms": len(self.term_doc_freq),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9\-]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths.get(doc_id, 0)
        score = 0.0
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * (numerator / denominator)
        return score * doc.weight

    def _score_tf_idf(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        tf_idf_vec = self.tf_idf_matrix.get(doc_id, {})
        for term in query_terms:
            score += tf_idf_vec.get(term, 0.0)
        return score * self.documents[doc_id].weight

    def _recompute_stats(self):
        if not self.doc_lengths:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / max(len(self.doc_lengths), 1)
        self.idf_cache.clear()

    def _compute_tf_idf(self, doc_id: int):
        tf_vec = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        tf_idf_vec = {}
        for term, tf in tf_vec.items():
            tf_norm = tf / doc_len
            idf = self._compute_idf(term)
            tf_idf_vec[term] = tf_norm * idf
        self.tf_idf_matrix[doc_id] = tf_idf_vec

    def _make_snippet(self, content: str, query_terms: List[str], length: int = 160) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:length]
        else:
            start = max(positions[0] - 10, 0)
            end = min(start + 40, len(tokens))
            snippet_tokens = tokens[start:end]
            snippet = ' '.join(snippet_tokens)
        return snippet[:length] + ('...' if len(snippet) > length else '')

# Singleton factory
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
            1,
            "p-n Junction Operation in Photovoltaic Cells",
            "The p-n junction is the core of a photovoltaic cell, enabling charge separation when photons excite electrons. The built-in electric field at the junction drives electrons and holes to respective contacts, generating current.",
            ["cell physics", "p-n junction", "charge separation"],
            1.0
        ),
        SearchDocument(
            2,
            "Monocrystalline Silicon vs Polycrystalline Silicon Technology",
            "Monocrystalline silicon cells offer higher efficiency due to their uniform crystal structure, while polycrystalline cells are less expensive but have lower efficiency. Both are widely used in commercial PV modules.",
            ["silicon", "monocrystalline", "polycrystalline", "efficiency"],
            1.0
        ),
        SearchDocument(
            3,
            "Thin-Film Solar Technologies: CdTe and CIGS",
            "Cadmium Telluride (CdTe) and Copper Indium Gallium Selenide (CIGS) are prominent thin-film technologies. They offer lower manufacturing costs and better performance in low-light conditions compared to silicon.",
            ["thin-film", "CdTe", "CIGS", "low-light"],
            1.0
        ),
        SearchDocument(
            4,
            "Emerging Perovskite Solar Cells",
            "Perovskite solar cells have rapidly advanced, offering high efficiency and flexible substrates. Challenges remain in stability and scaling for commercial deployment.",
            ["perovskite", "emerging", "efficiency", "stability"],
            1.0
        ),
        SearchDocument(
            5,
            "Solar Module Design: Cell Stringing and Bypass Diodes",
            "Cell stringing connects individual cells in series and parallel to form modules. Bypass diodes mitigate shading losses by allowing current to bypass shaded cells.",
            ["module design", "stringing", "bypass diodes", "shading"],
            1.0
        ),
        SearchDocument(
            6,
            "Inverter Technologies: String vs Micro vs Central",
            "String inverters are cost-effective for large arrays, microinverters optimize performance at the module level, and central inverters are used in utility-scale PV plants.",
            ["inverter", "string", "micro", "central", "utility"],
            1.0
        ),
        SearchDocument(
            7,
            "MPPT Algorithms: Perturb and Observe vs Incremental Conductance",
            "Maximum Power Point Tracking (MPPT) algorithms like Perturb and Observe and Incremental Conductance maximize PV output by dynamically adjusting operating voltage.",
            ["MPPT", "perturb", "incremental conductance", "algorithms"],
            1.0
        ),
        SearchDocument(
            8,
            "Solar Resource Assessment: GHI, DNI, DHI",
            "Global Horizontal Irradiance (GHI), Direct Normal Irradiance (DNI), and Diffuse Horizontal Irradiance (DHI) are key metrics for solar resource assessment and system design.",
            ["resource assessment", "GHI", "DNI", "DHI"],
            1.0
        ),
        SearchDocument(
            9,
            "PV System Sizing Methodology: DC-to-AC Ratio",
            "Proper PV system sizing involves calculating the DC-to-AC ratio, considering inverter loading and expected energy yield to optimize performance.",
            ["system sizing", "DC-to-AC", "inverter", "performance"],
            1.0
        ),
        SearchDocument(
            10,
            "Fixed-Tilt vs Single-Axis Tracker Systems",
            "Fixed-tilt systems are simple and cost-effective, while single-axis trackers increase energy yield by following the sun's movement throughout the day.",
            ["fixed-tilt", "tracker", "energy yield"],
            1.0
        ),
        SearchDocument(
            11,
            "Concentrated Solar Power: Parabolic Trough vs Power Tower",
            "Parabolic troughs concentrate sunlight onto a receiver tube, while power towers use a field of mirrors to focus sunlight onto a central receiver. Both enable thermal energy storage.",
            ["concentrated solar", "parabolic trough", "power tower", "thermal storage"],
            1.0
        ),
        SearchDocument(
            12,
            "Battery Storage Integration: Lithium-Ion vs Flow Batteries",
            "Lithium-ion batteries offer high energy density and fast response, while flow batteries provide scalable storage with longer lifespans, suitable for grid-scale applications.",
            ["battery storage", "lithium-ion", "flow batteries", "grid-scale"],
            1.0
        ),
        SearchDocument(
            13,
            "Grid-Tied vs Off-Grid System Design",
            "Grid-tied systems feed excess energy to the grid, while off-grid systems require battery storage and careful load management to ensure reliability.",
            ["grid-tied", "off-grid", "battery", "load management"],
            1.0
        ),
        SearchDocument(
            14,
            "PV System Losses: Soiling, Shading, Mismatch, Temperature",
            "System losses arise from soiling, shading, cell mismatch, and temperature effects. Mitigation strategies include regular cleaning, module layout optimization, and temperature management.",
            ["losses", "soiling", "shading", "mismatch", "temperature"],
            1.0
        ),
        SearchDocument(
            15,
            "NEC Article 690: Code Compliance for PV Systems",
            "NEC Article 690 outlines safety and code requirements for PV installations, including wiring, grounding, and disconnects to ensure safe operation.",
            ["NEC", "code compliance", "safety", "grounding"],
            1.0
        ),
        SearchDocument(
            16,
            "Bifacial Modules and Albedo",
            "Bifacial modules capture sunlight from both sides, increasing energy yield. Albedo, the reflectivity of the ground surface, significantly impacts bifacial performance.",
            ["bifacial", "albedo", "energy yield", "performance"],
            1.0
        ),
        SearchDocument(
            17,
            "Agrivoltaics: Dual Use of Land",
            "Agrivoltaics integrates PV systems with agriculture, enabling dual land use for crop production and solar energy generation, enhancing land productivity.",
            ["agrivoltaics", "dual use", "land", "crop"],
            1.0
        ),
        SearchDocument(
            18,
            "Floating Solar (Floatovoltaics)",
            "Floatovoltaics deploy PV modules on water bodies, reducing land use and benefiting from cooler temperatures, which improve module efficiency.",
            ["floating solar", "floatovoltaics", "water", "efficiency"],
            1.0
        ),
        SearchDocument(
            19,
            "Solar + Storage Economics: ITC and PTC",
            "Investment Tax Credit (ITC) and Production Tax Credit (PTC) incentivize solar and storage projects, improving financial viability and accelerating adoption.",
            ["economics", "ITC", "PTC", "storage"],
            1.0
        ),
        SearchDocument(
            20,
            "Solar Thermal Systems: Flat Plate vs Evacuated Tube",
            "Flat plate collectors are cost-effective for domestic hot water, while evacuated tube collectors offer higher efficiency in colder climates and industrial applications.",
            ["solar thermal", "flat plate", "evacuated tube", "efficiency"],
            1.0
        ),
        SearchDocument(
            21,
            "Cell Mismatch and Module Performance",
            "Cell mismatch occurs when cells in a module have varying electrical characteristics, reducing overall module performance. Proper sorting and stringing can mitigate mismatch losses.",
            ["cell mismatch", "module performance", "sorting", "stringing"],
            1.0
        ),
        SearchDocument(
            22,
            "Bypass Diodes: Protection Against Shading",
            "Bypass diodes protect PV modules from shading-induced losses by allowing current to bypass shaded cells, preventing hot spots and damage.",
            ["bypass diodes", "shading", "protection", "hot spots"],
            1.0
        ),
        SearchDocument(
            23,
            "Incremental Conductance MPPT Algorithm",
            "Incremental Conductance MPPT algorithm tracks the maximum power point by comparing incremental changes in current and voltage, offering faster and more accurate tracking than Perturb and Observe.",
            ["MPPT", "incremental conductance", "algorithm", "tracking"],
            1.0
        ),
        SearchDocument(
            24,
            "Single-Axis Tracker System Design",
            "Single-axis trackers rotate PV modules along one axis to follow the sun, increasing daily energy yield compared to fixed-tilt systems.",
            ["tracker", "single-axis", "energy yield", "system design"],
            1.0
        ),
        SearchDocument(
            25,
            "Lithium-Ion Battery Characteristics",
            "Lithium-ion batteries are widely used for PV storage due to their high energy density, fast charge/discharge, and long cycle life.",
            ["lithium-ion", "battery", "storage", "cycle life"],
            1.0
        ),
        SearchDocument(
            26,
            "Flow Battery Applications in Solar Storage",
            "Flow batteries offer scalable energy storage for large PV systems, with long lifespans and flexible capacity, ideal for grid-scale integration.",
            ["flow battery", "storage", "grid-scale", "lifespan"],
            1.0
        ),
        SearchDocument(
            27,
            "Power Tower Technology in Concentrated Solar Power",
            "Power towers use heliostats to focus sunlight onto a central receiver, generating high-temperature steam for electricity production and thermal storage.",
            ["power tower", "concentrated solar", "heliostat", "thermal storage"],
            1.0
        ),
        SearchDocument(
            28,
            "CdTe Thin-Film Solar Cell Advantages",
            "CdTe thin-film cells offer low-cost manufacturing, strong performance in diffuse light, and reduced material usage compared to silicon.",
            ["CdTe", "thin-film", "diffuse light", "cost"],
            1.0
        ),
        SearchDocument(
            29,
            "CIGS Thin-Film Solar Cell Performance",
            "CIGS cells provide high efficiency and flexibility, making them suitable for building-integrated photovoltaics and portable applications.",
            ["CIGS", "thin-film", "efficiency", "flexibility"],
            1.0
        ),
        SearchDocument(
            30,
            "Perovskite Cell Stability Challenges",
            "Perovskite cells face stability issues due to moisture and UV exposure. Research focuses on encapsulation and material improvements to enhance longevity.",
            ["perovskite", "stability", "encapsulation", "longevity"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)