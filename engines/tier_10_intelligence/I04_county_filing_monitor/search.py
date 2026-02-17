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
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[Tuple[str, str], float] = {}

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            tf = Counter(tokens)
            self.term_freqs[doc.id] = dict(tf)
            for term in tf:
                self.doc_freqs[term] += 1
            self.doc_lengths[doc.id] = len(tokens)
            self.documents[doc.id] = doc
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[str, float] = defaultdict(float)
        for term in query_terms:
            idf = self._compute_idf(term)
            for doc_id, tf_dict in self.term_freqs.items():
                tf = tf_dict.get(term, 0)
                if tf == 0:
                    continue
                bm25_score = self._score_bm25(term, doc_id, idf)
                tfidf_score = self._score_tfidf(term, doc_id, idf)
                doc = self.documents[doc_id]
                total_score = (bm25_score * 0.7 + tfidf_score * 0.3) * doc.weight
                doc_scores[doc_id] += total_score
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "document_count": self.N,
                "avg_doc_length": self.avg_doc_length,
                "unique_terms": len(self.doc_freqs)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, term: str, doc_id: str, idf: Optional[float] = None) -> float:
        tf = self.term_freqs[doc_id].get(term, 0)
        doc_len = self.doc_lengths[doc_id]
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        if idf is None:
            idf = self._compute_idf(term)
        numerator = tf * (self.k1 + 1)
        denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / avg_dl)
        return idf * numerator / denominator if denominator > 0 else 0.0

    def _score_tfidf(self, term: str, doc_id: str, idf: Optional[float] = None) -> float:
        key = (term, doc_id)
        if key in self._tfidf_cache:
            return self._tfidf_cache[key]
        tf = self.term_freqs[doc_id].get(term, 0)
        doc_len = self.doc_lengths[doc_id]
        tf_norm = tf / doc_len if doc_len > 0 else 0.0
        if idf is None:
            idf = self._compute_idf(term)
        score = tf_norm * idf
        self._tfidf_cache[key] = score
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            idx = content_lower.find(term)
            if idx != -1:
                positions.append(idx)
        if not positions:
            return content[:window] + "..." if len(content) > window else content
        start = max(0, min(positions) - window // 2)
        end = min(len(content), start + window)
        snippet = content[start:end]
        return snippet + "..." if end < len(content) else snippet

# Singleton factory
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
            "Kofile Filing System Reliability",
            "Analysis of system uptime, error rates, and data integrity in Kofile-managed county clerk filing platforms. Includes monitoring of batch polling and webhook reliability.",
            ["reliability", "kofile", "system", "monitoring"],
            1.0
        ),
        SearchDocument(
            "2",
            "Tyler PublicSearch Instrument Classification",
            "Evaluation of Tyler Technologies PublicSearch instrument type classification accuracy using clerk filing metadata and OCR.",
            ["tyler", "classification", "publicsearch", "ocr"],
            1.0
        ),
        SearchDocument(
            "3",
            "TexasFile Filing Volume Analysis",
            "Monthly and daily filing volume trends in TexasFile counties. Detects anomalies and surges in deed, lien, and plat filings.",
            ["texasfile", "volume", "trends", "deed", "lien", "plat"],
            1.0
        ),
        SearchDocument(
            "4",
            "Lease Trend Detection via Clerk Filings",
            "Detects new lease filings and renewal patterns using county clerk data feeds. Supports oil, gas, and mineral lease monitoring.",
            ["lease", "trend", "clerk", "oil", "gas", "mineral"],
            1.0
        ),
        SearchDocument(
            "5",
            "Deed Transfer Pattern Analysis",
            "Identifies patterns in deed transfers, including grantor-grantee relationships and subdivision activity.",
            ["deed", "transfer", "pattern", "subdivision"],
            1.0
        ),
        SearchDocument(
            "6",
            "Lien Filing Monitoring and Classification",
            "Monitors new and released liens, classifies by type (mechanics, tax, judgment, UCC), and tracks chain-of-custody.",
            ["lien", "monitoring", "classification", "mechanics", "tax", "judgment", "ucc"],
            1.0
        ),
        SearchDocument(
            "7",
            "Lis Pendens Tracking and Alerting",
            "Tracks new lis pendens filings and generates alerts for affected parcels and parties.",
            ["lis pendens", "tracking", "alerting", "parcels"],
            1.0
        ),
        SearchDocument(
            "8",
            "Probate Filing Alerts and Monitoring",
            "Monitors probate filings, detects estate openings, and triggers notifications for legal and title professionals.",
            ["probate", "monitoring", "alerts", "estate"],
            1.0
        ),
        SearchDocument(
            "9",
            "Assignment Chain Tracking",
            "Tracks assignment chains for deeds of trust, leases, and liens. Detects breaks and duplicate assignments.",
            ["assignment", "chain", "tracking", "deeds", "leases", "liens"],
            1.0
        ),
        SearchDocument(
            "10",
            "Release of Lien Monitoring",
            "Detects releases of liens and reconciles with original filings to ensure data completeness.",
            ["release", "lien", "monitoring", "reconciliation"],
            1.0
        ),
        SearchDocument(
            "11",
            "Mechanics Lien Detection and Monitoring",
            "Identifies mechanics lien filings, tracks contractor activity, and alerts on new claims.",
            ["mechanics", "lien", "detection", "monitoring", "contractor"],
            1.0
        ),
        SearchDocument(
            "12",
            "Federal Tax Lien Tracking",
            "Monitors federal tax lien filings, releases, and associated parties in county clerk records.",
            ["federal", "tax", "lien", "tracking", "releases"],
            1.0
        ),
        SearchDocument(
            "13",
            "Judgment Lien Identification",
            "Detects judgment liens, tracks satisfaction and release, and classifies by court and jurisdiction.",
            ["judgment", "lien", "identification", "court", "jurisdiction"],
            1.0
        ),
        SearchDocument(
            "14",
            "UCC Filing Monitoring",
            "Monitors Uniform Commercial Code (UCC) filings, amendments, and terminations in county clerk systems.",
            ["ucc", "filing", "monitoring", "amendment", "termination"],
            1.0
        ),
        SearchDocument(
            "15",
            "Plat Filing Tracking",
            "Tracks new plat filings, detects new subdivisions, and monitors right-of-way (ROW) acquisition patterns.",
            ["plat", "filing", "tracking", "subdivision", "row"],
            1.0
        ),
        SearchDocument(
            "16",
            "New Subdivision Detection",
            "Detects new subdivision activity from plat and deed filings, infers developer and builder activity.",
            ["subdivision", "detection", "plat", "deed", "developer"],
            1.0
        ),
        SearchDocument(
            "17",
            "ROW Acquisition Pattern Analysis",
            "Analyzes right-of-way acquisition patterns using deed and easement filings. Supports pipeline and utility monitoring.",
            ["row", "acquisition", "pattern", "deed", "easement", "pipeline"],
            1.0
        ),
        SearchDocument(
            "18",
            "Surface Use Agreement Filings",
            "Monitors filings related to surface use agreements, including oil and gas operations.",
            ["surface", "agreement", "filing", "oil", "gas"],
            1.0
        ),
        SearchDocument(
            "19",
            "Pipeline Easement Filing Monitoring",
            "Tracks pipeline easement filings, detects new pipeline activity, and infers operator involvement.",
            ["pipeline", "easement", "filing", "monitoring", "operator"],
            1.0
        ),
        SearchDocument(
            "20",
            "Operator Activity Inference from Filings",
            "Infers operator activity from lease, easement, and assignment filings. Supports oil and gas intelligence.",
            ["operator", "activity", "inference", "lease", "easement", "assignment"],
            1.0
        ),
        SearchDocument(
            "21",
            "Instrument Type Classification Accuracy",
            "Evaluates accuracy of instrument type classification in county clerk and vendor platforms using metadata and OCR.",
            ["instrument", "classification", "accuracy", "ocr", "metadata"],
            1.0
        ),
        SearchDocument(
            "22",
            "Data Completeness in County Clerk Filings",
            "Audits data completeness for required metadata fields in county clerk filings. Detects missing or inconsistent entries.",
            ["data", "completeness", "county", "clerk", "filing", "audit"],
            1.0
        ),
        SearchDocument(
            "23",
            "Audit Log Completeness in Clerk Filing Systems",
            "Monitors audit log entries for completeness and chain-of-custody in clerk filing systems.",
            ["audit", "log", "completeness", "chain-of-custody", "clerk"],
            1.0
        ),
        SearchDocument(
            "24",
            "OCR Accuracy in Clerk Filing Systems",
            "Evaluates OCR accuracy for scanned instruments in county clerk platforms. Detects and flags low-confidence extractions.",
            ["ocr", "accuracy", "clerk", "filing", "scanned"],
            1.0
        ),
        SearchDocument(
            "25",
            "API Availability and Latency in Clerk Filing Platforms",
            "Monitors API uptime, latency, and error rates for county clerk filing vendors (Kofile, Tyler, TexasFile).",
            ["api", "availability", "latency", "clerk", "kofile", "tyler", "texasfile"],
            1.0
        ),
        SearchDocument(
            "26",
            "Webhook Subscription Reliability in Clerk Filing Platforms",
            "Tracks webhook delivery success, retries, and failure rates for event subscriptions in filing platforms.",
            ["webhook", "subscription", "reliability", "filing", "platform"],
            1.0
        ),
        SearchDocument(
            "27",
            "Chain-of-Custody Features in Clerk Filing Systems",
            "Assesses chain-of-custody features, including audit trails and digital signatures, in county clerk systems.",
            ["chain-of-custody", "features", "audit", "digital", "signature"],
            1.0
        ),
        SearchDocument(
            "28",
            "Duplicate Filing Reconciliation",
            "Detects and reconciles duplicate filings in county clerk records, ensuring data accuracy.",
            ["duplicate", "filing", "reconciliation", "accuracy"],
            1.0
        ),
        SearchDocument(
            "29",
            "Batch Polling Frequency Optimization",
            "Optimizes batch polling intervals for clerk system integrations to balance timeliness and resource usage.",
            ["batch", "polling", "frequency", "optimization", "integration"],
            1.0
        ),
        SearchDocument(
            "30",
            "Instrument Metadata Completeness",
            "Audits instrument metadata for completeness, including grantor, grantee, legal description, and instrument type.",
            ["instrument", "metadata", "completeness", "grantor", "grantee"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)