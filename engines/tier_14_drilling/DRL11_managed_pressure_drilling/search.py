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
        self.documents: Dict[int, SearchDocument] = {}
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

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
                self.inverted_index[term][doc.id] = freq
                self.doc_freqs[term] += 1
            self._idf_cache.clear()
            self._update_avg_doc_length()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, {}).keys())
        scores = {}
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(query_terms, doc_id)
            tfidf_score = self._score_tfidf(query_terms, doc_id)
            doc_weight = self.documents[doc_id].weight
            final_score = 0.7 * bm25_score + 0.3 * tfidf_score
            final_score *= doc_weight
            scores[doc_id] = final_score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "total_docs": self.total_docs,
                "avg_doc_length": self.avg_doc_length,
                "unique_terms": len(self.inverted_index)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9\-]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in set(query_terms):
            f = self.inverted_index.get(term, {}).get(doc_id, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / (self.avg_doc_length or 1))
            score += idf * (f * (self._bm25_k1 + 1)) / (denom + 1e-9)
        return score

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tfidf = 0.0
        doc_len = self.doc_lengths[doc_id]
        term_counts = self.inverted_index
        for term in set(query_terms):
            tf = term_counts.get(term, {}).get(doc_id, 0)
            if tf == 0:
                continue
            tf_norm = tf / (doc_len or 1)
            idf = self._compute_idf(term)
            tfidf += tf_norm * idf
        return tfidf

    def _update_avg_doc_length(self):
        if self.total_docs == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str]) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:160] + "..." if len(content) > 160 else content
        start = max(positions[0] - 5, 0)
        end = min(positions[0] + 10, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(r'\b({})\b'.format(re.escape(term)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + "..."

__search_index_instance: Optional[SearchIndex] = None
__search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global __search_index_instance
    if __search_index_instance is None:
        with __search_index_lock:
            if __search_index_instance is None:
                __search_index_instance = SearchIndex()
                _seed_documents(__search_index_instance)
    return __search_index_instance

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "CBHP MPD Fundamental Principle",
            "Constant Bottom Hole Pressure (CBHP) Managed Pressure Drilling maintains a constant pressure at the bottom hole by adjusting surface backpressure and mud weight. This enables drilling within narrow pressure windows and minimizes influx or losses.",
            ["CBHP", "MPD", "Fundamental", "Pressure"],
            1.0
        ),
        SearchDocument(
            2,
            "RCD Selection and Rating Criteria",
            "Rotating Control Devices (RCDs) are selected based on pressure rating, bearing type, sealing element material, and compatibility with drilling fluids. Proper RCD selection is critical for safe MPD operations.",
            ["RCD", "Selection", "Rating", "MPD"],
            1.0
        ),
        SearchDocument(
            3,
            "Pressurized Mud Cap Drilling (PMCD) for Total Losses",
            "PMCD is an MPD variant used when total losses are encountered. The annulus is filled with a light fluid and mud is pumped down the drill pipe, allowing continued drilling despite loss zones.",
            ["PMCD", "Total Losses", "MPD", "Drilling"],
            1.0
        ),
        SearchDocument(
            4,
            "Dual Gradient Drilling - Subsea Mudlift System",
            "Dual Gradient Drilling (DGD) employs a subsea mudlift pump to reduce bottom hole pressure, enabling drilling in deepwater environments with narrow margins between pore and fracture pressures.",
            ["DGD", "Subsea", "Mudlift", "Dual Gradient"],
            1.0
        ),
        SearchDocument(
            5,
            "Automated Choke Control - PID Loop Tuning",
            "Automated choke control systems use PID controllers to maintain setpoint pressures. Proper tuning of proportional, integral, and derivative parameters is essential for stable MPD operations.",
            ["Choke", "PID", "Automation", "MPD"],
            1.0
        ),
        SearchDocument(
            6,
            "Narrow Margin Drilling - Pore Pressure to Frac Gradient",
            "Narrow margin drilling requires precise control between pore pressure and fracture gradient. MPD techniques allow for dynamic adjustment of mud weight and backpressure to stay within safe limits.",
            ["Narrow Margin", "Pore Pressure", "Frac Gradient", "MPD"],
            1.0
        ),
        SearchDocument(
            7,
            "Kick Detection Sensitivity in MPD Operations",
            "Kick detection in MPD relies on high-resolution flow and pressure sensors. Enhanced sensitivity allows for early influx detection, reducing the risk of well control incidents.",
            ["Kick Detection", "MPD", "Sensitivity", "Well Control"],
            1.0
        ),
        SearchDocument(
            8,
            "IADC MPD Classification - Reactive vs Proactive",
            "The IADC classifies MPD into reactive and proactive techniques. Reactive MPD responds to influxes, while proactive MPD continuously manages wellbore pressures to prevent kicks.",
            ["IADC", "MPD", "Classification", "Reactive", "Proactive"],
            1.0
        ),
        SearchDocument(
            9,
            "MPD Well Design - Casing Shoe Depth Optimization",
            "Optimizing casing shoe depth in MPD well design ensures sufficient shoe integrity and maximizes open hole exposure while maintaining well control.",
            ["MPD", "Well Design", "Casing Shoe", "Optimization"],
            1.0
        ),
        SearchDocument(
            10,
            "CBHP Implementation Steps",
            "CBHP implementation involves determining the required bottom hole pressure, selecting appropriate equipment, and calibrating the choke system for real-time adjustments.",
            ["CBHP", "Implementation", "Choke", "Pressure"],
            1.0
        ),
        SearchDocument(
            11,
            "RCD Bearing Types and Maintenance",
            "RCDs may use either mud-lubricated or sealed bearings. Regular maintenance and inspection are required to ensure RCD reliability during MPD operations.",
            ["RCD", "Bearings", "Maintenance", "MPD"],
            1.0
        ),
        SearchDocument(
            12,
            "PMCD Annular Fluid Selection",
            "In PMCD, the annulus is filled with a light fluid such as seawater or base oil. The selection depends on compatibility with formation fluids and operational safety.",
            ["PMCD", "Annular Fluid", "Selection", "MPD"],
            1.0
        ),
        SearchDocument(
            13,
            "Subsea Mudlift Pump Design Considerations",
            "Subsea mudlift pumps must be designed for high reliability, corrosion resistance, and compatibility with drilling fluids. Their operation is critical for dual gradient drilling.",
            ["Subsea", "Mudlift", "Pump", "Design"],
            1.0
        ),
        SearchDocument(
            14,
            "PID Controller Tuning Methods",
            "PID tuning methods include Ziegler-Nichols, Cohen-Coon, and trial-and-error. Proper tuning ensures the choke responds quickly without oscillation.",
            ["PID", "Tuning", "Choke", "MPD"],
            1.0
        ),
        SearchDocument(
            15,
            "Drilling Window Management in Narrow Margins",
            "Drilling window management involves monitoring ECD, adjusting mud weight, and using real-time data to avoid exceeding pore or fracture pressures.",
            ["Drilling Window", "Narrow Margin", "ECD", "MPD"],
            1.0
        ),
        SearchDocument(
            16,
            "Kick Detection Technologies",
            "Technologies for kick detection include Coriolis flow meters, differential pressure sensors, and real-time data analytics for anomaly detection.",
            ["Kick Detection", "Technology", "MPD", "Sensors"],
            1.0
        ),
        SearchDocument(
            17,
            "Reactive MPD Techniques",
            "Reactive MPD techniques involve adjusting surface backpressure or mud weight in response to detected influxes or losses.",
            ["Reactive", "MPD", "Techniques", "Backpressure"],
            1.0
        ),
        SearchDocument(
            18,
            "Proactive MPD Approaches",
            "Proactive MPD maintains wellbore pressure within a narrow window at all times, using automated control systems and predictive modeling.",
            ["Proactive", "MPD", "Control", "Modeling"],
            1.0
        ),
        SearchDocument(
            19,
            "Casing Design for MPD Wells",
            "Casing design in MPD wells must account for anticipated pressure regimes, shoe strength, and contingency for pressure control equipment.",
            ["Casing", "Design", "MPD", "Pressure"],
            1.0
        ),
        SearchDocument(
            20,
            "CBHP vs PMCD - Application Criteria",
            "CBHP is preferred when partial losses are manageable, while PMCD is used for total loss scenarios where annular returns cannot be maintained.",
            ["CBHP", "PMCD", "Application", "Criteria"],
            1.0
        ),
        SearchDocument(
            21,
            "RCD Pressure Rating Standards",
            "RCDs are rated according to API and manufacturer standards. Selection must consider maximum anticipated surface pressure during MPD.",
            ["RCD", "Pressure Rating", "Standards", "MPD"],
            1.0
        ),
        SearchDocument(
            22,
            "PMCD Operational Sequence",
            "PMCD operations begin with isolating the loss zone, filling the annulus with light fluid, and pumping mud down the drill pipe while monitoring well response.",
            ["PMCD", "Operation", "Sequence", "MPD"],
            1.0
        ),
        SearchDocument(
            23,
            "Dual Gradient Drilling Benefits",
            "DGD allows for deeper casing setting, reduced mud weights, and improved wellbore stability in deepwater environments.",
            ["Dual Gradient", "Drilling", "Benefits", "DGD"],
            1.0
        ),
        SearchDocument(
            24,
            "Automated Choke System Components",
            "Automated choke systems include sensors, controllers, actuators, and human-machine interfaces for precise pressure regulation.",
            ["Choke", "Automation", "System", "MPD"],
            1.0
        ),
        SearchDocument(
            25,
            "Narrow Margin Drilling Challenges",
            "Challenges in narrow margin drilling include rapid pressure fluctuations, limited mud weight flexibility, and increased risk of kicks or losses.",
            ["Narrow Margin", "Drilling", "Challenges", "MPD"],
            1.0
        ),
        SearchDocument(
            26,
            "Advanced Kick Detection Algorithms",
            "Machine learning algorithms are increasingly used to improve kick detection sensitivity and reduce false positives in MPD operations.",
            ["Kick Detection", "Algorithms", "Machine Learning", "MPD"],
            1.0
        ),
        SearchDocument(
            27,
            "IADC MPD Classification Overview",
            "The IADC MPD classification system defines the boundaries between managed pressure, underbalanced, and conventional drilling techniques.",
            ["IADC", "MPD", "Classification", "Overview"],
            1.0
        ),
        SearchDocument(
            28,
            "Casing Shoe Depth Optimization Methods",
            "Casing shoe depth optimization uses formation pressure data, offset well analysis, and simulation to maximize drilling efficiency and safety.",
            ["Casing Shoe", "Optimization", "MPD", "Well Design"],
            1.0
        ),
        SearchDocument(
            29,
            "CBHP Real-Time Monitoring",
            "Real-time monitoring of bottom hole pressure is essential for CBHP. Data from downhole sensors is integrated with surface control systems.",
            ["CBHP", "Monitoring", "Real-Time", "Sensors"],
            1.0
        ),
        SearchDocument(
            30,
            "PMCD Limitations and Risks",
            "PMCD is not suitable for wells with significant gas influx risk. Risks include uncontrolled migration of light fluids and loss of well control.",
            ["PMCD", "Limitations", "Risks", "MPD"],
            1.0
        ),
        SearchDocument(
            31,
            "Dual Gradient Drilling Equipment",
            "Key DGD equipment includes subsea mudlift pumps, riserless mud return lines, and pressure control manifolds.",
            ["Dual Gradient", "Equipment", "DGD", "MPD"],
            1.0
        ),
        SearchDocument(
            32,
            "PID Loop Stability in Choke Control",
            "Loop stability in automated choke control is achieved by minimizing phase lag and ensuring fast response to pressure deviations.",
            ["PID", "Loop Stability", "Choke", "MPD"],
            1.0
        ),
        SearchDocument(
            33,
            "Narrow Margin Drilling Case Study",
            "A North Sea well successfully drilled a 50-meter section with a 0.2 ppg margin using CBHP and automated choke control.",
            ["Narrow Margin", "Case Study", "CBHP", "MPD"],
            1.0
        ),
        SearchDocument(
            34,
            "Kick Detection Response Protocols",
            "Upon kick detection, MPD protocols include isolating the well, increasing backpressure, and circulating out the influx safely.",
            ["Kick Detection", "Response", "MPD", "Protocol"],
            1.0
        ),
        SearchDocument(
            35,
            "IADC Proactive MPD Examples",
            "Examples of proactive MPD include continuous backpressure management and automated influx detection systems.",
            ["IADC", "Proactive", "MPD", "Examples"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)