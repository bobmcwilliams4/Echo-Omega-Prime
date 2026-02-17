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
        self.k1 = 1.5
        self.b = 0.75
        self.idf_cache: Dict[str, float] = {}
        self.tf_idf_cache: Dict[int, Dict[str, float]] = defaultdict(dict)
        self._preseeded = False

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9\-]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.term_freqs[doc.id] = Counter(tokens)
            for term in self.term_freqs[doc.id]:
                self.term_doc_freq[term] += 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs
            self.idf_cache.clear()
            self.tf_idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        doc = self.documents[doc_id]
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0)
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / (self.avg_doc_length if self.avg_doc_length > 0 else 1))
            bm25_term = idf * (numerator / (denominator if denominator > 0 else 1))
            score += bm25_term
        return score * doc.weight

    def _score_tf_idf(self, query_terms: List[str], doc_id: int) -> float:
        if doc_id in self.tf_idf_cache and all(term in self.tf_idf_cache[doc_id] for term in query_terms):
            return sum(self.tf_idf_cache[doc_id][term] for term in query_terms)
        doc_len = self.doc_lengths.get(doc_id, 0)
        tf_idf_score = 0.0
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0)
            norm_tf = tf / (doc_len if doc_len > 0 else 1)
            idf = self._compute_idf(term)
            tf_idf = norm_tf * idf
            self.tf_idf_cache[doc_id][term] = tf_idf
            tf_idf_score += tf_idf
        return tf_idf_score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10, use_tf_idf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: List[Tuple[int, float]] = []
        for doc_id in self.documents:
            if use_tf_idf:
                score = self._score_tf_idf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                doc_scores.append((doc_id, score))
        doc_scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in doc_scores[:limit]:
            doc = self.documents[doc_id]
            snippet = self._generate_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _generate_snippet(self, content: str, query_terms: List[str], snippet_length: int = 160) -> str:
        tokens = self._tokenize(content)
        if not tokens:
            return ''
        positions = [i for i, token in enumerate(tokens) if token in query_terms]
        if not positions:
            return ' '.join(tokens[:snippet_length])
        start = max(positions[0] - snippet_length // 2, 0)
        end = min(start + snippet_length, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in query_terms:
            snippet = re.sub(r'\b({})\b'.format(re.escape(term)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
        }

    def _preseed_documents(self):
        if self._preseeded:
            return
        docs = [
            SearchDocument(
                1,
                "Diesel-Electric Prime Movers: Fundamentals",
                "Diesel-electric locomotives use large diesel engines (prime movers) to generate electricity for traction motors. Key parameters include displacement, turbocharging, and fuel injection systems.",
                ["prime mover", "diesel-electric", "engine"],
                1.0
            ),
            SearchDocument(
                2,
                "AC vs DC Traction Systems",
                "Locomotive traction systems use either AC or DC motors. AC traction offers superior adhesion, lower maintenance, and better performance under heavy loads compared to DC traction.",
                ["traction", "ac", "dc", "motors"],
                1.0
            ),
            SearchDocument(
                3,
                "Dynamic Braking Systems",
                "Dynamic braking converts kinetic energy into electrical energy, dissipated as heat. Modern locomotives use blended dynamic and air braking for optimal train control.",
                ["dynamic braking", "kinetic energy", "train control"],
                1.0
            ),
            SearchDocument(
                4,
                "Air Brake Systems: 26-L",
                "The 26-L air brake system is a standard for North American locomotives, featuring automatic and independent brake valves, control reservoirs, and relay valves.",
                ["air brake", "26-L", "reservoir", "valve"],
                1.0
            ),
            SearchDocument(
                5,
                "Air Brake Systems: CCBII",
                "CCBII is a microprocessor-controlled air brake system, offering advanced diagnostics, self-testing, and improved reliability compared to traditional pneumatic systems.",
                ["air brake", "CCBII", "microprocessor", "diagnostics"],
                1.0
            ),
            SearchDocument(
                6,
                "Electronically Controlled Pneumatic (ECP) Brakes",
                "ECP brakes provide faster and more uniform brake application throughout the train, reducing stopping distances and improving safety.",
                ["ECP", "brakes", "safety", "uniform application"],
                1.0
            ),
            SearchDocument(
                7,
                "Distributed Power and LOCOTROL",
                "Distributed power systems, such as LOCOTROL, allow remote control of locomotives throughout the train, improving train handling and reducing in-train forces.",
                ["distributed power", "LOCOTROL", "remote control"],
                1.0
            ),
            SearchDocument(
                8,
                "Locomotive Fuel Systems and Fuel Efficiency",
                "Fuel systems include tanks, pumps, filters, and injectors. Efficiency improvements involve optimizing combustion, reducing idle time, and using advanced control algorithms.",
                ["fuel system", "efficiency", "combustion", "control"],
                1.0
            ),
            SearchDocument(
                9,
                "Locomotive Cooling Systems",
                "Cooling systems regulate engine temperature using radiators, fans, and thermostats. Proper cooling prevents overheating and ensures optimal performance.",
                ["cooling system", "radiator", "fan", "thermostat"],
                1.0
            ),
            SearchDocument(
                10,
                "Turbocharger Systems",
                "Turbochargers increase engine power by forcing more air into the combustion chamber. Maintenance includes inspecting bearings, seals, and compressor wheels.",
                ["turbocharger", "combustion", "maintenance"],
                1.0
            ),
            SearchDocument(
                11,
                "Wheel-Rail Adhesion and Creep Control",
                "Adhesion is critical for traction. Creep control systems optimize wheel slip, using sensors and algorithms to maximize tractive effort without excessive wear.",
                ["adhesion", "creep control", "traction", "sensor"],
                1.0
            ),
            SearchDocument(
                12,
                "FRA Part 229 Locomotive Safety Standards",
                "FRA Part 229 outlines safety standards for locomotive inspection, maintenance, and operation, including requirements for event recorders and brake systems.",
                ["FRA", "safety", "inspection", "maintenance"],
                1.0
            ),
            SearchDocument(
                13,
                "Positive Train Control (PTC)",
                "PTC is an advanced safety system designed to prevent train collisions, derailments, and unauthorized movements using GPS, radio, and onboard computers.",
                ["PTC", "safety", "collision prevention", "GPS"],
                1.0
            ),
            SearchDocument(
                14,
                "Event Recorder Data Analysis",
                "Event recorders log locomotive operational data. Analysis helps identify safety issues, optimize performance, and ensure compliance with regulations.",
                ["event recorder", "data analysis", "safety", "regulation"],
                1.0
            ),
            SearchDocument(
                15,
                "Locomotive Weight and Tractive Effort Calculations",
                "Tractive effort depends on locomotive weight, adhesion, and motor characteristics. Calculations use formulas involving force, mass, and coefficient of friction.",
                ["weight", "tractive effort", "adhesion", "calculation"],
                1.0
            ),
            SearchDocument(
                16,
                "Locomotive Emissions Standards (EPA Tier 0-4)",
                "EPA Tier standards regulate locomotive emissions. Compliance requires advanced exhaust aftertreatment, optimized combustion, and regular testing.",
                ["emissions", "EPA", "Tier", "combustion", "testing"],
                1.0
            ),
            SearchDocument(
                17,
                "Locomotive Maintenance Programs (FRA 229 Compliance)",
                "Maintenance programs ensure FRA 229 compliance, covering inspections, repairs, and record-keeping. Predictive maintenance uses sensors and analytics.",
                ["maintenance", "FRA", "inspection", "predictive"],
                1.0
            ),
            SearchDocument(
                18,
                "Prime Mover Turbocharging Technologies",
                "Turbocharging technologies include variable geometry, intercooling, and electronic control. These improve power output and fuel efficiency.",
                ["prime mover", "turbocharging", "intercooling", "electronic control"],
                1.0
            ),
            SearchDocument(
                19,
                "AC Traction Motor Diagnostics",
                "AC traction motor diagnostics involve monitoring temperature, vibration, and electrical parameters. Early detection prevents failures and reduces downtime.",
                ["AC", "traction motor", "diagnostics", "monitoring"],
                1.0
            ),
            SearchDocument(
                20,
                "DC Traction Motor Maintenance",
                "DC traction motors require regular inspection of brushes, commutators, and bearings. Proper maintenance extends motor life and improves reliability.",
                ["DC", "traction motor", "maintenance", "inspection"],
                1.0
            ),
            SearchDocument(
                21,
                "ECP Brake System Troubleshooting",
                "Troubleshooting ECP brakes involves checking wiring, communication modules, and brake valves. Diagnostic tools help pinpoint faults quickly.",
                ["ECP", "brake", "troubleshooting", "diagnostics"],
                1.0
            ),
            SearchDocument(
                22,
                "LOCOTROL System Upgrades",
                "Upgrades to LOCOTROL systems include software updates, improved radio communication, and enhanced remote control features for distributed power.",
                ["LOCOTROL", "upgrade", "remote control", "distributed power"],
                1.0
            ),
            SearchDocument(
                23,
                "Fuel Efficiency Optimization Algorithms",
                "Optimization algorithms analyze engine load, throttle position, and route profile to minimize fuel consumption and emissions.",
                ["fuel efficiency", "optimization", "algorithm", "emissions"],
                1.0
            ),
            SearchDocument(
                24,
                "Cooling System Failure Modes",
                "Common cooling system failures include radiator leaks, fan malfunctions, and thermostat issues. Early detection prevents engine overheating.",
                ["cooling system", "failure", "radiator", "fan", "thermostat"],
                1.0
            ),
            SearchDocument(
                25,
                "Turbocharger Maintenance Procedures",
                "Maintenance procedures for turbochargers include cleaning compressor wheels, inspecting bearings, and checking for leaks or abnormal noise.",
                ["turbocharger", "maintenance", "procedure", "inspection"],
                1.0
            ),
            SearchDocument(
                26,
                "Wheel-Rail Creep Control Algorithms",
                "Creep control algorithms use real-time sensor data to adjust traction motor output, maximizing adhesion and minimizing wheel slip.",
                ["creep control", "algorithm", "adhesion", "sensor"],
                1.0
            ),
            SearchDocument(
                27,
                "FRA 229 Event Recorder Requirements",
                "FRA 229 mandates event recorders to capture speed, brake application, throttle position, and fault codes for safety and compliance.",
                ["FRA", "event recorder", "requirement", "safety"],
                1.0
            ),
            SearchDocument(
                28,
                "PTC Implementation Challenges",
                "PTC implementation faces challenges such as interoperability, radio spectrum allocation, and integration with legacy systems.",
                ["PTC", "implementation", "challenge", "interoperability"],
                1.0
            ),
            SearchDocument(
                29,
                "Locomotive Weight Distribution",
                "Weight distribution affects adhesion and tractive effort. Proper balancing improves performance and reduces wheel and rail wear.",
                ["weight", "distribution", "adhesion", "tractive effort"],
                1.0
            ),
            SearchDocument(
                30,
                "EPA Tier 4 Aftertreatment Systems",
                "Tier 4 aftertreatment systems include selective catalytic reduction (SCR) and diesel particulate filters (DPF) to reduce NOx and particulate emissions.",
                ["EPA", "Tier 4", "aftertreatment", "SCR", "DPF", "emissions"],
                1.0
            ),
            SearchDocument(
                31,
                "Predictive Maintenance Analytics",
                "Predictive analytics use machine learning to forecast failures, optimize maintenance schedules, and reduce downtime in locomotive fleets.",
                ["predictive maintenance", "analytics", "machine learning", "downtime"],
                1.0
            ),
            SearchDocument(
                32,
                "26-L Brake Valve Operation",
                "The 26-L brake valve controls air flow for automatic and independent braking. Proper operation ensures safe train handling and compliance.",
                ["26-L", "brake valve", "operation", "air flow", "compliance"],
                1.0
            ),
            SearchDocument(
                33,
                "CCBII System Diagnostics",
                "CCBII diagnostics include monitoring pressure sensors, valve actuators, and microprocessor health for reliable air brake performance.",
                ["CCBII", "diagnostics", "pressure sensor", "valve", "microprocessor"],
                1.0
            ),
            SearchDocument(
                34,
                "ECP Brake System Integration",
                "Integration of ECP brakes with train control systems improves response time, uniformity, and safety across long consists.",
                ["ECP", "brake", "integration", "train control", "safety"],
                1.0
            ),
            SearchDocument(
                35,
                "LOCOTROL Remote Diagnostics",
                "Remote diagnostics for LOCOTROL systems enable real-time monitoring, fault detection, and performance optimization for distributed power.",
                ["LOCOTROL", "remote diagnostics", "distributed power", "optimization"],
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