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
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                # Remove old document data
                self._remove_document(doc.id)
            tokens = self._tokenize(doc.content)
            length = len(tokens)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = length
            term_counts = Counter(tokens)
            for term, freq in term_counts.items():
                if self.term_freqs[term][doc.id] == 0:
                    self.doc_freqs[term] += 1
                self.term_freqs[term][doc.id] = freq
            self.N = len(self.documents)
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self.idf_cache.clear()

    def _remove_document(self, doc_id: str):
        if doc_id not in self.documents:
            return
        old_doc = self.documents[doc_id]
        old_tokens = self._tokenize(old_doc.content)
        old_term_counts = Counter(old_tokens)
        for term in old_term_counts:
            if doc_id in self.term_freqs[term]:
                del self.term_freqs[term][doc_id]
                if len(self.term_freqs[term]) == 0:
                    del self.term_freqs[term]
                    del self.doc_freqs[term]
                else:
                    self.doc_freqs[term] -= 1
        del self.documents[doc_id]
        del self.doc_lengths[doc_id]
        self.N = len(self.documents)
        self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
        self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        scores: Dict[str, float] = defaultdict(float)
        idf_values = {term: self._compute_idf(term) for term in query_terms}
        for term in query_terms:
            postings = self.term_freqs.get(term, {})
            idf = idf_values.get(term, 0.0)
            for doc_id, freq in postings.items():
                score = self._score_bm25(freq, idf, self.doc_lengths[doc_id])
                scores[doc_id] += score
        # Adjust scores by document weight
        for doc_id in scores:
            scores[doc_id] *= self.documents[doc_id].weight
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                'total_documents': self.N,
                'average_document_length': self.avg_doc_length,
                'total_terms_indexed': len(self.term_freqs),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, freq: int, idf: float, doc_length: int) -> float:
        numerator = freq * (self.k1 + 1)
        denominator = freq + self.k1 * (1 - self.b + self.b * (doc_length / self.avg_doc_length if self.avg_doc_length > 0 else 1))
        return idf * (numerator / denominator)

    def _make_snippet(self, content: str, query_terms: List[str], snippet_length: int = 160) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            pos = content_lower.find(term)
            if pos != -1:
                positions.append(pos)
        if not positions:
            snippet = content[:snippet_length].strip()
            if len(content) > snippet_length:
                snippet += "..."
            return snippet
        start = max(min(positions) - snippet_length // 4, 0)
        end = start + snippet_length
        snippet = content[start:end].strip()
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet += "..."
        return snippet


_singleton_instance: Optional[SearchIndex] = None
_singleton_lock = threading.Lock()


def get_search_index() -> SearchIndex:
    global _singleton_instance
    with _singleton_lock:
        if _singleton_instance is None:
            _singleton_instance = SearchIndex()
            _preseed_index(_singleton_instance)
        return _singleton_instance


def _preseed_index(index: SearchIndex):
    docs = [
        SearchDocument(
            "doc001",
            "SAE J3016 Automation Levels Overview",
            "The SAE J3016 standard defines six levels of driving automation from Level 0 (no automation) to Level 5 (full automation). Each level specifies the extent of driver assistance and system capabilities.",
            ["SAE J3016", "Automation Levels", "Standard", "Autonomous Driving"],
            1.0
        ),
        SearchDocument(
            "doc002",
            "LiDAR Point Cloud Processing Techniques",
            "LiDAR sensors generate point clouds representing the environment. Processing includes filtering, segmentation, and feature extraction to support perception and mapping in autonomous vehicles.",
            ["LiDAR", "Point Cloud", "Processing", "Perception"],
            1.2
        ),
        SearchDocument(
            "doc003",
            "Simultaneous Localization and Mapping (SLAM)",
            "SLAM algorithms enable a vehicle to build a map of an unknown environment while simultaneously tracking its location within it, critical for autonomous navigation.",
            ["SLAM", "Localization", "Mapping", "Autonomous Navigation"],
            1.3
        ),
        SearchDocument(
            "doc004",
            "YOLO CNN for Camera Vision Object Detection",
            "You Only Look Once (YOLO) is a real-time object detection system using convolutional neural networks to identify and locate objects in camera images.",
            ["YOLO", "CNN", "Object Detection", "Camera Vision"],
            1.1
        ),
        SearchDocument(
            "doc005",
            "Radar Millimeter Wave Doppler Velocity Measurement",
            "Radar sensors use millimeter wave frequencies to detect objects and measure their velocity using the Doppler effect, essential for adaptive cruise control and collision avoidance.",
            ["Radar", "Millimeter Wave", "Doppler", "Velocity Measurement"],
            1.0
        ),
        SearchDocument(
            "doc006",
            "Sensor Fusion Using Kalman Filters",
            "Kalman filters combine measurements from multiple sensors to estimate the state of a system more accurately than individual sensors alone.",
            ["Sensor Fusion", "Kalman Filter", "Estimation", "Data Fusion"],
            1.4
        ),
        SearchDocument(
            "doc007",
            "Extended and Unscented Kalman Filters for Nonlinear Systems",
            "Extended Kalman Filter (EKF) and Unscented Kalman Filter (UKF) are advanced techniques for sensor fusion and state estimation in nonlinear dynamic systems.",
            ["EKF", "UKF", "Nonlinear Systems", "Sensor Fusion"],
            1.3
        ),
        SearchDocument(
            "doc008",
            "Multi-Object Perception and Tracking",
            "Tracking multiple objects in the environment is crucial for safe autonomous driving, involving data association, motion prediction, and trajectory estimation.",
            ["Perception", "Object Tracking", "Multi-Object", "Autonomous Driving"],
            1.2
        ),
        SearchDocument(
            "doc009",
            "Path Planning Algorithms: A-star and RRT",
            "A-star is a heuristic search algorithm for pathfinding, while Rapidly-exploring Random Trees (RRT) are used for efficient exploration of high-dimensional spaces in motion planning.",
            ["Path Planning", "A-star", "RRT", "Motion Planning"],
            1.3
        ),
        SearchDocument(
            "doc010",
            "Trajectory Optimization for Motion Planning",
            "Trajectory optimization techniques generate smooth, feasible paths for autonomous vehicles by minimizing cost functions subject to constraints.",
            ["Trajectory Optimization", "Motion Planning", "Autonomous Vehicles"],
            1.2
        ),
        SearchDocument(
            "doc011",
            "PID Control in Autonomous Driving Systems",
            "Proportional-Integral-Derivative (PID) controllers regulate vehicle actuators to maintain desired speed, steering angle, and stability.",
            ["PID Control", "Control Systems", "Autonomous Driving"],
            1.0
        ),
        SearchDocument(
            "doc012",
            "Model Predictive Control (MPC) for Vehicle Dynamics",
            "MPC uses a model of vehicle dynamics to predict future states and optimize control inputs over a time horizon, improving trajectory tracking and safety.",
            ["MPC", "Model Predictive Control", "Vehicle Dynamics", "Control"],
            1.3
        ),
        SearchDocument(
            "doc013",
            "V2X Communication Technologies: DSRC and C-V2X",
            "Vehicle-to-Everything (V2X) communication enables vehicles to exchange information with infrastructure and other vehicles using DSRC and Cellular V2X technologies.",
            ["V2X", "DSRC", "C-V2X", "Communication"],
            1.4
        ),
        SearchDocument(
            "doc014",
            "HD Mapping and Lane-Level Localization",
            "High-definition maps provide detailed lane-level information to support precise localization and navigation in autonomous driving.",
            ["HD Mapping", "Localization", "Lane-Level", "Autonomous Driving"],
            1.2
        ),
        SearchDocument(
            "doc015",
            "Operational Design Domain (ODD) Specification",
            "ODD defines the specific conditions under which an autonomous vehicle is designed to operate safely, including environment, weather, and traffic scenarios.",
            ["ODD", "Operational Design Domain", "Safety", "Autonomous Driving"],
            1.1
        ),
        SearchDocument(
            "doc016",
            "Functional Safety: ISO 26262 ASIL Compliance",
            "ISO 26262 defines the automotive safety integrity levels (ASIL) and processes to ensure functional safety in automotive electronic systems.",
            ["Functional Safety", "ISO 26262", "ASIL", "Automotive Safety"],
            1.5
        ),
        SearchDocument(
            "doc017",
            "Safety of Intended Functionality (SOTIF) ISO 21448",
            "SOTIF addresses hazards arising from the intended functionality of autonomous systems, complementing functional safety standards.",
            ["SOTIF", "ISO 21448", "Safety", "Autonomous Driving"],
            1.4
        ),
        SearchDocument(
            "doc018",
            "Cybersecurity in Autonomous Vehicles: ISO SAE 21434",
            "ISO SAE 21434 provides guidelines for cybersecurity risk management in automotive systems to protect against threats and vulnerabilities.",
            ["Cybersecurity", "ISO SAE 21434", "Automotive Security", "Risk Management"],
            1.5
        ),
        SearchDocument(
            "doc019",
            "Scenario-Based Simulation Testing",
            "Simulation testing using realistic driving scenarios helps validate autonomous driving systems under diverse conditions including edge and corner cases.",
            ["Simulation", "Scenario-Based Testing", "Validation", "Autonomous Driving"],
            1.3
        ),
        SearchDocument(
            "doc020",
            "Edge Case and Corner Case Handling Strategies",
            "Identifying and handling rare or extreme driving situations is critical to ensure robustness and safety of autonomous vehicles.",
            ["Edge Case", "Corner Case", "Safety", "Autonomous Driving"],
            1.4
        ),
        SearchDocument(
            "doc021",
            "Redundancy and Fail-Operational Architectures",
            "Redundant systems and fail-operational designs increase reliability and safety by allowing continued operation despite component failures.",
            ["Redundancy", "Fail-Operational", "Safety", "Architecture"],
            1.5
        ),
        SearchDocument(
            "doc022",
            "Ethical Decision Making in Autonomous Driving: The Trolley Problem",
            "Ethical frameworks guide autonomous vehicles in making decisions during unavoidable accidents, balancing harm and safety.",
            ["Ethics", "Trolley Problem", "Decision Making", "Autonomous Driving"],
            1.3
        ),
        SearchDocument(
            "doc023",
            "Regulatory Frameworks: NHTSA Guidelines",
            "The National Highway Traffic Safety Administration (NHTSA) provides regulations and guidelines for the development and deployment of autonomous vehicles.",
            ["NHTSA", "Regulations", "Autonomous Vehicles", "Safety"],
            1.4
        ),
        SearchDocument(
            "doc024",
            "UNECE WP.29 Autonomous Vehicle Regulations",
            "UNECE WP.29 develops international regulations for vehicle safety, including autonomous driving system requirements and testing.",
            ["UNECE", "WP.29", "Regulations", "Autonomous Vehicles"],
            1.4
        ),
        SearchDocument(
            "doc025",
            "Sensor Calibration and Synchronization for Fusion",
            "Accurate sensor calibration and time synchronization are essential for effective sensor fusion and perception in autonomous systems.",
            ["Sensor Calibration", "Synchronization", "Sensor Fusion", "Autonomous Driving"],
            1.2
        ),
        SearchDocument(
            "doc026",
            "Real-Time Data Processing and Edge Computing",
            "Edge computing enables real-time processing of sensor data on the vehicle, reducing latency and improving responsiveness.",
            ["Edge Computing", "Real-Time Processing", "Autonomous Driving"],
            1.1
        ),
        SearchDocument(
            "doc027",
            "Localization Techniques Using GNSS and IMU",
            "Global Navigation Satellite Systems (GNSS) combined with Inertial Measurement Units (IMU) provide robust vehicle localization.",
            ["Localization", "GNSS", "IMU", "Autonomous Driving"],
            1.3
        ),
        SearchDocument(
            "doc028",
            "Dynamic Object Classification and Behavior Prediction",
            "Classifying dynamic objects and predicting their future behavior is vital for safe path and motion planning.",
            ["Object Classification", "Behavior Prediction", "Perception", "Autonomous Driving"],
            1.3
        ),
        SearchDocument(
            "doc029",
            "High-Definition Map Updates and Maintenance",
            "Maintaining up-to-date HD maps is necessary to reflect changes in road infrastructure and support autonomous navigation.",
            ["HD Maps", "Map Updates", "Maintenance", "Autonomous Driving"],
            1.2
        ),
        SearchDocument(
            "doc030",
            "Vehicle-to-Infrastructure (V2I) Communication Protocols",
            "V2I communication enables vehicles to interact with traffic signals, road signs, and other infrastructure for enhanced safety and efficiency.",
            ["V2I", "Communication", "Infrastructure", "Autonomous Driving"],
            1.3
        ),
    ]
    for doc in docs:
        index.add_document(doc)