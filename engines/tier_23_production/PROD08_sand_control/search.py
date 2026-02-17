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
# Search Index
# -----------------------------

class SearchIndex:
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_doc_norms: Dict[int, float] = {}

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            term_counts = Counter(tokens)
            for term, freq in term_counts.items():
                self.inverted_index[term][doc.id] = freq
                self.term_doc_freq[term] += 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs
            self._idf_cache.clear()
            self._tfidf_doc_norms.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, {}).keys())
        bm25_scores = {}
        tfidf_scores = {}
        for doc_id in candidate_docs:
            bm25_scores[doc_id] = self._score_bm25(doc_id, query_terms)
            tfidf_scores[doc_id] = self._score_tfidf(doc_id, query_terms)
        # Combine BM25 and TF-IDF (weighted average)
        results = []
        for doc_id in candidate_docs:
            bm25 = bm25_scores.get(doc_id, 0.0)
            tfidf = tfidf_scores.get(doc_id, 0.0)
            # BM25 weighted 0.7, TF-IDF weighted 0.3
            score = 0.7 * bm25 + 0.3 * tfidf
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "total_docs": self.total_docs,
                "avg_doc_length": self.avg_doc_length,
                "unique_terms": len(self.inverted_index)
            }

    def _tokenize(self, text: str) -> List[str]:
        # Lowercase, remove non-alphanum, split on whitespace
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        tokens = text.split()
        return tokens

    def _compute_idf(self, term: str) -> float:
        # IDF with smoothing
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        N = self.total_docs
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str], k1: float = 1.5, b: float = 0.75) -> float:
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        term_freqs = self.inverted_index
        for term in query_terms:
            f = term_freqs.get(term, {}).get(doc_id, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + k1 * (1 - b + b * doc_len / (self.avg_doc_length or 1))
            score += idf * f * (k1 + 1) / denom
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        # TF-IDF with cosine normalization
        doc = self.documents[doc_id]
        tokens = self._tokenize(doc.content)
        doc_tf = Counter(tokens)
        doc_norm = self._tfidf_doc_norms.get(doc_id)
        if doc_norm is None:
            doc_norm = math.sqrt(sum((self._compute_idf(t) * tf) ** 2 for t, tf in doc_tf.items()))
            self._tfidf_doc_norms[doc_id] = doc_norm
        score = 0.0
        for term in query_terms:
            tf = doc_tf.get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            score += (tf * idf)
        if doc_norm > 0:
            score /= doc_norm
        return score * doc.weight

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return " ".join(tokens[:window]) + ("..." if len(tokens) > window else "")
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        # Highlight query terms
        snippet = []
        for t in snippet_tokens:
            if t in query_terms:
                snippet.append(f"*{t}*")
            else:
                snippet.append(t)
        return " ".join(snippet) + ("..." if end < len(tokens) else "")

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
# Pre-seeded Documents
# -----------------------------

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Critical Drawdown Pressure Fundamentals",
            "Critical drawdown pressure is the maximum pressure drop that can be applied across a formation without initiating sand production. It depends on rock strength, in-situ stress, and wellbore conditions.",
            ["critical drawdown", "sand production", "rock strength"],
            1.0
        ),
        SearchDocument(
            2,
            "Thick Wall Cylinder Testing for Sand Control",
            "Thick wall cylinder testing simulates downhole stress conditions to evaluate formation sand strength and predict sand production onset. It is a laboratory test for sand control design.",
            ["thick wall cylinder", "sand strength", "laboratory testing"],
            1.0
        ),
        SearchDocument(
            3,
            "Formation Sand Analysis Techniques",
            "Formation sand analysis involves grain size distribution, mineralogy, and shape assessment. Sieve analysis and image analysis are common methods to characterize sand for control strategies.",
            ["sand analysis", "grain size", "mineralogy"],
            1.0
        ),
        SearchDocument(
            4,
            "Gravel Sizing Criteria in Sand Control",
            "Proper gravel sizing is critical to prevent sand production while maintaining permeability. Saucier and Coberly criteria are commonly used for gravel pack design.",
            ["gravel sizing", "saucier", "coberly"],
            1.0
        ),
        SearchDocument(
            5,
            "Gravel Pack Placement Techniques",
            "Gravel pack placement methods include alpha-beta wave, shunt tubes, and water packing. Proper placement ensures complete annular fill and effective sand exclusion.",
            ["gravel pack", "placement", "shunt tubes"],
            1.0
        ),
        SearchDocument(
            6,
            "Wire-Wrapped Screen Design Principles",
            "Wire-wrapped screens are designed based on slot width, open area, and collapse strength. They are widely used for sand control in unconsolidated formations.",
            ["wire-wrapped screen", "slot width", "collapse strength"],
            1.0
        ),
        SearchDocument(
            7,
            "Premium Mesh Screen Selection",
            "Premium mesh screens offer enhanced sand retention and plugging resistance. Selection depends on sand size, well conditions, and completion type.",
            ["premium mesh", "screen selection", "sand retention"],
            1.0
        ),
        SearchDocument(
            8,
            "Expandable Sand Screen Technology Overview",
            "Expandable sand screens provide zonal isolation and conform to wellbore irregularities. They are deployed in open hole completions to minimize sand production.",
            ["expandable screen", "zonal isolation", "open hole"],
            1.0
        ),
        SearchDocument(
            9,
            "Frac Pack vs Gravel Pack: Decision Factors",
            "Frac pack combines hydraulic fracturing and gravel packing to enhance productivity and sand control. The choice depends on formation properties and completion objectives.",
            ["frac pack", "gravel pack", "hydraulic fracturing"],
            1.0
        ),
        SearchDocument(
            10,
            "Proppant Selection for Frac Pack Operations",
            "Proppant selection considers strength, size, and chemical compatibility. Resin-coated sand and ceramic proppants are common for frac pack completions.",
            ["proppant selection", "resin-coated sand", "ceramic proppant"],
            1.0
        ),
        SearchDocument(
            11,
            "Resin Consolidation Systems for Sand Control",
            "Resin consolidation involves injecting resin into the formation to bind sand grains and reduce sand production. System selection depends on reservoir temperature and permeability.",
            ["resin consolidation", "sand control", "formation treatment"],
            1.0
        ),
        SearchDocument(
            12,
            "Acoustic Sand Monitoring Techniques",
            "Acoustic monitoring detects sand production by analyzing sound signatures in the wellbore. It enables real-time sand detection and proactive management.",
            ["acoustic monitoring", "sand detection", "real-time"],
            1.0
        ),
        SearchDocument(
            13,
            "Erosion Monitoring and Inspection Methods",
            "Erosion monitoring uses ultrasonic, caliper, and fiber optic tools to detect metal loss in downhole equipment caused by sand production.",
            ["erosion monitoring", "inspection", "metal loss"],
            1.0
        ),
        SearchDocument(
            14,
            "Economics of Sand Control",
            "Sand control economics evaluates the cost-benefit of various sand management strategies, including equipment, downtime, and remediation expenses.",
            ["sand control", "economics", "cost-benefit"],
            1.0
        ),
        SearchDocument(
            15,
            "Sand Management vs Sand Exclusion",
            "Sand management allows controlled sand production with surface handling, while sand exclusion aims to prevent sand entry into the wellbore.",
            ["sand management", "sand exclusion", "production"],
            1.0
        ),
        SearchDocument(
            16,
            "Perforation Strategy for Sand Control",
            "Perforation strategy includes selecting shot density, phasing, and charge size to minimize sand production and optimize inflow.",
            ["perforation", "shot density", "phasing"],
            1.0
        ),
        SearchDocument(
            17,
            "Slotted Liner vs Screen Completions",
            "Slotted liners offer mechanical sand control with simple design, while screens provide better sand retention and flow area.",
            ["slotted liner", "screen completion", "sand retention"],
            1.0
        ),
        SearchDocument(
            18,
            "Oriented Perforation for Sand Control",
            "Oriented perforation aligns shots with in-situ stress to minimize sand production and casing damage.",
            ["oriented perforation", "in-situ stress", "casing damage"],
            1.0
        ),
        SearchDocument(
            19,
            "Multi-Zone Sand Control Completions",
            "Multi-zone completions use packers, sleeves, and selective screens to control sand in stacked reservoirs.",
            ["multi-zone", "packers", "selective screens"],
            1.0
        ),
        SearchDocument(
            20,
            "Horizontal Well Sand Control Challenges",
            "Horizontal wells face unique sand control challenges such as uneven inflow, gravel placement difficulties, and screen plugging.",
            ["horizontal well", "sand control", "screen plugging"],
            1.0
        ),
        SearchDocument(
            21,
            "Gravel Pack Fluid Loss Control",
            "Fluid loss control during gravel pack operations prevents formation damage and ensures proper gravel placement.",
            ["gravel pack", "fluid loss", "formation damage"],
            1.0
        ),
        SearchDocument(
            22,
            "Shunt Tube Technology in Gravel Packing",
            "Shunt tubes enable complete gravel placement in long or deviated intervals by bypassing bridges and ensuring annular fill.",
            ["shunt tube", "gravel packing", "annular fill"],
            1.0
        ),
        SearchDocument(
            23,
            "Screen Plugging Prevention Methods",
            "Screen plugging is mitigated by prepacking, backwashing, and selecting appropriate screen size and mesh.",
            ["screen plugging", "prepacking", "backwashing"],
            1.0
        ),
        SearchDocument(
            24,
            "Sand Control in High Rate Gas Wells",
            "High rate gas wells require robust sand control solutions due to high velocities and erosional risks.",
            ["gas well", "sand control", "erosion"],
            1.0
        ),
        SearchDocument(
            25,
            "Sand Control for Deepwater Applications",
            "Deepwater sand control considers high pressure, temperature, and complex completion geometries.",
            ["deepwater", "sand control", "high pressure"],
            1.0
        ),
        SearchDocument(
            26,
            "Sand Control Completion Design Workflow",
            "A systematic workflow includes sand analysis, completion selection, and risk assessment for effective sand control.",
            ["completion design", "workflow", "risk assessment"],
            1.0
        ),
        SearchDocument(
            27,
            "Sand Control Failure Modes",
            "Failure modes include screen erosion, plugging, gravel pack breakdown, and formation collapse.",
            ["failure mode", "screen erosion", "formation collapse"],
            1.0
        ),
        SearchDocument(
            28,
            "Sand Control in Unconsolidated Formations",
            "Unconsolidated formations are prone to sand production and require tailored sand control strategies.",
            ["unconsolidated", "sand production", "control strategies"],
            1.0
        ),
        SearchDocument(
            29,
            "Sand Control Equipment Selection",
            "Equipment selection is based on formation properties, completion type, and operational constraints.",
            ["equipment selection", "formation", "completion"],
            1.0
        ),
        SearchDocument(
            30,
            "Advanced Sand Control Modeling",
            "Numerical modeling predicts sand production risk and evaluates sand control effectiveness under various scenarios.",
            ["modeling", "sand production", "numerical"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)