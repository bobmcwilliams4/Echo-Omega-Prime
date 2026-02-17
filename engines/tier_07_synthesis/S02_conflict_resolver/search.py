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
        self._documents: Dict[int, SearchDocument] = {}
        self._inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_length: float = 0.0
        self._doc_freqs: Dict[str, int] = defaultdict(int)
        self._total_docs: int = 0
        self._lock = threading.RLock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[Tuple[int, str], float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return  # Do not add duplicate IDs
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            token_counts = Counter(tokens)
            self._documents[doc.id] = doc
            self._doc_lengths[doc.id] = len(tokens)
            for token, count in token_counts.items():
                self._inverted_index[token][doc.id] = count
                self._doc_freqs[token] += 1
            self._total_docs += 1
            self._avg_doc_length = sum(self._doc_lengths.values()) / self._total_docs if self._total_docs > 0 else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        with self._lock:
            query_tokens = self._tokenize(query)
            if not query_tokens:
                return []
            doc_scores: Dict[int, float] = defaultdict(float)
            for token in query_tokens:
                idf = self._compute_idf(token)
                for doc_id, tf in self._inverted_index.get(token, {}).items():
                    bm25_score = self._score_bm25(token, doc_id, tf, idf)
                    tfidf_score = self._score_tfidf(token, doc_id, tf, idf)
                    doc_weight = self._documents[doc_id].weight
                    # Combine BM25 and TF-IDF (weighted sum)
                    score = 0.7 * bm25_score + 0.3 * tfidf_score
                    doc_scores[doc_id] += score * doc_weight
            # Rank and prepare results
            ranked_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
            results = []
            for doc_id, score in ranked_docs:
                doc = self._documents[doc_id]
                snippet = self._extract_snippet(doc, query_tokens)
                results.append(SearchResult(doc_id, score, doc.title, snippet))
            return results

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                "total_documents": self._total_docs,
                "average_document_length": self._avg_doc_length,
                "unique_terms": len(self._inverted_index),
            }

    def _tokenize(self, text: str) -> List[str]:
        # Lowercase, remove non-alphanum, split on whitespace
        text = text.lower()
        text = re.sub(r'[^a-z0-9_ ]+', ' ', text)
        tokens = text.split()
        return tokens

    def _compute_idf(self, term: str) -> float:
        # Cached for efficiency
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self._doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self._total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, term: str, doc_id: int, tf: int, idf: float) -> float:
        # BM25 formula
        doc_len = self._doc_lengths.get(doc_id, 0)
        avg_dl = self._avg_doc_length if self._avg_doc_length > 0 else 1.0
        k1 = self._bm25_k1
        b = self._bm25_b
        numerator = tf * (k1 + 1)
        denominator = tf + k1 * (1 - b + b * doc_len / avg_dl)
        return idf * numerator / denominator

    def _score_tfidf(self, term: str, doc_id: int, tf: int, idf: float) -> float:
        # TF-IDF with term frequency normalization
        key = (doc_id, term)
        if key in self._tfidf_cache:
            return self._tfidf_cache[key]
        doc_len = self._doc_lengths.get(doc_id, 1)
        tf_norm = tf / doc_len
        score = tf_norm * idf
        self._tfidf_cache[key] = score
        return score

    def _extract_snippet(self, doc: SearchDocument, query_tokens: List[str]) -> str:
        # Find the first occurrence of any query token in content, return 30 words around
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            return content[:180] + "..." if len(content) > 180 else content
        pos = positions[0]
        start = max(0, pos - 15)
        end = min(len(tokens), pos + 15)
        snippet = " ".join(tokens[start:end])
        return snippet + "..."

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

