import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

# -----------------------------
# SearchDocument and SearchResult
# -----------------------------

class SearchDocument:
    def __init__(self, id: str, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = id
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

# -----------------------------
# SearchIndex
# -----------------------------

class SearchIndex:
    def __init__(self):
        self._documents: Dict[str, SearchDocument] = {}
        self._doc_tokens: Dict[str, List[str]] = {}
        self._inverted_index: Dict[str, Set[str]] = defaultdict(set)
        self._doc_freqs: Dict[str, int] = defaultdict(int)
        self._term_freqs: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self._doc_lengths: Dict[str, int] = defaultdict(int)
        self._avg_doc_length: float = 0.0
        self._lock = threading.RLock()
        self._idf_cache: Dict[str, float] = {}
        self._total_docs: int = 0
        self._tfidf_norms: Dict[str, float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return  # Ignore duplicates
            tokens = self._tokenize(doc.title + ' ' + doc.content + ' ' + ' '.join(doc.tags))
            self._documents[doc.id] = doc
            self._doc_tokens[doc.id] = tokens
            self._doc_lengths[doc.id] = len(tokens)
            tf = Counter(tokens)
            for term, freq in tf.items():
                self._inverted_index[term].add(doc.id)
                self._term_freqs[doc.id][term] = freq
            for term in set(tokens):
                self._doc_freqs[term] += 1
            self._total_docs += 1
            self._avg_doc_length = sum(self._doc_lengths.values()) / self._total_docs
            self._idf_cache.clear()
            self._tfidf_norms[doc.id] = self._compute_tfidf_norm(doc.id)

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        with self._lock:
            query_tokens = self._tokenize(query)
            if not query_tokens:
                return []
            candidate_docs = set()
            for token in query_tokens:
                candidate_docs.update(self._inverted_index.get(token, set()))
            scored = []
            for doc_id in candidate_docs:
                bm25_score = self._score_bm25(doc_id, query_tokens)
                tfidf_score = self._score_tfidf(doc_id, query_tokens)
                doc = self._documents[doc_id]
                # Combine scores: BM25 (0.7), TF-IDF (0.3), doc.weight
                final_score = (0.7 * bm25_score + 0.3 * tfidf_score) * doc.weight
                snippet = self._make_snippet(doc, query_tokens)
                scored.append(SearchResult(doc_id, final_score, doc.title, snippet))
            scored.sort(key=lambda r: r.score, reverse=True)
            return scored[:limit]

    def get_stats(self) -> Dict[str, any]:
        with self._lock:
            return {
                'total_documents': self._total_docs,
                'avg_doc_length': self._avg_doc_length,
                'unique_terms': len(self._doc_freqs),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self._doc_freqs.get(term, 0)
        N = self._total_docs
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: str, query_tokens: List[str]) -> float:
        score = 0.0
        doc_len = self._doc_lengths[doc_id]
        avgdl = self._avg_doc_length if self._avg_doc_length > 0 else 1.0
        tf = self._term_freqs[doc_id]
        for term in query_tokens:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / avgdl)
            s = idf * freq * (self._bm25_k1 + 1) / (denom + 1e-6)
            score += s
        return score

    def _score_tfidf(self, doc_id: str, query_tokens: List[str]) -> float:
        tf = self._term_freqs[doc_id]
        norm = self._tfidf_norms.get(doc_id, 1.0)
        score = 0.0
        query_tf = Counter(query_tokens)
        for term in query_tf:
            if term not in tf:
                continue
            tf_val = tf[term]
            idf = self._compute_idf(term)
            score += (tf_val * idf)
        return score / (norm + 1e-6)

    def _compute_tfidf_norm(self, doc_id: str) -> float:
        tf = self._term_freqs[doc_id]
        norm = 0.0
        for term, freq in tf.items():
            idf = self._compute_idf(term)
            norm += (freq * idf) ** 2
        return math.sqrt(norm)

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], window: int = 30) -> str:
        content = doc.content
        content_tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(content_tokens) if t in query_tokens]
        if not positions:
            return content[:120] + ('...' if len(content) > 120 else '')
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(content_tokens))
        snippet_tokens = content_tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        # Highlight query terms
        for term in set(query_tokens):
            snippet = re.sub(r'\b({})\b'.format(re.escape(term)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet

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
# Pre-seed Domain Documents
# -----------------------------

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            id="1",
            title="Batch Job Scheduling Strategies",
            content="Learn about fixed, dynamic, and priority-based scheduling for batch jobs in distributed systems.",
            tags=["scheduling", "batch", "priority", "distributed"],
            weight=1.0
        ),
        SearchDocument(
            id="2",
            title="Parallel Execution Management in Batch Processing",
            content="Techniques for managing parallel execution of batch jobs, including thread pools, process pools, and task partitioning.",
            tags=["parallel", "execution", "batch", "thread pool", "process pool"],
            weight=1.0
        ),
        SearchDocument(
            id="3",
            title="Rate Limiting in Batch Processing",
            content="Implement rate limiting to control throughput and prevent resource exhaustion during batch job execution.",
            tags=["rate limiting", "batch", "throughput", "resource"],
            weight=1.0
        ),
        SearchDocument(
            id="4",
            title="Retry with Exponential Backoff",
            content="Best practices for implementing retry logic with exponential backoff in batch processing to handle transient failures.",
            tags=["retry", "backoff", "batch", "failure"],
            weight=1.0
        ),
        SearchDocument(
            id="5",
            title="Batch Result Aggregation Techniques",
            content="Aggregate results from parallel batch tasks efficiently using reduction, folding, and streaming aggregation.",
            tags=["aggregation", "batch", "results", "streaming"],
            weight=1.0
        ),
        SearchDocument(
            id="6",
            title="Progress Tracking in Batch Jobs",
            content="Track progress of large batch jobs using checkpoints, progress bars, and status callbacks.",
            tags=["progress", "tracking", "batch", "checkpoint"],
            weight=1.0
        ),
        SearchDocument(
            id="7",
            title="Error Isolation per Batch Item",
            content="Isolate errors to individual batch items to prevent cascading failures and enable partial success.",
            tags=["error", "isolation", "batch", "partial"],
            weight=1.0
        ),
        SearchDocument(
            id="8",
            title="Partial Result Delivery in Batch Processing",
            content="Deliver partial results to clients before the entire batch completes for improved responsiveness.",
            tags=["partial", "results", "batch", "delivery"],
            weight=1.0
        ),
        SearchDocument(
            id="9",
            title="Batch Priority Queuing",
            content="Implement priority queues to manage batch job execution order based on business importance.",
            tags=["priority", "queue", "batch", "scheduling"],
            weight=1.0
        ),
        SearchDocument(
            id="10",
            title="Resource Budgeting per Batch",
            content="Allocate and enforce resource budgets for each batch to ensure fair usage and prevent starvation.",
            tags=["resource", "budget", "batch", "allocation"],
            weight=1.0
        ),
        SearchDocument(
            id="11",
            title="Batch Cancellation Mechanisms",
            content="Enable safe cancellation of running batch jobs with rollback and cleanup strategies.",
            tags=["cancellation", "batch", "rollback", "cleanup"],
            weight=1.0
        ),
        SearchDocument(
            id="12",
            title="Checkpoint and Resume for Large Batches",
            content="Use checkpointing to resume large batch jobs after interruptions, minimizing lost work.",
            tags=["checkpoint", "resume", "batch", "fault tolerance"],
            weight=1.0
        ),
        SearchDocument(
            id="13",
            title="Batch Result Caching",
            content="Cache batch results to avoid redundant computation and improve response times.",
            tags=["caching", "batch", "results", "performance"],
            weight=1.0
        ),
        SearchDocument(
            id="14",
            title="Deduplication within Batches",
            content="Detect and remove duplicate items within a batch to ensure correctness and efficiency.",
            tags=["deduplication", "batch", "duplicates", "efficiency"],
            weight=1.0
        ),
        SearchDocument(
            id="15",
            title="Batch Size Optimization",
            content="Optimize batch sizes to balance throughput, latency, and resource utilization.",
            tags=["batch size", "optimization", "throughput", "latency"],
            weight=1.0
        ),
        SearchDocument(
            id="16",
            title="Memory Management for Large Batches",
            content="Manage memory usage in large batch jobs using streaming, chunking, and spill-to-disk techniques.",
            tags=["memory", "batch", "streaming", "chunking"],
            weight=1.0
        ),
        SearchDocument(
            id="17",
            title="Streaming Results in Batch Processing",
            content="Stream results from batch jobs as they become available to reduce wait times.",
            tags=["streaming", "results", "batch", "latency"],
            weight=1.0
        ),
        SearchDocument(
            id="18",
            title="Batch SLA Enforcement",
            content="Enforce Service Level Agreements (SLAs) for batch jobs using deadlines and monitoring.",
            tags=["sla", "batch", "deadline", "monitoring"],
            weight=1.0
        ),
        SearchDocument(
            id="19",
            title="Batch Cost Estimation",
            content="Estimate and track the cost of batch job execution for budgeting and optimization.",
            tags=["cost", "batch", "estimation", "budgeting"],
            weight=1.0
        ),
        SearchDocument(
            id="20",
            title="Batch Audit Logging",
            content="Maintain audit logs for batch jobs to support compliance and debugging.",
            tags=["audit", "logging", "batch", "compliance"],
            weight=1.0
        ),
        SearchDocument(
            id="21",
            title="Distributed Batch Job Coordination",
            content="Coordinate batch jobs across distributed systems using leader election and consensus protocols.",
            tags=["distributed", "coordination", "batch", "consensus"],
            weight=1.0
        ),
        SearchDocument(
            id="22",
            title="Handling Out-of-Order Results in Batches",
            content="Techniques for managing and reordering out-of-order results in parallel batch processing.",
            tags=["out-of-order", "batch", "results", "reordering"],
            weight=1.0
        ),
        SearchDocument(
            id="23",
            title="Adaptive Batch Scheduling",
            content="Adapt batch scheduling policies based on workload, resource availability, and job priorities.",
            tags=["adaptive", "scheduling", "batch", "workload"],
            weight=1.0
        ),
        SearchDocument(
            id="24",
            title="Monitoring and Alerting for Batch Jobs",
            content="Set up monitoring and alerting to detect failures and performance issues in batch pipelines.",
            tags=["monitoring", "alerting", "batch", "pipeline"],
            weight=1.0
        ),
        SearchDocument(
            id="25",
            title="Batch Job Dependency Management",
            content="Manage dependencies between batch jobs using directed acyclic graphs (DAGs) and dependency resolution.",
            tags=["dependency", "batch", "dag", "resolution"],
            weight=1.0
        ),
        SearchDocument(
            id="26",
            title="Idempotency in Batch Processing",
            content="Ensure idempotency in batch jobs to allow safe retries and avoid duplicate side effects.",
            tags=["idempotency", "batch", "retry", "safety"],
            weight=1.0
        ),
        SearchDocument(
            id="27",
            title="Batch Job Metrics Collection",
            content="Collect metrics such as execution time, throughput, and error rates for batch jobs.",
            tags=["metrics", "batch", "monitoring", "performance"],
            weight=1.0
        ),
        SearchDocument(
            id="28",
            title="Security in Batch Processing",
            content="Apply security best practices for batch jobs, including authentication, authorization, and data encryption.",
            tags=["security", "batch", "authentication", "encryption"],
            weight=1.0
        ),
        SearchDocument(
            id="29",
            title="Multi-Tenancy in Batch Engines",
            content="Support multi-tenancy by isolating resources and data between different batch job submitters.",
            tags=["multi-tenancy", "batch", "isolation", "resources"],
            weight=1.0
        ),
        SearchDocument(
            id="30",
            title="Batch Job Failure Handling",
            content="Handle batch job failures gracefully using retries, compensation, and alerting mechanisms.",
            tags=["failure", "batch", "retry", "compensation"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)