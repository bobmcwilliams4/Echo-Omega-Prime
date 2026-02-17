import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# -----------------------------
# Data Classes
# -----------------------------

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

# -----------------------------
# Search Index Implementation
# -----------------------------

class SearchIndex:
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)  # term -> doc_id -> tf
        self.doc_lengths: Dict[int, int] = {}  # doc_id -> length
        self.doc_tag_index: Dict[str, set] = defaultdict(set)
        self.N = 0
        self.avgdl = 0.0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.RLock()
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.title + " " + doc.content)
            tf = Counter(tokens)
            for term, freq in tf.items():
                self.inverted_index[term][doc.id] = freq
            self.doc_lengths[doc.id] = len(tokens)
            for tag in doc.tags:
                self.doc_tag_index[tag.lower()].add(doc.id)
            self.N += 1
            self.avgdl = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[int, float] = defaultdict(float)
        doc_snippets: Dict[int, str] = {}
        doc_titles: Dict[int, str] = {}
        doc_tf: Dict[int, Dict[str, int]] = defaultdict(dict)
        # Collect candidate docs
        candidate_docs = set()
        for term in query_terms:
            for doc_id in self.inverted_index.get(term, {}):
                candidate_docs.add(doc_id)
        # Score using BM25 and TF-IDF
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc = self.documents[doc_id]
            # Weighted sum: 0.7 BM25 + 0.3 TF-IDF
            score = 0.7 * bm25_score + 0.3 * tfidf_score
            doc_scores[doc_id] = score * doc.weight
            doc_titles[doc_id] = doc.title
            doc_snippets[doc_id] = self._make_snippet(doc, query_terms)
        # Sort and return
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = [
            SearchResult(doc_id=doc_id, score=score, title=doc_titles[doc_id], snippet=doc_snippets[doc_id])
            for doc_id, score in ranked
        ]
        return results

    def get_stats(self) -> Dict[str, int]:
        with self.lock:
            return {
                "num_documents": self.N,
                "num_terms": len(self.inverted_index),
                "avg_doc_length": int(self.avgdl),
            }

    def _tokenize(self, text: str) -> List[str]:
        # Lowercase, remove non-alphanumeric, split on whitespace
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        tokens = text.split()
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = len(self.inverted_index.get(term, {}))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        dl = self.doc_lengths[doc_id]
        for term in query_terms:
            tf = self.inverted_index.get(term, {}).get(doc_id, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            denom = tf + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * dl / self.avgdl)
            term_score = idf * (tf * (self._bm25_k1 + 1)) / denom
            score += term_score
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        # Term frequency normalization: tf / max_tf
        tf = {}
        max_tf = 1
        for term in query_terms:
            tf[term] = self.inverted_index.get(term, {}).get(doc_id, 0)
            if tf[term] > max_tf:
                max_tf = tf[term]
        score = 0.0
        for term in query_terms:
            if tf[term] == 0:
                continue
            idf = self._compute_idf(term)
            norm_tf = tf[term] / max_tf
            score += norm_tf * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            idx = content_lower.find(term)
            if idx != -1:
                positions.append(idx)
        if positions:
            start = max(0, min(positions) - window)
            end = min(len(content), max(positions) + window)
            snippet = content[start:end]
            # Highlight terms
            for term in set(query_terms):
                snippet = re.sub(r'(?i)\b(' + re.escape(term) + r')\b', r'**\1**', snippet)
            return snippet.strip()
        # Fallback: start of content
        return (content[:2 * window] + '...').strip() if len(content) > 2 * window else content

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
# Pre-seeded Domain Documents
# -----------------------------

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            id=1,
            title="ESP Selection and Sizing Guidelines",
            content="Proper ESP selection and sizing is critical for artificial lift performance. Consider well depth, production rate, fluid properties, and expected run life. Use the ESP selection matrix to compare with rod pump and gas lift options.",
            tags=["ESP", "Selection", "Sizing", "Artificial Lift"],
            weight=1.0
        ),
        SearchDocument(
            id=2,
            title="ESP Performance Curve Analysis",
            content="Analyzing ESP performance curves helps optimize pump operation. Evaluate head, efficiency, and power curves at various frequencies. Match the pump curve with well inflow performance for best results.",
            tags=["ESP", "Performance Curve", "Analysis"],
            weight=1.0
        ),
        SearchDocument(
            id=3,
            title="ESP Motor Design Considerations",
            content="ESP motor selection depends on voltage, horsepower, and cooling requirements. Ensure compatibility with downhole temperatures and fluid characteristics. Consider derating for high temperature operations.",
            tags=["ESP", "Motor", "Design"],
            weight=1.0
        ),
        SearchDocument(
            id=4,
            title="ESP Protector and Intake Design",
            content="The protector isolates the ESP motor from well fluids and balances pressure. Intake design affects pump NPSH and gas handling. Use charge traps for high gas wells.",
            tags=["ESP", "Protector", "Intake", "Design"],
            weight=1.0
        ),
        SearchDocument(
            id=5,
            title="ESP Cable Selection and Sizing",
            content="Cable selection for ESPs must consider voltage drop, ampacity, and mechanical strength. Use armored cable for deviated wells. Size cable for expected current and length.",
            tags=["ESP", "Cable", "Selection", "Sizing"],
            weight=1.0
        ),
        SearchDocument(
            id=6,
            title="ESP Gas Handling: Gas Separator and Charge Trap",
            content="Gas separators and charge traps improve ESP performance in gassy wells. Separators remove free gas before the pump intake, reducing gas lock risk. Charge traps accumulate and vent gas.",
            tags=["ESP", "Gas Handling", "Gas Separator", "Charge Trap"],
            weight=1.0
        ),
        SearchDocument(
            id=7,
            title="ESP Variable Speed Drive (VSD) Frequency Optimization",
            content="VSDs allow ESP speed adjustment to match changing well conditions. Optimize frequency to balance production rate, pump efficiency, and motor load. Monitor for resonance and harmonics.",
            tags=["ESP", "VSD", "Frequency", "Optimization"],
            weight=1.0
        ),
        SearchDocument(
            id=8,
            title="Rod Pump Sucker Rod and Beam Unit Design",
            content="Sucker rod design considers load, length, and grade. Beam unit selection depends on stroke length and speed. Proper design maximizes run life and minimizes failures.",
            tags=["Rod Pump", "Sucker Rod", "Beam Unit", "Design"],
            weight=1.0
        ),
        SearchDocument(
            id=9,
            title="Rod Pump Dynamometer Card Interpretation",
            content="Dynamometer cards reveal pump fillage, fluid pound, and mechanical issues. Analyze surface and downhole cards for diagnosis. Use POC data for optimization.",
            tags=["Rod Pump", "Dynamometer Card", "Interpretation"],
            weight=1.0
        ),
        SearchDocument(
            id=10,
            title="Rod Pump Rod String Design (API RP 11BR)",
            content="Follow API RP 11BR for rod string design. Calculate loads, select proper grades, and check for buckling. Consider corrosion and fatigue for long-term reliability.",
            tags=["Rod Pump", "Rod String", "API RP 11BR", "Design"],
            weight=1.0
        ),
        SearchDocument(
            id=11,
            title="Rod Pump Pump-Off Controller (POC) Optimization",
            content="POCs automate rod pump operation to prevent overpumping. Set optimal fillage and stroke parameters. Use real-time data to reduce failures and energy use.",
            tags=["Rod Pump", "POC", "Optimization"],
            weight=1.0
        ),
        SearchDocument(
            id=12,
            title="Gas Lift Design: Valve Spacing and Injection Rate",
            content="Proper valve spacing ensures efficient gas lift operation. Calculate injection rates based on well productivity and fluid level. Use IPR data for valve placement.",
            tags=["Gas Lift", "Valve Spacing", "Injection Rate", "Design"],
            weight=1.0
        ),
        SearchDocument(
            id=13,
            title="Gas Lift Optimization: Continuous vs. Intermittent",
            content="Continuous gas lift provides steady production, while intermittent is suited for low-rate wells. Optimize cycle time and injection volume for best economics.",
            tags=["Gas Lift", "Continuous", "Intermittent", "Optimization"],
            weight=1.0
        ),
        SearchDocument(
            id=14,
            title="Gas Lift Mandrel and Valve Performance (IPR)",
            content="Mandrel and valve performance affects gas lift efficiency. Use inflow performance relationship (IPR) to select proper valve types and settings.",
            tags=["Gas Lift", "Mandrel", "Valve", "IPR", "Performance"],
            weight=1.0
        ),
        SearchDocument(
            id=15,
            title="Plunger Lift Candidate Selection (Gas-Liquid Ratio)",
            content="Select plunger lift for wells with high gas-liquid ratio and intermittent flow. Evaluate well pressure and tubing size for feasibility.",
            tags=["Plunger Lift", "Candidate Selection", "Gas-Liquid Ratio"],
            weight=1.0
        ),
        SearchDocument(
            id=16,
            title="Plunger Lift Cycle Optimization (Arrival Velocity)",
            content="Optimize plunger lift cycles by monitoring arrival velocity and cycle time. Adjust shut-in and afterflow periods for maximum liquid recovery.",
            tags=["Plunger Lift", "Cycle Optimization", "Arrival Velocity"],
            weight=1.0
        ),
        SearchDocument(
            id=17,
            title="Jet Pump Design (Nozzle/Throat Area Ratio)",
            content="Jet pump performance depends on nozzle and throat area ratio. Calculate optimum ratio for desired flow and pressure. Consider solids handling and pump wear.",
            tags=["Jet Pump", "Design", "Nozzle", "Throat Area Ratio"],
            weight=1.0
        ),
        SearchDocument(
            id=18,
            title="Artificial Lift Selection Matrix (Flowrate/Depth)",
            content="Use the artificial lift selection matrix to compare ESP, rod pump, gas lift, and plunger lift for different flowrates and depths. Factor in economics and well constraints.",
            tags=["Artificial Lift", "Selection Matrix", "Flowrate", "Depth"],
            weight=1.0
        ),
        SearchDocument(
            id=19,
            title="Artificial Lift Economics (Operating Cost/CAPEX)",
            content="Analyze operating cost and CAPEX for each artificial lift method. ESPs have higher upfront cost but lower OPEX at high rates. Rod pumps excel at low rates and shallow wells.",
            tags=["Artificial Lift", "Economics", "Operating Cost", "CAPEX"],
            weight=1.0
        ),
        SearchDocument(
            id=20,
            title="Artificial Lift Run Life and MTBF Comparison",
            content="Compare run life and mean time between failures (MTBF) for ESP, rod pump, and gas lift. ESPs are sensitive to voltage and sand. Rod pumps are robust but require regular maintenance.",
            tags=["Artificial Lift", "Run Life", "MTBF", "Comparison"],
            weight=1.0
        ),
        SearchDocument(
            id=21,
            title="Artificial Lift Automation and Remote Monitoring",
            content="Automation improves artificial lift efficiency and reduces downtime. Use SCADA and remote monitoring for real-time optimization and failure prediction.",
            tags=["Artificial Lift", "Automation", "Remote Monitoring"],
            weight=1.0
        ),
        SearchDocument(
            id=22,
            title="Permian Basin Lift Selection: ESP vs. Rod Pump",
            content="In the Permian Basin, ESPs are favored for high-rate, deep wells, while rod pumps are preferred for shallow, low-rate wells. Consider formation sand and gas content.",
            tags=["Permian Basin", "ESP", "Rod Pump", "Selection"],
            weight=1.0
        ),
        SearchDocument(
            id=23,
            title="ESP Troubleshooting: Common Failures",
            content="Common ESP failures include motor burnout, gas lock, and cable damage. Diagnose using downhole sensors and surface readings. Prevent with proper design and operation.",
            tags=["ESP", "Troubleshooting", "Failure"],
            weight=1.0
        ),
        SearchDocument(
            id=24,
            title="Rod Pump Failure Analysis and Prevention",
            content="Analyze rod pump failures such as tubing leaks, rod parting, and pump sticking. Use failure data to improve design and maintenance schedules.",
            tags=["Rod Pump", "Failure", "Analysis", "Prevention"],
            weight=1.0
        ),
        SearchDocument(
            id=25,
            title="Gas Lift Troubleshooting and Optimization",
            content="Troubleshoot gas lift issues like valve malfunction and unstable injection. Optimize lift gas allocation and monitor well response for improved production.",
            tags=["Gas Lift", "Troubleshooting", "Optimization"],
            weight=1.0
        ),
        SearchDocument(
            id=26,
            title="Artificial Lift Digital Solutions",
            content="Digital solutions such as predictive analytics and IoT sensors enhance artificial lift performance. Integrate data from ESPs, rod pumps, and gas lift systems for unified optimization.",
            tags=["Artificial Lift", "Digital", "IoT", "Analytics"],
            weight=1.0
        ),
        SearchDocument(
            id=27,
            title="ESP Sand Handling Strategies",
            content="Sand production can damage ESPs. Use sand tolerant pumps, install sand separators, and monitor sand cut to prolong equipment life.",
            tags=["ESP", "Sand Handling", "Separator"],
            weight=1.0
        ),
        SearchDocument(
            id=28,
            title="Rod Pump Optimization in Unconventional Reservoirs",
            content="Optimize rod pump operation in unconventional reservoirs by adjusting stroke speed, rod design, and pump type. Monitor for gas interference and fluid pound.",
            tags=["Rod Pump", "Unconventional", "Optimization"],
            weight=1.0
        ),
        SearchDocument(
            id=29,
            title="Gas Lift Valve Testing and Calibration",
            content="Regular testing and calibration of gas lift valves ensures reliable operation. Use bench tests and field data to set opening pressures accurately.",
            tags=["Gas Lift", "Valve", "Testing", "Calibration"],
            weight=1.0
        ),
        SearchDocument(
            id=30,
            title="Artificial Lift System Integration",
            content="Integrate ESP, rod pump, and gas lift systems for complex wells. Use hybrid approaches for maximum production and reliability.",
            tags=["Artificial Lift", "System Integration", "Hybrid"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)