# --- Pre-seed Domain Documents ---

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Conflict Detection Taxonomy Overview",
            "This document outlines the taxonomy for conflict detection, including types such as factual, normative, and jurisdictional conflicts. It provides definitions and examples for each category.",
            ["taxonomy", "conflict detection", "definitions"],
            1.0
        ),
        SearchDocument(
            2,
            "Resolution by Authority Weight",
            "Resolution by authority weight prioritizes sources based on their recognized authority. The system assigns weights to sources such as legal codes, expert panels, and organizational policies.",
            ["authority", "weight", "resolution"],
            1.2
        ),
        SearchDocument(
            3,
            "Temporal Precedence Rules in Conflict Resolution",
            "Temporal precedence rules resolve conflicts by favoring the most recent or the earliest source, depending on the context. This document details rule hierarchies and exceptions.",
            ["temporal", "precedence", "rules"],
            1.1
        ),
        SearchDocument(
            4,
            "Jurisdictional Override Mechanisms",
            "Jurisdictional override rules allow certain authorities to supersede others based on legal or organizational boundaries. This includes cross-jurisdictional conflict handling.",
            ["jurisdiction", "override", "conflict"],
            1.3
        ),
        SearchDocument(
            5,
            "Majority Voting with Confidence Weighting",
            "Majority voting aggregates multiple sources, weighting each vote by the confidence assigned to the source. This method improves robustness in the presence of unreliable data.",
            ["majority", "voting", "confidence"],
            1.1
        ),
        SearchDocument(
            6,
            "Quantifying Disagreement in Conflict Detection",
            "Disagreement quantification measures the degree of conflict among sources using metrics such as entropy, variance, and pairwise disagreement rates.",
            ["disagreement", "quantification", "metrics"],
            1.0
        ),
        SearchDocument(
            7,
            "Conflict Escalation Triggers",
            "Escalation triggers are predefined conditions under which unresolved conflicts are promoted to higher authority or require human intervention.",
            ["escalation", "triggers", "conflict"],
            1.1
        ),
        SearchDocument(
            8,
            "Source Reliability Rankings",
            "This document describes methods for ranking sources by reliability, including historical accuracy, peer review, and transparency of methodology.",
            ["source", "reliability", "ranking"],
            1.2
        ),
        SearchDocument(
            9,
            "Inter-Engine Correlation Handling",
            "When multiple conflict resolution engines are in use, inter-engine correlation handling ensures consistent outcomes and prevents contradictory resolutions.",
            ["inter-engine", "correlation", "consistency"],
            1.0
        ),
        SearchDocument(
            10,
            "Reconciliation Strategies for Conflicting Data",
            "Reconciliation strategies include negotiation, consensus-building, and algorithmic synthesis to resolve conflicts and produce a unified outcome.",
            ["reconciliation", "strategies", "conflict"],
            1.1
        ),
        SearchDocument(
            11,
            "Factual vs. Normative Conflicts",
            "Distinguishes between factual conflicts (disagreement on facts) and normative conflicts (disagreement on values or rules), with examples and resolution techniques.",
            ["factual", "normative", "conflict"],
            1.0
        ),
        SearchDocument(
            12,
            "Authority Weight Calibration",
            "Describes methods for calibrating authority weights, including expert elicitation, empirical validation, and periodic review.",
            ["authority", "calibration", "weights"],
            1.15
        ),
        SearchDocument(
            13,
            "Temporal Exceptions and Overrides",
            "Explores scenarios where temporal precedence is overridden by other rules, such as emergency directives or retroactive legislation.",
            ["temporal", "exceptions", "override"],
            1.05
        ),
        SearchDocument(
            14,
            "Cross-Jurisdictional Conflict Resolution",
            "Addresses conflicts arising from overlapping jurisdictions and provides frameworks for resolving such disputes.",
            ["cross-jurisdictional", "conflict", "resolution"],
            1.2
        ),
        SearchDocument(
            15,
            "Weighted Majority Voting Algorithms",
            "Details algorithms for implementing weighted majority voting, including handling ties and outlier detection.",
            ["weighted", "majority", "voting"],
            1.1
        ),
        SearchDocument(
            16,
            "Entropy-Based Disagreement Metrics",
            "Introduces entropy-based metrics for quantifying disagreement among multiple sources.",
            ["entropy", "disagreement", "metrics"],
            1.0
        ),
        SearchDocument(
            17,
            "Escalation Pathways and Human-in-the-Loop",
            "Defines escalation pathways and criteria for involving human decision-makers in conflict resolution.",
            ["escalation", "human-in-the-loop", "pathways"],
            1.1
        ),
        SearchDocument(
            18,
            "Reliability Assessment Protocols",
            "Outlines protocols for assessing and updating source reliability rankings over time.",
            ["reliability", "assessment", "protocols"],
            1.2
        ),
        SearchDocument(
            19,
            "Multi-Engine Synchronization",
            "Discusses synchronization mechanisms for maintaining consistency across multiple conflict resolution engines.",
            ["multi-engine", "synchronization", "consistency"],
            1.0
        ),
        SearchDocument(
            20,
            "Consensus-Building Techniques",
            "Presents consensus-building techniques such as Delphi method, iterative negotiation, and hybrid approaches.",
            ["consensus", "negotiation", "techniques"],
            1.1
        ),
        SearchDocument(
            21,
            "Conflict Detection Workflow",
            "Describes the end-to-end workflow for detecting and classifying conflicts in structured and unstructured data.",
            ["workflow", "conflict detection", "classification"],
            1.0
        ),
        SearchDocument(
            22,
            "Authority Hierarchies and Precedence",
            "Explores hierarchical models of authority and their impact on conflict resolution.",
            ["authority", "hierarchies", "precedence"],
            1.2
        ),
        SearchDocument(
            23,
            "Temporal Reasoning in Resolution Engines",
            "Covers temporal reasoning algorithms and their application in conflict resolution engines.",
            ["temporal", "reasoning", "algorithms"],
            1.1
        ),
        SearchDocument(
            24,
            "Jurisdictional Boundaries and Overrides",
            "Analyzes the effect of jurisdictional boundaries on override rules and conflict outcomes.",
            ["jurisdictional", "boundaries", "override"],
            1.15
        ),
        SearchDocument(
            25,
            "Voting Confidence Calibration",
            "Explains how to calibrate confidence weights in majority voting systems for optimal performance.",
            ["voting", "confidence", "calibration"],
            1.1
        ),
        SearchDocument(
            26,
            "Pairwise Disagreement Analysis",
            "Details methods for analyzing pairwise disagreements among sources and their implications.",
            ["pairwise", "disagreement", "analysis"],
            1.0
        ),
        SearchDocument(
            27,
            "Escalation Thresholds and Triggers",
            "Defines thresholds for automatic escalation and the triggers that activate them.",
            ["escalation", "thresholds", "triggers"],
            1.1
        ),
        SearchDocument(
            28,
            "Reliability Ranking Algorithms",
            "Presents algorithms for ranking sources by reliability using statistical and machine learning methods.",
            ["reliability", "ranking", "algorithms"],
            1.2
        ),
        SearchDocument(
            29,
            "Inter-Engine Disagreement Handling",
            "Discusses strategies for handling disagreements between different conflict resolution engines.",
            ["inter-engine", "disagreement", "handling"],
            1.0
        ),
        SearchDocument(
            30,
            "Hybrid Reconciliation Approaches",
            "Explores hybrid approaches that combine algorithmic and human-driven reconciliation strategies.",
            ["hybrid", "reconciliation", "approaches"],
            1.1
        ),
    ]
    for doc in docs:
        index.add_document(doc)