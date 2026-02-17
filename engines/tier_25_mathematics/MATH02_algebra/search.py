import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# --- Data Classes ---

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

# --- Search Index ---

class SearchIndex:
    def __init__(self):
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_tokens: Dict[str, List[str]] = {}
        self.inverted_index: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.total_docs: int = 0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            self.documents[doc.id] = doc
            self.doc_tokens[doc.id] = tokens
            self.doc_lengths[doc.id] = len(tokens)
            for token in tokens:
                self.inverted_index[token][doc.id] = self.inverted_index[token].get(doc.id, 0) + 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        candidate_docs = set()
        for token in query_tokens:
            candidate_docs.update(self.inverted_index.get(token, {}).keys())
        scores: Dict[str, float] = {}
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_tokens)
            tfidf_score = self._score_tfidf(doc_id, query_tokens)
            doc = self.documents[doc_id]
            # Combine BM25 and TF-IDF (weighted sum, BM25 dominates)
            score = 0.7 * bm25_score + 0.3 * tfidf_score
            score *= doc.weight
            scores[doc_id] = score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> dict:
        return {
            "total_docs": self.total_docs,
            "avg_doc_length": self.avg_doc_length,
            "vocab_size": len(self.inverted_index)
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        text = re.sub(r'[^a-z0-9_+\-\^=]', ' ', text)
        tokens = text.split()
        return [t for t in tokens if t]

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = len(self.inverted_index.get(term, {}))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: str, query_tokens: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1
        doc_token_counts = Counter(self.doc_tokens[doc_id])
        for term in set(query_tokens):
            tf = doc_token_counts.get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            numerator = tf * (self._bm25_k1 + 1)
            denominator = tf + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / avg_dl)
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, doc_id: str, query_tokens: List[str]) -> float:
        score = 0.0
        doc_token_counts = Counter(self.doc_tokens[doc_id])
        doc_len = self.doc_lengths.get(doc_id, 1)
        for term in set(query_tokens):
            tf = doc_token_counts.get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str]) -> str:
        content = doc.content
        content_lower = content.lower()
        positions = []
        for qt in query_tokens:
            idx = content_lower.find(qt)
            if idx != -1:
                positions.append(idx)
        if positions:
            start = max(min(positions) - 30, 0)
            end = min(start + 120, len(content))
            snippet = content[start:end]
            if start > 0:
                snippet = "..." + snippet
            if end < len(content):
                snippet = snippet + "..."
            return snippet
        else:
            return content[:120] + ("..." if len(content) > 120 else "")

# --- Singleton Factory ---

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    if _search_index_instance is None:
        with _search_index_lock:
            if _search_index_instance is None:
                idx = SearchIndex()
                _preseed_documents(idx)
                _search_index_instance = idx
    return _search_index_instance

