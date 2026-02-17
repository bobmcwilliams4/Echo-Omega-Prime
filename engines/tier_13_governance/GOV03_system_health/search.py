import math
import threading
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

# --- Search Index ---

class SearchIndex:
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_doc_tf: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._preseeded = False

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            tf_counter = Counter(tokens)
            self.term_doc_tf[doc.id] = tf_counter
            for term in tf_counter:
                self.term_doc_freq[term] += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs else 0.0
            self._idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            return 0.0
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int, k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        tf_counter = self.term_doc_tf[doc_id]
        for term in query_terms:
            tf = tf_counter.get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            denom = tf + k1 * (1 - b + b * (doc_len / self.avg_doc_length))
            bm25 = idf * ((tf * (k1 + 1)) / (denom + 1e-8))
            score += bm25
        score *= doc.weight
        return score

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        tf_counter = self.term_doc_tf[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            tf = tf_counter.get(term, 0)
            if tf == 0:
                continue
            norm_tf = tf / doc_len
            idf = self._compute_idf(term)
            score += norm_tf * idf
        score *= doc.weight
        return score

    def search(self, query: str, limit: int = 10, method: str = 'bm25') -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scores: List[Tuple[int, float]] = []
        for doc_id in self.documents:
            if method == 'bm25':
                score = self._score_bm25(query_terms, doc_id)
            elif method == 'tfidf':
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0.0:
                scores.append((doc_id, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scores[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str], max_len: int = 160) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = ' '.join(tokens[:max_len])
            return snippet[:max_len] + ('...' if len(snippet) > max_len else '')
        start = max(positions[0] - 10, 0)
        end = min(start + max_len, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return snippet[:max_len] + ('...' if len(snippet) > max_len else '')

    def get_stats(self) -> Dict[str, any]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
            'doc_lengths': self.doc_lengths.copy(),
        }

    def _preseed(self):
        if self._preseeded:
            return
        docs = [
            SearchDocument(1, "Health Check Patterns", 
                "Health check patterns ensure services are monitored for uptime and responsiveness. Common patterns include HTTP endpoints, custom probes, and integration with orchestration platforms.", 
                ["health_check_patterns", "monitoring"], 1.0),
            SearchDocument(2, "Circuit Breaker Pattern", 
                "Circuit breaker pattern prevents cascading failures by stopping calls to unhealthy dependencies. It uses thresholds and fallback logic to maintain system stability.", 
                ["circuit_breaker_pattern", "dependency_management"], 1.0),
            SearchDocument(3, "Golden Signals in Observability", 
                "Golden signals are latency, traffic, errors, and saturation. Monitoring these helps detect issues in distributed systems quickly.", 
                ["golden_signals", "distributed_systems_observability"], 1.0),
            SearchDocument(4, "Distributed Systems Observability", 
                "Observability in distributed systems relies on logs, metrics, traces, and correlation across services. Tools like OpenTelemetry and service meshes enhance visibility.", 
                ["distributed_systems_observability", "service_mesh_monitoring"], 1.0),
            SearchDocument(5, "Error Budgets for Reliability", 
                "Error budgets quantify acceptable failure rates. SRE teams use error budgets to balance innovation and reliability, triggering alerts or change freezes when exceeded.", 
                ["error_budgets", "sla_compliance_monitoring"], 1.0),
            SearchDocument(6, "Alert Fatigue Prevention", 
                "Alert fatigue occurs when too many alerts desensitize operators. Prevention strategies include deduplication, prioritization, and actionable alerting.", 
                ["alert_fatigue_prevention", "monitoring_antipatterns"], 1.0),
            SearchDocument(7, "Capacity Planning Strategies", 
                "Capacity planning uses historical data, predictive analytics, and stress testing to ensure resources meet demand. It prevents outages from resource exhaustion.", 
                ["capacity_planning", "graceful_degradation"], 1.0),
            SearchDocument(8, "Dependency Management in Microservices", 
                "Managing dependencies involves versioning, health checks, and circuit breakers. Tools like service meshes automate dependency tracking and health monitoring.", 
                ["dependency_management", "service_mesh_monitoring"], 1.0),
            SearchDocument(9, "Incident Classification Frameworks", 
                "Incident classification helps prioritize response. Categories include severity, impact, root cause, and recurrence. Automation aids in consistent classification.", 
                ["incident_classification", "post_incident_review"], 1.0),
            SearchDocument(10, "Chaos Engineering for Resilience", 
                "Chaos engineering injects failures to test system resilience. Experiments target network, compute, and dependency failures to validate graceful degradation.", 
                ["chaos_engineering", "graceful_degradation"], 1.0),
            SearchDocument(11, "Service Mesh Monitoring", 
                "Service meshes provide observability, traffic control, and security. Monitoring includes latency, error rates, and dependency health.", 
                ["service_mesh_monitoring", "distributed_systems_observability"], 1.0),
            SearchDocument(12, "Runbook Automation", 
                "Automated runbooks reduce SRE toil and accelerate incident response. Integrations with monitoring and alerting systems enable self-healing operations.", 
                ["runbook_automation", "sre_toil_reduction"], 1.0),
            SearchDocument(13, "Monitoring Antipatterns", 
                "Antipatterns include alert storms, missing context, and unmaintained dashboards. Regular reviews and actionable metrics prevent monitoring failures.", 
                ["monitoring_antipatterns", "alert_fatigue_prevention"], 1.0),
            SearchDocument(14, "SRE Toil Reduction", 
                "Reducing toil involves automation, clear runbooks, and eliminating manual repetitive tasks. This increases reliability and frees SREs for engineering work.", 
                ["sre_toil_reduction", "runbook_automation"], 1.0),
            SearchDocument(15, "Graceful Degradation Techniques", 
                "Graceful degradation ensures partial functionality during failures. Techniques include feature flagging, fallback logic, and prioritized resource allocation.", 
                ["graceful_degradation", "chaos_engineering"], 1.0),
            SearchDocument(16, "Post-Incident Review Best Practices", 
                "Post-incident reviews analyze root causes, impact, and remediation. Blameless retrospectives foster learning and continuous improvement.", 
                ["post_incident_review", "incident_classification"], 1.0),
            SearchDocument(17, "Multi-Region Health Monitoring", 
                "Multi-region health checks detect outages and latency issues across geographies. Automated failover and region isolation improve reliability.", 
                ["multi_region_health", "network_health_monitoring"], 1.0),
            SearchDocument(18, "Container Health Checks", 
                "Containers use liveness and readiness probes for health monitoring. Orchestrators restart unhealthy containers and manage resource allocation.", 
                ["container_health", "health_check_patterns"], 1.0),
            SearchDocument(19, "Database Health Monitoring", 
                "Database health includes replication lag, query latency, and error rates. Automated failover and backup checks ensure data integrity.", 
                ["database_health_monitoring", "synthetic_monitoring"], 1.0),
            SearchDocument(20, "Synthetic Monitoring", 
                "Synthetic monitoring uses scripted probes to simulate user actions. It detects outages, latency, and functional issues proactively.", 
                ["synthetic_monitoring", "golden_signals"], 1.0),
            SearchDocument(21, "Cost Monitoring in Cloud Systems", 
                "Cost monitoring tracks resource usage and spending. Alerts for budget overruns and optimization recommendations prevent waste.", 
                ["cost_monitoring", "capacity_planning"], 1.0),
            SearchDocument(22, "Log Aggregation Health", 
                "Log aggregation systems monitor ingestion rates, error logs, and storage health. Alerting on dropped logs and latency ensures observability.", 
                ["log_aggregation_health", "distributed_systems_observability"], 1.0),
            SearchDocument(23, "Security Health Signals", 
                "Security health signals include authentication failures, anomaly detection, and vulnerability scans. Integration with SIEM tools enhances visibility.", 
                ["security_health_signals", "sla_compliance_monitoring"], 1.0),
            SearchDocument(24, "SLA Compliance Monitoring", 
                "SLA compliance is tracked via uptime, latency, and error rates. Automated reporting and alerting ensure contractual obligations are met.", 
                ["sla_compliance_monitoring", "error_budgets"], 1.0),
            SearchDocument(25, "Network Health Monitoring", 
                "Network health monitoring includes latency, packet loss, and bandwidth utilization. Automated diagnostics and failover improve reliability.", 
                ["network_health_monitoring", "multi_region_health"], 1.0),
            SearchDocument(26, "Topic-Based Monitoring", 
                "Topic-based monitoring organizes metrics and logs by service or domain. This enables targeted alerting and easier troubleshooting.", 
                ["topic", "monitoring"], 1.0),
            SearchDocument(27, "Dependency Health Dashboards", 
                "Dashboards visualize dependency health, error rates, and latency. Service meshes and tracing tools provide real-time insights.", 
                ["dependency_management", "service_mesh_monitoring"], 1.0),
            SearchDocument(28, "Incident Response Automation", 
                "Automated incident response uses runbooks, alert routing, and remediation scripts. Reduces mean time to recovery and operator fatigue.", 
                ["runbook_automation", "alert_fatigue_prevention"], 1.0),
            SearchDocument(29, "Monitoring for Toil Reduction", 
                "Effective monitoring reduces toil by automating detection, alerting, and remediation. SREs focus on engineering rather than firefighting.", 
                ["sre_toil_reduction", "monitoring"], 1.0),
            SearchDocument(30, "Golden Signals Dashboards", 
                "Dashboards for golden signals visualize latency, traffic, errors, and saturation. Enable rapid diagnosis and SLA compliance.", 
                ["golden_signals", "sla_compliance_monitoring"], 1.0),
            SearchDocument(31, "Chaos Engineering in Multi-Region Systems", 
                "Chaos engineering tests failover, region isolation, and network partitioning. Ensures reliability in distributed, multi-region architectures.", 
                ["chaos_engineering", "multi_region_health"], 1.0),
            SearchDocument(32, "Database Failover Automation", 
                "Automated database failover reduces downtime during incidents. Health checks, replication monitoring, and backup validation are critical.", 
                ["database_health_monitoring", "runbook_automation"], 1.0),
            SearchDocument(33, "Synthetic User Journeys", 
                "Synthetic user journeys simulate end-to-end workflows. Detects issues in authentication, database, and network layers.", 
                ["synthetic_monitoring", "network_health_monitoring"], 1.0),
            SearchDocument(34, "Cost Optimization Runbooks", 
                "Runbooks for cost optimization automate resource scaling, shutdown of idle workloads, and budget alerting.", 
                ["cost_monitoring", "runbook_automation"], 1.0),
            SearchDocument(35, "Security Incident Classification", 
                "Classification of security incidents enables rapid response. Categories include authentication failures, privilege escalation, and data breaches.", 
                ["security_health_signals", "incident_classification"], 1.0),
        ]
        for doc in docs:
            self.add_document(doc)
        self._preseeded = True

# --- Singleton Factory ---

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            idx = SearchIndex()
            idx._preseed()
            _search_index_instance = idx
        return _search_index_instance