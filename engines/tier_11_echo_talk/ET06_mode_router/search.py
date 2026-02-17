import math
import threading
import heapq
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

# --- SearchIndex Class ---

class SearchIndex:
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.total_docs: int = 0
        self.avg_doc_length: float = 0.0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = defaultdict(dict)
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            term_counts = Counter(tokens)
            self.term_freqs[doc.id] = term_counts
            for term in term_counts:
                self.term_doc_freq[term] += 1
            self._idf_cache.clear()
            self._tfidf_cache.clear()
            self._update_avg_doc_length()

    def _update_avg_doc_length(self):
        if self.total_docs == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        doc = self.documents[doc_id]
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            numerator = tf * (self._bm25_k1 + 1)
            denominator = tf + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_length / (self.avg_doc_length or 1))
            score += idf * (numerator / (denominator or 1))
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        if doc_id in self._tfidf_cache and query_terms == self._tfidf_cache[doc_id].get('query_terms', []):
            return self._tfidf_cache[doc_id]['score']
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        doc = self.documents[doc_id]
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / (doc_length or 1)
            idf = self._compute_idf(term)
            score += tf_norm * idf
        score *= doc.weight
        self._tfidf_cache[doc_id]['score'] = score
        self._tfidf_cache[doc_id]['query_terms'] = query_terms
        return score

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        scores = []
        for doc_id in self.documents:
            if use_tfidf:
                score = self._score_tfidf(doc_id, query_terms)
            else:
                score = self._score_bm25(doc_id, query_terms)
            if score > 0:
                snippet = self._make_snippet(doc_id, query_terms)
                scores.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scores.sort(key=lambda r: r.score, reverse=True)
        return scores[:limit]

    def _make_snippet(self, doc_id: int, query_terms: List[str]) -> str:
        doc = self.documents[doc_id]
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:160] + '...' if len(content) > 160 else content
        start = max(positions[0] - 10, 0)
        end = min(positions[0] + 20, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        return snippet + '...' if len(snippet_tokens) < len(tokens) else snippet

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                'total_docs': self.total_docs,
                'avg_doc_length': self.avg_doc_length,
                'unique_terms': len(self.term_doc_freq),
            }

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

