import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

# -------------------------
# Data Classes
# -------------------------

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

# -------------------------
# Search Index
# -------------------------

class SearchIndex:
    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.total_doc_length = 0
        self.N = 0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
        self._preprocessed = False

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            self.total_doc_length += len(tokens)
            self.documents[doc.id] = doc
            self.N += 1
            for term in tf:
                self.doc_freqs[term] += 1
                self.inverted_index[term].add(doc.id)
            self._preprocessed = False

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9\-]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        avgdl = self.total_doc_length / self.N if self.N > 0 else 0
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + self.k1 * (1 - self.b + self.b * doc_len / avgdl)
            bm25 = idf * freq * (self.k1 + 1) / denom
            score += bm25
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            tf_norm = tf[term] / doc_len if doc_len > 0 else 0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * self.documents[doc_id].weight

    def _preprocess(self):
        if self._preprocessed:
            return
        self.idf_cache.clear()
        for term in self.doc_freqs:
            self._compute_idf(term)
        self._preprocessed = True

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        self._preprocess()
        candidate_docs = set()
        for term in query_terms:
            candidate_docs |= self.inverted_index.get(term, set())
        scored = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(query_terms, doc_id)
            tfidf_score = self._score_tfidf(query_terms, doc_id)
            score = bm25_score * 0.7 + tfidf_score * 0.3
            if score > 0:
                snippet = self._make_snippet(doc_id, query_terms)
                scored.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scored.sort(key=lambda r: r.score, reverse=True)
        return scored[:limit]

    def _make_snippet(self, doc_id: int, query_terms: List[str], window: int = 30) -> str:
        doc = self.documents[doc_id]
        content = doc.content
        content_tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(content_tokens) if t in query_terms]
        if not positions:
            return content[:160] + "..." if len(content) > 160 else content
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(content_tokens))
        snippet_tokens = content_tokens[start:end]
        snippet = " ".join(snippet_tokens)
        # Highlight terms
        for term in set(query_terms):
            snippet = re.sub(r'\b({})\b'.format(re.escape(term)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + "..."

    def get_stats(self) -> Dict[str, int]:
        return {
            "num_documents": self.N,
            "num_terms": len(self.doc_freqs),
            "total_doc_length": self.total_doc_length,
            "avg_doc_length": self.total_doc_length / self.N if self.N else 0
        }

# -------------------------
# Singleton Factory
# -------------------------

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

# -------------------------
# Pre-seed Domain Documents
# -------------------------

def _seed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Lease Primary Term Expiration",
            "The primary term of an oil and gas lease is the initial period during which the lessee has the right, but not the obligation, to drill and produce. If no production or other savings clause applies, the lease will expire at the end of the primary term. Track the expiration date to avoid loss of lease rights.",
            ["lease", "primary term", "expiration", "deadline"],
            1.0
        ),
        SearchDocument(
            2,
            "Continuous Drilling Clause Deadline",
            "A continuous drilling clause requires the lessee to commence drilling operations within a specified period after the completion of the previous well. Missing this deadline may result in lease termination as to non-producing acreage.",
            ["drilling", "continuous", "clause", "deadline"],
            1.0
        ),
        SearchDocument(
            3,
            "Shut-In Royalty Payment Deadline",
            "When a well capable of production is shut-in, the lessee must pay shut-in royalties within the timeframe specified in the lease to maintain the lease in force. Failure to timely pay may cause lease termination.",
            ["shut-in", "royalty", "payment", "deadline"],
            1.0
        ),
        SearchDocument(
            4,
            "Pooling Election Deadlines",
            "Pooling clauses may require the lessor or lessee to elect whether to participate in a proposed unit within a set period. Missing the pooling election deadline can impact royalty interests and lease validity.",
            ["pooling", "election", "deadline"],
            1.0
        ),
        SearchDocument(
            5,
            "Lease Option Exercise Dates",
            "Some leases grant the lessee an option to extend the primary term or acquire additional acreage. The option must be exercised by the specified date, or the right is lost.",
            ["lease", "option", "exercise", "date"],
            1.0
        ),
        SearchDocument(
            6,
            "W-1 Permit Expiration",
            "A Texas Railroad Commission W-1 drilling permit is valid for a limited period, typically two years. If drilling is not commenced before expiration, a new permit must be obtained.",
            ["w-1", "permit", "expiration", "drilling"],
            1.0
        ),
        SearchDocument(
            7,
            "RRC Compliance Deadlines",
            "The Texas Railroad Commission imposes various compliance deadlines, including reporting, testing, and remediation requirements. Missing these deadlines can result in fines or permit suspensions.",
            ["rrc", "compliance", "deadline", "railroad commission"],
            1.0
        ),
        SearchDocument(
            8,
            "Well Plugging Deadlines (Rule 14)",
            "Under RRC Rule 14, wells must be plugged within one year after ceasing production unless otherwise authorized. Operators must file plugging reports and comply with all deadlines.",
            ["well", "plugging", "rule 14", "deadline"],
            1.0
        ),
        SearchDocument(
            9,
            "P-4 Operator Transfer Deadlines",
            "A P-4 form must be filed with the RRC to transfer operator status. There are strict deadlines for filing to ensure continuous regulatory coverage.",
            ["p-4", "operator", "transfer", "deadline"],
            1.0
        ),
        SearchDocument(
            10,
            "Production Report Due Dates",
            "Monthly production reports are due to the RRC by the 15th of the month following production. Late filings may result in penalties.",
            ["production", "report", "due date", "rrc"],
            1.0
        ),
        SearchDocument(
            11,
            "Tax Payment Deadlines (Mineral Severance)",
            "Mineral severance taxes must be paid to the Texas Comptroller by the 20th day of the second month after production. Timely payment avoids penalties and interest.",
            ["tax", "payment", "mineral severance", "deadline"],
            1.0
        ),
        SearchDocument(
            12,
            "Statute of Limitations for Title Claims",
            "Title claims related to mineral interests are subject to statutes of limitations, often four years for breach of contract and two years for torts. Track deadlines to avoid losing claims.",
            ["statute of limitations", "title", "claim", "deadline"],
            1.0
        ),
        SearchDocument(
            13,
            "Recording Deadline Requirements",
            "Deeds, leases, and assignments should be recorded promptly to protect against subsequent purchasers. Some counties require recording within a set period to avoid penalties.",
            ["recording", "deadline", "requirement"],
            1.0
        ),
        SearchDocument(
            14,
            "Probate Filing Deadlines",
            "Probate proceedings for mineral interests must be filed within statutory deadlines, often four years from date of death. Late filings may require additional affidavits or court approval.",
            ["probate", "filing", "deadline"],
            1.0
        ),
        SearchDocument(
            15,
            "Heirship Affidavit Timing",
            "Heirship affidavits are used to establish mineral ownership when no probate occurs. Timely filing is critical to ensure marketable title and avoid disputes.",
            ["heirship", "affidavit", "timing", "deadline"],
            1.0
        ),
        SearchDocument(
            16,
            "Surface Damage Notice Deadlines",
            "Texas law requires operators to provide notice to surface owners before commencing drilling operations. Notice must be given at least 15 days prior to entry.",
            ["surface", "damage", "notice", "deadline"],
            1.0
        ),
        SearchDocument(
            17,
            "Drill Site Restoration Deadlines",
            "After well plugging, operators must restore the drill site within a specified period, often 1 year. Failure to comply may result in enforcement action.",
            ["drill site", "restoration", "deadline"],
            1.0
        ),
        SearchDocument(
            18,
            "Environmental Permit Renewal Deadlines",
            "Environmental permits, such as stormwater or air emissions, must be renewed before expiration. Missing renewal deadlines can halt operations.",
            ["environmental", "permit", "renewal", "deadline"],
            1.0
        ),
        SearchDocument(
            19,
            "Water Well Permit Renewal Deadlines",
            "Water well permits issued by local GCDs must be renewed periodically. Track renewal deadlines to avoid unauthorized use.",
            ["water well", "permit", "renewal", "deadline"],
            1.0
        ),
        SearchDocument(
            20,
            "GCD Reporting Deadlines",
            "Groundwater Conservation Districts require periodic reporting of water production. Deadlines vary by district but are strictly enforced.",
            ["gcd", "reporting", "deadline", "groundwater"],
            1.0
        ),
        SearchDocument(
            21,
            "Assignment Recording Deadlines",
            "Assignments of leases or interests must be recorded within county records to be effective against third parties. Some counties impose deadlines for recording.",
            ["assignment", "recording", "deadline"],
            1.0
        ),
        SearchDocument(
            22,
            "Force Majeure Notice Deadlines",
            "Force majeure clauses may require prompt notice to the lessor in the event of an excusable delay. Failure to provide timely notice may waive the defense.",
            ["force majeure", "notice", "deadline"],
            1.0
        ),
        SearchDocument(
            23,
            "Division Order Execution Deadlines",
            "Division orders must be executed and returned to the operator within a specified period to receive royalty payments. Delays may suspend payments.",
            ["division order", "execution", "deadline"],
            1.0
        ),
        SearchDocument(
            24,
            "Unitization Election Deadlines",
            "Unitization agreements often require parties to elect participation by a certain deadline. Missing the election may result in exclusion from the unit.",
            ["unitization", "election", "deadline"],
            1.0
        ),
        SearchDocument(
            25,
            "Affidavit of Non-Production Filing",
            "To release expired leases, an affidavit of non-production should be filed in county records. Some states impose deadlines for such filings.",
            ["affidavit", "non-production", "filing", "deadline"],
            1.0
        ),
        SearchDocument(
            26,
            "Shut-In Well Reporting Requirements",
            "Operators must report shut-in well status to the RRC within prescribed deadlines. Failure to report may result in enforcement action.",
            ["shut-in", "well", "reporting", "deadline"],
            1.0
        ),
        SearchDocument(
            27,
            "Cessation of Production Clause Deadlines",
            "Leases may contain cessation of production clauses requiring resumption of operations within a set period to avoid lease termination.",
            ["cessation", "production", "clause", "deadline"],
            1.0
        ),
        SearchDocument(
            28,
            "Surface Use Agreement Notice Periods",
            "Surface use agreements may require notice to the surface owner before commencing operations. Notice periods vary by agreement.",
            ["surface use", "agreement", "notice", "period"],
            1.0
        ),
        SearchDocument(
            29,
            "Plugging Extension Application Deadlines",
            "Operators seeking an extension of plugging deadlines must file applications before the current deadline expires.",
            ["plugging", "extension", "application", "deadline"],
            1.0
        ),
        SearchDocument(
            30,
            "Royalty Payment Statute of Limitations",
            "Claims for unpaid royalties are subject to statutes of limitations, typically four years in Texas. Track deadlines to preserve claims.",
            ["royalty", "payment", "statute of limitations", "deadline"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)