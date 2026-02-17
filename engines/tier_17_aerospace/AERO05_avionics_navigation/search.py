import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# -----------------------------
# Data Classes
# -----------------------------

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

# -----------------------------
# Search Index
# -----------------------------

class SearchIndex:
    def __init__(self):
        self._documents: Dict[int, SearchDocument] = {}
        self._doc_tokens: Dict[int, List[str]] = {}
        self._doc_lengths: Dict[int, int] = {}
        self._inverted_index: Dict[str, List[int]] = defaultdict(list)
        self._term_freqs: Dict[int, Counter] = {}
        self._doc_freqs: Dict[str, int] = defaultdict(int)
        self._idf_cache: Dict[str, float] = {}
        self._avgdl: float = 0.0
        self._lock = threading.Lock()
        self._next_id = 1
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    # -------------------------
    # Tokenization
    # -------------------------
    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

    # -------------------------
    # Add Document
    # -------------------------
    def add_document(self, title: str, content: str, tags: List[str], weight: float = 1.0) -> int:
        with self._lock:
            doc_id = self._next_id
            self._next_id += 1

            document = SearchDocument(doc_id, title, content, tags, weight)
            self._documents[doc_id] = document

            tokens = self._tokenize(content)
            self._doc_tokens[doc_id] = tokens
            self._doc_lengths[doc_id] = len(tokens)
            tf = Counter(tokens)
            self._term_freqs[doc_id] = tf

            for term in set(tokens):
                self._inverted_index[term].append(doc_id)
                self._doc_freqs[term] += 1

            # Invalidate IDF cache and update avgdl
            self._idf_cache.clear()
            self._avgdl = sum(self._doc_lengths.values()) / len(self._doc_lengths)
            return doc_id

    # -------------------------
    # Compute IDF
    # -------------------------
    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        N = len(self._documents)
        df = self._doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            # BM25 IDF variant
            idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    # -------------------------
    # BM25 Scoring
    # -------------------------
    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc_len = self._doc_lengths[doc_id]
        avgdl = self._avgdl
        tf = self._term_freqs[doc_id]
        doc = self._documents[doc_id]
        for term in query_terms:
            if term not in tf:
                continue
            f = tf[term]
            idf = self._compute_idf(term)
            numerator = f * (self._bm25_k1 + 1)
            denominator = f + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / avgdl)
            score += idf * numerator / denominator
        return score * doc.weight

    # -------------------------
    # TF-IDF Scoring
    # -------------------------
    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self._term_freqs[doc_id]
        doc_len = self._doc_lengths[doc_id]
        doc = self._documents[doc_id]
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            tf_norm = tf[term] / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * doc.weight

    # -------------------------
    # Search
    # -------------------------
    def search(self, query: str, limit: int = 10, method: str = 'bm25') -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []

        # Find candidate documents
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self._inverted_index.get(term, []))
        if not candidate_docs:
            return []

        # Score candidates
        scored: List[Tuple[int, float]] = []
        for doc_id in candidate_docs:
            if method == 'bm25':
                score = self._score_bm25(query_terms, doc_id)
            else:
                score = self._score_tfidf(query_terms, doc_id)
            if score > 0:
                scored.append((doc_id, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored[:limit]:
            doc = self._documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    # -------------------------
    # Snippet Generation
    # -------------------------
    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:window]) + ('...' if len(tokens) > window else '')
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return '...' + snippet + '...' if start > 0 else snippet + '...'

    # -------------------------
    # Stats
    # -------------------------
    def get_stats(self) -> Dict[str, int]:
        return {
            'documents': len(self._documents),
            'terms': len(self._doc_freqs),
            'avg_doc_length': int(self._avgdl)
        }

# -----------------------------
# Singleton Factory
# -----------------------------

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

# -----------------------------
# Pre-seed Domain Documents
# -----------------------------

