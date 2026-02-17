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
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.total_docs: int = 0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = defaultdict(dict)
        self.k1 = 1.5
        self.b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            token_counts = Counter(tokens)
            for token, count in token_counts.items():
                self.inverted_index[token][doc.id] = count
                self.term_doc_freq[token] += 1
            self._idf_cache.clear()
            self._tfidf_cache.clear()
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        doc_scores: Dict[int, float] = defaultdict(float)
        doc_tfidf_scores: Dict[int, float] = defaultdict(float)
        for token in query_tokens:
            idf = self._compute_idf(token)
            docs_with_token = self.inverted_index.get(token, {})
            for doc_id, freq in docs_with_token.items():
                bm25_score = self._score_bm25(token, doc_id, freq, idf)
                doc_scores[doc_id] += bm25_score
                tfidf_score = self._score_tfidf(token, doc_id, freq, idf)
                doc_tfidf_scores[doc_id] += tfidf_score
        # Combine BM25 and TF-IDF scores (weighted average)
        results = []
        for doc_id in doc_scores:
            bm25 = doc_scores[doc_id]
            tfidf = doc_tfidf_scores[doc_id]
            doc = self.documents[doc_id]
            score = 0.7 * bm25 + 0.3 * tfidf
            snippet = self._make_snippet(doc.content, query_tokens)
            results.append(SearchResult(doc_id, score * doc.weight, doc.title, snippet))
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "total_documents": self.total_docs,
                "average_document_length": self.avg_doc_length,
                "unique_terms": len(self.inverted_index),
            }

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9_]+\b', text.lower())
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, term: str, doc_id: int, freq: int, idf: float) -> float:
        doc_length = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        numerator = freq * (self.k1 + 1)
        denominator = freq + self.k1 * (1 - self.b + self.b * doc_length / avg_dl)
        return idf * numerator / denominator if denominator > 0 else 0.0

    def _score_tfidf(self, term: str, doc_id: int, freq: int, idf: float) -> float:
        doc_length = self.doc_lengths.get(doc_id, 0)
        tf = freq / doc_length if doc_length > 0 else 0.0
        return tf * idf

    def _make_snippet(self, content: str, query_tokens: List[str], max_len: int = 160) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            snippet = ' '.join(tokens[:max_len])
        else:
            start = max(positions[0] - 10, 0)
            end = min(start + max_len, len(tokens))
            snippet = ' '.join(tokens[start:end])
        return snippet[:max_len] + ('...' if len(snippet) > max_len else '')

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
            1, "Crude Oil Assay & TBP Distillation",
            "Crude oil assay involves the detailed analysis of crude oil composition and properties. TBP (True Boiling Point) distillation separates crude into fractions based on boiling points, providing essential data for refinery operations.",
            ["crude", "assay", "tbp", "distillation", "analysis"], 1.0
        ),
        SearchDocument(
            2, "Atmospheric Distillation Column Tray Efficiency",
            "Tray efficiency in atmospheric distillation columns affects separation quality. Factors include tray design, vapor-liquid contact, and operational parameters. Efficiency impacts product yields and energy consumption.",
            ["distillation", "tray", "efficiency", "atmospheric"], 1.0
        ),
        SearchDocument(
            3, "Vacuum Distillation Reduced Crude",
            "Vacuum distillation processes reduced crude from atmospheric distillation to separate heavier fractions. Operating under reduced pressure prevents thermal cracking and enables recovery of gasoil and residuum.",
            ["vacuum", "distillation", "reduced crude", "gasoil", "residuum"], 1.0
        ),
        SearchDocument(
            4, "Fluid Catalytic Cracking (FCC) Conversion & Octane",
            "FCC converts heavy gasoil into lighter products such as gasoline and LPG. The process enhances octane rating and produces valuable olefins. Catalyst selection and operating conditions optimize conversion and product quality.",
            ["fcc", "conversion", "octane", "gasoline", "olefins"], 1.0
        ),
        SearchDocument(
            5, "Hydrocracking Diesel Production",
            "Hydrocracking employs hydrogen and catalysts to convert heavy fractions into diesel and other light products. The process improves cetane number and reduces sulfur content, meeting stringent fuel specifications.",
            ["hydrocracking", "diesel", "hydrogen", "catalyst", "cetane"], 1.0
        ),
        SearchDocument(
            6, "Kerosene & Jet Fuel Refining",
            "Kerosene and jet fuel are produced via distillation and hydrotreating. Key properties include flash point, freezing point, and smoke point. Refining ensures compliance with aviation fuel standards.",
            ["kerosene", "jet fuel", "refining", "hydrotreating"], 1.0
        ),
        SearchDocument(
            7, "Catalytic Reforming Naphtha & Aromatics",
            "Catalytic reforming transforms naphtha into high-octane gasoline and aromatics. The process increases octane and produces benzene, toluene, and xylenes. Catalyst activity and selectivity are critical for yield.",
            ["reforming", "naphtha", "aromatics", "octane", "catalyst"], 1.0
        ),
        SearchDocument(
            8, "Alkylation HF/H2SO4 Isobutane Olefin",
            "Alkylation combines isobutane and olefins using HF or H2SO4 catalysts to produce high-octane alkylate. The process is essential for blending premium gasoline. Safety and acid management are key considerations.",
            ["alkylation", "hf", "h2so4", "isobutane", "olefin"], 1.0
        ),
        SearchDocument(
            9, "Isomerization Light Naphtha RON Improvement",
            "Isomerization converts straight-chain hydrocarbons in light naphtha to branched isomers, improving Research Octane Number (RON). The process uses platinum catalysts and moderate temperatures.",
            ["isomerization", "naphtha", "ron", "octane", "platinum"], 1.0
        ),
        SearchDocument(
            10, "Delayed Coking Process",
            "Delayed coking thermally cracks heavy residues to produce lighter products and petroleum coke. The process operates in coke drums at high temperatures, maximizing conversion and minimizing coke yield.",
            ["coking", "delayed", "thermal cracking", "petroleum coke"], 1.0
        ),
        SearchDocument(
            11, "Fluid Coking & Flexicoking",
            "Fluid coking and flexicoking convert heavy residues into lighter hydrocarbons and coke. Flexicoking integrates gasification, producing syngas for refinery fuel. Both processes enhance residue utilization.",
            ["fluid coking", "flexicoking", "residue", "syngas"], 1.0
        ),
        SearchDocument(
            12, "Conradson Carbon Residue",
            "Conradson carbon residue measures the amount of carbon left after oil is heated in the absence of air. It indicates coke-forming tendencies and is used to assess feedstock quality for coking and FCC units.",
            ["conradson", "carbon residue", "coking", "fcc"], 1.0
        ),
        SearchDocument(
            13, "Hydrotreating Desulfurization HDS HDN HDM",
            "Hydrotreating removes sulfur, nitrogen, and metals from petroleum fractions. HDS (hydrodesulfurization), HDN (hydrodenitrogenation), and HDM (hydrodemetallization) processes use hydrogen and catalysts to improve product quality.",
            ["hydrotreating", "hds", "hdn", "hdm", "desulfurization"], 1.0
        ),
        SearchDocument(
            14, "Hydrogen Plant SMR PSA Steam Methane Reforming",
            "Hydrogen plants use Steam Methane Reforming (SMR) to produce hydrogen from natural gas. Pressure Swing Adsorption (PSA) purifies hydrogen for refinery use. SMR is the primary source of hydrogen in refining.",
            ["hydrogen", "smr", "psa", "steam methane reforming"], 1.0
        ),
        SearchDocument(
            15, "Sulfur Recovery Claus Process Tail Gas Treating",
            "The Claus process recovers sulfur from acid gas streams. Tail gas treating units further reduce emissions by converting residual sulfur compounds. Efficient sulfur recovery is vital for environmental compliance.",
            ["sulfur", "claus", "tail gas", "recovery", "environment"], 1.0
        ),
        SearchDocument(
            16, "Amine Treating MEA DEA MDEA Acid Gas",
            "Amine treating uses MEA, DEA, or MDEA to remove hydrogen sulfide and carbon dioxide from gas streams. The process is essential for acid gas removal and ensures compliance with emission standards.",
            ["amine", "mea", "dea", "mdea", "acid gas", "treating"], 1.0
        ),
        SearchDocument(
            17, "Merox Sweetening Mercaptan Oxidation",
            "Merox sweetening oxidizes mercaptans in LPG, gasoline, and kerosene, improving odor and stability. The process uses catalysts and air to convert mercaptans to disulfides, enhancing product quality.",
            ["merox", "sweetening", "mercaptan", "oxidation", "lpg"], 1.0
        ),
        SearchDocument(
            18, "Blending Gasoline, Diesel, Jet Fuel Specifications",
            "Blending combines refinery streams to meet gasoline, diesel, and jet fuel specifications. Parameters include octane, cetane, sulfur content, and volatility. Optimization ensures compliance and maximizes margin.",
            ["blending", "gasoline", "diesel", "jet fuel", "specifications"], 1.0
        ),
        SearchDocument(
            19, "Crude Scheduling Linear Programming Optimization",
            "Linear programming optimizes crude scheduling and refinery operations. Models balance feedstock selection, product yields, and constraints to maximize profitability. Scheduling impacts margin and logistics.",
            ["crude", "scheduling", "linear programming", "optimization"], 1.0
        ),
        SearchDocument(
            20, "Refinery Margin Crack Spread 3-2-1",
            "Crack spread measures refinery margin by comparing crude input and product output values. The 3-2-1 crack spread uses three barrels of crude, two of gasoline, and one of diesel to assess profitability.",
            ["refinery", "margin", "crack spread", "profitability"], 1.0
        ),
        SearchDocument(
            21, "Energy Integration Pinch Analysis Heat Exchanger Network",
            "Pinch analysis optimizes heat exchanger networks for energy integration. Identifying pinch points minimizes utility consumption and improves efficiency. Heat recovery is crucial for sustainable operations.",
            ["energy", "pinch analysis", "heat exchanger", "integration"], 1.0
        ),
        SearchDocument(
            22, "Environmental Compliance SOx NOx VOC Wastewater",
            "Refineries must comply with environmental regulations for SOx, NOx, VOC, and wastewater. Technologies include scrubbers, catalytic reduction, and biological treatment. Compliance reduces emissions and protects the environment.",
            ["environmental", "compliance", "sox", "nox", "voc", "wastewater"], 1.0
        ),
        SearchDocument(
            23, "Turnaround Planning Maintenance Scheduling Critical Path",
            "Turnaround planning schedules maintenance and upgrades for refinery units. Critical path analysis ensures timely completion and minimizes downtime. Effective planning improves reliability and safety.",
            ["turnaround", "planning", "maintenance", "scheduling", "critical path"], 1.0
        ),
        SearchDocument(
            24, "Residuum Upgrading Technologies",
            "Residuum upgrading converts heavy fractions into lighter, more valuable products. Technologies include hydrocracking, coking, and gasification. Upgrading maximizes refinery yield and profitability.",
            ["residuum", "upgrading", "hydrocracking", "coking", "gasification"], 1.0
        ),
        SearchDocument(
            25, "FCC Catalyst Regeneration",
            "FCC catalyst regeneration restores activity by burning off coke deposits. Proper regeneration is essential for maintaining conversion rates and product quality. Regeneration systems include air blowers and cyclones.",
            ["fcc", "catalyst", "regeneration", "coke", "conversion"], 1.0
        ),
        SearchDocument(
            26, "Diesel Hydrotreating Process",
            "Diesel hydrotreating removes sulfur and nitrogen compounds to meet ultra-low sulfur diesel specifications. The process uses hydrogen and catalysts, improving fuel quality and environmental compliance.",
            ["diesel", "hydrotreating", "sulfur", "nitrogen", "ultra-low sulfur"], 1.0
        ),
        SearchDocument(
            27, "Gasoline Pool Optimization",
            "Gasoline pool optimization blends streams from FCC, reforming, alkylation, and isomerization units to achieve desired octane and vapor pressure. Optimization maximizes margin and meets regulatory requirements.",
            ["gasoline", "pool", "optimization", "octane", "vapor pressure"], 1.0
        ),
        SearchDocument(
            28, "Jet Fuel Thermal Stability",
            "Jet fuel thermal stability is critical for aviation safety. Stability is assessed by testing for deposit formation at high temperatures. Additives and hydrotreating improve stability and performance.",
            ["jet fuel", "thermal stability", "aviation", "hydrotreating"], 1.0
        ),
        SearchDocument(
            29, "FCC Gasoline Desulfurization",
            "FCC gasoline desulfurization reduces sulfur content in FCC-produced gasoline. Processes include selective hydrodesulfurization and post-treatment. Compliance with sulfur regulations is essential for marketability.",
            ["fcc", "gasoline", "desulfurization", "hydrodesulfurization"], 1.0
        ),
        SearchDocument(
            30, "Refinery Wastewater Treatment",
            "Refinery wastewater treatment removes contaminants such as hydrocarbons, phenols, and heavy metals. Technologies include biological treatment, filtration, and chemical oxidation. Effective treatment ensures environmental compliance.",
            ["refinery", "wastewater", "treatment", "environmental"], 1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)