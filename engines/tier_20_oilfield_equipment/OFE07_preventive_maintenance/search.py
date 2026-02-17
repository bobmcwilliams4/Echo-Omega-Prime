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
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9_]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.term_freqs[doc.id] = Counter(tokens)
            for token in set(tokens):
                self.term_doc_freq[token] += 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            self._idf_cache.clear()

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

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        freq = self.term_freqs.get(doc_id, Counter())
        doc = self.documents[doc_id]
        for term in query_terms:
            idf = self._compute_idf(term)
            tf = freq[term]
            numerator = tf * (self._bm25_k1 + 1)
            denominator = tf + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / (self.avg_doc_length or 1))
            score += idf * (numerator / (denominator or 1))
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        freq = self.term_freqs.get(doc_id, Counter())
        doc_len = self.doc_lengths.get(doc_id, 1)
        for term in query_terms:
            tf = freq[term] / doc_len
            idf = self._compute_idf(term)
            score += tf * idf
        return score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: List[Tuple[int, float]] = []
        for doc_id in self.documents:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                doc_scores.append((doc_id, score))
        doc_scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in doc_scores[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str], length: int = 160) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = ' '.join(tokens[:length])
        else:
            start = max(positions[0] - 10, 0)
            end = min(start + length, len(tokens))
            snippet = ' '.join(tokens[start:end])
        return snippet + ('...' if len(tokens) > length else '')

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
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
            1,
            "API RP 53 BOP Maintenance Overview",
            "API RP 53 provides guidelines for Blowout Preventer (BOP) equipment maintenance, including inspection intervals, lubrication, and functional testing. Preventive maintenance ensures operational reliability and compliance with regulatory standards.",
            ["API_RP_53_BOP_MAINTENANCE", "BOP", "Preventive"],
            1.0
        ),
        SearchDocument(
            2,
            "Mud Pump Fluid End Maintenance Procedures",
            "Routine fluid end maintenance for mud pumps includes checking valves, seals, and liners for wear. Proper lubrication and timely replacement of parts reduce downtime and extend equipment life.",
            ["MUD_PUMP_FLUID_END_MAINTENANCE", "Mud Pump", "Fluid End"],
            1.0
        ),
        SearchDocument(
            3,
            "Drawworks Brake Inspection Checklist",
            "Drawworks brake systems require regular inspection for lining wear, hydraulic leaks, and operational integrity. API RP 53 recommends monthly checks and annual overhauls for safety.",
            ["DRAWWORKS_BRAKE_INSPECTION", "Drawworks", "Brake"],
            1.0
        ),
        SearchDocument(
            4,
            "Caterpillar 3512/3516 Engine Maintenance Best Practices",
            "Caterpillar 3512 and 3516 engines require scheduled oil changes, filter replacements, and coolant checks. Monitoring vibration and exhaust emissions helps detect early signs of failure.",
            ["CATERPILLAR_3512_3516_ENGINE_MAINTENANCE", "Engine", "Caterpillar"],
            1.0
        ),
        SearchDocument(
            5,
            "API 2C Crane Inspection Guidelines",
            "API 2C outlines crane inspection criteria including wire rope condition, load testing, and structural integrity. Preventive maintenance reduces risk of mechanical failure during lifting operations.",
            ["API_2C_CRANE_INSPECTION", "Crane", "Inspection"],
            1.0
        ),
        SearchDocument(
            6,
            "Pressure Vessel Inspection: NB-23 & API 510",
            "Pressure vessels must be inspected per NB-23 and API 510 standards. Key steps include visual examination, ultrasonic thickness testing, and review of safety relief devices.",
            ["PRESSURE_VESSEL_INSPECTION_NB23_API510", "Pressure Vessel", "Inspection"],
            1.0
        ),
        SearchDocument(
            7,
            "Piping Inspection per API 570",
            "API 570 specifies piping inspection intervals, corrosion monitoring, and defect assessment. Proper documentation and risk-based inspection strategies are essential for compliance.",
            ["PIPING_INSPECTION_API570", "Piping", "Inspection"],
            1.0
        ),
        SearchDocument(
            8,
            "Storage Tank Inspection: API 653",
            "API 653 governs storage tank inspection, including shell, roof, and foundation checks. Non-destructive testing and corrosion evaluation are critical for preventive maintenance.",
            ["STORAGE_TANK_INSPECTION_API653", "Storage Tank", "Inspection"],
            1.0
        ),
        SearchDocument(
            9,
            "Wire Rope Replacement Criteria",
            "Wire ropes must be replaced when broken wires, corrosion, or diameter reduction exceed API 2C limits. Regular inspection prevents catastrophic failure in lifting equipment.",
            ["WIRE_ROPE_REPLACEMENT_CRITERIA", "Wire Rope", "Replacement"],
            1.0
        ),
        SearchDocument(
            10,
            "Torque Wrench Calibration Procedures",
            "Torque wrenches require periodic calibration to ensure accuracy. Calibration involves applying known loads and adjusting the wrench to meet manufacturer specifications.",
            ["TORQUE_WRENCH_CALIBRATION", "Torque Wrench", "Calibration"],
            1.0
        ),
        SearchDocument(
            11,
            "NDT Methods Selection for Maintenance",
            "Non-destructive testing (NDT) methods such as ultrasonic, magnetic particle, and dye penetrant are selected based on material type and defect location. Proper NDT selection improves reliability.",
            ["NDT_METHODS_SELECTION", "NDT", "Maintenance"],
            1.0
        ),
        SearchDocument(
            12,
            "Vibration Analysis per ISO 10816",
            "ISO 10816 provides vibration analysis criteria for rotating machinery. Monitoring vibration levels enables early detection of imbalance, misalignment, and bearing defects.",
            ["VIBRATION_ANALYSIS_ISO10816", "Vibration", "Analysis"],
            1.0
        ),
        SearchDocument(
            13,
            "Oil Analysis Programs for Engines",
            "Oil analysis detects contaminants, wear metals, and degradation in engine lubricants. Regular sampling and laboratory testing support predictive maintenance strategies.",
            ["OIL_ANALYSIS_PROGRAMS", "Oil Analysis", "Engine"],
            1.0
        ),
        SearchDocument(
            14,
            "RCM: Reliability Centered Maintenance Fundamentals",
            "Reliability Centered Maintenance (RCM) optimizes maintenance schedules based on failure modes and criticality. RCM reduces costs and improves asset reliability.",
            ["RCM_RELIABILITY_CENTERED_MAINTENANCE", "RCM", "Reliability"],
            1.0
        ),
        SearchDocument(
            15,
            "BOP Stack Lubrication and Testing",
            "Lubrication of BOP stack components and functional testing are essential for maintaining blowout preventer reliability. API RP 53 recommends quarterly lubrication and annual testing.",
            ["API_RP_53_BOP_MAINTENANCE", "BOP", "Lubrication"],
            1.0
        ),
        SearchDocument(
            16,
            "Mud Pump Valve Replacement Criteria",
            "Mud pump valves should be replaced when leakage, wear, or seating issues are detected. Preventive maintenance reduces risk of pump failure during drilling operations.",
            ["MUD_PUMP_FLUID_END_MAINTENANCE", "Mud Pump", "Valve"],
            1.0
        ),
        SearchDocument(
            17,
            "Drawworks Brake Fluid Inspection",
            "Brake fluid levels and quality must be checked regularly in drawworks systems. Contaminated or low fluid can lead to brake failure and operational hazards.",
            ["DRAWWORKS_BRAKE_INSPECTION", "Drawworks", "Brake Fluid"],
            1.0
        ),
        SearchDocument(
            18,
            "Caterpillar Engine Coolant System Check",
            "Coolant system inspection for Caterpillar 3512/3516 engines includes checking for leaks, proper coolant concentration, and radiator cleanliness.",
            ["CATERPILLAR_3512_3516_ENGINE_MAINTENANCE", "Engine", "Coolant"],
            1.0
        ),
        SearchDocument(
            19,
            "Crane Wire Rope Lubrication",
            "Lubricating crane wire ropes reduces friction and corrosion, extending service life. API 2C recommends routine lubrication and inspection for safe operation.",
            ["API_2C_CRANE_INSPECTION", "Crane", "Wire Rope"],
            1.0
        ),
        SearchDocument(
            20,
            "Pressure Vessel Ultrasonic Thickness Testing",
            "Ultrasonic thickness testing is used to assess wall loss in pressure vessels. API 510 requires periodic thickness measurements to ensure vessel integrity.",
            ["PRESSURE_VESSEL_INSPECTION_NB23_API510", "Pressure Vessel", "Ultrasonic"],
            1.0
        ),
        SearchDocument(
            21,
            "Piping Corrosion Monitoring Techniques",
            "Corrosion monitoring in piping systems per API 570 includes ultrasonic, radiographic, and visual inspection methods. Early detection prevents leaks and failures.",
            ["PIPING_INSPECTION_API570", "Piping", "Corrosion"],
            1.0
        ),
        SearchDocument(
            22,
            "Storage Tank Roof Inspection",
            "Storage tank roofs are inspected for corrosion, leaks, and structural deformation. API 653 recommends annual roof inspections for preventive maintenance.",
            ["STORAGE_TANK_INSPECTION_API653", "Storage Tank", "Roof"],
            1.0
        ),
        SearchDocument(
            23,
            "Wire Rope Diameter Measurement",
            "Measuring wire rope diameter is critical for determining replacement criteria. API 2C specifies minimum diameter thresholds for safe operation.",
            ["WIRE_ROPE_REPLACEMENT_CRITERIA", "Wire Rope", "Diameter"],
            1.0
        ),
        SearchDocument(
            24,
            "Torque Wrench Accuracy Verification",
            "Accuracy verification of torque wrenches ensures proper bolt tightening. Calibration records must be maintained for traceability and compliance.",
            ["TORQUE_WRENCH_CALIBRATION", "Torque Wrench", "Accuracy"],
            1.0
        ),
        SearchDocument(
            25,
            "NDT for Pressure Vessel Welds",
            "Pressure vessel welds are inspected using NDT methods such as radiography and ultrasonic testing. NB-23 and API 510 require weld quality verification.",
            ["NDT_METHODS_SELECTION", "PRESSURE_VESSEL_INSPECTION_NB23_API510", "Weld"],
            1.0
        ),
        SearchDocument(
            26,
            "Vibration Monitoring for Mud Pumps",
            "Vibration monitoring detects imbalance and mechanical faults in mud pumps. ISO 10816 provides guidelines for vibration limits and corrective actions.",
            ["VIBRATION_ANALYSIS_ISO10816", "MUD_PUMP_FLUID_END_MAINTENANCE", "Vibration"],
            1.0
        ),
        SearchDocument(
            27,
            "Oil Analysis for Hydraulic Systems",
            "Hydraulic oil analysis identifies contamination and wear in hydraulic systems. Regular sampling supports preventive maintenance and reduces equipment failure.",
            ["OIL_ANALYSIS_PROGRAMS", "Hydraulic", "Oil Analysis"],
            1.0
        ),
        SearchDocument(
            28,
            "RCM Implementation Steps",
            "Implementing Reliability Centered Maintenance involves asset criticality analysis, failure mode identification, and maintenance task optimization.",
            ["RCM_RELIABILITY_CENTERED_MAINTENANCE", "RCM", "Implementation"],
            1.0
        ),
        SearchDocument(
            29,
            "BOP Control System Inspection",
            "BOP control systems must be inspected for hydraulic leaks, electrical faults, and proper function. API RP 53 recommends quarterly control system checks.",
            ["API_RP_53_BOP_MAINTENANCE", "BOP", "Control System"],
            1.0
        ),
        SearchDocument(
            30,
            "Crane Load Testing Procedures",
            "Crane load testing verifies lifting capacity and safety. API 2C requires annual load tests and documentation for compliance.",
            ["API_2C_CRANE_INSPECTION", "Crane", "Load Testing"],
            1.0
        ),
        SearchDocument(
            31,
            "Pressure Vessel Safety Relief Device Inspection",
            "Safety relief devices on pressure vessels must be inspected and tested per NB-23 and API 510. Proper operation prevents overpressure incidents.",
            ["PRESSURE_VESSEL_INSPECTION_NB23_API510", "Pressure Vessel", "Safety Relief"],
            1.0
        ),
        SearchDocument(
            32,
            "Piping Defect Assessment",
            "Defect assessment in piping systems includes evaluating cracks, corrosion, and mechanical damage. API 570 provides guidance for defect categorization.",
            ["PIPING_INSPECTION_API570", "Piping", "Defect Assessment"],
            1.0
        ),
        SearchDocument(
            33,
            "Storage Tank Foundation Inspection",
            "Inspection of storage tank foundations ensures structural stability and prevents settlement. API 653 recommends periodic foundation checks.",
            ["STORAGE_TANK_INSPECTION_API653", "Storage Tank", "Foundation"],
            1.0
        ),
        SearchDocument(
            34,
            "Wire Rope Corrosion Evaluation",
            "Corrosion evaluation of wire ropes is performed using visual and magnetic methods. API 2C defines corrosion limits for replacement.",
            ["WIRE_ROPE_REPLACEMENT_CRITERIA", "Wire Rope", "Corrosion"],
            1.0
        ),
        SearchDocument(
            35,
            "Torque Wrench Calibration Frequency",
            "Calibration frequency for torque wrenches depends on usage and manufacturer recommendations. Regular calibration ensures measurement accuracy.",
            ["TORQUE_WRENCH_CALIBRATION", "Torque Wrench", "Calibration Frequency"],
            1.0
        ),
        SearchDocument(
            36,
            "NDT Selection for Storage Tanks",
            "Storage tank welds and plates are inspected using NDT methods such as ultrasonic and magnetic particle testing. API 653 outlines NDT requirements.",
            ["NDT_METHODS_SELECTION", "STORAGE_TANK_INSPECTION_API653", "NDT"],
            1.0
        ),
        SearchDocument(
            37,
            "Vibration Analysis for Drawworks",
            "Vibration analysis identifies mechanical faults in drawworks systems. ISO 10816 provides vibration limits and corrective actions.",
            ["VIBRATION_ANALYSIS_ISO10816", "DRAWWORKS_BRAKE_INSPECTION", "Vibration"],
            1.0
        ),
        SearchDocument(
            38,
            "Oil Analysis for Caterpillar Engines",
            "Oil analysis for Caterpillar 3512/3516 engines detects wear metals and contaminants. Regular oil sampling supports preventive maintenance.",
            ["OIL_ANALYSIS_PROGRAMS", "CATERPILLAR_3512_3516_ENGINE_MAINTENANCE", "Oil Analysis"],
            1.0
        ),
        SearchDocument(
            39,
            "RCM Failure Mode Analysis",
            "Failure mode analysis in RCM identifies potential causes of equipment failure and guides maintenance task selection.",
            ["RCM_RELIABILITY_CENTERED_MAINTENANCE", "RCM", "Failure Mode"],
            1.0
        ),
        SearchDocument(
            40,
            "BOP Functional Testing Procedures",
            "Functional testing of BOPs includes pressure tests, control system checks, and operational verification. API RP 53 recommends annual functional testing.",
            ["API_RP_53_BOP_MAINTENANCE", "BOP", "Functional Testing"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)