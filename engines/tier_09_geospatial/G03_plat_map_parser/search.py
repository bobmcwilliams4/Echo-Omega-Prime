import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# --- Data Classes ---

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

# --- Search Index Implementation ---

class SearchIndex:
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[Tuple[int, str], float] = {}

        self.k1 = 1.5
        self.b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return  # No duplicate IDs

            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1

            term_counts = Counter(tokens)
            for term, freq in term_counts.items():
                self.inverted_index[term][doc.id] = freq
                self.doc_freqs[term] += 1

            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, {}).keys())

        scores = {}
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc_weight = self.documents[doc_id].weight
            total_score = bm25_score * 0.7 + tfidf_score * 0.3
            total_score *= doc_weight
            scores[doc_id] = total_score

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                'total_docs': self.total_docs,
                'avg_doc_length': self.avg_doc_length,
                'unique_terms': len(self.inverted_index),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        text = re.sub(r'[^a-z0-9]+', ' ', text)
        tokens = text.split()
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        tokens = self._tokenize(doc.content)
        term_counts = Counter(tokens)

        for term in set(query_terms):
            f = term_counts.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self.k1 * (1 - self.b + self.b * doc_len / (self.avg_doc_length or 1))
            score += idf * (f * (self.k1 + 1)) / denom
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        tokens = self._tokenize(doc.content)
        term_counts = Counter(tokens)
        doc_len = len(tokens)
        for term in set(query_terms):
            tf = term_counts.get(term, 0) / (doc_len or 1)
            idf = self._compute_idf(term)
            score += tf * idf
        return score

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:window]) + ('...' if len(tokens) > window else '')
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return snippet + ('...' if end < len(tokens) else '')

# --- Singleton Factory ---

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