def _preseed_documents(idx: SearchIndex):
    docs = [
        {
            "title": "VOR DME ILS Approach Procedures",
            "content": "VOR, DME, and ILS approaches provide precision and non-precision navigation guidance during instrument approaches. Pilots must tune and identify the correct frequencies, monitor CDI and GS indications, and comply with published minima and missed approach instructions.",
            "tags": ["VOR", "DME", "ILS", "Approach", "Navigation"]
        },
        {
            "title": "GPS WAAS and SBAS Augmentation",
            "content": "WAAS and SBAS enhance GPS accuracy and integrity for enroute, terminal, and approach phases. These systems provide corrections via geostationary satellites, enabling LPV approaches with vertical guidance.",
            "tags": ["GPS", "WAAS", "SBAS", "Augmentation", "Navigation"]
        },
        {
            "title": "GBAS Ground-Based Augmentation System",
            "content": "GBAS provides local differential corrections for GPS signals, supporting CAT I/II/III precision approaches. Aircraft avionics receive GBAS data via VHF datalink, improving approach accuracy and integrity.",
            "tags": ["GBAS", "GPS", "Augmentation", "Approach"]
        },
        {
            "title": "INS Inertial Navigation and Kalman Filtering",
            "content": "Inertial Navigation Systems (INS) use accelerometers and gyroscopes to compute position and velocity. Kalman filtering integrates INS with GPS and other sensors, correcting drift and enhancing navigation accuracy.",
            "tags": ["INS", "Inertial", "Kalman", "Filtering", "Navigation"]
        },
        {
            "title": "FMS CDU Operation and Flight Plan Management",
            "content": "The Flight Management System (FMS) Control Display Unit (CDU) enables pilots to enter, modify, and execute flight plans. Functions include route selection, waypoint editing, performance data entry, and lateral/vertical navigation mode selection.",
            "tags": ["FMS", "CDU", "Flight Plan", "Management"]
        },
        {
            "title": "ADS-B Surveillance and Transponder Modes",
            "content": "ADS-B Out broadcasts aircraft position, velocity, and identification. Transponder modes A, C, and S provide ATC with altitude and identity. Mode S supports selective interrogation and data link capabilities.",
            "tags": ["ADS-B", "Transponder", "Surveillance", "Mode S"]
        },
        {
            "title": "TCAS Collision Avoidance and Resolution Advisories",
            "content": "The Traffic Collision Avoidance System (TCAS) monitors nearby aircraft transponder signals. TCAS issues Traffic Advisories (TA) and Resolution Advisories (RA) to prevent mid-air collisions, providing vertical maneuver guidance.",
            "tags": ["TCAS", "Collision Avoidance", "Resolution Advisory"]
        },
        {
            "title": "EGPWS Terrain Awareness and Alerts",
            "content": "Enhanced Ground Proximity Warning System (EGPWS) uses terrain databases and aircraft position to provide predictive terrain alerts, cautioning pilots of potential Controlled Flight Into Terrain (CFIT) risks.",
            "tags": ["EGPWS", "Terrain", "Awareness", "CFIT"]
        },
        {
            "title": "Weather Radar (WXR) Interpretation",
            "content": "Weather radar displays precipitation intensity and movement. Pilots interpret color-coded returns to avoid hazardous weather, adjust tilt and gain, and use ground mapping for terrain awareness.",
            "tags": ["Weather Radar", "WXR", "Interpretation"]
        },
        {
            "title": "HF, VHF, and SATCOM Radio Systems",
            "content": "HF radios provide long-range communication, VHF is used for line-of-sight ATC comms, and SATCOM enables voice/data links over oceanic and remote areas. Proper frequency management is essential for effective communication.",
            "tags": ["HF", "VHF", "SATCOM", "Radio", "Communication"]
        },
        {
            "title": "Datalink: ACARS and CPDLC Operations",
            "content": "ACARS transmits operational and ATC messages between aircraft and ground. CPDLC enables digital ATC communications, reducing voice congestion and supporting clearances, requests, and reports.",
            "tags": ["Datalink", "ACARS", "CPDLC", "Communication"]
        },
        {
            "title": "Glass Cockpit: EFIS, PFD, ND, and EICAS",
            "content": "Electronic Flight Instrument System (EFIS) integrates Primary Flight Display (PFD), Navigation Display (ND), and Engine Indication and Crew Alerting System (EICAS) for situational awareness and system monitoring.",
            "tags": ["Glass Cockpit", "EFIS", "PFD", "ND", "EICAS"]
        },
        {
            "title": "Autopilot and Flight Director Servo Modes",
            "content": "Autopilot systems use servos to control pitch, roll, and yaw. Flight Director provides visual guidance cues. Modes include heading hold, LNAV, VNAV, approach, and altitude capture.",
            "tags": ["Autopilot", "Flight Director", "Servo", "Modes"]
        },
        {
            "title": "Air Data Computer and Pitot-Static Systems",
            "content": "The Air Data Computer (ADC) processes pitot-static and temperature data to compute airspeed, altitude, and vertical speed. Accurate pitot-static system operation is vital for reliable flight instrument indications.",
            "tags": ["Air Data Computer", "Pitot-Static", "Airspeed", "Altitude"]
        },
        {
            "title": "Radio Altimeter and Decision Height",
            "content": "Radio altimeters measure height above terrain using radar signals. Decision Height (DH) is set for precision approaches, triggering alerts at minimums for missed approach decision-making.",
            "tags": ["Radio Altimeter", "Decision Height", "Approach"]
        },
        {
            "title": "DME Arc and Procedure Turns",
            "content": "DME arcs require maintaining a constant distance from a DME station while intercepting approach courses. Procedure turns facilitate course reversal for approach alignment.",
            "tags": ["DME Arc", "Procedure Turn", "Approach"]
        },
        {
            "title": "RNAV and RNP Approaches",
            "content": "RNAV and RNP approaches use area navigation and onboard performance monitoring. RNP approaches require specific navigation accuracy and alerting capabilities for lateral and vertical guidance.",
            "tags": ["RNAV", "RNP", "Approach", "Navigation"]
        },
        {
            "title": "RVSM: Reduced Vertical Separation Minimum",
            "content": "RVSM airspace allows 1000-foot vertical separation between FL290 and FL410. Aircraft must meet stringent altimetry, autopilot, and monitoring requirements for RVSM operations.",
            "tags": ["RVSM", "Vertical Separation", "Altimetry"]
        },
        {
            "title": "ELT: Emergency Locator Transmitter",
            "content": "ELTs transmit distress signals on 121.5 and 406 MHz for search and rescue. Modern ELTs interface with GPS to provide accurate position data to rescue authorities.",
            "tags": ["ELT", "Emergency Locator", "Rescue"]
        },
        {
            "title": "Cockpit Voice Recorder and Flight Data Recorder",
            "content": "CVR records cockpit audio, while FDR logs flight parameters. Both are critical for accident investigation and safety analysis, meeting regulatory retention and survivability standards.",
            "tags": ["CVR", "FDR", "Recorder", "Accident Investigation"]
        },
        {
            "title": "Performance Monitoring and Altitude Management",
            "content": "Continuous performance monitoring ensures compliance with required navigation performance. Altitude management involves autopilot, FMS, and barometric settings to maintain assigned flight levels.",
            "tags": ["Performance Monitoring", "Altitude Management", "FMS"]
        },
        {
            "title": "Surveillance Integrity Monitoring",
            "content": "Integrity monitoring verifies the reliability of navigation and surveillance data. Systems like RAIM and ADS-B integrity checks ensure safe operations in performance-based navigation environments.",
            "tags": ["Surveillance", "Integrity Monitoring", "RAIM", "ADS-B"]
        },
        {
            "title": "Cockpit Display Management",
            "content": "Pilots manage display layouts, brightness, and data overlays on glass cockpit systems. Effective display management enhances situational awareness and reduces workload.",
            "tags": ["Cockpit Display", "Glass Cockpit", "Situational Awareness"]
        },
        {
            "title": "Emergency Communications Procedures",
            "content": "Emergency communications use dedicated frequencies, transponder codes (7700), and may involve SATCOM or HF in remote areas. Procedures ensure rapid coordination with ATC and rescue services.",
            "tags": ["Emergency", "Communications", "ATC", "SATCOM", "HF"]
        },
        {
            "title": "Navigation Database Management",
            "content": "Navigation databases in FMS and avionics require regular updates to ensure current procedures and waypoints. Database integrity is critical for RNAV and RNP operations.",
            "tags": ["Navigation Database", "FMS", "RNAV", "RNP"]
        },
        {
            "title": "Flight Data Monitoring and Analysis",
            "content": "Flight Data Monitoring (FDM) programs analyze recorded flight parameters for safety trends, compliance, and operational improvement. FDM supports proactive risk management.",
            "tags": ["Flight Data Monitoring", "FDM", "Safety"]
        },
        {
            "title": "Autopilot Servo Modes and Redundancy",
            "content": "Modern autopilot systems feature redundant servos and control channels. Redundancy ensures continued operation in case of component failure, supporting safe automated flight.",
            "tags": ["Autopilot", "Servo", "Redundancy"]
        },
        {
            "title": "System Redundancy and Integrity Monitoring",
            "content": "Critical avionics systems employ redundancy and continuous integrity monitoring to detect failures and maintain safe operation. Cross-checks and alerts support pilot awareness.",
            "tags": ["System Redundancy", "Integrity Monitoring", "Avionics"]
        },
        {
            "title": "Flight Plan Management in FMS",
            "content": "FMS flight plan management includes route entry, modification, and activation. Pilots can insert waypoints, airways, and alternate airports, optimizing routing and fuel efficiency.",
            "tags": ["Flight Plan", "FMS", "Routing"]
        },
        {
            "title": "Decision Height and Minimums in Approaches",
            "content": "Decision Height (DH) and Minimum Descent Altitude (MDA) are critical approach minima. Pilots must initiate missed approach if visual references are not acquired at DH/MDA.",
            "tags": ["Decision Height", "Minimums", "Approach"]
        },
        {
            "title": "Integrity Monitoring in Navigation Systems",
            "content": "Navigation systems employ integrity monitoring to detect and alert pilots to errors. RAIM, SBAS, and GBAS provide integrity assurance for GPS-based navigation.",
            "tags": ["Integrity Monitoring", "Navigation", "RAIM", "SBAS", "GBAS"]
        }
    ]
    for doc in docs:
        idx.add_document(doc["title"], doc["content"], doc["tags"])