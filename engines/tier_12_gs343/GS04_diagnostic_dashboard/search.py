import threading
import math
import re
import heapq
import json
import csv
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

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
        self._inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_length: float = 0.0
        self._doc_count: int = 0
        self._lock = threading.RLock()
        self._idf_cache: Dict[str, float] = {}
        self._tags_index: Dict[str, Set[int]] = defaultdict(set)

        # BM25 parameters
        self.k1 = 1.5
        self.b = 0.75

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            term_freq = Counter(tokens)
            self._documents[doc.id] = doc
            self._doc_lengths[doc.id] = len(tokens)
            for term, freq in term_freq.items():
                self._inverted_index[term][doc.id] = freq
            for tag in doc.tags:
                self._tags_index[tag.lower()].add(doc.id)
            self._doc_count += 1
            self._avg_doc_length = (
                sum(self._doc_lengths.values()) / self._doc_count
                if self._doc_count > 0 else 0.0
            )
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        with self._lock:
            query_terms = self._tokenize(query)
            if not query_terms:
                return []
            doc_scores = defaultdict(float)
            doc_snippets = {}
            query_tf = Counter(query_terms)

            # Find candidate documents
            candidate_docs = set()
            for term in query_terms:
                candidate_docs.update(self._inverted_index.get(term, {}).keys())

            for doc_id in candidate_docs:
                doc = self._documents[doc_id]
                bm25_score = self._score_bm25(doc_id, query_terms, query_tf)
                tfidf_score = self._score_tfidf(doc_id, query_terms, query_tf)
                # Combine BM25 and TF-IDF (weighted)
                final_score = 0.7 * bm25_score + 0.3 * tfidf_score
                final_score *= doc.weight
                doc_scores[doc_id] = final_score
                doc_snippets[doc_id] = self._make_snippet(doc, query_terms)

            top_docs = heapq.nlargest(limit, doc_scores.items(), key=lambda x: x[1])
            results = [
                SearchResult(doc_id=doc_id, score=score, title=self._documents[doc_id].title, snippet=doc_snippets[doc_id])
                for doc_id, score in top_docs if score > 0
            ]
            return results

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                "doc_count": self._doc_count,
                "avg_doc_length": self._avg_doc_length,
                "vocab_size": len(self._inverted_index)
            }

    def _tokenize(self, text: str) -> List[str]:
        # Simple tokenizer: lowercase, split on non-word chars, remove stopwords
        stopwords = {
            'the', 'and', 'of', 'in', 'to', 'a', 'for', 'on', 'with', 'by', 'an', 'is', 'as', 'at', 'be', 'from', 'or', 'that', 'this', 'are', 'it', 'was', 'which', 'has', 'have', 'but', 'not', 'can', 'will', 'if', 'their', 'all', 'any'
        }
        tokens = re.findall(r'\b\w+\b', text.lower())
        return [t for t in tokens if t not in stopwords]

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = len(self._inverted_index.get(term, {}))
        if df == 0:
            return 0.0
        idf = math.log(1 + (self._doc_count - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str], query_tf: Counter) -> float:
        score = 0.0
        doc_len = self._doc_lengths.get(doc_id, 0)
        avgdl = self._avg_doc_length if self._avg_doc_length > 0 else 1.0
        for term in set(query_terms):
            tf = self._inverted_index.get(term, {}).get(doc_id, 0)
            idf = self._compute_idf(term)
            denom = tf + self.k1 * (1 - self.b + self.b * doc_len / avgdl)
            if denom == 0:
                continue
            term_score = idf * (tf * (self.k1 + 1)) / denom
            score += term_score
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str], query_tf: Counter) -> float:
        # TF-IDF with term frequency normalization (log normalization)
        score = 0.0
        doc_len = self._doc_lengths.get(doc_id, 0)
        for term in set(query_terms):
            tf = self._inverted_index.get(term, {}).get(doc_id, 0)
            if tf == 0:
                continue
            tf_norm = 1 + math.log(tf)
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], snippet_len: int = 160) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:snippet_len]
            return snippet + ('...' if len(content) > snippet_len else '')
        start = max(positions[0] - 10, 0)
        end = min(start + 30, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet_text = ' '.join(snippet_tokens)
        # Highlight query terms
        for term in set(query_terms):
            snippet_text = re.sub(rf'\b({re.escape(term)})\b', r'*\1*', snippet_text, flags=re.IGNORECASE)
        return snippet_text[:snippet_len] + ('...' if len(snippet_text) > snippet_len else '')

# --- Singleton Factory ---

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

# --- Pre-seed Documents ---

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1, "Dashboard Data Aggregation Patterns",
            "Explore best practices for aggregating engine metrics, including time windowing, rollups, and real-time vs batch data flows.",
            ["aggregation", "dashboard", "metrics"], 1.0
        ),
        SearchDocument(
            2, "System Health Score: Weighted Composite",
            "The health score is computed as a weighted composite of subsystem metrics: CPU, memory, error rate, and recovery success.",
            ["health", "score", "composite"], 1.0
        ),
        SearchDocument(
            3, "Engine Status Matrix",
            "A status matrix displays the operational state of all GS04 engine nodes, including online, degraded, and offline statuses.",
            ["status", "matrix", "engine"], 1.0
        ),
        SearchDocument(
            4, "Error Rate Trending",
            "Visualize error rates over time to identify spikes, regressions, and correlations with deployments or configuration changes.",
            ["error", "trending", "dashboard"], 1.0
        ),
        SearchDocument(
            5, "Recovery Success Metrics",
            "Track the percentage of successful recoveries after engine faults, segmented by error type and subsystem.",
            ["recovery", "metrics", "success"], 1.0
        ),
        SearchDocument(
            6, "Drift Severity Dashboard",
            "Monitor configuration drift severity across engine clusters, with alerts for high-severity deviations.",
            ["drift", "dashboard", "severity"], 1.0
        ),
        SearchDocument(
            7, "Alert Management: Acknowledge, Snooze, Escalate",
            "Manage alerts with actions: acknowledge for review, snooze for temporary suppression, or escalate for urgent attention.",
            ["alert", "management", "dashboard"], 1.0
        ),
        SearchDocument(
            8, "Dashboard Refresh Strategies",
            "Choose between auto-refresh, manual refresh, or adaptive polling for dashboard data updates.",
            ["dashboard", "refresh", "strategies"], 1.0
        ),
        SearchDocument(
            9, "Real-Time vs Batch Metrics",
            "Compare real-time streaming metrics with batch-processed aggregates for latency and accuracy trade-offs.",
            ["real-time", "batch", "metrics"], 1.0
        ),
        SearchDocument(
            10, "Metric Retention Policies",
            "Define retention periods for different metric classes, balancing storage costs and historical analysis needs.",
            ["metric", "retention", "policy"], 1.0
        ),
        SearchDocument(
            11, "Dashboard Access Control",
            "Implement role-based access to dashboards, ensuring sensitive metrics are only visible to authorized users.",
            ["dashboard", "access", "control"], 1.0
        ),
        SearchDocument(
            12, "Custom Dashboard Views",
            "Allow users to create, save, and share custom dashboard layouts and metric selections.",
            ["dashboard", "custom", "views"], 1.0
        ),
        SearchDocument(
            13, "Metric Correlation Display",
            "Display correlated metrics to help diagnose root causes, using scatter plots and correlation coefficients.",
            ["metric", "correlation", "display"], 1.0
        ),
        SearchDocument(
            14, "Heat Map for Engine Health",
            "A heat map visualizes engine health across clusters, highlighting hotspots and healthy regions.",
            ["heatmap", "engine", "health"], 1.0
        ),
        SearchDocument(
            15, "Time Series Data Management",
            "Efficiently store and query time series data for high-cardinality engine metrics.",
            ["time-series", "data", "management"], 1.0
        ),
        SearchDocument(
            16, "Dashboard Export: JSON, CSV, PDF",
            "Enable dashboard data export in JSON, CSV, and PDF formats for offline analysis and reporting.",
            ["dashboard", "export", "formats"], 1.0
        ),
        SearchDocument(
            17, "SLO Compliance Dashboard",
            "Track Service Level Objective (SLO) compliance with real-time and historical views.",
            ["slo", "compliance", "dashboard"], 1.0
        ),
        SearchDocument(
            18, "Top Errors Leaderboard",
            "Leaderboard ranks the most frequent engine errors, aiding prioritization of fixes.",
            ["errors", "leaderboard", "dashboard"], 1.0
        ),
        SearchDocument(
            19, "Recovery Time Tracking",
            "Measure mean time to recovery (MTTR) for engine incidents, with breakdowns by subsystem.",
            ["recovery", "time", "tracking"], 1.0
        ),
        SearchDocument(
            20, "System Capacity Dashboard",
            "Visualize system capacity utilization, including CPU, memory, disk, and network bandwidth.",
            ["system", "capacity", "dashboard"], 1.0
        ),
        SearchDocument(
            21, "Composite Health Score Algorithm",
            "Details on the weighted scoring algorithm for overall engine health, including normalization and outlier handling.",
            ["health", "score", "algorithm"], 1.0
        ),
        SearchDocument(
            22, "Batch Metric Aggregation",
            "Batch jobs aggregate raw metrics into hourly and daily summaries for trend analysis.",
            ["batch", "aggregation", "metrics"], 1.0
        ),
        SearchDocument(
            23, "Alert Escalation Policy",
            "Define escalation rules for critical alerts, including paging and notification workflows.",
            ["alert", "escalation", "policy"], 1.0
        ),
        SearchDocument(
            24, "Retention Policy Editor",
            "UI for editing and applying metric retention policies per dashboard or metric group.",
            ["retention", "policy", "editor"], 1.0
        ),
        SearchDocument(
            25, "Custom Metric Correlation",
            "Users can select custom metrics to correlate and visualize in the dashboard.",
            ["custom", "metric", "correlation"], 1.0
        ),
        SearchDocument(
            26, "Drift Alerting Integration",
            "Integrate drift severity alerts with external notification systems and incident management.",
            ["drift", "alerting", "integration"], 1.0
        ),
        SearchDocument(
            27, "Export PDF Layouts",
            "Export dashboard layouts as PDFs, preserving visual formatting for reports.",
            ["export", "pdf", "dashboard"], 1.0
        ),
        SearchDocument(
            28, "Real-Time Alert Feed",
            "A real-time feed displays incoming alerts, with filtering and quick action buttons.",
            ["real-time", "alert", "feed"], 1.0
        ),
        SearchDocument(
            29, "Batch Export Scheduler",
            "Schedule regular exports of dashboard data to external storage for compliance.",
            ["batch", "export", "scheduler"], 1.0
        ),
        SearchDocument(
            30, "Access Control Roles",
            "Predefined roles (viewer, editor, admin) determine dashboard access and edit rights.",
            ["access", "control", "roles"], 1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)