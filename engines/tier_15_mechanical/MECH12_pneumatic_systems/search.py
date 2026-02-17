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
        self.idf_cache: Dict[str, float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.term_freqs[doc.id] = Counter(tokens)
            for term in set(tokens):
                self.term_doc_freq[term] += 1
            self.total_docs = len(self.documents)
            self.avg_doc_length = (
                sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            )
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scores: Dict[int, float] = defaultdict(float)
        snippets: Dict[int, str] = {}
        for doc_id, doc in self.documents.items():
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            final_score = bm25_score * 0.7 + tfidf_score * 0.3
            if final_score > 0:
                scores[doc_id] = final_score * doc.weight
                snippets[doc_id] = self._make_snippet(doc.content, query_terms)
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = [
            SearchResult(doc_id=doc_id, score=score, title=self.documents[doc_id].title, snippet=snippets[doc_id])
            for doc_id, score in ranked
        ]
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            "total_docs": self.total_docs,
            "avg_doc_length": self.avg_doc_length,
            "unique_terms": len(self.term_doc_freq),
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
        doc_len = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        tf = self.term_freqs.get(doc_id, Counter())
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
        score = 0.0
        tf = self.term_freqs.get(doc_id, Counter())
        doc_len = self.doc_lengths.get(doc_id, 1)
        for term in query_terms:
            term_freq = tf.get(term, 0) / doc_len
            idf = self._compute_idf(term)
            score += term_freq * idf
        return score

    def _make_snippet(self, content: str, query_terms: List[str], length: int = 160) -> str:
        content_lower = content.lower()
        for term in query_terms:
            idx = content_lower.find(term)
            if idx != -1:
                start = max(0, idx - 40)
                end = min(len(content), idx + length)
                snippet = content[start:end]
                return self._highlight(snippet, query_terms)
        snippet = content[:length]
        return self._highlight(snippet, query_terms)

    def _highlight(self, text: str, terms: List[str]) -> str:
        for term in set(terms):
            text = re.sub(r'(?i)\b({})\b'.format(re.escape(term)), r'**\1**', text)
        return text

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
            "Reciprocating Compressor Selection and Sizing",
            "Reciprocating compressors are chosen based on required flow rate, pressure, and application. Sizing involves calculating the demand, considering duty cycle, and selecting a compressor with adequate capacity and safety margin.",
            ["compressor", "reciprocating", "selection", "sizing"],
            1.0
        ),
        SearchDocument(
            2,
            "Rotary Screw Compressor Design and Application",
            "Rotary screw compressors provide continuous air flow and are ideal for industrial applications with high demand. Design factors include rotor profile, lubrication, cooling, and control systems.",
            ["compressor", "rotary screw", "design", "application"],
            1.0
        ),
        SearchDocument(
            3,
            "Air Receiver Tank Sizing and Pressure Stabilization",
            "Proper sizing of air receiver tanks ensures pressure stabilization and reduces compressor cycling. The volume is calculated based on system demand and allowable pressure drop.",
            ["air receiver", "tank", "sizing", "pressure stabilization"],
            1.0
        ),
        SearchDocument(
            4,
            "Compressed Air Dryer Selection - Refrigerated vs Desiccant",
            "Refrigerated dryers are suitable for general applications, while desiccant dryers are used for critical processes requiring low dew point. Selection depends on air quality requirements and operating conditions.",
            ["air dryer", "refrigerated", "desiccant", "selection"],
            1.0
        ),
        SearchDocument(
            5,
            "Pneumatic Cylinder Force and Sizing Calculations",
            "Cylinder force is calculated using bore diameter and supply pressure. Sizing considers load, speed, and stroke length to ensure reliable operation.",
            ["pneumatic cylinder", "force", "sizing", "calculation"],
            1.0
        ),
        SearchDocument(
            6,
            "Directional Control Valve Selection - 3/2, 5/2, 5/3 Configurations",
            "Directional control valves manage air flow to actuators. 3/2 valves are used for single-acting cylinders, 5/2 and 5/3 for double-acting cylinders. Selection is based on circuit requirements.",
            ["directional control valve", "3/2", "5/2", "5/3", "selection"],
            1.0
        ),
        SearchDocument(
            7,
            "Pneumatic Flow Control - Meter-In vs Meter-Out",
            "Meter-in controls air entering the actuator, while meter-out controls exhaust. Choice affects speed and stability of pneumatic motion.",
            ["flow control", "meter-in", "meter-out", "pneumatic"],
            1.0
        ),
        SearchDocument(
            8,
            "Vacuum Generation - Ejector vs Mechanical Pump Selection",
            "Ejectors use compressed air to generate vacuum, suitable for rapid cycling and lightweight applications. Mechanical pumps provide higher vacuum levels and are used for demanding tasks.",
            ["vacuum generation", "ejector", "mechanical pump", "selection"],
            1.0
        ),
        SearchDocument(
            9,
            "Compressed Air Quality per ISO 8573-1 Classification",
            "ISO 8573-1 defines air quality classes for particles, water, and oil. Proper filtration and drying ensure compliance with required class for sensitive equipment.",
            ["compressed air", "quality", "ISO 8573-1", "classification"],
            1.0
        ),
        SearchDocument(
            10,
            "Compressed Air Energy Audit and Specific Power Analysis",
            "Energy audits identify inefficiencies in compressed air systems. Specific power is calculated as kW per 100 cfm, helping optimize compressor selection and operation.",
            ["energy audit", "compressed air", "specific power", "analysis"],
            1.0
        ),
        SearchDocument(
            11,
            "Compressed Air Leak Detection and Management Program",
            "Leaks waste energy and increase costs. Detection methods include ultrasonic sensors and soapy water. Management involves regular inspections and prompt repairs.",
            ["leak detection", "compressed air", "management"],
            1.0
        ),
        SearchDocument(
            12,
            "Pneumatic Logic Circuits and Sequential Control",
            "Logic circuits use valves and actuators to achieve automated sequences. Common elements include AND, OR, NOT functions implemented with pneumatic components.",
            ["logic circuit", "sequential control", "pneumatic"],
            1.0
        ),
        SearchDocument(
            13,
            "Vacuum Cup Gripper Design and Suction Force Calculation",
            "Design of vacuum cup grippers considers material, shape, and suction force. Calculation involves pressure differential and cup area to ensure secure handling.",
            ["vacuum cup", "gripper", "design", "suction force"],
            1.0
        ),
        SearchDocument(
            14,
            "Pneumatic Pipe Sizing and Pressure Drop Calculation",
            "Pipe sizing is based on flow rate, length, and allowable pressure drop. Calculation ensures efficient air delivery and minimizes energy losses.",
            ["pipe sizing", "pressure drop", "pneumatic"],
            1.0
        ),
        SearchDocument(
            15,
            "OSHA Compressed Air Safety - 29 CFR 1910.242 and 1910.169",
            "OSHA regulations mandate safe use of compressed air. 29 CFR 1910.242 covers hand tools, while 1910.169 addresses pressure vessels and receiver tanks.",
            ["OSHA", "compressed air", "safety", "regulations"],
            1.0
        ),
        SearchDocument(
            16,
            "ISO 4414 Pneumatic System Design Rules and Safety",
            "ISO 4414 provides guidelines for pneumatic system design, including safety, reliability, and maintenance. Compliance ensures safe and efficient operation.",
            ["ISO 4414", "pneumatic", "system", "design", "safety"],
            1.0
        ),
        SearchDocument(
            17,
            "Heat Recovery from Compressed Air Systems",
            "Heat generated during compression can be recovered for heating or process use. Recovery methods include heat exchangers and integration with facility systems.",
            ["heat recovery", "compressed air", "energy"],
            1.0
        ),
        SearchDocument(
            18,
            "Variable Speed Drive (VSD) Compressor Energy Savings",
            "VSD compressors adjust speed to match demand, reducing energy consumption. Savings depend on load profile and proper control integration.",
            ["variable speed drive", "VSD", "compressor", "energy savings"],
            1.0
        ),
        SearchDocument(
            19,
            "Altitude Derating of Compressors and Pneumatic Equipment",
            "At high altitudes, air density decreases, requiring derating of compressors and pneumatic equipment. Calculations adjust capacity and pressure settings.",
            ["altitude", "derating", "compressor", "pneumatic equipment"],
            1.0
        ),
        SearchDocument(
            20,
            "Filter-Regulator-Lubricator (FRL) Unit Selection and Maintenance",
            "FRL units condition compressed air for pneumatic systems. Selection considers flow rate, filtration level, and maintenance requirements.",
            ["FRL", "filter", "regulator", "lubricator", "selection", "maintenance"],
            1.0
        ),
        SearchDocument(
            21,
            "Compressor Duty Cycle and Load Management",
            "Duty cycle determines compressor run time and affects sizing. Load management strategies optimize system efficiency and prolong equipment life.",
            ["compressor", "duty cycle", "load management"],
            1.0
        ),
        SearchDocument(
            22,
            "Compressed Air System Controls and Automation",
            "Modern compressed air systems use PLCs and sensors for automated control. Integration improves reliability, energy efficiency, and maintenance scheduling.",
            ["compressed air", "system", "controls", "automation"],
            1.0
        ),
        SearchDocument(
            23,
            "Air Quality Monitoring and Sensor Integration",
            "Continuous monitoring of air quality ensures compliance and protects equipment. Sensors detect particles, moisture, and oil, triggering alarms and maintenance.",
            ["air quality", "monitoring", "sensor", "integration"],
            1.0
        ),
        SearchDocument(
            24,
            "Pneumatic Actuator Selection and Application",
            "Actuator selection depends on force, speed, and stroke requirements. Applications range from simple linear motion to complex robotic systems.",
            ["pneumatic actuator", "selection", "application"],
            1.0
        ),
        SearchDocument(
            25,
            "Compressed Air Distribution Network Design",
            "Design of air distribution networks considers pipe layout, pressure drop, and redundancy. Proper design ensures reliable supply and minimizes losses.",
            ["compressed air", "distribution", "network", "design"],
            1.0
        ),
        SearchDocument(
            26,
            "Energy Efficiency Measures for Pneumatic Systems",
            "Measures include leak reduction, optimized compressor control, and heat recovery. Regular audits and upgrades improve overall efficiency.",
            ["energy efficiency", "pneumatic system", "measures"],
            1.0
        ),
        SearchDocument(
            27,
            "Pneumatic Safety Interlocks and Emergency Shutdown",
            "Safety interlocks prevent hazardous operation. Emergency shutdown systems protect personnel and equipment during faults or abnormal conditions.",
            ["pneumatic", "safety", "interlock", "emergency shutdown"],
            1.0
        ),
        SearchDocument(
            28,
            "Compressed Air System Maintenance Best Practices",
            "Maintenance includes filter replacement, leak repair, and monitoring of compressor performance. Best practices extend equipment life and reduce downtime.",
            ["compressed air", "system", "maintenance", "best practices"],
            1.0
        ),
        SearchDocument(
            29,
            "Pneumatic Tubing Material Selection",
            "Tubing material affects durability and compatibility. Common materials include polyurethane, nylon, and stainless steel, selected based on pressure and environment.",
            ["pneumatic tubing", "material", "selection"],
            1.0
        ),
        SearchDocument(
            30,
            "Compressed Air System Troubleshooting Guide",
            "Troubleshooting involves diagnosing pressure drops, leaks, and equipment failures. Systematic approach ensures rapid resolution and minimizes downtime.",
            ["compressed air", "system", "troubleshooting", "guide"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)