# --- Preseed Documents ---

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1, "Wakeword Detection Fundamentals",
            "Hey Echo Sentinel wakeword detection uses advanced neural models to identify activation phrases with high accuracy and low latency.",
            ["wakeword", "detection", "neural", "activation"], 1.0
        ),
        SearchDocument(
            2, "Activation Confidence Thresholds",
            "Activation confidence thresholds are dynamically adjusted based on environmental noise and user profile to minimize false positives.",
            ["confidence", "threshold", "activation", "noise"], 1.0
        ),
        SearchDocument(
            3, "False Positive Rejection Strategies",
            "False positive rejection in wakeword detection leverages multi-stage filtering and context-aware scoring to ensure reliable activation.",
            ["false positive", "rejection", "wakeword", "context"], 1.0
        ),
        SearchDocument(
            4, "Multi-Wakeword Routing",
            "Multi-wakeword routing enables simultaneous support for multiple activation phrases, optimizing for user intent and device context.",
            ["multi-wakeword", "routing", "intent", "context"], 1.0
        ),
        SearchDocument(
            5, "Mode Routing Decision Tree",
            "The mode routing decision tree evaluates query complexity, urgency, and context to select the optimal processing mode.",
            ["mode", "routing", "decision tree", "complexity"], 1.0
        ),
        SearchDocument(
            6, "Query Complexity Scoring",
            "Query complexity scoring assigns a numerical value to each query based on linguistic features, expected processing time, and user history.",
            ["query", "complexity", "scoring", "processing"], 1.0
        ),
        SearchDocument(
            7, "Mode Switching State Machine",
            "A robust state machine governs mode switching, ensuring smooth transitions between normal, degraded, and emergency modes.",
            ["mode", "switching", "state machine", "emergency"], 1.0
        ),
        SearchDocument(
            8, "Routing Latency Budgets",
            "Routing latency budgets are enforced to guarantee timely responses, with fallback chains activated when latency thresholds are exceeded.",
            ["routing", "latency", "budgets", "fallback"], 1.0
        ),
        SearchDocument(
            9, "Load Balancing Across Mode Handlers",
            "Load balancing distributes queries across mode handlers to prevent bottlenecks and maintain consistent performance.",
            ["load balancing", "mode handlers", "performance"], 1.0
        ),
        SearchDocument(
            10, "Routing Fallback Chains",
            "Fallback chains provide alternative routing paths when primary handlers fail or are overloaded, ensuring query completion.",
            ["routing", "fallback", "chains", "overload"], 1.0
        ),
        SearchDocument(
            11, "Priority Routing for Urgent Queries",
            "Urgent queries are prioritized in routing, bypassing batch queues and activating emergency bypass when necessary.",
            ["priority", "routing", "urgent", "bypass"], 1.0
        ),
        SearchDocument(
            12, "Batch Routing for Non-Urgent Queries",
            "Batch routing aggregates non-urgent queries for efficient processing, optimizing resource utilization and throughput.",
            ["batch", "routing", "non-urgent", "throughput"], 1.0
        ),
        SearchDocument(
            13, "A/B Routing for Testing",
            "A/B routing enables controlled testing of new mode handlers, collecting telemetry for performance comparison and improvement.",
            ["ab routing", "testing", "telemetry", "performance"], 1.0
        ),
        SearchDocument(
            14, "Routing Telemetry Collection",
            "Telemetry collection monitors routing decisions, latency, and handler performance, feeding data into continuous optimization pipelines.",
            ["routing", "telemetry", "collection", "optimization"], 1.0
        ),
        SearchDocument(
            15, "Routing Cache for Repeated Patterns",
            "Routing cache stores results for repeated query patterns, reducing latency and improving user experience.",
            ["routing", "cache", "patterns", "latency"], 1.0
        ),
        SearchDocument(
            16, "Context-Aware Routing",
            "Context-aware routing leverages user history, device state, and environmental cues to select the best processing mode.",
            ["context", "routing", "device", "environment"], 1.0
        ),
        SearchDocument(
            17, "Time-of-Day Routing Preferences",
            "Routing preferences adapt based on time-of-day, prioritizing certain modes during peak hours and enabling energy-saving modes at night.",
            ["routing", "time-of-day", "preferences", "energy"], 1.0
        ),
        SearchDocument(
            18, "Routing Circuit Breakers",
            "Circuit breakers monitor handler health and automatically reroute queries when failures or slowdowns are detected.",
            ["routing", "circuit breakers", "health", "failure"], 1.0
        ),
        SearchDocument(
            19, "Degraded Mode Routing",
            "Degraded mode routing activates when system resources are limited, maintaining basic functionality with reduced features.",
            ["degraded", "routing", "resources", "features"], 1.0
        ),
        SearchDocument(
            20, "Emergency Bypass Routing",
            "Emergency bypass routing ensures critical queries are processed immediately, overriding normal routing constraints.",
            ["emergency", "bypass", "routing", "critical"], 1.0
        ),
        SearchDocument(
            21, "Sentinel Wakeword Model Architecture",
            "The Sentinel wakeword model uses convolutional and recurrent layers to maximize detection accuracy across diverse environments.",
            ["sentinel", "wakeword", "model", "architecture"], 1.0
        ),
        SearchDocument(
            22, "Wakeword Detection Latency Optimization",
            "Latency optimization techniques include model pruning, quantization, and hardware acceleration for wakeword detection.",
            ["wakeword", "detection", "latency", "optimization"], 1.0
        ),
        SearchDocument(
            23, "User Profile-Based Routing",
            "Routing decisions are influenced by user profiles, enabling personalized mode selection and adaptive thresholds.",
            ["user profile", "routing", "personalized", "adaptive"], 1.0
        ),
        SearchDocument(
            24, "Environmental Noise Adaptation",
            "Environmental noise adaptation improves wakeword detection by dynamically adjusting thresholds and filtering strategies.",
            ["environmental", "noise", "adaptation", "wakeword"], 1.0
        ),
        SearchDocument(
            25, "Handler Performance Metrics",
            "Performance metrics for mode handlers include latency, throughput, error rates, and user satisfaction scores.",
            ["handler", "performance", "metrics", "latency"], 1.0
        ),
        SearchDocument(
            26, "Query Pattern Recognition",
            "Pattern recognition identifies repeated query types, enabling caching and preemptive routing optimizations.",
            ["query", "pattern", "recognition", "caching"], 1.0
        ),
        SearchDocument(
            27, "Device Context Integration",
            "Device context integration ensures routing decisions account for hardware capabilities and current device state.",
            ["device", "context", "integration", "hardware"], 1.0
        ),
        SearchDocument(
            28, "Routing Policy Management",
            "Policy management allows administrators to define routing rules, fallback priorities, and emergency protocols.",
            ["routing", "policy", "management", "protocols"], 1.0
        ),
        SearchDocument(
            29, "Wakeword Model Training Pipeline",
            "The training pipeline for wakeword models includes data augmentation, validation, and continuous deployment.",
            ["wakeword", "model", "training", "pipeline"], 1.0
        ),
        SearchDocument(
            30, "Routing Security Considerations",
            "Security considerations include authentication, encryption, and anomaly detection in routing decisions.",
            ["routing", "security", "authentication", "encryption"], 1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)