import math
import threading
import re
import heapq
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

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
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.doc_freqs[term] += 1
                self.inverted_index[term].add(doc.id)
            self.documents[doc.id] = doc
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, set()))
        scored_results = []
        for doc_id in candidate_docs:
            score_bm25 = self._score_bm25(doc_id, query_terms)
            score_tfidf = self._score_tfidf(doc_id, query_terms)
            doc = self.documents[doc_id]
            score = (score_bm25 * 0.7 + score_tfidf * 0.3) * doc.weight
            snippet = self._make_snippet(doc, query_terms)
            scored_results.append(SearchResult(doc_id, score, doc.title, snippet))
        top_results = heapq.nlargest(limit, scored_results, key=lambda r: r.score)
        return top_results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "num_documents": self.N,
                "avg_doc_length": self.avg_doc_length,
                "vocab_size": len(self.doc_freqs)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        text = re.sub(r'[\W_]+', ' ', text)
        tokens = text.split()
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

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths[doc_id]
        tf = self.term_freqs[doc_id]
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * (f * (self.k1 + 1)) / denom
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            tf_raw = tf.get(term, 0)
            if tf_raw == 0:
                continue
            tf_norm = tf_raw / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], max_len: int = 180) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:max_len]
            return snippet + "..." if len(content) > max_len else snippet
        start = max(positions[0] - 8, 0)
        end = min(start + 32, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(rf'\b({re.escape(term)})\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + "..." if len(snippet) > max_len else snippet

# Singleton factory for SearchIndex
_search_index_instance = None
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
        SearchDocument(1, "Bluebook Citation Format Overview",
            "The Bluebook prescribes citation formats for legal documents, including cases, statutes, and secondary sources. It emphasizes uniformity, abbreviation rules, and hierarchical authority.",
            ["bluebook", "citation", "format"], 1.0),
        SearchDocument(2, "ALWD Citation Manual Essentials",
            "The ALWD Guide to Legal Citation provides an alternative to the Bluebook, focusing on clarity and consistency in legal writing. It covers cases, statutes, and administrative materials.",
            ["alwd", "citation", "manual"], 1.0),
        SearchDocument(3, "Texas Citation Rules: Key Differences",
            "Texas citation rules diverge from the Bluebook in several respects, such as the use of 'v.' versus 'vs.', and unique abbreviations for Texas courts and statutes.",
            ["texas", "citation", "rules"], 1.0),
        SearchDocument(4, "Federal Citation Format: Statutes & Regulations",
            "Federal citation format covers the U.S. Code, Code of Federal Regulations, and federal case law. Proper citation ensures clarity and legal authority.",
            ["federal", "citation", "statutes", "regulations"], 1.0),
        SearchDocument(5, "Regulatory Citation Format: CFR and Federal Register",
            "Citations to the Code of Federal Regulations (C.F.R.) and the Federal Register must include title, section, and publication date for accuracy.",
            ["regulatory", "citation", "cfr", "federal register"], 1.0),
        SearchDocument(6, "Case Law Citation Hierarchies Explained",
            "Case law citations reflect court hierarchy, with Supreme Court decisions at the top, followed by appellate and trial courts. Proper hierarchy affects authority ranking.",
            ["case law", "hierarchy", "authority"], 1.1),
        SearchDocument(7, "Statutory Citation Assembly Techniques",
            "Statutory citations require precise assembly, including title, section, and year. Parallel citations may be necessary for statutes published in multiple sources.",
            ["statutory", "citation", "assembly"], 1.0),
        SearchDocument(8, "Citation Deduplication Strategies",
            "Deduplication removes redundant citations, ensuring each authority is cited only once per proposition. This improves readability and compliance.",
            ["deduplication", "citation"], 1.0),
        SearchDocument(9, "Authority Ranking by Court Level",
            "Ranking authorities by court level is essential: Supreme Court > Federal Appellate > Federal District > State Supreme > State Appellate > State Trial.",
            ["authority", "ranking", "court level"], 1.2),
        SearchDocument(10, "Citation String Normalization Methods",
            "Normalization standardizes citation strings, correcting abbreviations, spacing, and punctuation for consistency across documents.",
            ["normalization", "citation", "string"], 1.0),
        SearchDocument(11, "Handling Parallel Citations",
            "Parallel citations reference the same case in multiple reporters. Proper formatting and ordering are required by most citation manuals.",
            ["parallel", "citations"], 1.0),
        SearchDocument(12, "Recording Subsequent History",
            "Subsequent history, such as appeals or reversals, must be included in citations to provide full procedural context.",
            ["subsequent history", "citation"], 1.0),
        SearchDocument(13, "Pinpoint Citations (Jump Cites)",
            "Pinpoint citations direct the reader to a specific page or section within an authority, enhancing precision and credibility.",
            ["pinpoint", "citation", "jump cite"], 1.0),
        SearchDocument(14, "Signal Words Usage in Legal Citations",
            "Signal words (e.g., see, cf., but see) indicate the relationship between the cited authority and the proposition. Proper usage clarifies argument structure.",
            ["signal words", "citation"], 1.0),
        SearchDocument(15, "Parenthetical Construction in Citations",
            "Parentheticals provide explanatory information about the cited authority, such as holding, relevance, or procedural posture.",
            ["parenthetical", "citation"], 1.0),
        SearchDocument(16, "Citation Verification Techniques",
            "Verification ensures that citations are accurate, current, and properly formatted, often using tools like Shepard's or KeyCite.",
            ["verification", "citation"], 1.0),
        SearchDocument(17, "Cross-Reference Linking in Legal Documents",
            "Cross-references connect related citations within a document, improving navigation and supporting argument coherence.",
            ["cross-reference", "citation"], 1.0),
        SearchDocument(18, "Counting Citations per Authority",
            "Tracking the number of times each authority is cited helps identify key precedents and supports authority ranking.",
            ["citation count", "authority"], 1.0),
        SearchDocument(19, "Citation Freshness Scoring",
            "Citation freshness considers the recency of authorities, favoring more recent cases or statutes for certain legal arguments.",
            ["freshness", "citation", "scoring"], 1.0),
        SearchDocument(20, "Citation Relevance Ranking Algorithms",
            "Relevance ranking uses factors like authority, frequency, and context to prioritize citations in legal research and writing.",
            ["relevance", "ranking", "citation"], 1.0),
        SearchDocument(21, "Bluebook vs. ALWD: Comparative Analysis",
            "A comparative analysis of Bluebook and ALWD citation systems highlights differences in structure, abbreviations, and citation philosophy.",
            ["bluebook", "alwd", "comparison"], 1.0),
        SearchDocument(22, "Texas Greenbook: State-Specific Citation",
            "The Texas Greenbook supplements the Bluebook for Texas legal materials, providing unique rules for state cases and statutes.",
            ["texas", "greenbook", "citation"], 1.0),
        SearchDocument(23, "Federal Appellate Court Citation Conventions",
            "Federal appellate courts have specific citation conventions, including short forms, parallel citations, and procedural history.",
            ["federal", "appellate", "citation"], 1.0),
        SearchDocument(24, "Administrative Law Citation: Agency Decisions",
            "Citing administrative agency decisions requires agency name, docket number, and decision date, following Bluebook or ALWD guidance.",
            ["administrative", "agency", "citation"], 1.0),
        SearchDocument(25, "Legal Citation Tools and Automation",
            "Automation tools assist in citation formatting, verification, and deduplication, increasing efficiency and reducing errors.",
            ["automation", "citation", "tools"], 1.0),
        SearchDocument(26, "Parentheticals: Best Practices",
            "Best practices for parentheticals include brevity, clarity, and direct relevance to the cited proposition.",
            ["parenthetical", "best practices"], 1.0),
        SearchDocument(27, "Pinpoint Citation in Statutes",
            "Statutory pinpoint citations specify subsections or clauses, ensuring precise reference to statutory language.",
            ["pinpoint", "statute", "citation"], 1.0),
        SearchDocument(28, "Parallel Citations in State Courts",
            "Many state courts require parallel citations to regional and state reporters, following specific ordering conventions.",
            ["parallel", "state", "citation"], 1.0),
        SearchDocument(29, "Citation Normalization Algorithms",
            "Algorithms for citation normalization parse, standardize, and validate citation strings for consistency.",
            ["normalization", "algorithm", "citation"], 1.0),
        SearchDocument(30, "Citing Unpublished Opinions",
            "Unpublished opinions are cited with caution, noting their non-precedential status and following jurisdictional rules.",
            ["unpublished", "opinion", "citation"], 1.0),
    ]
    for doc in docs:
        index.add_document(doc)