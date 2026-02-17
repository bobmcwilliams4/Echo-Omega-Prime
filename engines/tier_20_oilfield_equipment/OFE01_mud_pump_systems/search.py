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
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.doc_lengths: Dict[int, int] = defaultdict(int)
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.lock = threading.Lock()
        self.k1 = 1.5
        self.b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            for term in tf:
                self.doc_freqs[term] += 1
            self.doc_lengths[doc.id] = len(tokens)
            self.documents[doc.id] = doc
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / max(1, self.N)

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            for doc_id in self.term_freqs:
                if term in self.term_freqs[doc_id]:
                    candidate_docs.add(doc_id)
        scored_results = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc = self.documents[doc_id]
            final_score = bm25_score * 0.7 + tfidf_score * 0.3
            snippet = self._make_snippet(doc.content, query_terms)
            scored_results.append(SearchResult(doc_id, final_score * doc.weight, doc.title, snippet))
        scored_results.sort(key=lambda x: x.score, reverse=True)
        return scored_results[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                'num_documents': self.N,
                'avg_doc_length': self.avg_doc_length,
                'vocabulary_size': len(self.doc_freqs)
            }

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

    def _compute_idf(self, term: str) -> float:
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            return 0.0
        return math.log(1 + (self.N - df + 0.5) / (df + 0.5))

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length or 1.0
        tf = self.term_freqs[doc_id]
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self.k1 * (1 - self.b + self.b * doc_len / avg_dl)
            numer = f * (self.k1 + 1)
            score += idf * numer / denom
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths.get(doc_id, 1)
        score = 0.0
        for term in query_terms:
            freq = tf.get(term, 0)
            if freq == 0:
                continue
            tf_norm = freq / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = ' '.join(tokens[:window])
            return snippet + ('...' if len(tokens) > window else '')
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(rf'\b({re.escape(term)})\b', r'**\1**', snippet, flags=re.IGNORECASE)
        if end < len(tokens):
            snippet += '...'
        return snippet

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
            "Triplex vs Duplex Pump Selection",
            "Triplex pumps offer higher efficiency and smoother flow compared to duplex pumps. Duplex pumps are simpler but less efficient. Selection depends on required flow rate, pressure, and maintenance considerations.",
            ["triplex", "duplex", "selection", "efficiency"],
            1.0
        ),
        SearchDocument(
            2,
            "Liner Sizing for Mud Pumps",
            "Proper liner sizing is critical for achieving desired flow rates and pressures. Oversized liners reduce pressure, while undersized liners increase wear and risk of failure.",
            ["liner", "sizing", "mud pump"],
            1.0
        ),
        SearchDocument(
            3,
            "Material Selection for Pump Liners",
            "Pump liner material should be chosen based on fluid properties, expected wear, and corrosion resistance. Common materials include hardened steel and ceramic.",
            ["liner", "material", "corrosion", "wear"],
            1.0
        ),
        SearchDocument(
            4,
            "Valve Maintenance Best Practices",
            "Routine inspection and timely replacement of valves prevent downtime. Lubrication and cleaning are essential to avoid sticking and erosion.",
            ["valve", "maintenance", "inspection"],
            1.0
        ),
        SearchDocument(
            5,
            "Valve Failure Analysis in Mud Pumps",
            "Valve failures often result from improper seating, material fatigue, or debris ingress. Root cause analysis should include inspection of valve seats and springs.",
            ["valve", "failure", "analysis"],
            1.0
        ),
        SearchDocument(
            6,
            "Pulsation Dampener Sizing and Function",
            "Correct sizing of pulsation dampeners reduces pressure fluctuations and extends component life. Calculation should consider pump output and system compliance.",
            ["pulsation", "dampener", "sizing"],
            1.0
        ),
        SearchDocument(
            7,
            "Fluid End Failure Modes",
            "Common fluid end failures include washout, cracking, and corrosion. Monitoring pressure and regular inspection help prevent catastrophic failures.",
            ["fluid end", "failure", "washout"],
            1.0
        ),
        SearchDocument(
            8,
            "Root Causes of Fluid End Failures",
            "Root causes often involve improper material selection, excessive pressure, or inadequate maintenance. Metallurgical analysis can identify contributing factors.",
            ["fluid end", "root cause", "analysis"],
            1.0
        ),
        SearchDocument(
            9,
            "Power End Diagnostics: Bearing Failures",
            "Bearing failures in the power end are commonly due to misalignment, inadequate lubrication, or contamination. Vibration analysis aids in early detection.",
            ["power end", "bearing", "diagnostics"],
            1.0
        ),
        SearchDocument(
            10,
            "Gear Failures in Mud Pump Power Ends",
            "Gear failures may result from overload, poor lubrication, or manufacturing defects. Regular oil analysis and gear inspection are recommended.",
            ["power end", "gear", "failure"],
            1.0
        ),
        SearchDocument(
            11,
            "Stroke Rate Optimization",
            "Optimizing stroke rate improves pump efficiency and reduces wear. Consider mud properties and desired flow rate when selecting stroke settings.",
            ["stroke rate", "optimization", "efficiency"],
            1.0
        ),
        SearchDocument(
            12,
            "Hydraulic Horsepower Calculation",
            "Hydraulic horsepower is calculated as (Flow Rate x Pressure) / 1714. Accurate calculation ensures proper pump sizing and energy efficiency.",
            ["hydraulic horsepower", "calculation", "pump sizing"],
            1.0
        ),
        SearchDocument(
            13,
            "Pressure Relief System Design",
            "Pressure relief systems protect pumps and personnel from overpressure events. Design should comply with API standards and include regular testing.",
            ["pressure relief", "system", "design"],
            1.0
        ),
        SearchDocument(
            14,
            "Mud Weight Impact on Pump Performance",
            "Increased mud weight raises discharge pressure and can reduce pump efficiency. Adjust liner size and stroke rate to compensate for heavier mud.",
            ["mud weight", "performance", "efficiency"],
            1.0
        ),
        SearchDocument(
            15,
            "Pump Efficiency Curves Explained",
            "Efficiency curves show pump performance at varying pressures and flow rates. Use these curves to select optimal operating points.",
            ["efficiency", "curves", "performance"],
            1.0
        ),
        SearchDocument(
            16,
            "Performance Mapping of Mud Pumps",
            "Performance mapping involves plotting flow, pressure, and efficiency to identify best operating conditions and diagnose issues.",
            ["performance", "mapping", "diagnostics"],
            1.0
        ),
        SearchDocument(
            17,
            "Gardner Denver vs National Oilwell",
            "Gardner Denver pumps are known for durability, while National Oilwell offers modular designs. Selection depends on application and service availability.",
            ["gardner denver", "national oilwell", "comparison"],
            1.0
        ),
        SearchDocument(
            18,
            "SPM Mud Pumps: OEM Comparison",
            "SPM pumps provide high-pressure capabilities and robust construction. Compare with other OEMs based on maintenance and parts availability.",
            ["spm", "oem", "comparison"],
            1.0
        ),
        SearchDocument(
            19,
            "Liner Wash Detection Techniques",
            "Early detection of liner wash prevents catastrophic failure. Use pressure monitoring and visual inspection for early warning.",
            ["liner wash", "detection", "inspection"],
            1.0
        ),
        SearchDocument(
            20,
            "Preventing Liner Wash in Mud Pumps",
            "Prevent liner wash by using proper materials, maintaining correct pressure, and regular inspection. Replace liners at recommended intervals.",
            ["liner wash", "prevention", "maintenance"],
            1.0
        ),
        SearchDocument(
            21,
            "Triplex Pump Flow Characteristics",
            "Triplex pumps deliver smoother flow and higher efficiency than duplex pumps. Their three-piston design reduces pulsation.",
            ["triplex", "flow", "characteristics"],
            1.0
        ),
        SearchDocument(
            22,
            "Duplex Pump Maintenance",
            "Duplex pumps are easier to maintain but less efficient. Regular valve and liner checks are necessary to avoid unplanned downtime.",
            ["duplex", "maintenance", "valve"],
            1.0
        ),
        SearchDocument(
            23,
            "API Standards for Mud Pump Systems",
            "API standards govern the design, operation, and maintenance of mud pump systems. Compliance ensures safety and reliability.",
            ["api", "standards", "mud pump"],
            1.0
        ),
        SearchDocument(
            24,
            "Corrosion Resistance in Liner Materials",
            "Ceramic liners offer superior corrosion resistance compared to steel. Material selection should consider mud chemistry and expected lifespan.",
            ["corrosion", "liner", "material"],
            1.0
        ),
        SearchDocument(
            25,
            "Mud Pump System Troubleshooting",
            "Troubleshooting involves checking pressure, flow, and component wear. Systematic diagnosis reduces downtime and repair costs.",
            ["troubleshooting", "mud pump", "diagnosis"],
            1.0
        ),
        SearchDocument(
            26,
            "Pulsation Dampener Maintenance",
            "Regular maintenance of pulsation dampeners includes checking pre-charge pressure and inspecting for leaks or bladder failure.",
            ["pulsation", "dampener", "maintenance"],
            1.0
        ),
        SearchDocument(
            27,
            "Valve Seat Material Selection",
            "Valve seat materials must withstand high pressure and abrasive fluids. Tungsten carbide and hardened steel are common choices.",
            ["valve", "seat", "material"],
            1.0
        ),
        SearchDocument(
            28,
            "Hydraulic Horsepower vs Brake Horsepower",
            "Hydraulic horsepower measures fluid power output, while brake horsepower is mechanical input. Efficiency losses occur between the two.",
            ["hydraulic horsepower", "brake horsepower", "efficiency"],
            1.0
        ),
        SearchDocument(
            29,
            "Optimizing Pump Performance with Variable Speed Drives",
            "Variable speed drives allow for precise control of pump output, improving efficiency and reducing wear on components.",
            ["variable speed", "pump", "performance"],
            1.0
        ),
        SearchDocument(
            30,
            "OEM Parts Availability and Lead Times",
            "OEM parts availability can affect maintenance schedules. Gardner Denver, National Oilwell, and SPM offer varying lead times for critical components.",
            ["oem", "parts", "lead time"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)