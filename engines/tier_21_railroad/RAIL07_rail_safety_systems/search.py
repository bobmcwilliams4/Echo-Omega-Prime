import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Set, Tuple, Optional

class SearchDocument:
    def __init__(self, id: int, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = id
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
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.doc_lengths: Dict[int, int] = defaultdict(int)
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tokenizer = re.compile(r'\b\w+\b', re.UNICODE)
    
    def _tokenize(self, text: str) -> List[str]:
        return [t.lower() for t in self._tokenizer.findall(text)]
    
    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf.keys():
                self.doc_freqs[term] += 1
            self.documents[doc.id] = doc
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / max(1, self.N)
            self._idf_cache.clear()
    
    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf
    
    def _score_bm25(self, query_terms: List[str], doc_id: int, k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        avg_dl = self.avg_doc_length
        doc = self.documents[doc_id]
        for term in set(query_terms):
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + k1 * (1 - b + b * doc_len / avg_dl)
            numer = f * (k1 + 1)
            score += idf * numer / denom
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        doc = self.documents[doc_id]
        score = 0.0
        for term in set(query_terms):
            tf_norm = tf.get(term, 0) / max(1, doc_len)
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, use_bm25: bool = True) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        doc_scores: Dict[int, float] = {}
        for doc_id in self.documents:
            if use_bm25:
                score = self._score_bm25(query_terms, doc_id)
            else:
                score = self._score_tfidf(query_terms, doc_id)
            if score > 0:
                doc_scores[doc_id] = score
        top_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in top_docs:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = ' '.join(tokens[:window])
            return snippet + '...' if len(tokens) > window else snippet
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return '...' + snippet + '...' if start > 0 or end < len(tokens) else snippet

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                'num_documents': self.N,
                'avg_doc_length': self.avg_doc_length,
                'num_terms': len(self.doc_freqs),
            }

