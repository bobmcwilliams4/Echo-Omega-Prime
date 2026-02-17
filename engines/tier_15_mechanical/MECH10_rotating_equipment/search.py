import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

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
    def __init__(self, bm25_k1: float = 1.5, bm25_b: float = 0.75):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.total_docs: int = 0
        self.avg_doc_length: float = 0.0
        self.bm25_k1 = bm25_k1
        self.bm25_b = bm25_b
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + ' ' + doc.content + ' ' + ' '.join(doc.tags))
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.doc_freqs[term] += 1
            self.documents[doc.id] = doc
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs else 0.0
            self.idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            freq = tf.get(term, 0)
            if freq == 0:
                continue
            idf = self._compute_idf(term)
            denom = freq + self.bm25_k1 * (1 - self.bm25_b + self.bm25_b * doc_len / (self.avg_doc_length or 1))
            numer = freq * (self.bm25_k1 + 1)
            score += idf * numer / denom
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        doc = self.documents[doc_id]
        for term in query_terms:
            tf_raw = tf.get(term, 0)
            if tf_raw == 0:
                continue
            tf_norm = tf_raw / doc_len if doc_len > 0 else 0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, use_bm25: bool = True) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidate_doc_ids = set()
        for term in query_terms:
            for doc_id in self.term_freqs:
                if term in self.term_freqs[doc_id]:
                    candidate_doc_ids.add(doc_id)
        scored: List[Tuple[int, float]] = []
        for doc_id in candidate_doc_ids:
            if use_bm25:
                score = self._score_bm25(query_terms, doc_id)
            else:
                score = self._score_tfidf(query_terms, doc_id)
            if score > 0:
                scored.append((doc_id, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:200] + ('...' if len(content) > 200 else '')
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in query_terms:
            snippet = re.sub(rf'\b({re.escape(term)})\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.doc_freqs)
        }

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
            1,
            "NEMA Frame Sizing for Electric Motors",
            "Guidelines for selecting NEMA frame sizes based on power, speed, and mounting configuration. Includes standard frame assignments and dimensional charts for industrial electric motors.",
            ["electric_motor_nema_frame_sizing", "nema", "motor_selection"],
            1.0
        ),
        SearchDocument(
            2,
            "Motor Efficiency Classes and IE Standards",
            "Overview of IE1, IE2, IE3, and IE4 motor efficiency classes per IEC 60034-30. Discusses test methods, regulatory requirements, and impact on energy savings.",
            ["motor_efficiency_classes_ie_standards", "iec", "energy_efficiency"],
            1.0
        ),
        SearchDocument(
            3,
            "Motor Service Factor and Thermal Margin",
            "Explains the concept of service factor for electric motors, its influence on allowable overload, and considerations for thermal margin in continuous and intermittent duty.",
            ["motor_service_factor_thermal_margin", "motor_protection", "thermal_analysis"],
            1.0
        ),
        SearchDocument(
            4,
            "VFD Harmonics and Mitigation Techniques",
            "Describes the generation of harmonics by variable frequency drives (VFDs), their effects on power quality, and mitigation strategies such as line reactors, filters, and 12-pulse rectifiers.",
            ["vfd_harmonics_mitigation", "power_quality", "harmonics"],
            1.0
        ),
        SearchDocument(
            5,
            "Gear Drive Types and Selection Criteria",
            "Compares parallel shaft, helical, bevel, and worm gear drives. Outlines selection criteria based on torque, efficiency, noise, and maintenance requirements.",
            ["gear_drive_types_selection", "gearbox", "mechanical_power_transmission"],
            1.0
        ),
        SearchDocument(
            6,
            "Flexible vs Rigid Coupling Selection",
            "Discusses the differences between flexible and rigid couplings, including misalignment accommodation, torsional damping, and typical application scenarios.",
            ["coupling_selection_flexible_vs_rigid", "coupling", "shaft_connection"],
            1.0
        ),
        SearchDocument(
            7,
            "Precision Shaft Alignment Methods",
            "Reviews dial indicator, laser, and reverse indicator methods for achieving precision shaft alignment. Emphasizes the importance of alignment for machinery reliability.",
            ["shaft_alignment_methods_precision", "alignment", "maintenance"],
            1.0
        ),
        SearchDocument(
            8,
            "API 682 Mechanical Seal Piping Plans",
            "Summarizes API 682 piping plans for mechanical seals, including Plan 11, Plan 23, and Plan 53. Covers selection guidelines for process and environmental conditions.",
            ["mechanical_seal_api_682_plans", "api_682", "seal_systems"],
            1.0
        ),
        SearchDocument(
            9,
            "Packing vs Mechanical Seal Selection",
            "Compares gland packing and mechanical seals for rotating equipment. Discusses leakage, maintenance, cost, and suitability for various services.",
            ["packing_vs_mechanical_seal_selection", "seal_selection", "maintenance"],
            1.0
        ),
        SearchDocument(
            10,
            "Shaft Design and Keyway Stress Analysis",
            "Covers shaft design fundamentals, keyway stress concentration factors, and calculation methods for safe torque transmission.",
            ["shaft_design_keyway_stress_analysis", "shaft_design", "stress_analysis"],
            1.0
        ),
        SearchDocument(
            11,
            "Torsional Critical Speed Analysis",
            "Explains how to perform torsional critical speed analysis for rotating shafts, including system modeling, resonance prediction, and mitigation strategies.",
            ["torsional_critical_speed_analysis", "critical_speed", "vibration"],
            1.0
        ),
        SearchDocument(
            12,
            "Lateral Critical Speed and Bearing Stiffness",
            "Describes lateral critical speed analysis, the role of bearing stiffness, and methods to avoid resonance in high-speed machinery.",
            ["lateral_critical_speed_bearing_stiffness", "bearing", "critical_speed"],
            1.0
        ),
        SearchDocument(
            13,
            "API 610 Centrifugal Pump Standard",
            "Provides an overview of API 610 requirements for centrifugal pumps, including design, testing, and documentation for petrochemical applications.",
            ["api_610_centrifugal_pump_standard", "api_610", "pump"],
            1.0
        ),
        SearchDocument(
            14,
            "API 617 Centrifugal Compressor Standard",
            "Summarizes API 617 specifications for centrifugal compressors, covering rotor dynamics, materials, and acceptance testing.",
            ["api_617_centrifugal_compressor_standard", "api_617", "compressor"],
            1.0
        ),
        SearchDocument(
            15,
            "API 670 Machinery Protection Systems",
            "Details API 670 requirements for vibration, temperature, and overspeed protection systems in critical rotating equipment.",
            ["api_670_machinery_protection_systems", "api_670", "protection"],
            1.0
        ),
        SearchDocument(
            16,
            "Vibration Analysis and Fault Diagnosis",
            "Introduces vibration analysis techniques for machinery fault diagnosis, including FFT, time waveform, and orbit analysis.",
            ["vibration_analysis_fault_diagnosis", "vibration", "fault_diagnosis"],
            1.0
        ),
        SearchDocument(
            17,
            "Developing a Condition Monitoring Program",
            "Guidelines for establishing a condition monitoring program, including data collection, trending, and predictive maintenance strategies.",
            ["condition_monitoring_program_development", "condition_monitoring", "maintenance"],
            1.0
        ),
        SearchDocument(
            18,
            "Root Cause Analysis of Machinery Failures",
            "Outlines systematic approaches for root cause analysis (RCA) of machinery failures, including FMEA and fault tree analysis.",
            ["root_cause_analysis_machinery_failures", "rca", "failure_analysis"],
            1.0
        ),
        SearchDocument(
            19,
            "Spare Parts Strategy: Insurance vs Consumable",
            "Discusses strategies for spare parts management, differentiating between insurance and consumable spares, and optimizing inventory.",
            ["spare_parts_strategy_insurance_vs_consumable", "spares_management", "inventory"],
            1.0
        ),
        SearchDocument(
            20,
            "Motor Enclosure Types and NEMA Ratings",
            "Explains open, drip-proof, TEFC, and explosion-proof motor enclosures and their NEMA environmental protection ratings.",
            ["motor_enclosure_types_nema_ratings", "nema", "motor_enclosure"],
            1.0
        ),
        SearchDocument(
            21,
            "Gearbox Lubrication: Oil vs Grease",
            "Compares oil and grease lubrication for gearboxes, including selection criteria, maintenance, and monitoring best practices.",
            ["gearbox_lubrication_oil_vs_grease", "lubrication", "gearbox"],
            1.0
        ),
        SearchDocument(
            22,
            "API 611 Steam Turbine Applications",
            "Reviews API 611 standard for general-purpose steam turbines, including design, operation, and maintenance considerations.",
            ["api_611_steam_turbine_applications", "api_611", "steam_turbine"],
            1.0
        ),
        SearchDocument(
            23,
            "Coupling Balance and Alignment Runout",
            "Explains the importance of coupling balance and alignment runout, measurement techniques, and corrective actions.",
            ["coupling_balance_and_alignment_runout", "coupling", "alignment"],
            1.0
        ),
        SearchDocument(
            24,
            "Selecting Mechanical Seals for Aggressive Services",
            "Factors to consider when selecting mechanical seals for aggressive chemical or high-temperature services, including material compatibility and seal arrangement.",
            ["mechanical_seal_selection", "seal_materials", "aggressive_service"],
            1.0
        ),
        SearchDocument(
            25,
            "Reverse Engineering of Rotating Equipment Components",
            "Describes reverse engineering practices for shafts, impellers, and bearings, including 3D scanning and material analysis.",
            ["reverse_engineering", "rotating_equipment", "component_analysis"],
            1.0
        ),
        SearchDocument(
            26,
            "Predictive Maintenance with IIoT Sensors",
            "Application of IIoT sensors for real-time monitoring of vibration, temperature, and lubrication in rotating equipment.",
            ["predictive_maintenance", "iiot", "condition_monitoring"],
            1.0
        ),
        SearchDocument(
            27,
            "Laser Alignment vs Dial Indicator Methods",
            "Comparison of laser alignment and dial indicator methods for shaft alignment, including accuracy, speed, and ease of use.",
            ["shaft_alignment_methods_precision", "laser_alignment", "dial_indicator"],
            1.0
        ),
        SearchDocument(
            28,
            "API 610 Pump Testing and Acceptance",
            "Details API 610 pump testing procedures, including performance, hydrostatic, and NPSH tests for compliance verification.",
            ["api_610_centrifugal_pump_standard", "pump_testing", "api_610"],
            1.0
        ),
        SearchDocument(
            29,
            "Common Causes of Gearbox Failure",
            "Lists typical causes of gearbox failure such as misalignment, lubrication issues, and overload, with troubleshooting guidance.",
            ["gearbox_failure", "maintenance", "gear_drive_types_selection"],
            1.0
        ),
        SearchDocument(
            30,
            "VFD Selection for Pump Applications",
            "Key considerations for selecting VFDs for centrifugal pump applications, including sizing, harmonics, and protection features.",
            ["vfd_selection", "vfd_harmonics_mitigation", "pump"],
            1.0
        ),
        SearchDocument(
            31,
            "API 682 Seal Failure Modes",
            "Describes common failure modes for API 682 mechanical seals, including thermal degradation, dry running, and improper piping plans.",
            ["mechanical_seal_api_682_plans", "seal_failure", "api_682"],
            1.0
        ),
        SearchDocument(
            32,
            "Bearing Types and Lubrication Methods",
            "Overview of rolling element and sleeve bearings, lubrication methods, and best practices for reliability.",
            ["bearing", "lubrication", "maintenance"],
            1.0
        ),
        SearchDocument(
            33,
            "API 617 Compressor Rotor Dynamics",
            "Discusses rotor dynamic analysis requirements for API 617 compressors, including critical speed mapping and stability.",
            ["api_617_centrifugal_compressor_standard", "rotor_dynamics", "api_617"],
            1.0
        ),
        SearchDocument(
            34,
            "Root Cause Analysis: Case Studies",
            "Presents case studies of machinery failures and the application of root cause analysis tools to resolve them.",
            ["root_cause_analysis_machinery_failures", "case_study", "failure_analysis"],
            1.0
        ),
        SearchDocument(
            35,
            "Shaft Key Design and Failure Prevention",
            "Design principles for shaft keys, keyways, and methods to prevent fatigue and fretting failures.",
            ["shaft_design_keyway_stress_analysis", "key_design", "failure_prevention"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)