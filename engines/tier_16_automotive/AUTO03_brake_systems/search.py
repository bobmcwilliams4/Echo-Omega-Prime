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
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
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
                del self.doc_term_freqs[doc.id]
                del self.doc_lengths[doc.id]
                self.N -= 1
                del self.documents[doc.id]

            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            tf = Counter(tokens)
            self.doc_term_freqs[doc.id] = tf
            for term in tf.keys():
                self.term_doc_freqs[term] += 1
            doc_len = sum(tf.values())
            self.doc_lengths[doc.id] = doc_len
            self.documents[doc.id] = doc
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []

        idf = {term: self._compute_idf(term) for term in query_terms}
        scores: Dict[str, float] = defaultdict(float)

        for doc_id, tf in self.doc_term_freqs.items():
            score = self._score_bm25(tf, idf, query_terms, self.doc_lengths[doc_id])
            if score > 0:
                scores[doc_id] = score * self.documents[doc_id].weight

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
                "total_documents": self.N,
                "average_document_length": self.avg_doc_length,
                "unique_terms": len(self.term_doc_freqs),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        df = self.term_doc_freqs.get(term, 0)
        if df == 0:
            return 0.0
        return math.log(1 + (self.N - df + 0.5) / (df + 0.5))

    def _score_bm25(self, tf: Counter, idf: Dict[str, float], query_terms: List[str], doc_len: int) -> float:
        score = 0.0
        for term in query_terms:
            freq = tf.get(term, 0)
            if freq == 0:
                continue
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf.get(term, 0.0) * numerator / denominator
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
                start = idx + len(term)
        if not positions:
            snippet = content[:snippet_length].strip()
            if len(content) > snippet_length:
                snippet += "..."
            return snippet

        positions.sort()
        start_pos = max(positions[0] - snippet_length // 4, 0)
        end_pos = start_pos + snippet_length
        if end_pos > len(content):
            end_pos = len(content)
            start_pos = max(end_pos - snippet_length, 0)
        snippet = content[start_pos:end_pos].strip()
        if start_pos > 0:
            snippet = "..." + snippet
        if end_pos < len(content):
            snippet = snippet + "..."
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
            "doc001",
            "Dual Diagonal Split Hydraulic Brake Circuit Design",
            "The dual diagonal split brake circuit divides the hydraulic system into two circuits, each controlling one front and the opposite rear wheel, enhancing safety and redundancy.",
            ["hydraulic", "brake circuit", "dual diagonal split", "safety"],
            1.2
        ),
        SearchDocument(
            "doc002",
            "Disc Brake Caliper Piston and Pad Analysis",
            "Analysis of disc brake caliper pistons includes piston diameter, number, and material to ensure optimal pad force distribution and heat dissipation.",
            ["disc brake", "caliper piston", "pad analysis", "force distribution"],
            1.1
        ),
        SearchDocument(
            "doc003",
            "Drum Brake Leading and Trailing Shoe Adjustment",
            "Proper adjustment of leading and trailing shoes in drum brakes is critical for uniform wear and effective braking performance.",
            ["drum brake", "shoe adjustment", "leading shoe", "trailing shoe"],
            1.0
        ),
        SearchDocument(
            "doc004",
            "ABS Anti-lock Braking System Wheel Speed Sensors",
            "Wheel speed sensors in ABS detect wheel rotation speed and send signals to the ECU to prevent wheel lockup during braking.",
            ["ABS", "anti-lock braking system", "wheel speed sensors", "ECU"],
            1.3
        ),
        SearchDocument(
            "doc005",
            "EBD Electronic Brakeforce Distribution",
            "EBD optimizes brakeforce between front and rear wheels based on load and road conditions to improve vehicle stability.",
            ["EBD", "electronic brakeforce distribution", "brakeforce", "stability"],
            1.2
        ),
        SearchDocument(
            "doc006",
            "ESC Electronic Stability Control: Yaw Rate and Lateral Acceleration",
            "ESC systems use yaw rate and lateral acceleration sensors to detect and correct vehicle skidding by modulating brakes and engine torque.",
            ["ESC", "electronic stability control", "yaw rate", "lateral acceleration"],
            1.3
        ),
        SearchDocument(
            "doc007",
            "Brake Fluid DOT Specifications and Boiling Point",
            "Brake fluids must meet DOT specifications including minimum boiling points to ensure performance under high temperature conditions.",
            ["brake fluid", "DOT specifications", "boiling point", "performance"],
            1.0
        ),
        SearchDocument(
            "doc008",
            "Master Cylinder Bore Ratio and Pedal Feel",
            "The master cylinder bore size affects hydraulic pressure and pedal travel, influencing brake pedal feel and responsiveness.",
            ["master cylinder", "bore ratio", "pedal feel", "hydraulic pressure"],
            1.1
        ),
        SearchDocument(
            "doc009",
            "Brake Pad Friction Coefficient (Mu) and Material Selection",
            "Brake pad materials are selected based on friction coefficient, wear rate, and thermal stability to optimize braking performance.",
            ["brake pad", "friction coefficient", "material selection", "wear rate"],
            1.2
        ),
        SearchDocument(
            "doc010",
            "Brake Rotor Thermal Analysis and Warping",
            "Thermal analysis of brake rotors helps predict warping and cracking due to uneven heat distribution during braking.",
            ["brake rotor", "thermal analysis", "warping", "heat distribution"],
            1.1
        ),
        SearchDocument(
            "doc011",
            "Vacuum Brake Booster and Assist Ratio",
            "Vacuum brake boosters amplify pedal force using engine vacuum, improving braking effort and driver comfort.",
            ["vacuum brake booster", "assist ratio", "pedal force", "engine vacuum"],
            1.0
        ),
        SearchDocument(
            "doc012",
            "Brake Line Routing and Flare Fitting Integrity",
            "Proper routing and flare fitting integrity of brake lines prevent leaks and ensure consistent hydraulic pressure.",
            ["brake line", "routing", "flare fitting", "hydraulic pressure"],
            1.0
        ),
        SearchDocument(
            "doc013",
            "Parking Brake Cable and Drum Mechanism",
            "The parking brake cable actuates the drum brake mechanism to hold the vehicle stationary when parked.",
            ["parking brake", "cable", "drum mechanism", "vehicle hold"],
            1.0
        ),
        SearchDocument(
            "doc014",
            "Brake Proportioning Valve and Bias Calibration",
            "Proportioning valves adjust brakeforce bias between front and rear wheels to prevent rear wheel lockup under heavy braking.",
            ["proportioning valve", "bias calibration", "brakeforce", "wheel lockup"],
            1.1
        ),
        SearchDocument(
            "doc015",
            "Regenerative Braking and Energy Recovery Integration",
            "Regenerative braking systems recover kinetic energy during deceleration, converting it into electrical energy to recharge batteries.",
            ["regenerative braking", "energy recovery", "deceleration", "battery recharge"],
            1.3
        ),
        SearchDocument(
            "doc016",
            "Brake-by-Wire Electromechanical Systems",
            "Brake-by-wire systems replace hydraulic linkages with electronic controls for faster response and integration with driver assistance systems.",
            ["brake-by-wire", "electromechanical", "electronic controls", "driver assistance"],
            1.4
        ),
        SearchDocument(
            "doc017",
            "Brake Noise, Vibration, and Harshness (NVH) Control",
            "NVH control techniques reduce brake squeal, vibration, and harshness through material selection and damping methods.",
            ["brake noise", "vibration", "harshness", "NVH control"],
            1.0
        ),
        SearchDocument(
            "doc018",
            "FMVSS 135 Brake Performance Standards",
            "FMVSS 135 specifies minimum brake performance requirements for passenger cars to ensure safety and reliability.",
            ["FMVSS 135", "brake performance", "standards", "safety"],
            1.2
        ),
        SearchDocument(
            "doc019",
            "Brake Fade and Thermal Recovery",
            "Brake fade occurs when excessive heat reduces friction; thermal recovery strategies include cooling and material selection.",
            ["brake fade", "thermal recovery", "heat", "friction"],
            1.1
        ),
        SearchDocument(
            "doc020",
            "Brake Wear Sensor and Indicator Systems",
            "Brake wear sensors monitor pad thickness and alert drivers when replacement is necessary to maintain safety.",
            ["brake wear sensor", "indicator system", "pad thickness", "safety"],
            1.0
        ),
        SearchDocument(
            "doc021",
            "Hydraulic Brake Circuit Redundancy and Safety",
            "Redundancy in hydraulic brake circuits ensures braking capability even if one circuit fails, enhancing vehicle safety.",
            ["hydraulic brake", "redundancy", "safety", "circuit failure"],
            1.2
        ),
        SearchDocument(
            "doc022",
            "Brake Pedal Travel and Force Relationship",
            "The relationship between pedal travel and force affects driver feedback and braking performance.",
            ["brake pedal", "travel", "force", "driver feedback"],
            1.0
        ),
        SearchDocument(
            "doc023",
            "Brake Fluid Moisture Contamination Effects",
            "Moisture contamination in brake fluid lowers boiling point and can cause vapor lock, reducing braking efficiency.",
            ["brake fluid", "moisture contamination", "boiling point", "vapor lock"],
            1.1
        ),
        SearchDocument(
            "doc024",
            "Disc Brake Pad Bedding and Break-in Procedures",
            "Proper bedding of disc brake pads ensures optimal friction and longevity by conditioning the pad and rotor surfaces.",
            ["disc brake", "pad bedding", "break-in", "friction"],
            1.0
        ),
        SearchDocument(
            "doc025",
            "Brake System Diagnostics and Fault Detection",
            "Advanced diagnostics detect faults in brake systems including sensor failures, hydraulic leaks, and electronic malfunctions.",
            ["brake system", "diagnostics", "fault detection", "sensor failure"],
            1.3
        ),
        SearchDocument(
            "doc026",
            "Thermal Expansion Effects on Brake Rotor Clearance",
            "Thermal expansion of brake rotors affects pad clearance and can cause drag or noise if not properly accounted for.",
            ["thermal expansion", "brake rotor", "clearance", "noise"],
            1.0
        ),
        SearchDocument(
            "doc027",
            "Brake Booster Vacuum Source and Performance",
            "The vacuum source for brake boosters impacts assist performance and pedal feel under various engine conditions.",
            ["brake booster", "vacuum source", "assist performance", "pedal feel"],
            1.0
        ),
        SearchDocument(
            "doc028",
            "Electronic Brakeforce Distribution Algorithms",
            "EBD algorithms dynamically adjust brakeforce based on sensor inputs to maximize braking efficiency and vehicle control.",
            ["EBD", "algorithms", "brakeforce", "sensor inputs"],
            1.2
        ),
        SearchDocument(
            "doc029",
            "Brake Line Material Selection and Corrosion Resistance",
            "Selecting brake line materials with high corrosion resistance ensures long-term reliability and safety.",
            ["brake line", "material selection", "corrosion resistance", "reliability"],
            1.0
        ),
        SearchDocument(
            "doc030",
            "Parking Brake System Integration with ABS and ESC",
            "Integration of parking brake systems with ABS and ESC enhances vehicle stability and safety during parking and emergency braking.",
            ["parking brake", "ABS", "ESC", "integration"],
            1.1
        ),
    ]

    for doc in docs:
        index.add_document(doc)