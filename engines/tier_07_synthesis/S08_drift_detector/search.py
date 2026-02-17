import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Set, Tuple, Optional

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
        self.inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.doc_tags: Dict[int, Set[str]] = {}
        self.doc_weights: Dict[int, float] = {}
        self.total_docs: int = 0
        self.avg_doc_length: float = 0.0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self.k1 = 1.5
        self.b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + ' ' + doc.content)
            tf = Counter(tokens)
            self.documents[doc.id] = doc
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            self.doc_tags[doc.id] = set(doc.tags)
            self.doc_weights[doc.id] = doc.weight
            for term in tf:
                self.inverted_index[term].add(doc.id)
            self.total_docs += 1
            self.avg_doc_length = (
                sum(self.doc_lengths.values()) / self.total_docs
            ) if self.total_docs > 0 else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidate_doc_ids = set()
        for term in query_terms:
            candidate_doc_ids.update(self.inverted_index.get(term, set()))
        scored_results: List[Tuple[int, float]] = []
        for doc_id in candidate_doc_ids:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            composite_score = 0.7 * bm25_score + 0.3 * tfidf_score
            composite_score *= self.doc_weights.get(doc_id, 1.0)
            scored_results.append((doc_id, composite_score))
        scored_results.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored_results[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, any]:
        with self.lock:
            return {
                'total_documents': self.total_docs,
                'average_document_length': self.avg_doc_length,
                'unique_terms': len(self.inverted_index),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = len(self.inverted_index.get(term, set()))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        tf = self.term_freqs.get(doc_id, Counter())
        for term in set(query_terms):
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            numerator = f * (self.k1 + 1)
            denominator = f + self.k1 * (1 - self.b + self.b * doc_len / avg_dl)
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self.term_freqs.get(doc_id, Counter())
        doc_len = self.doc_lengths.get(doc_id, 1)
        score = 0.0
        for term in set(query_terms):
            freq = tf.get(term, 0)
            if freq == 0:
                continue
            tf_norm = freq / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:200] + '...' if len(content) > 200 else content
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(rf'\b({re.escape(term)})\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + '...'

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

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Statistical Process Control Charts Overview",
            "Statistical Process Control (SPC) charts are used to monitor process stability and detect shifts or drifts in manufacturing and other processes. Common types include Shewhart, CUSUM, and EWMA charts.",
            ["spc", "control charts", "overview"],
            1.0
        ),
        SearchDocument(
            2,
            "CUSUM Change Point Detection",
            "CUSUM (Cumulative Sum) is a sequential analysis technique for change point detection in time series. It is highly sensitive to small and persistent shifts in process mean, making it ideal for drift detection.",
            ["cusum", "change point", "drift detection"],
            1.1
        ),
        SearchDocument(
            3,
            "EWMA Smoothing for Drift Detection",
            "Exponentially Weighted Moving Average (EWMA) is a smoothing technique used in control charts to detect gradual drifts. EWMA charts are less sensitive to large shifts but excel at identifying slow trends.",
            ["ewma", "smoothing", "drift"],
            1.0
        ),
        SearchDocument(
            4,
            "Shewhart Control Limits Explained",
            "Shewhart control charts use fixed control limits to detect out-of-control conditions. They are effective for identifying large, sudden changes but less sensitive to small drifts.",
            ["shewhart", "control limits", "spc"],
            1.0
        ),
        SearchDocument(
            5,
            "Calibration Drift Taxonomy",
            "Calibration drift refers to the gradual deviation of measurement instruments from their standard values. Taxonomy includes linear, exponential, and random walk drifts.",
            ["calibration", "drift", "taxonomy"],
            1.2
        ),
        SearchDocument(
            6,
            "Confidence Distribution Monitoring",
            "Monitoring confidence distributions allows for the detection of changes in the underlying data generating process, providing early warning of drift or anomalies.",
            ["confidence", "distribution", "monitoring"],
            1.0
        ),
        SearchDocument(
            7,
            "Inter-Engine Correlation Drift",
            "Drift can occur in the correlation structure between multiple engines or sensors. Monitoring inter-engine correlation is crucial for multivariate drift detection.",
            ["correlation", "multivariate", "drift"],
            1.1
        ),
        SearchDocument(
            8,
            "Seasonal Adjustment in Drift Detection",
            "Seasonal adjustment techniques remove periodic effects from data, improving the sensitivity of drift detection algorithms to genuine process changes.",
            ["seasonal", "adjustment", "drift"],
            1.0
        ),
        SearchDocument(
            9,
            "Drift Attribution Analysis",
            "Attribution analysis seeks to identify the root cause of detected drift, distinguishing between process, measurement, or environmental factors.",
            ["drift", "attribution", "analysis"],
            1.2
        ),
        SearchDocument(
            10,
            "Drift Severity Classification",
            "Classifying drift severity helps prioritize responses. Severity can be based on magnitude, duration, or impact on process quality.",
            ["drift", "severity", "classification"],
            1.1
        ),
        SearchDocument(
            11,
            "Automated Recalibration Triggers",
            "Automated systems can trigger recalibration when drift is detected, reducing downtime and maintaining measurement accuracy.",
            ["recalibration", "automation", "drift"],
            1.1
        ),
        SearchDocument(
            12,
            "Drift Reporting Protocols",
            "Standardized protocols for reporting drift events ensure traceability and facilitate regulatory compliance.",
            ["drift", "reporting", "protocols"],
            1.0
        ),
        SearchDocument(
            13,
            "Historical Baseline Comparison",
            "Comparing current process data to historical baselines is a fundamental approach for drift detection and process monitoring.",
            ["historical", "baseline", "comparison"],
            1.0
        ),
        SearchDocument(
            14,
            "Multivariate Drift Detection",
            "Multivariate techniques consider correlations between variables, enabling detection of complex drift patterns not visible in univariate analysis.",
            ["multivariate", "drift", "detection"],
            1.2
        ),
        SearchDocument(
            15,
            "Concept Drift vs Data Drift",
            "Concept drift refers to changes in the underlying relationship between input and output variables, while data drift involves changes in the input data distribution.",
            ["concept drift", "data drift", "comparison"],
            1.2
        ),
        SearchDocument(
            16,
            "KL Divergence Monitoring",
            "Kullback-Leibler (KL) divergence quantifies the difference between probability distributions and is used for monitoring distributional drift.",
            ["kl divergence", "monitoring", "drift"],
            1.1
        ),
        SearchDocument(
            17,
            "Kolmogorov-Smirnov Test for Drift",
            "The Kolmogorov-Smirnov (KS) test is a non-parametric test for comparing distributions, commonly used for detecting data drift.",
            ["ks test", "kolmogorov-smirnov", "drift"],
            1.0
        ),
        SearchDocument(
            18,
            "Drift Alert Thresholds",
            "Setting appropriate alert thresholds is critical to balance sensitivity and false positives in drift detection systems.",
            ["drift", "alert", "thresholds"],
            1.0
        ),
        SearchDocument(
            19,
            "Drift Root Cause Analysis",
            "Root cause analysis investigates the origin of detected drift, using statistical and process knowledge to guide corrective actions.",
            ["drift", "root cause", "analysis"],
            1.2
        ),
        SearchDocument(
            20,
            "Drift Correction Strategies",
            "Correction strategies include recalibration, retraining, or process adjustment, depending on the type and severity of drift.",
            ["drift", "correction", "strategies"],
            1.1
        ),
        SearchDocument(
            21,
            "Drift Watcher Baseline Comparison",
            "Drift watcher modules provide continuous comparison to baseline data, enabling real-time drift alerts and diagnostics.",
            ["drift watcher", "baseline", "comparison"],
            1.0
        ),
        SearchDocument(
            22,
            "Epistemic Gap Detection",
            "Epistemic gap refers to the difference between model knowledge and reality. Detecting this gap is crucial for robust drift monitoring.",
            ["epistemic gap", "detection", "drift"],
            1.2
        ),
        SearchDocument(
            23,
            "Fact Fragility Scoring",
            "Fact fragility scoring assesses the stability of knowledge or measurements, highlighting areas susceptible to drift or uncertainty.",
            ["fact fragility", "scoring", "drift"],
            1.1
        ),
        SearchDocument(
            24,
            "Zoned Analysis for Calibration Drift",
            "Zoned analysis divides the measurement space into regions, enabling localized detection and correction of calibration drift.",
            ["zoned analysis", "calibration", "drift"],
            1.1
        ),
        SearchDocument(
            25,
            "Three-Layer Response Architecture",
            "A three-layer architecture for drift response includes detection, attribution, and correction layers, ensuring comprehensive management.",
            ["three-layer", "architecture", "drift"],
            1.2
        ),
        SearchDocument(
            26,
            "Multi-Doctrine Decomposition for Deep Analysis",
            "Multi-doctrine decomposition applies multiple analytical frameworks to drift events, yielding deeper insights and robust diagnostics.",
            ["multi-doctrine", "decomposition", "deep analysis"],
            1.2
        ),
        SearchDocument(
            27,
            "Coverage Map Construction",
            "Coverage maps visualize the extent and location of drift across process parameters, supporting targeted interventions.",
            ["coverage map", "construction", "drift"],
            1.0
        ),
        SearchDocument(
            28,
            "Audit Trail Logging for Drift Detection",
            "Comprehensive audit trails log all drift detection events, supporting traceability, compliance, and forensic analysis.",
            ["audit trail", "logging", "drift detection"],
            1.1
        ),
        SearchDocument(
            29,
            "Deep Analysis Composite",
            "Composite analysis integrates multiple drift detection and attribution methods, providing a holistic view of process health.",
            ["deep analysis", "composite", "drift"],
            1.2
        ),
        SearchDocument(
            30,
            "Advanced SPC Charting for Drift",
            "Advanced SPC charting techniques combine Shewhart, CUSUM, and EWMA for robust drift detection in complex environments.",
            ["spc", "advanced", "charting", "drift"],
            1.1
        ),
        SearchDocument(
            31,
            "Process Drift vs Measurement Drift",
            "Distinguishing between process and measurement drift is essential for effective root cause analysis and corrective action.",
            ["process drift", "measurement drift", "analysis"],
            1.1
        ),
        SearchDocument(
            32,
            "Real-Time Drift Monitoring Systems",
            "Real-time drift monitoring systems leverage streaming analytics and automated alerting to maintain process control.",
            ["real-time", "monitoring", "drift"],
            1.1
        ),
        SearchDocument(
            33,
            "Drift Impact on Quality Metrics",
            "Drift can degrade quality metrics such as yield, accuracy, and reliability. Early detection is key to minimizing impact.",
            ["drift", "impact", "quality"],
            1.0
        ),
        SearchDocument(
            34,
            "Drift Correction Feedback Loops",
            "Feedback loops enable continuous correction of drift, adapting process parameters in response to detected changes.",
            ["drift", "correction", "feedback"],
            1.1
        ),
        SearchDocument(
            35,
            "Drift Detection in Multimodal Data",
            "Detecting drift in multimodal data requires specialized techniques to handle heterogeneous data types and sources.",
            ["drift detection", "multimodal", "data"],
            1.2
        ),
    ]
    for doc in docs:
        index.add_document(doc)