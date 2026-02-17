import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# --- Data Classes ---

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

# --- Search Index Implementation ---

class SearchIndex:
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_tokens: Dict[int, List[str]] = {}
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.total_docs: int = 0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self.k1 = 1.5
        self.b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_tokens[doc.id] = tokens
            self.doc_lengths[doc.id] = len(tokens)
            for token in tokens:
                self.inverted_index[token][doc.id] = self.inverted_index[token].get(doc.id, 0) + 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        doc_scores: Dict[int, float] = defaultdict(float)
        doc_tf: Dict[int, Counter] = {}
        for token in query_tokens:
            postings = self.inverted_index.get(token, {})
            idf = self._compute_idf(token)
            for doc_id, freq in postings.items():
                if doc_id not in doc_tf:
                    doc_tf[doc_id] = Counter(self.doc_tokens[doc_id])
                tf = doc_tf[doc_id][token]
                score = self._score_bm25(tf, len(self.doc_tokens[doc_id]), idf)
                doc_scores[doc_id] += score * self.documents[doc_id].weight
        # TF-IDF scoring for tie-breaker and snippet
        tfidf_scores = self._compute_tfidf(query_tokens)
        results = []
        for doc_id, score in doc_scores.items():
            snippet = self._make_snippet(self.documents[doc_id], query_tokens)
            tfidf_score = tfidf_scores.get(doc_id, 0.0)
            combined_score = score + 0.1 * tfidf_score
            results.append(SearchResult(doc_id, combined_score, self.documents[doc_id].title, snippet))
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                'total_docs': self.total_docs,
                'avg_doc_length': self.avg_doc_length,
                'vocab_size': len(self.inverted_index)
            }

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b\w+\b', text.lower())
        return [t for t in tokens if len(t) > 1]

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        N = self.total_docs
        df = len(self.inverted_index.get(term, {}))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, tf: int, doc_len: int, idf: float) -> float:
        denom = tf + self.k1 * (1 - self.b + self.b * (doc_len / (self.avg_doc_length + 1e-9)))
        return idf * ((tf * (self.k1 + 1)) / (denom + 1e-9))

    def _compute_tfidf(self, query_tokens: List[str]) -> Dict[int, float]:
        tfidf_scores: Dict[int, float] = defaultdict(float)
        for token in query_tokens:
            idf = self._compute_idf(token)
            postings = self.inverted_index.get(token, {})
            for doc_id, freq in postings.items():
                tf = freq / len(self.doc_tokens[doc_id])
                tfidf_scores[doc_id] += tf * idf
        return tfidf_scores

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], window: int = 30) -> str:
        content = doc.content
        content_lower = content.lower()
        first_pos = len(content)
        for token in query_tokens:
            idx = content_lower.find(token)
            if idx != -1 and idx < first_pos:
                first_pos = idx
        if first_pos == len(content):
            snippet = content[:window * 2]
        else:
            start = max(0, first_pos - window)
            end = min(len(content), first_pos + window)
            snippet = content[start:end]
        snippet = snippet.replace('\n', ' ')
        for token in query_tokens:
            pattern = re.compile(re.escape(token), re.IGNORECASE)
            snippet = pattern.sub(lambda m: f'**{m.group(0)}**', snippet)
        return snippet.strip()

# --- Singleton Factory ---

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

