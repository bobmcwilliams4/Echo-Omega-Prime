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
        self.term_freqs: Dict[int, Counter] = {}
        self.inverted_index: Dict[str, set] = defaultdict(set)
        self.doc_count: int = 0
        self.avg_doc_length: float = 0.0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._preseeded = False

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            tf = Counter(tokens)
            self.documents[doc.id] = doc
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.inverted_index[term].add(doc.id)
            self.doc_count += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.doc_count
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, set()))
        scored_results = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc = self.documents[doc_id]
            final_score = bm25_score * 0.7 + tfidf_score * 0.3
            snippet = self._make_snippet(doc.content, query_terms)
            scored_results.append(SearchResult(doc_id, final_score * doc.weight, doc.title, snippet))
        scored_results.sort(key=lambda r: r.score, reverse=True)
        return scored_results[:limit]

    def get_stats(self) -> Dict[str, float]:
        return {
            'doc_count': self.doc_count,
            'avg_doc_length': self.avg_doc_length,
            'vocab_size': len(self.inverted_index)
        }

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = len(self.inverted_index.get(term, set()))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.doc_count - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str], k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc_length = self.doc_lengths[doc_id]
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        tf = self.term_freqs[doc_id]
        for term in query_terms:
            idf = self._compute_idf(term)
            freq = tf.get(term, 0)
            numerator = freq * (k1 + 1)
            denominator = freq + k1 * (1 - b + b * doc_length / avg_dl)
            if denominator == 0:
                continue
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self.term_freqs[doc_id]
        doc_length = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            term_freq = tf.get(term, 0)
            if doc_length == 0:
                continue
            norm_tf = term_freq / doc_length
            idf = self._compute_idf(term)
            score += norm_tf * idf
        return score

    def _make_snippet(self, content: str, query_terms: List[str], length: int = 160) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, token in enumerate(tokens) if token in query_terms]
        if not positions:
            snippet = ' '.join(tokens[:length])
        else:
            start = max(positions[0] - 10, 0)
            end = min(start + length, len(tokens))
            snippet = ' '.join(tokens[start:end])
        return snippet[:length] + ('...' if len(snippet) > length else '')

    def _preseed_documents(self):
        if self._preseeded:
            return
        docs = [
            SearchDocument(
                1,
                "Common Rail High Pressure Fuel System Diagnostics",
                "Diagnosing high pressure fuel systems in common rail diesel engines involves checking rail pressure sensors, pump operation, injector leak-off, and pressure control valves. Symptoms of faults include hard starting, rough idle, and power loss.",
                ["fuel system", "common rail", "diagnostics"],
                1.0
            ),
            SearchDocument(
                2,
                "Turbocharger Boost Control and Compressor Surge Analysis",
                "Boost control diagnostics require inspection of actuator response, wastegate operation, and MAP sensor readings. Compressor surge is analyzed by monitoring boost pressure oscillations and intake noise.",
                ["turbocharger", "boost control", "compressor surge"],
                1.0
            ),
            SearchDocument(
                3,
                "Diesel Particulate Filter Regeneration and Ash Loading",
                "DPF regeneration strategies include passive and active cycles. Ash loading is measured by differential pressure sensors and monitored for excessive backpressure. Faults may trigger limp mode.",
                ["DPF", "regeneration", "ash loading"],
                1.0
            ),
            SearchDocument(
                4,
                "Selective Catalytic Reduction DEF System Diagnostics",
                "SCR system diagnostics focus on DEF dosing accuracy, NOx sensor feedback, and catalyst efficiency. DEF quality and injector operation are critical for emission compliance.",
                ["SCR", "DEF", "emissions", "diagnostics"],
                1.0
            ),
            SearchDocument(
                5,
                "Glow Plug System Operation and Pre-Heat Diagnostics",
                "Glow plug system diagnostics involve checking relay operation, plug resistance, and pre-heat duration. Faults result in poor cold starting and increased white smoke.",
                ["glow plug", "pre-heat", "diagnostics"],
                1.0
            ),
            SearchDocument(
                6,
                "Diesel Fuel Quality Assessment and Contamination Analysis",
                "Fuel quality is assessed by checking for water, particulates, and microbial contamination. Laboratory analysis and on-board sensors help detect issues affecting combustion and injector life.",
                ["fuel quality", "contamination", "assessment"],
                1.0
            ),
            SearchDocument(
                7,
                "Diesel Engine Compression Testing and Cylinder Sealing",
                "Compression testing reveals cylinder sealing issues, such as worn rings or leaking valves. Low compression leads to hard starting and reduced power. Test results are compared to manufacturer specs.",
                ["compression", "cylinder sealing", "testing"],
                1.0
            ),
            SearchDocument(
                8,
                "Diesel Injection Timing and Valve Train Synchronization",
                "Injection timing diagnostics use crank and cam sensor data to verify synchronization. Incorrect timing causes misfire, excessive smoke, and engine knock.",
                ["injection timing", "valve train", "synchronization"],
                1.0
            ),
            SearchDocument(
                9,
                "EGR System Diagnostics and Cooler Fouling Analysis",
                "EGR diagnostics include valve position checks, flow measurements, and cooler fouling inspection. Blocked coolers increase NOx emissions and reduce engine efficiency.",
                ["EGR", "cooler fouling", "diagnostics"],
                1.0
            ),
            SearchDocument(
                10,
                "Diesel Engine Oil Analysis and Wear Metal Trending",
                "Oil analysis detects wear metals, soot, and fuel dilution. Trending results help predict engine failure and optimize maintenance intervals.",
                ["oil analysis", "wear metals", "trending"],
                1.0
            ),
            SearchDocument(
                11,
                "Diesel Engine Cooling System and Cavitation Analysis",
                "Cooling system diagnostics involve checking coolant flow, thermostat operation, and cavitation signs. Cavitation causes pitting and premature failure of cylinder liners.",
                ["cooling system", "cavitation", "analysis"],
                1.0
            ),
            SearchDocument(
                12,
                "Diesel Engine Electrical System and Charging Analysis",
                "Electrical diagnostics include battery testing, alternator output checks, and wiring inspection. Charging faults cause starting issues and electronic system malfunctions.",
                ["electrical system", "charging", "analysis"],
                1.0
            ),
            SearchDocument(
                13,
                "Diesel Fuel Injector Flow Balance and Pattern Testing",
                "Injector flow balance testing ensures uniform fuel delivery. Pattern testing identifies nozzle clogging and spray anomalies, affecting combustion efficiency.",
                ["injector", "flow balance", "pattern testing"],
                1.0
            ),
            SearchDocument(
                14,
                "Diesel Crankcase Ventilation and Blowby Management",
                "Crankcase ventilation diagnostics check for excessive blowby, filter clogging, and oil mist. Proper management prevents pressure buildup and oil leaks.",
                ["crankcase ventilation", "blowby", "management"],
                1.0
            ),
            SearchDocument(
                15,
                "Common Rail Injector Leak-Off Testing Procedure",
                "Leak-off testing measures return flow from injectors to detect internal leaks. Excessive leak-off indicates worn injector seals or damaged internal components.",
                ["injector", "leak-off", "testing"],
                1.0
            ),
            SearchDocument(
                16,
                "DPF Pressure Sensor Calibration and Fault Codes",
                "DPF pressure sensor calibration is critical for accurate ash loading detection. Fault codes are diagnosed using scan tools and sensor voltage readings.",
                ["DPF", "pressure sensor", "calibration"],
                1.0
            ),
            SearchDocument(
                17,
                "Turbocharger Wastegate Actuator Testing",
                "Wastegate actuator testing involves vacuum or electronic control checks. Faulty actuators cause boost pressure deviations and possible compressor surge.",
                ["turbocharger", "wastegate", "actuator"],
                1.0
            ),
            SearchDocument(
                18,
                "SCR NOx Sensor Feedback and Catalyst Efficiency",
                "NOx sensor feedback is used to optimize DEF dosing and monitor catalyst efficiency. Faulty sensors lead to incorrect emission control and OBD codes.",
                ["SCR", "NOx sensor", "catalyst efficiency"],
                1.0
            ),
            SearchDocument(
                19,
                "Glow Plug Relay Testing and Replacement",
                "Relay testing ensures proper glow plug operation. Faulty relays cause extended pre-heat times and cold start difficulties.",
                ["glow plug", "relay", "testing"],
                1.0
            ),
            SearchDocument(
                20,
                "Diesel Fuel Water Separator Diagnostics",
                "Water separator diagnostics involve checking sensor operation and drain intervals. Water contamination leads to injector damage and corrosion.",
                ["fuel", "water separator", "diagnostics"],
                1.0
            ),
            SearchDocument(
                21,
                "Cylinder Pressure Analysis for Engine Performance",
                "Cylinder pressure analysis identifies combustion anomalies and mechanical faults. Data is used to optimize injection timing and valve train synchronization.",
                ["cylinder pressure", "performance", "analysis"],
                1.0
            ),
            SearchDocument(
                22,
                "EGR Cooler Cleaning and Flow Restoration",
                "EGR cooler cleaning restores flow and reduces NOx emissions. Blocked coolers are cleaned using chemical or mechanical methods.",
                ["EGR", "cooler", "cleaning"],
                1.0
            ),
            SearchDocument(
                23,
                "Diesel Engine Oil Contamination and Filter Diagnostics",
                "Oil contamination diagnostics involve checking for coolant, fuel, and particulate ingress. Filter diagnostics ensure proper oil flow and protection.",
                ["oil", "contamination", "filter"],
                1.0
            ),
            SearchDocument(
                24,
                "Diesel Engine Battery Testing and Replacement",
                "Battery testing checks voltage, capacity, and internal resistance. Replacement is recommended when performance drops below manufacturer specs.",
                ["battery", "testing", "replacement"],
                1.0
            ),
            SearchDocument(
                25,
                "Diesel Engine Cooling System Leak Detection",
                "Leak detection involves pressure testing, visual inspection, and dye tracing. Cooling system leaks cause overheating and engine damage.",
                ["cooling system", "leak detection", "diagnostics"],
                1.0
            ),
            SearchDocument(
                26,
                "Diesel Fuel Injector Coding and Adaptation",
                "Injector coding and adaptation are performed after replacement to ensure proper fuel delivery. Coding errors cause misfire and rough running.",
                ["injector", "coding", "adaptation"],
                1.0
            ),
            SearchDocument(
                27,
                "Diesel Engine Blowby Measurement and Analysis",
                "Blowby measurement quantifies combustion gas leakage past piston rings. Excessive blowby indicates worn rings or cylinder wall damage.",
                ["blowby", "measurement", "analysis"],
                1.0
            ),
            SearchDocument(
                28,
                "Diesel Engine Thermostat Testing and Replacement",
                "Thermostat testing ensures proper coolant temperature regulation. Faulty thermostats cause overheating or slow warm-up.",
                ["thermostat", "testing", "replacement"],
                1.0
            ),
            SearchDocument(
                29,
                "Diesel Engine Alternator Output Testing",
                "Alternator output testing checks voltage and current under load. Faulty alternators cause battery charging issues and electrical malfunctions.",
                ["alternator", "output", "testing"],
                1.0
            ),
            SearchDocument(
                30,
                "Diesel Engine Valve Train Wear Analysis",
                "Valve train wear analysis includes checking cam lobes, lifters, and rocker arms. Excessive wear leads to valve timing errors and reduced performance.",
                ["valve train", "wear", "analysis"],
                1.0
            ),
            SearchDocument(
                31,
                "Diesel Engine EGR Valve Position Sensor Diagnostics",
                "EGR valve position sensor diagnostics ensure proper feedback for emission control. Faulty sensors cause incorrect EGR flow and increased NOx emissions.",
                ["EGR", "valve position", "sensor"],
                1.0
            ),
            SearchDocument(
                32,
                "Diesel Engine Oil Pressure Sensor Testing",
                "Oil pressure sensor testing checks for accurate readings and sensor response. Faulty sensors cause incorrect oil pressure warnings and engine protection faults.",
                ["oil pressure", "sensor", "testing"],
                1.0
            ),
            SearchDocument(
                33,
                "Diesel Engine Cylinder Head Gasket Leak Diagnostics",
                "Cylinder head gasket leak diagnostics involve pressure testing, coolant analysis, and exhaust gas detection. Leaks cause overheating and loss of compression.",
                ["cylinder head", "gasket", "leak"],
                1.0
            ),
            SearchDocument(
                34,
                "Diesel Engine Fuel Pump Testing and Replacement",
                "Fuel pump testing checks flow rate and pressure. Replacement is required when pump performance drops below specification.",
                ["fuel pump", "testing", "replacement"],
                1.0
            ),
            SearchDocument(
                35,
                "Diesel Engine Injector Spray Pattern Analysis",
                "Injector spray pattern analysis uses imaging or paper tests to detect nozzle clogging and uneven distribution. Proper patterns ensure efficient combustion.",
                ["injector", "spray pattern", "analysis"],
                1.0
            ),
        ]
        for doc in docs:
            self.add_document(doc)
        self._preseeded = True

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _search_index_instance._preseed_documents()
        return _search_index_instance