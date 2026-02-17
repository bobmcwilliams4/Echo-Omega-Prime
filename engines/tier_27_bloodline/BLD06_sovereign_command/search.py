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
        self.lock = threading.Lock()

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                # Remove old doc term frequencies from index
                old_tf = self.doc_term_freqs.get(doc.id, Counter())
                for term in old_tf:
                    self.term_doc_freqs[term] -= 1
                    if self.term_doc_freqs[term] <= 0:
                        del self.term_doc_freqs[term]
                self.total_docs -= 1

            tokens = self._tokenize(doc.title + ' ' + doc.content + ' ' + ' '.join(doc.tags))
            term_freqs = Counter(tokens)

            self.documents[doc.id] = doc
            self.doc_term_freqs[doc.id] = term_freqs

            for term in term_freqs:
                self.term_doc_freqs[term] += 1

            self.total_docs = len(self.documents)
            self.avg_doc_len = self._compute_avg_doc_len()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []

        idf_cache = {}
        for term in set(query_terms):
            idf_cache[term] = self._compute_idf(term)

        scores = []
        for doc_id, doc in self.documents.items():
            score = self._score_bm25(doc_id, query_terms, idf_cache)
            if score > 0:
                snippet = self._create_snippet(doc, query_terms)
                scores.append(SearchResult(doc_id=doc_id, score=score, title=doc.title, snippet=snippet))

        scores.sort(key=lambda r: r.score, reverse=True)
        return scores[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                'total_documents': self.total_docs,
                'average_document_length': self.avg_doc_len,
                'unique_terms': len(self.term_doc_freqs),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        n_q = self.term_doc_freqs.get(term, 0)
        if n_q == 0:
            return 0.0
        return math.log(1 + (self.total_docs - n_q + 0.5) / (n_q + 0.5))

    def _score_bm25(self, doc_id: str, query_terms: List[str], idf_cache: Dict[str, float]) -> float:
        doc = self.documents[doc_id]
        term_freqs = self.doc_term_freqs[doc_id]
        doc_len = sum(term_freqs.values())
        score = 0.0
        for term in query_terms:
            if term not in term_freqs:
                continue
            idf = idf_cache.get(term, 0)
            tf = term_freqs[term]
            denom = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_len)
            score += idf * tf * (self.k1 + 1) / denom
        score *= doc.weight
        return score

    def _compute_avg_doc_len(self) -> float:
        if not self.documents:
            return 0.0
        total_len = 0
        for tf in self.doc_term_freqs.values():
            total_len += sum(tf.values())
        return total_len / len(self.documents)

    def _create_snippet(self, doc: SearchDocument, query_terms: List[str], snippet_len: int = 160) -> str:
        content = doc.content
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            start = 0
            while True:
                idx = content_lower.find(term, start)
                if idx == -1:
                    break
                positions.append(idx)
                start = idx + len(term)
        if not positions:
            snippet = content[:snippet_len]
            if len(content) > snippet_len:
                snippet += '...'
            return snippet

        positions.sort()
        start_pos = max(positions[0] - snippet_len // 4, 0)
        end_pos = min(start_pos + snippet_len, len(content))

        snippet = content[start_pos:end_pos]
        if start_pos > 0:
            snippet = '...' + snippet
        if end_pos < len(content):
            snippet = snippet + '...'

        # Highlight query terms (simple uppercase)
        def highlight(match):
            word = match.group(0)
            if word.lower() in query_terms:
                return word.upper()
            return word

        snippet = re.sub(r'\b\w+\b', highlight, snippet, flags=re.IGNORECASE)
        return snippet


_singleton_instance = None
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
            title="Sovereign Command Authority Overview",
            content=(
                "The sovereign command authority defines the ultimate control over fleet operations, "
                "ensuring strategic decisions align with national interests and policy enforcement."
            ),
            tags=["sovereign_command_authority", "policy_enforcement", "strategic_planning"],
            weight=2.0,
        ),
        SearchDocument(
            doc_id="doc002",
            title="Fleet Command Routing Protocols",
            content=(
                "Routing protocols within fleet command optimize path selection for units, "
                "balancing priority queue management and cross-engine data flow for effective deployment."
            ),
            tags=["fleet_command_routing", "priority_queue_management", "cross_engine_data_flow"],
            weight=1.8,
        ),
        SearchDocument(
            doc_id="doc003",
            title="Batch Operations Management",
            content=(
                "Batch operations enable simultaneous command execution across multiple units, "
                "integrating workflow orchestration and audit accountability."
            ),
            tags=["batch_operations", "workflow_orchestration", "audit_and_accountability"],
            weight=1.5,
        ),
        SearchDocument(
            doc_id="doc004",
            title="Workflow Orchestration in Command Systems",
            content=(
                "Workflow orchestration ensures sequential and conditional execution of commands, "
                "supporting emergency override protocols and deterministic command resolution."
            ),
            tags=["workflow_orchestration", "emergency_override_protocol", "deterministic_command_resolution"],
            weight=1.7,
        ),
        SearchDocument(
            doc_id="doc005",
            title="Policy Enforcement Mechanisms",
            content=(
                "Policy enforcement mechanisms validate command compliance with sovereign directives, "
                "utilizing audit trails and decision logging for accountability."
            ),
            tags=["policy_enforcement", "audit_and_accountability", "decision_logging"],
            weight=1.9,
        ),
        SearchDocument(
            doc_id="doc006",
            title="Priority Queue Management Strategies",
            content=(
                "Managing priority queues ensures critical commands are executed promptly, "
                "integrating with fleet health monitoring and strategic planning modules."
            ),
            tags=["priority_queue_management", "fleet_health_monitoring", "strategic_planning"],
            weight=1.6,
        ),
        SearchDocument(
            doc_id="doc007",
            title="Decision Logging and Audit Trails",
            content=(
                "Comprehensive decision logging supports audit and accountability, "
                "capturing command rationale and execution outcomes."
            ),
            tags=["decision_logging", "audit_and_accountability"],
            weight=1.4,
        ),
        SearchDocument(
            doc_id="doc008",
            title="Strategic Planning Framework",
            content=(
                "Strategic planning aligns fleet operations with long-term objectives, "
                "incorporating data from fleet health monitoring and cross-engine data flow."
            ),
            tags=["strategic_planning", "fleet_health_monitoring", "cross_engine_data_flow"],
            weight=1.8,
        ),
        SearchDocument(
            doc_id="doc009",
            title="Fleet Health Monitoring Systems",
            content=(
                "Fleet health monitoring tracks unit status and readiness, "
                "feeding data into command routing and priority queue management."
            ),
            tags=["fleet_health_monitoring", "fleet_command_routing", "priority_queue_management"],
            weight=1.7,
        ),
        SearchDocument(
            doc_id="doc010",
            title="Cross-Engine Data Flow Integration",
            content=(
                "Cross-engine data flow enables interoperability between command modules, "
                "facilitating seamless workflow orchestration and batch operations."
            ),
            tags=["cross_engine_data_flow", "workflow_orchestration", "batch_operations"],
            weight=1.6,
        ),
        SearchDocument(
            doc_id="doc011",
            title="System Configuration Management",
            content=(
                "System configuration management maintains consistent settings across engines, "
                "supporting emergency override protocols and deterministic command resolution."
            ),
            tags=["system_configuration_management", "emergency_override_protocol", "deterministic_command_resolution"],
            weight=1.5,
        ),
        SearchDocument(
            doc_id="doc012",
            title="Audit and Accountability Practices",
            content=(
                "Audit and accountability practices ensure transparency in command execution, "
                "leveraging decision logging and policy enforcement."
            ),
            tags=["audit_and_accountability", "decision_logging", "policy_enforcement"],
            weight=1.7,
        ),
        SearchDocument(
            doc_id="doc013",
            title="Emergency Override Protocols",
            content=(
                "Emergency override protocols provide immediate command control during critical situations, "
                "bypassing standard workflows while maintaining audit trails."
            ),
            tags=["emergency_override_protocol", "workflow_orchestration", "audit_and_accountability"],
            weight=2.0,
        ),
        SearchDocument(
            doc_id="doc014",
            title="Dashboard Aggregation Techniques",
            content=(
                "Dashboard aggregation consolidates operational data for real-time monitoring, "
                "integrating fleet health and command status."
            ),
            tags=["dashboard_aggregation", "fleet_health_monitoring", "fleet_command_routing"],
            weight=1.4,
        ),
        SearchDocument(
            doc_id="doc015",
            title="Deterministic Command Resolution",
            content=(
                "Deterministic command resolution ensures predictable outcomes in command conflicts, "
                "utilizing priority queues and policy enforcement."
            ),
            tags=["deterministic_command_resolution", "priority_queue_management", "policy_enforcement"],
            weight=1.8,
        ),
        SearchDocument(
            doc_id="doc016",
            title="Sovereign Authority Command Chains",
            content=(
                "Command chains under sovereign authority define hierarchical control and delegation, "
                "ensuring compliance with strategic planning."
            ),
            tags=["sovereign_command_authority", "strategic_planning", "policy_enforcement"],
            weight=1.9,
        ),
        SearchDocument(
            doc_id="doc017",
            title="Fleet Routing Optimization Algorithms",
            content=(
                "Optimization algorithms improve fleet routing efficiency, "
                "reducing latency and maximizing resource utilization."
            ),
            tags=["fleet_command_routing", "strategic_planning"],
            weight=1.5,
        ),
        SearchDocument(
            doc_id="doc018",
            title="Batch Command Execution Framework",
            content=(
                "Frameworks for batch command execution enable scalable operations, "
                "integrating workflow orchestration and audit logging."
            ),
            tags=["batch_operations", "workflow_orchestration", "audit_and_accountability"],
            weight=1.6,
        ),
        SearchDocument(
            doc_id="doc019",
            title="Policy Compliance Verification",
            content=(
                "Verification processes ensure commands adhere to established policies, "
                "leveraging decision logging and audit trails."
            ),
            tags=["policy_enforcement", "decision_logging", "audit_and_accountability"],
            weight=1.7,
        ),
        SearchDocument(
            doc_id="doc020",
            title="Priority Queue Scheduling Techniques",
            content=(
                "Scheduling techniques in priority queues balance command urgency with resource constraints."
            ),
            tags=["priority_queue_management", "strategic_planning"],
            weight=1.5,
        ),
        SearchDocument(
            doc_id="doc021",
            title="Comprehensive Decision Logging",
            content=(
                "Logging all command decisions supports forensic analysis and accountability."
            ),
            tags=["decision_logging", "audit_and_accountability"],
            weight=1.4,
        ),
        SearchDocument(
            doc_id="doc022",
            title="Strategic Fleet Health Analytics",
            content=(
                "Analytics on fleet health data inform strategic planning and routing decisions."
            ),
            tags=["fleet_health_monitoring", "strategic_planning"],
            weight=1.6,
        ),
        SearchDocument(
            doc_id="doc023",
            title="Inter-Engine Data Synchronization",
            content=(
                "Synchronization mechanisms maintain data consistency across command engines."
            ),
            tags=["cross_engine_data_flow", "system_configuration_management"],
            weight=1.5,
        ),
        SearchDocument(
            doc_id="doc024",
            title="System Configuration Version Control",
            content=(
                "Version control in system configuration management prevents conflicts and ensures rollback capability."
            ),
            tags=["system_configuration_management", "audit_and_accountability"],
            weight=1.4,
        ),
        SearchDocument(
            doc_id="doc025",
            title="Emergency Protocol Activation Procedures",
            content=(
                "Procedures for activating emergency override protocols prioritize safety and command integrity."
            ),
            tags=["emergency_override_protocol", "policy_enforcement"],
            weight=1.8,
        ),
        SearchDocument(
            doc_id="doc026",
            title="Dashboard Aggregation and Visualization",
            content=(
                "Visualization tools in dashboard aggregation enhance situational awareness for command centers."
            ),
            tags=["dashboard_aggregation", "fleet_command_routing"],
            weight=1.5,
        ),
        SearchDocument(
            doc_id="doc027",
            title="Deterministic Algorithms for Command Resolution",
            content=(
                "Algorithms ensure consistent command resolution outcomes, minimizing ambiguity."
            ),
            tags=["deterministic_command_resolution", "priority_queue_management"],
            weight=1.7,
        ),
    ]

    for doc in docs:
        index.add_document(doc)