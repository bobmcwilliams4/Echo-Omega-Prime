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
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.total_docs: int = 0
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[Tuple[int, str], float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def _tokenize(self, text: str) -> List[str]:
        return [token.lower() for token in re.findall(r"\b\w+\b", text)]

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            term_counts = Counter(tokens)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            for term, count in term_counts.items():
                self.inverted_index[term][doc.id] = count
                self.doc_freqs[term] += 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        term_counts = self.inverted_index
        for term in set(query_terms):
            if doc_id not in term_counts.get(term, {}):
                continue
            f = term_counts[term][doc_id]
            idf = self._compute_idf(term)
            denom = f + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / self.avg_doc_length)
            numer = f * (self._bm25_k1 + 1)
            score += idf * numer / denom
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        tfidf = 0.0
        for term in set(query_terms):
            tf = self.inverted_index.get(term, {}).get(doc_id, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            norm_tf = tf / doc_len
            tfidf += norm_tf * idf
        return tfidf * doc.weight

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, {}).keys())
        scored_docs = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(query_terms, doc_id)
            tfidf_score = self._score_tfidf(query_terms, doc_id)
            score = bm25_score + 0.5 * tfidf_score
            if score > 0:
                snippet = self._make_snippet(self.documents[doc_id], query_terms)
                scored_docs.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scored_docs.sort(key=lambda x: x.score, reverse=True)
        return scored_docs[:limit]

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], maxlen: int = 200) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:maxlen]
        else:
            start = max(positions[0] - 10, 0)
            end = min(positions[0] + 20, len(tokens))
            snippet_tokens = tokens[start:end]
            snippet = " ".join(snippet_tokens)
            for term in set(query_terms):
                snippet = re.sub(rf"\b({re.escape(term)})\b", r"**\1**", snippet, flags=re.IGNORECASE)
        if len(snippet) > maxlen:
            snippet = snippet[:maxlen] + "..."
        return snippet

    def get_stats(self) -> Dict[str, float]:
        return {
            "total_docs": self.total_docs,
            "avg_doc_length": self.avg_doc_length,
            "unique_terms": len(self.inverted_index),
        }

