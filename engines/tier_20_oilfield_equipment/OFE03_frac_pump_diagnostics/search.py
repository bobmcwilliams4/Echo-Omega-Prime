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
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._recompute_stats = True

    def add_document(self, doc: SearchDocument):
        with self.lock:
            tokens = self._tokenize(doc.title + ' ' + doc.content + ' ' + ' '.join(doc.tags))
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            self.documents[doc.id] = doc
            for term in tf:
                self.doc_freqs[term] += 1
            self.N += 1
            self._recompute_stats = True

    def _recompute_avg_doc_length(self):
        if self.N == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N

    def _tokenize(self, text: str) -> List[str]:
        # Lowercase, remove non-alphanumeric, split on whitespace
        tokens = re.findall(r'\b[a-z0-9]+\b', text.lower())
        return tokens

    def _compute_idf(self, term: str) -> float:
        # BM25 IDF
        if term in self.idf_cache:
            return self.idf_cache[term]
        n_q = self.doc_freqs.get(term, 0)
        if n_q == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - n_q + 0.5) / (n_q + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * freq * (self.k1 + 1) / denom
        return score * self.documents[doc_id].weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            tf_norm = tf[term] / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        with self.lock:
            if self._recompute_stats:
                self._recompute_avg_doc_length()
                self.idf_cache.clear()
                self._recompute_stats = False
            query_terms = self._tokenize(query)
            if not query_terms:
                return []
            doc_scores: Dict[int, float] = {}
            for doc_id in self.documents:
                bm25_score = self._score_bm25(query_terms, doc_id)
                tfidf_score = self._score_tfidf(query_terms, doc_id)
                # Weighted sum: BM25 (0.7), TF-IDF (0.3)
                score = 0.7 * bm25_score + 0.3 * tfidf_score
                if score > 0:
                    doc_scores[doc_id] = score
            ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
            results = []
            for doc_id, score in ranked:
                doc = self.documents[doc_id]
                snippet = self._make_snippet(doc, query_terms)
                results.append(SearchResult(doc_id, score, doc.title, snippet))
            return results

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], maxlen: int = 180) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if positions:
            start = max(positions[0] - 5, 0)
            end = min(start + 30, len(tokens))
            snippet_tokens = tokens[start:end]
            snippet = ' '.join(snippet_tokens)
        else:
            snippet = content[:maxlen]
        # Highlight terms
        for term in set(query_terms):
            snippet = re.sub(rf'\b({term})\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                'num_documents': self.N,
                'avg_doc_length': self.avg_doc_length,
                'unique_terms': len(self.doc_freqs)
            }

# Singleton factory
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            idx = SearchIndex()
            _seed_documents(idx)
            _search_index_instance = idx
        return _search_index_instance

