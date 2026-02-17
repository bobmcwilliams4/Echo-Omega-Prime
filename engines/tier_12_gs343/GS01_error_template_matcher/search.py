import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

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
        self._documents: Dict[int, SearchDocument] = {}
        self._doc_tokens: Dict[int, List[str]] = {}
        self._inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self._term_freqs: Dict[int, Counter] = {}
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_length: float = 0.0
        self._idf_cache: Dict[str, float] = {}
        self._lock = threading.Lock()
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75
        self._total_docs = 0
        self._total_length = 0

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            self._documents[doc.id] = doc
            self._doc_tokens[doc.id] = tokens
            tf = Counter(tokens)
            self._term_freqs[doc.id] = tf
            doc_length = len(tokens)
            self._doc_lengths[doc.id] = doc_length
            self._total_docs += 1
            self._total_length += doc_length
            for token in set(tokens):
                self._inverted_index[token].add(doc.id)
            self._avg_doc_length = self._total_length / self._total_docs if self._total_docs else 0.0
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
        candidate_docs = set()
        for token in query_tokens:
            candidate_docs.update(self._inverted_index.get(token, set()))
        scored: List[Tuple[int, float]] = []
        for doc_id in candidate_docs:
            if use_tfidf:
                score = self._score_tfidf(doc_id, query_tokens)
            else:
                score = self._score_bm25(doc_id, query_tokens)
            if score > 0:
                scored.append((doc_id, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored[:limit]:
            doc = self._documents[doc_id]
            snippet = self._make_snippet(doc, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                "total_docs": self._total_docs,
                "avg_doc_length": self._avg_doc_length,
                "unique_terms": len(self._inverted_index),
            }

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r"\b[a-zA-Z0-9_#\.\-]{2,}\b", text.lower())
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = len(self._inverted_index.get(term, []))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self._total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_tokens: List[str]) -> float:
        tf = self._term_freqs[doc_id]
        doc_length = self._doc_lengths[doc_id]
        avg_dl = self._avg_doc_length or 1.0
        score = 0.0
        doc = self._documents[doc_id]
        for term in query_tokens:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_length / avg_dl)
            score += idf * (f * (self._bm25_k1 + 1)) / denom
        score *= doc.weight
        return score

    def _score_tfidf(self, doc_id: int, query_tokens: List[str]) -> float:
        tf = self._term_freqs[doc_id]
        doc_length = self._doc_lengths[doc_id]
        score = 0.0
        doc = self._documents[doc_id]
        for term in query_tokens:
            tf_raw = tf.get(term, 0)
            if tf_raw == 0:
                continue
            tf_norm = tf_raw / doc_length
            idf = self._compute_idf(term)
            score += tf_norm * idf
        score *= doc.weight
        return score

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], maxlen: int = 180) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            snippet = content[:maxlen] + ("..." if len(content) > maxlen else "")
            return snippet
        start = max(positions[0] - 5, 0)
        end = min(positions[0] + 15, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        if len(snippet) > maxlen:
            snippet = snippet[:maxlen] + "..."
        return snippet

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

# --- Preseed Domain Documents ---

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Regex Error Pattern Extraction",
            "Learn how to extract error patterns using regular expressions. Useful for parsing stack traces and matching error templates.",
            ["regex", "pattern", "error", "stacktrace", "template"],
            1.0
        ),
        SearchDocument(
            2,
            "Fuzzy String Matching in Error Classification",
            "Apply fuzzy string matching algorithms (Levenshtein, Jaro-Winkler) to classify errors that do not match templates exactly.",
            ["fuzzy", "string", "matching", "classification", "levenshtein"],
            1.0
        ),
        SearchDocument(
            3,
            "Error Category Taxonomy",
            "A taxonomy of error categories: syntax, runtime, network, authentication, configuration, resource, timeout, permission.",
            ["taxonomy", "category", "classification", "error"],
            1.0
        ),
        SearchDocument(
            4,
            "Syntax Error Pattern Matching",
            "Detect and classify syntax errors in Python, JavaScript, and other languages using pattern templates.",
            ["syntax", "pattern", "matching", "python", "javascript"],
            1.0
        ),
        SearchDocument(
            5,
            "Runtime Error Pattern Matching",
            "Identify runtime errors such as TypeError, AttributeError, and KeyError using template-based matching.",
            ["runtime", "pattern", "typeerror", "attributeerror", "keyerror"],
            1.0
        ),
        SearchDocument(
            6,
            "Network Error Pattern Classification",
            "Classify network errors including timeouts, DNS failures, and HTTP 4xx/5xx responses.",
            ["network", "timeout", "dns", "http", "classification"],
            1.0
        ),
        SearchDocument(
            7,
            "Authentication Error Pattern Matching",
            "Match authentication errors such as invalid credentials, expired tokens, and permission denied.",
            ["authentication", "invalid", "token", "permission", "error"],
            1.0
        ),
        SearchDocument(
            8,
            "Configuration Error Pattern Matching",
            "Detect configuration errors: missing environment variables, invalid config files, and misconfigured dependencies.",
            ["configuration", "env", "file", "dependency", "error"],
            1.0
        ),
        SearchDocument(
            9,
            "Resource Dependency Error Pattern Matching",
            "Match errors related to missing or unavailable resources and dependencies.",
            ["resource", "dependency", "missing", "unavailable", "error"],
            1.0
        ),
        SearchDocument(
            10,
            "Timeout Error Pattern Matching",
            "Identify timeout errors in network requests, database queries, and external API calls.",
            ["timeout", "network", "database", "api", "error"],
            1.0
        ),
        SearchDocument(
            11,
            "Permission Error Pattern Matching",
            "Classify permission errors such as EACCES, PermissionError, and access denied messages.",
            ["permission", "eacces", "access", "denied", "error"],
            1.0
        ),
        SearchDocument(
            12,
            "Stack Trace Parsing and Error Fingerprinting",
            "Parse stack traces to extract error fingerprints for template matching and error correlation.",
            ["stacktrace", "parsing", "fingerprint", "template", "correlation"],
            1.0
        ),
        SearchDocument(
            13,
            "Template Creation from Novel Errors",
            "Automatically create new error templates from previously unseen error messages.",
            ["template", "creation", "novel", "error", "automatic"],
            1.0
        ),
        SearchDocument(
            14,
            "Template Confidence Scoring",
            "Score the confidence of template matches using statistical and heuristic methods.",
            ["template", "confidence", "scoring", "heuristic", "statistical"],
            1.0
        ),
        SearchDocument(
            15,
            "Error Chain Analysis and Root Cause Extraction",
            "Analyze error chains to extract the root cause and improve classification accuracy.",
            ["chain", "analysis", "root", "cause", "classification"],
            1.0
        ),
        SearchDocument(
            16,
            "Python Error Patterns: ImportError",
            "Recognize ImportError patterns in Python stack traces and error logs.",
            ["python", "importerror", "stacktrace", "pattern", "error"],
            1.0
        ),
        SearchDocument(
            17,
            "Python Error Patterns: AttributeError",
            "Detect AttributeError in Python applications using regex and template matching.",
            ["python", "attributeerror", "regex", "template", "error"],
            1.0
        ),
        SearchDocument(
            18,
            "Python Error Patterns: TypeError",
            "Classify TypeError in Python by matching against known error message templates.",
            ["python", "typeerror", "template", "classification", "error"],
            1.0
        ),
        SearchDocument(
            19,
            "Python Error Patterns: KeyError",
            "Identify KeyError in Python logs and suggest possible auto-fixes.",
            ["python", "keyerror", "logs", "autofix", "error"],
            1.0
        ),
        SearchDocument(
            20,
            "HTTP Error Patterns: 4xx and 5xx",
            "Match HTTP 4xx and 5xx error responses using pattern templates for classification.",
            ["http", "4xx", "5xx", "pattern", "classification"],
            1.0
        ),
        SearchDocument(
            21,
            "Database Error Patterns",
            "Detect database errors such as connection failures, SQL syntax errors, and constraint violations.",
            ["database", "connection", "sql", "syntax", "violation"],
            1.0
        ),
        SearchDocument(
            22,
            "Cloudflare Worker Error Patterns",
            "Classify Cloudflare Worker errors including runtime exceptions and deployment issues.",
            ["cloudflare", "worker", "runtime", "deployment", "error"],
            1.0
        ),
        SearchDocument(
            23,
            "Node.js Error Patterns",
            "Identify Node.js errors such as EADDRINUSE, ENOENT, and uncaught exceptions.",
            ["nodejs", "eaddrinuse", "enoent", "exception", "error"],
            1.0
        ),
        SearchDocument(
            24,
            "Template Versioning and Deprecation",
            "Manage template versions and handle deprecation for evolving error patterns.",
            ["template", "versioning", "deprecation", "error", "pattern"],
            1.0
        ),
        SearchDocument(
            25,
            "Error Frequency Analysis",
            "Analyze error frequency to prioritize template improvements and auto-fix suggestions.",
            ["frequency", "analysis", "template", "autofix", "error"],
            1.0
        ),
        SearchDocument(
            26,
            "Error Correlation Detection",
            "Detect correlations between error patterns to identify systemic issues.",
            ["correlation", "detection", "pattern", "systemic", "error"],
            1.0
        ),
        SearchDocument(
            27,
            "Auto-Fix Suggestion Templates",
            "Generate auto-fix suggestions based on matched error templates and context.",
            ["autofix", "suggestion", "template", "context", "error"],
            1.0
        ),
        SearchDocument(
            28,
            "Advanced Fuzzy Matching for Error Templates",
            "Use advanced fuzzy matching techniques to improve template recall for noisy logs.",
            ["fuzzy", "matching", "template", "recall", "logs"],
            1.0
        ),
        SearchDocument(
            29,
            "Error Pattern Extraction from Logs",
            "Extract error patterns from unstructured logs using regex and NLP techniques.",
            ["extraction", "logs", "regex", "nlp", "pattern"],
            1.0
        ),
        SearchDocument(
            30,
            "Heuristic Scoring in Error Template Matching",
            "Apply heuristic scoring to rank error template matches by likelihood.",
            ["heuristic", "scoring", "template", "ranking", "likelihood"],
            1.0
        ),
        SearchDocument(
            31,
            "Multi-Language Error Pattern Support",
            "Support error pattern matching for multiple languages: Python, Node.js, Go, Java.",
            ["multi-language", "pattern", "python", "nodejs", "java"],
            1.0
        ),
        SearchDocument(
            32,
            "Error Template Deprecation Strategy",
            "Develop strategies for deprecating outdated error templates while maintaining accuracy.",
            ["deprecation", "strategy", "template", "outdated", "accuracy"],
            1.0
        ),
        SearchDocument(
            33,
            "Stack Trace Fingerprinting Techniques",
            "Techniques for generating fingerprints from stack traces for error deduplication.",
            ["stacktrace", "fingerprinting", "deduplication", "error", "technique"],
            1.0
        ),
        SearchDocument(
            34,
            "Error Chain Visualization",
            "Visualize error chains to assist in root cause analysis and debugging.",
            ["visualization", "chain", "root", "cause", "debugging"],
            1.0
        ),
        SearchDocument(
            35,
            "Machine Learning for Error Template Matching",
            "Apply machine learning models to improve error template matching accuracy.",
            ["machine-learning", "template", "matching", "accuracy", "error"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)