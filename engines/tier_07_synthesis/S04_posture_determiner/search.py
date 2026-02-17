import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

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
        self.doc_tags: Dict[int, set] = defaultdict(set)
        self.total_docs: int = 0
        self.avg_doc_length: float = 0.0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.term_freqs[doc.id] = Counter(tokens)
            for term in self.term_freqs[doc.id]:
                self.term_doc_freqs[term][doc.id] = self.term_freqs[doc.id][term]
            self.doc_tags[doc.id] = set(doc.tags)
            self.total_docs += 1
            self._recompute_avg_doc_length()
            self._idf_cache.clear()

    def _recompute_avg_doc_length(self):
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
        df = len(self.term_doc_freqs.get(term, {}))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        doc = self.documents[doc_id]
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0)
            idf = self._compute_idf(term)
            numerator = tf * (self._bm25_k1 + 1)
            denominator = tf + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_length / (self.avg_doc_length or 1))
            score += idf * (numerator / (denominator or 1))
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_length = self.doc_lengths.get(doc_id, 1)
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0) / doc_length
            idf = self._compute_idf(term)
            score += tf * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_doc_ids = set()
        for term in query_terms:
            candidate_doc_ids.update(self.term_doc_freqs.get(term, {}).keys())
        scored_docs = []
        for doc_id in candidate_doc_ids:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                snippet = self._make_snippet(self.documents[doc_id], query_terms)
                scored_docs.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scored_docs.sort(key=lambda r: r.score, reverse=True)
        return scored_docs[:limit]

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str]) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:160] + ('...' if len(content) > 160 else '')
        start = max(positions[0] - 10, 0)
        end = min(positions[0] + 20, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in query_terms:
            snippet = re.sub(r'\b({})\b'.format(re.escape(term)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet[:160] + ('...' if len(snippet) > 160 else '')

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_documents': self.total_docs,
            'average_document_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freqs),
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
        SearchDocument(1, "PROCEED Criteria Definition",
            "Defines the criteria for proceeding with risk posture determination, including baseline requirements, minimum data sufficiency, and risk tolerance calibration.",
            ["criteria", "proceed", "definition", "baseline"], 1.0),
        SearchDocument(2, "CONDITIONAL Criteria and Mitigable Risks",
            "Outlines conditional criteria for posture assignment, identifies mitigable risks, and specifies escalation triggers for conditional clearance.",
            ["conditional", "criteria", "mitigable", "risks"], 1.0),
        SearchDocument(3, "BLOCKED Criteria for Unresolvable Issues",
            "Specifies blocked criteria for cases where risk cannot be mitigated, including defect classification and mandatory review triggers.",
            ["blocked", "criteria", "unresolvable", "defect"], 1.0),
        SearchDocument(4, "REVIEW Criteria Requiring Human Judgment",
            "Enumerates criteria that necessitate human review, such as ambiguous risk signals, jurisdictional conflicts, or confidence floor breaches.",
            ["review", "criteria", "human", "judgment"], 1.0),
        SearchDocument(5, "Risk Threshold Calibration",
            "Describes calibration of risk thresholds based on client profiles, jurisdictional requirements, and posture matrix scoring.",
            ["risk", "threshold", "calibration", "profiles"], 1.0),
        SearchDocument(6, "Posture Escalation Rules",
            "Details rules for escalating posture based on risk signals, temporal decay, and override protocols.",
            ["posture", "escalation", "rules", "override"], 1.0),
        SearchDocument(7, "Multi-Factor Posture Matrix",
            "Defines the multi-factor matrix for posture assignment, including weighted scoring of risk factors and mandatory review triggers.",
            ["multi-factor", "matrix", "posture", "scoring"], 1.0),
        SearchDocument(8, "Confidence Floor Requirements",
            "Specifies minimum confidence floor for automated posture assignment, and triggers for manual review when confidence is insufficient.",
            ["confidence", "floor", "requirements", "review"], 1.0),
        SearchDocument(9, "Mandatory Review Triggers",
            "Lists triggers for mandatory review, including blocked criteria, override requests, and jurisdictional exceptions.",
            ["mandatory", "review", "triggers", "exceptions"], 1.0),
        SearchDocument(10, "Override Protocols",
            "Describes protocols for overriding automated posture assignments, including justification templates and audit requirements.",
            ["override", "protocols", "justification", "audit"], 1.0),
        SearchDocument(11, "Posture Justification Templates",
            "Provides templates for documenting posture assignment justifications, including risk factor analysis and client tolerance alignment.",
            ["posture", "justification", "templates", "analysis"], 1.0),
        SearchDocument(12, "Client Risk Tolerance Profiles",
            "Defines client-specific risk tolerance profiles, including calibration methodology and jurisdiction-specific adjustments.",
            ["client", "risk", "tolerance", "profiles"], 1.0),
        SearchDocument(13, "Jurisdiction-Specific Thresholds",
            "Outlines jurisdiction-specific risk thresholds and posture assignment rules, including compliance requirements.",
            ["jurisdiction", "thresholds", "compliance", "assignment"], 1.0),
        SearchDocument(14, "Temporal Posture Decay",
            "Describes temporal decay rules for posture assignment, including risk re-evaluation intervals and decay triggers.",
            ["temporal", "posture", "decay", "intervals"], 1.0),
        SearchDocument(15, "Posture Audit Requirements",
            "Specifies audit requirements for posture assignment, including documentation, review logs, and exception handling.",
            ["posture", "audit", "requirements", "logs"], 1.0),
        SearchDocument(16, "Posture Appeal Process",
            "Details the process for appealing posture assignments, including submission protocols, review priority scoring, and escalation paths.",
            ["posture", "appeal", "process", "priority"], 1.0),
        SearchDocument(17, "Conditional Clearance Requirements",
            "Defines requirements for conditional clearance, including mitigable risk identification and review triggers.",
            ["conditional", "clearance", "requirements", "mitigable"], 1.0),
        SearchDocument(18, "Blocking Defect Classification",
            "Classifies blocking defects that prevent posture assignment, including unresolvable issues and mandatory review triggers.",
            ["blocking", "defect", "classification", "review"], 1.0),
        SearchDocument(19, "Review Priority Scoring",
            "Outlines scoring methodology for prioritizing reviews, including risk severity, client tolerance, and jurisdictional factors.",
            ["review", "priority", "scoring", "severity"], 1.0),
        SearchDocument(20, "Posture Notification Rules",
            "Specifies rules for notifying stakeholders of posture assignment, including escalation triggers and audit requirements.",
            ["posture", "notification", "rules", "stakeholders"], 1.0),
        SearchDocument(21, "Risk Signal Aggregation",
            "Describes aggregation of risk signals for posture determination, including multi-factor weighting and signal normalization.",
            ["risk", "signal", "aggregation", "weighting"], 1.0),
        SearchDocument(22, "Posture Assignment Workflow",
            "Details the workflow for posture assignment, including automated scoring, manual review, and override handling.",
            ["posture", "assignment", "workflow", "scoring"], 1.0),
        SearchDocument(23, "Mitigable Risk Identification",
            "Defines methodology for identifying mitigable risks and conditional clearance requirements.",
            ["mitigable", "risk", "identification", "clearance"], 1.0),
        SearchDocument(24, "Confidence Calibration",
            "Describes calibration of confidence scores for posture assignment, including minimum floor requirements and review triggers.",
            ["confidence", "calibration", "floor", "review"], 1.0),
        SearchDocument(25, "Jurisdictional Exception Handling",
            "Outlines handling of jurisdictional exceptions in posture assignment, including mandatory review triggers and escalation protocols.",
            ["jurisdictional", "exception", "handling", "escalation"], 1.0),
        SearchDocument(26, "Risk Tolerance Escalation",
            "Specifies escalation rules based on client risk tolerance profiles and jurisdiction-specific thresholds.",
            ["risk", "tolerance", "escalation", "thresholds"], 1.0),
        SearchDocument(27, "Posture Documentation Standards",
            "Defines standards for documenting posture assignments, including audit requirements and justification templates.",
            ["posture", "documentation", "standards", "audit"], 1.0),
        SearchDocument(28, "Review Queue Management",
            "Describes management of review queues, including priority scoring and mandatory review triggers.",
            ["review", "queue", "management", "priority"], 1.0),
        SearchDocument(29, "Override Request Workflow",
            "Details workflow for submitting override requests, including justification templates and audit requirements.",
            ["override", "request", "workflow", "justification"], 1.0),
        SearchDocument(30, "Temporal Decay Triggers",
            "Specifies triggers for temporal decay in posture assignment, including risk re-evaluation intervals and escalation rules.",
            ["temporal", "decay", "triggers", "escalation"], 1.0),
    ]
    for doc in docs:
        index.add_document(doc)