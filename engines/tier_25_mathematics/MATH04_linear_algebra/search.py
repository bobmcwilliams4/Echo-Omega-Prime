import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Any, Optional

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
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.idf: Dict[str, float] = {}
        self.tf: Dict[int, Dict[str, float]] = defaultdict(dict)
        self.lock = threading.Lock()
        self._stats_cache: Optional[Dict[str, Any]] = None

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9_]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            token_counts = Counter(tokens)
            for token, count in token_counts.items():
                self.inverted_index[token][doc.id] = count
            self.tf[doc.id] = {token: count / len(tokens) for token, count in token_counts.items()}
            self._update_avg_doc_length()
            self._compute_idf()
            self._stats_cache = None

    def _update_avg_doc_length(self):
        total_length = sum(self.doc_lengths.values())
        num_docs = len(self.doc_lengths)
        self.avg_doc_length = total_length / num_docs if num_docs > 0 else 0.0

    def _compute_idf(self):
        N = len(self.documents)
        self.idf = {}
        for token in self.inverted_index:
            df = len(self.inverted_index[token])
            self.idf[token] = math.log(1 + (N - df + 0.5) / (df + 0.5))

    def _score_bm25(self, query_tokens: List[str], doc_id: int, k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        avgdl = self.avg_doc_length
        for token in query_tokens:
            if token not in self.inverted_index or doc_id not in self.inverted_index[token]:
                continue
            f = self.inverted_index[token][doc_id]
            idf = self.idf.get(token, 0.0)
            denom = f + k1 * (1 - b + b * doc_len / avgdl)
            score += idf * ((f * (k1 + 1)) / (denom + 1e-10))
        return score * doc.weight

    def _score_tfidf(self, query_tokens: List[str], doc_id: int) -> float:
        score = 0.0
        doc_tf = self.tf.get(doc_id, {})
        for token in query_tokens:
            tf = doc_tf.get(token, 0.0)
            idf = self.idf.get(token, 0.0)
            score += tf * idf
        return score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        doc_scores = {}
        for doc_id in self.documents:
            if use_tfidf:
                score = self._score_tfidf(query_tokens, doc_id)
            else:
                score = self._score_bm25(query_tokens, doc_id)
            if score > 0.0:
                doc_scores[doc_id] = score
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, content: str, query_tokens: List[str], max_length: int = 160) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            snippet = ' '.join(tokens[:max_length])
        else:
            start = max(positions[0] - 10, 0)
            end = min(start + max_length, len(tokens))
            snippet = ' '.join(tokens[start:end])
        return snippet.strip()

    def get_stats(self) -> Dict[str, Any]:
        if self._stats_cache is not None:
            return self._stats_cache
        stats = {
            'num_documents': len(self.documents),
            'avg_doc_length': self.avg_doc_length,
            'num_tokens': len(self.inverted_index),
            'idf_sample': {k: self.idf[k] for k in list(self.idf)[:10]},
        }
        self._stats_cache = stats
        return stats

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
        SearchDocument(1, "Vector Spaces", 
            "A vector space is a collection of vectors, which are objects that can be added together and multiplied by scalars.", 
            ["vector", "space", "definition"], 1.0),
        SearchDocument(2, "Linear Transformations", 
            "A linear transformation is a mapping between vector spaces that preserves vector addition and scalar multiplication.", 
            ["linear", "transformation", "mapping"], 1.0),
        SearchDocument(3, "Matrix Multiplication", 
            "Matrix multiplication is a binary operation that produces a matrix from two matrices. The number of columns in the first matrix must equal the number of rows in the second.", 
            ["matrix", "multiplication", "operation"], 1.0),
        SearchDocument(4, "Eigenvalues and Eigenvectors", 
            "Eigenvalues and eigenvectors are fundamental in linear algebra. They are used in analyzing linear transformations.", 
            ["eigenvalue", "eigenvector", "linear", "algebra"], 1.0),
        SearchDocument(5, "Determinants", 
            "The determinant is a scalar value that can be computed from the elements of a square matrix and encodes certain properties of the matrix.", 
            ["determinant", "matrix", "property"], 1.0),
        SearchDocument(6, "Rank of a Matrix", 
            "The rank of a matrix is the dimension of the vector space generated by its columns.", 
            ["rank", "matrix", "dimension"], 1.0),
        SearchDocument(7, "Systems of Linear Equations", 
            "A system of linear equations is a collection of one or more linear equations involving the same set of variables.", 
            ["system", "linear", "equation"], 1.0),
        SearchDocument(8, "Gaussian Elimination", 
            "Gaussian elimination is a method for solving systems of linear equations. It transforms the system's matrix into row echelon form.", 
            ["gaussian", "elimination", "row", "echelon"], 1.0),
        SearchDocument(9, "LU Decomposition", 
            "LU decomposition factors a matrix as the product of a lower triangular matrix and an upper triangular matrix.", 
            ["lu", "decomposition", "triangular"], 1.0),
        SearchDocument(10, "Orthogonality", 
            "Orthogonality refers to the concept of perpendicularity in vector spaces. Orthogonal vectors have zero dot product.", 
            ["orthogonality", "vector", "dot", "product"], 1.0),
        SearchDocument(11, "Inner Product Spaces", 
            "An inner product space is a vector space with an additional structure called an inner product.", 
            ["inner", "product", "space"], 1.0),
        SearchDocument(12, "Gram-Schmidt Process", 
            "The Gram-Schmidt process is an algorithm for orthonormalizing a set of vectors in an inner product space.", 
            ["gram-schmidt", "orthonormal", "algorithm"], 1.0),
        SearchDocument(13, "Change of Basis", 
            "Change of basis is the process of expressing vectors in terms of a different set of basis vectors.", 
            ["change", "basis", "vector"], 1.0),
        SearchDocument(14, "Linear Independence", 
            "Vectors are linearly independent if no vector in the set can be written as a linear combination of the others.", 
            ["linear", "independence", "combination"], 1.0),
        SearchDocument(15, "Subspaces", 
            "A subspace is a subset of a vector space that is itself a vector space under the same operations.", 
            ["subspace", "vector", "space"], 1.0),
        SearchDocument(16, "Null Space and Column Space", 
            "The null space of a matrix is the set of all solutions to the homogeneous equation Ax=0. The column space is the span of the matrix's columns.", 
            ["null", "column", "space", "matrix"], 1.0),
        SearchDocument(17, "Singular Value Decomposition", 
            "Singular value decomposition (SVD) is a factorization of a real or complex matrix.", 
            ["singular", "value", "decomposition", "svd"], 1.0),
        SearchDocument(18, "Projection", 
            "Projection is the operation of mapping a vector onto a subspace.", 
            ["projection", "vector", "subspace"], 1.0),
        SearchDocument(19, "Diagonalization", 
            "Diagonalization is the process of finding a diagonal matrix similar to a given matrix.", 
            ["diagonalization", "matrix", "similar"], 1.0),
        SearchDocument(20, "Linear Operators", 
            "A linear operator is a function that acts on elements of a vector space and preserves vector addition and scalar multiplication.", 
            ["linear", "operator", "function"], 1.0),
        SearchDocument(21, "Spectral Theorem", 
            "The spectral theorem states that every normal operator on a finite-dimensional inner product space is diagonalizable.", 
            ["spectral", "theorem", "operator"], 1.0),
        SearchDocument(22, "Jordan Canonical Form", 
            "Jordan canonical form is a special form of a matrix representing its generalized eigenvectors.", 
            ["jordan", "canonical", "form", "matrix"], 1.0),
        SearchDocument(23, "Trace of a Matrix", 
            "The trace of a matrix is the sum of its diagonal elements.", 
            ["trace", "matrix", "sum"], 1.0),
        SearchDocument(24, "Linear Algebra Applications", 
            "Linear algebra is used in computer graphics, engineering, physics, and statistics.", 
            ["application", "linear", "algebra"], 1.0),
        SearchDocument(25, "Basis and Dimension", 
            "A basis of a vector space is a set of linearly independent vectors that span the space. The dimension is the number of vectors in the basis.", 
            ["basis", "dimension", "vector"], 1.0),
        SearchDocument(26, "Row Reduction", 
            "Row reduction is a technique for simplifying matrices to solve linear equations.", 
            ["row", "reduction", "matrix"], 1.0),
        SearchDocument(27, "Matrix Inverse", 
            "The inverse of a matrix is a matrix that, when multiplied with the original, yields the identity matrix.", 
            ["inverse", "matrix", "identity"], 1.0),
        SearchDocument(28, "Cramer's Rule", 
            "Cramer's rule is a method for solving systems of linear equations using determinants.", 
            ["cramer", "rule", "determinant"], 1.0),
        SearchDocument(29, "Vector Norms", 
            "A vector norm is a function that assigns a length to each vector in a vector space.", 
            ["vector", "norm", "length"], 1.0),
        SearchDocument(30, "Affine Spaces", 
            "An affine space is a geometric structure that generalizes the properties of Euclidean spaces.", 
            ["affine", "space", "geometry"], 1.0),
    ]
    for doc in docs:
        index.add_document(doc)