# Singleton factory for SearchIndex
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "PTC Implementation Requirements",
            "Positive Train Control (PTC) systems must be implemented on Class I main lines carrying toxic-by-inhalation hazardous materials and on any line with regularly scheduled intercity or commuter rail passenger service. Implementation deadlines, interoperability, and system certification are mandated by FRA regulations.",
            ["PTC", "FRA", "Implementation", "Regulations"]
        ),
        SearchDocument(
            2,
            "Grade Crossing Warning Systems",
            "Grade crossing warning systems include active devices such as flashing lights, gates, and bells, as well as passive signage. FRA regulations specify installation, maintenance, and inspection requirements to ensure public safety at highway-rail intersections.",
            ["Grade Crossing", "Warning Systems", "FRA", "Safety"]
        ),
        SearchDocument(
            3,
            "FRA Track Safety Standards Overview",
            "The FRA Track Safety Standards (49 CFR Part 213) establish minimum safety requirements for railroad track, including geometry, inspection intervals, and defect remediation. Compliance is mandatory for all railroads operating in the United States.",
            ["Track Safety", "FRA", "Standards", "Geometry"]
        ),
        SearchDocument(
            4,
            "Derailment Causation Analysis",
            "Derailments may result from track defects, equipment failures, human error, or environmental factors. Root cause analysis involves examination of wheel-rail interaction, track geometry, and maintenance records to identify contributing factors.",
            ["Derailment", "Analysis", "Track Defects", "Root Cause"]
        ),
        SearchDocument(
            5,
            "Hazmat Rail Transport Regulations",
            "Transport of hazardous materials by rail is governed by PHMSA and FRA regulations, including requirements for tank car design, routing analysis, emergency response planning, and security risk assessments.",
            ["Hazmat", "Rail Transport", "PHMSA", "FRA"]
        ),
        SearchDocument(
            6,
            "Locomotive Event Recorder Analysis",
            "Locomotive event recorders capture data such as speed, throttle position, brake application, horn use, and crew activity. Analysis of event recorder data is critical for accident investigation and operational review.",
            ["Locomotive", "Event Recorder", "Accident Investigation"]
        ),
        SearchDocument(
            7,
            "Locomotive Alerter and Vigilance Systems",
            "Alerter systems monitor engineer activity and provide visual and audible warnings if inactivity is detected. If no response is received, the system initiates a penalty brake application to stop the train.",
            ["Locomotive", "Alerter", "Vigilance", "Safety"]
        ),
        SearchDocument(
            8,
            "End-of-Train Device (EOT) Requirements",
            "EOT devices monitor brake pipe pressure and transmit data to the locomotive. FRA regulations require EOTs on most freight trains to ensure safe train operation and emergency brake application capability.",
            ["EOT", "End-of-Train", "FRA", "Brake Pipe"]
        ),
        SearchDocument(
            9,
            "Broken Rail Detection Technologies",
            "Broken rail detection uses track circuits, acoustic sensors, and fiber optic cables to identify rail fractures in real time. Early detection is vital for preventing derailments and maintaining track integrity.",
            ["Broken Rail", "Detection", "Sensors", "Track Circuits"]
        ),
        SearchDocument(
            10,
            "Track Geometry Degradation Analysis",
            "Track geometry degradation is monitored using geometry cars and automated inspection systems. Key parameters include alignment, gauge, crosslevel, and surface. Data analysis supports targeted maintenance.",
            ["Track Geometry", "Degradation", "Inspection", "Maintenance"]
        ),
        SearchDocument(
            11,
            "Signal System Types and Operations",
            "Railroad signal systems include automatic block, centralized traffic control, and cab signaling. Each system governs train movement authority and provides vital information to train crews.",
            ["Signal System", "Operations", "CTC", "Cab Signaling"]
        ),
        SearchDocument(
            12,
            "NTSB Railroad Investigation Procedures",
            "The NTSB investigates major railroad accidents, focusing on evidence collection, interviews, and analysis of operational, mechanical, and human factors. Recommendations are issued to improve safety.",
            ["NTSB", "Investigation", "Accident", "Safety"]
        ),
        SearchDocument(
            13,
            "Railroad Bridge Inspection and Safety",
            "Railroad bridges require periodic inspection per FRA Bridge Safety Standards. Inspections assess structural integrity, load capacity, and maintenance needs to prevent failures.",
            ["Bridge", "Inspection", "FRA", "Structural Integrity"]
        ),
        SearchDocument(
            14,
            "Freight Car Brake System Requirements",
            "Freight car brakes must comply with AAR and FRA standards, including periodic testing, maintenance, and component replacement. Proper brake operation is essential for train safety.",
            ["Freight Car", "Brake System", "AAR", "FRA"]
        ),
        SearchDocument(
            15,
            "Railroad Worker Safety and Roadway Worker Protection",
            "Roadway Worker Protection (RWP) rules require on-track safety briefings, use of personal protective equipment, and establishment of safe zones. FRA regulations mandate training and compliance audits.",
            ["Worker Safety", "RWP", "FRA", "Protection"]
        ),
        SearchDocument(
            16,
            "Tank Car Thermal Protection Requirements",
            "Tank cars transporting flammable or toxic materials must have thermal protection systems such as jackets, insulation, and pressure relief devices. These features mitigate risks during accidents or fires.",
            ["Tank Car", "Thermal Protection", "Hazmat", "Safety"]
        ),
        SearchDocument(
            17,
            "Railroad Dispatching and Train Authority",
            "Dispatching methods include timetable and train order, track warrant control, and centralized traffic control. Dispatchers grant movement authority and coordinate train operations to prevent conflicts.",
            ["Dispatching", "Train Authority", "CTC", "Operations"]
        ),
        SearchDocument(
            18,
            "Wheel Impact Load Detection (WILD)",
            "WILD systems use trackside sensors to detect high-impact wheels that can damage track or rolling stock. Data from WILD sites is used to schedule repairs and prevent derailments.",
            ["WILD", "Wheel Impact", "Detection", "Sensors"]
        ),
        SearchDocument(
            19,
            "Passenger Rail Crashworthiness Standards",
            "Crashworthiness standards for passenger railcars address structural strength, energy absorption, and occupant protection. FRA regulations specify requirements for new and refurbished equipment.",
            ["Passenger Rail", "Crashworthiness", "FRA", "Standards"]
        ),
        SearchDocument(
            20,
            "Railroad Crossing Sight Distance Requirements",
            "Adequate sight distance at railroad crossings is necessary for motorists to detect approaching trains. Standards define minimum clearances based on train speed, roadway geometry, and traffic volume.",
            ["Crossing", "Sight Distance", "Standards", "Safety"]
        ),
        SearchDocument(
            21,
            "Locomotive Fuel System Safety",
            "Locomotive fuel systems must be designed to minimize fire risk, including crash-resistant fuel tanks, protective skirting, and secure mounting. FRA rules govern inspection and maintenance.",
            ["Locomotive", "Fuel System", "Safety", "FRA"]
        ),
        SearchDocument(
            22,
            "Railroad Trespasser Prevention Measures",
            "Trespasser prevention includes fencing, signage, public education campaigns, and enforcement. Effective programs reduce injuries and fatalities associated with unauthorized track access.",
            ["Trespasser", "Prevention", "Safety", "Fencing"]
        ),
        SearchDocument(
            23,
            "Rail Fatigue and Defect Growth",
            "Rail fatigue is monitored using ultrasonic inspection and defect tracking. Growth rates inform rail replacement schedules and maintenance planning to prevent failures.",
            ["Rail Fatigue", "Defect Growth", "Inspection", "Maintenance"]
        ),
        SearchDocument(
            24,
            "Passenger Train Emergency Evacuation",
            "Emergency evacuation procedures for passenger trains include crew training, signage, emergency lighting, and accessible exits. Drills and regulatory compliance are essential for passenger safety.",
            ["Passenger Train", "Evacuation", "Emergency", "Safety"]
        ),
        SearchDocument(
            25,
            "Superelevation and Curve Maintenance",
            "Superelevation (cant) is the elevation difference between the two rails on a curve. Proper maintenance ensures safe train operation and reduces wear on wheels and rail.",
            ["Superelevation", "Curve", "Maintenance", "Track"]
        ),
        SearchDocument(
            26,
            "Railroad Signal Maintenance and Testing",
            "Signal systems require regular maintenance, including lamp checks, relay testing, and verification of aspect displays. FRA rules specify intervals and documentation requirements.",
            ["Signal", "Maintenance", "Testing", "FRA"]
        ),
        SearchDocument(
            27,
            "Wayside Detector Integration with PTC",
            "Wayside detectors such as hot box, dragging equipment, and WILD sensors can interface with PTC systems to provide real-time alerts and automate train response.",
            ["PTC", "Wayside Detector", "Integration", "Sensors"]
        ),
        SearchDocument(
            28,
            "Railroad Emergency Response Planning",
            "Emergency response plans for railroads address hazardous material releases, derailments, and passenger incidents. Coordination with local agencies and regular drills are required.",
            ["Emergency Response", "Planning", "Hazmat", "Drills"]
        ),
        SearchDocument(
            29,
            "Track Buckling and Thermal Stress Management",
            "Track buckling due to thermal expansion is managed through rail anchoring, stress monitoring, and maintenance of neutral temperature. FRA guidelines address inspection and remediation.",
            ["Track Buckling", "Thermal Stress", "Maintenance", "FRA"]
        ),
        SearchDocument(
            30,
            "Railroad Communication Protocols",
            "Communication protocols such as radio, digital messaging, and PTC data links are critical for train control and safety. FRA standards govern reliability and redundancy.",
            ["Communication", "Protocols", "PTC", "Safety"]
        ),
    ]
    for doc in docs:
        idx.add_document(doc)