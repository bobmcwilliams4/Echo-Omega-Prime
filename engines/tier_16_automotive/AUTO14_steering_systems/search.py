import math
import re
import threading
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional


class SearchDocument:
    def __init__(self, doc_id: str, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = doc_id
        self.title = title
        self.content = content
        self.tags = tags
        self.weight = weight


class SearchResult:
    def __init__(self, doc_id: str, score: float, title: str, snippet: str):
        self.doc_id = doc_id
        self.score = score
        self.title = title
        self.snippet = snippet


class SearchIndex:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_term_freqs: Dict[str, Counter] = {}
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.avg_doc_len: float = 0.0
        self.total_doc_len: int = 0
        self.N: int = 0
        self.lock = threading.Lock()

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                # Remove old doc stats
                old_tf = self.doc_term_freqs[doc.id]
                for term in old_tf:
                    self.term_doc_freqs[term] -= 1
                    if self.term_doc_freqs[term] <= 0:
                        del self.term_doc_freqs[term]
                old_len = sum(old_tf.values())
                self.total_doc_len -= old_len
                self.N -= 1
                del self.doc_term_freqs[doc.id]

            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            tf = Counter(tokens)
            self.doc_term_freqs[doc.id] = tf
            for term in tf:
                self.term_doc_freqs[term] += 1
            doc_len = sum(tf.values())
            self.total_doc_len += doc_len
            self.N += 1
            self.avg_doc_len = self.total_doc_len / self.N if self.N > 0 else 0.0

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms or self.N == 0:
            return []

        idf = self._compute_idf(query_terms)
        scores: Dict[str, float] = defaultdict(float)

        with self.lock:
            for doc_id, tf in self.doc_term_freqs.items():
                score = self._score_bm25(tf, idf, query_terms, self.documents[doc_id])
                if score > 0:
                    scores[doc_id] = score

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id=doc_id, score=score, title=doc.title, snippet=snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "total_documents": self.N,
                "average_document_length": self.avg_doc_len,
                "unique_terms": len(self.term_doc_freqs),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, query_terms: List[str]) -> Dict[str, float]:
        idf = {}
        for term in query_terms:
            df = self.term_doc_freqs.get(term, 0)
            # BM25 IDF with smoothing
            idf_val = math.log(1 + (self.N - df + 0.5) / (df + 0.5)) if self.N > 0 else 0.0
            idf[term] = idf_val
        return idf

    def _score_bm25(self, tf: Counter, idf: Dict[str, float], query_terms: List[str], doc: SearchDocument) -> float:
        score = 0.0
        doc_len = sum(tf.values())
        for term in query_terms:
            if term not in tf:
                continue
            f = tf[term]
            numerator = f * (self.k1 + 1)
            denominator = f + self.k1 * (1 - self.b + self.b * (doc_len / self.avg_doc_len if self.avg_doc_len > 0 else 1))
            score += idf.get(term, 0.0) * (numerator / denominator)
        # Incorporate document weight as a multiplier
        score *= doc.weight
        return score

    def _make_snippet(self, content: str, query_terms: List[str], snippet_length: int = 160) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            start = 0
            while True:
                idx = content_lower.find(term, start)
                if idx == -1:
                    break
                positions.append(idx)
                start = idx + 1
        if not positions:
            snippet = content[:snippet_length].strip()
            if len(content) > snippet_length:
                snippet += "..."
            return snippet

        positions.sort()
        # Take first occurrence for snippet window
        start_pos = max(positions[0] - snippet_length // 4, 0)
        end_pos = min(start_pos + snippet_length, len(content))
        snippet = content[start_pos:end_pos].strip()
        if start_pos > 0:
            snippet = "..." + snippet
        if end_pos < len(content):
            snippet += "..."
        return snippet


_singleton_instance: Optional[SearchIndex] = None
_singleton_lock = threading.Lock()


def get_search_index() -> SearchIndex:
    global _singleton_instance
    with _singleton_lock:
        if _singleton_instance is None:
            _singleton_instance = SearchIndex(k1=1.5, b=0.75)
            _preseed_documents(_singleton_instance)
        return _singleton_instance


def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            doc_id="doc001",
            title="Hydraulic Power Steering Fluid Contamination",
            content=(
                "Contamination in hydraulic power steering fluid can cause increased wear, "
                "reduced lubrication, and eventual failure of steering components. Regular "
                "fluid analysis and replacement are critical to maintain system integrity."
            ),
            tags=["hydraulic", "power steering", "fluid", "contamination"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc002",
            title="Electric Power Steering Torque Sensor Drift",
            content=(
                "Torque sensor drift in electric power steering systems leads to inaccurate "
                "steering assist and can cause vehicle instability. Calibration and sensor "
                "diagnostics are essential to detect and correct drift."
            ),
            tags=["electric power steering", "torque sensor", "drift", "calibration"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc003",
            title="Rack and Pinion Inner Tie Rod Wear",
            content=(
                "Wear in the inner tie rod of rack and pinion steering assemblies causes "
                "steering play and misalignment. Inspection and replacement prevent unsafe "
                "steering conditions."
            ),
            tags=["rack and pinion", "inner tie rod", "wear", "steering play"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc004",
            title="Ackermann Steering Geometry Principles",
            content=(
                "Ackermann steering geometry ensures that the inner and outer wheels turn "
                "at appropriate angles to reduce tire scrub during cornering, improving "
                "handling and tire wear."
            ),
            tags=["ackermann", "steering geometry", "cornering", "tire scrub"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="doc005",
            title="Steer-by-Wire Redundancy Architecture",
            content=(
                "Steer-by-wire systems rely on electronic controls without mechanical linkage. "
                "Redundancy architectures are critical to ensure safety and fault tolerance."
            ),
            tags=["steer-by-wire", "redundancy", "architecture", "safety"],
            weight=1.4,
        ),
        SearchDocument(
            doc_id="doc006",
            title="Steering Column Intermediate Shaft U-Joint Failure",
            content=(
                "Failure of the U-joint in the steering column intermediate shaft can cause "
                "steering stiffness or loss of control. Regular inspection and lubrication "
                "are recommended."
            ),
            tags=["steering column", "intermediate shaft", "u-joint", "failure"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc007",
            title="Power Steering Pump Flow and Pressure Testing",
            content=(
                "Testing the flow rate and pressure output of power steering pumps helps "
                "diagnose pump wear, leaks, and system blockages affecting steering performance."
            ),
            tags=["power steering pump", "flow", "pressure", "testing"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc008",
            title="Electric Power Steering Motor Current Draw Analysis",
            content=(
                "Analyzing the current draw of EPS motors can reveal motor faults, excessive "
                "load, or electrical issues impacting steering assist."
            ),
            tags=["electric power steering", "motor", "current draw", "analysis"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc009",
            title="Toe Angle and Tire Wear Correlation",
            content=(
                "Incorrect toe angle settings cause uneven tire wear and affect vehicle "
                "handling. Regular alignment checks are necessary to maintain optimal toe."
            ),
            tags=["toe angle", "tire wear", "alignment", "vehicle handling"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="doc010",
            title="Rack and Pinion Hydraulic Seal Leak Diagnosis",
            content=(
                "Leaks in rack and pinion hydraulic seals lead to fluid loss and steering "
                "performance degradation. Early diagnosis prevents component damage."
            ),
            tags=["rack and pinion", "hydraulic seal", "leak", "diagnosis"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc011",
            title="Steering Angle Sensor Calibration Procedures",
            content=(
                "Proper calibration of steering angle sensors is essential for stability control "
                "systems and accurate steering feedback."
            ),
            tags=["steering angle sensor", "calibration", "stability control"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc012",
            title="Variable Ratio Steering Analysis",
            content=(
                "Variable ratio steering systems adjust steering sensitivity based on vehicle "
                "speed and conditions, enhancing maneuverability and stability."
            ),
            tags=["variable ratio", "steering", "sensitivity", "vehicle speed"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc013",
            title="Power Steering Hose Pressure Rating and Failure",
            content=(
                "Power steering hoses must meet pressure ratings to avoid bursts or leaks. "
                "Failure analysis includes inspecting hose material and connections."
            ),
            tags=["power steering", "hose", "pressure rating", "failure"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc014",
            title="EPS Motor Position Sensor Hall Effect Failure",
            content=(
                "Hall effect sensor failures in EPS motor position sensing cause erratic "
                "steering assist and require sensor replacement or recalibration."
            ),
            tags=["EPS", "motor position sensor", "hall effect", "failure"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc015",
            title="Kingpin Inclination and Scrub Radius Effects",
            content=(
                "Kingpin inclination and scrub radius influence steering effort, stability, "
                "and tire wear. Proper design and adjustment optimize steering feel."
            ),
            tags=["kingpin inclination", "scrub radius", "steering effort", "stability"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc016",
            title="Steering Column Tilt and Telescoping Mechanism Failure",
            content=(
                "Failures in tilt and telescoping mechanisms reduce driver comfort and "
                "may cause steering misalignment."
            ),
            tags=["steering column", "tilt", "telescoping", "mechanism failure"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="doc017",
            title="Active Return-to-Center Steering Analysis",
            content=(
                "Active return-to-center systems assist the driver by automatically centering "
                "the steering wheel after a turn, improving safety and comfort."
            ),
            tags=["active return-to-center", "steering", "safety", "comfort"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc018",
            title="Rack and Pinion Mounting Bushing Wear",
            content=(
                "Wear in rack and pinion mounting bushings causes steering play and noise. "
                "Timely replacement maintains steering precision."
            ),
            tags=["rack and pinion", "mounting bushing", "wear", "steering play"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc019",
            title="EPS Column-Assist vs Rack-Assist Architecture",
            content=(
                "EPS systems can be column-assist or rack-assist, each with distinct design "
                "trade-offs affecting steering feel and packaging."
            ),
            tags=["EPS", "column-assist", "rack-assist", "architecture"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc020",
            title="Hydraulic Power Steering Pump Belt Failure Effects",
            content=(
                "Failure of the power steering pump belt results in loss of assist and "
                "increased steering effort, requiring immediate repair."
            ),
            tags=["hydraulic power steering", "pump belt", "failure", "steering effort"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc021",
            title="Steering Wheel Vibration Diagnosis (Shimmy vs Shake)",
            content=(
                "Differentiating shimmy from shake in steering wheel vibrations helps identify "
                "causes such as tire imbalance or suspension faults."
            ),
            tags=["steering wheel", "vibration", "shimmy", "shake", "diagnosis"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc022",
            title="Active Front Steering (AFS) Planetary Gear System",
            content=(
                "AFS uses planetary gear systems to vary steering ratio dynamically, improving "
                "maneuverability and stability."
            ),
            tags=["active front steering", "AFS", "planetary gear", "steering ratio"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc023",
            title="Steering Gear Ratio Calculation and Effects",
            content=(
                "Calculating steering gear ratio is essential for tuning steering response "
                "and driver feedback."
            ),
            tags=["steering gear ratio", "calculation", "steering response"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="doc024",
            title="EPS Thermal Management and Overheating Protection",
            content=(
                "Thermal management in EPS systems prevents motor overheating and prolongs "
                "component life through sensors and cooling strategies."
            ),
            tags=["EPS", "thermal management", "overheating", "protection"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc025",
            title="Four-Wheel Steering (4WS) Rear Steering Control",
            content=(
                "4WS systems control rear wheel steering angles to improve stability and "
                "maneuverability at various speeds."
            ),
            tags=["four-wheel steering", "4WS", "rear steering", "control"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc026",
            title="Steering Column Bearing Noise Diagnosis",
            content=(
                "Noises from steering column bearings indicate wear or lubrication issues, "
                "affecting steering smoothness."
            ),
            tags=["steering column", "bearing", "noise", "diagnosis"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="doc027",
            title="Bump Steer Analysis and Correction",
            content=(
                "Bump steer occurs when suspension movement causes unintended steering input. "
                "Analysis and correction improve vehicle stability and tire wear."
            ),
            tags=["bump steer", "analysis", "correction", "vehicle stability"],
            weight=1.2,
        ),
    ]
    for doc in docs:
        index.add_document(doc)