# --- Pre-seed Documents ---

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            id="1",
            title="Solving Linear Equations",
            content="A linear equation is an equation for a straight line. To solve ax + b = c, isolate x by subtracting b and dividing by a.",
            tags=["linear", "equation", "algebra"]
        ),
        SearchDocument(
            id="2",
            title="Quadratic Equations and the Quadratic Formula",
            content="Quadratic equations have the form ax^2 + bx + c = 0. The quadratic formula x = (-b ± sqrt(b^2 - 4ac)) / (2a) finds the roots.",
            tags=["quadratic", "formula", "algebra"]
        ),
        SearchDocument(
            id="3",
            title="Factoring Polynomials",
            content="Factoring expresses a polynomial as a product of its factors. For example, x^2 - 5x + 6 factors to (x - 2)(x - 3).",
            tags=["factoring", "polynomial", "algebra"]
        ),
        SearchDocument(
            id="4",
            title="The Distributive Property",
            content="The distributive property states that a(b + c) = ab + ac. It is used to expand expressions and solve equations.",
            tags=["distributive", "property", "algebra"]
        ),
        SearchDocument(
            id="5",
            title="Exponents and Powers",
            content="Exponents represent repeated multiplication. For example, x^3 = x * x * x. Laws of exponents include x^a * x^b = x^(a+b).",
            tags=["exponents", "powers", "algebra"]
        ),
        SearchDocument(
            id="6",
            title="Simplifying Algebraic Expressions",
            content="To simplify expressions, combine like terms and use the distributive property. For example, 2x + 3x = 5x.",
            tags=["simplifying", "expressions", "algebra"]
        ),
        SearchDocument(
            id="7",
            title="Systems of Linear Equations",
            content="A system of equations is two or more equations with the same variables. Solve using substitution, elimination, or graphing.",
            tags=["systems", "linear", "equations", "algebra"]
        ),
        SearchDocument(
            id="8",
            title="Inequalities and Their Graphs",
            content="An inequality compares two values. For example, x + 2 > 5. Solutions are shown on a number line or coordinate plane.",
            tags=["inequalities", "graphs", "algebra"]
        ),
        SearchDocument(
            id="9",
            title="Absolute Value Equations",
            content="The absolute value |x| is the distance from zero. To solve |x| = a, set x = a and x = -a.",
            tags=["absolute", "value", "equations", "algebra"]
        ),
        SearchDocument(
            id="10",
            title="Rational Expressions",
            content="A rational expression is a ratio of polynomials. Simplify by factoring numerator and denominator and canceling common factors.",
            tags=["rational", "expressions", "algebra"]
        ),
        SearchDocument(
            id="11",
            title="Radicals and Roots",
            content="A radical is an expression with a root, such as sqrt(x). Simplify by factoring out perfect squares.",
            tags=["radicals", "roots", "algebra"]
        ),
        SearchDocument(
            id="12",
            title="Completing the Square",
            content="Completing the square rewrites ax^2 + bx + c as a(x + h)^2 + k. Useful for solving quadratics and graphing parabolas.",
            tags=["completing", "square", "quadratic", "algebra"]
        ),
        SearchDocument(
            id="13",
            title="Functions and Function Notation",
            content="A function assigns each input exactly one output. Notation: f(x) = 2x + 3. Evaluate by substituting x.",
            tags=["functions", "notation", "algebra"]
        ),
        SearchDocument(
            id="14",
            title="Domain and Range",
            content="The domain is the set of possible inputs (x-values), and the range is the set of possible outputs (y-values) for a function.",
            tags=["domain", "range", "functions", "algebra"]
        ),
        SearchDocument(
            id="15",
            title="Slope and Intercept",
            content="The slope of a line is the ratio of rise to run. The y-intercept is where the line crosses the y-axis. y = mx + b.",
            tags=["slope", "intercept", "linear", "algebra"]
        ),
        SearchDocument(
            id="16",
            title="Graphing Linear Equations",
            content="To graph y = mx + b, plot the y-intercept and use the slope to find another point. Draw a straight line through the points.",
            tags=["graphing", "linear", "equations", "algebra"]
        ),
        SearchDocument(
            id="17",
            title="Parallel and Perpendicular Lines",
            content="Parallel lines have equal slopes. Perpendicular lines have slopes that are negative reciprocals.",
            tags=["parallel", "perpendicular", "lines", "algebra"]
        ),
        SearchDocument(
            id="18",
            title="Solving Word Problems with Algebra",
            content="Translate words into equations. Define variables, write equations, and solve for the unknowns.",
            tags=["word", "problems", "algebra"]
        ),
        SearchDocument(
            id="19",
            title="Inequalities with Absolute Value",
            content="To solve |x| < a, write -a < x < a. For |x| > a, write x < -a or x > a.",
            tags=["inequalities", "absolute", "value", "algebra"]
        ),
        SearchDocument(
            id="20",
            title="Polynomials: Degree and Leading Coefficient",
            content="The degree is the highest power of x. The leading coefficient is the coefficient of the highest degree term.",
            tags=["polynomials", "degree", "coefficient", "algebra"]
        ),
        SearchDocument(
            id="21",
            title="Synthetic Division",
            content="Synthetic division is a shortcut for dividing polynomials by linear divisors. It is faster than long division.",
            tags=["synthetic", "division", "polynomials", "algebra"]
        ),
        SearchDocument(
            id="22",
            title="The Zero Product Property",
            content="If ab = 0, then a = 0 or b = 0. Used to solve equations like (x - 2)(x + 3) = 0.",
            tags=["zero", "product", "property", "algebra"]
        ),
        SearchDocument(
            id="23",
            title="Rationalizing the Denominator",
            content="To rationalize, multiply numerator and denominator by a value that removes radicals from the denominator.",
            tags=["rationalizing", "denominator", "radicals", "algebra"]
        ),
        SearchDocument(
            id="24",
            title="Inverse Functions",
            content="The inverse of f(x) undoes the action of f. Swap x and y and solve for y to find the inverse.",
            tags=["inverse", "functions", "algebra"]
        ),
        SearchDocument(
            id="25",
            title="Exponential Growth and Decay",
            content="Exponential functions have the form y = ab^x. Growth occurs when b > 1, decay when 0 < b < 1.",
            tags=["exponential", "growth", "decay", "algebra"]
        ),
        SearchDocument(
            id="26",
            title="Logarithms and Their Properties",
            content="A logarithm is the inverse of an exponential. log_b(a) answers the question: b to what power equals a?",
            tags=["logarithms", "properties", "algebra"]
        ),
        SearchDocument(
            id="27",
            title="Solving Simultaneous Equations",
            content="Simultaneous equations are solved by finding values that satisfy all equations at once.",
            tags=["simultaneous", "equations", "algebra"]
        ),
        SearchDocument(
            id="28",
            title="Piecewise Functions",
            content="A piecewise function is defined by different expressions for different intervals of the domain.",
            tags=["piecewise", "functions", "algebra"]
        ),
        SearchDocument(
            id="29",
            title="The Binomial Theorem",
            content="The binomial theorem expands (a + b)^n using binomial coefficients. Useful for expanding powers.",
            tags=["binomial", "theorem", "algebra"]
        ),
        SearchDocument(
            id="30",
            title="Graphing Quadratic Functions",
            content="The graph of y = ax^2 + bx + c is a parabola. The vertex is at x = -b/(2a).",
            tags=["graphing", "quadratic", "functions", "algebra"]
        ),
    ]
    for doc in docs:
        idx.add_document(doc)