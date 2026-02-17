import math
import threading
import re
import heapq
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

# --- Data Classes ---

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

# --- Search Index Implementation ---

class SearchIndex:
    def __init__(self):
        self._documents: Dict[str, SearchDocument] = {}
        self._doc_tokens: Dict[str, List[str]] = {}
        self._inverted_index: Dict[str, Set[str]] = defaultdict(set)
        self._term_doc_freq: Dict[str, int] = defaultdict(int)
        self._doc_lengths: Dict[str, int] = {}
        self._avg_doc_length: float = 0.0
        self._lock = threading.RLock()
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75
        self._idf_cache: Dict[str, float] = {}
        self._total_docs = 0
        self._dirty = True

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                self._remove_document(doc.id)
            tokens = self._tokenize(doc.title + ' ' + doc.content + ' ' + ' '.join(doc.tags))
            self._documents[doc.id] = doc
            self._doc_tokens[doc.id] = tokens
            self._doc_lengths[doc.id] = len(tokens)
            for token in set(tokens):
                self._inverted_index[token].add(doc.id)
                self._term_doc_freq[token] += 1
            self._total_docs = len(self._documents)
            self._avg_doc_length = (
                sum(self._doc_lengths.values()) / self._total_docs if self._total_docs > 0 else 0.0
            )
            self._dirty = True

    def _remove_document(self, doc_id: str):
        if doc_id not in self._documents:
            return
        tokens = self._doc_tokens[doc_id]
        for token in set(tokens):
            self._inverted_index[token].discard(doc_id)
            self._term_doc_freq[token] -= 1
            if self._term_doc_freq[token] <= 0:
                del self._term_doc_freq[token]
                del self._inverted_index[token]
        del self._documents[doc_id]
        del self._doc_tokens[doc_id]
        del self._doc_lengths[doc_id]

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        with self._lock:
            query_tokens = self._tokenize(query)
            if not query_tokens:
                return []
            doc_candidates = set()
            for token in query_tokens:
                doc_candidates.update(self._inverted_index.get(token, set()))
            if not doc_candidates:
                return []
            self._refresh_idf_cache()
            scored = []
            for doc_id in doc_candidates:
                bm25_score = self._score_bm25(doc_id, query_tokens)
                tfidf_score = self._score_tfidf(doc_id, query_tokens)
                final_score = bm25_score * 0.7 + tfidf_score * 0.3
                doc = self._documents[doc_id]
                snippet = self._build_snippet(doc, query_tokens)
                scored.append((final_score, SearchResult(doc_id, final_score, doc.title, snippet)))
            top_results = heapq.nlargest(limit, scored, key=lambda x: x[0])
            return [r[1] for r in top_results]

    def get_stats(self) -> Dict[str, int]:
        with self._lock:
            return {
                "documents": len(self._documents),
                "unique_terms": len(self._inverted_index),
                "avg_doc_length": int(self._avg_doc_length),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        text = re.sub(r'[^a-z0-9_]+', ' ', text)
        tokens = [t for t in text.split() if len(t) > 1]
        return tokens

    def _refresh_idf_cache(self):
        if not self._dirty:
            return
        N = max(1, self._total_docs)
        self._idf_cache = {}
        for term, df in self._term_doc_freq.items():
            self._idf_cache[term] = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._dirty = False

    def _compute_idf(self, term: str) -> float:
        return self._idf_cache.get(term, math.log(1 + self._total_docs))

    def _score_bm25(self, doc_id: str, query_tokens: List[str]) -> float:
        doc = self._documents[doc_id]
        tokens = self._doc_tokens[doc_id]
        freq = Counter(tokens)
        score = 0.0
        dl = self._doc_lengths[doc_id]
        avg_dl = self._avg_doc_length if self._avg_doc_length > 0 else 1.0
        for term in query_tokens:
            if term not in freq:
                continue
            idf = self._compute_idf(term)
            tf = freq[term]
            denom = tf + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * dl / avg_dl)
            term_score = idf * ((tf * (self._bm25_k1 + 1)) / denom)
            score += term_score
        return score * doc.weight

    def _score_tfidf(self, doc_id: str, query_tokens: List[str]) -> float:
        tokens = self._doc_tokens[doc_id]
        freq = Counter(tokens)
        dl = self._doc_lengths[doc_id]
        score = 0.0
        for term in query_tokens:
            if term not in freq:
                continue
            tf = freq[term] / dl
            idf = self._compute_idf(term)
            score += tf * idf
        return score

    def _build_snippet(self, doc: SearchDocument, query_tokens: List[str], length: int = 160) -> str:
        content = doc.content
        content_lower = content.lower()
        positions = []
        for qt in query_tokens:
            idx = content_lower.find(qt)
            if idx >= 0:
                positions.append(idx)
        if positions:
            start = max(0, min(positions) - 30)
        else:
            start = 0
        snippet = content[start:start + length]
        for qt in query_tokens:
            snippet = re.sub(r'(?i)(' + re.escape(qt) + r')', r'**\1**', snippet)
        return snippet.strip()

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

