import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Optional, Tuple

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
        self.inverted_index: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.doc_tag_index: Dict[str, List[str]] = defaultdict(list)
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.RLock()
        self.k1 = 1.5
        self.b = 0.75

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.title + ' ' + doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.avg_doc_length = (
                sum(self.doc_lengths.values()) / len(self.doc_lengths)
                if self.doc_lengths else 0.0
            )
            term_counts = Counter(tokens)
            for term, freq in term_counts.items():
                self.inverted_index[term][doc.id] = freq
                self.term_doc_freq[term] += 1
            self.doc_tag_index[doc.id] = doc.tags
            self.idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        with self.lock:
            if term in self.idf_cache:
                return self.idf_cache[term]
            N = len(self.documents)
            df = self.term_doc_freq.get(term, 0)
            idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
            self.idf_cache[term] = idf
            return idf

    def _score_bm25(self, query_terms: List[str], doc_id: str) -> float:
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            freq = self.inverted_index.get(term, {}).get(doc_id, 0)
            if freq == 0:
                continue
            idf = self._compute_idf(term)
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (1 - self.b + self.b * doc_len / (self.avg_doc_length or 1))
            score += idf * (numerator / (denominator or 1))
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: str) -> float:
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        term_counts = self.inverted_index
        for term in query_terms:
            tf = term_counts.get(term, {}).get(doc_id, 0) / (doc_len or 1)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            score += tf * idf
        return score * doc.weight

    def _snippet(self, doc: SearchDocument, query_terms: List[str], max_length: int = 160) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:max_length]
        else:
            start = max(positions[0] - 10, 0)
            end = min(positions[0] + 10, len(tokens))
            snippet_tokens = tokens[start:end]
            snippet = ' '.join(snippet_tokens)
            if len(snippet) > max_length:
                snippet = snippet[:max_length] + '...'
        for term in query_terms:
            snippet = re.sub(r'\b({})\b'.format(re.escape(term)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet

    def search(self, query: str, limit: int = 10, method: str = 'bm25') -> List[SearchResult]:
        with self.lock:
            query_terms = self._tokenize(query)
            candidate_docs = set()
            for term in query_terms:
                candidate_docs.update(self.inverted_index.get(term, {}).keys())
            scored_docs: List[Tuple[str, float]] = []
            for doc_id in candidate_docs:
                if method == 'bm25':
                    score = self._score_bm25(query_terms, doc_id)
                elif method == 'tfidf':
                    score = self._score_tfidf(query_terms, doc_id)
                else:
                    score = self._score_bm25(query_terms, doc_id)
                if score > 0:
                    scored_docs.append((doc_id, score))
            scored_docs.sort(key=lambda x: x[1], reverse=True)
            results = []
            for doc_id, score in scored_docs[:limit]:
                doc = self.documents[doc_id]
                snippet = self._snippet(doc, query_terms)
                results.append(SearchResult(doc_id, score, doc.title, snippet))
            return results

    def get_stats(self) -> Dict[str, int]:
        with self.lock:
            return {
                'documents': len(self.documents),
                'unique_terms': len(self.inverted_index),
                'avg_doc_length': int(self.avg_doc_length),
                'tags_indexed': sum(len(tags) for tags in self.doc_tag_index.values()),
            }

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
            "1",
            "Tenant Isolation Enforcement Strategies",
            "Explore robust approaches to enforce tenant isolation in multi-tenancy architectures, including network segmentation, access control lists, and containerization.",
            ["tenant", "isolation", "architecture", "security"],
            1.0
        ),
        SearchDocument(
            "2",
            "Tenant-Specific Configuration Management",
            "Learn how to implement tenant-specific configuration using dynamic config stores, feature toggles, and per-tenant secrets management.",
            ["configuration", "tenant", "feature-flags", "secrets"],
            1.0
        ),
        SearchDocument(
            "3",
            "Resource Quota Management for Tenants",
            "Understand quota enforcement mechanisms such as rate limiting, resource pools, and hierarchical quota policies for multi-tenant systems.",
            ["quota", "resource", "management", "rate-limiting"],
            1.0
        ),
        SearchDocument(
            "4",
            "Per-Tenant Rate Limiting Patterns",
            "Discover scalable rate limiting techniques including token buckets, leaky buckets, and distributed counters tailored for tenant isolation.",
            ["rate-limiting", "tenant", "scalability", "patterns"],
            1.0
        ),
        SearchDocument(
            "5",
            "Tenant Onboarding Workflow Automation",
            "Automate tenant onboarding with workflow engines, self-service portals, and API-driven provisioning for seamless integration.",
            ["onboarding", "workflow", "automation", "provisioning"],
            1.0
        ),
        SearchDocument(
            "6",
            "Tenant Data Segregation Techniques",
            "Implement data segregation using schema-per-tenant, row-level security, and encrypted storage to prevent cross-tenant data leakage.",
            ["data", "segregation", "security", "tenant"],
            1.0
        ),
        SearchDocument(
            "7",
            "Cross-Tenant Query Prevention",
            "Prevent cross-tenant queries with query rewriting, access policies, and database-level guards to ensure strict data boundaries.",
            ["query", "prevention", "cross-tenant", "database"],
            1.0
        ),
        SearchDocument(
            "8",
            "Tenant Feature Flags and Dynamic Enablement",
            "Use feature flags to enable or disable features per tenant, supporting gradual rollouts and A/B testing in SaaS platforms.",
            ["feature-flags", "tenant", "rollout", "testing"],
            1.0
        ),
        SearchDocument(
            "9",
            "Tenant Billing and Metering Systems",
            "Design billing metering systems that track per-tenant usage, integrate with payment gateways, and support flexible pricing models.",
            ["billing", "metering", "tenant", "pricing"],
            1.0
        ),
        SearchDocument(
            "10",
            "Multi-Tenancy Architecture Patterns",
            "Compare shared schema, schema-per-tenant, and hybrid patterns for scalable multi-tenancy in cloud-native applications.",
            ["architecture", "multi-tenancy", "patterns", "cloud"],
            1.0
        ),
        SearchDocument(
            "11",
            "Tenant Lifecycle Management",
            "Manage tenant lifecycle events including onboarding, suspension, deletion, and migration with audit trails and compliance checks.",
            ["lifecycle", "management", "tenant", "audit"],
            1.0
        ),
        SearchDocument(
            "12",
            "Tenant Access Control Models",
            "Implement RBAC, ABAC, and custom access control models to enforce tenant-specific permissions and roles.",
            ["access-control", "rbac", "abac", "tenant"],
            1.0
        ),
        SearchDocument(
            "13",
            "Tenant API Throttling and Limits",
            "Apply API throttling strategies per tenant using distributed rate limiters and adaptive thresholds.",
            ["api", "throttling", "limits", "tenant"],
            1.0
        ),
        SearchDocument(
            "14",
            "Tenant Monitoring and Observability",
            "Monitor tenant activity with per-tenant metrics, logs, and distributed tracing for operational insight.",
            ["monitoring", "observability", "tenant", "metrics"],
            1.0
        ),
        SearchDocument(
            "15",
            "Tenant Customization and Branding",
            "Support tenant customization with branding, themes, and personalized dashboards in SaaS platforms.",
            ["customization", "branding", "tenant", "saas"],
            1.0
        ),
        SearchDocument(
            "16",
            "Tenant Security Best Practices",
            "Adopt best practices for tenant security including encryption, secure authentication, and vulnerability scanning.",
            ["security", "best-practices", "tenant", "encryption"],
            1.0
        ),
        SearchDocument(
            "17",
            "Tenant Migration Strategies",
            "Plan and execute tenant migrations with minimal downtime, data integrity, and compliance assurance.",
            ["migration", "tenant", "data", "compliance"],
            1.0
        ),
        SearchDocument(
            "18",
            "Tenant Audit Logging",
            "Enable audit logging per tenant to track access, changes, and compliance events for regulatory requirements.",
            ["audit", "logging", "tenant", "compliance"],
            1.0
        ),
        SearchDocument(
            "19",
            "Tenant Scalability and Elasticity",
            "Architect for tenant scalability with elastic resource allocation, auto-scaling, and horizontal partitioning.",
            ["scalability", "elasticity", "tenant", "partitioning"],
            1.0
        ),
        SearchDocument(
            "20",
            "Tenant Disaster Recovery Planning",
            "Develop disaster recovery plans for tenants including backup, restore, and failover procedures.",
            ["disaster-recovery", "backup", "restore", "tenant"],
            1.0
        ),
        SearchDocument(
            "21",
            "Tenant Compliance and Regulatory Controls",
            "Implement compliance controls for tenants such as GDPR, HIPAA, and PCI DSS in multi-tenant environments.",
            ["compliance", "regulatory", "tenant", "controls"],
            1.0
        ),
        SearchDocument(
            "22",
            "Tenant Performance Optimization",
            "Optimize performance for tenants with caching, query tuning, and load balancing strategies.",
            ["performance", "optimization", "tenant", "caching"],
            1.0
        ),
        SearchDocument(
            "23",
            "Tenant Notification Systems",
            "Build notification systems with per-tenant channels, preferences, and delivery guarantees.",
            ["notification", "systems", "tenant", "preferences"],
            1.0
        ),
        SearchDocument(
            "24",
            "Tenant Support and SLA Management",
            "Manage tenant support tickets, SLAs, and escalation workflows for customer satisfaction.",
            ["support", "sla", "tenant", "workflow"],
            1.0
        ),
        SearchDocument(
            "25",
            "Tenant API Gateway Design",
            "Design API gateways with tenant-aware routing, authentication, and request filtering.",
            ["api-gateway", "routing", "authentication", "tenant"],
            1.0
        ),
        SearchDocument(
            "26",
            "Tenant Analytics and Reporting",
            "Provide analytics and reporting per tenant with data visualization and export capabilities.",
            ["analytics", "reporting", "tenant", "visualization"],
            1.0
        ),
        SearchDocument(
            "27",
            "Tenant Session Management",
            "Implement secure session management for tenants including session isolation and expiration policies.",
            ["session", "management", "tenant", "security"],
            1.0
        ),
        SearchDocument(
            "28",
            "Tenant API Versioning",
            "Support API versioning per tenant to enable backward compatibility and phased feature rollouts.",
            ["api", "versioning", "tenant", "compatibility"],
            1.0
        ),
        SearchDocument(
            "29",
            "Tenant Resource Tagging",
            "Tag resources per tenant for billing, monitoring, and access control in cloud environments.",
            ["resource", "tagging", "tenant", "cloud"],
            1.0
        ),
        SearchDocument(
            "30",
            "Tenant Health Checks",
            "Perform health checks per tenant to ensure uptime, detect issues, and trigger automated remediation.",
            ["health-checks", "uptime", "tenant", "remediation"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)