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
        self.term_freqs: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
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
            tf_counter = Counter(tokens)
            self.term_freqs[doc.id] = tf_counter
            for term in tf_counter:
                self.term_doc_freq[term] += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scores: Dict[int, float] = defaultdict(float)
        tfidf_scores: Dict[int, float] = defaultdict(float)
        for doc_id, doc in self.documents.items():
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            combined_score = bm25_score * 0.7 + tfidf_score * 0.3
            scores[doc_id] = combined_score * doc.weight
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq)
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
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
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        tf_counter = self.term_freqs.get(doc_id, {})
        for term in query_terms:
            tf = tf_counter.get(term, 0)
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_length / avg_dl)
            if denominator == 0:
                continue
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        tf_counter = self.term_freqs.get(doc_id, {})
        doc_length = self.doc_lengths.get(doc_id, 0)
        for term in query_terms:
            tf = tf_counter.get(term, 0)
            if doc_length > 0:
                tf_norm = tf / doc_length
            else:
                tf_norm = 0.0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, content: str, query_terms: List[str]) -> str:
        tokens = self._tokenize(content)
        positions = []
        for idx, token in enumerate(tokens):
            if token in query_terms:
                positions.append(idx)
        if not positions:
            return ' '.join(tokens[:30]) + ('...' if len(tokens) > 30 else '')
        start = max(positions[0] - 10, 0)
        end = min(positions[0] + 20, len(tokens))
        snippet = tokens[start:end]
        snippet_text = ' '.join(snippet)
        for term in query_terms:
            snippet_text = re.sub(r'\b{}\b'.format(re.escape(term)), f'**{term}**', snippet_text, flags=re.IGNORECASE)
        return snippet_text + ('...' if end < len(tokens) else '')

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
            "GDI High Pressure System Design",
            "Gasoline Direct Injection (GDI) systems require robust high-pressure fuel pumps, precise injector placement, and optimized rail geometry to ensure atomization and combustion efficiency. Key design elements include pump cam profiles, pressure regulation, and material selection for durability.",
            ["GDI", "High Pressure", "Design", "Fuel Pump", "Injector"],
            1.2
        ),
        SearchDocument(
            2,
            "Port Fuel Injection Timing and Synchronization",
            "Port fuel injection relies on accurate timing relative to intake valve events. Synchronization with engine cycles maximizes fuel vaporization and minimizes wall wetting. Strategies include sequential and batch injection, with calibration for cold start and transient operation.",
            ["Port Injection", "Timing", "Synchronization", "Valve", "Calibration"],
            1.0
        ),
        SearchDocument(
            3,
            "Fuel Pump Performance and Failure Analysis",
            "Fuel pump performance is evaluated by flow rate, pressure stability, and response to demand changes. Common failures include cavitation, electrical faults, and wear. Diagnostic procedures involve pressure testing, waveform analysis, and inspection for contamination.",
            ["Fuel Pump", "Performance", "Failure", "Diagnostics", "Waveform"],
            1.1
        ),
        SearchDocument(
            4,
            "Fuel Rail Design and Pressure Dynamics",
            "Fuel rail geometry affects pressure pulsations and injector feed consistency. Design considerations include material rigidity, damping features, and integration of pressure sensors. Computational fluid dynamics (CFD) is used to optimize flow and minimize resonance.",
            ["Fuel Rail", "Pressure", "Design", "CFD", "Sensors"],
            1.0
        ),
        SearchDocument(
            5,
            "EVAP System and Fuel Vapor Management",
            "Evaporative Emission (EVAP) systems capture and recycle fuel vapors to reduce emissions. Components include purge valves, charcoal canisters, and leak detection monitors. Diagnostics focus on DTCs, purge flow rates, and system integrity testing.",
            ["EVAP", "Fuel Vapor", "Emissions", "Purge", "Diagnostics"],
            1.0
        ),
        SearchDocument(
            6,
            "Fuel Quality Specifications and Testing",
            "Fuel quality is defined by octane rating, volatility, sulfur content, and contamination levels. Testing methods include ASTM standards, spectrometry, and filter analysis. Poor quality can cause injector fouling, pump wear, and emission failures.",
            ["Fuel Quality", "Testing", "Octane", "Contamination", "ASTM"],
            1.0
        ),
        SearchDocument(
            7,
            "E85 and Flex-Fuel System Design",
            "Flex-fuel vehicles accommodate E85 ethanol blends via corrosion-resistant materials, adaptive fuel trim, and ethanol sensors. System calibration addresses cold start enrichment and vapor pressure variations. Injector sizing and pump capacity are critical for performance.",
            ["E85", "Flex-Fuel", "Design", "Ethanol", "Calibration"],
            1.1
        ),
        SearchDocument(
            8,
            "CNG and LPG Conversion Systems",
            "Compressed Natural Gas (CNG) and Liquefied Petroleum Gas (LPG) conversions require specialized injectors, regulators, and tank safety features. Engine mapping and fuel trim adaptation are essential for drivability and emissions compliance.",
            ["CNG", "LPG", "Conversion", "Injectors", "Regulators"],
            1.0
        ),
        SearchDocument(
            9,
            "Fuel Trim Analysis and Diagnostics",
            "Fuel trim diagnostics involve monitoring short-term and long-term adjustments made by the ECU to maintain stoichiometry. Analysis includes OBDII data, sensor feedback, and identifying causes of lean or rich conditions such as vacuum leaks or injector issues.",
            ["Fuel Trim", "Diagnostics", "OBDII", "Sensors", "Stoichiometry"],
            1.0
        ),
        SearchDocument(
            10,
            "Common Rail Diesel Injection Systems",
            "Common rail diesel systems utilize high-pressure accumulators, solenoid or piezo injectors, and precise electronic control. Advantages include multi-stage injection, reduced noise, and improved emissions. Maintenance involves filter changes and pressure testing.",
            ["Diesel", "Common Rail", "Injection", "Piezo", "Maintenance"],
            1.2
        ),
        SearchDocument(
            11,
            "Injector Flow Testing and Cleaning",
            "Injector flow testing measures delivery rates and spray patterns using bench equipment. Cleaning methods include ultrasonic baths, reverse flushing, and chemical treatments. Proper maintenance prevents misfire, poor economy, and emission failures.",
            ["Injector", "Flow Testing", "Cleaning", "Maintenance", "Spray Pattern"],
            1.0
        ),
        SearchDocument(
            12,
            "Returnless Fuel System Design",
            "Returnless fuel systems eliminate the return line by regulating pressure at the tank. Benefits include reduced vapor generation and improved emissions. Design challenges involve pump control, sensor integration, and transient response calibration.",
            ["Returnless", "Fuel System", "Design", "Pressure", "Sensors"],
            1.0
        ),
        SearchDocument(
            13,
            "Fuel Pressure Diagnostics and Testing",
            "Fuel pressure diagnostics use mechanical gauges and electronic sensors to verify system operation. Testing procedures include static and dynamic measurements, leak checks, and regulator performance evaluation. Faults can cause starting issues and drivability complaints.",
            ["Fuel Pressure", "Diagnostics", "Testing", "Regulator", "Sensors"],
            1.0
        ),
        SearchDocument(
            14,
            "Fuel System Contamination and Filtration",
            "Contamination sources include water, particulates, and microbial growth. Filtration strategies use multi-stage filters, water separators, and regular maintenance schedules. Effects include injector clogging, pump wear, and emission failures.",
            ["Contamination", "Filtration", "Fuel System", "Maintenance", "Injector"],
            1.0
        ),
        SearchDocument(
            15,
            "Cold Start Enrichment and Warm-Up Control",
            "Cold start enrichment increases fuel delivery to compensate for poor vaporization. Warm-up control involves temperature sensors, ECU mapping, and injector timing. Proper calibration ensures reduced emissions and improved drivability during cold operation.",
            ["Cold Start", "Enrichment", "Warm-Up", "Calibration", "Sensors"],
            1.0
        ),
        SearchDocument(
            16,
            "Fuel System OBDII Diagnostics and DTCs",
            "OBDII diagnostics monitor fuel system operation via sensors and actuators. Diagnostic Trouble Codes (DTCs) indicate faults such as misfire, lean/rich conditions, and evaporative leaks. Scan tools and live data analysis are used for troubleshooting.",
            ["OBDII", "Diagnostics", "DTCs", "Sensors", "Troubleshooting"],
            1.0
        ),
        SearchDocument(
            17,
            "Performance Fuel System Modifications",
            "Performance modifications include high-flow injectors, upgraded pumps, and larger fuel rails. Calibration is required for increased flow rates and altered pressure dynamics. Safety considerations involve fire prevention and compliance with regulations.",
            ["Performance", "Modifications", "Injectors", "Fuel Pump", "Calibration"],
            1.1
        ),
        SearchDocument(
            18,
            "Fuel System Safety and Fire Prevention",
            "Safety measures include proper routing of fuel lines, use of fire-resistant materials, and integration of shut-off valves. Fire prevention strategies involve leak detection, electrical isolation, and compliance with safety standards.",
            ["Safety", "Fire Prevention", "Fuel Lines", "Materials", "Valves"],
            1.0
        ),
        SearchDocument(
            19,
            "Diesel Fuel Quality and Cold Weather Operation",
            "Diesel fuel quality is affected by cetane rating, sulfur content, and contamination. Cold weather operation requires anti-gel additives, heated filters, and proper storage. Poor quality can cause injector fouling, pump wear, and starting issues.",
            ["Diesel", "Fuel Quality", "Cold Weather", "Additives", "Injector"],
            1.0
        ),
        SearchDocument(
            20,
            "Fuel System Corrosion and Material Compatibility",
            "Corrosion prevention involves material selection, coatings, and regular inspection. Compatibility with ethanol and biodiesel blends is critical for long-term durability. Failure modes include pitting, leaks, and structural degradation.",
            ["Corrosion", "Material Compatibility", "Ethanol", "Biodiesel", "Durability"],
            1.0
        ),
        SearchDocument(
            21,
            "Fuel Injector Electrical Diagnostics and Waveform Analysis",
            "Electrical diagnostics for injectors include resistance measurement, waveform analysis, and pulse width verification. Faults may manifest as misfire, rough idle, or emission failures. Oscilloscope testing is used for detailed analysis.",
            ["Injector", "Electrical Diagnostics", "Waveform", "Pulse Width", "Oscilloscope"],
            1.0
        ),
        SearchDocument(
            22,
            "Fuel System Calibration for E85",
            "Calibration for E85 involves adjusting injector pulse width, fuel trim, and cold start enrichment. Ethanol sensors provide feedback for adaptive mapping. Proper calibration ensures performance and emission compliance.",
            ["Calibration", "E85", "Fuel Trim", "Ethanol", "Sensors"],
            1.0
        ),
        SearchDocument(
            23,
            "Fuel Rail Pressure Sensor Integration",
            "Pressure sensors integrated into fuel rails provide real-time feedback for ECU control. Sensor selection involves accuracy, response time, and durability. Integration challenges include electrical noise and thermal effects.",
            ["Pressure Sensor", "Fuel Rail", "Integration", "ECU", "Durability"],
            1.0
        ),
        SearchDocument(
            24,
            "Injector Spray Pattern Optimization",
            "Optimizing injector spray patterns improves atomization and combustion. Factors include nozzle geometry, pressure, and pulse duration. Testing involves high-speed imaging and flow bench analysis.",
            ["Injector", "Spray Pattern", "Optimization", "Atomization", "Testing"],
            1.0
        ),
        SearchDocument(
            25,
            "Fuel System Leak Detection and Repair",
            "Leak detection methods include pressure decay testing, dye tracing, and electronic sniffers. Repair procedures involve component replacement, seal inspection, and torque verification. Leaks affect safety, emissions, and drivability.",
            ["Leak Detection", "Repair", "Fuel System", "Pressure", "Safety"],
            1.0
        ),
        SearchDocument(
            26,
            "Fuel System Sensor Types and Diagnostics",
            "Fuel system sensors include pressure, temperature, and ethanol content sensors. Diagnostics involve signal analysis, calibration, and replacement. Sensor faults can cause drivability issues and emission failures.",
            ["Sensors", "Diagnostics", "Pressure", "Temperature", "Ethanol"],
            1.0
        ),
        SearchDocument(
            27,
            "Fuel System Control Algorithms",
            "Control algorithms manage fuel delivery, pressure regulation, and injector timing. Adaptive strategies use sensor feedback and learning cycles. Calibration is critical for performance, emissions, and reliability.",
            ["Control Algorithms", "Calibration", "Injector Timing", "Pressure", "Sensors"],
            1.0
        ),
        SearchDocument(
            28,
            "Fuel System Design for CNG Vehicles",
            "CNG fuel system design includes high-pressure tanks, regulators, and injectors. Safety features involve pressure relief devices and leak detection. Engine mapping adapts to CNG combustion characteristics.",
            ["CNG", "Design", "Regulators", "Injectors", "Safety"],
            1.0
        ),
        SearchDocument(
            29,
            "Fuel System Maintenance Scheduling",
            "Maintenance scheduling involves filter replacement, pump inspection, and injector cleaning. Regular maintenance prevents failures, improves performance, and ensures emission compliance.",
            ["Maintenance", "Scheduling", "Filter", "Pump", "Injector"],
            1.0
        ),
        SearchDocument(
            30,
            "Fuel System Emission Compliance",
            "Emission compliance requires proper calibration, leak prevention, and vapor management. Regulatory standards dictate allowable emissions and testing procedures. System design must address evaporative and exhaust emissions.",
            ["Emission", "Compliance", "Calibration", "Leak Prevention", "Vapor Management"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)