# Singleton factory
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    if _search_index_instance is None:
        with _search_index_lock:
            if _search_index_instance is None:
                _search_index_instance = SearchIndex()
                _preseed_documents(_search_index_instance)
    return _search_index_instance

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Optimizing RTU Polling Intervals in Oilfield SCADA",
            "Learn how to optimize RTU polling intervals to balance data freshness and bandwidth usage. Discusses best practices for setting polling rates in Modbus and DNP3 environments.",
            ["RTU", "Polling", "Optimization", "SCADA"],
            1.0
        ),
        SearchDocument(
            2,
            "Modbus Register Mapping: Best Practices",
            "A comprehensive guide to mapping Modbus registers for oilfield automation. Covers contiguous mapping, function code selection, and addressing strategies to maximize efficiency.",
            ["Modbus", "Register Mapping", "Best Practices"],
            1.0
        ),
        SearchDocument(
            3,
            "DNP3 Configuration for Oilfield SCADA Systems",
            "Step-by-step instructions for configuring DNP3 protocol in oilfield SCADA. Includes security, event classes, and unsolicited messaging setup.",
            ["DNP3", "SCADA", "Configuration"],
            1.0
        ),
        SearchDocument(
            4,
            "ROC800 Flow Computer Setup for Custody Transfer",
            "Detailed procedures for configuring ROC800 flow computers for custody transfer applications. Focuses on API compliance, audit trails, and calibration.",
            ["ROC800", "Flow Computer", "Custody Transfer"],
            1.0
        ),
        SearchDocument(
            5,
            "Flow Computer vs PLC for Custody Transfer",
            "Comparison of flow computers and PLCs for custody transfer. Evaluates accuracy, compliance, and integration with SCADA systems.",
            ["Flow Computer", "PLC", "Custody Transfer"],
            1.0
        ),
        SearchDocument(
            6,
            "Radio Telemetry Frequency Selection in Oilfield SCADA",
            "Guidelines for selecting radio telemetry frequencies for oilfield SCADA, including FCC regulations, interference mitigation, and propagation considerations.",
            ["Radio Telemetry", "Frequency Selection", "SCADA"],
            1.0
        ),
        SearchDocument(
            7,
            "Cellular SCADA vs Radio Telemetry: Pros and Cons",
            "Analyzes the advantages and disadvantages of cellular SCADA versus radio telemetry. Discusses cost, reliability, coverage, and security.",
            ["Cellular SCADA", "Radio Telemetry", "Comparison"],
            1.0
        ),
        SearchDocument(
            8,
            "Selecting Tank Level Measurement Technologies",
            "Overview of tank level measurement technologies including radar, ultrasonic, and hydrostatic sensors. Provides selection criteria for oilfield applications.",
            ["Tank Level", "Measurement", "Technology Selection"],
            1.0
        ),
        SearchDocument(
            9,
            "OT Network Segmentation for SCADA Cybersecurity",
            "Best practices for segmenting OT networks to enhance SCADA cybersecurity. Covers VLANs, firewalls, and DMZ architectures.",
            ["OT Network", "Segmentation", "Cybersecurity", "SCADA"],
            1.0
        ),
        SearchDocument(
            10,
            "SCADA Alarm Management: Applying ISA-18.2 Principles",
            "How to implement alarm management in SCADA systems using ISA-18.2. Includes alarm rationalization, prioritization, and performance monitoring.",
            ["SCADA", "Alarm Management", "ISA-18.2"],
            1.0
        ),
        SearchDocument(
            11,
            "Reducing Bandwidth Usage in RTU Polling",
            "Techniques for minimizing bandwidth during RTU polling, such as event-based polling and data compression.",
            ["RTU", "Bandwidth", "Polling"],
            1.0
        ),
        SearchDocument(
            12,
            "Modbus Function Codes Explained",
            "Explains the various Modbus function codes and their use cases in oilfield automation.",
            ["Modbus", "Function Codes", "Automation"],
            1.0
        ),
        SearchDocument(
            13,
            "DNP3 Secure Authentication",
            "Introduction to DNP3 Secure Authentication for critical infrastructure. Discusses configuration and key management.",
            ["DNP3", "Security", "Authentication"],
            1.0
        ),
        SearchDocument(
            14,
            "ROC800 Audit Trail Configuration",
            "How to configure audit trails on ROC800 flow computers for regulatory compliance.",
            ["ROC800", "Audit Trail", "Compliance"],
            1.0
        ),
        SearchDocument(
            15,
            "Integrating Flow Computers with SCADA",
            "Methods for integrating flow computers with SCADA systems, including protocol selection and data mapping.",
            ["Flow Computer", "SCADA", "Integration"],
            1.0
        ),
        SearchDocument(
            16,
            "PLC Programming for Custody Transfer",
            "Key considerations when programming PLCs for custody transfer, including pulse counting and timestamping.",
            ["PLC", "Custody Transfer", "Programming"],
            1.0
        ),
        SearchDocument(
            17,
            "Radio Path Surveys for Oilfield SCADA",
            "How to conduct radio path surveys to ensure reliable SCADA communications in oilfields.",
            ["Radio", "Path Survey", "SCADA"],
            1.0
        ),
        SearchDocument(
            18,
            "Cellular Network Redundancy in SCADA",
            "Strategies for implementing redundancy in cellular SCADA networks to maximize uptime.",
            ["Cellular", "SCADA", "Redundancy"],
            1.0
        ),
        SearchDocument(
            19,
            "Radar vs Ultrasonic Tank Level Sensors",
            "Comparison of radar and ultrasonic sensors for tank level measurement in oilfield environments.",
            ["Radar", "Ultrasonic", "Tank Level"],
            1.0
        ),
        SearchDocument(
            20,
            "Implementing VLANs for OT Network Segmentation",
            "Step-by-step guide to implementing VLANs for segmenting OT networks in SCADA environments.",
            ["VLAN", "OT Network", "Segmentation"],
            1.0
        ),
        SearchDocument(
            21,
            "Alarm Flood Prevention in SCADA",
            "Techniques for preventing alarm floods in SCADA systems, including alarm shelving and suppression.",
            ["SCADA", "Alarm Management", "Flood Prevention"],
            1.0
        ),
        SearchDocument(
            22,
            "Optimizing Modbus Register Utilization",
            "Tips for optimizing register utilization in Modbus devices, including grouping and addressing.",
            ["Modbus", "Register", "Optimization"],
            1.0
        ),
        SearchDocument(
            23,
            "DNP3 Event Buffer Configuration",
            "How to configure event buffers in DNP3 outstations for efficient data reporting.",
            ["DNP3", "Event Buffer", "Configuration"],
            1.0
        ),
        SearchDocument(
            24,
            "ROC800 Flow Computer Calibration",
            "Procedures for calibrating ROC800 flow computers to ensure custody transfer accuracy.",
            ["ROC800", "Calibration", "Custody Transfer"],
            1.0
        ),
        SearchDocument(
            25,
            "PLC vs Flow Computer: Compliance Considerations",
            "Regulatory compliance considerations when choosing between PLCs and flow computers for custody transfer.",
            ["PLC", "Flow Computer", "Compliance"],
            1.0
        ),
        SearchDocument(
            26,
            "Radio Telemetry Interference Mitigation",
            "Best practices for mitigating interference in radio telemetry systems for SCADA.",
            ["Radio Telemetry", "Interference", "Mitigation"],
            1.0
        ),
        SearchDocument(
            27,
            "Cellular SCADA Security Best Practices",
            "Security best practices for cellular SCADA deployments, including encryption and APN management.",
            ["Cellular SCADA", "Security", "Best Practices"],
            1.0
        ),
        SearchDocument(
            28,
            "Hydrostatic Tank Level Measurement",
            "Principles and installation tips for hydrostatic tank level measurement in oilfields.",
            ["Hydrostatic", "Tank Level", "Measurement"],
            1.0
        ),
        SearchDocument(
            29,
            "Firewalls in OT Network Segmentation",
            "Role of firewalls in segmenting OT networks and protecting SCADA assets.",
            ["Firewalls", "OT Network", "Segmentation"],
            1.0
        ),
        SearchDocument(
            30,
            "Alarm Rationalization Workshop Guide",
            "A practical guide to running alarm rationalization workshops in compliance with ISA-18.2.",
            ["Alarm Management", "ISA-18.2", "Rationalization"],
            1.0
        ),
        SearchDocument(
            31,
            "Event-Based Polling in RTUs",
            "Advantages and implementation of event-based polling in RTUs to reduce network load.",
            ["RTU", "Event-Based Polling", "Optimization"],
            1.0
        ),
        SearchDocument(
            32,
            "Modbus Addressing Strategies",
            "Effective addressing strategies for Modbus networks in oilfield SCADA.",
            ["Modbus", "Addressing", "SCADA"],
            1.0
        ),
        SearchDocument(
            33,
            "DNP3 Unsolicited Messaging",
            "Configuring DNP3 unsolicited messaging for timely event reporting in SCADA.",
            ["DNP3", "Unsolicited Messaging", "SCADA"],
            1.0
        ),
        SearchDocument(
            34,
            "ROC800 API Compliance Features",
            "Overview of API compliance features in ROC800 flow computers for custody transfer.",
            ["ROC800", "API Compliance", "Custody Transfer"],
            1.0
        ),
        SearchDocument(
            35,
            "PLC Timestamping for Custody Transfer",
            "Implementing accurate timestamping in PLCs for custody transfer records.",
            ["PLC", "Timestamping", "Custody Transfer"],
            1.0
        ),
        SearchDocument(
            36,
            "Radio Propagation in Oilfield SCADA",
            "Understanding radio propagation and its impact on SCADA communications in oilfields.",
            ["Radio", "Propagation", "SCADA"],
            1.0
        ),
        SearchDocument(
            37,
            "Cellular SCADA APN Configuration",
            "How to configure APNs for secure and reliable cellular SCADA communications.",
            ["Cellular SCADA", "APN", "Configuration"],
            1.0
        ),
        SearchDocument(
            38,
            "Ultrasonic Tank Level Sensor Installation",
            "Best practices for installing ultrasonic tank level sensors in oilfield environments.",
            ["Ultrasonic", "Tank Level", "Installation"],
            1.0
        ),
        SearchDocument(
            39,
            "DMZ Architectures for SCADA Cybersecurity",
            "Designing DMZ architectures to secure SCADA and OT networks from external threats.",
            ["DMZ", "SCADA", "Cybersecurity"],
            1.0
        ),
        SearchDocument(
            40,
            "Alarm Performance Monitoring in SCADA",
            "Methods for monitoring alarm system performance in SCADA, including KPIs and reporting.",
            ["SCADA", "Alarm Management", "Performance Monitoring"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)