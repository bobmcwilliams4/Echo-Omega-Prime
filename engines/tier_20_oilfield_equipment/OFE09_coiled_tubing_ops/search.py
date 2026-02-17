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
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.N: int = 0
        self.avgdl: float = 0.0
        self.lock = threading.Lock()
        self.inverted_index: Dict[str, set] = defaultdict(set)
        self.k1 = 1.5
        self.b = 0.75

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
                self.inverted_index[term].add(doc.id)
            self.documents[doc.id] = doc
            self.N += 1
            self.avgdl = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, set()))
        scored: List[Tuple[int, float]] = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc = self.documents[doc_id]
            score = bm25_score * 0.7 + tfidf_score * 0.3
            score *= doc.weight
            scored.append((doc_id, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self):
        with self.lock:
            return {
                "documents": self.N,
                "avgdl": self.avgdl,
                "unique_terms": len(self.doc_freqs)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            return 0.0
        return math.log(1 + (self.N - df + 0.5) / (df + 0.5))

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        tf = self.term_freqs[doc_id]
        dl = self.doc_lengths[doc_id]
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
            score += idf * (f * (self.k1 + 1)) / denom
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self.term_freqs[doc_id]
        dl = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            freq = tf.get(term, 0)
            if freq == 0:
                continue
            tf_norm = freq / dl
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:160]
            return snippet + '...' if len(snippet) < len(content) else snippet
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(rf'\b({term})\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + '...'

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
            "CT String Fatigue Life Tracking",
            "Comprehensive tracking of coiled tubing (CT) string fatigue life using cycle counts, bending radii, and tension/compression history. Integrates with Schlumberger CoilLife and NOV fatigue modeling software for real-time monitoring and string management.",
            ["fatigue", "string", "tracking", "coillife", "nov"],
            1.0
        ),
        SearchDocument(
            2,
            "BHA Design for CT Drilling Applications",
            "Best practices for bottom hole assembly (BHA) design in coiled tubing drilling, including motor selection, MWD/LWD integration, vibration mitigation, and tool string optimization for extended reach wells.",
            ["bha", "drilling", "design", "mwd", "lwd"],
            1.0
        ),
        SearchDocument(
            3,
            "Injector Head Operation and Gripper Block Maintenance",
            "Standard operating procedures for CT injector head operation. Includes gripper block inspection, replacement intervals, lubrication, and troubleshooting common injector issues to minimize downtime.",
            ["injector", "gripper", "maintenance", "operation"],
            1.0
        ),
        SearchDocument(
            4,
            "CT BOP Configuration and Stripper/Packer Operation",
            "Guidelines for configuring coiled tubing blowout preventer (BOP) stacks, stripper assembly operation, and packer element maintenance. Covers pressure testing and emergency shut-in protocols.",
            ["bop", "stripper", "packer", "configuration"],
            1.0
        ),
        SearchDocument(
            5,
            "Reel Capacity Calculations and CT String Length Management",
            "Formulas and examples for calculating reel capacity based on CT OD, wall thickness, and drum dimensions. Methods for managing string length, spooling procedures, and tracking footage during operations.",
            ["reel", "capacity", "string", "length", "calculation"],
            1.0
        ),
        SearchDocument(
            6,
            "CT Tubing OD Selection and Grade Specification",
            "Selection criteria for coiled tubing outside diameter (OD) and steel grade. Considers collapse, burst, tensile, and fatigue limits, as well as compatibility with wellbore geometry and operational loads.",
            ["od", "grade", "selection", "specification"],
            1.0
        ),
        SearchDocument(
            7,
            "Nitrogen Pumping Through CT for Underbalanced Operations",
            "Procedures and safety considerations for nitrogen pumping through coiled tubing during underbalanced drilling and cleanout. Includes equipment setup, flow rate calculations, and pressure control.",
            ["nitrogen", "underbalanced", "pumping", "operations"],
            1.0
        ),
        SearchDocument(
            8,
            "CT Fracturing Operations and Proppant Limitations",
            "Operational limits and best practices for coiled tubing fracturing, including proppant type, concentration, and maximum allowable rates to prevent screen-out and tubing erosion.",
            ["fracturing", "proppant", "operations", "limitations"],
            1.0
        ),
        SearchDocument(
            9,
            "Real-Time Depth Tracking and Weight Indicator Monitoring",
            "Techniques for real-time depth tracking using encoders, load cells, and weight indicators. Discusses calibration, error sources, and integration with surface data acquisition systems.",
            ["depth", "tracking", "weight", "monitoring"],
            1.0
        ),
        SearchDocument(
            10,
            "Wellbore Cleanout Operations and Circulation Design",
            "Designing effective circulation programs for wellbore cleanout with coiled tubing. Covers fluid selection, annular velocity, solids transport, and contingency planning for stuck pipe.",
            ["cleanout", "circulation", "design", "wellbore"],
            1.0
        ),
        SearchDocument(
            11,
            "CT Fishing Operations and Stuck Pipe Recovery",
            "Procedures for fishing operations with coiled tubing, including tool selection, jarring techniques, and stuck pipe diagnostics. Emphasizes risk assessment and contingency planning.",
            ["fishing", "stuck", "pipe", "recovery"],
            1.0
        ),
        SearchDocument(
            12,
            "CT Power Pack Hydraulic System and Preventive Maintenance",
            "Maintenance routines for coiled tubing power pack hydraulic systems. Includes fluid checks, filter replacement, leak detection, and scheduled preventive maintenance tasks.",
            ["power", "hydraulic", "maintenance", "system"],
            1.0
        ),
        SearchDocument(
            13,
            "CT Fatigue Modeling Using Schlumberger CoilLife and NOV Software",
            "Comparison of fatigue modeling methodologies in Schlumberger CoilLife and NOV software. Discusses input parameters, model calibration, and interpretation of fatigue life predictions.",
            ["fatigue", "coillife", "nov", "modeling"],
            1.0
        ),
        SearchDocument(
            14,
            "Surface Equipment Layout and Rig-Up Safety",
            "Best practices for surface equipment layout during CT operations. Focuses on rig-up safety, equipment spacing, emergency access, and minimizing trip hazards.",
            ["surface", "layout", "rig-up", "safety"],
            1.0
        ),
        SearchDocument(
            15,
            "CT Cement Squeeze Operations",
            "Procedures for cement squeeze operations using coiled tubing. Includes cement slurry design, placement techniques, and pressure monitoring for effective zonal isolation.",
            ["cement", "squeeze", "operations"],
            1.0
        ),
        SearchDocument(
            16,
            "CT Plug Drill-Out and Composite Frac Plug Milling",
            "Guidelines for milling composite frac plugs and drilling out cement with coiled tubing. Addresses bit selection, weight on bit, and debris management.",
            ["plug", "drill-out", "milling", "frac"],
            1.0
        ),
        SearchDocument(
            17,
            "Flowback Operations Through CT and Production Testing",
            "Managing flowback through coiled tubing during production testing. Covers separator setup, flow measurement, sand management, and pressure control.",
            ["flowback", "production", "testing", "operations"],
            1.0
        ),
        SearchDocument(
            18,
            "CT String Inspection and NDT Techniques",
            "Overview of non-destructive testing (NDT) methods for CT string inspection, including magnetic flux leakage, ultrasonic testing, and wall thickness measurement.",
            ["inspection", "ndt", "string", "testing"],
            1.0
        ),
        SearchDocument(
            19,
            "Injector Chain Tensioning and Wear Monitoring",
            "Procedures for injector chain tension adjustment and wear monitoring. Includes inspection intervals, lubrication, and replacement criteria.",
            ["injector", "chain", "tension", "wear"],
            1.0
        ),
        SearchDocument(
            20,
            "CT Data Acquisition and Logging Systems",
            "Integration of data acquisition and logging systems with CT operations. Discusses sensor selection, data transmission, and real-time monitoring.",
            ["data", "acquisition", "logging", "systems"],
            1.0
        ),
        SearchDocument(
            21,
            "Emergency Shutdown and Well Control Procedures",
            "Step-by-step emergency shutdown and well control procedures for CT operations. Includes BOP activation, kill fluid pumping, and communication protocols.",
            ["emergency", "shutdown", "well", "control"],
            1.0
        ),
        SearchDocument(
            22,
            "CT String Spooling and Handling Safety",
            "Safe practices for CT string spooling, handling, and transportation. Covers personnel safety, equipment checks, and incident prevention.",
            ["spooling", "handling", "safety", "string"],
            1.0
        ),
        SearchDocument(
            23,
            "CT Corrosion Prevention and Inhibitor Selection",
            "Methods for preventing CT string corrosion, including inhibitor selection, chemical injection, and monitoring of corrosion rates.",
            ["corrosion", "prevention", "inhibitor", "selection"],
            1.0
        ),
        SearchDocument(
            24,
            "CT Annular Pressure Control Devices",
            "Function and operation of annular pressure control devices in CT applications. Includes stripper heads, packers, and rotating control devices.",
            ["annular", "pressure", "control", "devices"],
            1.0
        ),
        SearchDocument(
            25,
            "CT Job Planning and Risk Assessment",
            "Comprehensive job planning for CT operations, including risk assessment, contingency planning, and pre-job safety meetings.",
            ["planning", "risk", "assessment", "job"],
            1.0
        ),
        SearchDocument(
            26,
            "CT String Fatigue Tracking with Real-Time Software",
            "Application of real-time software for tracking CT string fatigue during operations. Enables proactive string management and reduces risk of failure.",
            ["fatigue", "tracking", "real-time", "software"],
            1.0
        ),
        SearchDocument(
            27,
            "CT String Make-Up and End Fitting Installation",
            "Procedures for CT string make-up, welding, and end fitting installation. Includes quality control and pressure testing.",
            ["make-up", "end", "fitting", "installation"],
            1.0
        ),
        SearchDocument(
            28,
            "CT Leak Detection and Pressure Testing",
            "Methods for detecting leaks in CT strings and performing pressure tests. Includes hydrostatic and pneumatic testing procedures.",
            ["leak", "detection", "pressure", "testing"],
            1.0
        ),
        SearchDocument(
            29,
            "CT Well Entry and Lubricator Operations",
            "Safe procedures for CT well entry using lubricators. Covers pressure control, tool deployment, and wellhead equipment.",
            ["well", "entry", "lubricator", "operations"],
            1.0
        ),
        SearchDocument(
            30,
            "CT String Life Extension Strategies",
            "Strategies for extending CT string life, including optimized bending radii, fatigue monitoring, and periodic inspection.",
            ["string", "life", "extension", "strategies"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)