# --- Pre-seed Domain Documents ---

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Texas Subdivision Plat Requirements Overview",
            "Subdivision plats in Texas must comply with state and local regulations. Key requirements include accurate boundary descriptions, lot and block numbering, right-of-way dedications, utility easements, and compliance with Texas Local Government Code Chapter 212.",
            ["plat", "requirements", "overview", "texas"],
            1.0
        ),
        SearchDocument(
            2,
            "Lot and Block Numbering Systems",
            "A plat must clearly label each lot and block with unique numbers or letters. The numbering system should be sequential and avoid duplication within the subdivision. This ensures clarity for property identification and legal descriptions.",
            ["lot", "block", "numbering", "systems"],
            1.0
        ),
        SearchDocument(
            3,
            "Required Plat Elements",
            "Essential elements of a Texas subdivision plat include metes and bounds descriptions, bearings and distances, curve data, scale, north arrow, legend, dedication statements, and signatures of the surveyor and property owner.",
            ["plat", "elements", "required"],
            1.0
        ),
        SearchDocument(
            4,
            "Replat Procedures in Texas",
            "Replatting involves amending an existing subdivision plat. The process requires public notice, hearings, and compliance with local ordinances. Certain replats may be exempt from hearings if no public infrastructure is affected.",
            ["replat", "procedures", "texas"],
            1.0
        ),
        SearchDocument(
            5,
            "Amending Plat Requirements",
            "An amending plat may be filed to correct errors, relocate lot lines, or address minor changes. Texas law allows amending plats without notice or hearing if no new lots are created and no public interests are adversely affected.",
            ["amending", "plat", "requirements"],
            1.0
        ),
        SearchDocument(
            6,
            "Metes and Bounds Extraction",
            "Metes and bounds descriptions define property boundaries using bearings, distances, and reference points. Extraction involves parsing legal descriptions to identify courses, calls, and monument references for mapping.",
            ["metes", "bounds", "extraction"],
            1.0
        ),
        SearchDocument(
            7,
            "Bearing and Distance Parsing",
            "Bearings indicate direction (e.g., N45°30'E), while distances specify length (e.g., 125.00 feet). Accurate parsing is essential for reconstructing property lines from plat documents.",
            ["bearing", "distance", "parsing"],
            1.0
        ),
        SearchDocument(
            8,
            "Curve Data Extraction",
            "Curves on plats are described by radius, chord, arc length, and central angle. Extraction requires identifying these parameters and associating them with the correct lot or boundary segment.",
            ["curve", "data", "extraction"],
            1.0
        ),
        SearchDocument(
            9,
            "Plat Scale Interpretation",
            "The plat scale (e.g., 1\"=100') translates measurements on the drawing to real-world distances. Accurate interpretation ensures proper dimensioning and compliance with survey standards.",
            ["plat", "scale", "interpretation"],
            1.0
        ),
        SearchDocument(
            10,
            "Right-of-Way Dedications",
            "Plats must show right-of-way dedications for streets, alleys, and public spaces. These dedications are typically labeled and dimensioned, with notes indicating the entity accepting the dedication.",
            ["right-of-way", "dedications"],
            1.0
        ),
        SearchDocument(
            11,
            "Utility Easement Extraction",
            "Utility easements must be clearly indicated on plats, with dimensions and purposes specified. Extraction involves identifying labeled easements and their associated restrictions.",
            ["utility", "easement", "extraction"],
            1.0
        ),
        SearchDocument(
            12,
            "Building Setback Lines",
            "Setback lines define the minimum distance structures must be from property boundaries. Plats must show these lines, typically labeled as 'building setback' or 'B.S.L.'.",
            ["building", "setback", "lines"],
            1.0
        ),
        SearchDocument(
            13,
            "Flood Zone Annotations",
            "Plats should indicate flood zones as designated by FEMA. Annotations may reference FIRM panels, base flood elevations, and floodplain boundaries.",
            ["flood", "zone", "annotations"],
            1.0
        ),
        SearchDocument(
            14,
            "Plat Filing Requirements by County",
            "Each Texas county may have unique plat filing requirements, including submission format, fees, and review processes. Always consult the county clerk for current procedures.",
            ["plat", "filing", "requirements", "county"],
            1.0
        ),
        SearchDocument(
            15,
            "Texas Local Government Code Chapter 212 Overview",
            "Chapter 212 of the Texas Local Government Code governs municipal regulation of plats and subdivisions. It outlines approval processes, enforcement, and exceptions for certain types of development.",
            ["texas", "local", "government", "code", "212"],
            1.0
        ),
        SearchDocument(
            16,
            "Dedication Statements",
            "Dedication statements on plats convey public rights in streets, easements, or other areas. These statements must be signed and notarized as required by law.",
            ["dedication", "statements"],
            1.0
        ),
        SearchDocument(
            17,
            "Surveyor's Certificate",
            "A surveyor's certificate affirms the accuracy of the plat and its compliance with surveying standards. It must bear the surveyor's seal and signature.",
            ["surveyor", "certificate"],
            1.0
        ),
        SearchDocument(
            18,
            "Legend and North Arrow",
            "A plat legend explains symbols and abbreviations. The north arrow orients the drawing and must be clearly shown.",
            ["legend", "north", "arrow"],
            1.0
        ),
        SearchDocument(
            19,
            "Public Notice for Replats",
            "Texas law requires public notice for certain replats, including publication in a newspaper and notification of adjacent property owners.",
            ["public", "notice", "replats"],
            1.0
        ),
        SearchDocument(
            20,
            "Plat Review Process",
            "The plat review process involves submission to municipal or county authorities, technical review, and approval or denial based on compliance with regulations.",
            ["plat", "review", "process"],
            1.0
        ),
        SearchDocument(
            21,
            "Lot Line Adjustments",
            "Lot line adjustments may be processed as amending plats if no new lots are created and all lots remain compliant with zoning and subdivision regulations.",
            ["lot", "line", "adjustments"],
            1.0
        ),
        SearchDocument(
            22,
            "Common Plat Errors",
            "Frequent errors include missing bearings, incorrect lot numbering, omitted dedication statements, and incomplete legend information.",
            ["plat", "errors", "common"],
            1.0
        ),
        SearchDocument(
            23,
            "Monument Reference in Metes and Bounds",
            "Metes and bounds descriptions often reference monuments such as iron rods, concrete markers, or trees. Accurate identification is critical for boundary location.",
            ["monument", "reference", "metes", "bounds"],
            1.0
        ),
        SearchDocument(
            24,
            "FIRM Panel References",
            "Flood Insurance Rate Map (FIRM) panel numbers should be cited on plats when flood zones are present. This ensures compliance with floodplain management requirements.",
            ["firm", "panel", "references"],
            1.0
        ),
        SearchDocument(
            25,
            "Plat Approval Exceptions",
            "Certain subdivisions may be exempt from plat approval under Texas law, such as divisions of land for agricultural use or where all lots exceed five acres and no public improvements are required.",
            ["plat", "approval", "exceptions"],
            1.0
        ),
        SearchDocument(
            26,
            "Digital Plat Submission Standards",
            "Many counties require plats to be submitted digitally in PDF or CAD formats. Digital standards may specify resolution, layering, and file naming conventions.",
            ["digital", "plat", "submission", "standards"],
            1.0
        ),
        SearchDocument(
            27,
            "Plat Amendment Filing Process",
            "Amending plats must be filed with the county clerk, accompanied by the required fees and documentation. The process may differ by jurisdiction.",
            ["plat", "amendment", "filing", "process"],
            1.0
        ),
        SearchDocument(
            28,
            "Easement Types on Plats",
            "Plats may show various easement types, including utility, drainage, access, and landscape easements. Each must be labeled and dimensioned.",
            ["easement", "types", "plats"],
            1.0
        ),
        SearchDocument(
            29,
            "Plat Legend Symbols",
            "Symbols used in plat legends may include lines for easements, dashed lines for setbacks, and icons for monuments. The legend ensures correct interpretation.",
            ["plat", "legend", "symbols"],
            1.0
        ),
        SearchDocument(
            30,
            "Subdivision Name and Legal Description",
            "A plat must state the subdivision name and provide a legal description, including survey, abstract, county, and state references.",
            ["subdivision", "name", "legal", "description"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)