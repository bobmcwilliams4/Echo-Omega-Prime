import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Optional, Tuple

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
        self.doc_lengths: Dict[int, int] = {}
        self.term_doc_freqs: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.doc_tags: Dict[int, List[str]] = {}
        self.total_terms: int = 0
        self.lock = threading.Lock()
        self.avg_doc_length: float = 0.0
        self.idf_cache: Dict[str, float] = {}
        self.doc_snippets: Dict[int, str] = {}
        self._stats_cache = None

    def add_document(self, document: SearchDocument):
        with self.lock:
            self.documents[document.id] = document
            tokens = self._tokenize(document.content)
            self.doc_lengths[document.id] = len(tokens)
            self.term_freqs[document.id] = Counter(tokens)
            for term in self.term_freqs[document.id]:
                self.term_doc_freqs[term][document.id] = self.term_freqs[document.id][term]
            self.doc_tags[document.id] = document.tags
            self.total_terms += len(tokens)
            self.avg_doc_length = self.total_terms / max(1, len(self.documents))
            self.doc_snippets[document.id] = self._generate_snippet(document.content)
            self._stats_cache = None
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores = defaultdict(float)
        doc_tf_scores = defaultdict(float)
        for term in query_terms:
            idf = self._compute_idf(term)
            for doc_id in self.term_doc_freqs.get(term, {}):
                tf = self.term_freqs[doc_id][term]
                doc_length = self.doc_lengths[doc_id]
                bm25_score = self._score_bm25(tf, idf, doc_length)
                doc_scores[doc_id] += bm25_score * self.documents[doc_id].weight
                tf_norm = tf / (doc_length + 1)
                doc_tf_scores[doc_id] += tf_norm * idf * self.documents[doc_id].weight
        results = []
        for doc_id in doc_scores:
            snippet = self._highlight_snippet(self.doc_snippets[doc_id], query_terms)
            score = doc_scores[doc_id] + doc_tf_scores[doc_id]
            results.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:limit]

    def get_stats(self) -> Dict[str, float]:
        if self._stats_cache:
            return self._stats_cache
        stats = {
            'document_count': len(self.documents),
            'avg_doc_length': self.avg_doc_length,
            'total_terms': self.total_terms,
            'unique_terms': len(self.term_doc_freqs),
        }
        self._stats_cache = stats
        return stats

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        N = len(self.documents)
        df = len(self.term_doc_freqs.get(term, {}))
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, tf: int, idf: float, doc_length: int, k1: float = 1.5, b: float = 0.75) -> float:
        avg_dl = self.avg_doc_length if self.avg_doc_length else 1
        numerator = tf * (k1 + 1)
        denominator = tf + k1 * (1 - b + b * (doc_length / avg_dl))
        return idf * (numerator / denominator)

    def _generate_snippet(self, content: str, max_length: int = 160) -> str:
        snippet = content.strip()
        if len(snippet) > max_length:
            snippet = snippet[:max_length].rsplit(' ', 1)[0] + '...'
        return snippet

    def _highlight_snippet(self, snippet: str, terms: List[str]) -> str:
        for term in set(terms):
            snippet = re.sub(r'(?i)\b' + re.escape(term) + r'\b', f'**{term}**', snippet)
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

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "DAG Construction from Engine Specifications",
            "Build directed acyclic graphs (DAGs) from engine specifications, mapping dependencies and execution order for orchestrated tasks.",
            ["dag", "construction", "engine", "specifications", "dependency"],
            1.0
        ),
        SearchDocument(
            2,
            "Topological Sort Algorithms",
            "Utilize topological sorting to determine valid execution sequences in dependency graphs, ensuring no cycles and proper task ordering.",
            ["topological_sort", "algorithm", "dependency_graph", "execution_order"],
            1.0
        ),
        SearchDocument(
            3,
            "Cycle Detection in Dependency Graphs",
            "Detect cycles within dependency graphs to prevent invalid DAGs and ensure safe orchestration of engine tasks.",
            ["cycle_detection", "dependency_graph", "dag", "validation"],
            1.0
        ),
        SearchDocument(
            4,
            "Parallel Execution Scheduling",
            "Schedule tasks for parallel execution where dependencies allow, optimizing resource utilization and reducing overall latency.",
            ["parallel_execution", "scheduling", "optimization", "resource"],
            1.0
        ),
        SearchDocument(
            5,
            "Dependency Failure Propagation",
            "Handle propagation of failures across dependent tasks, marking downstream nodes as failed or skipped based on upstream errors.",
            ["failure_propagation", "dependency", "error_handling", "engine"],
            1.0
        ),
        SearchDocument(
            6,
            "Circuit Breaker Pattern for Engine Orchestration",
            "Implement circuit breaker patterns to halt execution in case of repeated failures, protecting the engine from cascading errors.",
            ["circuit_breaker", "pattern", "engine", "orchestration", "error"],
            1.0
        ),
        SearchDocument(
            7,
            "Engine Timeout Handling",
            "Configure and enforce timeouts for engine tasks, aborting long-running operations and ensuring timely completion.",
            ["timeout_handling", "engine", "task", "abort"],
            1.0
        ),
        SearchDocument(
            8,
            "Resource Budget Enforcement",
            "Monitor and enforce resource budgets for engine executions, preventing overuse and ensuring fair allocation across tasks.",
            ["resource_budget", "enforcement", "engine", "monitoring"],
            1.0
        ),
        SearchDocument(
            9,
            "Critical Path Analysis",
            "Identify and analyze the critical path in dependency graphs to optimize execution plans and minimize total runtime.",
            ["critical_path", "analysis", "optimization", "dependency_graph"],
            1.0
        ),
        SearchDocument(
            10,
            "Execution Plan Optimization",
            "Optimize execution plans using heuristics and analysis of dependency structures, improving throughput and efficiency.",
            ["execution_plan", "optimization", "heuristics", "dependency"],
            1.0
        ),
        SearchDocument(
            11,
            "Dependency Graph Versioning",
            "Maintain versions of dependency graphs to track changes, support rollback, and enable deterministic execution replays.",
            ["dependency_graph", "versioning", "rollback", "determinism"],
            1.0
        ),
        SearchDocument(
            12,
            "Lazy Evaluation for Optional Dependencies",
            "Apply lazy evaluation for optional dependencies, deferring execution until required and improving resource efficiency.",
            ["lazy_evaluation", "optional_dependency", "resource", "engine"],
            1.0
        ),
        SearchDocument(
            13,
            "Fan-Out and Fan-In Patterns",
            "Implement fan-out and fan-in patterns to scale task execution and aggregate results efficiently in engine orchestration.",
            ["fan_out", "fan_in", "pattern", "engine", "aggregation"],
            1.0
        ),
        SearchDocument(
            14,
            "Engine Health Check Integration",
            "Integrate health checks into engine orchestration to monitor task status, detect failures, and trigger recovery mechanisms.",
            ["health_check", "integration", "engine", "monitoring"],
            1.0
        ),
        SearchDocument(
            15,
            "Execution Replay and Determinism",
            "Enable deterministic execution replay by capturing engine states and dependency graph versions, ensuring reproducibility.",
            ["execution_replay", "determinism", "engine", "state"],
            1.0
        ),
        SearchDocument(
            16,
            "DAG Validation and Consistency Checks",
            "Perform validation and consistency checks on DAGs to ensure correctness and prevent invalid dependency configurations.",
            ["dag", "validation", "consistency", "dependency"],
            1.0
        ),
        SearchDocument(
            17,
            "Task Prioritization in Engine Scheduling",
            "Prioritize tasks based on dependency importance, resource requirements, and critical path analysis for optimal scheduling.",
            ["task_prioritization", "engine", "scheduling", "critical_path"],
            1.0
        ),
        SearchDocument(
            18,
            "Dynamic Dependency Resolution",
            "Resolve dependencies dynamically at runtime, adapting to changing engine states and external conditions.",
            ["dynamic_dependency", "resolution", "runtime", "engine"],
            1.0
        ),
        SearchDocument(
            19,
            "Failure Recovery Strategies",
            "Design and implement recovery strategies for failed tasks, including retries, fallback paths, and error isolation.",
            ["failure_recovery", "strategy", "engine", "error"],
            1.0
        ),
        SearchDocument(
            20,
            "Resource Allocation Algorithms",
            "Apply algorithms for allocating resources to engine tasks, balancing load and maximizing throughput.",
            ["resource_allocation", "algorithm", "engine", "load_balancing"],
            1.0
        ),
        SearchDocument(
            21,
            "Task State Management",
            "Manage task states throughout engine execution, tracking progress, failures, and completion for orchestration.",
            ["task_state", "management", "engine", "orchestration"],
            1.0
        ),
        SearchDocument(
            22,
            "Dependency Injection for Engine Modules",
            "Use dependency injection to configure engine modules, enabling flexible orchestration and modular design.",
            ["dependency_injection", "engine", "module", "configuration"],
            1.0
        ),
        SearchDocument(
            23,
            "Graph Traversal Techniques",
            "Employ graph traversal techniques for dependency analysis, cycle detection, and path optimization in engine orchestration.",
            ["graph_traversal", "technique", "dependency_analysis", "engine"],
            1.0
        ),
        SearchDocument(
            24,
            "Engine Metrics Collection",
            "Collect and analyze metrics from engine executions, monitoring performance, resource usage, and failure rates.",
            ["metrics_collection", "engine", "performance", "monitoring"],
            1.0
        ),
        SearchDocument(
            25,
            "Task Retry Policies",
            "Define and apply retry policies for engine tasks, handling transient failures and improving reliability.",
            ["retry_policy", "engine", "task", "reliability"],
            1.0
        ),
        SearchDocument(
            26,
            "Dependency Graph Serialization",
            "Serialize and deserialize dependency graphs for persistence, sharing, and versioning in engine orchestration.",
            ["dependency_graph", "serialization", "persistence", "engine"],
            1.0
        ),
        SearchDocument(
            27,
            "Task Execution Determinism",
            "Ensure deterministic task execution by controlling randomness, versioning dependencies, and capturing engine states.",
            ["task_execution", "determinism", "engine", "state"],
            1.0
        ),
        SearchDocument(
            28,
            "Engine Configuration Management",
            "Manage engine configurations, supporting dynamic updates, rollback, and validation for orchestration reliability.",
            ["configuration_management", "engine", "rollback", "validation"],
            1.0
        ),
        SearchDocument(
            29,
            "Graph Partitioning for Scalability",
            "Partition dependency graphs to scale engine orchestration, enabling distributed execution and load balancing.",
            ["graph_partitioning", "scalability", "engine", "distributed"],
            1.0
        ),
        SearchDocument(
            30,
            "Task Dependency Visualization",
            "Visualize task dependencies in engine orchestration, aiding debugging, optimization, and monitoring.",
            ["dependency_visualization", "engine", "task", "monitoring"],
            1.0
        ),
        SearchDocument(
            31,
            "Engine Logging and Audit Trails",
            "Maintain logging and audit trails for engine executions, supporting traceability, debugging, and compliance.",
            ["logging", "audit_trail", "engine", "traceability"],
            1.0
        ),
        SearchDocument(
            32,
            "Task Grouping and Batch Execution",
            "Group tasks for batch execution, optimizing resource usage and reducing orchestration overhead.",
            ["task_grouping", "batch_execution", "engine", "optimization"],
            1.0
        ),
        SearchDocument(
            33,
            "Dependency Graph Querying",
            "Query dependency graphs for task relationships, status, and execution history in engine orchestration.",
            ["dependency_graph", "querying", "engine", "history"],
            1.0
        ),
        SearchDocument(
            34,
            "Engine Security and Access Control",
            "Implement security and access control for engine orchestration, restricting task execution and protecting sensitive data.",
            ["security", "access_control", "engine", "protection"],
            1.0
        ),
        SearchDocument(
            35,
            "Task Completion Notification",
            "Notify stakeholders upon task completion in engine orchestration, integrating with alerting and monitoring systems.",
            ["task_completion", "notification", "engine", "alerting"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)