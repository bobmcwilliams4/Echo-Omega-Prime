import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

class SearchDocument:
    def __init__(self, id: int, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = id
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

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.doc_freqs[term] += 1
                self.inverted_index[term].add(doc.id)
            self.documents[doc.id] = doc
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, set()))
        scored: List[Tuple[int, float]] = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc = self.documents[doc_id]
            score = 0.7 * bm25_score + 0.3 * tfidf_score
            score *= doc.weight
            scored.append((doc_id, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "num_documents": self.N,
                "avg_doc_length": self.avg_doc_length,
                "vocab_size": len(self.doc_freqs)
            }

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

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

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        tf = self.term_freqs.get(doc_id, Counter())
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self.k1 * (1 - self.b + self.b * doc_len / avg_dl)
            score += idf * (f * (self.k1 + 1)) / denom
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        tf = self.term_freqs.get(doc_id, Counter())
        doc_len = self.doc_lengths.get(doc_id, 1)
        for term in query_terms:
            freq = tf.get(term, 0)
            if freq == 0:
                continue
            tf_norm = freq / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:200]
            return snippet + ("..." if len(content) > 200 else "")
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        return snippet + ("..." if end < len(tokens) else "")

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
            "MDEA vs DEA vs MEA: Amine Selection for Gas Sweetening",
            "Comparison of MDEA, DEA, and MEA for amine gas sweetening. MDEA offers selective H2S removal, lower energy consumption, and reduced corrosion. DEA and MEA are more reactive but less selective. Selection depends on feed gas composition, required H2S and CO2 removal, and operational economics.",
            ["amine", "sweetening", "MDEA", "DEA", "MEA", "selection"],
            1.0
        ),
        SearchDocument(
            2,
            "Designing a Triethylene Glycol (TEG) Dehydration System",
            "Key parameters in TEG dehydration system design include inlet water content, target dewpoint, TEG circulation rate, contactor tray design, and reboiler temperature. Proper selection ensures efficient water removal and prevents glycol degradation.",
            ["TEG", "dehydration", "design", "glycol"],
            1.0
        ),
        SearchDocument(
            3,
            "Turboexpander vs Mechanical Refrigeration for NGL Recovery",
            "Turboexpander processes provide higher ethane and propane recovery compared to mechanical refrigeration. Selection depends on feed gas composition, desired NGL recovery, and plant economics.",
            ["NGL", "turboexpander", "refrigeration", "process", "selection"],
            1.0
        ),
        SearchDocument(
            4,
            "Demethanizer Column Design and Operation",
            "Demethanizer columns separate methane from NGLs using cryogenic distillation. Key design factors include feed composition, reflux ratio, tray or packing selection, and heat integration.",
            ["demethanizer", "column", "design", "operation"],
            1.0
        ),
        SearchDocument(
            5,
            "Pipeline Quality Specifications: H2S, CO2, Water Dewpoint, BTU",
            "Pipeline quality specifications for natural gas include limits on H2S, CO2, water dewpoint, and heating value (BTU). Meeting these specs is essential for pipeline integrity and marketability.",
            ["pipeline", "specifications", "H2S", "CO2", "dewpoint", "BTU"],
            1.0
        ),
        SearchDocument(
            6,
            "Reciprocating vs Centrifugal Compressor Selection",
            "Reciprocating compressors are suitable for high-pressure, low-flow applications, while centrifugal compressors are preferred for high-flow, low-pressure ratio services. Selection is based on process requirements, efficiency, and maintenance considerations.",
            ["compressor", "reciprocating", "centrifugal", "selection"],
            1.0
        ),
        SearchDocument(
            7,
            "Claus Sulfur Recovery Process Overview",
            "The Claus process recovers elemental sulfur from acid gas streams containing H2S. It involves thermal and catalytic stages, with overall recovery typically 95-98%. Tail gas cleanup may be required for stringent sulfur emissions.",
            ["Claus", "sulfur", "recovery", "acid gas"],
            1.0
        ),
        SearchDocument(
            8,
            "Molecular Sieve Dehydration for Very Low Dewpoints",
            "Molecular sieves are used for dehydration when very low water dewpoints are required, such as for cryogenic processing. Proper bed design, regeneration, and protection from contaminants are critical.",
            ["molecular sieve", "dehydration", "dewpoint", "design"],
            1.0
        ),
        SearchDocument(
            9,
            "Gas Chromatograph Analysis and BTU Calculation (GPA 2172)",
            "Gas chromatographs analyze hydrocarbon composition. GPA 2172 provides methods for calculating heating value (BTU), specific gravity, and compressibility from component analysis.",
            ["gas chromatograph", "GPA 2172", "BTU", "analysis"],
            1.0
        ),
        SearchDocument(
            10,
            "Inlet Separation and Slug Catcher Design",
            "Inlet separators and slug catchers remove bulk liquids and slugs from gas streams. Proper sizing and configuration prevent downstream upsets and protect equipment.",
            ["inlet separation", "slug catcher", "design"],
            1.0
        ),
        SearchDocument(
            11,
            "Amine System Corrosion Control Strategies",
            "Corrosion in amine systems can be mitigated by controlling oxygen ingress, maintaining proper amine concentration, and using corrosion inhibitors. Material selection is also important.",
            ["amine", "corrosion", "control"],
            1.0
        ),
        SearchDocument(
            12,
            "TEG Regeneration and Reboiler Operation",
            "Efficient TEG regeneration requires proper reboiler temperature control to minimize glycol losses and prevent thermal degradation. Stripping gas may be used to achieve low water content.",
            ["TEG", "regeneration", "reboiler", "operation"],
            1.0
        ),
        SearchDocument(
            13,
            "Acid Gas Enrichment Prior to Claus Unit",
            "Acid gas enrichment increases H2S concentration to improve Claus unit performance. Typical methods include selective absorption and stripping.",
            ["acid gas", "enrichment", "Claus"],
            1.0
        ),
        SearchDocument(
            14,
            "BTEX and Heavy Hydrocarbon Management in TEG Systems",
            "BTEX and heavy hydrocarbons can contaminate TEG and cause emissions issues. Proper design and operation of flash tanks and stripping columns help control these contaminants.",
            ["TEG", "BTEX", "hydrocarbons", "management"],
            1.0
        ),
        SearchDocument(
            15,
            "Amine System Foaming: Causes and Prevention",
            "Foaming in amine systems is caused by hydrocarbon, surfactant, or particulate contamination. Prevention includes upstream separation, filtration, and antifoam injection.",
            ["amine", "foaming", "prevention"],
            1.0
        ),
        SearchDocument(
            16,
            "TEG Contactor Internals: Trays vs Structured Packing",
            "TEG contactors may use trays or structured packing. Packing offers lower pressure drop and higher efficiency but may be more susceptible to channeling if not properly installed.",
            ["TEG", "contactor", "trays", "packing"],
            1.0
        ),
        SearchDocument(
            17,
            "Mercury Removal in Natural Gas Processing",
            "Mercury is removed using activated carbon or molecular sieve beds. Removal is critical to prevent corrosion of aluminum heat exchangers in cryogenic plants.",
            ["mercury", "removal", "natural gas"],
            1.0
        ),
        SearchDocument(
            18,
            "Lean/Rich Amine Heat Exchanger Design",
            "The lean/rich amine heat exchanger improves energy efficiency by recovering heat from the rich amine stream. Proper design minimizes fouling and maximizes heat recovery.",
            ["amine", "heat exchanger", "design"],
            1.0
        ),
        SearchDocument(
            19,
            "TEG System Emissions and Environmental Compliance",
            "TEG dehydration units can emit VOCs and hazardous air pollutants. Emissions control may require condensers, incinerators, or BTEX removal systems.",
            ["TEG", "emissions", "environmental", "compliance"],
            1.0
        ),
        SearchDocument(
            20,
            "Hydrate Prevention in Gas Processing",
            "Hydrate formation is prevented by dehydration, temperature control, or injection of inhibitors such as methanol or glycol. Hydrate blockages can disrupt operations.",
            ["hydrate", "prevention", "gas processing"],
            1.0
        ),
        SearchDocument(
            21,
            "Amine Reclaimer Operation and Maintenance",
            "Amines degrade over time, forming heat-stable salts and other contaminants. Reclaimers remove these impurities to maintain system performance.",
            ["amine", "reclaimer", "operation", "maintenance"],
            1.0
        ),
        SearchDocument(
            22,
            "NGL Fractionation Train Design",
            "NGL fractionation trains separate ethane, propane, butane, and heavier components using a series of distillation columns. Design considers feed composition and product specifications.",
            ["NGL", "fractionation", "design"],
            1.0
        ),
        SearchDocument(
            23,
            "Molecular Sieve Bed Regeneration Strategies",
            "Molecular sieve beds are regenerated using heated gas. Cycle time, temperature, and purge flow are optimized to maximize water removal and bed life.",
            ["molecular sieve", "regeneration", "dehydration"],
            1.0
        ),
        SearchDocument(
            24,
            "Tail Gas Treatment after Claus Process",
            "Tail gas treatment units (TGTU) recover additional sulfur and reduce emissions. Common technologies include SCOT and CBA processes.",
            ["tail gas", "Claus", "treatment"],
            1.0
        ),
        SearchDocument(
            25,
            "Gas Processing Plant Utilities: Air, Nitrogen, Steam",
            "Utilities such as instrument air, nitrogen, and steam are essential for safe and reliable gas processing plant operation.",
            ["utilities", "air", "nitrogen", "steam"],
            1.0
        ),
        SearchDocument(
            26,
            "Water Dewpoint Measurement Techniques",
            "Water dewpoint in natural gas is measured using chilled mirror, electrolytic, or spectroscopic analyzers. Accurate measurement is critical for dehydration system control.",
            ["water", "dewpoint", "measurement"],
            1.0
        ),
        SearchDocument(
            27,
            "Amine Solution Filtration and Solids Management",
            "Filtration removes particulates from amine solutions, preventing exchanger fouling and foaming. Cartridge or bag filters are commonly used.",
            ["amine", "filtration", "solids"],
            1.0
        ),
        SearchDocument(
            28,
            "TEG System Troubleshooting Guide",
            "Common TEG system issues include excessive glycol losses, foaming, and high water content. Troubleshooting involves checking for leaks, proper circulation, and reboiler operation.",
            ["TEG", "troubleshooting", "guide"],
            1.0
        ),
        SearchDocument(
            29,
            "Designing for Pipeline Gas BTU Specification",
            "Gas must meet pipeline BTU specifications, typically 950-1100 BTU/scf. Blending, NGL recovery, or inert removal may be required to adjust heating value.",
            ["pipeline", "BTU", "specification"],
            1.0
        ),
        SearchDocument(
            30,
            "Centrifugal Compressor Surge and Antisurge Control",
            "Centrifugal compressors require antisurge control to prevent flow reversal and mechanical damage. Control systems recycle gas to maintain safe operation.",
            ["centrifugal", "compressor", "surge", "control"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)