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

# --- Search Index Implementation ---

class SearchIndex:
    def __init__(self, bm25_k1: float = 1.5, bm25_b: float = 0.75):
        self._documents: Dict[int, SearchDocument] = {}
        self._inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_length: float = 0.0
        self._doc_count: int = 0
        self._idf_cache: Dict[str, float] = {}
        self._bm25_k1 = bm25_k1
        self._bm25_b = bm25_b
        self._lock = threading.Lock()
        self._corpus_size = 0
        self._term_doc_freq: Dict[str, int] = defaultdict(int)
        self._doc_term_freq: Dict[int, Counter] = {}
        self._doc_titles: Dict[int, str] = {}

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return  # Ignore duplicate IDs
            self._documents[doc.id] = doc
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            term_freq = Counter(tokens)
            self._doc_term_freq[doc.id] = term_freq
            self._doc_lengths[doc.id] = len(tokens)
            self._doc_titles[doc.id] = doc.title
            for term in term_freq:
                self._inverted_index[term][doc.id] = term_freq[term]
                self._term_doc_freq[term] += 1
            self._doc_count += 1
            self._corpus_size += len(tokens)
            self._avg_doc_length = self._corpus_size / self._doc_count if self._doc_count > 0 else 0.0
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self._inverted_index.get(term, {}).keys())
        scored_results: List[Tuple[int, float]] = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc = self._documents[doc_id]
            # Combine BM25 and TF-IDF, weighted by doc.weight
            score = (0.7 * bm25_score + 0.3 * tfidf_score) * doc.weight
            scored_results.append((doc_id, score))
        scored_results.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored_results[:limit]:
            doc = self._documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                "document_count": self._doc_count,
                "avg_doc_length": self._avg_doc_length,
                "corpus_size": self._corpus_size,
                "unique_terms": len(self._inverted_index),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
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
        doc_length = self._doc_lengths.get(doc_id, 0)
        score = 0.0
        term_freq = self._doc_term_freq.get(doc_id, Counter())
        for term in query_terms:
            tf = term_freq.get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            denom = tf + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_length / (self._avg_doc_length + 1e-9))
            score += idf * ((tf * (self._bm25_k1 + 1)) / (denom + 1e-9))
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        doc_length = self._doc_lengths.get(doc_id, 0)
        if doc_length == 0:
            return 0.0
        term_freq = self._doc_term_freq.get(doc_id, Counter())
        score = 0.0
        for term in query_terms:
            tf = term_freq.get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_length
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], length: int = 160) -> str:
        content = doc.content
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            idx = content_lower.find(term)
            if idx != -1:
                positions.append(idx)
        if positions:
            start = max(min(positions) - 30, 0)
        else:
            start = 0
        snippet = content[start:start + length]
        if len(snippet) < len(content):
            snippet += "..."
        return snippet

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

