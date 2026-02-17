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
    def __init__(self, bm25_k1: float = 1.5, bm25_b: float = 0.75):
        self.bm25_k1 = bm25_k1
        self.bm25_b = bm25_b
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_doc_freqs: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.doc_lengths: Dict[str, int] = defaultdict(int)
        self.avg_doc_length: float = 0.0
        self.total_docs: int = 0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._recompute_stats = True

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.documents[doc.id] = doc
            term_counts = Counter(tokens)
            for term, count in term_counts.items():
                self.term_doc_freqs[term][doc.id] = count
                self.doc_freqs[term] += 1
            self.total_docs += 1
            self._recompute_stats = True

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        candidate_doc_ids = set()
        for token in query_tokens:
            if token in self.term_doc_freqs:
                candidate_doc_ids.update(self.term_doc_freqs[token].keys())
        scored_results = []
        for doc_id in candidate_doc_ids:
            bm25_score = self._score_bm25(doc_id, query_tokens)
            tfidf_score = self._score_tfidf(doc_id, query_tokens)
            doc = self.documents[doc_id]
            final_score = (bm25_score * 0.7 + tfidf_score * 0.3) * doc.weight
            snippet = self._make_snippet(doc.content, query_tokens)
            scored_results.append(SearchResult(doc_id, final_score, doc.title, snippet))
        scored_results.sort(key=lambda x: x.score, reverse=True)
        return scored_results[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            if self._recompute_stats:
                self._update_stats()
            return {
                "total_docs": self.total_docs,
                "avg_doc_length": self.avg_doc_length,
                "unique_terms": len(self.doc_freqs)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        with self.lock:
            if self._recompute_stats:
                self._update_stats()
            if term in self.idf_cache:
                return self.idf_cache[term]
            df = self.doc_freqs.get(term, 0)
            if df == 0:
                idf = 0.0
            else:
                idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
            self.idf_cache[term] = idf
            return idf

    def _update_stats(self):
        total_length = sum(self.doc_lengths.values())
        self.avg_doc_length = total_length / self.total_docs if self.total_docs > 0 else 0.0
        self.idf_cache.clear()
        self._recompute_stats = False

    def _score_bm25(self, doc_id: str, query_tokens: List[str]) -> float:
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in set(query_tokens):
            tf = self.term_doc_freqs.get(term, {}).get(doc_id, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            denom = tf + self.bm25_k1 * (1 - self.bm25_b + self.bm25_b * doc_len / (self.avg_doc_length or 1))
            numer = tf * (self.bm25_k1 + 1)
            score += idf * numer / denom
        return score

    def _score_tfidf(self, doc_id: str, query_tokens: List[str]) -> float:
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        tfidf = 0.0
        term_counts = Counter(self._tokenize(doc.content))
        for term in set(query_tokens):
            tf = term_counts.get(term, 0) / (doc_len or 1)
            idf = self._compute_idf(term)
            tfidf += tf * idf
        return tfidf

    def _make_snippet(self, content: str, query_tokens: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            return ' '.join(tokens[:window]) + ('...' if len(tokens) > window else '')
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        return snippet + ('...' if end < len(tokens) else '')

# Singleton search index
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
            "Mode Enforcement Rules",
            "All responses must adhere strictly to the currently enforced mode. No deviation is permitted except under emergency override conditions. Enforcement is logged for audit.",
            ["mode", "enforcement", "rules"],
            1.0
        ),
        SearchDocument(
            "2",
            "Mode Downgrade Triggers",
            "Triggers for mode downgrade include detection of regulatory risk, user request for lower sensitivity, or system-initiated fallback. All downgrades are logged.",
            ["mode", "downgrade", "triggers"],
            1.0
        ),
        SearchDocument(
            "3",
            "Mode Upgrade Requirements",
            "Upgrading mode requires validation of user credentials, regulatory compliance check, and explicit confirmation. Upgrade attempts are subject to logging.",
            ["mode", "upgrade", "requirements"],
            1.0
        ),
        SearchDocument(
            "4",
            "Clause Template Selection",
            "Clause templates are selected based on the response context, regulatory requirements, and enforced mode. Template selection logic must be transparent and auditable.",
            ["clause", "template", "selection"],
            1.0
        ),
        SearchDocument(
            "5",
            "Response Structure Enforcement",
            "Responses must follow the prescribed structure for the current mode, including required headers, body, and footers. Structure violations are flagged.",
            ["response", "structure", "enforcement"],
            1.0
        ),
        SearchDocument(
            "6",
            "Evidence Requirement Validation",
            "Each claim within a response must be supported by evidence. Evidence requirements are mode-dependent and validated before response finalization.",
            ["evidence", "requirement", "validation"],
            1.0
        ),
        SearchDocument(
            "7",
            "Citation Inclusion Rules",
            "Citations are mandatory for all factual statements. The citation format and inclusion rules are enforced per mode and regulatory requirements.",
            ["citation", "inclusion", "rules"],
            1.0
        ),
        SearchDocument(
            "8",
            "Confidence Threshold for Mode Selection",
            "A minimum confidence threshold must be met before a mode transition is permitted. Thresholds are configurable and logged.",
            ["confidence", "threshold", "mode", "selection"],
            1.0
        ),
        SearchDocument(
            "9",
            "Mode Transition Logging",
            "All mode transitions, including upgrades, downgrades, and overrides, are logged with timestamp, initiator, and justification for audit purposes.",
            ["mode", "transition", "logging"],
            1.0
        ),
        SearchDocument(
            "10",
            "Forbidden Mode Transitions",
            "Certain mode transitions are forbidden, such as direct downgrade from Mode 3 to Mode 1 without intermediate steps. Violations trigger alerts.",
            ["forbidden", "mode", "transitions"],
            1.0
        ),
        SearchDocument(
            "11",
            "Emergency Mode Override",
            "Emergency override allows bypassing standard mode enforcement under critical conditions. Overrides require dual authorization and are fully logged.",
            ["emergency", "mode", "override"],
            1.0
        ),
        SearchDocument(
            "12",
            "Clause Integrity Verification",
            "All clauses must be verified for integrity before inclusion in the response. Integrity checks include hash validation and template conformity.",
            ["clause", "integrity", "verification"],
            1.0
        ),
        SearchDocument(
            "13",
            "Response Boundary Enforcement",
            "Responses must not exceed defined boundaries for length, scope, or content. Boundary violations are blocked and reported.",
            ["response", "boundary", "enforcement"],
            1.0
        ),
        SearchDocument(
            "14",
            "Personality Clause Injection",
            "Personality clauses are injected based on the selected persona and enforced mode. Injection logic is governed by professional standards.",
            ["personality", "clause", "injection"],
            1.0
        ),
        SearchDocument(
            "15",
            "Professional Standards Enforcement",
            "All responses must comply with professional standards relevant to the domain and enforced mode. Non-compliance is flagged for review.",
            ["professional", "standards", "enforcement"],
            1.0
        ),
        SearchDocument(
            "16",
            "Disclaimer Clause Triggers",
            "Disclaimer clauses are triggered by specific content patterns or regulatory requirements. Triggers are mode-dependent and must be documented.",
            ["disclaimer", "clause", "triggers"],
            1.0
        ),
        SearchDocument(
            "17",
            "Disclosure Requirements",
            "Disclosure requirements are enforced based on the response context, user role, and regulatory mandates. All disclosures are logged.",
            ["disclosure", "requirements"],
            1.0
        ),
        SearchDocument(
            "18",
            "Regulatory Response Clauses",
            "Regulatory response clauses are selected and enforced according to jurisdiction, mode, and subject matter. Clause selection is auditable.",
            ["regulatory", "response", "clauses"],
            1.0
        ),
        SearchDocument(
            "19",
            "Audit-Ready Clause Formatting",
            "All clauses must be formatted for audit-readiness, including metadata, timestamps, and author identifiers. Formatting is enforced at response generation.",
            ["audit-ready", "clause", "formatting"],
            1.0
        ),
        SearchDocument(
            "20",
            "LLM Guardrails Mode 3",
            "Mode 3 applies the strictest guardrails, including mandatory citations, evidence validation, and audit logging. All responses are subject to review.",
            ["llm", "guardrails", "mode3"],
            1.0
        ),
        SearchDocument(
            "21",
            "User Role Validation",
            "User roles are validated before permitting mode transitions or access to sensitive clauses. Role validation is logged for compliance.",
            ["user", "role", "validation"],
            1.0
        ),
        SearchDocument(
            "22",
            "Template Version Control",
            "All clause templates are version-controlled. Updates require review and approval before deployment. Version history is maintained.",
            ["template", "version", "control"],
            1.0
        ),
        SearchDocument(
            "23",
            "Sensitive Data Handling",
            "Sensitive data is handled according to mode and regulatory requirements. Data access and transmission are logged and encrypted.",
            ["sensitive", "data", "handling"],
            1.0
        ),
        SearchDocument(
            "24",
            "Automated Clause Auditing",
            "Automated tools audit clause inclusion, formatting, and evidence compliance. Audit results are stored for regulatory review.",
            ["automated", "clause", "auditing"],
            1.0
        ),
        SearchDocument(
            "25",
            "Justification Requirement for Mode Changes",
            "All mode changes require a justification statement, which is logged and reviewed. Unjustified changes are blocked.",
            ["justification", "requirement", "mode", "changes"],
            1.0
        ),
        SearchDocument(
            "26",
            "Incident Response Mode Activation",
            "Incident response mode can be activated upon detection of a security or compliance incident. Activation is logged and triggers special clauses.",
            ["incident", "response", "mode", "activation"],
            1.0
        ),
        SearchDocument(
            "27",
            "Cross-Jurisdictional Clause Selection",
            "Clause selection must account for cross-jurisdictional regulatory requirements. Conflicts are resolved according to the strictest applicable rule.",
            ["cross-jurisdictional", "clause", "selection"],
            1.0
        ),
        SearchDocument(
            "28",
            "Response Time Logging",
            "Response times for clause selection and enforcement are logged for performance and compliance monitoring.",
            ["response", "time", "logging"],
            1.0
        ),
        SearchDocument(
            "29",
            "Manual Review Triggers",
            "Manual review is triggered by flagged responses, boundary violations, or override activations. Review outcomes are documented.",
            ["manual", "review", "triggers"],
            1.0
        ),
        SearchDocument(
            "30",
            "Mode Transition Notification",
            "Users and administrators are notified of all mode transitions, including the reason and effective time. Notifications are logged.",
            ["mode", "transition", "notification"],
            1.0
        ),
        SearchDocument(
            "31",
            "LLM Guardrails Mode 2",
            "Mode 2 applies moderate guardrails, balancing evidence requirements and flexibility. Some clauses are optional but logged.",
            ["llm", "guardrails", "mode2"],
            1.0
        ),
        SearchDocument(
            "32",
            "LLM Guardrails Mode 1",
            "Mode 1 applies minimal guardrails, prioritizing user flexibility. Evidence and citation requirements are relaxed.",
            ["llm", "guardrails", "mode1"],
            1.0
        ),
        SearchDocument(
            "33",
            "Clause Deletion Logging",
            "All clause deletions are logged with user, timestamp, and reason. Unauthorized deletions are blocked.",
            ["clause", "deletion", "logging"],
            1.0
        ),
        SearchDocument(
            "34",
            "Automated Mode Reversion",
            "The system can automatically revert to a safer mode upon detection of anomalies or compliance risks. Reversions are logged.",
            ["automated", "mode", "reversion"],
            1.0
        ),
        SearchDocument(
            "35",
            "Template Usage Analytics",
            "Analytics on clause template usage are collected for compliance and optimization. Usage trends are reviewed periodically.",
            ["template", "usage", "analytics"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)