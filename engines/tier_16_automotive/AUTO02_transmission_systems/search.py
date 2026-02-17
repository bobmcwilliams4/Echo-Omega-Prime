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
        self.doc_tokens: Dict[int, List[str]] = {}
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_doc_map: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.lock = threading.Lock()
        self._recalc_stats()

    def _recalc_stats(self):
        with self.lock:
            self.avg_doc_length = (
                sum(self.doc_lengths.values()) / len(self.doc_lengths)
                if self.doc_lengths else 0.0
            )

    def add_document(self, doc: SearchDocument):
        with self.lock:
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.title + " " + doc.content)
            self.doc_tokens[doc.id] = tokens
            self.doc_lengths[doc.id] = len(tokens)
            token_counts = Counter(tokens)
            for token in token_counts:
                self.term_doc_freq[token] += 1
                self.term_doc_map[token][doc.id] = token_counts[token]
            self._recalc_stats()

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        N = len(self.documents)
        df = self.term_doc_freq.get(term, 0)
        return math.log(1 + (N - df + 0.5) / (df + 0.5))

    def _score_bm25(self, query_terms: List[str], doc_id: int, k1=1.5, b=0.75) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        doc = self.documents[doc_id]
        for term in query_terms:
            tf = self.term_doc_map.get(term, {}).get(doc_id, 0)
            idf = self._compute_idf(term)
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * doc_len / avg_dl)
            score += idf * (numerator / denominator) if denominator else 0.0
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        doc = self.documents[doc_id]
        for term in query_terms:
            tf = self.term_doc_map.get(term, {}).get(doc_id, 0)
            norm_tf = tf / doc_len if doc_len > 0 else 0
            idf = self._compute_idf(term)
            score += norm_tf * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.term_doc_map.get(term, {}).keys())
        scored_docs = []
        for doc_id in candidate_docs:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                doc = self.documents[doc_id]
                snippet = self._make_snippet(doc, query_terms)
                scored_docs.append(SearchResult(doc_id, score, doc.title, snippet))
        scored_docs.sort(key=lambda r: r.score, reverse=True)
        return scored_docs[:limit]

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str]) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:160] + "..." if len(content) > 160 else content
        start = max(positions[0] - 10, 0)
        end = min(positions[0] + 30, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        return snippet[:160] + "..." if len(snippet) > 160 else snippet

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "num_documents": len(self.documents),
                "avg_doc_length": self.avg_doc_length,
                "num_unique_terms": len(self.term_doc_freq),
            }

