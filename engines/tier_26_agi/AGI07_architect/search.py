import math
import threading
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
        self._doc_term_freqs: Dict[int, Counter] = {}
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_len: float = 0.0
        self._doc_count: int = 0
        self._term_doc_freq: Dict[str, int] = defaultdict(int)
        self._idf_cache: Dict[str, float] = {}
        self._lock = threading.Lock()
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return  # Ignore duplicates
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            term_freq = Counter(tokens)
            self._documents[doc.id] = doc
            self._doc_term_freqs[doc.id] = term_freq
            self._doc_lengths[doc.id] = len(tokens)
            for term in term_freq:
                self._inverted_index[term].add(doc.id)
                self._term_doc_freq[term] += 1
            self._doc_count += 1
            self._avg_doc_len = sum(self._doc_lengths.values()) / self._doc_count if self._doc_count > 0 else 0.0
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidate_doc_ids = set()
        for term in query_terms:
            candidate_doc_ids.update(self._inverted_index.get(term, set()))
        scored_docs = []
        for doc_id in candidate_doc_ids:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            # Combine BM25 and TF-IDF (weighted sum, BM25 prioritized)
            score = 0.7 * bm25_score + 0.3 * tfidf_score
            doc = self._documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            scored_docs.append(SearchResult(doc_id, score, doc.title, snippet))
        scored_docs.sort(key=lambda r: r.score, reverse=True)
        return scored_docs[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                "document_count": self._doc_count,
                "avg_doc_length": self._avg_doc_len,
                "unique_terms": len(self._inverted_index),
            }

    def _tokenize(self, text: str) -> List[str]:
        # Lowercase, remove non-alphanum, split on whitespace
        text = text.lower()
        text = re.sub(r"[^a-z0-9_+/#.-]", " ", text)
        tokens = text.split()
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self._term_doc_freq.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self._doc_count - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        doc = self._documents[doc_id]
        term_freqs = self._doc_term_freqs[doc_id]
        doc_len = self._doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            tf = term_freqs.get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            numerator = tf * (self._bm25_k1 + 1)
            denominator = tf + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / (self._avg_doc_len + 1e-9))
            score += idf * numerator / denominator
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        doc = self._documents[doc_id]
        term_freqs = self._doc_term_freqs[doc_id]
        doc_len = self._doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            tf = term_freqs.get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / (doc_len + 1e-9)
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * doc.weight

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], snippet_len: int = 160) -> str:
        content = doc.content
        content_lc = content.lower()
        positions = []
        for term in query_terms:
            idx = content_lc.find(term)
            if idx != -1:
                positions.append(idx)
        if positions:
            start = max(min(positions) - 40, 0)
            end = min(start + snippet_len, len(content))
            snippet = content[start:end]
            # Highlight terms
            for term in set(query_terms):
                snippet = re.sub(r'(?i)(' + re.escape(term) + r')', r'**\1**', snippet)
            return snippet.strip()
        else:
            return content[:snippet_len].strip()

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

