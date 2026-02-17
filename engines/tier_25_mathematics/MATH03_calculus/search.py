import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

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

class SearchIndex:
    def __init__(self):
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.term_doc_freqs: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.term_freqs: Dict[str, int] = defaultdict(int)
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.total_docs: int = 0
        self.avg_doc_length: float = 0.0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._preseed_documents()

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            token_counts = Counter(tokens)
            for token, count in token_counts.items():
                self.term_doc_freqs[token][doc.id] = count
                self.term_freqs[token] += count
            for token in token_counts.keys():
                self.doc_freqs[token] += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        scores: Dict[str, float] = defaultdict(float)
        for doc_id, doc in self.documents.items():
            bm25_score = self._score_bm25(doc_id, query_tokens)
            tfidf_score = self._score_tfidf(doc_id, query_tokens)
            combined_score = bm25_score * 0.7 + tfidf_score * 0.3
            scores[doc_id] = combined_score * doc.weight
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            "total_docs": self.total_docs,
            "avg_doc_length": self.avg_doc_length,
            "unique_terms": len(self.doc_freqs),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: str, query_tokens: List[str], k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        for term in query_tokens:
            tf = self.term_doc_freqs.get(term, {}).get(doc_id, 0)
            idf = self._compute_idf(term)
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * doc_length / avg_dl)
            if denominator == 0:
                continue
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, doc_id: str, query_tokens: List[str]) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        for term in query_tokens:
            tf = self.term_doc_freqs.get(term, {}).get(doc_id, 0)
            if doc_length > 0:
                norm_tf = tf / doc_length
            else:
                norm_tf = 0.0
            idf = self._compute_idf(term)
            score += norm_tf * idf
        return score

    def _make_snippet(self, content: str, query_tokens: List[str], snippet_length: int = 160) -> str:
        tokens = self._tokenize(content)
        indices = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not indices:
            snippet = content[:snippet_length]
        else:
            start = max(indices[0] - 10, 0)
            end = min(indices[0] + 20, len(tokens))
            snippet_tokens = tokens[start:end]
            snippet = ' '.join(snippet_tokens)
            if len(snippet) > snippet_length:
                snippet = snippet[:snippet_length] + '...'
        return snippet

    def _preseed_documents(self):
        docs = [
            SearchDocument(
                id="calc01",
                title="Limits and Continuity",
                content="Limits are foundational in calculus, describing the behavior of functions as inputs approach a value. Continuity ensures no abrupt jumps in the graph of a function.",
                tags=["limits", "continuity", "calculus"]
            ),
            SearchDocument(
                id="calc02",
                title="Derivatives: Definition and Interpretation",
                content="The derivative measures the instantaneous rate of change of a function. It is defined as the limit of the difference quotient as the interval approaches zero.",
                tags=["derivatives", "calculus", "rate of change"]
            ),
            SearchDocument(
                id="calc03",
                title="Differentiation Rules",
                content="Common differentiation rules include the product rule, quotient rule, and chain rule. These allow computation of derivatives for composite functions.",
                tags=["differentiation", "rules", "calculus"]
            ),
            SearchDocument(
                id="calc04",
                title="Applications of Derivatives",
                content="Derivatives are used to find local maxima and minima, analyze concavity, and solve optimization problems in calculus.",
                tags=["applications", "derivatives", "optimization"]
            ),
            SearchDocument(
                id="calc05",
                title="Implicit Differentiation",
                content="Implicit differentiation is used when functions are defined implicitly, allowing calculation of derivatives without explicit formulas.",
                tags=["implicit differentiation", "calculus"]
            ),
            SearchDocument(
                id="calc06",
                title="Related Rates",
                content="Related rates problems involve finding the rate at which one quantity changes in relation to another, using derivatives.",
                tags=["related rates", "calculus", "derivatives"]
            ),
            SearchDocument(
                id="calc07",
                title="Mean Value Theorem",
                content="The Mean Value Theorem states that for a continuous and differentiable function, there exists a point where the instantaneous rate equals the average rate.",
                tags=["mean value theorem", "calculus", "theorems"]
            ),
            SearchDocument(
                id="calc08",
                title="Integrals: Definition and Interpretation",
                content="An integral represents the accumulation of quantities, such as area under a curve. The definite integral computes the net area between a function and the x-axis.",
                tags=["integrals", "calculus", "area"]
            ),
            SearchDocument(
                id="calc09",
                title="Fundamental Theorem of Calculus",
                content="The Fundamental Theorem of Calculus links differentiation and integration, showing that integration can be reversed by differentiation.",
                tags=["fundamental theorem", "calculus", "integration"]
            ),
            SearchDocument(
                id="calc10",
                title="Techniques of Integration",
                content="Integration techniques include substitution, integration by parts, partial fractions, and trigonometric substitution.",
                tags=["integration", "techniques", "calculus"]
            ),
            SearchDocument(
                id="calc11",
                title="Improper Integrals",
                content="Improper integrals extend the concept of integration to unbounded intervals or unbounded functions, requiring limits to evaluate.",
                tags=["improper integrals", "calculus"]
            ),
            SearchDocument(
                id="calc12",
                title="Applications of Integrals",
                content="Integrals are used to compute areas, volumes, work, and other physical quantities in calculus.",
                tags=["applications", "integrals", "calculus"]
            ),
            SearchDocument(
                id="calc13",
                title="Differential Equations",
                content="Differential equations involve functions and their derivatives, modeling dynamic systems in calculus and physics.",
                tags=["differential equations", "calculus", "modeling"]
            ),
            SearchDocument(
                id="calc14",
                title="Slope Fields",
                content="Slope fields provide a graphical representation of differential equations, showing possible solution curves.",
                tags=["slope fields", "differential equations", "calculus"]
            ),
            SearchDocument(
                id="calc15",
                title="Euler's Method",
                content="Euler's method is a numerical technique for approximating solutions to differential equations using tangent line steps.",
                tags=["euler's method", "numerical", "differential equations"]
            ),
            SearchDocument(
                id="calc16",
                title="Sequences and Series",
                content="Sequences are ordered lists of numbers, while series are sums of sequences. Convergence is a key concept in calculus.",
                tags=["sequences", "series", "convergence", "calculus"]
            ),
            SearchDocument(
                id="calc17",
                title="Taylor and Maclaurin Series",
                content="Taylor and Maclaurin series approximate functions using infinite sums of derivatives at a point.",
                tags=["taylor series", "maclaurin series", "calculus"]
            ),
            SearchDocument(
                id="calc18",
                title="Power Series",
                content="Power series represent functions as infinite sums of powers of a variable, with radius of convergence determining validity.",
                tags=["power series", "calculus"]
            ),
            SearchDocument(
                id="calc19",
                title="Convergence Tests",
                content="Convergence tests such as the ratio test, root test, and comparison test determine whether series converge.",
                tags=["convergence tests", "series", "calculus"]
            ),
            SearchDocument(
                id="calc20",
                title="Parametric Equations",
                content="Parametric equations express curves using parameters, allowing representation of complex motion and shapes.",
                tags=["parametric equations", "calculus", "curves"]
            ),
            SearchDocument(
                id="calc21",
                title="Polar Coordinates",
                content="Polar coordinates describe points in terms of radius and angle, useful for curves and areas in calculus.",
                tags=["polar coordinates", "calculus"]
            ),
            SearchDocument(
                id="calc22",
                title="Vector Calculus",
                content="Vector calculus extends calculus to vector fields, including gradient, divergence, and curl operations.",
                tags=["vector calculus", "fields", "calculus"]
            ),
            SearchDocument(
                id="calc23",
                title="Multivariable Functions",
                content="Multivariable functions depend on several variables, requiring partial derivatives and multiple integrals.",
                tags=["multivariable", "functions", "calculus"]
            ),
            SearchDocument(
                id="calc24",
                title="Partial Derivatives",
                content="Partial derivatives measure change with respect to one variable in multivariable functions.",
                tags=["partial derivatives", "multivariable", "calculus"]
            ),
            SearchDocument(
                id="calc25",
                title="Multiple Integrals",
                content="Multiple integrals compute volumes and other quantities in higher dimensions, including double and triple integrals.",
                tags=["multiple integrals", "calculus", "dimensions"]
            ),
            SearchDocument(
                id="calc26",
                title="Lagrange Multipliers",
                content="Lagrange multipliers are used for constrained optimization in multivariable calculus.",
                tags=["lagrange multipliers", "optimization", "calculus"]
            ),
            SearchDocument(
                id="calc27",
                title="Green's Theorem",
                content="Green's Theorem relates a line integral around a closed curve to a double integral over the region it encloses.",
                tags=["green's theorem", "integrals", "calculus"]
            ),
            SearchDocument(
                id="calc28",
                title="Stokes' Theorem",
                content="Stokes' Theorem generalizes Green's Theorem to higher dimensions, connecting surface integrals and curl.",
                tags=["stokes' theorem", "integrals", "calculus"]
            ),
            SearchDocument(
                id="calc29",
                title="Divergence Theorem",
                content="The Divergence Theorem connects the flux of a vector field through a surface to the divergence over the volume.",
                tags=["divergence theorem", "vector calculus"]
            ),
        ]
        for doc in docs:
            self.add_document(doc)

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
        return _search_index_instance