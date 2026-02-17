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
                # Remove old frequencies
                old_tf = self.doc_term_freqs.get(doc.id, Counter())
                for term in old_tf:
                    self.term_doc_freqs[term] -= 1
                    if self.term_doc_freqs[term] <= 0:
                        del self.term_doc_freqs[term]
                self.N -= 1
                del self.doc_term_freqs[doc.id]
                del self.doc_lengths[doc.id]
                del self.documents[doc.id]

            tokens = self._tokenize(doc.title + " " + doc.content)
            tf = Counter(tokens)
            self.doc_term_freqs[doc.id] = tf
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = sum(tf.values())
            self.N += 1

            for term in tf:
                self.term_doc_freqs[term] += 1

            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []

        idf_cache = {}
        for term in set(query_terms):
            idf_cache[term] = self._compute_idf(term)

        scores = []
        for doc_id, doc in self.documents.items():
            score = self._score_bm25(doc_id, query_terms, idf_cache)
            if score > 0:
                snippet = self._create_snippet(doc.content, query_terms)
                scores.append(SearchResult(doc_id, score * doc.weight, doc.title, snippet))

        scores.sort(key=lambda x: x.score, reverse=True)
        return scores[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "num_documents": self.N,
                "avg_doc_length": self.avg_doc_length,
                "num_terms": len(self.term_doc_freqs),
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

    def _score_bm25(self, doc_id: str, query_terms: List[str], idf_cache: Dict[str, float]) -> float:
        score = 0.0
        tf = self.doc_term_freqs.get(doc_id, Counter())
        doc_len = self.doc_lengths.get(doc_id, 0)
        avgdl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0

        for term in query_terms:
            if term not in tf or idf_cache.get(term, 0) == 0:
                continue
            f = tf[term]
            idf = idf_cache[term]
            numerator = f * (self.k1 + 1)
            denominator = f + self.k1 * (1 - self.b + self.b * doc_len / avgdl)
            score += idf * (numerator / denominator)
        return score

    def _create_snippet(self, content: str, query_terms: List[str], snippet_length: int = 160) -> str:
        content_lower = content.lower()
        positions = []
        for term in set(query_terms):
            pos = content_lower.find(term)
            if pos != -1:
                positions.append(pos)
        if not positions:
            snippet = content[:snippet_length].strip()
            if len(content) > snippet_length:
                snippet += "..."
            return snippet

        start = max(min(positions) - snippet_length // 4, 0)
        end = min(start + snippet_length, len(content))
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
            _seed_documents(_singleton_instance)
        return _singleton_instance


def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            "doc001",
            "Radial vs Bias-Ply Tire Construction",
            "Radial tires have cords arranged at 90 degrees to the direction of travel, "
            "providing better flexibility and fuel efficiency. Bias-ply tires have cords "
            "at alternating angles, offering a stiffer ride but less tread life.",
            ["construction", "radial", "bias-ply"]
        ),
        SearchDocument(
            "doc002",
            "Center Wear Pattern Analysis",
            "Center wear occurs when tires are overinflated, causing the middle tread to wear faster "
            "than the edges. Proper tire pressure maintenance prevents this uneven wear.",
            ["wear", "center", "pressure"]
        ),
        SearchDocument(
            "doc003",
            "Shoulder Wear Pattern Analysis",
            "Shoulder wear is caused by underinflation or aggressive cornering, leading to excessive "
            "wear on the tire edges. Regular pressure checks and driving habits affect shoulder wear.",
            ["wear", "shoulder", "pressure"]
        ),
        SearchDocument(
            "doc004",
            "Cupping and Scalloping Wear",
            "Cupping and scalloping are irregular wear patterns caused by suspension issues or "
            "wheel imbalance, resulting in a bumpy ride and noise.",
            ["wear", "cupping", "scalloping", "suspension", "balance"]
        ),
        SearchDocument(
            "doc005",
            "Feathering Wear Pattern",
            "Feathering is a wear pattern where tread ribs develop a sawtooth edge, often due to "
            "improper wheel alignment.",
            ["wear", "feathering", "alignment"]
        ),
        SearchDocument(
            "doc006",
            "Load Index and Speed Rating Compliance",
            "Tires must meet or exceed the vehicle's load index and speed rating to ensure safety "
            "and performance under specified conditions.",
            ["load index", "speed rating", "safety"]
        ),
        SearchDocument(
            "doc007",
            "Seasonal Tire Selection - Winter vs All-Season",
            "Winter tires provide better traction in snow and ice due to specialized rubber compounds "
            "and tread designs, while all-season tires offer balanced performance year-round.",
            ["seasonal", "winter", "all-season", "traction"]
        ),
        SearchDocument(
            "doc008",
            "Tire Pressure Monitoring System (TPMS) Function and Limitations",
            "TPMS alerts drivers to low tire pressure but may not detect slow leaks or provide exact "
            "pressure readings. Regular manual checks remain important.",
            ["tpms", "pressure", "monitoring", "limitations"]
        ),
        SearchDocument(
            "doc009",
            "Sidewall Impact Damage and Bubble Formation",
            "Impacts against curbs or potholes can cause sidewall damage and bubbles, compromising "
            "tire integrity and safety.",
            ["sidewall", "impact", "damage", "bubble"]
        ),
        SearchDocument(
            "doc010",
            "Hydroplaning Dynamics and Tread Depth Requirements",
            "Adequate tread depth is critical to channel water and prevent hydroplaning, which occurs "
            "when tires lose contact with the road surface.",
            ["hydroplaning", "tread depth", "water", "safety"]
        ),
        SearchDocument(
            "doc011",
            "Tire Age and Date Code Interpretation",
            "Tires have a DOT date code indicating manufacture week and year. Tires older than six "
            "years should be inspected regularly regardless of tread wear.",
            ["age", "date code", "dot", "inspection"]
        ),
        SearchDocument(
            "doc012",
            "Run-Flat Tire Technology and Limitations",
            "Run-flat tires allow limited driving after a puncture but have stiffer sidewalls and "
            "may affect ride comfort and repair options.",
            ["run-flat", "technology", "limitations", "puncture"]
        ),
        SearchDocument(
            "doc013",
            "Wheel Balance and Vibration Diagnosis",
            "Unbalanced wheels cause vibrations and uneven tire wear. Proper balancing improves ride "
            "comfort and tire life.",
            ["wheel", "balance", "vibration", "diagnosis"]
        ),
        SearchDocument(
            "doc014",
            "Nitrogen Inflation vs Compressed Air",
            "Nitrogen inflation reduces moisture and pressure fluctuations but offers marginal benefits "
            "over compressed air for typical passenger vehicles.",
            ["nitrogen", "inflation", "compressed air", "pressure"]
        ),
        SearchDocument(
            "doc015",
            "Tire Rotation Patterns and Intervals",
            "Regular tire rotation promotes even wear. Common patterns include front-to-back and cross "
            "rotations, typically every 5,000 to 8,000 miles.",
            ["rotation", "patterns", "intervals", "wear"]
        ),
        SearchDocument(
            "doc016",
            "Plus-Sizing and Minus-Sizing Tire Changes",
            "Plus-sizing involves increasing wheel diameter and lowering tire profile for performance, "
            "while minus-sizing increases sidewall height for comfort and off-road use.",
            ["plus-sizing", "minus-sizing", "performance", "comfort"]
        ),
        SearchDocument(
            "doc017",
            "Radial Tire Advantages and Disadvantages",
            "Radial tires offer better fuel economy and tread life but may have less sidewall stiffness "
            "compared to bias-ply tires.",
            ["radial", "advantages", "disadvantages"]
        ),
        SearchDocument(
            "doc018",
            "Bias-Ply Tire Applications and Characteristics",
            "Bias-ply tires are preferred for heavy loads and off-road due to their robust sidewalls but "
            "have higher rolling resistance.",
            ["bias-ply", "applications", "characteristics"]
        ),
        SearchDocument(
            "doc019",
            "Interpreting Tire Wear Indicators",
            "Tire wear indicators signal when tread depth is below safe limits, requiring replacement.",
            ["wear indicators", "tread depth", "replacement"]
        ),
        SearchDocument(
            "doc020",
            "Effects of Overinflation and Underinflation",
            "Overinflation causes center wear and harsher ride; underinflation causes shoulder wear and "
            "increased heat buildup.",
            ["overinflation", "underinflation", "wear", "heat"]
        ),
        SearchDocument(
            "doc021",
            "TPMS Sensor Types and Maintenance",
            "Direct TPMS uses pressure sensors inside tires; indirect TPMS relies on wheel speed sensors. "
            "Sensor battery life and calibration are maintenance considerations.",
            ["tpms", "sensor", "maintenance"]
        ),
        SearchDocument(
            "doc022",
            "Diagnosing Tire Noise Related to Wear Patterns",
            "Cupping and scalloping cause rhythmic noise; feathering may cause a rough feel. Diagnosis "
            "involves inspection and balancing.",
            ["noise", "wear patterns", "diagnosis"]
        ),
        SearchDocument(
            "doc023",
            "Impact of Wheel Alignment on Tire Wear",
            "Misalignment causes uneven wear patterns such as feathering and shoulder wear, reducing tire "
            "life and vehicle handling.",
            ["alignment", "wear", "handling"]
        ),
        SearchDocument(
            "doc024",
            "Tire Pressure Effects on Fuel Efficiency",
            "Proper tire pressure reduces rolling resistance and improves fuel economy; underinflated tires "
            "increase fuel consumption.",
            ["pressure", "fuel efficiency", "rolling resistance"]
        ),
        SearchDocument(
            "doc025",
            "Winter Tire Rubber Compounds and Tread Design",
            "Winter tires use softer rubber and specialized tread patterns to maintain flexibility and grip "
            "in cold temperatures.",
            ["winter tires", "rubber compounds", "tread design"]
        ),
        SearchDocument(
            "doc026",
            "All-Season Tire Performance Characteristics",
            "All-season tires balance wet, dry, and light snow performance but do not excel in extreme conditions.",
            ["all-season", "performance", "balance"]
        ),
        SearchDocument(
            "doc027",
            "Run-Flat Tire Repair and Replacement Guidelines",
            "Run-flat tires often require replacement after puncture; repair options are limited compared to "
            "standard tires.",
            ["run-flat", "repair", "replacement"]
        ),
        SearchDocument(
            "doc028",
            "Nitrogen Inflation Safety and Environmental Impact",
            "Nitrogen inflation reduces oxidation and moisture, potentially extending tire life and improving "
            "safety marginally.",
            ["nitrogen", "safety", "environment"]
        ),
        SearchDocument(
            "doc029",
            "Tire Rotation Effects on Vehicle Handling",
            "Regular rotation maintains balanced handling and traction, preventing uneven wear that can affect "
            "vehicle stability.",
            ["rotation", "handling", "traction"]
        ),
        SearchDocument(
            "doc030",
            "Plus-Sizing Effects on Speedometer and Suspension",
            "Changing tire size affects speedometer accuracy and suspension geometry; recalibration may be needed.",
            ["plus-sizing", "speedometer", "suspension"]
        ),
    ]

    for doc in docs:
        index.add_document(doc)