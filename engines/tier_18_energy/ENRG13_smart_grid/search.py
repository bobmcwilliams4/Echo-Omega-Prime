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
    def __init__(self, bm25_k1: float = 1.5, bm25_b: float = 0.75):
        self.documents: Dict[int, SearchDocument] = {}
        self.inverted_index: Dict[str, List[Tuple[int, int]]] = defaultdict(list)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.total_docs: int = 0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.bm25_k1 = bm25_k1
        self.bm25_b = bm25_b
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_norms: Dict[int, float] = {}

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            term_counts = Counter(tokens)
            for term, freq in term_counts.items():
                self.inverted_index[term].append((doc.id, freq))
                self.term_doc_freq[term] += 1
            self._idf_cache.clear()
            self._tfidf_norms.clear()
            self._update_avg_doc_length()

    def _update_avg_doc_length(self):
        if self.total_docs == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int, term_freqs: Dict[str, int]) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        for term in query_terms:
            if term not in term_freqs:
                continue
            idf = self._compute_idf(term)
            tf = term_freqs[term]
            numerator = tf * (self.bm25_k1 + 1)
            denominator = tf + self.bm25_k1 * (1 - self.bm25_b + self.bm25_b * doc_length / (self.avg_doc_length or 1))
            score += idf * numerator / denominator
        doc = self.documents[doc_id]
        return score * doc.weight

    def _compute_tfidf_norm(self, doc_id: int, term_freqs: Dict[str, int]) -> float:
        if doc_id in self._tfidf_norms:
            return self._tfidf_norms[doc_id]
        norm = 0.0
        for term, tf in term_freqs.items():
            idf = self._compute_idf(term)
            norm += (tf * idf) ** 2
        norm = math.sqrt(norm)
        self._tfidf_norms[doc_id] = norm
        return norm

    def _score_tfidf(self, query_terms: List[str], doc_id: int, term_freqs: Dict[str, int]) -> float:
        score = 0.0
        query_tf = Counter(query_terms)
        norm = self._compute_tfidf_norm(doc_id, term_freqs)
        if norm == 0:
            return 0.0
        for term in query_tf:
            tf = term_freqs.get(term, 0)
            idf = self._compute_idf(term)
            score += (tf * idf)
        doc = self.documents[doc_id]
        return (score / norm) * doc.weight

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], max_len: int = 160) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:max_len]
            return snippet + ('...' if len(content) > max_len else '')
        start = max(positions[0] - 5, 0)
        end = min(positions[0] + 10, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        if len(snippet) > max_len:
            snippet = snippet[:max_len] + '...'
        return snippet

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidate_docs: Dict[int, Dict[str, int]] = {}
        for term in query_terms:
            for doc_id, freq in self.inverted_index.get(term, []):
                if doc_id not in candidate_docs:
                    candidate_docs[doc_id] = {}
                candidate_docs[doc_id][term] = freq
        results = []
        for doc_id, term_freqs in candidate_docs.items():
            bm25_score = self._score_bm25(query_terms, doc_id, term_freqs)
            tfidf_score = self._score_tfidf(query_terms, doc_id, term_freqs)
            combined_score = 0.7 * bm25_score + 0.3 * tfidf_score
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, combined_score, doc.title, snippet))
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:limit]

    def get_stats(self) -> Dict[str, int]:
        return {
            'total_documents': self.total_docs,
            'unique_terms': len(self.inverted_index),
            'avg_doc_length': int(self.avg_doc_length),
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
            "AMI: Two-way Communication",
            "Advanced Metering Infrastructure (AMI) enables two-way communication between utilities and consumers, allowing for real-time data collection, remote meter reading, and improved demand response.",
            ["AMI", "Communication", "Smart Grid"], 1.0
        ),
        SearchDocument(
            2,
            "SCADA: Supervisory Control and Data Acquisition",
            "SCADA systems provide centralized monitoring and control of grid assets, supporting automation, fault detection, and efficient grid operations.",
            ["SCADA", "Automation", "Monitoring"], 1.0
        ),
        SearchDocument(
            3,
            "DER Integration: Distributed Energy Resources",
            "Integration of distributed energy resources (DER) such as solar, wind, and storage requires advanced grid management, real-time monitoring, and bidirectional power flow control.",
            ["DER", "Integration", "Renewables"], 1.0
        ),
        SearchDocument(
            4,
            "Demand Response: Incentive and Price-Based Programs",
            "Demand response (DR) programs incentivize consumers to reduce or shift electricity usage during peak periods through price signals or direct load control.",
            ["Demand Response", "DR", "Pricing"], 1.0
        ),
        SearchDocument(
            5,
            "Microgrid: Islanding and Reconnection",
            "Microgrids can operate independently (islanding) or reconnect to the main grid, providing resilience during outages and supporting black start capabilities.",
            ["Microgrid", "Islanding", "Resilience"], 1.0
        ),
        SearchDocument(
            6,
            "Energy Storage: Battery, Flywheel, and Compressed Air",
            "Energy storage technologies such as batteries, flywheels, and compressed air energy storage (CAES) enhance grid flexibility, reliability, and support renewable integration.",
            ["Energy Storage", "Battery", "CAES"], 1.0
        ),
        SearchDocument(
            7,
            "Power Quality: Voltage Sag, Swell, Harmonics, THD",
            "Power quality management addresses voltage sags, swells, harmonics, and total harmonic distortion (THD) to ensure reliable operation of sensitive equipment.",
            ["Power Quality", "Harmonics", "THD"], 1.0
        ),
        SearchDocument(
            8,
            "Wide Area Monitoring (WAMS): Synchrophasor, PMU",
            "WAMS uses synchrophasor measurements from Phasor Measurement Units (PMUs) to monitor grid stability and detect disturbances in real-time.",
            ["WAMS", "PMU", "Synchrophasor"], 1.0
        ),
        SearchDocument(
            9,
            "Distribution Automation: Recloser, Sectionalizer",
            "Distribution automation employs devices like reclosers and sectionalizers to automatically isolate faults and restore power, improving reliability.",
            ["Distribution Automation", "Recloser", "Sectionalizer"], 1.0
        ),
        SearchDocument(
            10,
            "Volt-VAR Optimization: Capacitor Bank, Regulator",
            "Volt-VAR optimization uses capacitor banks and voltage regulators to maintain optimal voltage profiles and reduce losses across the distribution network.",
            ["Volt-VAR", "Capacitor Bank", "Regulator"], 1.0
        ),
        SearchDocument(
            11,
            "Outage Management System (OMS): Fault Location, FLISR",
            "OMS leverages fault location, isolation, and service restoration (FLISR) to minimize outage duration and improve customer satisfaction.",
            ["OMS", "FLISR", "Outage"], 1.0
        ),
        SearchDocument(
            12,
            "Cybersecurity: NERC CIP Standards Compliance",
            "Cybersecurity in smart grids is governed by NERC CIP standards, ensuring protection of critical infrastructure from cyber threats and vulnerabilities.",
            ["Cybersecurity", "NERC CIP", "Compliance"], 1.0
        ),
        SearchDocument(
            13,
            "AMI: Remote Meter Reading",
            "Remote meter reading via AMI reduces operational costs, improves billing accuracy, and enables faster detection of meter tampering or outages.",
            ["AMI", "Meter Reading", "Remote"], 1.0
        ),
        SearchDocument(
            14,
            "SCADA: Fault Detection and Isolation",
            "SCADA systems rapidly detect and isolate faults, minimizing disruption and supporting self-healing grid capabilities.",
            ["SCADA", "Fault Detection", "Isolation"], 1.0
        ),
        SearchDocument(
            15,
            "DER: Solar and Wind Integration Challenges",
            "Integrating solar and wind DERs introduces variability and intermittency, requiring advanced forecasting and grid balancing solutions.",
            ["DER", "Solar", "Wind"], 1.0
        ),
        SearchDocument(
            16,
            "Demand Response: Automated Load Control",
            "Automated load control in DR programs enables utilities to manage peak demand and grid stability through direct control of customer loads.",
            ["Demand Response", "Automation", "Load Control"], 1.0
        ),
        SearchDocument(
            17,
            "Microgrid: Black Start Capability",
            "Microgrids with black start capability can restore power without external grid support, enhancing resilience during widespread outages.",
            ["Microgrid", "Black Start", "Resilience"], 1.0
        ),
        SearchDocument(
            18,
            "Energy Storage: Grid Services",
            "Energy storage systems provide grid services such as frequency regulation, spinning reserve, and peak shaving, supporting overall grid reliability.",
            ["Energy Storage", "Grid Services", "Frequency Regulation"], 1.0
        ),
        SearchDocument(
            19,
            "Power Quality: Harmonic Mitigation",
            "Mitigating harmonics in power systems prevents equipment overheating, misoperation, and extends asset lifespan.",
            ["Power Quality", "Harmonics", "Mitigation"], 1.0
        ),
        SearchDocument(
            20,
            "WAMS: Real-Time Grid Monitoring",
            "Real-time grid monitoring with WAMS enhances situational awareness and enables proactive grid management.",
            ["WAMS", "Real-Time", "Monitoring"], 1.0
        ),
        SearchDocument(
            21,
            "Distribution Automation: Self-Healing Networks",
            "Self-healing networks automatically detect, isolate, and restore faults, reducing outage times and operational costs.",
            ["Distribution Automation", "Self-Healing", "Networks"], 1.0
        ),
        SearchDocument(
            22,
            "Volt-VAR: Conservation Voltage Reduction",
            "Conservation voltage reduction (CVR) through Volt-VAR optimization lowers energy consumption and peak demand.",
            ["Volt-VAR", "CVR", "Optimization"], 1.0
        ),
        SearchDocument(
            23,
            "OMS: Customer Communication",
            "OMS platforms provide outage notifications and restoration updates to customers, improving transparency and satisfaction.",
            ["OMS", "Customer", "Communication"], 1.0
        ),
        SearchDocument(
            24,
            "Cybersecurity: Threat Detection",
            "Advanced cybersecurity solutions detect and mitigate threats to smart grid infrastructure, ensuring data integrity and system availability.",
            ["Cybersecurity", "Threat Detection", "Smart Grid"], 1.0
        ),
        SearchDocument(
            25,
            "DER: Aggregation and Market Participation",
            "DER aggregation enables small-scale resources to participate in energy markets, providing flexibility and new revenue streams.",
            ["DER", "Aggregation", "Market"], 1.0
        ),
        SearchDocument(
            26,
            "SCADA: Data Acquisition Protocols",
            "SCADA systems utilize protocols like DNP3 and IEC 61850 for reliable data acquisition and device interoperability.",
            ["SCADA", "Protocols", "Data Acquisition"], 1.0
        ),
        SearchDocument(
            27,
            "Energy Storage: Compressed Air Systems",
            "Compressed air energy storage (CAES) systems store energy in the form of compressed air, offering long-duration storage for grid applications.",
            ["Energy Storage", "CAES", "Compressed Air"], 1.0
        ),
        SearchDocument(
            28,
            "Microgrid: Renewable Integration",
            "Microgrids facilitate the integration of renewables, enabling local generation and consumption with minimal grid dependency.",
            ["Microgrid", "Renewables", "Integration"], 1.0
        ),
        SearchDocument(
            29,
            "Power Quality: Voltage Regulation",
            "Voltage regulation devices maintain stable voltage levels, preventing equipment damage and improving power quality.",
            ["Power Quality", "Voltage Regulation", "Devices"], 1.0
        ),
        SearchDocument(
            30,
            "Distribution Automation: Fault Location",
            "Automated fault location in distribution networks accelerates restoration and reduces manual intervention.",
            ["Distribution Automation", "Fault Location", "Restoration"], 1.0
        ),
        SearchDocument(
            31,
            "Volt-VAR: Smart Inverters",
            "Smart inverters support Volt-VAR optimization by dynamically adjusting reactive power to maintain voltage stability.",
            ["Volt-VAR", "Smart Inverters", "Reactive Power"], 1.0
        ),
        SearchDocument(
            32,
            "OMS: Integration with GIS",
            "OMS integration with Geographic Information Systems (GIS) enhances situational awareness and outage response efficiency.",
            ["OMS", "GIS", "Integration"], 1.0
        ),
        SearchDocument(
            33,
            "Cybersecurity: Incident Response",
            "Incident response plans ensure rapid detection, containment, and recovery from cybersecurity events in smart grid environments.",
            ["Cybersecurity", "Incident Response", "Smart Grid"], 1.0
        ),
        SearchDocument(
            34,
            "DER: Grid Interconnection Standards",
            "Grid interconnection standards for DERs ensure safety, reliability, and interoperability of distributed resources.",
            ["DER", "Interconnection", "Standards"], 1.0
        ),
        SearchDocument(
            35,
            "SCADA: Human-Machine Interface",
            "SCADA Human-Machine Interfaces (HMIs) provide operators with intuitive dashboards for real-time grid management.",
            ["SCADA", "HMI", "Interface"], 1.0
        ),
        SearchDocument(
            36,
            "Microgrid: Economic Dispatch",
            "Economic dispatch in microgrids optimizes the use of local generation and storage to minimize operational costs.",
            ["Microgrid", "Economic Dispatch", "Optimization"], 1.0
        ),
        SearchDocument(
            37,
            "Energy Storage: Flywheel Systems",
            "Flywheel energy storage systems deliver high-power, short-duration energy for grid stabilization and frequency support.",
            ["Energy Storage", "Flywheel", "Grid Stabilization"], 1.0
        ),
        SearchDocument(
            38,
            "Power Quality: Monitoring Solutions",
            "Advanced power quality monitoring solutions detect and analyze disturbances, supporting proactive maintenance.",
            ["Power Quality", "Monitoring", "Disturbances"], 1.0
        ),
        SearchDocument(
            39,
            "WAMS: Data Analytics",
            "WAMS data analytics extract actionable insights from synchrophasor data to enhance grid reliability and planning.",
            ["WAMS", "Analytics", "Synchrophasor"], 1.0
        ),
        SearchDocument(
            40,
            "Distribution Automation: Volt-VAR Control",
            "Automated Volt-VAR control in distribution networks optimizes voltage and reactive power for efficient operation.",
            ["Distribution Automation", "Volt-VAR", "Control"], 1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)