# --- Pre-seeding Documents ---

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            id="1",
            title="Twelve-Factor App: Configuration",
            content="Store config in the environment. Configuration that varies between deploys (staging, production, developer environments) should be stored in environment variables.",
            tags=["twelve_factor_config", "environment_management"],
            weight=1.0
        ),
        SearchDocument(
            id="2",
            title="Secret Management Best Practices",
            content="Never commit secrets to version control. Use secret managers to securely store and access secrets at runtime.",
            tags=["secret_management", "config_security"],
            weight=1.0
        ),
        SearchDocument(
            id="3",
            title="Versioning Configuration Files",
            content="Track configuration changes using version control systems. Tag releases and maintain changelogs for configuration updates.",
            tags=["config_versioning", "config_as_code"],
            weight=1.0
        ),
        SearchDocument(
            id="4",
            title="Configuration Inheritance Patterns",
            content="Use base configuration files and override settings for specific environments. Inheritance reduces duplication and eases maintenance.",
            tags=["config_inheritance", "environment_management"],
            weight=1.0
        ),
        SearchDocument(
            id="5",
            title="Hot Reloading Configuration",
            content="Support hot reloading to apply configuration changes without restarting services. Watch for file or environment changes and reload safely.",
            tags=["hot_reload", "config_observability"],
            weight=1.0
        ),
        SearchDocument(
            id="6",
            title="Feature Flags in Production",
            content="Feature flags enable dynamic toggling of features. Store flag states in configuration and ensure fast, consistent access.",
            tags=["feature_flags", "config_testing"],
            weight=1.0
        ),
        SearchDocument(
            id="7",
            title="Validating Configuration Schemas",
            content="Validate configuration files against schemas (e.g., JSON Schema, YAML). Fail fast on invalid config to prevent runtime errors.",
            tags=["config_validation", "config_testing"],
            weight=1.0
        ),
        SearchDocument(
            id="8",
            title="Detecting Configuration Drift",
            content="Monitor deployed configuration for drift from source of truth. Alert and remediate when drift is detected.",
            tags=["config_drift_detection", "config_observability"],
            weight=1.0
        ),
        SearchDocument(
            id="9",
            title="Managing Multiple Environments",
            content="Use environment variables and per-environment config files to manage dev, staging, and prod settings.",
            tags=["environment_management", "twelve_factor_config"],
            weight=1.0
        ),
        SearchDocument(
            id="10",
            title="Configuration as Code",
            content="Store configuration in version-controlled files. Use code review and CI/CD pipelines to manage configuration changes.",
            tags=["config_as_code", "config_security"],
            weight=1.0
        ),
        SearchDocument(
            id="11",
            title="Securing Configuration Data",
            content="Encrypt sensitive configuration at rest and in transit. Limit access to configuration data using RBAC and audit logs.",
            tags=["config_security", "secret_management"],
            weight=1.0
        ),
        SearchDocument(
            id="12",
            title="Immutable Infrastructure and Configuration",
            content="Treat infrastructure and configuration as immutable. Deploy new versions rather than mutating live systems.",
            tags=["immutable_infrastructure", "config_versioning"],
            weight=1.0
        ),
        SearchDocument(
            id="13",
            title="Templating Configuration Files",
            content="Use templates (e.g., Jinja2, Helm) to generate environment-specific configuration from base templates.",
            tags=["config_templating", "config_inheritance"],
            weight=1.0
        ),
        SearchDocument(
            id="14",
            title="Testing Configuration Changes",
            content="Test configuration in CI/CD pipelines. Use static analysis and integration tests to catch errors early.",
            tags=["config_testing", "config_validation"],
            weight=1.0
        ),
        SearchDocument(
            id="15",
            title="Observability for Configuration",
            content="Log configuration loads and changes. Expose config state via metrics and dashboards for troubleshooting.",
            tags=["config_observability", "hot_reload"],
            weight=1.0
        ),
        SearchDocument(
            id="16",
            title="Dynamic Configuration Reloading",
            content="Implement mechanisms to reload configuration at runtime without downtime, using signals or file watchers.",
            tags=["hot_reload", "config_observability"],
            weight=1.0
        ),
        SearchDocument(
            id="17",
            title="Configuration File Formats",
            content="Choose human-readable and machine-parseable formats like YAML, JSON, or TOML for configuration files.",
            tags=["config_validation", "config_as_code"],
            weight=1.0
        ),
        SearchDocument(
            id="18",
            title="Auditing Configuration Changes",
            content="Maintain audit logs for configuration changes. Track who changed what and when for compliance.",
            tags=["config_security", "config_versioning"],
            weight=1.0
        ),
        SearchDocument(
            id="19",
            title="Centralized Configuration Management",
            content="Use centralized services (e.g., Consul, etcd) to manage and distribute configuration to services.",
            tags=["environment_management", "config_as_code"],
            weight=1.0
        ),
        SearchDocument(
            id="20",
            title="Configuration Rollback Strategies",
            content="Support rolling back to previous configuration versions quickly in case of failures.",
            tags=["config_versioning", "config_testing"],
            weight=1.0
        ),
        SearchDocument(
            id="21",
            title="Parameterizing Configuration",
            content="Parameterize configuration to support multiple deployments with minimal changes.",
            tags=["config_templating", "environment_management"],
            weight=1.0
        ),
        SearchDocument(
            id="22",
            title="Managing Secrets in CI/CD",
            content="Integrate secret management into CI/CD pipelines. Use ephemeral secrets and rotate them regularly.",
            tags=["secret_management", "config_security"],
            weight=1.0
        ),
        SearchDocument(
            id="23",
            title="Configuration Change Notification",
            content="Notify services and teams when configuration changes. Use webhooks or message queues for notifications.",
            tags=["config_observability", "hot_reload"],
            weight=1.0
        ),
        SearchDocument(
            id="24",
            title="Configuration Policy Enforcement",
            content="Enforce policies on configuration values using validation tools and admission controllers.",
            tags=["config_validation", "config_security"],
            weight=1.0
        ),
        SearchDocument(
            id="25",
            title="Managing Feature Flags at Scale",
            content="Organize, document, and retire feature flags to avoid technical debt. Use centralized flag management.",
            tags=["feature_flags", "config_as_code"],
            weight=1.0
        ),
        SearchDocument(
            id="26",
            title="Configuration for Immutable Deployments",
            content="Embed configuration in immutable artifacts. Avoid runtime mutation for predictability.",
            tags=["immutable_infrastructure", "twelve_factor_config"],
            weight=1.0
        ),
        SearchDocument(
            id="27",
            title="Configuration Linting",
            content="Lint configuration files to catch errors and enforce style before deployment.",
            tags=["config_testing", "config_validation"],
            weight=1.0
        ),
        SearchDocument(
            id="28",
            title="Dynamic Environment Variables",
            content="Inject environment variables dynamically at runtime for flexible configuration.",
            tags=["twelve_factor_config", "environment_management"],
            weight=1.0
        ),
        SearchDocument(
            id="29",
            title="Configuration Documentation",
            content="Document configuration options, defaults, and usage for maintainability.",
            tags=["config_as_code", "config_observability"],
            weight=1.0
        ),
        SearchDocument(
            id="30",
            title="Configuration and Compliance",
            content="Ensure configuration adheres to compliance requirements. Automate checks and reporting.",
            tags=["config_security", "config_validation"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)