# Singleton factory
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
            "Manual Transmission Synchronizer Design Principles",
            "Synchronizers enable smooth gear shifts in manual transmissions by matching shaft speeds. Key design factors include cone angle, friction material, and spring force. Common failures are excessive wear and poor engagement.",
            ["manual", "synchronizer", "design", "failure"],
            1.0
        ),
        SearchDocument(
            2,
            "Automatic Transmission Planetary Gear Set Design",
            "Planetary gear sets are the foundation of automatic transmissions, providing multiple gear ratios. Design involves sun, planet, and ring gears, carrier, and clutch/brake elements. Diagnosis includes checking for gear tooth wear and carrier cracks.",
            ["automatic", "planetary", "gear", "design"],
            1.0
        ),
        SearchDocument(
            3,
            "Torque Converter Operation and Diagnosis",
            "Torque converters transfer engine power to the transmission using fluid coupling. Operation phases: stall, coupling, and lockup. Diagnosing issues involves checking for shudder, leaks, and lockup clutch failure.",
            ["torque", "converter", "operation", "diagnosis"],
            1.0
        ),
        SearchDocument(
            4,
            "CVT Belt/Chain System Design and Failure Modes",
            "CVTs use steel belts or chains to provide variable gear ratios. Design focuses on belt tension, pulley shape, and lubrication. Failures include belt slippage, chain stretching, and pulley wear.",
            ["cvt", "belt", "chain", "design", "failure"],
            1.0
        ),
        SearchDocument(
            5,
            "Dual Clutch Transmission (DCT) Operation",
            "DCTs use two clutches for fast gear changes. Operation involves alternating between odd and even gear shafts. Diagnosis includes checking for clutch wear, actuator faults, and shift quality.",
            ["dual", "clutch", "dct", "operation", "diagnosis"],
            1.0
        ),
        SearchDocument(
            6,
            "Transfer Case Design - Part-Time vs Full-Time 4WD",
            "Transfer cases distribute torque between axles. Part-time 4WD uses manual engagement, full-time uses differential. Design considerations include chain vs gear drive, lubrication, and shift mechanisms.",
            ["transfer", "case", "4wd", "design"],
            1.0
        ),
        SearchDocument(
            7,
            "Differential Types and Limited-Slip Operation",
            "Differentials allow wheels to rotate at different speeds. Types: open, limited-slip, locking. Limited-slip uses clutches or gears to transfer torque. Diagnosis involves checking for chatter, wear, and fluid leaks.",
            ["differential", "limited-slip", "operation", "diagnosis"],
            1.0
        ),
        SearchDocument(
            8,
            "Transmission Fluid Analysis and Specification",
            "Transmission fluid lubricates and cools components. Analysis includes viscosity, contamination, and additive depletion. Specification depends on transmission type and manufacturer requirements.",
            ["fluid", "analysis", "specification"],
            1.0
        ),
        SearchDocument(
            9,
            "Clutch Hydraulic System Operation and Diagnosis",
            "Hydraulic clutches use master and slave cylinders for actuation. Diagnosis includes checking for leaks, pedal feel, and pressure loss. Design focuses on cylinder sizing and fluid selection.",
            ["clutch", "hydraulic", "operation", "diagnosis"],
            1.0
        ),
        SearchDocument(
            10,
            "Automatic Transmission Pressure Testing and Diagnosis",
            "Pressure testing identifies faults in automatic transmission hydraulics. Tools include gauges and scan tools. Diagnosis covers low pressure, solenoid failure, and valve body issues.",
            ["automatic", "pressure", "testing", "diagnosis"],
            1.0
        ),
        SearchDocument(
            11,
            "Transmission Control Module (TCM) Adaptive Learning",
            "TCMs adapt shift strategies based on driving style and wear. Learning algorithms adjust shift points and clutch engagement. Diagnosis includes checking for adaptation errors and software updates.",
            ["tcm", "adaptive", "learning", "diagnosis"],
            1.0
        ),
        SearchDocument(
            12,
            "Toyota Hybrid Transaxle (eCVT) Operation",
            "Toyota's eCVT uses planetary gear sets and electric motors for seamless power delivery. Operation involves blending engine and motor torque. Diagnosis includes checking for motor faults and gear wear.",
            ["toyota", "hybrid", "ecvt", "operation", "diagnosis"],
            1.0
        ),
        SearchDocument(
            13,
            "Transmission Rebuild Quality Gates and Inspection",
            "Rebuilding transmissions requires quality gates: teardown, cleaning, inspection, assembly, and testing. Inspection covers gear wear, bearing condition, and hydraulic integrity.",
            ["rebuild", "quality", "inspection"],
            1.0
        ),
        SearchDocument(
            14,
            "Drivetrain NVH (Noise, Vibration, Harshness) Diagnosis",
            "NVH issues in transmissions arise from gear mesh, bearing wear, and imbalance. Diagnosis uses spectrum analysis, road tests, and component isolation. Solutions include gear redesign and damping.",
            ["drivetrain", "nvh", "noise", "vibration", "diagnosis"],
            1.0
        ),
        SearchDocument(
            15,
            "Performance Transmission Tuning and Modifications",
            "Performance tuning involves upgrading clutches, shift solenoids, and gear ratios. Modifications improve durability and shift speed. Diagnosis includes checking for excessive heat and premature wear.",
            ["performance", "tuning", "modification"],
            1.0
        ),
        SearchDocument(
            16,
            "Final Drive Ratio Selection and Gear Ratio Calculations",
            "Selecting final drive ratios affects acceleration and fuel economy. Calculations involve gear tooth counts and desired speed range. Diagnosis includes checking for incorrect ratios and drivability issues.",
            ["final", "drive", "ratio", "gear", "calculation"],
            1.0
        ),
        SearchDocument(
            17,
            "Fleet Transmission Maintenance and Predictive Monitoring",
            "Fleet maintenance uses predictive monitoring to reduce downtime. Techniques include fluid analysis, telematics, and scheduled inspections. Diagnosis covers wear patterns and abnormal temperature spikes.",
            ["fleet", "maintenance", "predictive", "monitoring"],
            1.0
        ),
        SearchDocument(
            18,
            "Transmission Temperature Management and Cooling Systems",
            "Managing transmission temperature is critical for longevity. Cooling systems include heat exchangers, fans, and fluid circuits. Diagnosis includes checking for overheating and coolant leaks.",
            ["temperature", "management", "cooling", "system"],
            1.0
        ),
        SearchDocument(
            19,
            "Manual Transmission Gear Tooth Wear and Diagnosis",
            "Gear tooth wear in manual transmissions leads to noise and shifting issues. Diagnosis includes visual inspection, pattern analysis, and measuring backlash.",
            ["manual", "gear", "wear", "diagnosis"],
            1.0
        ),
        SearchDocument(
            20,
            "Automatic Transmission Solenoid Function and Failure",
            "Solenoids control hydraulic flow in automatic transmissions. Failures cause shift errors and pressure loss. Diagnosis includes electrical testing and scan tool analysis.",
            ["automatic", "solenoid", "failure", "diagnosis"],
            1.0
        ),
        SearchDocument(
            21,
            "CVT Pulley Design and Lubrication",
            "CVT pulleys require precise machining and lubrication to prevent wear. Design focuses on surface finish and oil selection. Diagnosis includes checking for scoring and lubrication breakdown.",
            ["cvt", "pulley", "design", "lubrication"],
            1.0
        ),
        SearchDocument(
            22,
            "Dual Clutch Actuator Calibration",
            "Actuators in DCTs require calibration for optimal shift performance. Calibration involves sensor alignment and software updates. Diagnosis covers actuator lag and calibration errors.",
            ["dual", "clutch", "actuator", "calibration"],
            1.0
        ),
        SearchDocument(
            23,
            "Transfer Case Chain Wear and Replacement",
            "Chains in transfer cases stretch and wear over time. Replacement involves measuring chain length and inspecting sprockets. Diagnosis includes checking for noise and engagement issues.",
            ["transfer", "case", "chain", "wear", "replacement"],
            1.0
        ),
        SearchDocument(
            24,
            "Limited-Slip Differential Clutch Pack Inspection",
            "Clutch packs in limited-slip differentials wear and lose effectiveness. Inspection includes measuring friction material thickness and checking for chatter.",
            ["limited-slip", "differential", "clutch", "inspection"],
            1.0
        ),
        SearchDocument(
            25,
            "Transmission Fluid Specification for Hybrid Vehicles",
            "Hybrid transmissions require specialized fluid for electric motor compatibility. Specification includes dielectric strength, viscosity, and additive package.",
            ["fluid", "specification", "hybrid", "transmission"],
            1.0
        ),
        SearchDocument(
            26,
            "Clutch Hydraulic System Bleeding Procedure",
            "Bleeding hydraulic clutch systems removes air for proper operation. Procedure involves using vacuum tools or manual pumping. Diagnosis includes checking for spongy pedal and incomplete bleeding.",
            ["clutch", "hydraulic", "bleeding", "procedure"],
            1.0
        ),
        SearchDocument(
            27,
            "Automatic Transmission Valve Body Design",
            "Valve bodies direct hydraulic flow for gear changes. Design includes channel layout, solenoid placement, and material selection. Diagnosis covers shift errors and fluid contamination.",
            ["automatic", "valve", "body", "design"],
            1.0
        ),
        SearchDocument(
            28,
            "Transmission Control Module Software Update",
            "TCM software updates improve shift quality and fix bugs. Procedure involves using OEM tools and verifying update success. Diagnosis includes checking for update errors and compatibility.",
            ["tcm", "software", "update"],
            1.0
        ),
        SearchDocument(
            29,
            "Toyota Hybrid Transaxle Motor Diagnosis",
            "Motor faults in Toyota hybrid transaxles cause reduced efficiency. Diagnosis includes scan tool analysis, resistance measurement, and gear inspection.",
            ["toyota", "hybrid", "transaxle", "motor", "diagnosis"],
            1.0
        ),
        SearchDocument(
            30,
            "Transmission Rebuild Assembly Techniques",
            "Proper assembly techniques ensure transmission reliability. Techniques include torque specs, alignment, and seal installation. Inspection covers assembly errors and component fit.",
            ["rebuild", "assembly", "technique", "inspection"],
            1.0
        ),
        SearchDocument(
            31,
            "Drivetrain NVH Reduction Strategies",
            "Reducing NVH involves balancing shafts, using dampers, and optimizing gear mesh. Diagnosis includes spectrum analysis and test drives.",
            ["drivetrain", "nvh", "reduction", "strategy"],
            1.0
        ),
        SearchDocument(
            32,
            "Performance Transmission Fluid Selection",
            "Performance transmissions require fluids with high shear stability and thermal resistance. Selection involves matching fluid to clutch material and gear type.",
            ["performance", "fluid", "selection"],
            1.0
        ),
        SearchDocument(
            33,
            "Final Drive Ratio Impact on Vehicle Dynamics",
            "Final drive ratios affect acceleration, top speed, and fuel consumption. Calculations involve tire size and gear ratios. Diagnosis includes checking for drivability complaints.",
            ["final", "drive", "ratio", "vehicle", "dynamics"],
            1.0
        ),
        SearchDocument(
            34,
            "Fleet Transmission Predictive Analytics",
            "Predictive analytics use machine learning to forecast transmission failures. Data sources include telematics, fluid sensors, and maintenance logs.",
            ["fleet", "transmission", "predictive", "analytics"],
            1.0
        ),
        SearchDocument(
            35,
            "Transmission Cooling System Upgrades",
            "Upgrading cooling systems improves transmission durability. Upgrades include larger heat exchangers, electric fans, and improved fluid routing.",
            ["cooling", "system", "upgrade"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)