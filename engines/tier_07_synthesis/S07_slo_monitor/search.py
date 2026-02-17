import math
import threading
import heapq
import re
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

# --- Search Index ---

class SearchIndex:
    def __init__(self):
        self._documents: Dict[int, SearchDocument] = {}
        self._inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self._doc_freq: Dict[str, int] = defaultdict(int)
        self._term_freqs: Dict[int, Counter] = {}
        self._doc_lengths: Dict[int, int] = {}
        self._total_doc_length: int = 0
        self._N: int = 0
        self._lock = threading.RLock()
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            tf = Counter(tokens)
            self._documents[doc.id] = doc
            self._term_freqs[doc.id] = tf
            self._doc_lengths[doc.id] = len(tokens)
            self._total_doc_length += len(tokens)
            self._N += 1
            for term in tf:
                self._inverted_index[term].add(doc.id)
                self._doc_freq[term] += 1

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        with self._lock:
            candidate_docs = set()
            for term in query_terms:
                candidate_docs.update(self._inverted_index.get(term, set()))
            scored = []
            for doc_id in candidate_docs:
                bm25_score = self._score_bm25(doc_id, query_terms)
                tfidf_score = self._score_tfidf(doc_id, query_terms)
                doc = self._documents[doc_id]
                score = (bm25_score * 0.7 + tfidf_score * 0.3) * doc.weight
                snippet = self._make_snippet(doc, query_terms)
                scored.append(SearchResult(doc_id, score, doc.title, snippet))
            scored.sort(key=lambda r: r.score, reverse=True)
            return scored[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            avg_dl = self._total_doc_length / self._N if self._N else 0
            return {
                "documents": self._N,
                "avg_doc_length": avg_dl,
                "unique_terms": len(self._inverted_index),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        df = self._doc_freq.get(term, 0)
        if df == 0:
            return 0.0
        return math.log(1 + (self._N - df + 0.5) / (df + 0.5))

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self._term_freqs[doc_id]
        dl = self._doc_lengths[doc_id]
        avg_dl = self._total_doc_length / self._N if self._N else 0
        score = 0.0
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * dl / avg_dl) if avg_dl > 0 else 1
            score += idf * (f * (self._bm25_k1 + 1)) / denom
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self._term_freqs[doc_id]
        dl = self._doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            tf_raw = tf.get(term, 0)
            if tf_raw == 0:
                continue
            tf_norm = tf_raw / dl if dl > 0 else 0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str]) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:160]
            return snippet + "..." if len(content) > 160 else snippet
        start = max(positions[0] - 5, 0)
        end = min(positions[0] + 10, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        return snippet + "..." if end < len(tokens) else snippet

# --- Singleton Factory ---

_search_index_singleton: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_singleton
    with _search_index_lock:
        if _search_index_singleton is None:
            _search_index_singleton = SearchIndex()
            _preseed_documents(_search_index_singleton)
        return _search_index_singleton

# --- Pre-seed Domain Documents ---

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "SLO Definition Standards",
            "Defines the best practices for establishing Service Level Objectives (SLOs), including target, window, and SLI selection. Covers how to align SLOs with business requirements and reliability goals.",
            ["slo", "definition", "standards", "best_practices"],
            1.0
        ),
        SearchDocument(
            2,
            "Error Budget Calculation Explained",
            "Describes how to calculate error budgets from SLO targets. Includes formulas, examples, and how error budgets inform engineering decisions and risk management.",
            ["error_budget", "calculation", "slo"],
            1.0
        ),
        SearchDocument(
            3,
            "Burn Rate Analysis for SLOs",
            "Explains burn rate as a measure of error budget consumption speed. Discusses multi-window burn rate, alerting thresholds, and operational response strategies.",
            ["burn_rate", "analysis", "slo", "alerting"],
            1.0
        ),
        SearchDocument(
            4,
            "Latency Percentile Tracking (p50, p95, p99)",
            "Details how to measure and track latency percentiles (p50, p95, p99) for SLOs. Covers histogram-based approaches and implications for user experience.",
            ["latency", "percentile", "p50", "p95", "p99"],
            1.0
        ),
        SearchDocument(
            5,
            "Throughput SLI Measurement",
            "Provides guidelines for defining and measuring throughput as a Service Level Indicator (SLI). Includes examples for API and streaming services.",
            ["throughput", "sli", "measurement"],
            1.0
        ),
        SearchDocument(
            6,
            "Availability Calculation Methods",
            "Outlines methods for calculating service availability, including request success ratios and uptime/downtime tracking. Discusses impact on SLOs.",
            ["availability", "calculation", "slo"],
            1.0
        ),
        SearchDocument(
            7,
            "SLO Violation Alerting",
            "Covers alerting strategies for SLO violations, including static and dynamic thresholds, multi-window alerting, and reducing alert fatigue.",
            ["slo", "violation", "alerting"],
            1.0
        ),
        SearchDocument(
            8,
            "Error Budget Exhaustion Prediction",
            "Introduces predictive techniques for forecasting error budget exhaustion using historical data, burn rates, and anomaly detection.",
            ["error_budget", "prediction", "burn_rate"],
            1.0
        ),
        SearchDocument(
            9,
            "Multi-Window SLO Rolling",
            "Explains multi-window SLO evaluation, such as short-term and long-term windows, and their role in resilient alerting and error budget policies.",
            ["multi_window", "slo", "rolling"],
            1.0
        ),
        SearchDocument(
            10,
            "Composite SLOs from Multiple SLIs",
            "Describes how to construct composite SLOs by aggregating multiple SLIs, including weighted and logical combinations.",
            ["composite", "slo", "sli", "aggregation"],
            1.0
        ),
        SearchDocument(
            11,
            "Error Budget Policy Design",
            "Discusses policies for error budget spend, freeze, and reset. Includes escalation paths and communication best practices.",
            ["error_budget", "policy", "design"],
            1.0
        ),
        SearchDocument(
            12,
            "Latency SLI Instrumentation",
            "Guides on instrumenting latency SLIs, including request/response tracing, histogram buckets, and percentile calculation.",
            ["latency", "sli", "instrumentation"],
            1.0
        ),
        SearchDocument(
            13,
            "SLI vs SLO vs SLA: Key Differences",
            "Clarifies the distinctions between Service Level Indicators (SLIs), Service Level Objectives (SLOs), and Service Level Agreements (SLAs).",
            ["sli", "slo", "sla", "differences"],
            1.0
        ),
        SearchDocument(
            14,
            "Error Budget Alerts: Multi-Stage",
            "Explains multi-stage alerting based on error budget burn rates and exhaustion predictions, with examples for paging and ticketing.",
            ["error_budget", "alerts", "multi_stage"],
            1.0
        ),
        SearchDocument(
            15,
            "SLO Review and Iteration",
            "Best practices for periodic SLO review, iteration, and alignment with evolving product and reliability needs.",
            ["slo", "review", "iteration"],
            1.0
        ),
        SearchDocument(
            16,
            "Availability SLI: Request Success Ratio",
            "Defines how to measure availability using the ratio of successful requests to total requests, with pitfalls and edge cases.",
            ["availability", "sli", "request_success"],
            1.0
        ),
        SearchDocument(
            17,
            "Latency SLOs for User Experience",
            "Discusses setting latency SLOs that reflect real user experience, including tail latency and percentile targets.",
            ["latency", "slo", "user_experience"],
            1.0
        ),
        SearchDocument(
            18,
            "Composite SLOs: Logical AND/OR",
            "Shows how to combine SLIs using logical AND/OR to form composite SLOs, with examples and trade-offs.",
            ["composite", "slo", "logical_and", "logical_or"],
            1.0
        ),
        SearchDocument(
            19,
            "Error Budget Burn Rate Calculation",
            "Provides formulas and code snippets for calculating error budget burn rates over different time windows.",
            ["error_budget", "burn_rate", "calculation"],
            1.0
        ),
        SearchDocument(
            20,
            "Throughput SLI for Streaming Services",
            "Special considerations for throughput SLIs in streaming and event-driven architectures.",
            ["throughput", "sli", "streaming"],
            1.0
        ),
        SearchDocument(
            21,
            "SLO Alert Fatigue Mitigation",
            "Techniques to reduce alert fatigue from SLO-based alerting, including multi-window and severity-based approaches.",
            ["slo", "alert_fatigue", "alerting"],
            1.0
        ),
        SearchDocument(
            22,
            "Error Budget Visualization",
            "Describes dashboards and visualization techniques for tracking error budget status and burn rate trends.",
            ["error_budget", "visualization", "dashboard"],
            1.0
        ),
        SearchDocument(
            23,
            "Latency Histogram Buckets",
            "How to select and configure histogram buckets for accurate latency percentile computation.",
            ["latency", "histogram", "buckets"],
            1.0
        ),
        SearchDocument(
            24,
            "Availability SLOs for APIs",
            "Setting and measuring availability SLOs for API endpoints, including synthetic monitoring and real-user metrics.",
            ["availability", "slo", "api"],
            1.0
        ),
        SearchDocument(
            25,
            "Composite SLO Weighting Strategies",
            "Strategies for weighting SLIs in composite SLOs, including reliability tiers and criticality.",
            ["composite", "slo", "weighting"],
            1.0
        ),
        SearchDocument(
            26,
            "SLO Violation Root Cause Analysis",
            "Methods for investigating and remediating SLO violations, with links to incident management.",
            ["slo", "violation", "root_cause"],
            1.0
        ),
        SearchDocument(
            27,
            "Error Budget Reset Policies",
            "How and when to reset error budgets, including calendar-based and event-based resets.",
            ["error_budget", "reset", "policy"],
            1.0
        ),
        SearchDocument(
            28,
            "Multi-Window Alerting for SLOs",
            "Implementing alerting strategies that consider both short-term and long-term SLO burn rates.",
            ["multi_window", "alerting", "slo"],
            1.0
        ),
        SearchDocument(
            29,
            "SLI Instrumentation Pitfalls",
            "Common mistakes in SLI instrumentation and how to avoid them for accurate SLO measurement.",
            ["sli", "instrumentation", "pitfalls"],
            1.0
        ),
        SearchDocument(
            30,
            "SLOs for Distributed Systems",
            "Challenges and solutions for defining SLOs in distributed and microservices architectures.",
            ["slo", "distributed_systems", "microservices"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)