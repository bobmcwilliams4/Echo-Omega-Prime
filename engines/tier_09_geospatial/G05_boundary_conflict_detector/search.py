import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# --- Data Classes ---

class SearchDocument:
    def __init__(self, id: int, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = id
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

# --- Search Index ---

class SearchIndex:
    def __init__(self):
        self._documents: Dict[int, SearchDocument] = {}
        self._doc_tokens: Dict[int, List[str]] = {}
        self._doc_freqs: Dict[int, Counter] = {}
        self._inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self._doc_lengths: Dict[int, int] = {}
        self._avgdl: float = 0.0
        self._N: int = 0
        self._lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            self._documents[doc.id] = doc
            self._doc_tokens[doc.id] = tokens
            tf = Counter(tokens)
            self._doc_freqs[doc.id] = tf
            self._doc_lengths[doc.id] = len(tokens)
            for term, freq in tf.items():
                self._inverted_index[term][doc.id] = freq
            self._N += 1
            self._avgdl = sum(self._doc_lengths.values()) / self._N if self._N > 0 else 0.0
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self._inverted_index.get(term, {}).keys())
        scored: List[Tuple[int, float]] = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc_weight = self._documents[doc_id].weight
            final_score = 0.7 * bm25_score + 0.3 * tfidf_score
            final_score *= doc_weight
            scored.append((doc_id, final_score))
        scored.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored[:limit]:
            doc = self._documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                "document_count": self._N,
                "average_doc_length": self._avgdl,
                "unique_terms": len(self._inverted_index),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s\-\.]", " ", text)
        tokens = [t for t in text.split() if t]
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = len(self._inverted_index.get(term, {}))
        N = max(self._N, 1)
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc_len = self._doc_lengths.get(doc_id, 0)
        avgdl = self._avgdl if self._avgdl > 0 else 1.0
        tf = self._doc_freqs.get(doc_id, Counter())
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / avgdl)
            term_score = idf * (f * (self._bm25_k1 + 1)) / (denom + 1e-9)
            score += term_score
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self._doc_freqs.get(doc_id, Counter())
        doc_len = self._doc_lengths.get(doc_id, 1)
        score = 0.0
        for term in query_terms:
            term_tf = tf.get(term, 0) / doc_len
            idf = self._compute_idf(term)
            score += term_tf * idf
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
        start = max(min(positions) - window // 2, 0)
        end = min(start + window, len(content))
        snippet = content[start:end]
        return snippet + "..." if end < len(content) else snippet

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

# --- Pre-seed Domain Documents ---

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Vacancy Strip Detection in Texas Surveys",
            "Vacancy strips are narrow parcels of unclaimed land between surveyed tracts, often resulting from closure errors or ambiguous calls. Detection involves analyzing metes and bounds, survey overlaps, and historical records.",
            ["vacancy", "strip", "texas", "detection", "closure error"],
            1.0
        ),
        SearchDocument(
            2,
            "Junior vs Senior Survey Priority Doctrine",
            "When two surveys overlap, the senior survey (earlier in time) generally prevails over the junior survey. Exceptions may apply if the senior survey is ambiguous or defective.",
            ["junior", "senior", "priority", "overlap", "doctrine"],
            1.0
        ),
        SearchDocument(
            3,
            "Excess and Deficit in Survey Area",
            "Excess or deficit occurs when the measured area of a tract differs from its recorded area. Texas law provides rules for apportioning excess or deficit among conflicting tracts.",
            ["excess", "deficit", "area", "apportionment", "texas"],
            1.0
        ),
        SearchDocument(
            4,
            "Gap Detection Between Adjacent Tracts",
            "Gaps between tracts may arise from survey errors, ambiguous calls, or misinterpretation of natural boundaries. Detecting gaps requires careful analysis of deeds, maps, and field evidence.",
            ["gap", "detection", "tract", "survey", "boundary"],
            1.0
        ),
        SearchDocument(
            5,
            "Closure Error Analysis in Metes and Bounds",
            "Closure error is the failure of a survey traverse to return to its point of beginning. Analyzing closure error involves checking bearings, distances, and monument calls.",
            ["closure error", "metes and bounds", "analysis", "bearings"],
            1.0
        ),
        SearchDocument(
            6,
            "Metes and Bounds Traversal Techniques",
            "Metes and bounds surveys describe land by courses and distances. Traversal techniques include chaining, compass readings, and monument referencing.",
            ["metes and bounds", "traversal", "techniques", "survey"],
            1.0
        ),
        SearchDocument(
            7,
            "Bearing Tree and Monument Calls",
            "Bearing trees and monuments are physical references used to mark survey corners. Calls to these features help resolve ambiguities in boundary location.",
            ["bearing tree", "monument", "calls", "survey", "boundary"],
            1.0
        ),
        SearchDocument(
            8,
            "Natural Boundary Interpretation",
            "Natural boundaries such as rivers, creeks, and ridges often control over artificial calls. Interpreting natural boundaries requires understanding accretion, avulsion, and historical changes.",
            ["natural boundary", "interpretation", "accretion", "avulsion"],
            1.0
        ),
        SearchDocument(
            9,
            "Accretion and Avulsion in Boundary Law",
            "Accretion is the gradual addition of land by water, while avulsion is a sudden change. Texas law distinguishes between these for boundary determination.",
            ["accretion", "avulsion", "boundary", "law", "texas"],
            1.0
        ),
        SearchDocument(
            10,
            "Resurvey Procedures for Texas Land",
            "Resurveys are conducted to clarify or correct original surveys. Procedures involve retracing original lines, evaluating evidence, and applying survey call hierarchy.",
            ["resurvey", "procedures", "texas", "survey", "call hierarchy"],
            1.0
        ),
        SearchDocument(
            11,
            "Survey Call Hierarchy Explained",
            "The hierarchy of survey calls determines which calls control in case of conflict: natural objects, artificial monuments, courses, distances, and area.",
            ["survey", "call hierarchy", "conflict", "monuments"],
            1.0
        ),
        SearchDocument(
            12,
            "Patent vs. Deed Boundary Conflicts",
            "Conflicts between patent and deed boundaries are resolved by giving priority to the patent if the deed description is ambiguous or inconsistent.",
            ["patent", "deed", "boundary", "conflict", "priority"],
            1.0
        ),
        SearchDocument(
            13,
            "Railroad Survey Strip Conflicts",
            "Railroad surveys often created narrow strips that conflict with adjacent grants. Resolving these requires analysis of original survey intent and seniority.",
            ["railroad", "survey", "strip", "conflict", "seniority"],
            1.0
        ),
        SearchDocument(
            14,
            "Spanish and Mexican Land Grant Boundaries",
            "Spanish and Mexican land grants in Texas have unique boundary descriptions, often referencing natural features and early monuments. Interpretation requires historical research.",
            ["spanish", "mexican", "land grant", "boundary", "texas"],
            1.0
        ),
        SearchDocument(
            15,
            "Mineral Reservation Boundary Disputes",
            "Mineral reservations may create boundaries distinct from surface boundaries, leading to disputes over ownership and access.",
            ["mineral", "reservation", "boundary", "dispute", "surface"],
            1.0
        ),
        SearchDocument(
            16,
            "Surface vs. Subsurface Boundary Divergence",
            "Surface and subsurface boundaries may diverge due to mineral reservations, pooling, or directional drilling. Legal doctrine governs resolution.",
            ["surface", "subsurface", "boundary", "divergence", "doctrine"],
            1.0
        ),
        SearchDocument(
            17,
            "Boundary by Acquiescence Doctrine",
            "Boundaries may be established by long-term acquiescence of adjoining landowners, even if not matching the record description.",
            ["boundary", "acquiescence", "doctrine", "landowner"],
            1.0
        ),
        SearchDocument(
            18,
            "Agreed Boundary Doctrine in Texas",
            "When parties agree on a boundary and act accordingly, the agreed boundary may control over conflicting descriptions.",
            ["agreed boundary", "doctrine", "texas", "conflict"],
            1.0
        ),
        SearchDocument(
            19,
            "Vacancy Strip Litigation Procedures",
            "Litigation over vacancy strips involves title examination, historical research, and expert testimony regarding survey methods.",
            ["vacancy", "strip", "litigation", "procedures", "survey"],
            1.0
        ),
        SearchDocument(
            20,
            "Resolving Overlapping Surveys",
            "Overlapping surveys are resolved by applying the junior-senior doctrine, analyzing call hierarchy, and considering extrinsic evidence.",
            ["overlap", "survey", "junior", "senior", "call hierarchy"],
            1.0
        ),
        SearchDocument(
            21,
            "Historical Survey Methods in Texas",
            "Early Texas surveys used chains, compasses, and natural features. Understanding these methods aids in resolving modern boundary disputes.",
            ["historical", "survey", "methods", "texas", "boundary"],
            1.0
        ),
        SearchDocument(
            22,
            "Field Notes and Survey Plats",
            "Field notes and plats provide critical evidence for boundary location. Discrepancies between them must be reconciled using legal principles.",
            ["field notes", "plats", "boundary", "evidence"],
            1.0
        ),
        SearchDocument(
            23,
            "Doctrine of Monuments in Boundary Law",
            "Monuments, whether natural or artificial, generally control over courses and distances in boundary disputes.",
            ["doctrine", "monuments", "boundary", "law"],
            1.0
        ),
        SearchDocument(
            24,
            "Surveying Water Boundaries in Texas",
            "Water boundaries, such as the beds of rivers and lakes, are governed by doctrines of accretion, reliction, and avulsion.",
            ["survey", "water", "boundary", "texas", "accretion"],
            1.0
        ),
        SearchDocument(
            25,
            "Resolving Gaps and Overlaps in Deed Descriptions",
            "Gaps and overlaps in deed descriptions are resolved by applying rules of construction, considering intent, and referencing monuments.",
            ["gaps", "overlaps", "deed", "description", "monuments"],
            1.0
        ),
        SearchDocument(
            26,
            "Surveying Techniques for Boundary Resolution",
            "Modern and historical surveying techniques, including GPS, total station, and compass chaining, are used to resolve boundary conflicts.",
            ["surveying", "techniques", "boundary", "resolution"],
            1.0
        ),
        SearchDocument(
            27,
            "Title Examination in Boundary Disputes",
            "Title examination traces the chain of title to identify conflicting claims and resolve boundary disputes.",
            ["title", "examination", "boundary", "disputes"],
            1.0
        ),
        SearchDocument(
            28,
            "Role of Extrinsic Evidence in Survey Conflicts",
            "Extrinsic evidence, such as witness testimony and historical maps, may be used to resolve ambiguities in survey descriptions.",
            ["extrinsic", "evidence", "survey", "conflict"],
            1.0
        ),
        SearchDocument(
            29,
            "Texas Supreme Court Precedents on Survey Overlap",
            "Key Texas Supreme Court cases provide guidance on resolving survey overlaps, vacancy strips, and conflicting boundary descriptions.",
            ["texas", "supreme court", "survey", "overlap", "precedent"],
            1.0
        ),
        SearchDocument(
            30,
            "Practical Steps for Boundary Conflict Resolution",
            "Boundary conflict resolution involves research, field investigation, legal analysis, and, if necessary, litigation.",
            ["boundary", "conflict", "resolution", "litigation"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)