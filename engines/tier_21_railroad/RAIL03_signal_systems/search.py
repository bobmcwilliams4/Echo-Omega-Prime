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

# --- Search Index ---

class SearchIndex:
    def __init__(self):
        self._documents: Dict[int, SearchDocument] = {}
        self._inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)  # term -> doc_id -> freq
        self._doc_lengths: Dict[int, int] = {}  # doc_id -> length
        self._doc_norms: Dict[int, float] = {}  # doc_id -> tf-idf norm
        self._avg_doc_length: float = 0.0
        self._lock = threading.RLock()
        self._total_terms = 0
        self._idf_cache: Dict[str, float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            self._documents[doc.id] = doc
            terms = self._tokenize(doc.content)
            term_counts = Counter(terms)
            self._doc_lengths[doc.id] = len(terms)
            self._total_terms += len(terms)
            for term, freq in term_counts.items():
                self._inverted_index[term][doc.id] = freq
            self._avg_doc_length = (
                sum(self._doc_lengths.values()) / len(self._doc_lengths)
                if self._doc_lengths else 0.0
            )
            self._idf_cache.clear()
            self._doc_norms[doc.id] = self._compute_doc_norm(doc.id)

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        with self._lock:
            query_terms = self._tokenize(query)
            if not query_terms:
                return []
            candidate_docs = set()
            for term in query_terms:
                candidate_docs.update(self._inverted_index.get(term, {}).keys())
            scored: List[Tuple[int, float]] = []
            for doc_id in candidate_docs:
                bm25_score = self._score_bm25(doc_id, query_terms)
                tfidf_score = self._score_tfidf(doc_id, query_terms)
                doc_weight = self._documents[doc_id].weight
                score = 0.7 * bm25_score + 0.3 * tfidf_score
                score *= doc_weight
                scored.append((doc_id, score))
            scored.sort(key=lambda x: x[1], reverse=True)
            results = []
            for doc_id, score in scored[:limit]:
                doc = self._documents[doc_id]
                snippet = self._make_snippet(doc.content, query_terms)
                results.append(SearchResult(doc_id, score, doc.title, snippet))
            return results

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                "documents": len(self._documents),
                "avg_doc_length": self._avg_doc_length,
                "total_terms": self._total_terms,
                "unique_terms": len(self._inverted_index),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9\-]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        with self._lock:
            if term in self._idf_cache:
                return self._idf_cache[term]
            N = len(self._documents)
            df = len(self._inverted_index.get(term, {}))
            if df == 0:
                idf = 0.0
            else:
                idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
            self._idf_cache[term] = idf
            return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        doc = self._documents[doc_id]
        doc_len = self._doc_lengths[doc_id]
        avgdl = self._avg_doc_length or 1.0
        score = 0.0
        term_freqs = self._inverted_index
        for term in query_terms:
            f = term_freqs.get(term, {}).get(doc_id, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / avgdl)
            score += idf * (f * (self._bm25_k1 + 1)) / (denom + 1e-9)
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        doc = self._documents[doc_id]
        doc_len = self._doc_lengths[doc_id]
        tfidf = 0.0
        norm = self._doc_norms.get(doc_id, 1.0)
        for term in query_terms:
            tf = self._inverted_index.get(term, {}).get(doc_id, 0) / (doc_len or 1)
            idf = self._compute_idf(term)
            tfidf += tf * idf
        return tfidf / (norm or 1.0)

    def _compute_doc_norm(self, doc_id: int) -> float:
        doc_len = self._doc_lengths[doc_id]
        norm = 0.0
        for term, docs in self._inverted_index.items():
            tf = docs.get(doc_id, 0) / (doc_len or 1)
            idf = self._compute_idf(term)
            norm += (tf * idf) ** 2
        return math.sqrt(norm) or 1.0

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:window]) + ('...' if len(tokens) > window else '')
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(r'\b({})\b'.format(re.escape(term)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + ('...' if end < len(tokens) else '')

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
            "Absolute Permissive Block (APB) Overview",
            "The Absolute Permissive Block (APB) system is a railroad signaling method that divides tracks into blocks. Each block is protected by signals that prevent trains from entering an occupied block, ensuring safe train separation.",
            ["APB", "Block System", "Safety"],
            1.0
        ),
        SearchDocument(
            2,
            "APB Signal Aspects and Indications",
            "APB systems use color light, position light, and searchlight signals to convey track status. Aspects include green for proceed, yellow for approach, and red for stop, with rules for permissive and absolute indications.",
            ["APB", "Signal Aspects", "Color Light"],
            1.0
        ),
        SearchDocument(
            3,
            "Mechanical Interlocking Principles",
            "Mechanical interlocking systems use levers, rods, and bars to physically prevent conflicting train movements at junctions. Fail-safe design ensures that a failure results in the most restrictive aspect.",
            ["Interlocking", "Mechanical", "Fail-Safe"],
            1.0
        ),
        SearchDocument(
            4,
            "Relay-Based Interlocking Systems",
            "Relay interlocking replaces mechanical linkages with electrical relays, allowing more complex logic for route locking, signal control, and detection. Relays are wired to default to safe states upon failure.",
            ["Interlocking", "Relay", "Fail-Safe"],
            1.0
        ),
        SearchDocument(
            5,
            "Electronic and Computer-Based Interlocking",
            "Modern interlocking uses microprocessors and software to control signals and switches. Redundant hardware and software checks are implemented for fail-safe operation.",
            ["Interlocking", "Electronic", "Computer-Based"],
            1.0
        ),
        SearchDocument(
            6,
            "Color Light Signal Aspects",
            "Color light signals use combinations of red, yellow, and green lights to indicate track status. Multiple heads or lamps may be used to provide additional information such as speed or route.",
            ["Signal Aspects", "Color Light"],
            1.0
        ),
        SearchDocument(
            7,
            "Position Light Signal Systems",
            "Position light signals use arrays of lamps to form patterns representing different aspects. Commonly used on the Pennsylvania Railroad, these signals are highly visible in poor weather.",
            ["Signal Aspects", "Position Light"],
            1.0
        ),
        SearchDocument(
            8,
            "Searchlight Signal Mechanisms",
            "Searchlight signals use a single lamp and movable color filter to display multiple aspects. They are compact and energy efficient, but require precise mechanical alignment.",
            ["Signal Aspects", "Searchlight"],
            1.0
        ),
        SearchDocument(
            9,
            "DC Track Circuits in Signal Systems",
            "Direct current (DC) track circuits are the oldest and most common method for train detection. The presence of a train shunts the circuit, causing the relay to drop and signals to display stop.",
            ["Track Circuits", "DC"],
            1.0
        ),
        SearchDocument(
            10,
            "AC Track Circuits and Audio Frequency Track Circuits",
            "Alternating current (AC) and audio frequency track circuits are used where DC circuits are unsuitable, such as in electrified territory. Audio frequency circuits allow for jointless operation.",
            ["Track Circuits", "AC", "Audio Frequency", "Jointless"],
            1.0
        ),
        SearchDocument(
            11,
            "Jointless Track Circuit Technology",
            "Jointless track circuits eliminate insulated rail joints by using coded signals or different frequencies for adjacent blocks. This reduces maintenance and improves reliability.",
            ["Track Circuits", "Jointless"],
            1.0
        ),
        SearchDocument(
            12,
            "Positive Train Control (PTC) Fundamentals",
            "Positive Train Control (PTC) is a safety overlay system that prevents train-to-train collisions, overspeed derailments, and unauthorized movements. PTC integrates signals, GPS, and wireless communications.",
            ["PTC", "Safety", "Overlay"],
            1.0
        ),
        SearchDocument(
            13,
            "I-ETMS Architecture in PTC",
            "The Interoperable Electronic Train Management System (I-ETMS) is a PTC implementation that uses on-board computers, wayside interface units, and a back office server for centralized control.",
            ["PTC", "I-ETMS", "Architecture"],
            1.0
        ),
        SearchDocument(
            14,
            "Centralized Traffic Control (CTC) Overview",
            "Centralized Traffic Control (CTC) allows a dispatcher to remotely control signals and switches over a large territory. CTC increases efficiency and safety by reducing manual intervention.",
            ["CTC", "Dispatcher", "Control"],
            1.0
        ),
        SearchDocument(
            15,
            "Dispatcher Command and Control in CTC",
            "In CTC, the dispatcher issues commands from a central office. Field equipment receives and executes commands, updating the dispatcher with real-time status.",
            ["CTC", "Dispatcher", "Command"],
            1.0
        ),
        SearchDocument(
            16,
            "Active Grade Crossing Warning Systems",
            "Active grade crossing protection includes flashing lights, bells, and gates activated by approaching trains. Track circuits or axle counters detect train presence to trigger warnings.",
            ["Grade Crossing", "Active Protection"],
            1.0
        ),
        SearchDocument(
            17,
            "Passive Grade Crossing Protection",
            "Passive protection at grade crossings consists of signs and pavement markings. No active warning is provided; motorists must observe and obey the signage.",
            ["Grade Crossing", "Passive Protection"],
            1.0
        ),
        SearchDocument(
            18,
            "Fail-Safe Design Principles in Signaling",
            "Fail-safe design ensures that any failure in the signal system results in the safest possible condition, typically a stop signal. Redundancy and default states are key strategies.",
            ["Fail-Safe", "Design", "Safety"],
            1.0
        ),
        SearchDocument(
            19,
            "Assured Safety Through Failure Modes",
            "Signal systems are engineered to default to restrictive aspects upon failure. Failure mode analysis is performed to identify and mitigate unsafe conditions.",
            ["Fail-Safe", "Failure Modes"],
            1.0
        ),
        SearchDocument(
            20,
            "Signal System Redundancy",
            "Redundant circuits, power supplies, and communication links are used to maintain signal system operation in the event of a component failure.",
            ["Fail-Safe", "Redundancy"],
            1.0
        ),
        SearchDocument(
            21,
            "Wayside Interface Units in PTC",
            "Wayside interface units (WIUs) connect field devices to the PTC network, relaying status and control information between the train and the back office server.",
            ["PTC", "Wayside", "WIU"],
            1.0
        ),
        SearchDocument(
            22,
            "Back Office Server Role in PTC",
            "The back office server maintains the database of track, signal, and speed restriction information. It communicates with trains and wayside equipment to enforce movement authorities.",
            ["PTC", "Back Office", "Server"],
            1.0
        ),
        SearchDocument(
            23,
            "Route Locking in Interlocking Systems",
            "Route locking prevents conflicting train movements by ensuring that once a route is set and occupied, no other conflicting route can be established until the first is cleared.",
            ["Interlocking", "Route Locking"],
            1.0
        ),
        SearchDocument(
            24,
            "Signal Aspect Rules and Indications",
            "Rules for interpreting signal aspects are codified in operating rules. Each aspect corresponds to a specific action, such as proceed, approach, or stop and proceed.",
            ["Signal Aspects", "Rules"],
            1.0
        ),
        SearchDocument(
            25,
            "Axle Counters in Train Detection",
            "Axle counters are an alternative to track circuits for train detection. They count axles entering and leaving a section to determine occupancy, useful where track circuits are impractical.",
            ["Track Circuits", "Axle Counter"],
            1.0
        ),
        SearchDocument(
            26,
            "Communications in Modern Signal Systems",
            "Modern signal systems use digital communications, including fiber optics and wireless networks, to transmit control and status data between field equipment and control centers.",
            ["Signal Systems", "Communications"],
            1.0
        ),
        SearchDocument(
            27,
            "Event Logging and Diagnostics",
            "Signal systems incorporate event loggers and diagnostic tools to monitor system health, record failures, and assist in troubleshooting and maintenance.",
            ["Diagnostics", "Event Logging"],
            1.0
        ),
        SearchDocument(
            28,
            "Speed Enforcement in PTC",
            "PTC systems enforce speed restrictions by continuously monitoring train speed and location, automatically applying brakes if limits are exceeded.",
            ["PTC", "Speed Enforcement"],
            1.0
        ),
        SearchDocument(
            29,
            "Interlocking Control Logic",
            "Interlocking logic determines when signals and switches can be cleared based on track occupancy, route requests, and safety rules. Logic is implemented in hardware or software.",
            ["Interlocking", "Control Logic"],
            1.0
        ),
        SearchDocument(
            30,
            "System Integration and Testing",
            "Integration and testing of signaling systems ensures compatibility and reliability. Simulations and field tests validate system performance under normal and failure conditions.",
            ["Signal Systems", "Integration", "Testing"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)