# --- Pre-seed Domain Documents ---

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Service Restart Taxonomy Overview",
            "A comprehensive taxonomy for classifying service restart scenarios, including graceful, forced, and rolling restarts. Discusses triggers, impact, and rollback implications.",
            ["service", "restart", "taxonomy"],
            1.0
        ),
        SearchDocument(
            2,
            "Rollback Procedure Generation Patterns",
            "Describes automated rollback procedure generation, including snapshotting, transactional rollbacks, and stateful vs stateless service considerations.",
            ["rollback", "procedure", "generation"],
            1.0
        ),
        SearchDocument(
            3,
            "Retry Logic Patterns for Distributed Systems",
            "Explores retry logic patterns such as exponential backoff, jitter, and circuit breaker integration for robust recovery in distributed environments.",
            ["retry", "logic", "patterns", "distributed"],
            1.0
        ),
        SearchDocument(
            4,
            "Configuration Repair Patterns",
            "Covers common patterns for repairing corrupted or inconsistent configuration files, including default fallback, merging, and validation strategies.",
            ["configuration", "repair", "patterns"],
            1.0
        ),
        SearchDocument(
            5,
            "Dependency Resolution Strategies",
            "Analyzes strategies for resolving service dependencies during recovery, including dependency graphs, lazy loading, and fail-fast approaches.",
            ["dependency", "resolution", "strategies"],
            1.0
        ),
        SearchDocument(
            6,
            "Database Recovery Procedures",
            "Details procedures for recovering databases after failure, including point-in-time recovery, replication failover, and transaction log replay.",
            ["database", "recovery", "procedures"],
            1.0
        ),
        SearchDocument(
            7,
            "File System Repair Procedures",
            "Outlines file system repair techniques such as fsck, journaling, and snapshot-based restoration for various file system types.",
            ["file", "system", "repair", "procedures"],
            1.0
        ),
        SearchDocument(
            8,
            "Network Recovery Procedures",
            "Describes recovery procedures for network partitions and failures, including route reconfiguration, interface cycling, and DNS cache flushing.",
            ["network", "recovery", "procedures"],
            1.0
        ),
        SearchDocument(
            9,
            "Cache Invalidation Strategies",
            "Discusses cache invalidation strategies such as time-based, write-through, and explicit invalidation for consistency after recovery.",
            ["cache", "invalidation", "strategies"],
            1.0
        ),
        SearchDocument(
            10,
            "Queue Drain Procedures",
            "Explains safe draining of message queues during recovery, including idempotency, poison message handling, and checkpointing.",
            ["queue", "drain", "procedures"],
            1.0
        ),
        SearchDocument(
            11,
            "Graceful vs Forced Service Restarts",
            "Compares the impact and use cases for graceful and forced restarts, including session draining and state preservation.",
            ["service", "restart", "graceful", "forced"],
            1.0
        ),
        SearchDocument(
            12,
            "Transactional Rollback Techniques",
            "Explores transactional rollback techniques, including compensating transactions and two-phase commit aborts.",
            ["transactional", "rollback", "techniques"],
            1.0
        ),
        SearchDocument(
            13,
            "Exponential Backoff and Jitter",
            "Details the implementation of exponential backoff with jitter to avoid thundering herd problems in retry logic.",
            ["exponential", "backoff", "jitter", "retry"],
            1.0
        ),
        SearchDocument(
            14,
            "Configuration Drift Detection and Repair",
            "Describes methods for detecting and repairing configuration drift using checksums, versioning, and automated remediation.",
            ["configuration", "drift", "repair"],
            1.0
        ),
        SearchDocument(
            15,
            "Dependency Graph Construction",
            "Explains how to construct and analyze dependency graphs for service recovery and restart sequencing.",
            ["dependency", "graph", "construction"],
            1.0
        ),
        SearchDocument(
            16,
            "Point-in-Time Database Recovery",
            "Covers point-in-time recovery using backups and transaction logs, with examples for PostgreSQL and MySQL.",
            ["database", "recovery", "point-in-time"],
            1.0
        ),
        SearchDocument(
            17,
            "File System Journaling",
            "Explains how journaling file systems aid in rapid recovery after crashes and power failures.",
            ["file", "system", "journaling", "recovery"],
            1.0
        ),
        SearchDocument(
            18,
            "Network Partition Healing",
            "Discusses strategies for detecting and healing network partitions, including split-brain avoidance.",
            ["network", "partition", "healing"],
            1.0
        ),
        SearchDocument(
            19,
            "Write-Through Cache Invalidation",
            "Describes write-through cache invalidation and its role in maintaining consistency during recovery.",
            ["cache", "write-through", "invalidation"],
            1.0
        ),
        SearchDocument(
            20,
            "Poison Message Handling in Queues",
            "Covers detection and handling of poison messages during queue drain procedures to prevent repeated failures.",
            ["queue", "poison", "message", "handling"],
            1.0
        ),
        SearchDocument(
            21,
            "Rolling Restart Patterns",
            "Explains rolling restart patterns for minimizing downtime and maintaining service availability.",
            ["service", "rolling", "restart", "patterns"],
            1.0
        ),
        SearchDocument(
            22,
            "Automated Rollback Generation",
            "Details automated generation of rollback scripts and procedures using configuration diffs and version control.",
            ["rollback", "automated", "generation"],
            1.0
        ),
        SearchDocument(
            23,
            "Circuit Breaker Integration with Retry Logic",
            "Discusses integrating circuit breakers with retry logic to prevent cascading failures.",
            ["circuit", "breaker", "retry", "logic"],
            1.0
        ),
        SearchDocument(
            24,
            "Configuration Validation Strategies",
            "Explores strategies for validating configuration correctness before and after repair.",
            ["configuration", "validation", "strategies"],
            1.0
        ),
        SearchDocument(
            25,
            "Lazy Dependency Resolution",
            "Describes lazy loading and resolution of dependencies to accelerate service recovery.",
            ["dependency", "lazy", "resolution"],
            1.0
        ),
        SearchDocument(
            26,
            "Snapshot-Based File System Restoration",
            "Explains how to use file system snapshots for rapid restoration after corruption or accidental deletion.",
            ["file", "system", "snapshot", "restoration"],
            1.0
        ),
        SearchDocument(
            27,
            "DNS Cache Flushing in Network Recovery",
            "Describes the importance of DNS cache flushing during network recovery procedures.",
            ["network", "dns", "cache", "flushing"],
            1.0
        ),
        SearchDocument(
            28,
            "Checkpointing in Queue Drain Procedures",
            "Covers checkpointing techniques to ensure safe and resumable queue draining.",
            ["queue", "checkpointing", "drain", "procedures"],
            1.0
        ),
        SearchDocument(
            29,
            "Fail-Fast Dependency Resolution",
            "Discusses fail-fast strategies for dependency resolution to avoid cascading failures.",
            ["dependency", "fail-fast", "resolution"],
            1.0
        ),
        SearchDocument(
            30,
            "Idempotency in Queue Draining",
            "Explains the importance of idempotency in queue drain procedures for safe message processing.",
            ["queue", "idempotency", "drain"],
            1.0
        ),
        SearchDocument(
            31,
            "Service Restart Impact Analysis",
            "Analyzes the impact of various service restart strategies on system availability and recovery time.",
            ["service", "restart", "impact", "analysis"],
            1.0
        ),
        SearchDocument(
            32,
            "Automated Configuration Remediation",
            "Describes tools and patterns for automated remediation of configuration errors during recovery.",
            ["configuration", "automated", "remediation"],
            1.0
        ),
        SearchDocument(
            33,
            "Replication Failover for Database Recovery",
            "Explores replication failover techniques for minimizing downtime during database recovery.",
            ["database", "replication", "failover", "recovery"],
            1.0
        ),
        SearchDocument(
            34,
            "Two-Phase Commit Abort Handling",
            "Details abort handling in two-phase commit protocols for transactional rollback.",
            ["transactional", "two-phase", "commit", "abort"],
            1.0
        ),
        SearchDocument(
            35,
            "Explicit Cache Invalidation",
            "Explains explicit cache invalidation mechanisms for ensuring data consistency.",
            ["cache", "explicit", "invalidation"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)