import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# --- Data Classes ---

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

# --- Search Index ---

class SearchIndex:
    def __init__(self):
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.total_terms: int = 0
        self.lock = threading.Lock()
        self.avg_doc_length: float = 0.0
        self.k1 = 1.5
        self.b = 0.75
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[str, Dict[str, float]] = defaultdict(dict)
        self._tokenizer = re.compile(r"\b\w+\b")
        self._preseeded = False

    def _tokenize(self, text: str) -> List[str]:
        tokens = self._tokenizer.findall(text.lower())
        return tokens

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
                self.term_doc_freqs[term] += 1
            self._idf_cache.clear()
            self._tfidf_cache.clear()
            self.avg_doc_length = (
                sum(self.doc_lengths.values()) / len(self.doc_lengths) if self.doc_lengths else 0.0
            )

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        N = len(self.documents)
        df = self.term_doc_freqs.get(term, 0)
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: str) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        doc = self.documents[doc_id]
        for term in query_terms:
            tf = self.term_freqs.get(term, {}).get(doc_id, 0)
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_length / (self.avg_doc_length or 1))
            bm25 = idf * (numerator / (denominator or 1))
            score += bm25
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: str) -> float:
        doc = self.documents[doc_id]
        doc_tokens = self._tokenize(doc.content)
        doc_length = len(doc_tokens)
        term_counts = Counter(doc_tokens)
        score = 0.0
        for term in query_terms:
            tf = term_counts.get(term, 0) / (doc_length or 1)
            idf = self._compute_idf(term)
            score += tf * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.term_freqs.get(term, {}).keys())
        scored_docs = []
        for doc_id in candidate_docs:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                doc = self.documents[doc_id]
                snippet = self._make_snippet(doc.content, query_terms)
                scored_docs.append(SearchResult(doc_id, score, doc.title, snippet))
        scored_docs.sort(key=lambda r: r.score, reverse=True)
        return scored_docs[:limit]

    def _make_snippet(self, content: str, query_terms: List[str], snippet_len: int = 160) -> str:
        tokens = self._tokenize(content)
        indices = [i for i, t in enumerate(tokens) if t in query_terms]
        if not indices:
            return content[:snippet_len] + ("..." if len(content) > snippet_len else "")
        start = max(0, indices[0] - 10)
        end = min(len(tokens), indices[0] + 20)
        snippet = " ".join(tokens[start:end])
        return snippet[:snippet_len] + ("..." if len(snippet) > snippet_len else "")

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            stats = {
                "num_documents": len(self.documents),
                "avg_doc_length": self.avg_doc_length,
                "num_terms": len(self.term_doc_freqs),
                "total_terms": self.total_terms,
            }
            return stats

    def _preseed_documents(self):
        if self._preseeded:
            return
        docs = [
            SearchDocument(
                "1", "Voice Transcript Audit Logging",
                "Audit logs for voice transcripts must capture all transcript modifications, access events, and reviewer actions. The audit trail must be immutable and exportable for regulatory review.",
                ["audit", "logging", "voice", "transcript"], 1.0
            ),
            SearchDocument(
                "2", "PII Detection in Voice Transcripts",
                "Automated detection of personally identifiable information (PII) in voice transcripts is required. Detected PII must be flagged and redacted according to compliance rules.",
                ["PII", "detection", "redaction", "compliance"], 1.0
            ),
            SearchDocument(
                "3", "Transcript-to-Evidence Binding",
                "Each voice transcript must be cryptographically bound to its corresponding evidence file, ensuring chain of custody and preventing tampering.",
                ["evidence", "binding", "chain of custody", "tampering"], 1.0
            ),
            SearchDocument(
                "4", "Audit Trail Format for Voice",
                "Audit trails for voice transcripts must follow a standardized format, including timestamps, user IDs, and action types. Format must be compatible with regulatory export requirements.",
                ["audit", "trail", "format", "regulatory"], 1.0
            ),
            SearchDocument(
                "5", "Voice Authentication Verification",
                "Voice authentication events must be logged and verified. Authentication failures must trigger incident response procedures and be included in audit logs.",
                ["authentication", "verification", "incident response"], 1.0
            ),
            SearchDocument(
                "6", "Speaker Verification Logging",
                "Speaker verification results, including confidence scores and verification failures, must be logged for each voice session.",
                ["speaker", "verification", "logging"], 1.0
            ),
            SearchDocument(
                "7", "Conversation Recording Consent",
                "Consent for recording conversations must be obtained and logged. Consent logs must be retrievable and auditable.",
                ["consent", "recording", "logging", "audit"], 1.0
            ),
            SearchDocument(
                "8", "Retention Policy Enforcement",
                "Voice transcript retention policies must be enforced automatically. Expired transcripts must be deleted or archived according to policy.",
                ["retention", "policy", "enforcement", "deletion"], 1.0
            ),
            SearchDocument(
                "9", "Voice Data Encryption Requirements",
                "All voice transcript data must be encrypted at rest and in transit using industry-standard algorithms. Encryption keys must be managed securely.",
                ["encryption", "voice", "transcript", "security"], 1.0
            ),
            SearchDocument(
                "10", "HIPAA Compliance for Voice Transcripts",
                "Voice transcripts containing protected health information (PHI) must comply with HIPAA regulations. Access controls and audit logging are mandatory.",
                ["HIPAA", "compliance", "PHI", "audit"], 1.0
            ),
            SearchDocument(
                "11", "Attorney-Client Privilege Detection",
                "Voice transcripts must be analyzed for attorney-client privileged content. Privileged segments must be flagged and access restricted.",
                ["attorney-client", "privilege", "detection", "restriction"], 1.0
            ),
            SearchDocument(
                "12", "Work Product Doctrine for Voice Transcripts",
                "Voice transcripts may contain attorney work product. Such content must be identified and protected from disclosure.",
                ["work product", "doctrine", "protection"], 1.0
            ),
            SearchDocument(
                "13", "Voice Evidence Chain of Custody",
                "Chain of custody for voice evidence must be maintained, including timestamps, handlers, and transfer logs.",
                ["chain of custody", "voice", "evidence", "logging"], 1.0
            ),
            SearchDocument(
                "14", "Transcript Accuracy Verification",
                "Accuracy of voice transcripts must be verified against original recordings. Verification logs must be maintained.",
                ["accuracy", "verification", "transcript"], 1.0
            ),
            SearchDocument(
                "15", "Redaction Rules for Sensitive Voice Data",
                "Sensitive information in voice transcripts must be redacted according to predefined rules. Redaction events must be logged.",
                ["redaction", "sensitive", "voice", "logging"], 1.0
            ),
            SearchDocument(
                "16", "Voice Data Access Control",
                "Access to voice transcript data must be controlled via role-based permissions. Access events must be logged and reviewed.",
                ["access control", "voice", "transcript", "logging"], 1.0
            ),
            SearchDocument(
                "17", "Voice Session Integrity",
                "Integrity of voice transcript sessions must be ensured via cryptographic checksums and session logs.",
                ["integrity", "session", "voice", "checksum"], 1.0
            ),
            SearchDocument(
                "18", "Tampering Detection in Voice Transcripts",
                "Tampering attempts in voice transcripts must be detected using hash comparisons and anomaly detection algorithms.",
                ["tampering", "detection", "voice", "hash"], 1.0
            ),
            SearchDocument(
                "19", "Voice Audit Report Generation",
                "Audit reports for voice transcript systems must be generated automatically, including compliance status and exception logs.",
                ["audit", "report", "generation", "compliance"], 1.0
            ),
            SearchDocument(
                "20", "Regulatory Compliance Checking",
                "Voice transcript systems must check for regulatory compliance on a scheduled basis. Non-compliance events must be logged and reported.",
                ["regulatory", "compliance", "checking", "logging"], 1.0
            ),
            SearchDocument(
                "21", "Voice Transcript Metadata Completeness",
                "Metadata for voice transcripts must be complete, including speaker IDs, timestamps, and session IDs. Incomplete metadata must trigger alerts.",
                ["metadata", "completeness", "voice", "transcript"], 1.0
            ),
            SearchDocument(
                "22", "Voice Transcript Exportability",
                "Voice transcripts and their audit trails must be exportable in standardized formats for regulatory review.",
                ["exportability", "audit", "trail", "regulatory"], 1.0
            ),
            SearchDocument(
                "23", "Voice Transcript Session Termination Logging",
                "Session termination events for voice transcripts must be logged, including reason for termination and user ID.",
                ["session", "termination", "logging", "voice"], 1.0
            ),
            SearchDocument(
                "24", "Voice Transcript Reviewer Accountability",
                "Actions by reviewers of voice transcripts must be logged. Reviewer accountability must be enforced via audit trails.",
                ["reviewer", "accountability", "audit", "logging"], 1.0
            ),
            SearchDocument(
                "25", "Voice Transcript Compliance Exception Handling",
                "Compliance exceptions in voice transcript systems must be handled according to regulatory requirements. Exception logs must be maintained.",
                ["compliance", "exception", "handling", "logging"], 1.0
            ),
            SearchDocument(
                "26", "Voice Transcript Regulatory Notification Logging",
                "Regulatory notifications related to voice transcripts must be logged and retrievable for audit purposes.",
                ["regulatory", "notification", "logging", "audit"], 1.0
            ),
            SearchDocument(
                "27", "Voice Transcript Compliance Training Logging",
                "Compliance training events for voice transcript system users must be logged and auditable.",
                ["compliance", "training", "logging", "audit"], 1.0
            ),
            SearchDocument(
                "28", "Voice Transcript System Configuration Logging",
                "System configuration changes affecting voice transcript processing must be logged, including user ID and timestamp.",
                ["system", "configuration", "logging", "voice"], 1.0
            ),
            SearchDocument(
                "29", "Voice Transcript Incident Response Logging",
                "Incident response events related to voice transcript systems must be logged and reviewed for compliance.",
                ["incident response", "logging", "compliance", "voice"], 1.0
            ),
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
            idx._preseed_documents()
            _search_index_instance = idx
        return _search_index_instance