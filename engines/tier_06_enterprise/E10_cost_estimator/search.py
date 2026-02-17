import math
import threading
import re
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
    def __init__(self):
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.doc_tags: Dict[str, List[str]] = {}
        self.doc_weights: Dict[str, float] = {}
        self.total_terms: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._avg_doc_len: float = 0.0

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.total_terms += len(tokens)
            self.doc_tags[doc.id] = doc.tags
            self.doc_weights[doc.id] = doc.weight
            term_counter = Counter(tokens)
            for term, freq in term_counter.items():
                self.term_freqs[term][doc.id] = freq
                self.term_doc_freq[term] += 1
            self._idf_cache.clear()
            self._avg_doc_len = sum(self.doc_lengths.values()) / max(len(self.doc_lengths), 1)

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        candidate_docs = set()
        for term in query_tokens:
            candidate_docs.update(self.term_freqs.get(term, {}).keys())
        scores: Dict[str, float] = {}
        for doc_id in candidate_docs:
            if use_tfidf:
                scores[doc_id] = self._score_tfidf(doc_id, query_tokens)
            else:
                scores[doc_id] = self._score_bm25(doc_id, query_tokens)
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                'num_documents': len(self.documents),
                'avg_doc_length': self._avg_doc_len,
                'total_terms': self.total_terms,
                'unique_terms': len(self.term_doc_freq),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        N = len(self.documents)
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: str, query_tokens: List[str], k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        avg_doc_len = self._avg_doc_len
        doc_weight = self.doc_weights.get(doc_id, 1.0)
        for term in query_tokens:
            idf = self._compute_idf(term)
            freq = self.term_freqs.get(term, {}).get(doc_id, 0)
            numerator = freq * (k1 + 1)
            denominator = freq + k1 * (1 - b + b * (doc_len / (avg_doc_len + 1e-6)))
            term_score = idf * (numerator / (denominator + 1e-6))
            score += term_score
        score *= doc_weight
        return score

    def _score_tfidf(self, doc_id: str, query_tokens: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        doc_weight = self.doc_weights.get(doc_id, 1.0)
        for term in query_tokens:
            tf = self.term_freqs.get(term, {}).get(doc_id, 0) / (doc_len + 1e-6)
            idf = self._compute_idf(term)
            score += tf * idf
        score *= doc_weight
        return score

    def _make_snippet(self, content: str, query_tokens: List[str], window: int = 40) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            return ' '.join(tokens[:window])
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return snippet

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
            "1", "LLM Token Cost Estimation",
            "Estimate the cost of LLM token usage for queries, including prompt and completion tokens. Supports OpenAI, Anthropic, and custom engines.",
            ["llm", "token", "cost", "estimation"], 1.0
        ),
        SearchDocument(
            "2", "External API Call Cost Estimation",
            "Calculate the cost incurred by external API calls, including per-call pricing, rate limits, and response size factors.",
            ["api", "external", "cost", "estimation"], 1.0
        ),
        SearchDocument(
            "3", "CPU Compute Cost Estimation",
            "Estimate CPU compute costs for inference, preprocessing, and postprocessing operations. Includes per-core and per-second pricing.",
            ["cpu", "compute", "cost", "estimation"], 1.0
        ),
        SearchDocument(
            "4", "Storage Operation Cost Estimation",
            "Assess the cost of storage operations such as reads, writes, and deletes. Supports cloud and local storage pricing models.",
            ["storage", "operation", "cost", "estimation"], 1.0
        ),
        SearchDocument(
            "5", "Wall-Clock Time Estimation",
            "Estimate wall-clock time for engine operations, including latency, throughput, and concurrency factors.",
            ["wall-clock", "time", "estimation"], 1.0
        ),
        SearchDocument(
            "6", "Daily Budget Enforcement",
            "Enforce daily budgets for engine usage, preventing overages and supporting automatic throttling or degradation.",
            ["budget", "daily", "enforcement"], 1.0
        ),
        SearchDocument(
            "7", "Monthly Budget Enforcement",
            "Enforce monthly budgets for engine usage, tracking cumulative costs and supporting alerts for approaching limits.",
            ["budget", "monthly", "enforcement"], 1.0
        ),
        SearchDocument(
            "8", "Response Mode Cost Multiplier",
            "Apply cost multipliers based on response modes (e.g., streaming, batch, synchronous) to reflect operational overhead.",
            ["response", "mode", "cost", "multiplier"], 1.0
        ),
        SearchDocument(
            "9", "Multi-Engine Chain Cost Estimation",
            "Estimate costs for chained multi-engine queries, including cumulative token, compute, and API call costs.",
            ["multi-engine", "chain", "cost", "estimation"], 1.0
        ),
        SearchDocument(
            "10", "Batch Query Cost Estimation",
            "Estimate costs for batch queries, including per-query and aggregate pricing, and efficiency factors.",
            ["batch", "query", "cost", "estimation"], 1.0
        ),
        SearchDocument(
            "11", "Doctrine Cache Hit Cost Reduction",
            "Reduce costs via doctrine cache hits, tracking cache effectiveness and calculating savings for repeated queries.",
            ["cache", "doctrine", "cost", "reduction"], 1.0
        ),
        SearchDocument(
            "12", "Document Length Cost Factor",
            "Factor document length into cost estimation, including long-form completions and retrieval operations.",
            ["document", "length", "cost", "factor"], 1.0
        ),
        SearchDocument(
            "13", "Query Complexity Scoring for Cost",
            "Score query complexity to adjust cost estimates, including semantic depth, token count, and retrieval difficulty.",
            ["query", "complexity", "scoring", "cost"], 1.0
        ),
        SearchDocument(
            "14", "Cloud Retriever Overhead Cost",
            "Estimate overhead costs for cloud retriever operations, including network latency and per-request surcharges.",
            ["cloud", "retriever", "overhead", "cost"], 1.0
        ),
        SearchDocument(
            "15", "Cost-Aware Engine Routing",
            "Route queries to engines based on cost profiles, supporting dynamic routing and fallback strategies under budget pressure.",
            ["cost-aware", "engine", "routing"], 1.0
        ),
        SearchDocument(
            "16", "Free Tier Usage Tracking",
            "Track free tier usage for engines, including quota enforcement and automatic upgrade triggers.",
            ["free-tier", "usage", "tracking"], 1.0
        ),
        SearchDocument(
            "17", "Automatic Mode Degradation Under Budget Pressure",
            "Automatically degrade response modes or quality when budgets are tight, preserving essential functionality.",
            ["automatic", "mode", "degradation", "budget"], 1.0
        ),
        SearchDocument(
            "18", "Historical Cost Analysis and Trend Detection",
            "Analyze historical cost data to detect trends, forecast future usage, and optimize engine configuration.",
            ["historical", "cost", "analysis", "trend"], 1.0
        ),
        SearchDocument(
            "19", "Cost Profile for Engine {eng_id}",
            "View and manage cost profiles for individual engines, including pricing, usage history, and optimization recommendations.",
            ["cost", "profile", "engine"], 1.0
        ),
        SearchDocument(
            "20", "Token Cost Estimator API",
            "API endpoint for estimating token costs, supporting batch and streaming queries with detailed breakdowns.",
            ["token", "cost", "estimator", "api"], 1.0
        ),
        SearchDocument(
            "21", "Budget Enforcement Strategies",
            "Strategies for enforcing budgets, including soft and hard limits, alerts, and adaptive throttling.",
            ["budget", "enforcement", "strategy"], 1.0
        ),
        SearchDocument(
            "22", "Cost-Aware Query Planning",
            "Plan queries with cost-awareness, optimizing for minimal expense and maximal coverage.",
            ["cost-aware", "query", "planning"], 1.0
        ),
        SearchDocument(
            "23", "Engine Chain Cost Aggregator",
            "Aggregate costs across chained engine operations, providing unified cost reporting and optimization.",
            ["engine", "chain", "cost", "aggregator"], 1.0
        ),
        SearchDocument(
            "24", "Storage Cost Optimization",
            "Optimize storage operation costs, including tiered storage, compression, and access pattern analysis.",
            ["storage", "cost", "optimization"], 1.0
        ),
        SearchDocument(
            "25", "Compute Cost Optimization",
            "Optimize compute costs, including workload scheduling, resource scaling, and idle time reduction.",
            ["compute", "cost", "optimization"], 1.0
        ),
        SearchDocument(
            "26", "Token Cost Forecasting",
            "Forecast token costs based on historical usage and projected query volumes.",
            ["token", "cost", "forecasting"], 1.0
        ),
        SearchDocument(
            "27", "API Call Cost Forecasting",
            "Forecast API call costs, including seasonal trends and anomaly detection.",
            ["api", "call", "cost", "forecasting"], 1.0
        ),
        SearchDocument(
            "28", "Budget Alerting and Notification",
            "Alert users and administrators when budgets approach limits, supporting email, webhook, and dashboard notifications.",
            ["budget", "alert", "notification"], 1.0
        ),
        SearchDocument(
            "29", "Cost Trend Visualization",
            "Visualize cost trends over time, supporting charts and dashboards for actionable insights.",
            ["cost", "trend", "visualization"], 1.0
        ),
        SearchDocument(
            "30", "Cost-Aware Document Retrieval",
            "Retrieve documents with cost-awareness, prioritizing cache hits and minimizing expensive operations.",
            ["cost-aware", "document", "retrieval"], 1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)