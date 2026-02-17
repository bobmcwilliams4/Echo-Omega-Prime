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
        self._documents: Dict[int, SearchDocument] = {}
        self._inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_length: float = 0.0
        self._doc_freqs: Dict[str, int] = defaultdict(int)
        self._N: int = 0
        self._lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            term_counts = Counter(tokens)
            self._documents[doc.id] = doc
            self._doc_lengths[doc.id] = len(tokens)
            for term, count in term_counts.items():
                self._inverted_index[term][doc.id] = count
                self._doc_freqs[term] += 1
            self._N += 1
            self._avg_doc_length = sum(self._doc_lengths.values()) / self._N if self._N > 0 else 0.0
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidate_docs = set()
        for term in query_terms:
            if term in self._inverted_index:
                candidate_docs.update(self._inverted_index[term].keys())
        scored_results: List[Tuple[int, float]] = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(query_terms, doc_id)
            tfidf_score = self._score_tfidf(query_terms, doc_id)
            doc = self._documents[doc_id]
            score = 0.7 * bm25_score + 0.3 * tfidf_score
            score *= doc.weight
            scored_results.append((doc_id, score))
        scored_results.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored_results[:limit]:
            doc = self._documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                "total_documents": self._N,
                "avg_doc_length": self._avg_doc_length,
                "unique_terms": len(self._doc_freqs)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self._doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self._N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc_len = self._doc_lengths.get(doc_id, 0)
        avgdl = self._avg_doc_length if self._avg_doc_length > 0 else 1.0
        doc = self._documents[doc_id]
        doc_tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
        term_counts = Counter(doc_tokens)
        for term in set(query_terms):
            if doc_id not in self._inverted_index.get(term, {}):
                continue
            f = term_counts.get(term, 0)
            idf = self._compute_idf(term)
            numerator = f * (self._bm25_k1 + 1)
            denominator = f + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / avgdl)
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        doc = self._documents[doc_id]
        doc_tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
        term_counts = Counter(doc_tokens)
        doc_len = len(doc_tokens)
        score = 0.0
        for term in set(query_terms):
            tf = term_counts.get(term, 0) / doc_len if doc_len > 0 else 0.0
            idf = self._compute_idf(term)
            score += tf * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str]) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = []
        for i, token in enumerate(tokens):
            if token in query_terms:
                positions.append(i)
        if not positions:
            snippet = content[:160]
            return snippet + "..." if len(content) > 160 else snippet
        start = max(positions[0] - 8, 0)
        end = min(positions[0] + 12, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet_text = " ".join(snippet_tokens)
        for term in set(query_terms):
            snippet_text = re.sub(rf'\b({term})\b', r'*\1*', snippet_text, flags=re.IGNORECASE)
        return snippet_text + "..."

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
            "Centrifugal Pump Specific Speed Selection",
            "Specific speed (Ns) is a dimensionless parameter used to classify centrifugal pumps based on their speed, flow, and head. Selecting the correct specific speed ensures optimal efficiency and performance.",
            ["centrifugal", "specific speed", "selection"],
            1.0
        ),
        SearchDocument(
            2,
            "NPSH Calculations and Cavitation Prevention",
            "Net Positive Suction Head (NPSH) is critical to prevent cavitation in centrifugal pumps. Calculate NPSHa and compare with NPSHr to ensure safe operation.",
            ["NPSH", "cavitation", "prevention"],
            1.0
        ),
        SearchDocument(
            3,
            "Pump Affinity Laws Explained",
            "The affinity laws relate pump speed, flow, head, and power. They are essential for predicting pump performance changes due to speed or impeller diameter variations.",
            ["affinity laws", "performance", "centrifugal"],
            1.0
        ),
        SearchDocument(
            4,
            "Pump Curve Analysis and Operating Point Determination",
            "Pump curves show the relationship between flow rate and head. The operating point is where the pump curve intersects the system curve, determining actual flow and head.",
            ["pump curve", "operating point", "analysis"],
            1.0
        ),
        SearchDocument(
            5,
            "Positive Displacement Pump Selection: Reciprocating vs Rotary",
            "Positive displacement pumps are classified as reciprocating or rotary. Selection depends on fluid properties, required flow, and pressure.",
            ["positive displacement", "reciprocating", "rotary"],
            1.0
        ),
        SearchDocument(
            6,
            "Pump Materials Selection and Metallurgy",
            "Selecting the right pump material is vital for corrosion resistance and mechanical integrity. Common materials include stainless steel, cast iron, and special alloys.",
            ["materials", "metallurgy", "corrosion"],
            1.0
        ),
        SearchDocument(
            7,
            "Mechanical Seal Selection and Flush Plans",
            "Mechanical seals prevent leakage in pumps. Selecting the appropriate seal and flush plan depends on process fluid, temperature, and pressure.",
            ["mechanical seal", "flush plan", "leakage"],
            1.0
        ),
        SearchDocument(
            8,
            "Pump Bearing Selection: Radial vs Thrust Loads",
            "Bearings support pump shafts and manage radial and thrust loads. Proper selection extends pump life and reduces maintenance.",
            ["bearing", "radial load", "thrust load"],
            1.0
        ),
        SearchDocument(
            9,
            "Pump Vibration Analysis and Diagnostics",
            "Vibration analysis helps diagnose pump issues such as imbalance, misalignment, or bearing failure. Regular monitoring prevents unexpected downtime.",
            ["vibration", "diagnostics", "analysis"],
            1.0
        ),
        SearchDocument(
            10,
            "API 610 Centrifugal Pump Standard Compliance",
            "API 610 sets requirements for centrifugal pumps in petroleum, petrochemical, and gas industries. Compliance ensures reliability and safety.",
            ["API 610", "standard", "compliance"],
            1.0
        ),
        SearchDocument(
            11,
            "Pump Alignment Methods: Laser vs Reverse Indicator",
            "Proper alignment reduces vibration and wear. Laser alignment offers higher accuracy compared to traditional reverse indicator methods.",
            ["alignment", "laser", "reverse indicator"],
            1.0
        ),
        SearchDocument(
            12,
            "Variable Speed Drives for Pump Energy Savings",
            "Variable speed drives (VSDs) adjust pump speed to match system demand, reducing energy consumption and extending equipment life.",
            ["variable speed drive", "energy savings", "VSD"],
            1.0
        ),
        SearchDocument(
            13,
            "Multistage Pump Design and Application",
            "Multistage pumps use multiple impellers to achieve higher pressures. They are ideal for boiler feedwater, reverse osmosis, and high-head applications.",
            ["multistage", "design", "application"],
            1.0
        ),
        SearchDocument(
            14,
            "Slurry Pump Design and Abrasive Wear Considerations",
            "Slurry pumps handle abrasive fluids. Design features include robust materials, replaceable liners, and large clearances to minimize wear.",
            ["slurry", "abrasive wear", "design"],
            1.0
        ),
        SearchDocument(
            15,
            "Centrifugal Pump Performance Curves",
            "Performance curves illustrate pump characteristics such as flow, head, efficiency, and power consumption across operating conditions.",
            ["performance curve", "centrifugal", "characteristics"],
            1.0
        ),
        SearchDocument(
            16,
            "Pump System Curve Development",
            "System curves represent the relationship between flow and head loss in the piping system. They are essential for proper pump selection.",
            ["system curve", "head loss", "piping"],
            1.0
        ),
        SearchDocument(
            17,
            "Reciprocating Pump Types and Applications",
            "Reciprocating pumps include piston, plunger, and diaphragm types. They are used for high-pressure, low-flow applications.",
            ["reciprocating", "piston", "diaphragm"],
            1.0
        ),
        SearchDocument(
            18,
            "Rotary Pump Types: Gear, Vane, and Screw",
            "Rotary pumps provide smooth flow and are suitable for viscous fluids. Common types are gear, vane, and screw pumps.",
            ["rotary", "gear", "vane", "screw"],
            1.0
        ),
        SearchDocument(
            19,
            "Pump Suction Piping Design Guidelines",
            "Proper suction piping design prevents cavitation and ensures stable pump operation. Guidelines include minimizing elbows and maintaining adequate submergence.",
            ["suction piping", "design", "cavitation"],
            1.0
        ),
        SearchDocument(
            20,
            "Pump Impeller Types and Selection",
            "Impeller type affects pump performance and suitability for different fluids. Types include open, semi-open, and closed impellers.",
            ["impeller", "selection", "performance"],
            1.0
        ),
        SearchDocument(
            21,
            "Pump Troubleshooting: Common Failures",
            "Common pump failures include seal leakage, bearing failure, and cavitation. Systematic troubleshooting minimizes downtime.",
            ["troubleshooting", "failure", "maintenance"],
            1.0
        ),
        SearchDocument(
            22,
            "API 682 Mechanical Seal Plans",
            "API 682 standardizes mechanical seal flush plans for centrifugal and rotary pumps, improving reliability and safety.",
            ["API 682", "mechanical seal", "flush plan"],
            1.0
        ),
        SearchDocument(
            23,
            "Pump Efficiency Optimization Techniques",
            "Efficiency can be improved by proper selection, regular maintenance, and system optimization. Monitoring performance helps identify improvement areas.",
            ["efficiency", "optimization", "maintenance"],
            1.0
        ),
        SearchDocument(
            24,
            "Pump Start-Up and Commissioning Checklist",
            "A thorough start-up checklist includes alignment, lubrication, priming, and verification of operating parameters to ensure safe commissioning.",
            ["start-up", "commissioning", "checklist"],
            1.0
        ),
        SearchDocument(
            25,
            "Pump Maintenance Best Practices",
            "Best practices include routine inspection, vibration monitoring, lubrication, and timely replacement of wear parts.",
            ["maintenance", "inspection", "vibration"],
            1.0
        ),
        SearchDocument(
            26,
            "Corrosion Mechanisms in Pump Materials",
            "Understanding corrosion mechanisms such as pitting, crevice, and galvanic corrosion is essential for selecting pump materials.",
            ["corrosion", "materials", "mechanisms"],
            1.0
        ),
        SearchDocument(
            27,
            "Pump System Energy Audits",
            "Energy audits identify inefficiencies in pump systems, enabling targeted improvements and cost savings.",
            ["energy audit", "system", "efficiency"],
            1.0
        ),
        SearchDocument(
            28,
            "Pump Noise Diagnostics",
            "Unusual noise in pumps can indicate cavitation, bearing failure, or misalignment. Diagnostics help prevent catastrophic failures.",
            ["noise", "diagnostics", "cavitation"],
            1.0
        ),
        SearchDocument(
            29,
            "Pump Shaft Alignment Tolerances",
            "Adhering to alignment tolerances reduces vibration and extends bearing and seal life.",
            ["shaft alignment", "tolerances", "vibration"],
            1.0
        ),
        SearchDocument(
            30,
            "Pump Control Strategies",
            "Control strategies include on/off, throttling, and variable speed operation to match process requirements.",
            ["control", "throttling", "variable speed"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)