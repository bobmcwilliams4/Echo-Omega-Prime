import threading
import math
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
        self.tags_index: Dict[str, set] = defaultdict(set)
        self.lock = threading.Lock()
        self.total_terms = 0
        self.avg_doc_length = 0.0
        self._re_token = re.compile(r"\w+")
        self._idf_cache: Dict[str, float] = {}
        self._stats_cache = None

    def _tokenize(self, text: str) -> List[str]:
        return [t.lower() for t in self._re_token.findall(text)]

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_terms += len(tokens)
            for token in tokens:
                self.term_freqs[doc.id][token] += 1
            for token in set(tokens):
                self.term_doc_freq[token] += 1
            for tag in doc.tags:
                self.tags_index[tag.lower()].add(doc.id)
            self.avg_doc_length = self.total_terms / max(1, len(self.documents))
            self._idf_cache.clear()
            self._stats_cache = None

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        N = len(self.documents)
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: str, query_terms: List[str], k1=1.5, b=0.75) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1
        doc = self.documents[doc_id]
        tf = self.term_freqs[doc_id]
        for term in query_terms:
            f = tf.get(term, 0)
            idf = self._compute_idf(term)
            numerator = f * (k1 + 1)
            denominator = f + k1 * (1 - b + b * (doc_len / avg_dl))
            score += idf * (numerator / (denominator + 1e-9))
        return score * doc.weight

    def _score_tfidf(self, doc_id: str, query_terms: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        tf = self.term_freqs[doc_id]
        for term in query_terms:
            f = tf.get(term, 0)
            if doc_len > 0:
                tf_norm = f / doc_len
            else:
                tf_norm = 0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False, tags: Optional[List[str]] = None) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_ids = set(self.documents.keys())
        if tags:
            tag_ids = set()
            for tag in tags:
                tag_ids |= self.tags_index.get(tag.lower(), set())
            candidate_ids &= tag_ids
        scores = []
        for doc_id in candidate_ids:
            if use_tfidf:
                score = self._score_tfidf(doc_id, query_terms)
            else:
                score = self._score_bm25(doc_id, query_terms)
            if score > 0:
                snippet = self._make_snippet(self.documents[doc_id], query_terms)
                scores.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scores.sort(key=lambda r: r.score, reverse=True)
        return scores[:limit]

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], max_len: int = 200) -> str:
        tokens = self._tokenize(doc.content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = doc.content[:max_len]
        else:
            start = max(positions[0] - 10, 0)
            end = min(positions[0] + 30, len(tokens))
            snippet_tokens = tokens[start:end]
            snippet = " ".join(snippet_tokens)
            if len(snippet) > max_len:
                snippet = snippet[:max_len] + "..."
        return snippet

    def get_stats(self) -> Dict[str, any]:
        if self._stats_cache is not None:
            return self._stats_cache
        stats = {
            "num_documents": len(self.documents),
            "avg_doc_length": self.avg_doc_length,
            "num_terms": len(self.term_doc_freq),
            "num_tags": len(self.tags_index),
            "total_terms": self.total_terms,
        }
        self._stats_cache = stats
        return stats

# Singleton factory
_search_index_instance = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            "1",
            "Conversation Session Lifecycle",
            "Describes the stages of a conversation session, including creation, active engagement, timeout, and resumption. Covers lifecycle management best practices.",
            ["session", "lifecycle", "management"],
            1.0
        ),
        SearchDocument(
            "2",
            "Session Creation and Resumption",
            "Outlines strategies for creating new conversation sessions and resuming previous sessions, including context restoration and user prompts.",
            ["session", "creation", "resumption"],
            1.0
        ),
        SearchDocument(
            "3",
            "Context Persistence Strategies",
            "Discusses methods for persisting conversation context across sessions, including serialization, key-value storage, and privacy considerations.",
            ["context", "persistence", "storage"],
            1.0
        ),
        SearchDocument(
            "4",
            "Conversation History Storage (D1 KV)",
            "Explains how to store conversation history using D1 KV, ensuring efficient retrieval and scalability.",
            ["history", "storage", "D1", "KV"],
            1.0
        ),
        SearchDocument(
            "5",
            "User Preference Tracking",
            "Details techniques for tracking user preferences within conversations, including explicit and implicit signals, and adapting conversation flows.",
            ["user", "preferences", "tracking"],
            1.0
        ),
        SearchDocument(
            "6",
            "Conversation Branching",
            "Explores branching logic in conversations, enabling multiple possible paths and outcomes based on user input and system state.",
            ["conversation", "branching", "logic"],
            1.0
        ),
        SearchDocument(
            "7",
            "Undo/Redo in Conversations",
            "Provides mechanisms for undoing and redoing actions within a conversation, maintaining state consistency and user control.",
            ["undo", "redo", "state"],
            1.0
        ),
        SearchDocument(
            "8",
            "Conversation Search and Retrieval",
            "Covers search algorithms and retrieval techniques for finding relevant conversations and session fragments.",
            ["search", "retrieval", "conversation"],
            1.0
        ),
        SearchDocument(
            "9",
            "Session Timeout Management",
            "Describes timeout policies for conversation sessions, including inactivity detection and session expiry handling.",
            ["session", "timeout", "management"],
            1.0
        ),
        SearchDocument(
            "10",
            "Multi-Device Conversation Sync",
            "Explains synchronization of conversation state across multiple devices, ensuring seamless user experience.",
            ["multi-device", "sync", "conversation"],
            1.0
        ),
        SearchDocument(
            "11",
            "Conversation Export and Import",
            "Details procedures for exporting and importing conversation sessions, including format specifications and privacy safeguards.",
            ["export", "import", "conversation"],
            1.0
        ),
        SearchDocument(
            "12",
            "Privacy-Aware State Management",
            "Discusses privacy-aware approaches to managing conversation state, including data minimization and user consent.",
            ["privacy", "state", "management"],
            1.0
        ),
        SearchDocument(
            "13",
            "PII Redaction in Stored State",
            "Explains techniques for redacting personally identifiable information (PII) from stored conversation state.",
            ["PII", "redaction", "privacy"],
            1.0
        ),
        SearchDocument(
            "14",
            "Conversation Analytics",
            "Outlines analytics methods for conversation sessions, including engagement metrics and quality assessment.",
            ["analytics", "metrics", "conversation"],
            1.0
        ),
        SearchDocument(
            "15",
            "Topic Distribution Tracking",
            "Describes tracking topic distribution within conversations for improved context management and analytics.",
            ["topic", "distribution", "tracking"],
            1.0
        ),
        SearchDocument(
            "16",
            "User Engagement Scoring",
            "Explores scoring models for user engagement in conversation sessions, including activity and satisfaction signals.",
            ["user", "engagement", "scoring"],
            1.0
        ),
        SearchDocument(
            "17",
            "Conversation Quality Metrics",
            "Defines metrics for assessing conversation quality, such as coherence, relevance, and user satisfaction.",
            ["quality", "metrics", "conversation"],
            1.0
        ),
        SearchDocument(
            "18",
            "AB Testing Conversation Flows",
            "Describes AB testing methodologies for conversation flows, including variant management and statistical analysis.",
            ["AB", "testing", "conversation"],
            1.0
        ),
        SearchDocument(
            "19",
            "Conversation Templating",
            "Explains templating systems for conversation flows, enabling reuse and customization.",
            ["templating", "conversation", "reuse"],
            1.0
        ),
        SearchDocument(
            "20",
            "Cross-Session Context Linking",
            "Covers methods for linking context across multiple conversation sessions, enhancing continuity and personalization.",
            ["context", "linking", "session"],
            1.0
        ),
        SearchDocument(
            "21",
            "Session State Serialization",
            "Details serialization formats and strategies for session state persistence and transfer.",
            ["serialization", "session", "state"],
            1.0
        ),
        SearchDocument(
            "22",
            "Session Fragment Retrieval",
            "Explores retrieval of session fragments for partial context restoration and analytics.",
            ["fragment", "retrieval", "session"],
            1.0
        ),
        SearchDocument(
            "23",
            "Conversation Flow Optimization",
            "Discusses optimization techniques for conversation flows, including path pruning and adaptive branching.",
            ["optimization", "flow", "conversation"],
            1.0
        ),
        SearchDocument(
            "24",
            "Conversation Session Security",
            "Outlines security considerations for conversation sessions, including authentication and data protection.",
            ["security", "session", "protection"],
            1.0
        ),
        SearchDocument(
            "25",
            "Session Recovery Strategies",
            "Describes strategies for recovering lost or corrupted conversation sessions, including backup and restoration.",
            ["recovery", "session", "backup"],
            1.0
        ),
        SearchDocument(
            "26",
            "User Identity Management",
            "Explains user identity management within conversation sessions, including authentication and personalization.",
            ["identity", "user", "management"],
            1.0
        ),
        SearchDocument(
            "27",
            "Conversation Session Auditing",
            "Describes auditing mechanisms for conversation sessions, including logging and compliance.",
            ["auditing", "session", "logging"],
            1.0
        ),
        SearchDocument(
            "28",
            "Session State Versioning",
            "Details versioning strategies for session state, supporting rollback and historical analysis.",
            ["versioning", "session", "state"],
            1.0
        ),
        SearchDocument(
            "29",
            "Conversation Session Scalability",
            "Explores scalability techniques for conversation session management, including sharding and load balancing.",
            ["scalability", "session", "management"],
            1.0
        ),
        SearchDocument(
            "30",
            "Session State Consistency",
            "Discusses consistency models for session state, ensuring reliable context across devices and flows.",
            ["consistency", "session", "state"],
            1.0
        ),
        SearchDocument(
            "31",
            "Session State Encryption",
            "Explains encryption approaches for session state, protecting sensitive data in transit and at rest.",
            ["encryption", "session", "state"],
            1.0
        ),
        SearchDocument(
            "32",
            "Session State Compression",
            "Details compression techniques for session state storage and transfer, optimizing resource usage.",
            ["compression", "session", "state"],
            1.0
        ),
        SearchDocument(
            "33",
            "Session State Deletion Policies",
            "Outlines deletion policies for session state, including retention periods and compliance requirements.",
            ["deletion", "session", "state"],
            1.0
        ),
        SearchDocument(
            "34",
            "Session State Access Control",
            "Describes access control mechanisms for session state, ensuring authorized usage and privacy.",
            ["access", "control", "session", "state"],
            1.0
        ),
        SearchDocument(
            "35",
            "Session State Monitoring",
            "Explains monitoring strategies for session state, including anomaly detection and alerting.",
            ["monitoring", "session", "state"],
            1.0
        ),
        SearchDocument(
            "36",
            "Session State Migration",
            "Details migration approaches for session state, supporting upgrades and platform transitions.",
            ["migration", "session", "state"],
            1.0
        ),
        SearchDocument(
            "37",
            "Session State API Design",
            "Discusses API design principles for session state management, including extensibility and versioning.",
            ["API", "design", "session", "state"],
            1.0
        ),
        SearchDocument(
            "38",
            "Session State Testing",
            "Outlines testing methodologies for session state, including unit, integration, and end-to-end tests.",
            ["testing", "session", "state"],
            1.0
        ),
        SearchDocument(
            "39",
            "Session State Documentation",
            "Explains documentation best practices for session state, supporting maintainability and onboarding.",
            ["documentation", "session", "state"],
            1.0
        ),
        SearchDocument(
            "40",
            "Session State Integration",
            "Describes integration strategies for session state with external systems and services.",
            ["integration", "session", "state"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)