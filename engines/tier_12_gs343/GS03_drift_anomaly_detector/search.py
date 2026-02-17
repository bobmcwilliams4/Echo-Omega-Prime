import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# --- Data Classes ---

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

# --- Search Index Implementation ---

class SearchIndex:
    def __init__(self):
        self._documents: Dict[int, SearchDocument] = {}
        self._doc_lengths: Dict[int, int] = {}
        self._inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self._doc_freq: Dict[str, int] = defaultdict(int)
        self._total_terms = 0
        self._lock = threading.RLock()
        self._avg_doc_length = 0.0
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
            self._total_terms += len(tokens)
            for term, count in term_counts.items():
                self._inverted_index[term][doc.id] = count
                self._doc_freq[term] += 1
            self._avg_doc_length = self._total_terms / max(1, len(self._documents))
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        doc_scores: Dict[int, float] = defaultdict(float)
        doc_snippets: Dict[int, str] = {}
        for term in query_terms:
            idf = self._compute_idf(term)
            postings = self._inverted_index.get(term, {})
            for doc_id, tf in postings.items():
                doc = self._documents[doc_id]
                bm25_score = self._score_bm25(term, tf, doc_id, idf) * doc.weight
                doc_scores[doc_id] += bm25_score
                if doc_id not in doc_snippets:
                    doc_snippets[doc_id] = self._make_snippet(doc, query_terms)
        # TF-IDF scoring for tie-breaking
        for doc_id in doc_scores:
            tfidf_score = self._score_tfidf(query_terms, doc_id)
            doc_scores[doc_id] += 0.1 * tfidf_score
        top_docs = heapq.nlargest(limit, doc_scores.items(), key=lambda x: x[1])
        results = []
        for doc_id, score in top_docs:
            doc = self._documents[doc_id]
            snippet = doc_snippets.get(doc_id, self._make_snippet(doc, query_terms))
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                "num_documents": len(self._documents),
                "avg_doc_length": self._avg_doc_length,
                "total_terms": self._total_terms,
                "vocab_size": len(self._inverted_index)
            }

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9_]+\b', text.lower())
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        N = len(self._documents)
        df = self._doc_freq.get(term, 0)
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, term: str, tf: int, doc_id: int, idf: float) -> float:
        dl = self._doc_lengths.get(doc_id, 0)
        avg_dl = self._avg_doc_length or 1.0
        k1 = self._bm25_k1
        b = self._bm25_b
        numerator = tf * (k1 + 1)
        denominator = tf + k1 * (1 - b + b * dl / avg_dl)
        return idf * numerator / denominator

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tfidf = 0.0
        dl = self._doc_lengths.get(doc_id, 0)
        for term in query_terms:
            tf = self._inverted_index.get(term, {}).get(doc_id, 0)
            if tf == 0:
                continue
            tf_norm = tf / (dl or 1)
            idf = self._compute_idf(term)
            tfidf += tf_norm * idf
        return tfidf

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 40) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:window*2]
            return snippet + ("..." if len(content) > window*2 else "")
        pos = positions[0]
        start = max(0, pos - window)
        end = min(len(tokens), pos + window)
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        return snippet + ("..." if end < len(tokens) else "")

# --- Singleton Factory ---

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_domain_documents(_search_index_instance)
        return _search_index_instance

# --- Pre-seed Domain Documents ---

