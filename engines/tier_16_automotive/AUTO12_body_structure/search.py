import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

# --- Data Classes ---

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

# --- Search Index Implementation ---

class SearchIndex:
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_tokens: Dict[int, List[str]] = {}
        self.inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.df: Dict[str, int] = defaultdict(int)
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + ' ' + doc.content)
            self.documents[doc.id] = doc
            self.doc_tokens[doc.id] = tokens
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.inverted_index[term].add(doc.id)
                self.df[term] += 1
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidate_doc_ids = set()
        for term in query_terms:
            candidate_doc_ids.update(self.inverted_index.get(term, set()))
        scored_results = []
        for doc_id in candidate_doc_ids:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc = self.documents[doc_id]
            total_score = bm25_score * 0.7 + tfidf_score * 0.3
            snippet = self._make_snippet(doc, query_terms)
            scored_results.append(SearchResult(doc_id, total_score * doc.weight, doc.title, snippet))
        scored_results.sort(key=lambda r: r.score, reverse=True)
        return scored_results[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "num_documents": self.N,
                "avg_doc_length": self.avg_doc_length,
                "vocab_size": len(self.df)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.df.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        for term in query_terms:
            idf = self._compute_idf(term)
            freq = tf.get(term, 0)
            numerator = freq * (self._bm25_k1 + 1)
            denominator = freq + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / avg_dl)
            if denominator == 0:
                continue
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            tf_norm = tf.get(term, 0) / doc_len if doc_len > 0 else 0.0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        content_tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(content_tokens) if t in query_terms]
        if not positions:
            snippet = content[:window * 2]
            return snippet + "..." if len(content) > window * 2 else snippet
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(content_tokens))
        snippet_tokens = content_tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        return snippet + "..."

# --- Singleton Factory ---

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

