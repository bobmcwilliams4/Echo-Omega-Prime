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
        self.doc_lengths: Dict[int, int] = {}
        self.term_doc_freqs: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.doc_tags: Dict[int, List[str]] = {}
        self.doc_weights: Dict[int, float] = {}
        self.total_docs: int = 0
        self.avg_doc_length: float = 0.0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._precomputed_stats = False

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.doc_tags[doc.id] = doc.tags
            self.doc_weights[doc.id] = doc.weight
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            for term in tf:
                self.term_doc_freqs[term][doc.id] = tf[term]
            self.total_docs += 1
            self._precomputed_stats = False

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = len(self.term_doc_freqs.get(term, {}))
        if df == 0:
            return 0.0
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int, k1=1.5, b=0.75) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        avgdl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        tf = self.term_freqs.get(doc_id, Counter())
        weight = self.doc_weights.get(doc_id, 1.0)
        for term in query_terms:
            f = tf.get(term, 0)
            idf = self._compute_idf(term)
            numerator = f * (k1 + 1)
            denominator = f + k1 * (1 - b + b * doc_length / avgdl)
            if denominator == 0:
                continue
            score += idf * (numerator / denominator)
        return score * weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs.get(doc_id, Counter())
        doc_length = self.doc_lengths.get(doc_id, 1)
        weight = self.doc_weights.get(doc_id, 1.0)
        score = 0.0
        for term in query_terms:
            term_tf = tf.get(term, 0) / doc_length
            idf = self._compute_idf(term)
            score += term_tf * idf
        return score * weight

    def search(self, query: str, limit: int = 10, method: str = "bm25") -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        with self.lock:
            if not self._precomputed_stats:
                self._update_stats()
        doc_scores = {}
        for doc_id in self.documents:
            if method == "bm25":
                score = self._score_bm25(query_terms, doc_id)
            elif method == "tfidf":
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                doc_scores[doc_id] = score
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str], length: int = 160) -> str:
        tokens = self._tokenize(content)
        indices = [i for i, t in enumerate(tokens) if t in query_terms]
        if not indices:
            return content[:length] + ("..." if len(content) > length else "")
        start = max(indices[0] - 10, 0)
        end = min(indices[0] + 20, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        if len(snippet) > length:
            snippet = snippet[:length] + "..."
        return snippet

    def _update_stats(self):
        total_length = sum(self.doc_lengths.values())
        self.avg_doc_length = total_length / self.total_docs if self.total_docs > 0 else 1.0
        self._idf_cache = {}
        self._precomputed_stats = True

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            self._update_stats()
            return {
                "total_docs": self.total_docs,
                "avg_doc_length": self.avg_doc_length,
                "unique_terms": len(self.term_doc_freqs),
            }

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_frac02_documents(_search_index_instance)
        return _search_index_instance

def _seed_frac02_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Northern White Sand Selection",
            "Northern White Sand is preferred for its high purity and roundness, offering superior conductivity and crush resistance compared to regional brown sand. Selection criteria include API RP 19C compliance, mesh size, and logistics optimization.",
            ["northern_white_sand", "conductivity", "api_rp_19c", "logistics"],
            1.0
        ),
        SearchDocument(
            2,
            "Regional Brown Sand Advantages",
            "Regional Brown Sand is locally sourced, reducing transportation costs. Though it has lower purity and roundness than Northern White, it is suitable for formations with moderate closure stress. Logistics and mine proximity are key factors.",
            ["regional_brown_sand", "logistics", "mine_proximity"],
            0.9
        ),
        SearchDocument(
            3,
            "Mesh Size Selection: 20/40 vs 30/50",
            "Mesh size impacts proppant transport and fracture conductivity. 20/40 mesh offers higher permeability but may settle faster in non-Newtonian fluids. 30/50 mesh balances transport and pack strength for most shale plays.",
            ["mesh_size", "transport", "conductivity", "non_newtonian"],
            1.0
        ),
        SearchDocument(
            4,
            "40/70 Mesh Sand for Tight Formations",
            "40/70 mesh is optimal for tight formations requiring high pack strength and minimal fines migration. Its smaller size enhances embedment resistance and long-term conductivity.",
            ["mesh_size", "tight_formations", "embedment", "fines_migration"],
            1.0
        ),
        SearchDocument(
            5,
            "100 Mesh Sand in Slickwater Fracs",
            "100 mesh sand is used in slickwater fracturing for initial proppant placement. Its fine size aids transport but is prone to pack damage and fines migration under high closure stress.",
            ["100_mesh", "slickwater", "fines_migration", "pack_damage"],
            0.95
        ),
        SearchDocument(
            6,
            "Resin-Coated Sand (RCS) for Flowback Control",
            "RCS mitigates proppant flowback by forming a resin shell around sand grains. It is effective in wells with high flowback risk and can reduce pack damage and fines generation.",
            ["rcs", "flowback_control", "pack_damage", "fines"],
            1.0
        ),
        SearchDocument(
            7,
            "Ceramic Proppants: Lightweight vs High-Strength",
            "Ceramic proppants are engineered for high closure stress environments. Lightweight ceramics offer improved transport, while high-strength ceramics resist crush and embedment, maintaining long-term conductivity.",
            ["ceramic", "lightweight", "high_strength", "embedment", "conductivity"],
            1.0
        ),
        SearchDocument(
            8,
            "Intermediate Strength Ceramic Proppants",
            "Intermediate ceramics balance cost and performance, suitable for formations with moderate closure stress. They provide better crush resistance than sand and maintain pack integrity.",
            ["ceramic", "intermediate", "crush_resistance", "pack_integrity"],
            0.98
        ),
        SearchDocument(
            9,
            "Proppant Concentration Scheduling",
            "Proppant concentration per stage is scheduled based on formation properties and fracture geometry. Ramp design optimizes transport and minimizes premature screenout. Typical concentrations range from 1.5 to 5 PPA.",
            ["concentration", "scheduling", "ramp_design", "screenout"],
            1.0
        ),
        SearchDocument(
            10,
            "API RP 19C Proppant Testing",
            "API RP 19C outlines standardized tests for proppant properties including crush resistance, sphericity, roundness, and conductivity. Compliance ensures proppant suitability for hydraulic fracturing.",
            ["api_rp_19c", "testing", "crush", "sphericity", "roundness"],
            1.0
        ),
        SearchDocument(
            11,
            "ISO 13503-2 Proppant Specifications",
            "ISO 13503-2 complements API standards, specifying test procedures for proppant performance. It includes methods for measuring fines generation, pack permeability, and embedment resistance.",
            ["iso_13503_2", "specifications", "fines", "embedment"],
            0.97
        ),
        SearchDocument(
            12,
            "Proppant Transport in Non-Newtonian Fluids",
            "Non-Newtonian fluids enhance proppant suspension and transport. Viscosity and shear-thinning properties are critical for preventing settling and optimizing placement in fractures.",
            ["transport", "non_newtonian", "viscosity", "placement"],
            1.0
        ),
        SearchDocument(
            13,
            "Proppant Settling and Placement",
            "Proppant settling is influenced by fluid rheology, mesh size, and density. Proper ramp design and fluid selection reduce settling and improve fracture coverage.",
            ["settling", "placement", "ramp_design", "fluid_selection"],
            0.98
        ),
        SearchDocument(
            14,
            "Proppant Embedment in Soft Formations",
            "Soft formations increase proppant embedment risk, reducing fracture conductivity. High-strength proppants and resin coatings mitigate embedment and maintain pack structure.",
            ["embedment", "soft_formations", "conductivity", "rcs"],
            1.0
        ),
        SearchDocument(
            15,
            "Fines Migration and Pack Damage",
            "Fines migration occurs when proppant packs are damaged by high closure stress or flowback. Selecting appropriate mesh size and resin coatings reduces fines generation and maintains permeability.",
            ["fines_migration", "pack_damage", "mesh_size", "rcs"],
            1.0
        ),
        SearchDocument(
            16,
            "Long-Term Conductivity Degradation",
            "Conductivity degradation results from proppant crush, embedment, and diagenesis. High-strength ceramics and resin coatings improve long-term performance in challenging formations.",
            ["conductivity", "degradation", "crush", "embedment", "diagenesis"],
            1.0
        ),
        SearchDocument(
            17,
            "In-Basin Sand Mines and Logistics",
            "In-basin sand mines reduce transportation costs and supply chain risks. Logistics optimization includes mine proximity, rail access, and storage capacity for efficient proppant delivery.",
            ["in_basin", "logistics", "mine_proximity", "supply_chain"],
            1.0
        ),
        SearchDocument(
            18,
            "Proppant Logistics Optimization",
            "Optimizing proppant logistics involves balancing cost, delivery time, and storage. In-basin sourcing and digital tracking improve supply reliability and reduce operational delays.",
            ["logistics", "optimization", "in_basin", "tracking"],
            1.0
        ),
        SearchDocument(
            19,
            "Proppant Concentration per Lateral Foot",
            "Proppant concentration per lateral foot is calculated to maximize fracture coverage and conductivity. Typical values range from 1,200 to 2,500 lbs/ft, adjusted for formation stress and geometry.",
            ["concentration", "lateral_foot", "coverage", "conductivity"],
            1.0
        ),
        SearchDocument(
            20,
            "Tail-In Strategy with Higher Concentration Proppant",
            "Tail-in strategies use higher concentration proppant in final stages to enhance fracture conductivity and prevent screenout. Selection of mesh size and proppant type is critical for effectiveness.",
            ["tail_in", "concentration", "screenout", "mesh_size"],
            1.0
        ),
        SearchDocument(
            21,
            "Proppant Pack Integrity and Fines Control",
            "Maintaining pack integrity reduces fines migration and preserves permeability. Resin coatings and optimized mesh size selection are effective for fines control in high-stress environments.",
            ["pack_integrity", "fines_control", "rcs", "mesh_size"],
            1.0
        ),
        SearchDocument(
            22,
            "Proppant Testing: Sphericity and Roundness",
            "Sphericity and roundness are measured to assess proppant quality. Higher values indicate better transport and pack structure, reducing embedment and crush risk.",
            ["testing", "sphericity", "roundness", "quality"],
            1.0
        ),
        SearchDocument(
            23,
            "Crush Resistance in Proppant Selection",
            "Crush resistance is a key parameter for proppant selection. High-strength ceramics and Northern White Sand offer superior resistance to closure stress and maintain fracture conductivity.",
            ["crush_resistance", "ceramic", "northern_white_sand", "conductivity"],
            1.0
        ),
        SearchDocument(
            24,
            "Diagenesis Impact on Proppant Packs",
            "Diagenesis alters proppant pack structure over time, affecting conductivity. Selecting stable proppant types and resin coatings mitigates diagenetic effects.",
            ["diagenesis", "pack_structure", "conductivity", "rcs"],
            0.97
        ),
        SearchDocument(
            25,
            "Digital Tracking in Proppant Logistics",
            "Digital tracking systems enhance proppant logistics by monitoring delivery, inventory, and mine output. Real-time data improves supply chain efficiency and reduces operational risks.",
            ["digital_tracking", "logistics", "supply_chain", "inventory"],
            0.98
        ),
        SearchDocument(
            26,
            "Proppant Ramp Design for Screenout Prevention",
            "Ramp design involves gradually increasing proppant concentration to optimize transport and prevent screenout. Fluid rheology and mesh size selection are critical for successful ramp implementation.",
            ["ramp_design", "screenout", "transport", "mesh_size"],
            1.0
        ),
        SearchDocument(
            27,
            "Proppant Placement in Horizontal Wells",
            "Placement strategies in horizontal wells focus on maximizing coverage and conductivity. Mesh size, fluid selection, and ramp design are tailored to formation properties.",
            ["placement", "horizontal_wells", "coverage", "conductivity"],
            1.0
        ),
        SearchDocument(
            28,
            "Fines Generation and Proppant Pack Damage",
            "Fines generation is minimized by selecting high-quality proppants and resin coatings. Pack damage is monitored through API RP 19C and ISO 13503-2 testing protocols.",
            ["fines_generation", "pack_damage", "testing", "rcs"],
            1.0
        ),
        SearchDocument(
            29,
            "Proppant Sourcing: In-Basin vs Out-of-Basin",
            "In-basin sourcing reduces logistics costs and improves supply reliability. Out-of-basin proppants may offer higher quality but incur greater transportation expenses.",
            ["sourcing", "in_basin", "out_of_basin", "logistics"],
            0.99
        ),
        SearchDocument(
            30,
            "Proppant Pack Permeability Optimization",
            "Pack permeability is optimized by selecting appropriate mesh size, proppant type, and resin coatings. Testing per API RP 19C and ISO 13503-2 ensures long-term performance.",
            ["permeability", "mesh_size", "proppant_type", "rcs", "testing"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)