def _seed_domain_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Z-Score Based Anomaly Detection",
            "Detects anomalies by calculating the z-score of engine metrics. Outliers are flagged if their z-score exceeds a configurable threshold. Robust for normally distributed data.",
            ["z-score", "anomaly", "outlier", "metrics"],
            1.0
        ),
        SearchDocument(
            2,
            "Interquartile Range (IQR) Outlier Detection",
            "Uses the interquartile range to identify outliers in engine performance data. Values outside 1.5*IQR from Q1 or Q3 are considered anomalies.",
            ["iqr", "outlier", "engine", "statistics"],
            1.0
        ),
        SearchDocument(
            3,
            "Isolation Forest for Anomaly Detection",
            "Applies Isolation Forest algorithm to engine telemetry. Efficiently isolates anomalies in high-dimensional data. Suitable for unsupervised anomaly detection.",
            ["isolation-forest", "anomaly", "unsupervised", "telemetry"],
            1.0
        ),
        SearchDocument(
            4,
            "Engine Performance Baseline Tracking",
            "Establishes a baseline for engine metrics using historical data. Detects drift when current metrics deviate significantly from the baseline.",
            ["baseline", "drift", "metrics", "performance"],
            1.0
        ),
        SearchDocument(
            5,
            "Response Time Drift Detection",
            "Monitors engine response times for gradual or sudden drift. Alerts are triggered if median or percentile response times exceed thresholds.",
            ["response-time", "drift", "latency", "alert"],
            1.0
        ),
        SearchDocument(
            6,
            "Error Rate Drift Analysis",
            "Tracks error rates over time to detect abnormal increases. Uses moving averages and statistical tests to distinguish between noise and true drift.",
            ["error-rate", "drift", "statistical-test", "monitoring"],
            1.0
        ),
        SearchDocument(
            7,
            "Confidence Score Distribution Shift",
            "Analyzes the distribution of model confidence scores. Flags significant shifts which may indicate data drift or model degradation.",
            ["confidence-score", "distribution", "drift", "model"],
            1.0
        ),
        SearchDocument(
            8,
            "Output Quality Metric Drift",
            "Monitors output quality metrics such as accuracy, precision, and recall. Detects drift when these metrics fall below baseline.",
            ["output-quality", "accuracy", "drift", "metrics"],
            1.0
        ),
        SearchDocument(
            9,
            "Behavioral Fingerprinting per Engine",
            "Builds behavioral fingerprints for each engine instance. Compares real-time behavior to fingerprints to detect anomalies.",
            ["fingerprinting", "behavior", "engine", "anomaly"],
            1.0
        ),
        SearchDocument(
            10,
            "Seasonal Pattern Accounting",
            "Accounts for seasonal patterns in engine metrics to avoid false positives. Uses time series decomposition to separate trend, seasonality, and residuals.",
            ["seasonal", "pattern", "time-series", "metrics"],
            1.0
        ),
        SearchDocument(
            11,
            "Alert Fatigue Prevention: Minimum Severity Thresholds",
            "Implements minimum severity thresholds to reduce alert fatigue. Only alerts on anomalies exceeding a configurable impact level.",
            ["alert", "fatigue", "severity", "threshold"],
            1.0
        ),
        SearchDocument(
            12,
            "Anomaly Correlation Across Engines",
            "Correlates anomalies detected across multiple engines. Identifies systemic issues versus isolated incidents.",
            ["anomaly", "correlation", "engine", "systemic"],
            1.0
        ),
        SearchDocument(
            13,
            "Root Cause Inference from Anomaly Patterns",
            "Infers root causes by analyzing patterns of anomalies across metrics and time. Suggests likely sources for remediation.",
            ["root-cause", "anomaly", "pattern", "inference"],
            1.0
        ),
        SearchDocument(
            14,
            "Anomaly Severity Classification",
            "Classifies detected anomalies by severity using impact analysis. Severity levels guide alerting and remediation priorities.",
            ["anomaly", "severity", "classification", "impact"],
            1.0
        ),
        SearchDocument(
            15,
            "Trending vs Sudden Anomalies",
            "Distinguishes between trending (gradual) and sudden (spike) anomalies. Uses slope analysis and change point detection.",
            ["trending", "sudden", "anomaly", "change-point"],
            1.0
        ),
        SearchDocument(
            16,
            "Phantom Load Detection",
            "Detects phantom loads—unexplained resource consumption—by analyzing baseline and current usage. Useful for uncovering hidden processes.",
            ["phantom-load", "resource", "baseline", "detection"],
            1.0
        ),
        SearchDocument(
            17,
            "Resource Leak Pattern Detection",
            "Identifies resource leak patterns such as memory or handle leaks. Uses time series and threshold-based alerts.",
            ["resource-leak", "pattern", "memory", "alert"],
            1.0
        ),
        SearchDocument(
            18,
            "Memory Growth Analysis",
            "Monitors memory usage growth over time. Flags abnormal increases that may indicate leaks or inefficient code.",
            ["memory", "growth", "analysis", "leak"],
            1.0
        ),
        SearchDocument(
            19,
            "Connection Pool Drift Detection",
            "Tracks connection pool sizes and usage. Detects drift from expected behavior, which may signal leaks or configuration issues.",
            ["connection-pool", "drift", "leak", "configuration"],
            1.0
        ),
        SearchDocument(
            20,
            "Cache Hit Rate Degradation",
            "Monitors cache hit rates and alerts on degradation. Helps identify caching inefficiencies or data access pattern changes.",
            ["cache", "hit-rate", "degradation", "monitoring"],
            1.0
        ),
        SearchDocument(
            21,
            "API Latency Distribution Shift",
            "Analyzes API latency distributions for shifts. Detects performance regressions and helps with root cause analysis.",
            ["api", "latency", "distribution", "shift"],
            1.0
        ),
        SearchDocument(
            22,
            "Data Quality Drift Indicators",
            "Monitors data quality metrics such as completeness, consistency, and validity. Flags drift that may impact downstream processes.",
            ["data-quality", "drift", "metrics", "monitoring"],
            1.0
        ),
        SearchDocument(
            23,
            "Composite Anomaly Scoring",
            "Combines multiple anomaly detectors (z-score, IQR, Isolation Forest) into a composite score for robust detection.",
            ["composite", "anomaly", "score", "detector"],
            1.0
        ),
        SearchDocument(
            24,
            "Anomaly Suppression Rules",
            "Defines rules to suppress known benign anomalies. Reduces noise and focuses attention on actionable events.",
            ["anomaly", "suppression", "rules", "noise"],
            1.0
        ),
        SearchDocument(
            25,
            "Automated Remediation Triggers",
            "Links anomaly detection to automated remediation scripts. Enables rapid response to critical issues.",
            ["remediation", "automation", "trigger", "anomaly"],
            1.0
        ),
        SearchDocument(
            26,
            "Adaptive Thresholding",
            "Dynamically adjusts anomaly detection thresholds based on recent data trends. Improves sensitivity and reduces false positives.",
            ["adaptive", "threshold", "anomaly", "trend"],
            1.0
        ),
        SearchDocument(
            27,
            "Metric Aggregation Strategies",
            "Describes aggregation strategies (mean, median, p95) for engine metrics to support robust anomaly detection.",
            ["aggregation", "metrics", "mean", "median", "p95"],
            1.0
        ),
        SearchDocument(
            28,
            "Drift Detection in Streaming Data",
            "Implements drift detection algorithms for streaming engine data. Supports real-time anomaly detection.",
            ["drift", "streaming", "data", "real-time"],
            1.0
        ),
        SearchDocument(
            29,
            "Multi-Engine Anomaly Dashboard",
            "Provides a dashboard to visualize anomalies across multiple engines. Supports filtering, correlation, and drill-down analysis.",
            ["dashboard", "multi-engine", "visualization", "correlation"],
            1.0
        ),
        SearchDocument(
            30,
            "Explainable Anomaly Detection",
            "Offers explanations for detected anomalies, including feature attribution and context. Enhances trust and actionability.",
            ["explainable", "anomaly", "feature", "context"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)