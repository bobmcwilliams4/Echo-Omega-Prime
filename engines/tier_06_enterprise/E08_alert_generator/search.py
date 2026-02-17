import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# -----------------------------
# Data Classes
# -----------------------------

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

# -----------------------------
# Search Index
# -----------------------------

class SearchIndex:
    def __init__(self):
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_tokens: Dict[str, List[str]] = {}
        self.inverted_index: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.RLock()
        self._dirty = True

    def add_document(self, doc: SearchDocument):
        with self.lock:
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.title + ' ' + doc.content + ' ' + ' '.join(doc.tags))
            self.doc_tokens[doc.id] = tokens
            self.doc_lengths[doc.id] = len(tokens)
            token_counts = Counter(tokens)
            for token, count in token_counts.items():
                self.inverted_index[token][doc.id] = count
            self.N = len(self.documents)
            self._dirty = True

    def _update_stats(self):
        if not self._dirty:
            return
        with self.lock:
            total_length = sum(self.doc_lengths.values())
            self.avg_doc_length = total_length / self.N if self.N > 0 else 0.0
            self.idf_cache.clear()
            for token in self.inverted_index:
                self.idf_cache[token] = self._compute_idf(token)
            self._dirty = False

    def _tokenize(self, text: str) -> List[str]:
        # Lowercase, remove non-alphanumeric, split on whitespace
        tokens = re.findall(r'\b[a-z0-9]+\b', text.lower())
        return tokens

    def _compute_idf(self, term: str) -> float:
        df = len(self.inverted_index.get(term, {}))
        if df == 0:
            return 0.0
        return math.log(1 + (self.N - df + 0.5) / (df + 0.5))

    def _score_bm25(self, query_tokens: List[str], doc_id: str, k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        if doc_len == 0:
            return 0.0
        doc = self.documents[doc_id]
        for term in query_tokens:
            tf = self.inverted_index.get(term, {}).get(doc_id, 0)
            if tf == 0:
                continue
            idf = self.idf_cache.get(term, self._compute_idf(term))
            denom = tf + k1 * (1 - b + b * doc_len / (self.avg_doc_length + 1e-9))
            score += idf * ((tf * (k1 + 1)) / (denom + 1e-9))
        return score * doc.weight

    def _score_tfidf(self, query_tokens: List[str], doc_id: str) -> float:
        tfidf = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        if doc_len == 0:
            return 0.0
        doc = self.documents[doc_id]
        tf_counts = self.inverted_index
        for term in query_tokens:
            tf = tf_counts.get(term, {}).get(doc_id, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_len
            idf = self.idf_cache.get(term, self._compute_idf(term))
            tfidf += tf_norm * idf
        return tfidf * doc.weight

    def search(self, query: str, limit: int = 10, use_bm25: bool = True) -> List[SearchResult]:
        self._update_stats()
        query_tokens = self._tokenize(query)
        candidate_docs = set()
        for term in query_tokens:
            candidate_docs.update(self.inverted_index.get(term, {}).keys())
        scored = []
        for doc_id in candidate_docs:
            if use_bm25:
                score = self._score_bm25(query_tokens, doc_id)
            else:
                score = self._score_tfidf(query_tokens, doc_id)
            if score > 0.0:
                scored.append((score, doc_id))
        top = heapq.nlargest(limit, scored)
        results = []
        for score, doc_id in top:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], maxlen: int = 160) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            snippet = content[:maxlen]
            if len(content) > maxlen:
                snippet += '...'
            return snippet
        start = max(positions[0] - 5, 0)
        end = min(positions[0] + 10, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        if len(snippet) > maxlen:
            snippet = snippet[:maxlen] + '...'
        return snippet

    def get_stats(self) -> Dict[str, float]:
        self._update_stats()
        return {
            'num_documents': self.N,
            'avg_doc_length': self.avg_doc_length,
            'vocab_size': len(self.inverted_index)
        }

# -----------------------------
# Singleton Factory
# -----------------------------

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

# -----------------------------
# Pre-seed Domain Documents
# -----------------------------

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            id="1",
            title="New Filing Detected for Lease 101",
            content="A new filing has been detected for Lease 101 in the RRC system. Review the filing for compliance and possible ownership changes.",
            tags=["new filing", "lease", "rrc"],
            weight=1.0
        ),
        SearchDocument(
            id="2",
            title="Ownership Transfer: Lease 202",
            content="Ownership transfer recorded for Lease 202. The new operator is Midland Oil LLC. Update division orders and notify stakeholders.",
            tags=["ownership transfer", "lease", "operator change"],
            weight=1.1
        ),
        SearchDocument(
            id="3",
            title="Lease Expiration Warning: Lease 303",
            content="Lease 303 is set to expire in 60 days. Review extension options and notify lessee.",
            tags=["lease expiration", "warning"],
            weight=1.2
        ),
        SearchDocument(
            id="4",
            title="Lease Extension Deadline Approaching",
            content="The deadline for lease extension on Lease 404 is 2024-09-30. Ensure all paperwork is filed.",
            tags=["lease extension", "deadline"],
            weight=1.1
        ),
        SearchDocument(
            id="5",
            title="Drilling Permit Issued: Well 505",
            content="A drilling permit has been issued for Well 505. Operator: Eagle Drilling Inc. Review permit details and compliance requirements.",
            tags=["drilling permit", "well", "permit issued"],
            weight=1.0
        ),
        SearchDocument(
            id="6",
            title="Permit Expiration Warning: Well 606",
            content="Drilling permit for Well 606 will expire in 30 days. Action required to maintain permit validity.",
            tags=["permit expiration", "well", "warning"],
            weight=1.1
        ),
        SearchDocument(
            id="7",
            title="RRC Violation Detected: Lease 707",
            content="A violation has been detected by the Railroad Commission for Lease 707. Review violation notice and prepare response.",
            tags=["rrc violation", "lease", "compliance"],
            weight=1.3
        ),
        SearchDocument(
            id="8",
            title="Production Change Detected: Well 808",
            content="Significant production change detected for Well 808. Investigate cause and update production forecasts.",
            tags=["production change", "well", "alert"],
            weight=1.2
        ),
        SearchDocument(
            id="9",
            title="Operator Change Detected: Lease 909",
            content="Operator change recorded for Lease 909. New operator: Lone Star Energy. Update records accordingly.",
            tags=["operator change", "lease"],
            weight=1.1
        ),
        SearchDocument(
            id="10",
            title="Lien Filed: Lease 1010",
            content="A lien has been filed against Lease 1010. Review lien details and determine impact on title.",
            tags=["lien filed", "lease", "title defect"],
            weight=1.3
        ),
        SearchDocument(
            id="11",
            title="Lien Release: Lease 1111",
            content="Lien on Lease 1111 has been released. Update title records and notify interested parties.",
            tags=["lien release", "lease"],
            weight=1.0
        ),
        SearchDocument(
            id="12",
            title="Probate Filing Detected: Estate of John Smith",
            content="Probate filing detected for the Estate of John Smith. Review for potential impact on mineral interests.",
            tags=["probate filing", "title defect"],
            weight=1.2
        ),
        SearchDocument(
            id="13",
            title="Court Order: Lease 1212",
            content="Court order affecting Lease 1212 has been recorded. Review order and update lease status.",
            tags=["court order", "lease"],
            weight=1.1
        ),
        SearchDocument(
            id="14",
            title="Tax Delinquency Detected: Lease 1313",
            content="Tax delinquency reported for Lease 1313. Immediate action required to prevent tax sale.",
            tags=["tax delinquency", "lease", "alert"],
            weight=1.4
        ),
        SearchDocument(
            id="15",
            title="Competitive Activity: Offset Well Drilled",
            content="A competitor has drilled a new offset well near Lease 1414. Assess impact on lease value.",
            tags=["competitive activity", "offset well"],
            weight=1.2
        ),
        SearchDocument(
            id="16",
            title="Price Threshold Alert: Oil Drops Below $60",
            content="Oil price has dropped below the $60 threshold. Review economic impact on active leases.",
            tags=["price threshold", "alert", "oil"],
            weight=1.3
        ),
        SearchDocument(
            id="17",
            title="Royalty Payment Alert: Lease 1515",
            content="Royalty payment for Lease 1515 is overdue. Contact operator for payment status.",
            tags=["royalty payment", "alert", "lease"],
            weight=1.2
        ),
        SearchDocument(
            id="18",
            title="Well Shut-In Detected: Well 1616",
            content="Well 1616 has been shut-in. Review shut-in notice and update production status.",
            tags=["well shut-in", "production change"],
            weight=1.1
        ),
        SearchDocument(
            id="19",
            title="Plugging Notice: Well 1717",
            content="Plugging notice filed for Well 1717. Ensure all plugging operations comply with RRC regulations.",
            tags=["plugging notice", "well", "rrc"],
            weight=1.2
        ),
        SearchDocument(
            id="20",
            title="Unitization Application: Lease 1818",
            content="Unitization application submitted for Lease 1818. Review application details and coordinate with stakeholders.",
            tags=["unitization application", "lease"],
            weight=1.1
        ),
        SearchDocument(
            id="21",
            title="Force Pooling Application: Lease 1919",
            content="Force pooling application filed for Lease 1919. Review for potential impact on working interests.",
            tags=["force pooling application", "lease"],
            weight=1.2
        ),
        SearchDocument(
            id="22",
            title="Surface Damage Claim: Lease 2020",
            content="Surface damage claim filed for Lease 2020. Assess damages and coordinate with surface owner.",
            tags=["surface damage", "claim", "lease"],
            weight=1.3
        ),
        SearchDocument(
            id="23",
            title="Environmental Release Detected: Lease 2121",
            content="Environmental release reported on Lease 2121. Initiate remediation and notify regulatory authorities.",
            tags=["environmental release", "lease", "alert"],
            weight=1.4
        ),
        SearchDocument(
            id="24",
            title="Bankruptcy Filing: Operator XYZ Resources",
            content="Operator XYZ Resources has filed for bankruptcy. Review impact on active leases and royalty payments.",
            tags=["bankruptcy filing", "operator", "lease"],
            weight=1.3
        ),
        SearchDocument(
            id="25",
            title="Title Defect Detected: Lease 2222",
            content="Title defect identified for Lease 2222. Review defect details and initiate curative action.",
            tags=["title defect", "lease"],
            weight=1.4
        ),
        SearchDocument(
            id="26",
            title="Assignment Recording: Lease 2323",
            content="Assignment recorded for Lease 2323. Update records to reflect new working interest owner.",
            tags=["assignment recording", "lease"],
            weight=1.1
        ),
        SearchDocument(
            id="27",
            title="Division Order Change: Lease 2424",
            content="Division order change submitted for Lease 2424. Review changes and update payment schedules.",
            tags=["division order", "lease"],
            weight=1.1
        ),
        SearchDocument(
            id="28",
            title="Well Completion Notice: Well 2525",
            content="Completion notice filed for Well 2525. Update production status and notify royalty owners.",
            tags=["well completion", "notice", "production"],
            weight=1.2
        ),
        SearchDocument(
            id="29",
            title="Spacing Order Detected: Lease 2626",
            content="Spacing order issued for Lease 2626. Review order for impact on drilling plans.",
            tags=["spacing order", "lease"],
            weight=1.1
        ),
        SearchDocument(
            id="30",
            title="Force Majeure Declaration: Lease 2727",
            content="Force majeure declared for Lease 2727 due to severe weather. Review lease obligations.",
            tags=["force majeure", "lease", "alert"],
            weight=1.3
        ),
        # Additional documents for coverage
        SearchDocument(
            id="31",
            title="Lease 2828: New Well Permit Application",
            content="A new well permit application has been submitted for Lease 2828. Review for completeness and compliance.",
            tags=["new filing", "permit", "lease"],
            weight=1.0
        ),
        SearchDocument(
            id="32",
            title="Production Drop Alert: Well 2929",
            content="Production for Well 2929 has dropped by 30% this month. Investigate possible causes.",
            tags=["production change", "well", "alert"],
            weight=1.2
        ),
        SearchDocument(
            id="33",
            title="Environmental Violation: Lease 3030",
            content="An environmental violation has been reported on Lease 3030. Immediate remediation required.",
            tags=["environmental release", "violation", "lease"],
            weight=1.4
        ),
        SearchDocument(
            id="34",
            title="Probate Impact: Lease 3131",
            content="Probate action may affect Lease 3131. Review estate filings for changes in ownership.",
            tags=["probate filing", "lease", "ownership transfer"],
            weight=1.2
        ),
        SearchDocument(
            id="35",
            title="Tax Sale Notice: Lease 3232",
            content="Lease 3232 is scheduled for tax sale due to unpaid taxes. Immediate payment required to avoid loss.",
            tags=["tax delinquency", "lease", "sale"],
            weight=1.4
        ),
    ]
    for doc in docs:
        index.add_document(doc)