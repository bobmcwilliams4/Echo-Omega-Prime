import math
import threading
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
        self.total_terms: int = 0
        self.lock = threading.Lock()
        self.k1 = 1.5
        self.b = 0.75
        self.avg_doc_length: float = 0.0
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[Tuple[str, str], float] = {}
        self._stats_cache: Optional[Dict[str, int]] = None

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_terms += len(tokens)
            term_counts = Counter(tokens)
            for term, freq in term_counts.items():
                self.term_freqs[term][doc.id] = freq
                self.term_doc_freq[term] += 1
            self.avg_doc_length = self.total_terms / max(len(self.documents), 1)
            self._idf_cache.clear()
            self._tfidf_cache.clear()
            self._stats_cache = None

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scores = defaultdict(float)
        snippets = {}
        for doc_id, doc in self.documents.items():
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            combined_score = bm25_score * 0.7 + tfidf_score * 0.3
            if combined_score > 0:
                scores[doc_id] = combined_score * doc.weight
                snippets[doc_id] = self._make_snippet(doc, query_terms)
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = snippets[doc_id]
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, int]:
        if self._stats_cache:
            return self._stats_cache
        stats = {
            'documents': len(self.documents),
            'terms': len(self.term_doc_freq),
            'avg_doc_length': int(self.avg_doc_length),
            'total_terms': self.total_terms
        }
        self._stats_cache = stats
        return stats

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        N = len(self.documents)
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: str, query_terms: List[str]) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        doc = self.documents[doc_id]
        for term in query_terms:
            freq = self.term_freqs[term].get(doc_id, 0)
            idf = self._compute_idf(term)
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (1 - self.b + self.b * doc_length / (self.avg_doc_length or 1))
            if denominator == 0:
                continue
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, doc_id: str, query_terms: List[str]) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        for term in query_terms:
            tf = self.term_freqs[term].get(doc_id, 0)
            if doc_length > 0:
                tf_norm = tf / doc_length
            else:
                tf_norm = 0.0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str]) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = []
        for i, token in enumerate(tokens):
            if token in query_terms:
                positions.append(i)
        if not positions:
            snippet = content[:160] + ("..." if len(content) > 160 else "")
            return snippet
        start = max(positions[0] - 10, 0)
        end = min(positions[0] + 30, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in query_terms:
            snippet = re.sub(r'\b(%s)\b' % re.escape(term), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + ("..." if end < len(tokens) else "")

# Singleton factory for SearchIndex
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            doc_id="E06-001",
            title="E06 Report Generator Overview",
            content="The E06 report generator provides automated synthesis of data into actionable reports. It supports custom templates, multi-source integration, and rapid deployment for enterprise analytics.",
            tags=["overview", "automation", "templates"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-002",
            title="Data Integration in E06",
            content="E06 engine integrates data from SQL, NoSQL, and API sources. It normalizes disparate datasets, applies schema mapping, and ensures consistency for reporting workflows.",
            tags=["data integration", "sql", "api", "schema"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-003",
            title="Custom Template Design",
            content="Templates in E06 allow users to define report layouts using Jinja2 syntax. Dynamic fields, conditional blocks, and reusable components streamline report customization.",
            tags=["templates", "jinja2", "customization"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-004",
            title="Automated Scheduling",
            content="E06 report generator supports cron-based scheduling. Reports can be generated at fixed intervals, with notification hooks for Slack, email, and webhooks.",
            tags=["scheduling", "cron", "notifications"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-005",
            title="Security and Access Control",
            content="E06 implements RBAC for report access. User roles, permissions, and audit logs ensure compliance and data privacy in enterprise environments.",
            tags=["security", "rbac", "audit"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-006",
            title="Multi-Source Data Aggregation",
            content="E06 can aggregate data from multiple sources, including CSV, Excel, REST APIs, and cloud databases. Aggregation logic is configurable via YAML files.",
            tags=["aggregation", "csv", "excel", "cloud"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-007",
            title="Report Export Formats",
            content="Reports generated by E06 can be exported as PDF, HTML, XLSX, and JSON. Export options include custom branding, watermarks, and encryption.",
            tags=["export", "pdf", "html", "xlsx", "json"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-008",
            title="Real-Time Analytics",
            content="E06 supports real-time data streaming for analytics dashboards. Kafka and MQTT connectors enable live updates and event-driven reporting.",
            tags=["analytics", "real-time", "kafka", "mqtt"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-009",
            title="API Reference",
            content="The E06 engine exposes a RESTful API for report generation, template management, and data ingestion. Endpoints are documented with OpenAPI specifications.",
            tags=["api", "rest", "openapi"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-010",
            title="User Authentication",
            content="E06 supports OAuth2 and SAML authentication. Single sign-on integration and session management are provided for secure access.",
            tags=["authentication", "oauth2", "saml", "sso"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-011",
            title="Error Handling and Logging",
            content="E06 features structured logging and error handling. Logs are available in JSON format, with support for log rotation and external monitoring.",
            tags=["logging", "error", "monitoring"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-012",
            title="Performance Optimization",
            content="E06 report generator is optimized for high throughput. Caching, parallel processing, and lazy evaluation improve performance for large datasets.",
            tags=["performance", "caching", "parallel"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-013",
            title="Deployment Strategies",
            content="E06 can be deployed on-premises, in Docker containers, or on cloud platforms such as AWS and Azure. Deployment scripts and Helm charts are available.",
            tags=["deployment", "docker", "cloud", "helm"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-014",
            title="Data Validation",
            content="E06 validates input data using schema definitions. Validation errors are reported with detailed messages, and custom validators can be registered.",
            tags=["validation", "schema", "custom"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-015",
            title="Report Versioning",
            content="E06 supports version control for report templates and generated reports. Git integration enables tracking changes and rollback.",
            tags=["versioning", "git", "rollback"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-016",
            title="Localization and Internationalization",
            content="E06 provides i18n support for multi-language reports. Locale settings, translation files, and Unicode handling are built-in.",
            tags=["localization", "i18n", "translation"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-017",
            title="Custom Scripting",
            content="E06 allows custom Python scripts for data transformation. Scripts are sandboxed, and execution limits are enforced for security.",
            tags=["scripting", "python", "transformation"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-018",
            title="Report Distribution",
            content="Reports can be distributed via email, FTP, or cloud storage. Distribution rules are configurable, and delivery logs are maintained.",
            tags=["distribution", "email", "ftp", "cloud"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-019",
            title="User Interface",
            content="E06 features a web-based UI for report management. Drag-and-drop template editing, preview, and dashboard widgets are included.",
            tags=["ui", "web", "dashboard"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-020",
            title="Data Transformation Pipelines",
            content="E06 supports ETL pipelines for data transformation. Pipelines can be defined in YAML, with support for mapping, filtering, and aggregation.",
            tags=["etl", "pipeline", "yaml", "mapping"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-021",
            title="Extensibility and Plugins",
            content="E06 architecture is extensible via plugins. Custom data sources, report formats, and analytics modules can be added.",
            tags=["extensibility", "plugins", "modules"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-022",
            title="Compliance and Auditing",
            content="E06 provides compliance features such as audit trails, GDPR support, and export controls. All report actions are logged for regulatory review.",
            tags=["compliance", "gdpr", "audit"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-023",
            title="Mobile Access",
            content="E06 reports can be accessed on mobile devices via responsive web interfaces and native apps. Push notifications are supported.",
            tags=["mobile", "responsive", "apps"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-024",
            title="Data Encryption",
            content="E06 encrypts sensitive data at rest and in transit. AES-256 and TLS are used for security, with key management integration.",
            tags=["encryption", "aes", "tls", "security"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-025",
            title="Report Customization API",
            content="E06 exposes APIs for customizing report generation. Users can define custom fields, filters, and aggregation logic programmatically.",
            tags=["api", "customization", "fields", "aggregation"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-026",
            title="Integration with BI Tools",
            content="E06 integrates with business intelligence tools such as Tableau, PowerBI, and Looker. Data connectors and export formats are provided.",
            tags=["bi", "tableau", "powerbi", "looker"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-027",
            title="Report Lifecycle Management",
            content="E06 manages report lifecycle from creation to archival. Lifecycle policies, retention rules, and automated cleanup are configurable.",
            tags=["lifecycle", "archival", "retention"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-028",
            title="Advanced Filtering",
            content="E06 supports advanced filtering with boolean logic, regex, and custom expressions. Filters can be applied at data source or report level.",
            tags=["filtering", "boolean", "regex", "expressions"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-029",
            title="Collaboration Features",
            content="E06 enables collaboration with shared reports, comments, and access control. Teams can work together on report design and review.",
            tags=["collaboration", "shared", "comments", "teams"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="E06-030",
            title="Report Quality Assurance",
            content="E06 includes QA tools for report validation, preview, and error detection. Automated tests and manual review workflows are supported.",
            tags=["qa", "validation", "preview", "error"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)