# --- Domain Documents ---

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Airbus FBW Normal Law Architecture",
            "The Airbus fly-by-wire (FBW) system in Normal Law provides full envelope protection, load factor demand, and automatic flight path stabilization. Normal Law is implemented via three primary flight control computers (PRIMs) and two secondary computers (SECs), ensuring redundancy and fault tolerance.",
            ["Airbus", "FBW", "Normal Law", "Architecture"],
            1.0
        ),
        SearchDocument(
            2,
            "Airbus FBW Alternate Law Degradation",
            "Alternate Law is activated in the Airbus FBW system when certain failures occur, such as multiple sensor discrepancies or PRIM/SEC faults. In Alternate Law, some protections are lost, including high angle-of-attack and load factor limits, but pitch and roll control remain available.",
            ["Airbus", "FBW", "Alternate Law", "Degradation"],
            1.0
        ),
        SearchDocument(
            3,
            "Boeing Control Law Philosophy vs Airbus",
            "Boeing's control law philosophy emphasizes pilot authority and manual override, whereas Airbus prioritizes envelope protection and automation. Boeing FBW systems typically provide tactile feedback and allow override of protections, while Airbus restricts control inputs to remain within safe limits.",
            ["Boeing", "Airbus", "Control Law", "Philosophy"],
            1.0
        ),
        SearchDocument(
            4,
            "C* Control Law Implementation",
            "C* (C-star) control law is a flight control strategy that commands a combination of pitch rate and normal acceleration, resulting in consistent handling qualities across flight regimes. Both Airbus and Boeing have implemented variants of C* in their FBW systems.",
            ["C*", "Control Law", "Implementation", "FBW"],
            1.0
        ),
        SearchDocument(
            5,
            "Hydraulic vs Electro-Hydrostatic Actuator Trade-offs",
            "Traditional hydraulic actuators provide high force and reliability but require centralized hydraulic systems. Electro-hydrostatic actuators (EHAs) are self-contained, offer weight savings, and improve redundancy, but may have different failure modes and maintenance requirements.",
            ["Hydraulic", "EHA", "Actuator", "Trade-off"],
            1.0
        ),
        SearchDocument(
            6,
            "Actuator Jam Detection and Mitigation",
            "Jam detection in flight control actuators uses position sensors and force feedback to identify anomalies. Mitigation strategies include load alleviation, actuator disconnection, and pilot advisories. Redundant actuators and control surface splitting can maintain controllability after a jam.",
            ["Actuator", "Jam", "Detection", "Mitigation"],
            1.0
        ),
        SearchDocument(
            7,
            "Flight Control Computer Redundancy Architecture",
            "Modern flight control systems employ multiple redundant computers, such as PRIMs and SECs in Airbus aircraft, to ensure continued operation after failures. Cross-monitoring and voting logic are used to detect faults and reconfigure control laws as needed.",
            ["Flight Control", "Computer", "Redundancy", "Architecture"],
            1.0
        ),
        SearchDocument(
            8,
            "Autopilot LNAV and VNAV Mode Logic",
            "Lateral Navigation (LNAV) and Vertical Navigation (VNAV) autopilot modes manage aircraft trajectory along predefined routes and altitude profiles. Mode logic includes engagement criteria, mode transitions, and integration with flight management systems.",
            ["Autopilot", "LNAV", "VNAV", "Mode Logic"],
            1.0
        ),
        SearchDocument(
            9,
            "Autoland System Requirements and Categories",
            "Autoland systems must meet stringent reliability and redundancy requirements for Category II/III operations. These include multiple autopilot channels, independent sensor inputs, and fail-operational capability to ensure safe automatic landings in low-visibility conditions.",
            ["Autoland", "System", "Requirements", "Categories"],
            1.0
        ),
        SearchDocument(
            10,
            "Yaw Damper System Design and Failure Effects",
            "Yaw dampers provide automatic rudder inputs to counteract Dutch roll and improve lateral stability. System design includes redundancy and failure detection to prevent inadvertent rudder deflection. Failure effects are mitigated by manual pilot intervention and system isolation.",
            ["Yaw Damper", "System", "Design", "Failure"],
            1.0
        ),
        SearchDocument(
            11,
            "High Angle-of-Attack Protection and Alpha Floor",
            "Airbus FBW systems incorporate high angle-of-attack (alpha) protection and alpha floor functionality. These features prevent stalls by limiting pitch-up commands and automatically applying TOGA thrust if critical angles are approached.",
            ["High AoA", "Alpha Floor", "Protection", "Airbus"],
            1.0
        ),
        SearchDocument(
            12,
            "DO-178C Software Certification for Flight Control Systems",
            "DO-178C is the primary standard for software certification in airborne systems, including flight control computers. It defines development assurance levels, verification activities, and documentation requirements to ensure software reliability and safety.",
            ["DO-178C", "Software", "Certification", "Flight Control"],
            1.0
        ),
        SearchDocument(
            13,
            "Control Surface Flutter Analysis and Prevention",
            "Flutter analysis uses computational models and flight testing to ensure control surfaces remain stable across the flight envelope. Prevention strategies include mass balancing, structural damping, and active control surface monitoring.",
            ["Control Surface", "Flutter", "Analysis", "Prevention"],
            1.0
        ),
        SearchDocument(
            14,
            "FAR Part 25 Flight Control System Certification Requirements",
            "FAR Part 25 specifies certification requirements for transport category aircraft flight control systems, including redundancy, fail-safe design, and demonstration of safe operation under all foreseeable conditions.",
            ["FAR Part 25", "Certification", "Flight Control", "Requirements"],
            1.0
        ),
        SearchDocument(
            15,
            "Runaway Stabilizer Failure Analysis",
            "Runaway stabilizer failures are analyzed through fault tree analysis and simulator testing. Mitigation includes cutout switches, manual trim wheels, and clear pilot procedures to regain control.",
            ["Runaway Stabilizer", "Failure", "Analysis"],
            1.0
        ),
        SearchDocument(
            16,
            "Airbus PRIM and SEC Computer Roles",
            "In Airbus FBW architecture, PRIM computers provide primary flight control law computation, while SECs serve as backups and manage secondary functions. Both types cross-monitor each other for fault detection.",
            ["Airbus", "PRIM", "SEC", "Computer", "Roles"],
            1.0
        ),
        SearchDocument(
            17,
            "Airbus Envelope Protection Logic",
            "Envelope protection in Airbus FBW ensures that pilot inputs cannot exceed safe flight parameters, such as load factor, pitch, and bank angle. Protections are implemented in Normal Law and degrade in Alternate Law.",
            ["Airbus", "Envelope Protection", "Logic"],
            1.0
        ),
        SearchDocument(
            18,
            "Boeing FBW Manual Reversion",
            "Boeing FBW aircraft are designed to allow manual reversion in the event of total computer failure, restoring direct mechanical or hydraulic control to the pilot. This philosophy contrasts with Airbus, which relies on electronic backup laws.",
            ["Boeing", "FBW", "Manual Reversion"],
            1.0
        ),
        SearchDocument(
            19,
            "Load Factor Demand in FBW Systems",
            "Load factor demand control enables pilots to command a specific acceleration rather than a direct control surface deflection. This approach improves handling qualities and reduces pilot workload.",
            ["Load Factor", "Demand", "FBW"],
            1.0
        ),
        SearchDocument(
            20,
            "Flight Control Mode Reconfiguration",
            "Automatic reconfiguration of flight control modes occurs when faults are detected. The system transitions from Normal to Alternate or Direct Law, with associated changes in protections and control response.",
            ["Flight Control", "Mode", "Reconfiguration"],
            1.0
        ),
        SearchDocument(
            21,
            "Electro-Hydrostatic Actuator (EHA) Failure Modes",
            "EHAs can fail due to electrical faults, hydraulic leaks, or software errors. Redundant power supplies and health monitoring are used to detect and isolate failures, maintaining safe operation.",
            ["EHA", "Failure Modes", "Actuator"],
            1.0
        ),
        SearchDocument(
            22,
            "Autopilot Engagement and Disengagement Logic",
            "Autopilot engagement requires specific flight conditions and system health checks. Disengagement can be triggered by pilot input, system faults, or mode transitions. Clear annunciation is provided to the crew.",
            ["Autopilot", "Engagement", "Disengagement", "Logic"],
            1.0
        ),
        SearchDocument(
            23,
            "Yaw Damper Redundancy and Monitoring",
            "Multiple yaw damper channels and continuous monitoring ensure system reliability. Fault detection logic isolates failed channels and alerts the crew, maintaining lateral stability.",
            ["Yaw Damper", "Redundancy", "Monitoring"],
            1.0
        ),
        SearchDocument(
            24,
            "Alpha Floor Activation Scenarios",
            "Alpha floor protection is triggered when the aircraft approaches a critical angle-of-attack, automatically commanding maximum thrust to prevent a stall. Activation scenarios include windshear recovery and aggressive maneuvers.",
            ["Alpha Floor", "Activation", "Scenarios"],
            1.0
        ),
        SearchDocument(
            25,
            "Certification of Autoland Systems",
            "Autoland certification requires demonstration of fail-operational capability, triple redundancy, and compliance with Category III minima. Testing includes simulated failures and low-visibility landings.",
            ["Certification", "Autoland", "Systems"],
            1.0
        ),
        SearchDocument(
            26,
            "Direct Law Characteristics in Airbus FBW",
            "Direct Law is the most basic mode in Airbus FBW, providing a direct relationship between sidestick input and control surface deflection. Protections are lost, and pilot skill becomes critical.",
            ["Direct Law", "Airbus", "FBW"],
            1.0
        ),
        SearchDocument(
            27,
            "Flight Control System Health Monitoring",
            "Continuous health monitoring of flight control computers and actuators detects latent faults and enables timely maintenance. Data is logged for post-flight analysis and trend monitoring.",
            ["Flight Control", "Health Monitoring"],
            1.0
        ),
        SearchDocument(
            28,
            "Load Alleviation Function in FBW",
            "Load alleviation functions automatically adjust control surfaces to reduce structural loads during turbulence or maneuvers, enhancing airframe longevity and passenger comfort.",
            ["Load Alleviation", "FBW", "Function"],
            1.0
        ),
        SearchDocument(
            29,
            "Control Surface Mass Balancing Techniques",
            "Mass balancing of control surfaces prevents flutter by aligning the center of mass with the hinge line. Techniques include counterweights and optimized structural design.",
            ["Control Surface", "Mass Balancing", "Flutter"],
            1.0
        ),
        SearchDocument(
            30,
            "Redundant Sensor Architectures in Flight Control",
            "Redundant sensors, such as multiple air data and inertial reference units, provide fault tolerance and enable cross-checking for accurate flight control system inputs.",
            ["Redundant Sensors", "Flight Control", "Architecture"],
            1.0
        ),
        SearchDocument(
            31,
            "FBW System Mode Annunciation",
            "Clear annunciation of flight control law modes (Normal, Alternate, Direct) is provided to the crew on Airbus aircraft, ensuring situational awareness during system reconfiguration.",
            ["FBW", "Mode", "Annunciation"],
            1.0
        ),
        SearchDocument(
            32,
            "Manual Trim and Stabilizer Cutout Procedures",
            "Manual trim wheels and stabilizer cutout switches are critical for recovering from runaway trim or autopilot malfunctions. Procedures are trained and documented for all flight crews.",
            ["Manual Trim", "Stabilizer", "Cutout", "Procedures"],
            1.0
        ),
        SearchDocument(
            33,
            "Flight Envelope Computation in FBW",
            "Flight envelope computation uses sensor data and aerodynamic models to define safe operating limits. FBW computers continuously monitor and enforce these boundaries.",
            ["Flight Envelope", "Computation", "FBW"],
            1.0
        ),
        SearchDocument(
            34,
            "Pilot Override in FBW Systems",
            "Some FBW systems, such as Boeing's, allow pilot override of envelope protections, while Airbus restricts control authority to maintain safety. This reflects differing design philosophies.",
            ["Pilot Override", "FBW", "Systems"],
            1.0
        ),
        SearchDocument(
            35,
            "Control Law Mode Transition Logic",
            "Transition logic between control law modes is based on system health, sensor validity, and flight phase. Automated transitions ensure continued safe operation after failures.",
            ["Control Law", "Mode Transition", "Logic"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)