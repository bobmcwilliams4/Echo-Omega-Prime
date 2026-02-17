import math
import re
import threading
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
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_term_freqs: Dict[str, Counter] = {}
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.avg_doc_len: float = 0.0
        self.total_docs: int = 0
        self.lock = threading.RLock()

    def add_document(self, document: SearchDocument):
        with self.lock:
            if document.id in self.documents:
                # Remove old document stats
                old_tf = self.doc_term_freqs.get(document.id)
                if old_tf:
                    for term in old_tf:
                        self.term_doc_freqs[term] -= 1
                        if self.term_doc_freqs[term] <= 0:
                            del self.term_doc_freqs[term]
                self.total_docs -= 1

            tokens = self._tokenize(document.title + " " + document.content + " " + " ".join(document.tags))
            term_freq = Counter(tokens)
            for term in term_freq:
                self.term_doc_freqs[term] += 1

            self.documents[document.id] = document
            self.doc_term_freqs[document.id] = term_freq
            self.total_docs = len(self.documents)
            self.avg_doc_len = self._compute_avg_doc_len()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        with self.lock:
            query_terms = self._tokenize(query)
            if not query_terms or self.total_docs == 0:
                return []

            idf = {term: self._compute_idf(term) for term in query_terms}
            scores: Dict[str, float] = defaultdict(float)

            for doc_id, term_freqs in self.doc_term_freqs.items():
                doc_len = sum(term_freqs.values())
                score = 0.0
                for term in query_terms:
                    tf = term_freqs.get(term, 0)
                    if tf == 0:
                        continue
                    score += self._score_bm25(tf, idf.get(term, 0.0), doc_len)
                if score > 0:
                    # Incorporate document weight
                    score *= self.documents[doc_id].weight
                    scores[doc_id] = score

            ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
            results = []
            for doc_id, score in ranked:
                doc = self.documents[doc_id]
                snippet = self._make_snippet(doc.content, query_terms)
                results.append(SearchResult(doc_id=doc_id, score=score, title=doc.title, snippet=snippet))
            return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "total_documents": self.total_docs,
                "average_document_length": self.avg_doc_len,
                "unique_terms": len(self.term_doc_freqs),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        df = self.term_doc_freqs.get(term, 0)
        if df == 0:
            return 0.0
        return math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))

    def _score_bm25(self, tf: int, idf: float, doc_len: int) -> float:
        norm_tf = tf
        denom = tf + self.k1 * (1 - self.b + self.b * (doc_len / self.avg_doc_len if self.avg_doc_len > 0 else 1))
        score = idf * ((norm_tf * (self.k1 + 1)) / denom) if denom > 0 else 0.0
        return score

    def _compute_avg_doc_len(self) -> float:
        if not self.doc_term_freqs:
            return 0.0
        total_len = sum(sum(freqs.values()) for freqs in self.doc_term_freqs.values())
        return total_len / len(self.doc_term_freqs)

    def _make_snippet(self, content: str, query_terms: List[str], snippet_length: int = 160) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            start = 0
            while True:
                idx = content_lower.find(term, start)
                if idx == -1:
                    break
                positions.append(idx)
                start = idx + 1
        if not positions:
            snippet = content[:snippet_length].strip()
            if len(content) > snippet_length:
                snippet += "..."
            return snippet

        positions.sort()
        start_pos = max(positions[0] - snippet_length // 4, 0)
        end_pos = start_pos + snippet_length
        snippet = content[start_pos:end_pos].strip()
        if start_pos > 0:
            snippet = "..." + snippet
        if end_pos < len(content):
            snippet += "..."
        return snippet


_singleton_instance: Optional[SearchIndex] = None
_singleton_lock = threading.Lock()


def get_search_index() -> SearchIndex:
    global _singleton_instance
    if _singleton_instance is None:
        with _singleton_lock:
            if _singleton_instance is None:
                _singleton_instance = SearchIndex()
                _preseed_documents(_singleton_instance)
    return _singleton_instance


def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            doc_id="doc001",
            title="Content-Based Message Routing Overview",
            content=(
                "Content-Based Message Routing directs messages to destinations "
                "based on message content, enabling flexible and dynamic routing "
                "in event-driven architectures."
            ),
            tags=["content-based", "routing", "message", "EDA"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc002",
            title="Topic-Based Message Routing Explained",
            content=(
                "Topic-Based Message Routing uses topics or subjects to route messages "
                "to subscribers interested in those topics, commonly used in pub-sub systems."
            ),
            tags=["topic-based", "routing", "publish-subscribe", "pub-sub"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc003",
            title="Publish-Subscribe Event Pattern Fundamentals",
            content=(
                "The Publish-Subscribe pattern decouples message producers and consumers "
                "through topics or channels, supporting scalable and asynchronous event processing."
            ),
            tags=["publish-subscribe", "event pattern", "pub-sub", "EDA"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc004",
            title="Fan-Out and Fan-In Event Patterns",
            content=(
                "Fan-Out distributes a single event to multiple consumers, while Fan-In aggregates "
                "multiple events into a single processing stream, enabling parallelism and coordination."
            ),
            tags=["fan-out", "fan-in", "event pattern", "parallelism"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="doc005",
            title="Event-Driven Architecture (EDA) Principles",
            content=(
                "Event-Driven Architecture promotes reactive systems where components communicate "
                "through events, improving scalability and responsiveness."
            ),
            tags=["EDA", "event-driven", "architecture", "reactive"],
            weight=1.4,
        ),
        SearchDocument(
            doc_id="doc006",
            title="Event Sourcing Explained",
            content=(
                "Event Sourcing stores state changes as a sequence of events, allowing "
                "reconstruction of current state and auditability."
            ),
            tags=["event sourcing", "state", "events", "audit"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc007",
            title="CQRS: Command Query Responsibility Segregation",
            content=(
                "CQRS separates read and write operations into different models, optimizing "
                "performance and scalability in complex systems."
            ),
            tags=["CQRS", "command", "query", "segregation"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc008",
            title="Data Flow Optimization and Pipeline Parallelism",
            content=(
                "Optimizing data flow and leveraging pipeline parallelism enhances throughput "
                "and reduces latency in event processing pipelines."
            ),
            tags=["data flow", "optimization", "pipeline", "parallelism"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc009",
            title="Backpressure Handling in Reactive Streams",
            content=(
                "Backpressure mechanisms prevent overwhelming consumers by controlling data flow "
                "rates in reactive stream processing."
            ),
            tags=["backpressure", "reactive streams", "flow control"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc010",
            title="Circuit Breaker Pattern with Hystrix and Resilience4j",
            content=(
                "Circuit Breakers improve system resilience by detecting failures and "
                "stopping cascading faults using libraries like Hystrix and Resilience4j."
            ),
            tags=["circuit breaker", "hystrix", "resilience4j", "fault tolerance"],
            weight=1.4,
        ),
        SearchDocument(
            doc_id="doc011",
            title="Retry Strategies: Exponential Backoff, Jitter, and Decorrelated",
            content=(
                "Retry strategies with exponential backoff and jitter reduce retry storms "
                "and improve reliability in distributed systems."
            ),
            tags=["retry", "exponential backoff", "jitter", "decorrelated"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc012",
            title="Dead Letter Queue and Poison Message Handling",
            content=(
                "Dead Letter Queues capture messages that cannot be processed, enabling "
                "analysis and handling of poison messages."
            ),
            tags=["dead letter queue", "poison message", "error handling"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc013",
            title="Message Serialization Formats: Protobuf, Avro, JSON",
            content=(
                "Serialization formats like Protobuf, Avro, and JSON enable efficient "
                "and interoperable message exchange."
            ),
            tags=["serialization", "protobuf", "avro", "json"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc014",
            title="Saga Orchestration and Choreography Patterns",
            content=(
                "Saga patterns manage distributed transactions using orchestration or choreography "
                "to maintain eventual consistency."
            ),
            tags=["saga", "orchestration", "choreography", "transactions"],
            weight=1.4,
        ),
        SearchDocument(
            doc_id="doc015",
            title="Eventual Consistency in Distributed Systems",
            content=(
                "Eventual consistency ensures data convergence over time in distributed environments, "
                "trading off immediate consistency for availability."
            ),
            tags=["eventual consistency", "distributed systems", "CAP theorem"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc016",
            title="BASE Theorem and CAP Tradeoffs",
            content=(
                "BASE (Basically Available, Soft state, Eventual consistency) complements CAP theorem "
                "tradeoffs in distributed system design."
            ),
            tags=["BASE theorem", "CAP theorem", "distributed systems"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc017",
            title="Load Balancing Techniques: Round-Robin, Weighted, Least-Connections",
            content=(
                "Load balancing distributes traffic using round-robin, weighted, or least-connections "
                "strategies to optimize resource utilization."
            ),
            tags=["load balancing", "round-robin", "weighted", "least-connections"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc018",
            title="Service Mesh Architecture: Sidecar Proxy, Data Plane, Control Plane",
            content=(
                "Service Mesh uses sidecar proxies and separates data and control planes to manage "
                "microservice communication."
            ),
            tags=["service mesh", "sidecar proxy", "data plane", "control plane"],
            weight=1.4,
        ),
        SearchDocument(
            doc_id="doc019",
            title="Connection Pooling: Lifecycle Management and Sizing",
            content=(
                "Connection pooling improves performance by reusing connections with proper lifecycle "
                "management and sizing."
            ),
            tags=["connection pooling", "lifecycle", "sizing", "performance"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc020",
            title="Rate Limiting Algorithms: Token Bucket, Sliding Window, Fixed Window",
            content=(
                "Rate limiting controls request rates using algorithms like token bucket, sliding window, "
                "and fixed window to protect services."
            ),
            tags=["rate limiting", "token bucket", "sliding window", "fixed window"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc021",
            title="Bulkhead Isolation: Thread Pool, Semaphore, Timeout Management",
            content=(
                "Bulkhead isolation prevents cascading failures by isolating resources using thread pools, "
                "semaphores, and timeouts."
            ),
            tags=["bulkhead", "isolation", "thread pool", "semaphore", "timeout"],
            weight=1.4,
        ),
        SearchDocument(
            doc_id="doc022",
            title="Cascading Deadline Propagation Techniques",
            content=(
                "Cascading deadline propagation ensures timeouts propagate through distributed calls, "
                "improving system responsiveness."
            ),
            tags=["deadline propagation", "timeouts", "distributed systems"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc023",
            title="Health Check Propagation: Liveness, Readiness, Startup",
            content=(
                "Health checks monitor service status with liveness, readiness, and startup probes "
                "to support orchestration."
            ),
            tags=["health check", "liveness", "readiness", "startup"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc024",
            title="Service Discovery Methods: Client-Side, Server-Side, DNS",
            content=(
                "Service discovery enables dynamic service location using client-side, server-side, "
                "and DNS-based approaches."
            ),
            tags=["service discovery", "client-side", "server-side", "DNS"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc025",
            title="API Gateway Pattern: Aggregation, Routing, Authentication",
            content=(
                "API Gateways provide a single entry point for clients, handling aggregation, routing, "
                "and authentication."
            ),
            tags=["API gateway", "aggregation", "routing", "authentication"],
            weight=1.4,
        ),
        SearchDocument(
            doc_id="doc026",
            title="Reactive Streams and Backpressure Management",
            content=(
                "Reactive streams provide asynchronous stream processing with non-blocking backpressure "
                "management to handle varying data rates."
            ),
            tags=["reactive streams", "backpressure", "asynchronous"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc027",
            title="Message Serialization Best Practices",
            content=(
                "Choosing the right serialization format affects performance, compatibility, and "
                "schema evolution in messaging systems."
            ),
            tags=["serialization", "best practices", "protobuf", "avro", "json"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc028",
            title="Distributed Transaction Management with Sagas",
            content=(
                "Sagas coordinate distributed transactions by breaking them into smaller, compensatable "
                "steps to maintain consistency."
            ),
            tags=["distributed transactions", "saga", "compensation", "consistency"],
            weight=1.4,
        ),
    ]

    for doc in docs:
        index.add_document(doc)