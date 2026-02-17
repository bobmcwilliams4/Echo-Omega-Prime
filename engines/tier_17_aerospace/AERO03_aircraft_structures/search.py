import math
import threading
import re
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
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_doc_tfs: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.doc_tags: Dict[str, List[str]] = {}
        self.doc_titles: Dict[str, str] = {}
        self.doc_weights: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._recompute_stats()

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9_]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.doc_tags[doc.id] = doc.tags
            self.doc_titles[doc.id] = doc.title
            self.doc_weights[doc.id] = doc.weight
            tf = Counter(tokens)
            for term, freq in tf.items():
                self.term_doc_freq[term] += 1
                self.term_doc_tfs[term][doc.id] = freq
            self._recompute_stats()

    def _recompute_stats(self):
        if self.documents:
            self.avg_doc_length = sum(self.doc_lengths.values()) / len(self.doc_lengths)
        else:
            self.avg_doc_length = 0.0

    def _compute_idf(self, term: str) -> float:
        N = len(self.documents)
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            return 0.0
        return math.log(1 + (N - df + 0.5) / (df + 0.5))

    def _score_bm25(self, query_terms: List[str], doc_id: str) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        weight = self.doc_weights.get(doc_id, 1.0)
        for term in query_terms:
            tf = self.term_doc_tfs.get(term, {}).get(doc_id, 0)
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_length / (self.avg_doc_length if self.avg_doc_length > 0 else 1))
            score += idf * (numerator / (denominator if denominator > 0 else 1))
        return score * weight

    def _score_tfidf(self, query_terms: List[str], doc_id: str) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        weight = self.doc_weights.get(doc_id, 1.0)
        for term in query_terms:
            tf = self.term_doc_tfs.get(term, {}).get(doc_id, 0)
            if doc_length > 0:
                tf_norm = tf / doc_length
            else:
                tf_norm = 0.0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * weight

    def search(self, query: str, limit: int = 10, method: str = 'bm25') -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[str, float] = {}
        for doc_id in self.documents:
            if method == 'bm25':
                score = self._score_bm25(query_terms, doc_id)
            elif method == 'tfidf':
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0.0:
                doc_scores[doc_id] = score
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str], max_length: int = 160) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = ' '.join(tokens[:max_length])
        else:
            start = max(positions[0] - 10, 0)
            end = min(start + max_length, len(tokens))
            snippet = ' '.join(tokens[start:end])
        return snippet

    def get_stats(self) -> Dict[str, float]:
        return {
            'num_documents': len(self.documents),
            'avg_doc_length': self.avg_doc_length,
            'num_terms': len(self.term_doc_freq),
        }

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
            id="safe_life_01",
            title="Safe Life Design Philosophy Overview",
            content="Safe life design philosophy ensures that aircraft structures are designed to withstand operational loads for a specified period without failure. No cracks or damage are allowed during the service life. This philosophy is commonly applied to landing gear and other critical components.",
            tags=["safe_life_design_philosophy", "structural_integrity"],
            weight=1.0
        ),
        SearchDocument(
            id="safe_life_02",
            title="Safe Life vs Fail Safe Approaches",
            content="Safe life design requires structures to be retired before any damage occurs, whereas fail safe design allows for continued operation with damage, provided redundancy exists. The choice depends on component criticality and inspection intervals.",
            tags=["safe_life_design_philosophy", "fail_safe_design_philosophy"],
            weight=1.0
        ),
        SearchDocument(
            id="fail_safe_01",
            title="Fail Safe Design Philosophy in Aircraft",
            content="Fail safe design philosophy incorporates redundant load paths so that if one element fails, others can carry the load. This approach relies on periodic inspections to detect damage before catastrophic failure.",
            tags=["fail_safe_design_philosophy", "redundancy"],
            weight=1.0
        ),
        SearchDocument(
            id="fail_safe_02",
            title="Fail Safe Design: Examples and Limitations",
            content="Examples of fail safe structures include multi-spar wings and fuselage skins with stringers. Limitations include increased weight and complexity, and the need for rigorous inspection schedules.",
            tags=["fail_safe_design_philosophy", "wing_structural_design_spar_rib_skin"],
            weight=1.0
        ),
        SearchDocument(
            id="damage_tolerant_01",
            title="Damage Tolerant Design Philosophy",
            content="Damage tolerant design philosophy assumes cracks or damage may exist and ensures structures can tolerate them until detected and repaired. This approach uses fracture mechanics and regular inspections to maintain safety.",
            tags=["damage_tolerant_design", "fracture_mechanics_paris_law"],
            weight=1.0
        ),
        SearchDocument(
            id="damage_tolerant_02",
            title="Damage Tolerance and Certification",
            content="Certification standards such as AC 25.571 require damage tolerant design for primary aircraft structures. This involves analysis of crack growth rates and inspection intervals to prevent catastrophic failure.",
            tags=["damage_tolerant_design", "certification_AC25571_damage_tolerance"],
            weight=1.0
        ),
        SearchDocument(
            id="stress_analysis_01",
            title="Stress Analysis Methods in Aircraft Structures",
            content="Stress analysis methods include analytical calculations, finite element modeling, and experimental testing. Accurate stress analysis is essential for safe life, fail safe, and damage tolerant design philosophies.",
            tags=["stress_analysis_methods", "safe_life_design_philosophy"],
            weight=1.0
        ),
        SearchDocument(
            id="stress_analysis_02",
            title="Finite Element Analysis for Structural Design",
            content="Finite element analysis (FEA) enables detailed modeling of complex aircraft structures, predicting stress distributions and identifying critical locations for fatigue and fracture.",
            tags=["stress_analysis_methods", "fatigue_life_prediction_SN_curves"],
            weight=1.0
        ),
        SearchDocument(
            id="fatigue_01",
            title="Fatigue Life Prediction Using S-N Curves",
            content="S-N curves relate cyclic stress amplitude to the number of cycles to failure. Fatigue life prediction is crucial for safe life and damage tolerant design, especially in aluminum alloys and composite materials.",
            tags=["fatigue_life_prediction_SN_curves", "aluminum_alloys_2024_7075"],
            weight=1.0
        ),
        SearchDocument(
            id="fatigue_02",
            title="Factors Affecting Fatigue Life in Aircraft",
            content="Fatigue life is influenced by material properties, stress concentrations, surface finish, and environmental conditions such as corrosion. Regular inspections and maintenance extend fatigue life.",
            tags=["fatigue_life_prediction_SN_curves", "corrosion_types_galvanic_pitting"],
            weight=1.0
        ),
        SearchDocument(
            id="fracture_01",
            title="Fracture Mechanics and Paris Law",
            content="Paris Law describes crack growth rate as a function of stress intensity factor range. Fracture mechanics is used to predict crack propagation and set inspection intervals for damage tolerant structures.",
            tags=["fracture_mechanics_paris_law", "damage_tolerant_design"],
            weight=1.0
        ),
        SearchDocument(
            id="fracture_02",
            title="Application of Fracture Mechanics in Aircraft",
            content="Fracture mechanics analysis helps determine critical crack sizes, residual strength, and safe inspection intervals. It is essential for certification and structural repair procedures.",
            tags=["fracture_mechanics_paris_law", "structural_repair_manual_procedures"],
            weight=1.0
        ),
        SearchDocument(
            id="composite_01",
            title="Composite Materials: Carbon Fiber in Aircraft",
            content="Carbon fiber composites offer high strength-to-weight ratios and corrosion resistance. They are used in wing skins, fuselage sections, and control surfaces. Design requires understanding of ply orientation and failure criteria.",
            tags=["composite_materials_carbon_fiber", "wing_structural_design_spar_rib_skin"],
            weight=1.0
        ),
        SearchDocument(
            id="composite_02",
            title="Composite Failure Criteria: Tsai-Wu Theory",
            content="Tsai-Wu failure criterion is used to predict failure in composite laminates under multiaxial loading. It considers interaction between different stress components and material anisotropy.",
            tags=["composite_failure_criteria_tsai_wu", "composite_materials_carbon_fiber"],
            weight=1.0
        ),
        SearchDocument(
            id="aluminum_01",
            title="Aluminum Alloys 2024 and 7075 in Aircraft",
            content="Aluminum alloys 2024 and 7075 are widely used in aircraft structures due to their high strength and fatigue resistance. 2024 is preferred for fuselage skins, while 7075 is used for wing spars and landing gear.",
            tags=["aluminum_alloys_2024_7075", "wing_structural_design_spar_rib_skin"],
            weight=1.0
        ),
        SearchDocument(
            id="aluminum_02",
            title="Corrosion in Aluminum Alloys",
            content="Aluminum alloys are susceptible to galvanic and pitting corrosion, especially when in contact with dissimilar metals. Protective coatings and regular inspections mitigate corrosion risks.",
            tags=["aluminum_alloys_2024_7075", "corrosion_types_galvanic_pitting"],
            weight=1.0
        ),
        SearchDocument(
            id="corrosion_01",
            title="Types of Corrosion in Aircraft Structures",
            content="Common corrosion types include galvanic, pitting, intergranular, and exfoliation. Galvanic corrosion occurs when dissimilar metals are in contact in the presence of an electrolyte.",
            tags=["corrosion_types_galvanic_pitting", "aluminum_alloys_2024_7075"],
            weight=1.0
        ),
        SearchDocument(
            id="corrosion_02",
            title="Corrosion Prevention and Inspection",
            content="Corrosion prevention involves material selection, protective coatings, and regular NDT inspections. Ultrasonic and eddy current methods are effective for detecting hidden corrosion.",
            tags=["corrosion_types_galvanic_pitting", "ndt_methods_ultrasonic_eddy_current"],
            weight=1.0
        ),
        SearchDocument(
            id="ndt_01",
            title="NDT Methods: Ultrasonic Testing",
            content="Ultrasonic testing uses high-frequency sound waves to detect internal flaws and cracks in aircraft structures. It is widely used for inspecting composite materials and aluminum alloys.",
            tags=["ndt_methods_ultrasonic_eddy_current", "composite_materials_carbon_fiber"],
            weight=1.0
        ),
        SearchDocument(
            id="ndt_02",
            title="NDT Methods: Eddy Current Testing",
            content="Eddy current testing detects surface and subsurface defects in conductive materials. It is effective for finding cracks and corrosion in aluminum aircraft structures.",
            tags=["ndt_methods_ultrasonic_eddy_current", "aluminum_alloys_2024_7075"],
            weight=1.0
        ),
        SearchDocument(
            id="repair_01",
            title="Structural Repair Manual Procedures",
            content="Structural repair manuals (SRM) provide guidelines for repairing damaged aircraft structures. Procedures include material selection, fastener installation, and inspection requirements.",
            tags=["structural_repair_manual_procedures", "fastener_selection_rivets_hilok"],
            weight=1.0
        ),
        SearchDocument(
            id="repair_02",
            title="Repair of Composite Structures",
            content="Composite repairs require careful preparation, ply layup, and curing. NDT methods are used to verify repair quality and detect hidden damage.",
            tags=["structural_repair_manual_procedures", "composite_materials_carbon_fiber"],
            weight=1.0
        ),
        SearchDocument(
            id="fuselage_01",
            title="Pressurized Fuselage: Hoop Stress Analysis",
            content="Hoop stress in pressurized fuselage sections is calculated using thin-walled cylinder theory. Accurate stress analysis is essential for safe life and damage tolerant design.",
            tags=["pressurized_fuselage_hoop_stress", "stress_analysis_methods"],
            weight=1.0
        ),
        SearchDocument(
            id="fuselage_02",
            title="Fuselage Structural Design Considerations",
            content="Fuselage design must account for pressurization cycles, fatigue, and corrosion. Materials such as 2024 aluminum and carbon fiber composites are commonly used.",
            tags=["pressurized_fuselage_hoop_stress", "aluminum_alloys_2024_7075"],
            weight=1.0
        ),
        SearchDocument(
            id="wing_01",
            title="Wing Structural Design: Spar, Rib, and Skin",
            content="Wing structures consist of spars, ribs, and skins. Spars carry bending loads, ribs maintain airfoil shape, and skins transfer aerodynamic forces. Material selection and fastener choice are critical.",
            tags=["wing_structural_design_spar_rib_skin", "fastener_selection_rivets_hilok"],
            weight=1.0
        ),
        SearchDocument(
            id="wing_02",
            title="Composite Wing Design and Failure Modes",
            content="Composite wings offer weight savings but require careful analysis of ply orientation and failure criteria such as Tsai-Wu. Inspection and repair procedures differ from metallic wings.",
            tags=["wing_structural_design_spar_rib_skin", "composite_failure_criteria_tsai_wu"],
            weight=1.0
        ),
        SearchDocument(
            id="certification_01",
            title="Certification: AC 25.571 Damage Tolerance",
            content="AC 25.571 outlines requirements for damage tolerance in transport aircraft structures. It mandates fracture mechanics analysis, crack growth prediction, and inspection intervals.",
            tags=["certification_AC25571_damage_tolerance", "fracture_mechanics_paris_law"],
            weight=1.0
        ),
        SearchDocument(
            id="fastener_01",
            title="Fastener Selection: Rivets and Hi-Lok",
            content="Rivets and Hi-Lok fasteners are used in aircraft structures for joining skins, spars, and ribs. Selection depends on load requirements, material compatibility, and inspection accessibility.",
            tags=["fastener_selection_rivets_hilok", "wing_structural_design_spar_rib_skin"],
            weight=1.0
        ),
        SearchDocument(
            id="fastener_02",
            title="Installation and Inspection of Fasteners",
            content="Proper installation of fasteners is essential for structural integrity. Inspection methods include visual checks and NDT techniques such as ultrasonic and eddy current testing.",
            tags=["fastener_selection_rivets_hilok", "ndt_methods_ultrasonic_eddy_current"],
            weight=1.0
        ),
        SearchDocument(
            id="overview_01",
            title="Aircraft Structures: Design Philosophy Overview",
            content="Aircraft structural design incorporates safe life, fail safe, and damage tolerant philosophies. Material selection, stress analysis, fatigue prediction, and fracture mechanics are integral to ensuring safety and certification.",
            tags=["safe_life_design_philosophy", "fail_safe_design_philosophy", "damage_tolerant_design", "stress_analysis_methods", "fatigue_life_prediction_SN_curves", "fracture_mechanics_paris_law", "certification_AC25571_damage_tolerance"],
            weight=1.2
        ),
        SearchDocument(
            id="overview_02",
            title="Composite and Metallic Structure Comparison",
            content="Composite materials such as carbon fiber offer advantages in weight and corrosion resistance compared to aluminum alloys. However, failure criteria and repair procedures differ significantly.",
            tags=["composite_materials_carbon_fiber", "aluminum_alloys_2024_7075", "composite_failure_criteria_tsai_wu", "structural_repair_manual_procedures"],
            weight=1.0
        ),
        SearchDocument(
            id="inspection_01",
            title="Inspection Techniques for Aircraft Structures",
            content="Inspection techniques include visual, ultrasonic, and eddy current methods. Regular inspections are required for damage tolerant and fail safe structures to detect cracks, corrosion, and fastener issues.",
            tags=["ndt_methods_ultrasonic_eddy_current", "damage_tolerant_design", "fail_safe_design_philosophy"],
            weight=1.0
        ),
        SearchDocument(
            id="maintenance_01",
            title="Maintenance and Repair of Aircraft Structures",
            content="Maintenance procedures include corrosion prevention, fatigue crack detection, and structural repairs using SRM guidelines. Fastener replacement and NDT inspections are routine tasks.",
            tags=["structural_repair_manual_procedures", "corrosion_types_galvanic_pitting", "fastener_selection_rivets_hilok"],
            weight=1.0
        ),
        SearchDocument(
            id="certification_02",
            title="Regulatory Requirements for Structural Design",
            content="Regulatory requirements mandate safe life, fail safe, and damage tolerant design philosophies. Certification involves stress analysis, fatigue life prediction, fracture mechanics, and inspection intervals.",
            tags=["certification_AC25571_damage_tolerance", "safe_life_design_philosophy", "fail_safe_design_philosophy", "damage_tolerant_design"],
            weight=1.1
        ),
        SearchDocument(
            id="fatigue_03",
            title="Fatigue Crack Growth and Inspection Intervals",
            content="Fatigue crack growth is predicted using S-N curves and Paris Law. Inspection intervals are set to ensure cracks are detected before reaching critical size, maintaining structural safety.",
            tags=["fatigue_life_prediction_SN_curves", "fracture_mechanics_paris_law", "damage_tolerant_design"],
            weight=1.0
        ),
        SearchDocument(
            id="composite_03",
            title="Composite Material Inspection and Failure",
            content="Composite materials require specialized NDT methods for inspection. Failure modes include delamination, fiber breakage, and matrix cracking. Tsai-Wu criterion is used for failure prediction.",
            tags=["composite_materials_carbon_fiber", "composite_failure_criteria_tsai_wu", "ndt_methods_ultrasonic_eddy_current"],
            weight=1.0
        ),
        SearchDocument(
            id="corrosion_03",
            title="Galvanic Corrosion Prevention in Aircraft",
            content="Galvanic corrosion is prevented by isolating dissimilar metals, applying protective coatings, and using compatible fasteners such as Hi-Lok. Regular inspection is critical.",
            tags=["corrosion_types_galvanic_pitting", "fastener_selection_rivets_hilok"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)