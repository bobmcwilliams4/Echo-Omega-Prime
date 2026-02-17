import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# --- Data Classes ---

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

# --- Search Index ---

class SearchIndex:
    def __init__(self):
        self._documents: Dict[str, SearchDocument] = {}
        self._doc_tokens: Dict[str, List[str]] = {}
        self._inverted_index: Dict[str, Dict[str, int]] = defaultdict(dict)
        self._doc_lengths: Dict[str, int] = {}
        self._avg_doc_length: float = 0.0
        self._idf_cache: Dict[str, float] = {}
        self._lock = threading.Lock()
        self._total_docs = 0
        self._doc_titles: Dict[str, str] = {}
        self._doc_contents: Dict[str, str] = {}
        self._doc_tags: Dict[str, List[str]] = {}
        self._doc_weights: Dict[str, float] = {}
        self._tf_cache: Dict[Tuple[str, str], float] = {}

    # --- Tokenization ---
    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    # --- Add Document ---
    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return  # No duplicate IDs
            tokens = self._tokenize(doc.title + ' ' + doc.content)
            self._documents[doc.id] = doc
            self._doc_tokens[doc.id] = tokens
            self._doc_lengths[doc.id] = len(tokens)
            self._doc_titles[doc.id] = doc.title
            self._doc_contents[doc.id] = doc.content
            self._doc_tags[doc.id] = doc.tags
            self._doc_weights[doc.id] = doc.weight
            tf = Counter(tokens)
            for term, freq in tf.items():
                self._inverted_index[term][doc.id] = freq
            self._total_docs += 1
            self._avg_doc_length = sum(self._doc_lengths.values()) / self._total_docs
            self._idf_cache.clear()
            self._tf_cache.clear()

    # --- Compute IDF ---
    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        N = self._total_docs
        df = len(self._inverted_index.get(term, {}))
        # Add 1 to numerator and denominator for smoothing
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    # --- Compute TF (Normalized) ---
    def _compute_tf(self, term: str, doc_id: str) -> float:
        key = (term, doc_id)
        if key in self._tf_cache:
            return self._tf_cache[key]
        tokens = self._doc_tokens.get(doc_id, [])
        tf = tokens.count(term)
        norm_tf = tf / len(tokens) if tokens else 0.0
        self._tf_cache[key] = norm_tf
        return norm_tf

    # --- BM25 Scoring ---
    def _score_bm25(self, query_terms: List[str], doc_id: str, k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc_len = self._doc_lengths.get(doc_id, 0)
        avg_dl = self._avg_doc_length if self._avg_doc_length > 0 else 1.0
        weight = self._doc_weights.get(doc_id, 1.0)
        for term in query_terms:
            f = self._inverted_index.get(term, {}).get(doc_id, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + k1 * (1 - b + b * doc_len / avg_dl)
            score += idf * ((f * (k1 + 1)) / denom)
        return score * weight

    # --- TF-IDF Scoring ---
    def _score_tfidf(self, query_terms: List[str], doc_id: str) -> float:
        score = 0.0
        weight = self._doc_weights.get(doc_id, 1.0)
        for term in query_terms:
            tf = self._compute_tf(term, doc_id)
            idf = self._compute_idf(term)
            score += tf * idf
        return score * weight

    # --- Snippet Extraction ---
    def _extract_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:window]) + ('...' if len(tokens) > window else '')
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet = ' '.join(tokens[start:end])
        if start > 0:
            snippet = '...' + snippet
        if end < len(tokens):
            snippet = snippet + '...'
        return snippet

    # --- Search ---
    def search(self, query: str, limit: int = 10, method: str = 'bm25') -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self._inverted_index.get(term, {}).keys())
        scored = []
        for doc_id in candidate_docs:
            if method == 'bm25':
                score = self._score_bm25(query_terms, doc_id)
            elif method == 'tfidf':
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                title = self._doc_titles.get(doc_id, '')
                content = self._doc_contents.get(doc_id, '')
                snippet = self._extract_snippet(content, query_terms)
                scored.append(SearchResult(doc_id, score, title, snippet))
        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:limit]

    # --- Stats ---
    def get_stats(self) -> Dict[str, int]:
        return {
            'documents': self._total_docs,
            'unique_terms': len(self._inverted_index),
            'avg_doc_length': int(self._avg_doc_length)
        }

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

