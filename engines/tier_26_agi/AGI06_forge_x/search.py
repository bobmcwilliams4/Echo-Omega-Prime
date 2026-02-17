import math
import re
import threading
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
        self.doc_freqs: Dict[str, int] = defaultdict(int)  # document frequency per term
        self.term_freqs: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))  # term_freqs[doc_id][term]
        self.doc_lengths: Dict[str, int] = {}  # length in tokens per document
        self.avg_doc_length: float = 0.0
        self.N: int = 0  # total number of documents
        self._idf_cache: Dict[str, float] = {}
        self._lock = threading.Lock()

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self.documents:
                # Remove old document data before adding new
                self._remove_document(doc.id)
            tokens = self._tokenize(doc.title + " " + doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.N = len(self.documents)
            tf_counter = Counter(tokens)
            self.term_freqs[doc.id] = dict(tf_counter)
            # Update document frequencies
            for term in tf_counter.keys():
                self.doc_freqs[term] += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self._idf_cache.clear()

    def _remove_document(self, doc_id: str):
        # Remove document data from index
        if doc_id not in self.documents:
            return
        old_terms = self.term_freqs.get(doc_id, {})
        for term in old_terms.keys():
            self.doc_freqs[term] -= 1
            if self.doc_freqs[term] <= 0:
                del self.doc_freqs[term]
        del self.term_freqs[doc_id]
        del self.doc_lengths[doc_id]
        del self.documents[doc_id]
        self.N = len(self.documents)
        self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
        self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        tokens = self._tokenize(query)
        if not tokens:
            return []
        scores: Dict[str, float] = defaultdict(float)
        idf_values = {term: self._compute_idf(term) for term in set(tokens)}
        query_tf = Counter(tokens)
        for doc_id, doc in self.documents.items():
            score = 0.0
            doc_tf = self.term_freqs.get(doc_id, {})
            doc_len = self.doc_lengths.get(doc_id, 0)
            for term in query_tf.keys():
                if term not in doc_tf:
                    continue
                tf = doc_tf[term]
                idf = idf_values.get(term, 0.0)
                score += self._score_bm25(tf, idf, doc_len)
            if score > 0:
                # Incorporate document weight
                scores[doc_id] = score * doc.weight
        # Sort by score descending
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, tokens)
            results.append(SearchResult(doc_id=doc_id, score=score, title=doc.title, snippet=snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                "num_documents": self.N,
                "avg_doc_length": self.avg_doc_length,
                "num_terms": len(self.doc_freqs),
            }

    def _tokenize(self, text: str) -> List[str]:
        # Lowercase, remove non-alphanumeric, split on whitespace
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
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

    def _score_bm25(self, tf: int, idf: float, doc_len: int) -> float:
        denom = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length) if self.avg_doc_length > 0 else tf + self.k1
        score = idf * tf * (self.k1 + 1) / denom if denom > 0 else 0.0
        return score

    def _make_snippet(self, content: str, query_terms: List[str], snippet_length: int = 150) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            start = 0
            while True:
                idx = content_lower.find(term, start)
                if idx == -1:
                    break
                positions.append(idx)
                start = idx + len(term)
        if not positions:
            snippet = content[:snippet_length]
            if len(content) > snippet_length:
                snippet += "..."
            return snippet
        start_pos = max(min(positions) - snippet_length // 4, 0)
        end_pos = min(start_pos + snippet_length, len(content))
        snippet = content[start_pos:end_pos]
        if start_pos > 0:
            snippet = "..." + snippet
        if end_pos < len(content):
            snippet += "..."
        return snippet


_singleton_instance: Optional[SearchIndex] = None
_singleton_lock = threading.Lock()


def get_search_index() -> SearchIndex:
    global _singleton_instance
    with _singleton_lock:
        if _singleton_instance is None:
            _singleton_instance = SearchIndex()
            _preseed_index(_singleton_instance)
        return _singleton_instance


def _preseed_index(index: SearchIndex):
    # 25+ domain documents matching the engine's doctrine topics
    docs = [
        SearchDocument(
            doc_id="doc001",
            title="Abstract Syntax Tree Manipulation Techniques",
            content=(
                "Abstract Syntax Tree (AST) manipulation is a core technique in code generation engines. "
                "It allows transformation and analysis of source code structures programmatically."
            ),
            tags=["AST", "code generation", "transformation"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc002",
            title="Template Engines for Automated Code Generation",
            content=(
                "Template engines facilitate code generation by separating code structure from logic, "
                "enabling reuse and maintainability."
            ),
            tags=["template engine", "code generation", "reuse"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc003",
            title="Gang of Four Design Patterns in Code Generation",
            content=(
                "The Gang of Four (GoF) design patterns provide reusable solutions to common design problems, "
                "essential in automated code generation to enforce best practices."
            ),
            tags=["GoF", "design patterns", "code generation"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc004",
            title="Applying SOLID Principles in Automated Code Generation",
            content=(
                "SOLID principles guide the design of maintainable and scalable code, "
                "and their application in automated code generation improves code quality."
            ),
            tags=["SOLID", "code quality", "automation"],
            weight=1.4,
        ),
        SearchDocument(
            doc_id="doc005",
            title="DRY, KISS, and YAGNI in Automated Refactoring",
            content=(
                "Automated refactoring tools implement principles like DRY (Don't Repeat Yourself), "
                "KISS (Keep It Simple Stupid), and YAGNI (You Aren't Gonna Need It) to optimize codebases."
            ),
            tags=["refactoring", "DRY", "KISS", "YAGNI"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc006",
            title="Refactoring Catalog: Extract Method",
            content=(
                "Extract Method is a refactoring technique that improves code readability and reuse "
                "by extracting code fragments into separate methods."
            ),
            tags=["refactoring", "extract method"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="doc007",
            title="Refactoring Catalog: Move Field",
            content=(
                "Move Field refactoring relocates fields to more appropriate classes, "
                "enhancing encapsulation and reducing coupling."
            ),
            tags=["refactoring", "move field"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="doc008",
            title="Refactoring Catalog: Inline Temp",
            content=(
                "Inline Temp replaces temporary variables with direct expressions, "
                "simplifying code and reducing unnecessary variables."
            ),
            tags=["refactoring", "inline temp"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="doc009",
            title="Refactoring Catalog: Rename Variable",
            content=(
                "Rename Variable improves code clarity by giving variables meaningful names, "
                "facilitating maintenance and understanding."
            ),
            tags=["refactoring", "rename variable"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="doc010",
            title="Unit Test Generation for Automated Code",
            content=(
                "Unit test generation automates the creation of tests that verify individual components, "
                "ensuring correctness and facilitating regression detection."
            ),
            tags=["testing", "unit tests", "automation"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc011",
            title="Integration Test Generation Strategies",
            content=(
                "Integration tests verify the interaction between components, "
                "and automated generation helps maintain system integrity."
            ),
            tags=["testing", "integration tests"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc012",
            title="Property-Based Testing in Code Generation",
            content=(
                "Property-based testing checks code behavior against properties or invariants, "
                "enabling broad and effective test coverage."
            ),
            tags=["testing", "property-based testing"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc013",
            title="Mutation Testing with PIT and Stryker",
            content=(
                "Mutation testing tools like PIT and Stryker introduce faults to evaluate test suite effectiveness."
            ),
            tags=["mutation testing", "PIT", "Stryker"],
            weight=1.4,
        ),
        SearchDocument(
            doc_id="doc014",
            title="Detecting Code Smells: Long Method",
            content=(
                "Long Method code smell indicates methods that are too lengthy and complex, "
                "suggesting refactoring opportunities."
            ),
            tags=["code smell", "long method"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc015",
            title="Detecting Code Smells: God Class",
            content=(
                "God Class is a code smell where a class has too many responsibilities, "
                "violating single responsibility principle."
            ),
            tags=["code smell", "god class"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc016",
            title="Detecting Code Smells: Feature Envy",
            content=(
                "Feature Envy occurs when a method accesses data of other classes excessively, "
                "indicating misplaced functionality."
            ),
            tags=["code smell", "feature envy"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc017",
            title="Cyclomatic Complexity: McCabe Metric",
            content=(
                "McCabe's cyclomatic complexity measures the number of linearly independent paths "
                "through a program's source code."
            ),
            tags=["metrics", "cyclomatic complexity", "McCabe"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc018",
            title="Halstead Metrics for Code Complexity",
            content=(
                "Halstead metrics quantify code complexity based on operators and operands, "
                "helping in maintainability assessment."
            ),
            tags=["metrics", "Halstead"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc019",
            title="Technical Debt Quantification with SQALE",
            content=(
                "SQALE method quantifies technical debt by evaluating code quality and maintainability."
            ),
            tags=["technical debt", "SQALE"],
            weight=1.4,
        ),
        SearchDocument(
            doc_id="doc020",
            title="SonarQube for Continuous Code Quality Analysis",
            content=(
                "SonarQube is a platform for continuous inspection of code quality, "
                "detecting bugs, vulnerabilities, and code smells."
            ),
            tags=["code quality", "SonarQube"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc021",
            title="Dependency Injection: Constructor Pattern",
            content=(
                "Constructor injection provides dependencies through class constructors, "
                "promoting immutability and testability."
            ),
            tags=["dependency injection", "constructor"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc022",
            title="Dependency Injection: Setter Pattern",
            content=(
                "Setter injection assigns dependencies via setter methods, allowing optional dependencies."
            ),
            tags=["dependency injection", "setter"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc023",
            title="Dependency Injection: Interface Pattern",
            content=(
                "Interface injection uses interfaces to provide dependencies, "
                "enabling decoupling and flexibility."
            ),
            tags=["dependency injection", "interface"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc024",
            title="Factory Pattern: Abstract Factory",
            content=(
                "Abstract Factory pattern creates families of related objects without specifying their concrete classes."
            ),
            tags=["factory pattern", "abstract factory"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc025",
            title="Factory Pattern: Builder",
            content=(
                "Builder pattern separates object construction from representation, "
                "allowing step-by-step creation."
            ),
            tags=["factory pattern", "builder"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc026",
            title="Factory Pattern: Prototype",
            content=(
                "Prototype pattern creates new objects by cloning existing instances, "
                "enhancing performance and flexibility."
            ),
            tags=["factory pattern", "prototype"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc027",
            title="Clean Architecture: Hexagonal Architecture",
            content=(
                "Hexagonal architecture emphasizes separation of concerns through ports and adapters, "
                "improving maintainability."
            ),
            tags=["clean architecture", "hexagonal", "ports & adapters"],
            weight=1.4,
        ),
        SearchDocument(
            doc_id="doc028",
            title="Clean Architecture: Onion Architecture",
            content=(
                "Onion architecture organizes code into concentric layers, "
                "enforcing dependency rules and separation."
            ),
            tags=["clean architecture", "onion"],
            weight=1.4,
        ),
        SearchDocument(
            doc_id="doc029",
            title="Clean Architecture: Ports and Adapters Pattern",
            content=(
                "Ports and Adapters pattern decouples application core from external systems, "
                "facilitating testing and evolution."
            ),
            tags=["clean architecture", "ports & adapters"],
            weight=1.3,
        ),
    ]
    for doc in docs:
        index.add_document(doc)