# --- Pre-seed Documents ---

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Body-in-White Design Principles",
            "Body-in-white (BIW) refers to the stage in automotive design where the car body's sheet metal components are welded together. Key principles include structural integrity, crashworthiness, manufacturability, and weight optimization.",
            ["body_in_white_design_principles", "structural_integrity"],
            1.0
        ),
        SearchDocument(
            2,
            "Frontal Crash Structure Design Fundamentals",
            "Frontal crash structures are engineered to absorb impact energy and protect occupants. Design focuses on crumple zones, load paths, and material selection to maximize safety and minimize intrusion.",
            ["frontal_crash_structure_design", "crashworthiness"],
            1.0
        ),
        SearchDocument(
            3,
            "Side Impact Structure Design",
            "Side impact protection involves reinforced door beams, B-pillars, and energy-absorbing materials. The structure must dissipate lateral forces and maintain occupant survival space.",
            ["side_impact_structure_design", "occupant_protection"],
            1.0
        ),
        SearchDocument(
            4,
            "Roof Crush and Rollover Protection",
            "Roof structures are strengthened using high-strength steel and optimized cross-sections to resist deformation during rollovers. Regulatory tests such as FMVSS 216 guide design requirements.",
            ["roof_crush_and_rollover_protection", "safety"],
            1.0
        ),
        SearchDocument(
            5,
            "Corrosion Protection Strategies in BIW",
            "Corrosion protection employs coatings, sealants, and material selection. Galvanization, cathodic protection, and design for drainage are critical to extending vehicle life.",
            ["corrosion_protection_strategies", "durability"],
            1.0
        ),
        SearchDocument(
            6,
            "NVH Contribution of Body Structure",
            "Noise, vibration, and harshness (NVH) are influenced by the body structure's stiffness, damping, and joint quality. Optimized weld patterns and reinforcements reduce cabin noise.",
            ["nvh_body_structure_contribution", "comfort"],
            1.0
        ),
        SearchDocument(
            7,
            "Aerodynamic Body Optimization",
            "Aerodynamic efficiency is achieved through smooth body contours, underbody panels, and active aerodynamic elements. Reducing drag improves fuel economy and high-speed stability.",
            ["aerodynamic_body_optimization", "efficiency"],
            1.0
        ),
        SearchDocument(
            8,
            "Structural Durability and Fatigue",
            "Durability analysis ensures the body structure withstands repeated loads over the vehicle's life. Fatigue hotspots are addressed through material upgrades and geometry refinement.",
            ["structural_durability_and_fatigue", "lifecycle"],
            1.0
        ),
        SearchDocument(
            9,
            "Advanced High-Strength Steel Selection",
            "Advanced high-strength steels (AHSS) offer superior strength-to-weight ratios. Selection considers formability, weldability, and crash performance for optimal BIW design.",
            ["advanced_high_strength_steel_selection", "materials"],
            1.0
        ),
        SearchDocument(
            10,
            "Joining Methods Comparison in BIW",
            "Joining methods include spot welding, laser welding, adhesives, and mechanical fasteners. Selection depends on material compatibility, joint strength, and manufacturing cost.",
            ["joining_methods_comparison", "manufacturing"],
            1.0
        ),
        SearchDocument(
            11,
            "Body Structure Weight Optimization",
            "Weight optimization balances safety, cost, and performance. Techniques include topology optimization, material substitution, and part consolidation.",
            ["body_structure_weight_optimization", "lightweighting"],
            1.0
        ),
        SearchDocument(
            12,
            "Crash Load Path Management",
            "Effective load path management directs crash forces away from occupants. Strategic reinforcement and geometry control are essential for crashworthiness.",
            ["frontal_crash_structure_design", "load_path"],
            1.0
        ),
        SearchDocument(
            13,
            "Multi-Material BIW Construction",
            "Combining steel, aluminum, and composites in BIW construction reduces weight while maintaining strength. Joining dissimilar materials requires advanced techniques.",
            ["body_in_white_design_principles", "multi_material"],
            1.0
        ),
        SearchDocument(
            14,
            "B-Pillar Reinforcement for Side Impact",
            "B-pillar design uses ultra-high-strength steel and tailored blanks to maximize side impact protection. Local reinforcements improve intrusion resistance.",
            ["side_impact_structure_design", "b_pillar"],
            1.0
        ),
        SearchDocument(
            15,
            "Sealing and Drainage for Corrosion Prevention",
            "Effective sealing and drainage prevent water ingress and accumulation, reducing corrosion risk. Design features include hem flanges, drain holes, and seam sealers.",
            ["corrosion_protection_strategies", "sealing"],
            1.0
        ),
        SearchDocument(
            16,
            "Laser Welding in Body Assembly",
            "Laser welding offers precise, high-speed joining with minimal heat distortion. It is suitable for complex joints and mixed-material assemblies.",
            ["joining_methods_comparison", "laser_welding"],
            1.0
        ),
        SearchDocument(
            17,
            "Topology Optimization for Lightweight BIW",
            "Topology optimization algorithms remove unnecessary material while maintaining strength. This approach leads to innovative, lightweight body structures.",
            ["body_structure_weight_optimization", "topology_optimization"],
            1.0
        ),
        SearchDocument(
            18,
            "Fatigue Testing Protocols",
            "Fatigue testing simulates real-world loading to identify potential failure points. Common protocols include block loading and variable amplitude testing.",
            ["structural_durability_and_fatigue", "testing"],
            1.0
        ),
        SearchDocument(
            19,
            "Active Aerodynamics in Modern Vehicles",
            "Active aerodynamic systems, such as grille shutters and adjustable spoilers, dynamically optimize airflow for efficiency and performance.",
            ["aerodynamic_body_optimization", "active_aero"],
            1.0
        ),
        SearchDocument(
            20,
            "NVH Simulation Techniques",
            "Finite element analysis and multi-body dynamics are used to simulate NVH behavior. Early prediction enables targeted structural improvements.",
            ["nvh_body_structure_contribution", "simulation"],
            1.0
        ),
        SearchDocument(
            21,
            "Cathodic Protection in Automotive Bodies",
            "Cathodic protection uses sacrificial anodes or impressed current to prevent corrosion. It is especially useful in harsh environments.",
            ["corrosion_protection_strategies", "cathodic_protection"],
            1.0
        ),
        SearchDocument(
            22,
            "Crashworthiness Regulations Overview",
            "Global crashworthiness standards, such as Euro NCAP and FMVSS, dictate minimum performance for frontal, side, and rollover events.",
            ["frontal_crash_structure_design", "side_impact_structure_design", "roof_crush_and_rollover_protection", "regulations"],
            1.0
        ),
        SearchDocument(
            23,
            "Adhesive Bonding in BIW",
            "Structural adhesives distribute loads and improve fatigue resistance. They are often used in combination with spot welding.",
            ["joining_methods_comparison", "adhesives"],
            1.0
        ),
        SearchDocument(
            24,
            "Formability of Advanced High-Strength Steels",
            "Formability challenges of AHSS are addressed through tailored blanks, hot stamping, and advanced forming simulations.",
            ["advanced_high_strength_steel_selection", "formability"],
            1.0
        ),
        SearchDocument(
            25,
            "BIW Stiffness and Vehicle Handling",
            "A stiff BIW improves handling, NVH, and crash performance. Key metrics include torsional and bending stiffness.",
            ["body_in_white_design_principles", "nvh_body_structure_contribution"],
            1.0
        ),
        SearchDocument(
            26,
            "Spot Welding Fundamentals",
            "Spot welding is the most common joining method in BIW assembly. It provides reliable joints for steel structures.",
            ["joining_methods_comparison", "spot_welding"],
            1.0
        ),
        SearchDocument(
            27,
            "Crash Energy Management Materials",
            "Materials such as TRIP and DP steels are used in zones requiring high energy absorption during crashes.",
            ["frontal_crash_structure_design", "advanced_high_strength_steel_selection"],
            1.0
        ),
        SearchDocument(
            28,
            "BIW Lifecycle Assessment",
            "Lifecycle assessment evaluates the environmental impact of BIW materials and processes, guiding sustainable design choices.",
            ["body_in_white_design_principles", "structural_durability_and_fatigue"],
            1.0
        ),
        SearchDocument(
            29,
            "Rivet Bonding for Mixed-Material Joints",
            "Rivet bonding combines mechanical fasteners with adhesives for joining aluminum and steel in BIW.",
            ["joining_methods_comparison", "multi_material"],
            1.0
        ),
        SearchDocument(
            30,
            "Crash Simulation in BIW Development",
            "Crash simulation tools predict deformation, intrusion, and energy absorption, enabling virtual optimization of BIW structures.",
            ["frontal_crash_structure_design", "simulation"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)