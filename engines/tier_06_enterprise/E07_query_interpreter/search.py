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
    def __init__(self):
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.total_terms: int = 0
        self.lock = threading.Lock()
        self.avg_doc_length: float = 0.0
        self.k1 = 1.5
        self.b = 0.75
        self.idf_cache: Dict[str, float] = {}
        self._preseed_documents()

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_terms += len(tokens)
            term_counts = Counter(tokens)
            for term, freq in term_counts.items():
                self.term_freqs[doc.id][term] = freq
                self.term_doc_freq[term] += 1
            self._update_avg_doc_length()
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        tokens = self._tokenize(query)
        if not tokens:
            return []
        scores: Dict[str, float] = defaultdict(float)
        for doc_id, doc in self.documents.items():
            bm25_score = self._score_bm25(doc_id, tokens)
            tfidf_score = self._score_tfidf(doc_id, tokens)
            combined_score = bm25_score * 0.7 + tfidf_score * 0.3
            combined_score *= doc.weight
            if combined_score > 0:
                scores[doc_id] = combined_score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._snippet(doc.content, tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "documents": len(self.documents),
                "avg_doc_length": self.avg_doc_length,
                "unique_terms": len(self.term_doc_freq),
                "total_terms": self.total_terms
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        N = len(self.documents)
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: str, query_terms: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1
        for term in query_terms:
            idf = self._compute_idf(term)
            freq = self.term_freqs[doc_id].get(term, 0)
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (1 - self.b + self.b * doc_len / avg_dl)
            if denominator == 0:
                continue
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, doc_id: str, query_terms: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        if doc_len == 0:
            return 0.0
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0) / doc_len
            idf = self._compute_idf(term)
            score += tf * idf
        return score

    def _update_avg_doc_length(self):
        if self.documents:
            self.avg_doc_length = sum(self.doc_lengths.values()) / len(self.documents)
        else:
            self.avg_doc_length = 0.0

    def _snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:window])
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return snippet

    def _preseed_documents(self):
        docs = [
            SearchDocument(
                "E07-001",
                "Query Language Syntax",
                "The E07 query interpreter supports a domain-specific language for expressing search queries. Syntax includes logical operators, field filters, and range expressions.",
                ["syntax", "query", "dsl", "operators"],
                1.0
            ),
            SearchDocument(
                "E07-002",
                "Logical Operators",
                "E07 query engine recognizes AND, OR, and NOT operators for combining search conditions. Parentheses can be used to group expressions and control precedence.",
                ["operators", "logic", "precedence"],
                1.0
            ),
            SearchDocument(
                "E07-003",
                "Field Filtering",
                "Users can filter queries by specific fields such as title, tags, or content. Field filters use the format field:value for targeted searches.",
                ["fields", "filter", "targeted"],
                1.0
            ),
            SearchDocument(
                "E07-004",
                "Range Expressions",
                "Range queries allow users to specify numeric or date intervals. Supported syntax includes [start TO end] and comparison operators like >, <, >=, <=.",
                ["range", "interval", "numeric", "date"],
                1.0
            ),
            SearchDocument(
                "E07-005",
                "Tokenization Process",
                "The interpreter tokenizes input queries using whitespace and punctuation delimiters. Token normalization includes lowercasing and stemming for improved recall.",
                ["tokenization", "normalization", "stemming"],
                1.0
            ),
            SearchDocument(
                "E07-006",
                "Stopword Removal",
                "Common stopwords are removed from queries to reduce noise and improve relevance. The stopword list is customizable per domain requirements.",
                ["stopwords", "noise", "relevance"],
                1.0
            ),
            SearchDocument(
                "E07-007",
                "Query Expansion",
                "E07 supports query expansion techniques such as synonym substitution and spelling correction to enhance search coverage.",
                ["expansion", "synonyms", "spelling"],
                1.0
            ),
            SearchDocument(
                "E07-008",
                "BM25 Ranking",
                "Documents are ranked using the BM25 algorithm with k1=1.5 and b=0.75. BM25 considers term frequency, document length, and inverse document frequency.",
                ["bm25", "ranking", "algorithm"],
                1.0
            ),
            SearchDocument(
                "E07-009",
                "TF-IDF Scoring",
                "TF-IDF is used to compute document relevance based on term frequency and inverse document frequency. Normalization ensures fair scoring across documents.",
                ["tf-idf", "scoring", "relevance"],
                1.0
            ),
            SearchDocument(
                "E07-010",
                "Document Indexing",
                "Documents are indexed by unique identifiers, titles, content, tags, and weights. Indexing supports fast retrieval and efficient ranking.",
                ["indexing", "retrieval", "ranking"],
                1.0
            ),
            SearchDocument(
                "E07-011",
                "Query Interpretation",
                "The interpreter parses user queries, resolves operators, and constructs executable search plans. Interpretation handles ambiguity and resolves conflicts.",
                ["interpretation", "parsing", "ambiguity"],
                1.0
            ),
            SearchDocument(
                "E07-012",
                "Search Results",
                "Search results include document ID, score, title, and content snippet. Results are ranked and limited according to user preferences.",
                ["results", "ranking", "snippet"],
                1.0
            ),
            SearchDocument(
                "E07-013",
                "Tag-Based Filtering",
                "Documents can be filtered by tags for domain-specific searches. Tag filters are case-insensitive and support partial matches.",
                ["tags", "filtering", "domain"],
                1.0
            ),
            SearchDocument(
                "E07-014",
                "Weighting Documents",
                "Documents can be assigned weights to influence ranking. Higher weights increase document visibility in search results.",
                ["weights", "ranking", "visibility"],
                1.0
            ),
            SearchDocument(
                "E07-015",
                "Custom Scoring Functions",
                "E07 allows custom scoring functions to be plugged in for specialized ranking requirements. Scoring functions can combine BM25, TF-IDF, and domain heuristics.",
                ["scoring", "custom", "heuristics"],
                1.0
            ),
            SearchDocument(
                "E07-016",
                "Index Statistics",
                "Index statistics include document count, average document length, unique term count, and total term frequency. Statistics are used for tuning ranking algorithms.",
                ["statistics", "index", "tuning"],
                1.0
            ),
            SearchDocument(
                "E07-017",
                "Query Caching",
                "Frequently executed queries are cached for performance. Cache invalidation occurs when documents are added or updated.",
                ["caching", "performance", "invalidation"],
                1.0
            ),
            SearchDocument(
                "E07-018",
                "Concurrency Control",
                "The search index uses locks to ensure thread-safe document addition and query execution. Concurrency control prevents race conditions.",
                ["concurrency", "thread-safe", "locks"],
                1.0
            ),
            SearchDocument(
                "E07-019",
                "Field Boosting",
                "Field boosting allows certain fields (e.g., title) to have higher impact on ranking. Boost factors are configurable per field.",
                ["boosting", "fields", "ranking"],
                1.0
            ),
            SearchDocument(
                "E07-020",
                "Phrase Search",
                "E07 supports phrase search using quoted expressions. Phrase matching requires contiguous terms in documents.",
                ["phrase", "search", "quoted"],
                1.0
            ),
            SearchDocument(
                "E07-021",
                "Wildcard Queries",
                "Wildcard queries use * and ? for partial term matching. Wildcards are supported in field filters and general search.",
                ["wildcard", "partial", "matching"],
                1.0
            ),
            SearchDocument(
                "E07-022",
                "Fuzzy Search",
                "Fuzzy search allows approximate term matching based on edit distance. Useful for handling typos and variant spellings.",
                ["fuzzy", "edit-distance", "approximate"],
                1.0
            ),
            SearchDocument(
                "E07-023",
                "Multi-Field Queries",
                "Queries can target multiple fields simultaneously. Field-specific boosts and filters enable complex search scenarios.",
                ["multi-field", "boost", "complex"],
                1.0
            ),
            SearchDocument(
                "E07-024",
                "Result Pagination",
                "Search results support pagination with offset and limit parameters. Pagination enables browsing large result sets efficiently.",
                ["pagination", "offset", "limit"],
                1.0
            ),
            SearchDocument(
                "E07-025",
                "Domain Adaptation",
                "E07 query interpreter can be adapted to different domains via configurable tokenization, stopwords, and ranking heuristics.",
                ["domain", "adaptation", "configurable"],
                1.0
            ),
            SearchDocument(
                "E07-026",
                "Query Logging",
                "All queries are logged for analytics and debugging. Logs include query text, execution time, and result statistics.",
                ["logging", "analytics", "debugging"],
                1.0
            ),
            SearchDocument(
                "E07-027",
                "Error Handling",
                "The interpreter provides robust error handling for malformed queries, missing fields, and unsupported operators.",
                ["error", "handling", "robust"],
                1.0
            ),
            SearchDocument(
                "E07-028",
                "Security Considerations",
                "E07 implements input validation and sanitization to prevent injection attacks. Security is enforced at all query processing stages.",
                ["security", "validation", "sanitization"],
                1.0
            ),
            SearchDocument(
                "E07-029",
                "Extensibility",
                "The engine is extensible via plugin interfaces for custom tokenization, scoring, and result formatting.",
                ["extensibility", "plugin", "custom"],
                1.0
            ),
            SearchDocument(
                "E07-030",
                "Integration APIs",
                "E07 provides REST and Python APIs for integration with external systems. API endpoints support search, indexing, and statistics.",
                ["api", "integration", "rest", "python"],
                1.0
            ),
        ]
        for doc in docs:
            self.add_document(doc)

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    if _search_index_instance is None:
        with _search_index_lock:
            if _search_index_instance is None:
                _search_index_instance = SearchIndex()
    return _search_index_instance