def _seed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Plunger Wear Patterns in Quintuplex Pumps",
            "Analysis of plunger wear in quintuplex pumps reveals common failure modes such as scoring, pitting, and ovality. Regular inspection and dimensional checks are critical for early detection.",
            ["plunger", "wear", "quintuplex", "failure analysis"],
            1.0
        ),
        SearchDocument(
            2,
            "Fluid End Crack Detection Techniques",
            "Non-destructive testing (NDT) methods such as magnetic particle inspection and dye penetrant are used to detect cracks in fluid ends. Early crack detection prevents catastrophic failures.",
            ["fluid end", "crack detection", "NDT", "inspection"],
            1.0
        ),
        SearchDocument(
            3,
            "Power End Bearing Failure Analysis",
            "Bearings in the power end are prone to spalling, overheating, and lubrication breakdown. Vibration analysis and oil sampling are recommended for predictive maintenance.",
            ["power end", "bearing", "failure analysis", "maintenance"],
            1.0
        ),
        SearchDocument(
            4,
            "Discharge Valve Inspection Procedures",
            "Routine inspection of discharge valves includes checking for seat erosion, spring fatigue, and proper sealing. Failure modes include leakage and loss of pressure control.",
            ["discharge valve", "inspection", "failure modes"],
            1.0
        ),
        SearchDocument(
            5,
            "Treating Iron Integrity: Hammer Unions and Swivels",
            "Hammer unions and swivels must be inspected for thread wear, deformation, and seal integrity. Regular pressure testing ensures treating iron reliability.",
            ["treating iron", "hammer unions", "swivels", "inspection"],
            1.0
        ),
        SearchDocument(
            6,
            "Pump Rate Optimization Strategies",
            "Optimizing pump rate improves efficiency and reduces wear. SCADA integration enables real-time adjustments based on pressure and flow data.",
            ["pump rate", "optimization", "efficiency", "SCADA"],
            1.0
        ),
        SearchDocument(
            7,
            "Suction Valve Cavitation Damage",
            "Cavitation in suction valves leads to pitting and material loss. Proper NPSH and flow control are essential to minimize cavitation damage.",
            ["suction valve", "cavitation", "damage", "NPSH"],
            1.0
        ),
        SearchDocument(
            8,
            "Cold Weather Pump Operations",
            "Freeze protection for pumps includes heat tracing, insulation, and glycol circulation. Cold weather increases risk of plunger and fluid end failures.",
            ["cold weather", "pump operations", "freeze protection"],
            1.0
        ),
        SearchDocument(
            9,
            "Proppant Erosion and Wear Mitigation",
            "High proppant concentrations accelerate erosion in fluid ends and valves. Hardfacing and material upgrades extend component life.",
            ["proppant", "erosion", "wear mitigation", "fluid end"],
            1.0
        ),
        SearchDocument(
            10,
            "Chemical Compatibility and Fluid End Corrosion",
            "Incompatible chemicals can cause rapid corrosion of fluid ends. Material selection and regular chemical analysis are vital for corrosion prevention.",
            ["chemical compatibility", "corrosion", "fluid end"],
            1.0
        ),
        SearchDocument(
            11,
            "Pressure Relief Valve Sizing and Testing",
            "Correct sizing and routine testing of pressure relief valves prevent overpressure incidents. Set pressure must match system requirements.",
            ["pressure relief valve", "sizing", "testing"],
            1.0
        ),
        SearchDocument(
            12,
            "Real-Time Pump Monitoring with SCADA",
            "SCADA systems provide real-time monitoring of pump parameters including pressure, temperature, and vibration. Early anomaly detection reduces downtime.",
            ["SCADA", "real-time monitoring", "pumps"],
            1.0
        ),
        SearchDocument(
            13,
            "Pump Fleet Management Best Practices",
            "Effective fleet management involves tracking pump usage, maintenance schedules, and deployment optimization to maximize asset utilization.",
            ["fleet management", "deployment", "optimization"],
            1.0
        ),
        SearchDocument(
            14,
            "NDT Methods for Fluid End Inspection",
            "Ultrasonic and eddy current testing are advanced NDT methods for detecting subsurface cracks in fluid ends.",
            ["NDT", "fluid end", "inspection", "ultrasonic"],
            1.0
        ),
        SearchDocument(
            15,
            "Bearing Lubrication and Overheating Prevention",
            "Proper lubrication intervals and oil analysis prevent bearing overheating and extend power end life.",
            ["bearing", "lubrication", "overheating", "power end"],
            1.0
        ),
        SearchDocument(
            16,
            "Valve Spring Fatigue and Replacement",
            "Valve springs are subject to cyclic fatigue. Regular load testing and timely replacement are necessary to prevent valve failures.",
            ["valve", "spring", "fatigue", "replacement"],
            1.0
        ),
        SearchDocument(
            17,
            "Hammer Union Thread Inspection",
            "Thread galling and deformation in hammer unions can lead to leaks. Visual and thread gauge inspections are recommended.",
            ["hammer union", "thread", "inspection", "leak"],
            1.0
        ),
        SearchDocument(
            18,
            "Pump Efficiency Metrics and Analysis",
            "Key efficiency metrics include volumetric efficiency, mechanical efficiency, and overall pump performance. Data-driven analysis identifies improvement areas.",
            ["pump", "efficiency", "metrics", "analysis"],
            1.0
        ),
        SearchDocument(
            19,
            "Cavitation Prevention in Suction Valves",
            "Maintaining adequate NPSH and avoiding high flow velocities are critical for preventing cavitation in suction valves.",
            ["cavitation", "suction valve", "NPSH", "flow"],
            1.0
        ),
        SearchDocument(
            20,
            "Freeze Protection for Fluid Ends",
            "Insulation and heat tracing are effective freeze protection strategies for fluid ends during cold weather operations.",
            ["freeze protection", "fluid end", "cold weather"],
            1.0
        ),
        SearchDocument(
            21,
            "Proppant Handling and Erosion Control",
            "Proper proppant handling minimizes erosion in treating iron and fluid ends. Use of wear-resistant materials is recommended.",
            ["proppant", "handling", "erosion", "control"],
            1.0
        ),
        SearchDocument(
            22,
            "Corrosion-Resistant Materials for Fluid Ends",
            "Selecting corrosion-resistant alloys extends fluid end service life in harsh chemical environments.",
            ["corrosion", "resistant", "materials", "fluid end"],
            1.0
        ),
        SearchDocument(
            23,
            "Pressure Relief Valve Testing Protocols",
            "Testing protocols for pressure relief valves include set pressure verification and leak testing.",
            ["pressure relief valve", "testing", "protocols"],
            1.0
        ),
        SearchDocument(
            24,
            "SCADA Integration for Pump Operations",
            "SCADA integration enables remote monitoring, control, and diagnostics for pump fleets.",
            ["SCADA", "integration", "pump operations"],
            1.0
        ),
        SearchDocument(
            25,
            "Pump Deployment Optimization Algorithms",
            "Advanced algorithms optimize pump deployment based on job requirements, maintenance status, and location.",
            ["pump", "deployment", "optimization", "algorithms"],
            1.0
        ),
        SearchDocument(
            26,
            "Plunger Material Selection for Wear Resistance",
            "Material selection for plungers impacts wear rates. Hardened alloys and surface treatments improve longevity.",
            ["plunger", "material", "wear resistance"],
            1.0
        ),
        SearchDocument(
            27,
            "Root Cause Analysis of Fluid End Failures",
            "Root cause analysis identifies underlying issues such as material defects, improper assembly, or operational overload in fluid end failures.",
            ["root cause", "fluid end", "failure analysis"],
            1.0
        ),
        SearchDocument(
            28,
            "Chemical Attack and Fluid End Degradation",
            "Acidic or incompatible chemicals can degrade fluid end materials. Monitoring chemical composition is essential.",
            ["chemical", "attack", "fluid end", "degradation"],
            1.0
        ),
        SearchDocument(
            29,
            "Real-Time Vibration Monitoring",
            "Continuous vibration monitoring detects early signs of bearing and plunger issues in quintuplex pumps.",
            ["real-time", "vibration", "monitoring", "quintuplex"],
            1.0
        ),
        SearchDocument(
            30,
            "Suction Valve Inspection Checklist",
            "A comprehensive checklist for suction valve inspection includes checking for seat wear, spring condition, and proper alignment.",
            ["suction valve", "inspection", "checklist"],
            1.0
        ),
        SearchDocument(
            31,
            "Freeze Damage Remediation Steps",
            "If freeze damage occurs, inspect all fluid end components for cracks and replace compromised parts before restart.",
            ["freeze", "damage", "remediation", "fluid end"],
            1.0
        ),
        SearchDocument(
            32,
            "Hammer Union Pressure Testing",
            "Pressure testing of hammer unions verifies seal integrity and detects leaks before service.",
            ["hammer union", "pressure testing", "seal integrity"],
            1.0
        ),
        SearchDocument(
            33,
            "Pump Rate Adjustment for Proppant Slurries",
            "Adjusting pump rate for high proppant slurries reduces risk of line plugging and excessive wear.",
            ["pump rate", "proppant", "slurry", "adjustment"],
            1.0
        ),
        SearchDocument(
            34,
            "Bearing Failure Modes and Diagnostics",
            "Common bearing failure modes include fatigue, contamination, and misalignment. Diagnostics involve vibration and temperature analysis.",
            ["bearing", "failure modes", "diagnostics"],
            1.0
        ),
        SearchDocument(
            35,
            "NDT for Hammer Union Crack Detection",
            "Magnetic particle and dye penetrant NDT methods are effective for detecting surface cracks in hammer unions.",
            ["NDT", "hammer union", "crack detection"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)