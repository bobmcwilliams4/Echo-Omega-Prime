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
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.doc_lengths: Dict[int, int] = {}
        self.N = 0
        self.avg_doc_len = 0.0
        self.inverted_index: Dict[str, set] = defaultdict(set)
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_norms: Dict[int, float] = {}
        self._tfidf_cache: Dict[Tuple[int, str], float] = {}

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            tf = Counter(tokens)
            self.documents[doc.id] = doc
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.doc_freqs[term] += 1
                self.inverted_index[term].add(doc.id)
            self.N += 1
            self.avg_doc_len = sum(self.doc_lengths.values()) / self.N
            self._idf_cache.clear()
            self._tfidf_norms.clear()
            self._tfidf_cache.clear()

    def search(self, query: str, limit: int = 10, method: str = "bm25") -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, set()))
        scores = {}
        for doc_id in candidate_docs:
            if method == "bm25":
                score = self._score_bm25(doc_id, query_terms)
            elif method == "tfidf":
                score = self._score_tfidf(doc_id, query_terms)
            else:
                raise ValueError("Unknown scoring method: %s" % method)
            if score > 0:
                scores[doc_id] = score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self):
        return {
            "num_documents": self.N,
            "avg_doc_length": self.avg_doc_len,
            "vocab_size": len(self.doc_freqs)
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
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

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        doc = self.documents[doc_id]
        tf = self.term_freqs[doc_id]
        dl = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            f = tf[term]
            denom = f + self.k1 * (1 - self.b + self.b * dl / self.avg_doc_len)
            score += idf * (f * (self.k1 + 1)) / denom
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        doc = self.documents[doc_id]
        tf = self.term_freqs[doc_id]
        dl = self.doc_lengths[doc_id]
        norm = self._tfidf_norm(doc_id)
        score = 0.0
        query_tf = Counter(query_terms)
        for term in query_tf:
            if term not in tf:
                continue
            tf_val = tf[term] / dl
            idf = self._compute_idf(term)
            score += (tf_val * idf) * (query_tf[term])
        if norm > 0:
            score /= norm
        return score * doc.weight

    def _tfidf_norm(self, doc_id: int) -> float:
        if doc_id in self._tfidf_norms:
            return self._tfidf_norms[doc_id]
        tf = self.term_freqs[doc_id]
        dl = self.doc_lengths[doc_id]
        s = 0.0
        for term in tf:
            tf_val = tf[term] / dl
            idf = self._compute_idf(term)
            s += (tf_val * idf) ** 2
        norm = math.sqrt(s)
        self._tfidf_norms[doc_id] = norm
        return norm

    def _make_snippet(self, content: str, query_terms: List[str], length: int = 160) -> str:
        content = content.strip()
        tokens = self._tokenize(content)
        positions = []
        for i, token in enumerate(tokens):
            if token in query_terms:
                positions.append(i)
        if not positions:
            snippet = content[:length] + "..." if len(content) > length else content
            return snippet
        start = max(positions[0] - 10, 0)
        end = min(start + 30, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(r'\b(%s)\b' % re.escape(term), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + "..."

# Singleton factory
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_math10_geometry(_search_index_instance)
        return _search_index_instance

def _preseed_math10_geometry(index: SearchIndex):
    docs = [
        SearchDocument(
            1, "Congruent Triangles",
            "Two triangles are congruent if their corresponding sides and angles are equal. SSS, SAS, ASA, and RHS are common congruence criteria.",
            ["triangles", "congruence", "criteria"], 1.0
        ),
        SearchDocument(
            2, "Similarity of Triangles",
            "Triangles are similar if their corresponding angles are equal and their corresponding sides are proportional. AA, SAS, and SSS are similarity criteria.",
            ["triangles", "similarity", "criteria"], 1.0
        ),
        SearchDocument(
            3, "Pythagoras Theorem",
            "In a right-angled triangle, the square of the hypotenuse is equal to the sum of the squares of the other two sides.",
            ["triangles", "pythagoras", "theorem"], 1.0
        ),
        SearchDocument(
            4, "Properties of Parallelograms",
            "Opposite sides of a parallelogram are equal and parallel. Opposite angles are equal. Diagonals bisect each other.",
            ["quadrilaterals", "parallelogram", "properties"], 1.0
        ),
        SearchDocument(
            5, "Area of a Triangle",
            "The area of a triangle is given by 1/2 × base × height. For Heron's formula, use the semi-perimeter.",
            ["triangles", "area", "heron"], 1.0
        ),
        SearchDocument(
            6, "Circle: Chord Properties",
            "A chord divides a circle into two segments. The perpendicular from the center to a chord bisects the chord.",
            ["circle", "chord", "properties"], 1.0
        ),
        SearchDocument(
            7, "Cyclic Quadrilaterals",
            "A quadrilateral is cyclic if all its vertices lie on a circle. Opposite angles of a cyclic quadrilateral sum to 180 degrees.",
            ["quadrilaterals", "cyclic", "circle"], 1.0
        ),
        SearchDocument(
            8, "Tangent to a Circle",
            "A tangent to a circle is perpendicular to the radius at the point of contact. The lengths of tangents from an external point are equal.",
            ["circle", "tangent", "radius"], 1.0
        ),
        SearchDocument(
            9, "Basic Constructions",
            "Geometric constructions include bisecting a segment, constructing perpendiculars, and drawing tangents to circles.",
            ["constructions", "geometry", "basic"], 1.0
        ),
        SearchDocument(
            10, "Angle Sum Property of Triangle",
            "The sum of the interior angles of a triangle is always 180 degrees.",
            ["triangles", "angles", "sum"], 1.0
        ),
        SearchDocument(
            11, "Midpoint Theorem",
            "The line joining the midpoints of two sides of a triangle is parallel to the third side and half its length.",
            ["triangles", "midpoint", "theorem"], 1.0
        ),
        SearchDocument(
            12, "Exterior Angle Theorem",
            "The exterior angle of a triangle is equal to the sum of the two opposite interior angles.",
            ["triangles", "angles", "exterior"], 1.0
        ),
        SearchDocument(
            13, "Centroid of a Triangle",
            "The centroid is the point of intersection of the medians of a triangle. It divides each median in a 2:1 ratio.",
            ["triangles", "centroid", "median"], 1.0
        ),
        SearchDocument(
            14, "Incenter and Incircle",
            "The incenter is the point where the angle bisectors meet. The incircle touches all sides of the triangle.",
            ["triangles", "incenter", "incircle"], 1.0
        ),
        SearchDocument(
            15, "Circumcenter and Circumcircle",
            "The circumcenter is the intersection of perpendicular bisectors of the sides. The circumcircle passes through all vertices.",
            ["triangles", "circumcenter", "circumcircle"], 1.0
        ),
        SearchDocument(
            16, "Orthocenter of a Triangle",
            "The orthocenter is the intersection of the altitudes of a triangle.",
            ["triangles", "orthocenter", "altitude"], 1.0
        ),
        SearchDocument(
            17, "Properties of Rectangles",
            "All angles in a rectangle are right angles. Opposite sides are equal and parallel. Diagonals are equal.",
            ["quadrilaterals", "rectangle", "properties"], 1.0
        ),
        SearchDocument(
            18, "Properties of Rhombus",
            "All sides of a rhombus are equal. Opposite angles are equal. Diagonals bisect at right angles.",
            ["quadrilaterals", "rhombus", "properties"], 1.0
        ),
        SearchDocument(
            19, "Properties of Square",
            "A square has all sides equal and all angles 90 degrees. Diagonals are equal and bisect at right angles.",
            ["quadrilaterals", "square", "properties"], 1.0
        ),
        SearchDocument(
            20, "Properties of Trapezium",
            "A trapezium has one pair of parallel sides. The non-parallel sides are called legs.",
            ["quadrilaterals", "trapezium", "properties"], 1.0
        ),
        SearchDocument(
            21, "Area of Parallelogram",
            "Area = base × height. Opposite sides are equal and parallel.",
            ["parallelogram", "area", "quadrilaterals"], 1.0
        ),
        SearchDocument(
            22, "Area of Circle",
            "The area of a circle is πr², where r is the radius.",
            ["circle", "area", "radius"], 1.0
        ),
        SearchDocument(
            23, "Perimeter of Circle",
            "The perimeter (circumference) of a circle is 2πr.",
            ["circle", "perimeter", "circumference"], 1.0
        ),
        SearchDocument(
            24, "Arc and Sector of Circle",
            "An arc is a part of the circumference. The area of a sector is (θ/360) × πr².",
            ["circle", "arc", "sector"], 1.0
        ),
        SearchDocument(
            25, "Locus in Geometry",
            "A locus is the set of points satisfying certain conditions, such as equidistant from a point or a line.",
            ["locus", "geometry", "points"], 1.0
        ),
        SearchDocument(
            26, "Angle Bisector Theorem",
            "The angle bisector divides the opposite side in the ratio of the adjacent sides.",
            ["triangles", "angle", "bisector"], 1.0
        ),
        SearchDocument(
            27, "Basic Proportionality Theorem",
            "If a line is drawn parallel to one side of a triangle, it divides the other two sides proportionally.",
            ["triangles", "proportionality", "theorem"], 1.0
        ),
        SearchDocument(
            28, "Intersecting Chords Theorem",
            "If two chords intersect inside a circle, the products of their segments are equal.",
            ["circle", "chord", "intersect"], 1.0
        ),
        SearchDocument(
            29, "Alternate Segment Theorem",
            "The angle between a tangent and a chord is equal to the angle in the alternate segment.",
            ["circle", "tangent", "segment"], 1.0
        ),
        SearchDocument(
            30, "Equal Chords and Arcs",
            "Equal chords of a circle subtend equal angles at the center and are equidistant from the center.",
            ["circle", "chord", "equal"], 1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)