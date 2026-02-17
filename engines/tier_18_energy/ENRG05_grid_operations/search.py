import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

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
        self._documents: Dict[int, SearchDocument] = {}
        self._inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_length: float = 0.0
        self._total_docs: int = 0
        self._idf_cache: Dict[str, float] = {}
        self._lock = threading.RLock()
        self._doc_id_counter = 1

    def add_document(self, title: str, content: str, tags: List[str], weight: float = 1.0) -> int:
        with self._lock:
            doc_id = self._doc_id_counter
            self._doc_id_counter += 1
            doc = SearchDocument(doc_id, title, content, tags, weight)
            self._documents[doc_id] = doc
            tokens = self._tokenize(content)
            self._doc_lengths[doc_id] = len(tokens)
            for token in tokens:
                self._inverted_index[token][doc_id] = self._inverted_index[token].get(doc_id, 0) + 1
            self._total_docs += 1
            self._avg_doc_length = sum(self._doc_lengths.values()) / max(1, self._total_docs)
            self._idf_cache.clear()
            return doc_id

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        tokens = self._tokenize(query)
        if not tokens:
            return []
        doc_scores: Dict[int, float] = defaultdict(float)
        doc_snippets: Dict[int, str] = {}
        for token in set(tokens):
            idf = self._compute_idf(token)
            postings = self._inverted_index.get(token, {})
            for doc_id, freq in postings.items():
                doc = self._documents[doc_id]
                bm25_score = self._score_bm25(token, doc_id, freq, idf)
                tfidf_score = self._score_tfidf(token, doc_id, freq, idf)
                score = bm25_score + 0.25 * tfidf_score
                doc_scores[doc_id] += score * doc.weight
                if doc_id not in doc_snippets:
                    doc_snippets[doc_id] = self._make_snippet(doc, tokens)
        top_docs = heapq.nlargest(limit, doc_scores.items(), key=lambda x: x[1])
        results = []
        for doc_id, score in top_docs:
            doc = self._documents[doc_id]
            snippet = doc_snippets[doc_id]
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                "total_documents": self._total_docs,
                "average_doc_length": self._avg_doc_length,
                "unique_terms": len(self._inverted_index)
            }

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

    def _compute_idf(self, term: str) -> float:
        with self._lock:
            if term in self._idf_cache:
                return self._idf_cache[term]
            df = len(self._inverted_index.get(term, {}))
            N = self._total_docs
            idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
            self._idf_cache[term] = idf
            return idf

    def _score_bm25(self, term: str, doc_id: int, freq: int, idf: float) -> float:
        k1 = 1.5
        b = 0.75
        dl = self._doc_lengths.get(doc_id, 0)
        avgdl = self._avg_doc_length if self._avg_doc_length > 0 else 1
        tf = freq
        numerator = tf * (k1 + 1)
        denominator = tf + k1 * (1 - b + b * dl / avgdl)
        return idf * numerator / denominator

    def _score_tfidf(self, term: str, doc_id: int, freq: int, idf: float) -> float:
        tf = freq / self._doc_lengths.get(doc_id, 1)
        return tf * idf

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str]) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            return content[:160] + "..." if len(content) > 160 else content
        start = max(positions[0] - 8, 0)
        end = min(positions[0] + 12, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        return snippet + "..." if end < len(tokens) else snippet

# --- Singleton Factory ---

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    if _search_index_instance is None:
        with _search_index_lock:
            if _search_index_instance is None:
                idx = SearchIndex()
                _seed_documents(idx)
                _search_index_instance = idx
    return _search_index_instance

# --- Pre-seed Domain Documents ---

def _seed_documents(idx: SearchIndex):
    docs = [
        {
            "title": "Three-Phase AC Power Fundamentals",
            "content": (
                "Three-phase systems use three alternating currents, each phase offset by 120 degrees. "
                "This configuration provides constant power transfer, higher efficiency, and is the standard for power transmission and distribution."
            ),
            "tags": ["three-phase", "ac", "fundamentals", "power"],
        },
        {
            "title": "Power Factor and Reactive Power Management",
            "content": (
                "Power factor is the ratio of real power to apparent power. Low power factor increases losses. "
                "Reactive power compensation using capacitors or synchronous condensers improves system efficiency and voltage regulation."
            ),
            "tags": ["power factor", "reactive power", "compensation", "capacitors"],
        },
        {
            "title": "Transmission System Voltage Levels: HV, EHV, UHV",
            "content": (
                "High Voltage (HV), Extra High Voltage (EHV), and Ultra High Voltage (UHV) levels are used for long-distance power transmission. "
                "Higher voltages reduce line losses and allow efficient bulk power transfer."
            ),
            "tags": ["transmission", "hv", "ehv", "uhv", "voltage"],
        },
        {
            "title": "HVDC Transmission Systems",
            "content": (
                "High Voltage Direct Current (HVDC) transmission enables efficient long-distance and underwater power transfer. "
                "HVDC links improve grid stability and facilitate asynchronous interconnections."
            ),
            "tags": ["hvdc", "transmission", "dc", "grid"],
        },
        {
            "title": "Distribution System Configurations: Radial, Loop, Network",
            "content": (
                "Radial systems are simple and cost-effective but less reliable. Loop and networked configurations provide higher reliability and flexibility, "
                "allowing for alternative power paths during faults or maintenance."
            ),
            "tags": ["distribution", "radial", "loop", "network"],
        },
        {
            "title": "Power Transformers: Design and Operation",
            "content": (
                "Power transformers step voltage levels up or down for transmission and distribution. "
                "Key design considerations include core material, winding configuration, cooling, and insulation."
            ),
            "tags": ["transformer", "design", "operation", "power"],
        },
        {
            "title": "Circuit Breaker Technologies: SF6, Vacuum, Oil",
            "content": (
                "Circuit breakers interrupt fault currents. SF6 breakers offer high dielectric strength, vacuum breakers are maintenance-free, "
                "and oil breakers are used in legacy systems. Selection depends on application and voltage level."
            ),
            "tags": ["circuit breaker", "sf6", "vacuum", "oil"],
        },
        {
            "title": "Protective Relaying: Overcurrent, Distance, Differential",
            "content": (
                "Protective relays detect abnormal conditions and initiate circuit breaker operation. "
                "Overcurrent relays respond to excessive current, distance relays measure impedance, and differential relays compare currents at two points."
            ),
            "tags": ["protective relaying", "overcurrent", "distance", "differential"],
        },
        {
            "title": "SCADA and Energy Management Systems",
            "content": (
                "Supervisory Control and Data Acquisition (SCADA) systems enable remote monitoring and control of grid assets. "
                "Energy Management Systems (EMS) optimize power flows, generation dispatch, and reliability."
            ),
            "tags": ["scada", "ems", "energy management", "control"],
        },
        {
            "title": "Load Flow Analysis for Power System Planning",
            "content": (
                "Load flow studies determine voltage, current, and power flows in the network under steady-state conditions. "
                "They are essential for planning, operation, and expansion of power systems."
            ),
            "tags": ["load flow", "planning", "analysis"],
        },
        {
            "title": "Fault Analysis: Symmetrical and Asymmetrical Faults",
            "content": (
                "Symmetrical faults involve all phases equally, while asymmetrical faults affect one or two phases. "
                "Fault analysis helps determine fault currents, system stability, and protection settings."
            ),
            "tags": ["fault analysis", "symmetrical", "asymmetrical"],
        },
        {
            "title": "Power Quality Issues: Harmonics, Sag, Swell, Flicker",
            "content": (
                "Power quality disturbances include harmonics (distorted waveforms), voltage sags, swells, and flicker. "
                "Mitigation involves filters, voltage regulators, and proper equipment sizing."
            ),
            "tags": ["power quality", "harmonics", "sag", "swell", "flicker"],
        },
        {
            "title": "Voltage Regulation: Tap Changers, Regulators, Capacitors",
            "content": (
                "Voltage regulation devices maintain voltage within acceptable limits. "
                "Tap changers adjust transformer ratios, regulators control feeder voltage, and capacitors supply reactive power."
            ),
            "tags": ["voltage regulation", "tap changer", "regulator", "capacitor"],
        },
        {
            "title": "NERC Reliability Standards: Compliance Requirements",
            "content": (
                "The North American Electric Reliability Corporation (NERC) sets standards for grid reliability. "
                "Compliance includes critical infrastructure protection, event reporting, and operational planning."
            ),
            "tags": ["nerc", "reliability", "standards", "compliance"],
        },
        {
            "title": "Grid Interconnection: IEEE 1547 for Distributed Energy Resources",
            "content": (
                "IEEE 1547 defines requirements for interconnecting distributed energy resources (DER) with the grid. "
                "It covers voltage regulation, anti-islanding, and interoperability."
            ),
            "tags": ["ieee 1547", "interconnection", "der", "distributed energy"],
        },
        {
            "title": "Energy Storage Technologies: Battery, Pumped Hydro, Flywheel",
            "content": (
                "Energy storage improves grid flexibility and reliability. Technologies include batteries (fast response), "
                "pumped hydro (large scale), and flywheels (high cycle life)."
            ),
            "tags": ["energy storage", "battery", "pumped hydro", "flywheel"],
        },
        {
            "title": "Renewable Integration Challenges: Variability and Inverter Dynamics",
            "content": (
                "Renewable generation introduces variability and requires advanced inverter controls. "
                "Grid codes specify ride-through, frequency, and voltage support requirements."
            ),
            "tags": ["renewable", "integration", "inverter", "variability"],
        },
        {
            "title": "Microgrid Operation: Islanded and Grid-Connected Modes",
            "content": (
                "Microgrids can operate independently (islanded) or in parallel with the main grid. "
                "Control strategies manage transitions, load sharing, and voltage/frequency regulation."
            ),
            "tags": ["microgrid", "islanded", "grid-connected", "operation"],
        },
        {
            "title": "Power Market Operations: LMP and Ancillary Services",
            "content": (
                "Locational Marginal Pricing (LMP) reflects the cost of delivering electricity at specific locations. "
                "Ancillary services support grid reliability, including frequency regulation and spinning reserve."
            ),
            "tags": ["power market", "lmp", "ancillary services"],
        },
        {
            "title": "Static VAR Compensator (SVC) and STATCOM",
            "content": (
                "SVC and STATCOM are flexible AC transmission devices that provide dynamic reactive power support. "
                "They enhance voltage stability and power transfer capability."
            ),
            "tags": ["svc", "statcom", "var", "compensator"],
        },
        {
            "title": "Smart Grid Technologies: AMI, DA, DMS, DERMS",
            "content": (
                "Advanced Metering Infrastructure (AMI), Distribution Automation (DA), Distribution Management Systems (DMS), "
                "and Distributed Energy Resource Management Systems (DERMS) enable grid modernization and integration of renewables."
            ),
            "tags": ["smart grid", "ami", "da", "dms", "derms"],
        },
        {
            "title": "Demand Response and Load Management",
            "content": (
                "Demand response programs incentivize consumers to reduce or shift electricity usage during peak periods. "
                "Load management improves system reliability and reduces operational costs."
            ),
            "tags": ["demand response", "load management"],
        },
        {
            "title": "Arc Flash Hazard Analysis: NFPA 70E and IEEE 1584",
            "content": (
                "Arc flash analysis determines incident energy and required PPE. NFPA 70E and IEEE 1584 provide methodologies "
                "for calculating arc flash boundaries and mitigating electrical hazards."
            ),
            "tags": ["arc flash", "nfpa 70e", "ieee 1584", "hazard"],
        },
        {
            "title": "Distribution Automation and Self-Healing Grids",
            "content": (
                "Distribution automation enables real-time monitoring and control. Self-healing grids automatically detect, isolate, "
                "and restore faults, improving reliability and reducing outage durations."
            ),
            "tags": ["distribution automation", "self-healing", "grid"],
        },
        {
            "title": "Wide Area Monitoring, Protection, and Control (WAMPAC)",
            "content": (
                "WAMPAC systems use synchrophasor data for real-time situational awareness. They enhance protection, "
                "islanding detection, and system restoration capabilities in large interconnected grids."
            ),
            "tags": ["wampac", "synchrophasor", "monitoring", "protection"],
        },
        {
            "title": "Synchrophasor Technology and PMUs",
            "content": (
                "Phasor Measurement Units (PMUs) provide time-synchronized voltage and current measurements. "
                "Synchrophasor technology supports dynamic stability analysis and wide-area control."
            ),
            "tags": ["synchrophasor", "pmu", "phasor", "measurement"],
        },
        {
            "title": "Black Start Capability in Power Systems",
            "content": (
                "Black start capability enables grid restoration after a total blackout. Designated units can start without external power "
                "and sequentially energize the network."
            ),
            "tags": ["black start", "restoration", "grid"],
        },
        {
            "title": "Flexible AC Transmission Systems (FACTS)",
            "content": (
                "FACTS devices, such as SVC, STATCOM, and series compensators, enhance controllability and increase power transfer limits "
                "in AC transmission networks."
            ),
            "tags": ["facts", "svc", "statcom", "compensator"],
        },
        {
            "title": "Dynamic Line Rating for Transmission Optimization",
            "content": (
                "Dynamic line rating uses real-time environmental and loading data to adjust transmission line ratings, "
                "maximizing asset utilization and preventing thermal overloads."
            ),
            "tags": ["dynamic line rating", "transmission", "optimization"],
        },
        {
            "title": "Wide Area Protection Schemes",
            "content": (
                "Wide area protection schemes coordinate relays across the grid to prevent cascading failures. "
                "They use communication-assisted tripping and adaptive settings."
            ),
            "tags": ["wide area", "protection", "relays", "grid"],
        },
        {
            "title": "Grid Forming Inverters for Renewable Integration",
            "content": (
                "Grid forming inverters establish voltage and frequency reference in weak or islanded grids. "
                "They support renewable integration and microgrid operation."
            ),
            "tags": ["grid forming", "inverter", "renewable", "microgrid"],
        },
        {
            "title": "IEC 61850 for Substation Automation",
            "content": (
                "IEC 61850 is a communication standard for substation automation. It enables interoperability, "
                "fast protection schemes, and integration of intelligent electronic devices (IEDs)."
            ),
            "tags": ["iec 61850", "substation", "automation"],
        },
    ]
    for doc in docs:
        idx.add_document(doc["title"], doc["content"], doc["tags"])