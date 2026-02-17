import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Any, Optional

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
        self.term_doc_freqs: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.doc_tags: Dict[int, List[str]] = {}
        self.doc_weights: Dict[int, float] = {}
        self.lock = threading.Lock()
        self.avg_doc_length: float = 0.0
        self.total_docs: int = 0
        self.idf_cache: Dict[str, float] = {}
        self._update_stats_needed = True

    def add_document(self, doc: SearchDocument):
        with self.lock:
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            for term, freq in tf.items():
                self.term_doc_freqs[term][doc.id] = freq
            self.doc_tags[doc.id] = doc.tags
            self.doc_weights[doc.id] = doc.weight
            self._update_stats_needed = True

    def _update_stats(self):
        if not self._update_stats_needed:
            return
        self.total_docs = len(self.documents)
        if self.total_docs == 0:
            self.avg_doc_length = 0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs
        self.idf_cache.clear()
        self._update_stats_needed = False

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        tokens = text.split()
        return tokens

    def _compute_idf(self, term: str) -> float:
        self._update_stats()
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = len(self.term_doc_freqs.get(term, {}))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        self._update_stats()
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        weight = self.doc_weights.get(doc_id, 1.0)
        tf = self.term_freqs.get(doc_id, Counter())
        for term in query_terms:
            idf = self._compute_idf(term)
            freq = tf.get(term, 0)
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (1 - self.b + self.b * doc_length / (self.avg_doc_length if self.avg_doc_length > 0 else 1))
            if denominator == 0:
                continue
            score += idf * numerator / denominator
        return score * weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        self._update_stats()
        tf = self.term_freqs.get(doc_id, Counter())
        doc_length = self.doc_lengths.get(doc_id, 1)
        weight = self.doc_weights.get(doc_id, 1.0)
        score = 0.0
        for term in query_terms:
            term_freq = tf.get(term, 0) / doc_length
            idf = self._compute_idf(term)
            score += term_freq * idf
        return score * weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        self._update_stats()
        query_terms = self._tokenize(query)
        doc_scores = {}
        for doc_id in self.documents:
            if use_tfidf:
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

    def _make_snippet(self, content: str, query_terms: List[str], max_length: int = 160) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = ' '.join(tokens[:max_length])
        else:
            start = max(positions[0] - 10, 0)
            end = min(start + max_length, len(tokens))
            snippet = ' '.join(tokens[start:end])
        return snippet[:max_length] + ('...' if len(snippet) > max_length else '')

    def get_stats(self) -> Dict[str, Any]:
        self._update_stats()
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freqs),
        }

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    if _search_index_instance is None:
        with _search_index_lock:
            if _search_index_instance is None:
                _search_index_instance = SearchIndex()
                _seed_documents(_search_index_instance)
    return _search_index_instance

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Conductor Casing Design Principles",
            "Conductor casing is the first casing string set in a well. It provides structural support for subsequent drilling operations and prevents shallow formation caving. Key design factors include diameter selection, setting depth, and load analysis.",
            ["conductor_casing_design", "structural_support", "load_analysis"],
            1.0
        ),
        SearchDocument(
            2,
            "Surface Casing Seat Selection Criteria",
            "Surface casing seat selection is critical for isolating freshwater zones and providing blowout protection. Factors influencing seat selection include formation integrity, pore pressure, and fracture gradient.",
            ["surface_casing_seat_selection", "pore_pressure", "fracture_gradient"],
            1.0
        ),
        SearchDocument(
            3,
            "Casing Grade Selection for Burst Loads",
            "Burst load analysis involves evaluating internal pressure scenarios such as gas kicks and cement displacement. Casing grade selection must ensure sufficient burst resistance, considering API and premium grades.",
            ["casing_grade_selection_burst", "burst_resistance", "api_grades"],
            1.0
        ),
        SearchDocument(
            4,
            "Casing Grade Selection for Collapse Loads",
            "Collapse load analysis addresses external pressures from formation fluids and overburden. Casing grade selection for collapse must account for minimum collapse rating and triaxial stress effects.",
            ["casing_grade_selection_collapse", "collapse_rating", "triaxial_stress"],
            1.0
        ),
        SearchDocument(
            5,
            "Casing Tensile Design Fundamentals",
            "Tensile design ensures the casing string can withstand axial loads during running and cementing. Key considerations include tensile strength, connection efficiency, and safety factors.",
            ["casing_tensile_design", "tensile_strength", "connection_efficiency"],
            1.0
        ),
        SearchDocument(
            6,
            "Biaxial and Triaxial Stress Analysis in Casing Design",
            "Biaxial and triaxial stress analysis evaluates combined loading scenarios including internal pressure, external pressure, and axial tension. Advanced models improve casing reliability under complex well conditions.",
            ["biaxial_triaxial_stress_analysis", "combined_loading", "advanced_models"],
            1.0
        ),
        SearchDocument(
            7,
            "Casing Wear Analysis and Mitigation",
            "Casing wear results from drill string contact and abrasive fluids. Wear analysis models predict casing life, and mitigation strategies include hardbanding and centralizer placement.",
            ["casing_wear_analysis", "wear_models", "mitigation"],
            1.0
        ),
        SearchDocument(
            8,
            "Pore Pressure and Fracture Gradient Estimation",
            "Accurate estimation of pore pressure and fracture gradient is essential for safe casing design. Methods include log analysis, seismic data, and formation tests.",
            ["pore_pressure_fracture_gradient", "log_analysis", "formation_tests"],
            1.0
        ),
        SearchDocument(
            9,
            "Premium Connections for Casing Strings",
            "Premium connections offer enhanced sealing and mechanical performance compared to API connections. Selection criteria include torque capacity, gas-tightness, and fatigue resistance.",
            ["premium_connections", "sealing_performance", "fatigue_resistance"],
            1.0
        ),
        SearchDocument(
            10,
            "Liner Design and Tieback Considerations",
            "Liner design involves selecting liner length, diameter, and overlap with previous casing. Tieback procedures restore full well integrity and are used in deep or HPHT wells.",
            ["liner_design_tieback", "liner_length", "well_integrity"],
            1.0
        ),
        SearchDocument(
            11,
            "Casing Centralizer Placement Optimization",
            "Centralizer placement ensures casing standoff and improves cementing quality. Optimization methods include spacing calculations and simulation of casing deformation.",
            ["casing_centralizer_placement", "cementing_quality", "optimization"],
            1.0
        ),
        SearchDocument(
            12,
            "HPHT Casing Design Challenges",
            "High Pressure High Temperature (HPHT) wells require casing with enhanced mechanical properties and corrosion resistance. Design challenges include material selection, thermal expansion, and stress analysis.",
            ["hpht_casing_design", "material_selection", "thermal_expansion"],
            1.0
        ),
        SearchDocument(
            13,
            "Casing Running and Landing Procedures",
            "Proper casing running and landing procedures minimize risk of stuck pipe and ensure correct placement. Procedures include running speed control, centralizer installation, and monitoring of well parameters.",
            ["casing_running_landing_procedures", "stuck_pipe", "running_speed"],
            1.0
        ),
        SearchDocument(
            14,
            "Corrosion Design for H2S and CO2 Environments",
            "Corrosive environments with H2S and CO2 require specialized casing materials and coatings. Design considerations include material compatibility, corrosion allowance, and monitoring strategies.",
            ["corrosion_design_h2s_co2", "material_compatibility", "corrosion_allowance"],
            1.0
        ),
        SearchDocument(
            15,
            "Expandable Casing Technology Overview",
            "Expandable casing technology enables diameter expansion downhole, improving wellbore integrity and reducing drilling costs. Applications include remedial operations and zonal isolation.",
            ["expandable_casing_technology", "wellbore_integrity", "zonal_isolation"],
            1.0
        ),
        SearchDocument(
            16,
            "Casing Design Software Validation",
            "Software validation ensures casing design tools produce accurate and reliable results. Validation methods include benchmark comparisons, laboratory testing, and field trials.",
            ["casing_design_software_validation", "software_validation", "benchmark"],
            1.0
        ),
        SearchDocument(
            17,
            "API Casing Grades and Specifications",
            "API casing grades define mechanical properties and chemical composition for standard casing strings. Specifications cover yield strength, collapse and burst ratings, and manufacturing tolerances.",
            ["api_grades", "yield_strength", "manufacturing_tolerances"],
            1.0
        ),
        SearchDocument(
            18,
            "Cementing Practices for Casing Strings",
            "Effective cementing practices ensure zonal isolation and casing protection. Techniques include pre-flush, spacer design, and cement slurry optimization.",
            ["cementing_practices", "zonal_isolation", "slurry_optimization"],
            1.0
        ),
        SearchDocument(
            19,
            "Casing String Design Workflow",
            "A systematic workflow for casing string design includes load analysis, grade selection, connection evaluation, and centralizer placement. Documentation and review are essential for quality assurance.",
            ["casing_string_design", "workflow", "quality_assurance"],
            1.0
        ),
        SearchDocument(
            20,
            "Formation Integrity Test (FIT) Procedures",
            "FIT procedures assess formation strength at casing shoe depth. Results inform casing seat selection and mud weight design.",
            ["fit_procedures", "formation_strength", "mud_weight"],
            1.0
        ),
        SearchDocument(
            21,
            "Wellbore Stability and Casing Design",
            "Wellbore stability analysis guides casing diameter and grade selection. Factors include rock mechanics, pore pressure, and drilling fluid properties.",
            ["wellbore_stability", "rock_mechanics", "drilling_fluid"],
            1.0
        ),
        SearchDocument(
            22,
            "Casing Leak Detection and Remediation",
            "Leak detection methods include pressure testing, acoustic monitoring, and tracer injection. Remediation techniques involve patching, cement squeeze, and expandable casing.",
            ["casing_leak_detection", "remediation", "patching"],
            1.0
        ),
        SearchDocument(
            23,
            "Casing Design for Deepwater Wells",
            "Deepwater casing design addresses high external pressure, temperature gradients, and complex well architecture. Material selection and connection integrity are critical.",
            ["deepwater_casing_design", "external_pressure", "connection_integrity"],
            1.0
        ),
        SearchDocument(
            24,
            "Casing Fatigue Analysis",
            "Fatigue analysis predicts casing life under cyclic loading from drilling and production operations. Models include S-N curves and finite element analysis.",
            ["casing_fatigue_analysis", "cyclic_loading", "finite_element"],
            1.0
        ),
        SearchDocument(
            25,
            "Casing String Failure Modes",
            "Common casing failure modes include burst, collapse, tensile failure, and corrosion. Prevention strategies involve proper design, material selection, and monitoring.",
            ["casing_failure_modes", "burst", "collapse", "corrosion"],
            1.0
        ),
        SearchDocument(
            26,
            "Advanced Casing Centralizer Technologies",
            "Advanced centralizer technologies improve casing standoff and reduce wear. Innovations include composite materials and adjustable designs.",
            ["centralizer_technologies", "composite_materials", "adjustable_designs"],
            1.0
        ),
        SearchDocument(
            27,
            "Casing Pressure Testing Protocols",
            "Pressure testing protocols verify casing integrity after installation. Tests include leak-off, pressure hold, and monitoring for pressure drops.",
            ["pressure_testing", "casing_integrity", "leak_off"],
            1.0
        ),
        SearchDocument(
            28,
            "Casing Design for Unconventional Wells",
            "Unconventional wells require casing designs that accommodate high deviation, hydraulic fracturing, and multi-stage completions.",
            ["unconventional_casing_design", "hydraulic_fracturing", "multi_stage"],
            1.0
        ),
        SearchDocument(
            29,
            "Casing String Logistics and Supply Chain",
            "Logistics and supply chain management ensure timely delivery and quality of casing strings. Key aspects include inventory tracking, transport, and inspection.",
            ["casing_logistics", "supply_chain", "inventory_tracking"],
            1.0
        ),
        SearchDocument(
            30,
            "Casing Design for Enhanced Oil Recovery (EOR)",
            "EOR operations require casing designs that withstand chemical injection, thermal cycles, and increased production rates.",
            ["eor_casing_design", "chemical_injection", "thermal_cycles"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)