# --- Preseed Domain Documents ---

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "The Twelve-Factor App: Principles for Modern SaaS",
            "The Twelve-Factor App methodology provides a set of best practices for building scalable, maintainable cloud-native applications. Key factors include codebase, dependencies, config, backing services, build, release, run, processes, port binding, concurrency, disposability, dev/prod parity, logs, and admin processes.",
            ["twelve-factor", "cloud-native", "best-practices"],
            1.0
        ),
        SearchDocument(
            2,
            "Serverless Patterns: Cloudflare Workers vs AWS Lambda",
            "Cloudflare Workers and AWS Lambda represent two leading serverless compute platforms. While Lambda provides deep AWS integration and flexible runtimes, Workers offer ultra-low latency at the edge. Both support event-driven architectures, but differ in cold start, deployment, and scaling characteristics.",
            ["serverless", "cloudflare", "aws", "lambda", "edge"],
            1.0
        ),
        SearchDocument(
            3,
            "CDN Optimization: Cache-Control and Stale-While-Revalidate",
            "Optimizing CDN caching involves tuning Cache-Control headers such as max-age, s-maxage, and leveraging stale-while-revalidate for seamless user experience. Proper configuration reduces origin load, improves latency, and handles cache invalidation gracefully.",
            ["cdn", "cache-control", "stale-while-revalidate", "performance"],
            1.0
        ),
        SearchDocument(
            4,
            "Docker Multi-Stage Builds for Efficient Images",
            "Multi-stage builds in Docker enable developers to create minimal production images by separating build and runtime environments. This reduces image size, attack surface, and improves CI/CD pipeline efficiency.",
            ["docker", "multi-stage", "containerization", "ci/cd"],
            1.0
        ),
        SearchDocument(
            5,
            "Kubernetes Pod Design Patterns",
            "Effective pod design in Kubernetes involves sidecars, ambassadors, and adapters. These patterns enable modularity, observability, and separation of concerns in containerized workloads.",
            ["kubernetes", "pod", "design-patterns", "container"],
            1.0
        ),
        SearchDocument(
            6,
            "Service Mesh: Istio, Linkerd, Envoy, and mTLS",
            "A service mesh like Istio, Linkerd, or Envoy provides traffic management, observability, and security (including mutual TLS) for microservices. mTLS ensures encrypted service-to-service communication and strong identity.",
            ["service-mesh", "istio", "linkerd", "envoy", "mtls"],
            1.0
        ),
        SearchDocument(
            7,
            "Infrastructure as Code: Terraform and Pulumi State Management",
            "Managing infrastructure state is crucial for reproducibility. Terraform uses state files (local or remote), while Pulumi manages state via backends. Both support locking, versioning, and drift detection.",
            ["iac", "terraform", "pulumi", "state-management"],
            1.0
        ),
        SearchDocument(
            8,
            "GitOps: ArgoCD, Flux, and Reconciliation Loops",
            "GitOps leverages tools like ArgoCD and Flux to continuously reconcile desired and actual state in Kubernetes. Reconciliation loops ensure declarative infrastructure is always up-to-date.",
            ["gitops", "argocd", "flux", "reconciliation"],
            1.0
        ),
        SearchDocument(
            9,
            "Database Selection: SQL, NoSQL, NewSQL, and the CAP Theorem",
            "Choosing a database involves understanding trade-offs: SQL for ACID, NoSQL for scalability, NewSQL for hybrid needs. The CAP theorem states that Consistency, Availability, and Partition tolerance cannot all be fully achieved simultaneously.",
            ["database", "sql", "nosql", "newsql", "cap-theorem"],
            1.0
        ),
        SearchDocument(
            10,
            "Caching Strategies: Redis, Memcached, CDN, Write-Through & Write-Behind",
            "Effective caching uses technologies like Redis and Memcached for low-latency data, CDNs for static assets, and strategies such as write-through and write-behind for data consistency.",
            ["caching", "redis", "memcached", "cdn", "write-through", "write-behind"],
            1.0
        ),
        SearchDocument(
            11,
            "Message Queues: Kafka, RabbitMQ, SQS, and Ordering Guarantees",
            "Distributed message queues like Kafka, RabbitMQ, and AWS SQS provide asynchronous communication. Kafka offers strong ordering and durability, while SQS is fully managed and scalable.",
            ["message-queue", "kafka", "rabbitmq", "sqs", "ordering"],
            1.0
        ),
        SearchDocument(
            12,
            "Monitoring: Prometheus, Grafana, Datadog, and the RED & USE Methods",
            "Modern monitoring stacks use Prometheus for metrics, Grafana for visualization, and Datadog for observability. The RED (Rate, Errors, Duration) and USE (Utilization, Saturation, Errors) methods guide SLOs and error budgets.",
            ["monitoring", "prometheus", "grafana", "datadog", "red", "use"],
            1.0
        ),
        SearchDocument(
            13,
            "SLO, SLI, SLA, and Error Budget Burn Rate Explained",
            "Service Level Objectives (SLOs), Indicators (SLIs), and Agreements (SLAs) define reliability targets. Error budget burn rate measures how quickly reliability is consumed, guiding engineering priorities.",
            ["slo", "sli", "sla", "error-budget"],
            1.0
        ),
        SearchDocument(
            14,
            "Twelve-Factor: Dev/Prod Parity and Disposability",
            "Maintaining dev/prod parity and disposability ensures rapid iteration and reliable deployments. Containers and ephemeral environments support these principles.",
            ["twelve-factor", "dev-prod-parity", "disposability"],
            1.0
        ),
        SearchDocument(
            15,
            "Edge Computing with Cloudflare Workers",
            "Cloudflare Workers enable serverless execution at the edge, reducing latency and improving global performance. Use cases include API gateways, A/B testing, and custom CDN logic.",
            ["cloudflare", "workers", "edge", "serverless"],
            1.0
        ),
        SearchDocument(
            16,
            "Advanced Cache-Control: s-maxage and Immutable",
            "s-maxage targets shared caches (CDNs), while the immutable directive signals that content won't change, maximizing cache hit rates and reducing revalidation.",
            ["cache-control", "cdn", "immutable", "s-maxage"],
            1.0
        ),
        SearchDocument(
            17,
            "Kubernetes Sidecar Pattern",
            "The sidecar pattern in Kubernetes allows auxiliary containers to provide logging, proxying, or configuration alongside the main application container.",
            ["kubernetes", "sidecar", "pattern"],
            1.0
        ),
        SearchDocument(
            18,
            "Istio: Traffic Management and Observability",
            "Istio provides fine-grained traffic routing, retries, circuit breaking, and telemetry for microservices. Its control plane configures Envoy proxies for consistent policy enforcement.",
            ["istio", "traffic-management", "observability", "envoy"],
            1.0
        ),
        SearchDocument(
            19,
            "Terraform State Backends: S3, GCS, and Remote Locking",
            "Terraform supports remote state backends like AWS S3 and Google Cloud Storage, with locking mechanisms to prevent concurrent changes and ensure consistency.",
            ["terraform", "state", "s3", "gcs", "locking"],
            1.0
        ),
        SearchDocument(
            20,
            "Flux: GitOps for Kubernetes",
            "Flux automates Kubernetes deployments by syncing manifests from Git repositories, ensuring cluster state matches version-controlled configuration.",
            ["flux", "gitops", "kubernetes"],
            1.0
        ),
        SearchDocument(
            21,
            "NoSQL Databases: Eventual Consistency and Partition Tolerance",
            "NoSQL systems like Cassandra and DynamoDB prioritize availability and partition tolerance, often sacrificing strong consistency for scalability.",
            ["nosql", "cassandra", "dynamodb", "cap-theorem"],
            1.0
        ),
        SearchDocument(
            22,
            "Redis vs Memcached: Use Cases and Performance",
            "Redis supports advanced data types and persistence, while Memcached excels at simple key-value caching with high throughput.",
            ["redis", "memcached", "caching", "performance"],
            1.0
        ),
        SearchDocument(
            23,
            "Kafka: Exactly-Once Semantics and Partitioning",
            "Kafka's exactly-once semantics and partitioning model enable reliable, ordered message processing at scale.",
            ["kafka", "exactly-once", "partitioning", "ordering"],
            1.0
        ),
        SearchDocument(
            24,
            "Prometheus: Metrics Collection and Alerting",
            "Prometheus scrapes metrics from targets, supports multi-dimensional data, and integrates with Alertmanager for incident response.",
            ["prometheus", "metrics", "alerting"],
            1.0
        ),
        SearchDocument(
            25,
            "Error Budgets: Balancing Reliability and Innovation",
            "Error budgets allow teams to balance reliability targets with feature velocity, using burn rate to inform engineering decisions.",
            ["error-budget", "slo", "reliability"],
            1.0
        ),
        SearchDocument(
            26,
            "Containerization: Security Best Practices",
            "Minimize container attack surface by using multi-stage builds, non-root users, and image scanning. Kubernetes pod security policies enforce runtime constraints.",
            ["containerization", "security", "docker", "kubernetes"],
            1.0
        ),
        SearchDocument(
            27,
            "Envoy Proxy: Service Mesh Data Plane",
            "Envoy acts as the data plane in service meshes, providing L7 routing, observability, and mTLS termination for microservices.",
            ["envoy", "service-mesh", "mtls", "proxy"],
            1.0
        ),
        SearchDocument(
            28,
            "Pulumi: Infrastructure as Code in TypeScript and Python",
            "Pulumi enables infrastructure as code using familiar programming languages, with state management and cloud resource provisioning.",
            ["pulumi", "iac", "typescript", "python"],
            1.0
        ),
        SearchDocument(
            29,
            "ArgoCD: Declarative Continuous Delivery",
            "ArgoCD provides declarative GitOps for Kubernetes, supporting automated sync, drift detection, and RBAC.",
            ["argocd", "gitops", "kubernetes", "cd"],
            1.0
        ),
        SearchDocument(
            30,
            "Write-Through vs Write-Behind Caching",
            "Write-through caching synchronously writes to cache and backing store, while write-behind buffers writes for improved throughput.",
            ["caching", "write-through", "write-behind"],
            1.0
        ),
        SearchDocument(
            31,
            "SQS: At-Least-Once Delivery and Visibility Timeout",
            "AWS SQS guarantees at-least-once delivery and uses visibility timeouts to prevent message duplication during processing.",
            ["sqs", "message-queue", "delivery"],
            1.0
        ),
        SearchDocument(
            32,
            "Grafana: Visualizing Metrics and Logs",
            "Grafana connects to Prometheus, Loki, and other data sources to provide dashboards and alerting for observability.",
            ["grafana", "metrics", "logs", "observability"],
            1.0
        ),
        SearchDocument(
            33,
            "Service Mesh Security: Mutual TLS (mTLS)",
            "mTLS in service meshes ensures that both client and server authenticate each other, encrypting traffic and enabling zero-trust architectures.",
            ["service-mesh", "security", "mtls"],
            1.0
        ),
        SearchDocument(
            34,
            "CAP Theorem in Distributed Databases",
            "The CAP theorem describes trade-offs in distributed systems: consistency, availability, and partition tolerance. Real-world databases make different choices based on use case.",
            ["cap-theorem", "database", "distributed"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)