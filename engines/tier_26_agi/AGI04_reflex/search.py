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
        self._documents: Dict[int, SearchDocument] = {}
        self._inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_length: float = 0.0
        self._idf: Dict[str, float] = {}
        self._lock = threading.RLock()
        self._total_docs = 0
        self._doc_freq: Dict[str, int] = defaultdict(int)
        self._tokenizer = re.compile(r'\b\w+\b')
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            tokens = self._tokenize(doc.title + ' ' + doc.content + ' ' + ' '.join(doc.tags))
            token_counts = Counter(tokens)
            self._documents[doc.id] = doc
            self._doc_lengths[doc.id] = len(tokens)
            for token, count in token_counts.items():
                self._inverted_index[token][doc.id] = count
                self._doc_freq[token] += 1
            self._total_docs += 1
            self._avg_doc_length = sum(self._doc_lengths.values()) / self._total_docs
            self._compute_idf()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        with self._lock:
            query_tokens = self._tokenize(query)
            candidate_docs = set()
            for token in query_tokens:
                candidate_docs.update(self._inverted_index.get(token, {}).keys())
            scored_results: List[Tuple[int, float]] = []
            for doc_id in candidate_docs:
                bm25_score = self._score_bm25(doc_id, query_tokens)
                tfidf_score = self._score_tfidf(doc_id, query_tokens)
                doc_weight = self._documents[doc_id].weight
                score = 0.7 * bm25_score + 0.3 * tfidf_score
                score *= doc_weight
                scored_results.append((doc_id, score))
            scored_results.sort(key=lambda x: x[1], reverse=True)
            results = []
            for doc_id, score in scored_results[:limit]:
                doc = self._documents[doc_id]
                snippet = self._make_snippet(doc, query_tokens)
                results.append(SearchResult(doc_id, score, doc.title, snippet))
            return results

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                'total_documents': self._total_docs,
                'avg_doc_length': self._avg_doc_length,
                'unique_terms': len(self._inverted_index),
            }

    def _tokenize(self, text: str) -> List[str]:
        return [t.lower() for t in self._tokenizer.findall(text)]

    def _compute_idf(self):
        N = self._total_docs
        for term, df in self._doc_freq.items():
            self._idf[term] = math.log(1 + (N - df + 0.5) / (df + 0.5))

    def _score_bm25(self, doc_id: int, query_tokens: List[str]) -> float:
        score = 0.0
        doc_len = self._doc_lengths[doc_id]
        avg_dl = self._avg_doc_length if self._avg_doc_length > 0 else 1.0
        for token in query_tokens:
            if token not in self._inverted_index:
                continue
            f = self._inverted_index[token].get(doc_id, 0)
            if f == 0:
                continue
            idf = self._idf.get(token, 0.0)
            denom = f + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / avg_dl)
            numer = f * (self._bm25_k1 + 1)
            score += idf * numer / denom
        return score

    def _score_tfidf(self, doc_id: int, query_tokens: List[str]) -> float:
        score = 0.0
        doc_len = self._doc_lengths[doc_id]
        for token in query_tokens:
            tf = self._inverted_index[token].get(doc_id, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_len
            idf = self._idf.get(token, 0.0)
            score += tf_norm * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], max_len: int = 160) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            snippet = content[:max_len]
            if len(content) > max_len:
                snippet += '...'
            return snippet
        start = max(positions[0] - 5, 0)
        end = min(positions[0] + 10, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for qt in set(query_tokens):
            snippet = re.sub(rf'\b({re.escape(qt)})\b', r'**\1**', snippet, flags=re.IGNORECASE)
        if len(snippet) > max_len:
            snippet = snippet[:max_len] + '...'
        return snippet

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    if _search_index_instance is None:
        with _search_index_lock:
            if _search_index_instance is None:
                _search_index_instance = SearchIndex()
                _preseed_documents(_search_index_instance)
    return _search_index_instance

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Circuit Breaker Pattern Overview",
            "The Circuit Breaker pattern prevents an application from repeatedly trying to execute an operation that's likely to fail. This is essential for building resilient distributed systems.",
            ["circuit breaker", "resilience", "patterns"],
            1.0
        ),
        SearchDocument(
            2,
            "Hot Path Optimization Techniques",
            "Optimizing the hot path in your application can yield significant performance improvements. Focus on reducing latency and minimizing resource contention.",
            ["hot path", "optimization", "performance"],
            1.0
        ),
        SearchDocument(
            3,
            "Emergency Incident Response Workflow",
            "Effective incident response requires clear workflows, rapid detection, and prioritized mitigation. Automation can accelerate response times.",
            ["incident response", "emergency", "workflow"],
            1.0
        ),
        SearchDocument(
            4,
            "Priority Queue Management in Distributed Systems",
            "Priority queues help manage tasks with different urgency levels. Use efficient data structures to ensure high throughput and fairness.",
            ["priority queue", "distributed systems", "management"],
            1.0
        ),
        SearchDocument(
            5,
            "Graceful Degradation Strategies",
            "Graceful degradation ensures that when parts of a system fail, the overall system continues to operate in a reduced capacity instead of failing completely.",
            ["graceful degradation", "resilience", "failover"],
            1.0
        ),
        SearchDocument(
            6,
            "Implementing Circuit Breakers in Python",
            "Python provides several libraries for implementing the Circuit Breaker pattern. Key considerations include failure thresholds and recovery timeouts.",
            ["circuit breaker", "python", "implementation"],
            1.0
        ),
        SearchDocument(
            7,
            "Monitoring and Alerting for Hot Paths",
            "Monitoring hot paths is crucial for early detection of bottlenecks. Integrate alerting systems to notify teams of performance regressions.",
            ["hot path", "monitoring", "alerting"],
            1.0
        ),
        SearchDocument(
            8,
            "Automated Incident Response Playbooks",
            "Automated playbooks can standardize and accelerate incident response, reducing manual intervention and human error.",
            ["incident response", "automation", "playbooks"],
            1.0
        ),
        SearchDocument(
            9,
            "Designing Priority Queues for Low Latency",
            "Low-latency priority queues are essential for real-time systems. Consider lock-free algorithms and memory-efficient data structures.",
            ["priority queue", "low latency", "design"],
            1.0
        ),
        SearchDocument(
            10,
            "Graceful Degradation in Microservices",
            "Microservices architectures benefit from graceful degradation by isolating failures and providing fallback mechanisms.",
            ["graceful degradation", "microservices", "fallback"],
            1.0
        ),
        SearchDocument(
            11,
            "Circuit Breaker States Explained",
            "Circuit breakers typically have three states: closed, open, and half-open. Transitions depend on error rates and recovery policies.",
            ["circuit breaker", "states", "error handling"],
            1.0
        ),
        SearchDocument(
            12,
            "Profiling Hot Paths in Production",
            "Production profiling tools can identify hot paths by sampling stack traces and measuring execution times.",
            ["hot path", "profiling", "production"],
            1.0
        ),
        SearchDocument(
            13,
            "Incident Response Communication Protocols",
            "Clear communication protocols are vital during incident response to coordinate teams and stakeholders.",
            ["incident response", "communication", "protocols"],
            1.0
        ),
        SearchDocument(
            14,
            "Priority Queue Backpressure Mechanisms",
            "Backpressure in priority queues prevents overload by controlling the rate at which tasks are accepted.",
            ["priority queue", "backpressure", "overload"],
            1.0
        ),
        SearchDocument(
            15,
            "Graceful Degradation User Experience",
            "Designing for graceful degradation includes providing informative error messages and alternative functionality.",
            ["graceful degradation", "user experience", "ux"],
            1.0
        ),
        SearchDocument(
            16,
            "Advanced Circuit Breaker Metrics",
            "Track metrics such as failure rate, throughput, and mean time to recovery to tune circuit breaker behavior.",
            ["circuit breaker", "metrics", "monitoring"],
            1.0
        ),
        SearchDocument(
            17,
            "Hot Path Optimization Case Study",
            "A case study on optimizing a payment processing hot path, reducing latency by 40% through code refactoring.",
            ["hot path", "optimization", "case study"],
            1.0
        ),
        SearchDocument(
            18,
            "Incident Response Automation Tools",
            "Modern incident response leverages automation tools for detection, triage, and remediation.",
            ["incident response", "automation", "tools"],
            1.0
        ),
        SearchDocument(
            19,
            "Fairness in Priority Queue Scheduling",
            "Ensuring fairness in priority queue scheduling prevents starvation and improves system reliability.",
            ["priority queue", "fairness", "scheduling"],
            1.0
        ),
        SearchDocument(
            20,
            "Graceful Degradation Patterns for APIs",
            "API design should include graceful degradation patterns such as rate limiting and fallback responses.",
            ["graceful degradation", "api", "patterns"],
            1.0
        ),
        SearchDocument(
            21,
            "Timeouts and Retries with Circuit Breakers",
            "Combine timeouts and retries with circuit breakers to handle transient failures effectively.",
            ["circuit breaker", "timeouts", "retries"],
            1.0
        ),
        SearchDocument(
            22,
            "Hot Path Bottleneck Analysis",
            "Analyzing bottlenecks in hot paths helps prioritize optimization efforts for maximum impact.",
            ["hot path", "bottleneck", "analysis"],
            1.0
        ),
        SearchDocument(
            23,
            "Incident Response Postmortem Best Practices",
            "Postmortems after incidents help teams learn and improve future response strategies.",
            ["incident response", "postmortem", "best practices"],
            1.0
        ),
        SearchDocument(
            24,
            "Dynamic Priority Queue Adjustment",
            "Dynamically adjusting priority queues based on workload can improve responsiveness and resource utilization.",
            ["priority queue", "dynamic", "adjustment"],
            1.0
        ),
        SearchDocument(
            25,
            "Graceful Degradation in Frontend Applications",
            "Frontend applications should degrade gracefully by loading essential features first and deferring non-critical resources.",
            ["graceful degradation", "frontend", "applications"],
            1.0
        ),
        SearchDocument(
            26,
            "Distributed Circuit Breaker Coordination",
            "Coordinating circuit breakers across distributed services requires shared state and consistent policies.",
            ["circuit breaker", "distributed", "coordination"],
            1.0
        ),
        SearchDocument(
            27,
            "Hot Path Optimization in Real-Time Systems",
            "Real-time systems demand aggressive hot path optimization to meet strict latency requirements.",
            ["hot path", "real-time", "optimization"],
            1.0
        ),
        SearchDocument(
            28,
            "Incident Response Escalation Policies",
            "Escalation policies define when and how incidents are escalated to higher support tiers.",
            ["incident response", "escalation", "policies"],
            1.0
        ),
        SearchDocument(
            29,
            "Priority Queue Starvation Prevention",
            "Preventing starvation in priority queues ensures all tasks eventually receive processing time.",
            ["priority queue", "starvation", "prevention"],
            1.0
        ),
        SearchDocument(
            30,
            "Graceful Degradation for Mobile Apps",
            "Mobile apps should implement graceful degradation to handle poor network conditions and limited resources.",
            ["graceful degradation", "mobile", "apps"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)