# --- Pre-seed Documents ---

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            "D1",
            "Multi-Domain Conflict Resolution Framework",
            "This document outlines the framework for resolving conflicts across regulatory, legal, and operational domains, emphasizing weighted confidence aggregation and cross-reference validation.",
            ["conflict", "multi-domain", "framework"],
            1.2
        ),
        SearchDocument(
            "D2",
            "Weighted Confidence Aggregation in Regulatory Synthesis",
            "Weighted confidence aggregation is essential for synthesizing multi-source regulatory data, enabling robust executive report generation and risk matrix construction.",
            ["aggregation", "confidence", "regulatory"],
            1.1
        ),
        SearchDocument(
            "D3",
            "Cross-Reference Validation Techniques",
            "Cross-reference validation ensures consistency and accuracy across jurisdictional boundaries, supporting hierarchical summarization and authority hierarchy resolution.",
            ["validation", "cross-reference", "jurisdiction"],
            1.0
        ),
        SearchDocument(
            "D4",
            "Hierarchical Summarization for Executive Reporting",
            "Hierarchical summarization enables the condensation of complex multi-domain information into actionable executive reports, tailored for stakeholder-specific formatting.",
            ["summarization", "executive", "hierarchy"],
            1.0
        ),
        SearchDocument(
            "D5",
            "Executive Report Generation Best Practices",
            "Best practices for executive report generation include materiality thresholds, audit trail tracking, and explainability for interpretability.",
            ["report", "executive", "materiality"],
            1.0
        ),
        SearchDocument(
            "D6",
            "Risk Matrix Construction in Cross-Domain Contexts",
            "Constructing risk matrices across domains requires temporal analysis, cross-domain risk aggregation, and regulatory deadline tracking.",
            ["risk", "matrix", "cross-domain"],
            1.1
        ),
        SearchDocument(
            "D7",
            "Temporal Analysis Across Regulatory Domains",
            "Temporal analysis techniques help track regulatory changes, deadlines, and their impact on multi-scenario analysis and continuous synthesis monitoring.",
            ["temporal", "analysis", "regulatory"],
            1.0
        ),
        SearchDocument(
            "D8",
            "Jurisdiction Conflict Detection Algorithms",
            "Algorithms for detecting jurisdiction conflicts leverage authority hierarchy resolution and materiality thresholds to ensure compliance.",
            ["jurisdiction", "conflict", "detection"],
            1.2
        ),
        SearchDocument(
            "D9",
            "Authority Hierarchy Resolution in Synthesis Engines",
            "Resolving authority hierarchies is crucial for federated data integration and regulatory change impact analysis.",
            ["authority", "hierarchy", "resolution"],
            1.0
        ),
        SearchDocument(
            "D10",
            "Materiality Thresholds for Regulatory Reporting",
            "Materiality thresholds define the significance of issues for stakeholder-specific formatting and executive report generation.",
            ["materiality", "threshold", "regulatory"],
            1.1
        ),
        SearchDocument(
            "D11",
            "Stakeholder-Specific Formatting Guidelines",
            "Formatting guidelines ensure that synthesized reports meet the needs of diverse stakeholders, supporting explainability and audit trail tracking.",
            ["stakeholder", "formatting", "guidelines"],
            1.0
        ),
        SearchDocument(
            "D12",
            "Sub-Query Routing to Specialized Engines",
            "Sub-query routing enables efficient delegation of domain-specific queries to specialized engines, improving cross-domain synthesis.",
            ["sub-query", "routing", "specialized"],
            1.0
        ),
        SearchDocument(
            "D13",
            "Cross-Domain Risk Aggregation Methods",
            "Aggregating risks across domains involves uncertainty quantification, error propagation, and explainability.",
            ["risk", "aggregation", "cross-domain"],
            1.1
        ),
        SearchDocument(
            "D14",
            "Conflict of Interest Detection in Synthesis",
            "Detecting conflicts of interest is vital for audit trail and provenance tracking within federated data integration.",
            ["conflict", "interest", "detection"],
            1.0
        ),
        SearchDocument(
            "D15",
            "Regulatory Deadline Tracking Systems",
            "Tracking regulatory deadlines supports temporal analysis and regulatory change impact analysis.",
            ["regulatory", "deadline", "tracking"],
            1.0
        ),
        SearchDocument(
            "D16",
            "Natural Language Query Understanding",
            "Natural language query understanding enhances the usability of synthesis engines, supporting explainability and interpretability.",
            ["natural language", "query", "understanding"],
            1.0
        ),
        SearchDocument(
            "D17",
            "Audit Trail and Provenance Tracking",
            "Audit trails and provenance tracking are essential for transparency, error propagation analysis, and regulatory compliance.",
            ["audit", "provenance", "tracking"],
            1.1
        ),
        SearchDocument(
            "D18",
            "Error Propagation and Uncertainty Quantification",
            "Quantifying uncertainty and tracking error propagation are key for robust multi-scenario analysis and continuous synthesis monitoring.",
            ["error", "uncertainty", "propagation"],
            1.0
        ),
        SearchDocument(
            "D19",
            "Multi-Scenario Analysis in Regulatory Synthesis",
            "Multi-scenario analysis allows for the evaluation of regulatory impacts under varying conditions, supporting explainability.",
            ["multi-scenario", "analysis", "regulatory"],
            1.0
        ),
        SearchDocument(
            "D20",
            "Continuous Synthesis Monitoring Protocols",
            "Protocols for continuous synthesis monitoring ensure up-to-date cross-domain integration and regulatory compliance.",
            ["continuous", "monitoring", "synthesis"],
            1.0
        ),
        SearchDocument(
            "D21",
            "Federated Data Integration Strategies",
            "Federated data integration enables seamless synthesis across domains, supporting conflict resolution and audit trail tracking.",
            ["federated", "data", "integration"],
            1.1
        ),
        SearchDocument(
            "D22",
            "Regulatory Change Impact Analysis",
            "Analyzing the impact of regulatory changes is critical for executive reporting and risk matrix construction.",
            ["regulatory", "change", "impact"],
            1.0
        ),
        SearchDocument(
            "D23",
            "Explainability and Interpretability in Synthesis",
            "Explainability and interpretability are foundational for stakeholder trust and regulatory acceptance.",
            ["explainability", "interpretability", "synthesis"],
            1.0
        ),
        SearchDocument(
            "D24",
            "Weighted Aggregation for Cross-Reference Validation",
            "Weighted aggregation methods enhance cross-reference validation and hierarchical summarization.",
            ["aggregation", "cross-reference", "validation"],
            1.0
        ),
        SearchDocument(
            "D25",
            "Advanced Risk Matrix Construction",
            "Advanced techniques for risk matrix construction include temporal analysis, multi-scenario evaluation, and uncertainty quantification.",
            ["risk", "matrix", "advanced"],
            1.1
        ),
        SearchDocument(
            "D26",
            "SYN01 Cross-Domain Synthesizer Overview",
            "SYN01 is a cross-domain synthesizer engine designed for federated integration, conflict detection, and executive report generation.",
            ["SYN01", "cross-domain", "synthesizer"],
            1.3
        ),
        SearchDocument(
            "D27",
            "Regulatory Synthesis: Error Handling",
            "Error handling in regulatory synthesis involves uncertainty quantification and audit trail management.",
            ["regulatory", "error", "handling"],
            1.0
        ),
        SearchDocument(
            "D28",
            "Materiality and Stakeholder Communication",
            "Materiality thresholds inform stakeholder communication and executive reporting in multi-domain contexts.",
            ["materiality", "stakeholder", "communication"],
            1.0
        ),
        SearchDocument(
            "D29",
            "Scenario-Based Regulatory Impact Assessment",
            "Scenario-based assessments support regulatory change analysis and risk aggregation.",
            ["scenario", "regulatory", "impact"],
            1.0
        ),
        SearchDocument(
            "D30",
            "Provenance Tracking in Federated Synthesis",
            "Tracking provenance in federated synthesis ensures explainability, auditability, and conflict resolution.",
            ["provenance", "federated", "synthesis"],
            1.1
        ),
    ]
    for doc in docs:
        index.add_document(doc)